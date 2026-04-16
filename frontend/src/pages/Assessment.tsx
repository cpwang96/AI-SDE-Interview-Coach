import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import Editor from '@monaco-editor/react'
import ReactMarkdown from 'react-markdown'
import { startAssessment, submitAssessment, executeCode } from '../api/client'

export default function Assessment() {
  const navigate = useNavigate()
  const userId = localStorage.getItem('userId')

  const [question, setQuestion] = useState<any>(null)
  const [problem, setProblem] = useState<any>(null)
  const [code, setCode] = useState('')
  const [language, setLanguage] = useState('python')
  const [output, setOutput] = useState<string | null>(null)
  const [running, setRunning] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [evaluation, setEvaluation] = useState<any>(null)
  const [total, setTotal] = useState(0)
  const [completed, setCompleted] = useState(0)
  const [studyPlan, setStudyPlan] = useState<string | null>(null)
  const [overallLevel, setOverallLevel] = useState<string | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    if (!userId) {
      navigate('/onboarding')
      return
    }
    startAssessment(userId).then(res => {
      if (res.message) {
        // Assessment already done
        setStudyPlan(res.results?.study_plan || 'Assessment complete.')
        setOverallLevel(res.results?.overall_level || null)
      } else {
        setQuestion(res.question)
        setProblem(res.current_problem)
        setCode(res.question.starter_code[language] || '')
        setTotal(res.total_problems)
        setCompleted(res.completed_count)
      }
      setLoading(false)
    }).catch(() => setLoading(false))
  }, [])

  const handleRun = async () => {
    setRunning(true)
    setOutput(null)
    try {
      const res = await executeCode(code, language)
      let out = res.stdout || ''
      if (res.stderr) out += (out ? '\n' : '') + res.stderr
      if (!out) out = res.exit_code === 0 ? '(no output)' : `Exit code: ${res.exit_code}`
      if (res.time_ms) out += `\n--- ${res.time_ms}ms ---`
      setOutput(out)
    } catch {
      setOutput('Error running code')
    }
    setRunning(false)
  }

  const handleSubmit = async () => {
    if (!userId || !problem) return
    setSubmitting(true)
    setEvaluation(null)
    try {
      const res = await submitAssessment(userId, problem.question_id, code, language)
      setEvaluation(res.evaluation)
      setCompleted(res.completed_count)
      setTotal(res.total_problems)

      if (res.assessment_complete) {
        setStudyPlan(res.study_plan)
        setOverallLevel(res.overall_level)
        setQuestion(null)
      } else if (res.next_question) {
        // Queue next problem — user clicks "Next" to proceed
        setQuestion(res.next_question)
        setProblem(res.next_problem)
      }
    } catch {
      setEvaluation({ score: 0, evaluation: 'Error submitting. Try again.' })
    }
    setSubmitting(false)
  }

  const handleNext = () => {
    if (question) {
      setCode(question.starter_code[language] || '')
      setOutput(null)
      setEvaluation(null)
    }
  }

  if (loading) {
    return (
      <div style={{ height: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <p style={{ color: 'var(--text-secondary)' }}>Loading assessment...</p>
      </div>
    )
  }

  // Assessment complete — show study plan
  if (studyPlan) {
    return (
      <div style={{ height: '100vh', overflowY: 'auto', padding: '40px 20px' }}>
        <div style={{ maxWidth: 800, margin: '0 auto' }}>
          <h1 style={{ fontSize: 28, fontWeight: 700, marginBottom: 8 }}>Assessment Complete!</h1>
          {overallLevel && (
            <p style={{
              fontSize: 18,
              marginBottom: 24,
              color: overallLevel === 'advanced' ? 'var(--green)' : overallLevel === 'intermediate' ? 'var(--yellow)' : 'var(--red)',
            }}>
              Level: {overallLevel.charAt(0).toUpperCase() + overallLevel.slice(1)}
            </p>
          )}
          <div style={{
            background: 'var(--bg-surface)',
            padding: 24,
            borderRadius: 12,
            lineHeight: 1.7,
          }}>
            <h2 style={{ marginBottom: 16 }}>Your Personalized Study Plan</h2>
            <ReactMarkdown>{studyPlan}</ReactMarkdown>
          </div>
          <button
            onClick={() => navigate('/')}
            style={{
              marginTop: 24,
              background: 'var(--accent)',
              color: 'var(--bg-primary)',
              padding: '12px 32px',
              fontWeight: 600,
              fontSize: 15,
            }}
          >
            Start Practicing
          </button>
        </div>
      </div>
    )
  }

  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column' }}>
      {/* Header */}
      <div style={{
        padding: '10px 20px',
        borderBottom: '1px solid var(--border)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        background: 'var(--bg-secondary)',
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 16 }}>
          <h2 style={{ fontSize: 16, fontWeight: 600 }}>Skill Assessment</h2>
          {question && (
            <>
              <span style={{ fontSize: 14, color: 'var(--text-secondary)' }}>
                {question.title}
              </span>
              <span style={{
                fontSize: 12,
                fontWeight: 600,
                color: question.difficulty === 'easy' ? 'var(--green)' : question.difficulty === 'medium' ? 'var(--yellow)' : 'var(--red)',
              }}>
                {question.difficulty}
              </span>
            </>
          )}
        </div>
        <div style={{ fontSize: 13, color: 'var(--text-muted)' }}>
          Problem {completed + (evaluation ? 0 : 1)} of {total}
        </div>
      </div>

      {/* Progress bar */}
      <div style={{ height: 3, background: 'var(--bg-surface)' }}>
        <div style={{
          height: '100%',
          width: `${(completed / total) * 100}%`,
          background: 'var(--accent)',
          transition: 'width 0.3s ease',
        }} />
      </div>

      <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>
        {/* Left: Problem + Editor */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', borderRight: '1px solid var(--border)' }}>
          {question && (
            <div style={{
              padding: 16,
              borderBottom: '1px solid var(--border)',
              maxHeight: 220,
              overflowY: 'auto',
              fontSize: 14,
              lineHeight: 1.6,
            }}>
              <p style={{ whiteSpace: 'pre-wrap' }}>{question.description}</p>
              <div style={{ marginTop: 12 }}>
                {question.examples.map((ex: any, i: number) => (
                  <div key={i} style={{ background: 'var(--bg-surface)', padding: 10, borderRadius: 6, marginBottom: 8, fontSize: 13 }}>
                    <div><strong>Input:</strong> {ex.input}</div>
                    <div><strong>Output:</strong> {ex.output}</div>
                    {ex.explanation && <div style={{ color: 'var(--text-muted)' }}>{ex.explanation}</div>}
                  </div>
                ))}
              </div>
            </div>
          )}

          {/* Editor */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', padding: '8px 12px', borderBottom: '1px solid var(--border)', background: 'var(--bg-secondary)' }}>
            <select
              value={language}
              onChange={e => {
                setLanguage(e.target.value)
                if (question?.starter_code[e.target.value]) setCode(question.starter_code[e.target.value])
              }}
              style={{ padding: '4px 8px', fontSize: 13 }}
            >
              <option value="python">Python</option>
              <option value="javascript">JavaScript</option>
            </select>
            <div style={{ display: 'flex', gap: 8 }}>
              <button
                onClick={handleRun}
                disabled={running}
                style={{ background: 'var(--bg-surface)', color: 'var(--text-primary)', fontSize: 13, opacity: running ? 0.5 : 1 }}
              >
                {running ? 'Running...' : 'Run'}
              </button>
              <button
                onClick={handleSubmit}
                disabled={submitting || !!evaluation}
                style={{ background: 'var(--green)', color: 'var(--bg-primary)', fontWeight: 600, fontSize: 13, opacity: submitting || evaluation ? 0.5 : 1 }}
              >
                {submitting ? 'Evaluating...' : 'Submit'}
              </button>
            </div>
          </div>

          <div style={{ flex: 1 }}>
            <Editor
              height="100%"
              language={language}
              value={code}
              onChange={v => setCode(v || '')}
              theme="vs-dark"
              options={{ fontSize: 14, minimap: { enabled: false }, scrollBeyondLastLine: false, padding: { top: 12 }, tabSize: 4, automaticLayout: true }}
            />
          </div>

          {output !== null && (
            <div style={{ borderTop: '1px solid var(--border)', background: 'var(--bg-secondary)', padding: 12, maxHeight: 120, overflowY: 'auto' }}>
              <div style={{ fontSize: 11, color: 'var(--text-muted)', marginBottom: 4 }}>Output</div>
              <pre style={{ fontSize: 13, whiteSpace: 'pre-wrap', fontFamily: 'monospace' }}>{output}</pre>
            </div>
          )}
        </div>

        {/* Right: Evaluation panel */}
        <div style={{ width: 350, padding: 20, overflowY: 'auto' }}>
          {!evaluation && !submitting && (
            <div style={{ color: 'var(--text-secondary)', fontSize: 14, lineHeight: 1.7 }}>
              <h3 style={{ color: 'var(--text-primary)', marginBottom: 12 }}>Assessment Mode</h3>
              <p>Solve this problem to the best of your ability. The AI coach will evaluate your solution.</p>
              <p style={{ marginTop: 12 }}>Tips:</p>
              <ul style={{ paddingLeft: 20, marginTop: 4 }}>
                <li>Use "Run" to test your code first</li>
                <li>Click "Submit" when you're ready for evaluation</li>
                <li>Think about time & space complexity</li>
                <li>Handle edge cases</li>
              </ul>
            </div>
          )}

          {submitting && (
            <div style={{ color: 'var(--text-muted)', fontSize: 14 }}>
              Claude is evaluating your solution...
            </div>
          )}

          {evaluation && (
            <div>
              <h3 style={{ marginBottom: 12 }}>Evaluation</h3>
              <div style={{
                fontSize: 36,
                fontWeight: 700,
                color: evaluation.score >= 70 ? 'var(--green)' : evaluation.score >= 40 ? 'var(--yellow)' : 'var(--red)',
                marginBottom: 12,
              }}>
                {evaluation.score}/100
              </div>
              <p style={{ fontSize: 14, lineHeight: 1.6, color: 'var(--text-secondary)' }}>
                {evaluation.evaluation}
              </p>
              <button
                onClick={handleNext}
                style={{
                  marginTop: 24,
                  width: '100%',
                  background: 'var(--accent)',
                  color: 'var(--bg-primary)',
                  padding: '12px',
                  fontWeight: 600,
                }}
              >
                {completed >= total ? 'See Study Plan' : 'Next Problem'}
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
