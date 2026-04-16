import { useState, useEffect, useRef, useCallback } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import CodeEditor from '../components/CodeEditor'
import ChatPanel from '../components/ChatPanel'
import { startCodingSession, sendCodingMessage, executeCode, submitSolution, getLatestSubmission } from '../api/client'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

function useResizable(initialPct: number, direction: 'horizontal' | 'vertical', containerRef: React.RefObject<HTMLDivElement | null>) {
  const [pct, setPct] = useState(initialPct)
  const dragging = useRef(false)

  const onMouseDown = useCallback((e: React.MouseEvent) => {
    e.preventDefault()
    dragging.current = true

    const onMouseMove = (ev: MouseEvent) => {
      if (!dragging.current || !containerRef.current) return
      const rect = containerRef.current.getBoundingClientRect()
      let newPct: number
      if (direction === 'horizontal') {
        newPct = ((ev.clientX - rect.left) / rect.width) * 100
      } else {
        newPct = ((ev.clientY - rect.top) / rect.height) * 100
      }
      setPct(Math.min(80, Math.max(15, newPct)))
    }

    const onMouseUp = () => {
      dragging.current = false
      document.removeEventListener('mousemove', onMouseMove)
      document.removeEventListener('mouseup', onMouseUp)
      document.body.style.cursor = ''
      document.body.style.userSelect = ''
    }

    document.body.style.cursor = direction === 'horizontal' ? 'col-resize' : 'row-resize'
    document.body.style.userSelect = 'none'
    document.addEventListener('mousemove', onMouseMove)
    document.addEventListener('mouseup', onMouseUp)
  }, [direction, containerRef])

  return { pct, onMouseDown }
}

function formatQuestionMd(question: any): string {
  let md = `${question.description}\n\n`
  md += `### Examples\n\n`
  for (const [i, ex] of (question.examples || []).entries()) {
    md += `**Example ${i + 1}:**\n\n`
    md += `\`\`\`\nInput: ${ex.input}\nOutput: ${ex.output}\n\`\`\`\n\n`
    if (ex.explanation) md += `> ${ex.explanation}\n\n`
  }
  const constraints = question.constraints || []
  if (constraints.length > 0) {
    md += `### Constraints\n\n`
    for (const c of constraints) {
      md += `- \`${c}\`\n`
    }
  }
  return md
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
  const [coachOpen, setCoachOpen] = useState(false)
  const [unreadCoach, setUnreadCoach] = useState(0)

  const mainRef = useRef<HTMLDivElement>(null)
  const leftRef = useRef<HTMLDivElement>(null)

  const hResize = useResizable(45, 'horizontal', mainRef)
  const vResize = useResizable(35, 'vertical', leftRef)

  useEffect(() => {
    startCodingSession(questionId).then(async (res) => {
      setSessionId(res.session_id)
      setQuestion(res.question)
      setMessages([{ role: 'assistant', content: res.coach_message }])

      if (res.question.id) {
        try {
          const sub = await getLatestSubmission(res.question.id)
          if (sub?.code) {
            setCode(sub.code)
            if (sub.language) setLanguage(sub.language)
            setInitializing(false)
            return
          }
        } catch {}
      }
      setCode(res.question.starter_code?.[language] || '')
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
      if (!coachOpen) setUnreadCoach(prev => prev + 1)
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

      if (res.all_passed) {
        const msg = `I passed all ${res.total} test cases! Please review my solution for code quality, time/space complexity, and suggest any optimizations.`
        setMessages(prev => [...prev, { role: 'user', content: `Submitted — ${res.passed}/${res.total} tests passed` }])
        setLoading(true)
        if (!coachOpen) setUnreadCoach(prev => prev + 1)
        try {
          const coachRes = await sendCodingMessage(sessionId, msg, code, language)
          setMessages(prev => [...prev, { role: 'assistant', content: coachRes.response }])
          if (!coachOpen) setUnreadCoach(prev => prev + 1)
        } catch {}
        setLoading(false)
      } else if (res.total > 0) {
        setMessages(prev => [...prev, {
          role: 'assistant',
          content: `**${res.passed}/${res.total} tests passed.** Check the output panel for details. Keep working on it, or ask me for a hint!`
        }])
        if (!coachOpen) setUnreadCoach(prev => prev + 1)
      }
    } catch {
      setOutput('Error submitting solution')
    }
    setSubmitting(false)
  }

  const toggleCoach = () => {
    setCoachOpen(prev => !prev)
    if (!coachOpen) setUnreadCoach(0)
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
        padding: '8px 16px',
        borderBottom: '1px solid var(--border)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        background: 'var(--bg-secondary)',
        flexShrink: 0,
      }}>
        <div style={{ display: 'flex', alignItems: 'center', gap: 12 }}>
          <button
            onClick={() => navigate('/')}
            style={{ background: 'var(--bg-surface)', color: 'var(--text-primary)', fontSize: 13, padding: '5px 12px' }}
          >
            Back
          </button>
          {question && (
            <>
              <h2 style={{ fontSize: 15, fontWeight: 600 }}>{question.title}</h2>
              <span style={{
                fontSize: 11,
                fontWeight: 600,
                padding: '2px 8px',
                borderRadius: 4,
                color: question.difficulty === 'easy' ? 'var(--green)' : question.difficulty === 'medium' ? 'var(--yellow)' : 'var(--red)',
                background: question.difficulty === 'easy' ? 'rgba(34,197,94,0.1)' : question.difficulty === 'medium' ? 'rgba(234,179,8,0.1)' : 'rgba(239,68,68,0.1)',
              }}>
                {question.difficulty}
              </span>
              {question.tags?.slice(0, 3).map((t: string) => (
                <span key={t} style={{ fontSize: 10, color: 'var(--text-muted)', background: 'var(--bg-surface)', padding: '2px 6px', borderRadius: 4 }}>
                  {t}
                </span>
              ))}
            </>
          )}
        </div>
        <button
          onClick={toggleCoach}
          style={{
            background: coachOpen ? 'var(--accent)' : 'var(--bg-surface)',
            color: coachOpen ? '#fff' : 'var(--text-primary)',
            fontSize: 13,
            fontWeight: 600,
            padding: '5px 14px',
            position: 'relative',
          }}
        >
          Coach
          {unreadCoach > 0 && !coachOpen && (
            <span style={{
              position: 'absolute',
              top: -6,
              right: -6,
              width: 18,
              height: 18,
              borderRadius: '50%',
              background: 'var(--red)',
              color: '#fff',
              fontSize: 10,
              fontWeight: 700,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}>
              {unreadCoach}
            </span>
          )}
        </button>
      </div>

      {/* Main content */}
      <div ref={mainRef} style={{ flex: 1, display: 'flex', overflow: 'hidden', position: 'relative' }}>
        {/* Left panel: Question (top) + Editor (bottom), split vertically */}
        <div
          ref={leftRef}
          style={{
            width: coachOpen ? `calc(100% - 400px)` : '100%',
            display: 'flex',
            flexDirection: 'column',
            transition: coachOpen ? 'width 0.2s ease' : 'none',
          }}
        >
          {/* Question panel */}
          {question && (
            <div style={{
              height: `${vResize.pct}%`,
              overflowY: 'auto',
              padding: '16px 20px',
              fontSize: 14,
              lineHeight: 1.7,
              borderBottom: 'none',
              flexShrink: 0,
            }}>
              <div className="markdown-body" style={{ maxWidth: 800 }}>
                <ReactMarkdown>{formatQuestionMd(question)}</ReactMarkdown>
              </div>
            </div>
          )}

          {/* Vertical resize handle */}
          <div
            onMouseDown={vResize.onMouseDown}
            style={{
              height: 6,
              cursor: 'row-resize',
              background: 'var(--border)',
              flexShrink: 0,
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
            }}
          >
            <div style={{ width: 40, height: 2, borderRadius: 1, background: 'var(--text-muted)', opacity: 0.5 }} />
          </div>

          {/* Editor + output */}
          <div style={{ flex: 1, display: 'flex', flexDirection: 'column', minHeight: 0 }}>
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
              flexShrink: 0,
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

        {/* Coach flyout panel */}
        <div style={{
          width: coachOpen ? 400 : 0,
          overflow: 'hidden',
          transition: 'width 0.2s ease',
          borderLeft: coachOpen ? '1px solid var(--border)' : 'none',
          flexShrink: 0,
        }}>
          {coachOpen && (
            <div style={{ width: 400, height: '100%' }}>
              <ChatPanel
                messages={messages}
                onSend={handleSend}
                loading={loading}
                placeholder="Ask for a hint, discuss approach..."
              />
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
