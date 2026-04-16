import { useState, useEffect } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import CodeEditor from '../components/CodeEditor'
import ChatPanel from '../components/ChatPanel'
import { startCodingSession, sendCodingMessage, executeCode, submitSolution } from '../api/client'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

export default function CodingSession() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const questionId = searchParams.get('id') || undefined

  const [sessionId, setSessionId] = useState<string | null>(null)
  const [question, setQuestion] = useState<any>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [code, setCode] = useState('')
  const [language, setLanguage] = useState('python')
  const [output, setOutput] = useState<string | null>(null)
  const [loading, setLoading] = useState(false)
  const [running, setRunning] = useState(false)
  const [submitting, setSubmitting] = useState(false)
  const [submitResult, setSubmitResult] = useState<any>(null)
  const [initializing, setInitializing] = useState(true)

  useEffect(() => {
    startCodingSession(questionId).then(res => {
      setSessionId(res.session_id)
      setQuestion(res.question)
      setCode(res.question.starter_code?.[language] || '')
      setMessages([{ role: 'assistant', content: res.coach_message }])
      setInitializing(false)
    }).catch(() => setInitializing(false))
  }, [])

  const handleLanguageChange = (lang: string) => {
    setLanguage(lang)
    if (question?.starter_code?.[lang]) {
      setCode(question.starter_code[lang])
    }
  }

  const handleSend = async (message: string) => {
    if (!sessionId) return
    setMessages(prev => [...prev, { role: 'user', content: message }])
    setLoading(true)
    try {
      const res = await sendCodingMessage(sessionId, message, code, language)
      setMessages(prev => [...prev, { role: 'assistant', content: res.response }])
    } catch {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Error communicating with coach. Please try again.' }])
    }
    setLoading(false)
  }

  const handleRun = async () => {
    setRunning(true)
    setOutput(null)
    setSubmitResult(null)
    try {
      const res = await executeCode(code, language)
      let out = ''
      if (res.stdout) out += res.stdout
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
    if (!sessionId || !question) return
    setSubmitting(true)
    setOutput(null)
    setSubmitResult(null)
    try {
      const res = await submitSolution(sessionId, code, language, question.id)
      setSubmitResult(res)
      setOutput(res.stdout + (res.stderr ? '\n' + res.stderr : ''))

      // Auto-send results to coach for feedback if all passed
      if (res.all_passed) {
        const msg = `I passed all ${res.total} test cases! Please review my solution for code quality, time/space complexity, and suggest any optimizations.`
        setMessages(prev => [...prev, { role: 'user', content: `Submitted — ${res.passed}/${res.total} tests passed` }])
        setLoading(true)
        try {
          const coachRes = await sendCodingMessage(sessionId, msg, code, language)
          setMessages(prev => [...prev, { role: 'assistant', content: coachRes.response }])
        } catch {}
        setLoading(false)
      } else if (res.total > 0) {
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: `**${res.passed}/${res.total} tests passed.** Check the output panel for details. Keep working on it, or ask me for a hint!`
        }])
      }
    } catch {
      setOutput('Error submitting solution')
    }
    setSubmitting(false)
  }

  if (initializing) {
    return (
      <div style={{ height: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <p style={{ color: 'var(--text-secondary)' }}>Starting session...</p>
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
        gap: 16,
        background: 'var(--bg-secondary)',
      }}>
        <button
          onClick={() => navigate('/')}
          style={{ background: 'var(--bg-surface)', color: 'var(--text-primary)', fontSize: 13 }}
        >
          Back
        </button>
        {question && (
          <>
            <h2 style={{ fontSize: 16, fontWeight: 600 }}>{question.title}</h2>
            <span style={{
              fontSize: 12,
              fontWeight: 600,
              color: question.difficulty === 'easy' ? 'var(--green)' : question.difficulty === 'medium' ? 'var(--yellow)' : 'var(--red)',
            }}>
              {question.difficulty}
            </span>
            {question.tags?.map((t: string) => (
              <span key={t} style={{ fontSize: 11, color: 'var(--text-muted)', background: 'var(--bg-surface)', padding: '2px 8px', borderRadius: 4 }}>
                {t}
              </span>
            ))}
          </>
        )}
      </div>

      {/* Main layout */}
      <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>
        {/* Left: Problem + Code Editor */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', borderRight: '1px solid var(--border)' }}>
          {question && (
            <div style={{
              padding: 16,
              borderBottom: '1px solid var(--border)',
              maxHeight: 200,
              overflowY: 'auto',
              fontSize: 14,
              lineHeight: 1.6,
            }}>
              <p style={{ whiteSpace: 'pre-wrap' }}>{question.description}</p>
              <div style={{ marginTop: 12 }}>
                {question.examples?.map((ex: any, i: number) => (
                  <div key={i} style={{ background: 'var(--bg-surface)', padding: 10, borderRadius: 6, marginBottom: 8, fontSize: 13 }}>
                    <div><strong>Input:</strong> {ex.input}</div>
                    <div><strong>Output:</strong> {ex.output}</div>
                    {ex.explanation && <div style={{ color: 'var(--text-muted)' }}>{ex.explanation}</div>}
                  </div>
                ))}
              </div>
            </div>
          )}
          <div style={{ flex: 1 }}>
            <CodeEditor
              code={code}
              language={language}
              onChange={setCode}
              onLanguageChange={handleLanguageChange}
              onRun={handleRun}
              onSubmit={handleSubmit}
              output={output}
              running={running}
              submitting={submitting}
            />
          </div>

          {/* Submit result banner */}
          {submitResult && (
            <div style={{
              padding: '8px 16px',
              background: submitResult.all_passed ? 'var(--green)' : 'var(--red)',
              color: 'var(--bg-primary)',
              fontWeight: 600,
              fontSize: 14,
              display: 'flex',
              justifyContent: 'space-between',
            }}>
              <span>
                {submitResult.all_passed
                  ? `All ${submitResult.total} tests passed!`
                  : `${submitResult.passed}/${submitResult.total} tests passed`
                }
              </span>
              {submitResult.time_ms && <span>{submitResult.time_ms}ms</span>}
            </div>
          )}
        </div>

        {/* Right: Chat */}
        <div style={{ width: 420, minWidth: 350 }}>
          <ChatPanel
            messages={messages}
            onSend={handleSend}
            loading={loading}
            placeholder="Ask for a hint, discuss approach..."
          />
        </div>
      </div>
    </div>
  )
}
