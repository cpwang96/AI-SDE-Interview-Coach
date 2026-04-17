import { useState, useEffect, useRef, useCallback } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import CodeEditor from '../components/CodeEditor'
import ChatPanel from '../components/ChatPanel'
import {
  startCodingSession, sendCodingMessage, executeCode,
  submitSolution, getLatestSubmission, getQuestions,
} from '../api/client'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

// ─── Resizable split hook ─────────────────────────────────────────────────────
function useResizable(
  initialPct: number,
  direction: 'horizontal' | 'vertical',
  containerRef: React.RefObject<HTMLDivElement | null>,
  min = 15,
  max = 80,
) {
  const [pct, setPct] = useState(initialPct)
  const dragging = useRef(false)

  const onMouseDown = useCallback((e: React.MouseEvent) => {
    e.preventDefault()
    dragging.current = true

    const onMouseMove = (ev: MouseEvent) => {
      if (!dragging.current || !containerRef.current) return
      const rect = containerRef.current.getBoundingClientRect()
      const newPct = direction === 'horizontal'
        ? ((ev.clientX - rect.left) / rect.width) * 100
        : ((ev.clientY - rect.top) / rect.height) * 100
      setPct(Math.min(max, Math.max(min, newPct)))
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

// ─── Timer hook ───────────────────────────────────────────────────────────────
function useTimer() {
  const [totalSeconds, setTotalSeconds] = useState(0)   // chosen duration
  const [remaining, setRemaining]       = useState(0)   // counts down
  const [running, setRunning]           = useState(false)
  const [expired, setExpired]           = useState(false)
  const intervalRef = useRef<ReturnType<typeof setInterval> | null>(null)

  const start = useCallback((minutes: number) => {
    const secs = minutes * 60
    setTotalSeconds(secs)
    setRemaining(secs)
    setRunning(true)
    setExpired(false)
  }, [])

  const pause = useCallback(() => setRunning(false), [])
  const resume = useCallback(() => { if (remaining > 0) setRunning(true) }, [remaining])
  const reset = useCallback(() => {
    setRunning(false)
    setExpired(false)
    setTotalSeconds(0)
    setRemaining(0)
  }, [])

  useEffect(() => {
    if (!running) {
      if (intervalRef.current) clearInterval(intervalRef.current)
      return
    }
    intervalRef.current = setInterval(() => {
      setRemaining(prev => {
        if (prev <= 1) {
          setRunning(false)
          setExpired(true)
          return 0
        }
        return prev - 1
      })
    }, 1000)
    return () => { if (intervalRef.current) clearInterval(intervalRef.current) }
  }, [running])

  const elapsed = totalSeconds - remaining

  return { totalSeconds, remaining, elapsed, running, expired, start, pause, resume, reset }
}

function formatTime(s: number) {
  const m = Math.floor(Math.abs(s) / 60)
  const sec = Math.abs(s) % 60
  return `${m}:${sec.toString().padStart(2, '0')}`
}

// ─── Question formatter ───────────────────────────────────────────────────────
function formatQuestionMd(question: any): string {
  let md = `${question.description}\n\n`
  md += `### Examples\n\n`
  for (const [i, ex] of (question.examples || []).entries()) {
    md += `**Example ${i + 1}:**\n\`\`\`\nInput:  ${ex.input}\nOutput: ${ex.output}\n\`\`\`\n`
    if (ex.explanation) md += `> ${ex.explanation}\n\n`
    else md += '\n'
  }
  const constraints = question.constraints || []
  if (constraints.length > 0) {
    md += `### Constraints\n\n`
    for (const c of constraints) md += `- \`${c}\`\n`
  }
  return md
}

// ─── Main component ───────────────────────────────────────────────────────────
export default function CodingSession() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const questionId = searchParams.get('id') || undefined

  const [sessionId, setSessionId]       = useState<string | null>(null)
  const [question, setQuestion]         = useState<any>(null)
  const [allQuestions, setAllQuestions] = useState<any[]>([])
  const [messages, setMessages]         = useState<Message[]>([])
  const [code, setCode]                 = useState('')
  const [language, setLanguage]         = useState('java')
  const [output, setOutput]             = useState<string | null>(null)
  const [loading, setLoading]           = useState(false)
  const [running, setRunning]           = useState(false)
  const [submitting, setSubmitting]     = useState(false)
  const [submitResult, setSubmitResult] = useState<any>(null)
  const [initializing, setInitializing] = useState(true)
  const [coachOpen, setCoachOpen]       = useState(false)
  const [unreadCoach, setUnreadCoach]   = useState(0)

  // Timer
  const timer = useTimer()
  const [showDurationPicker, setShowDurationPicker] = useState(false)
  const DURATIONS = [20, 30, 45, 60]

  const mainRef = useRef<HTMLDivElement>(null)
  const leftRef = useRef<HTMLDivElement>(null)

  const hResize = useResizable(45, 'horizontal', mainRef)
  const vResize = useResizable(38, 'vertical', leftRef, 20, 60)

  // Init session + prefetch question list
  useEffect(() => {
    getQuestions().then(qs => setAllQuestions(qs)).catch(() => {})

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

  // Pause timer automatically when all tests pass
  useEffect(() => {
    if (submitResult?.all_passed && timer.running) timer.pause()
  }, [submitResult])

  const handleLanguageChange = (lang: string) => {
    setLanguage(lang)
    if (question?.starter_code?.[lang]) setCode(question.starter_code[lang])
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
    } catch {
      setOutput('Error submitting solution')
    }
    setSubmitting(false)
  }

  // Pick a random question (prefer same difficulty, exclude current)
  const handleNext = useCallback(() => {
    if (allQuestions.length === 0) { navigate('/'); return }
    const sameDiff = allQuestions.filter(
      q => q.id !== question?.id && q.difficulty === question?.difficulty
    )
    const pool = sameDiff.length > 0 ? sameDiff : allQuestions.filter(q => q.id !== question?.id)
    const next = pool[Math.floor(Math.random() * pool.length)]
    if (next) navigate(`/coding?id=${next.id}`)
  }, [allQuestions, question, navigate])

  const toggleCoach = () => {
    setCoachOpen(prev => !prev)
    if (!coachOpen) setUnreadCoach(0)
  }

  // ─── Timer display ──────────────────────────────────────────────────────────
  const timerColor = timer.expired
    ? 'var(--red)'
    : timer.remaining <= 300 && timer.totalSeconds > 0
      ? 'var(--red)'
      : timer.remaining <= 600 && timer.totalSeconds > 0
        ? 'var(--yellow)'
        : 'var(--text-muted)'

  const TimerWidget = () => {
    if (!timer.totalSeconds) {
      // Not started yet — show start button
      return (
        <div style={{ position: 'relative' }}>
          <button
            onClick={() => setShowDurationPicker(p => !p)}
            style={{
              background: 'var(--bg-surface)',
              color: 'var(--text-muted)',
              fontSize: 12,
              padding: '4px 10px',
              display: 'flex',
              alignItems: 'center',
              gap: 5,
            }}
          >
            ⏱ Start Timer
          </button>
          {showDurationPicker && (
            <div style={{
              position: 'absolute',
              top: '100%',
              right: 0,
              marginTop: 4,
              background: 'var(--bg-secondary)',
              border: '1px solid var(--border)',
              borderRadius: 6,
              padding: 6,
              display: 'flex',
              gap: 4,
              zIndex: 100,
              boxShadow: '0 4px 12px rgba(0,0,0,0.3)',
            }}>
              {DURATIONS.map(d => (
                <button
                  key={d}
                  onClick={() => { timer.start(d); setShowDurationPicker(false) }}
                  style={{
                    background: 'var(--bg-surface)',
                    color: 'var(--text-primary)',
                    fontSize: 12,
                    padding: '4px 10px',
                    borderRadius: 4,
                    fontWeight: 500,
                  }}
                >
                  {d}m
                </button>
              ))}
            </div>
          )}
        </div>
      )
    }

    return (
      <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
        <span style={{
          fontFamily: 'monospace',
          fontSize: 14,
          fontWeight: 700,
          color: timerColor,
          minWidth: 48,
          letterSpacing: '0.05em',
        }}>
          {timer.expired ? '⏰ 0:00' : `⏱ ${formatTime(timer.remaining)}`}
        </span>
        {/* pause/resume */}
        {!timer.expired && (
          <button
            onClick={timer.running ? timer.pause : timer.resume}
            style={{ background: 'none', color: 'var(--text-muted)', fontSize: 11, padding: '2px 6px' }}
            title={timer.running ? 'Pause' : 'Resume'}
          >
            {timer.running ? '⏸' : '▶'}
          </button>
        )}
        {/* reset */}
        <button
          onClick={timer.reset}
          style={{ background: 'none', color: 'var(--text-muted)', fontSize: 11, padding: '2px 4px' }}
          title="Reset timer"
        >
          ✕
        </button>
        {/* solved time badge */}
        {submitResult?.all_passed && (
          <span style={{ fontSize: 11, color: 'var(--green)', fontWeight: 600 }}>
            Solved in {formatTime(timer.elapsed)}
          </span>
        )}
      </div>
    )
  }

  // ─── Loading state ──────────────────────────────────────────────────────────
  if (initializing) {
    return (
      <div style={{ height: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
        <p style={{ color: 'var(--text-secondary)' }}>Starting session...</p>
      </div>
    )
  }

  // ─── Main render ────────────────────────────────────────────────────────────
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
        {/* Left: back + title + tags */}
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
                fontSize: 11, fontWeight: 600, padding: '2px 8px', borderRadius: 4,
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

        {/* Right: timer + next + coach */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <TimerWidget />
          <button
            onClick={handleNext}
            title="Random question (same difficulty)"
            style={{ background: 'var(--bg-surface)', color: 'var(--text-muted)', fontSize: 12, padding: '4px 10px' }}
          >
            Next →
          </button>
          <button
            onClick={toggleCoach}
            style={{
              background: coachOpen ? 'var(--accent)' : 'var(--bg-surface)',
              color: coachOpen ? '#fff' : 'var(--text-primary)',
              fontSize: 13, fontWeight: 600, padding: '5px 14px', position: 'relative',
            }}
          >
            Coach
            {unreadCoach > 0 && !coachOpen && (
              <span style={{
                position: 'absolute', top: -6, right: -6, width: 18, height: 18,
                borderRadius: '50%', background: 'var(--red)', color: '#fff',
                fontSize: 10, fontWeight: 700, display: 'flex', alignItems: 'center', justifyContent: 'center',
              }}>
                {unreadCoach}
              </span>
            )}
          </button>
        </div>
      </div>

      {/* Main content */}
      <div ref={mainRef} style={{ flex: 1, display: 'flex', overflow: 'hidden', position: 'relative' }}>
        {/* Left panel: Question (top) + Editor (bottom) */}
        <div
          ref={leftRef}
          style={{
            width: coachOpen ? 'calc(100% - 400px)' : '100%',
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
              height: 6, cursor: 'row-resize', background: 'var(--border)',
              flexShrink: 0, display: 'flex', alignItems: 'center', justifyContent: 'center',
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
              onNext={handleNext}
              output={output}
              running={running}
              submitting={submitting}
              submitResult={submitResult}
            />
          </div>
        </div>

        {/* Coach flyout */}
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
