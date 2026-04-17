import { useState, useEffect, useRef, useCallback } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import CodeEditor from '../components/CodeEditor'
import ChatPanel from '../components/ChatPanel'
import {
  startCodingSession, sendCodingMessage, executeCode,
  submitSolution, getLatestSubmission, getQuestions, markQuestionComplete,
  getNote, saveNote,
} from '../api/client'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

// ─── Horizontal resize ────────────────────────────────────────────────────────
function useHorizontalResize(
  initialPct: number,
  containerRef: React.RefObject<HTMLDivElement | null>,
  min = 25,
  max = 60,
) {
  const [pct, setPct] = useState(initialPct)
  const dragging = useRef(false)

  const onMouseDown = useCallback((e: React.MouseEvent) => {
    e.preventDefault()
    dragging.current = true
    document.body.style.cursor = 'col-resize'
    document.body.style.userSelect = 'none'

    const onMouseMove = (ev: MouseEvent) => {
      if (!dragging.current || !containerRef.current) return
      const rect = containerRef.current.getBoundingClientRect()
      const newPct = ((ev.clientX - rect.left) / rect.width) * 100
      setPct(Math.min(max, Math.max(min, newPct)))
    }
    const onMouseUp = () => {
      dragging.current = false
      document.removeEventListener('mousemove', onMouseMove)
      document.removeEventListener('mouseup', onMouseUp)
      document.body.style.cursor = ''
      document.body.style.userSelect = ''
    }
    document.addEventListener('mousemove', onMouseMove)
    document.addEventListener('mouseup', onMouseUp)
  }, [containerRef])

  return { pct, onMouseDown }
}

// ─── Timer hook ───────────────────────────────────────────────────────────────
function useTimer() {
  const [totalSeconds, setTotalSeconds] = useState(0)
  const [remaining, setRemaining]       = useState(0)
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

  const pause  = useCallback(() => setRunning(false), [])
  const resume = useCallback(() => { if (remaining > 0) setRunning(true) }, [remaining])
  const reset  = useCallback(() => {
    setRunning(false); setExpired(false); setTotalSeconds(0); setRemaining(0)
  }, [])

  useEffect(() => {
    if (!running) { if (intervalRef.current) clearInterval(intervalRef.current); return }
    intervalRef.current = setInterval(() => {
      setRemaining(prev => {
        if (prev <= 1) { setRunning(false); setExpired(true); return 0 }
        return prev - 1
      })
    }, 1000)
    return () => { if (intervalRef.current) clearInterval(intervalRef.current) }
  }, [running])

  return { totalSeconds, remaining, elapsed: totalSeconds - remaining, running, expired, start, pause, resume, reset }
}

function formatTime(s: number) {
  const m = Math.floor(Math.abs(s) / 60)
  const sec = Math.abs(s) % 60
  return `${m}:${sec.toString().padStart(2, '0')}`
}

// ─── Question markdown formatter ──────────────────────────────────────────────
function formatQuestionMd(question: any): string {
  let md = `${question.description}\n\n`
  md += `### Examples\n\n`
  for (const [i, ex] of (question.examples || []).entries()) {
    md += `**Example ${i + 1}:**\n\`\`\`\nInput:  ${ex.input}\nOutput: ${ex.output}\n\`\`\`\n`
    if (ex.explanation) md += `*${ex.explanation}*\n\n`
    else md += '\n'
  }
  const constraints = question.constraints || []
  if (constraints.length > 0) {
    md += `### Constraints\n\n`
    for (const c of constraints) md += `- \`${c}\`\n`
  }
  return md
}

// ─── Main page ────────────────────────────────────────────────────────────────
export default function CodingSession() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const questionId = searchParams.get('id') || undefined
  const fromStudy = searchParams.get('from') === 'study'
  const studyPlanId = searchParams.get('plan') || null

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
  const [showDurationPicker, setShowDurationPicker] = useState(false)
  const [note, setNote]                 = useState('')
  const [noteSaved, setNoteSaved]       = useState(false)
  const noteSaveTimer                   = useRef<ReturnType<typeof setTimeout> | null>(null)

  const timer = useTimer()
  const containerRef = useRef<HTMLDivElement>(null)
  const { pct: leftPct, onMouseDown: onDividerDown } = useHorizontalResize(40, containerRef)

  // ── Init ──────────────────────────────────────────────────────────────────
  useEffect(() => {
    getQuestions().then(qs => setAllQuestions(qs)).catch(() => {})

    startCodingSession(questionId).then(async (res) => {
      setSessionId(res.session_id)
      setQuestion(res.question)
      setMessages([{ role: 'assistant', content: res.coach_message }])
      // Load saved note for this question
      if (res.question.id) {
        getNote(res.question.id).then(r => setNote(r.note)).catch(() => {})
      }
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

  // Pause timer on solve
  useEffect(() => {
    if (submitResult?.all_passed && timer.running) timer.pause()
  }, [submitResult])

  // ── Handlers ──────────────────────────────────────────────────────────────
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
    setRunning(true); setOutput(null); setSubmitResult(null)
    try {
      const res = await executeCode(code, language)
      let out = ''
      if (res.stdout) out += res.stdout
      if (res.stderr) out += (out ? '\n' : '') + res.stderr
      if (!out) out = res.exit_code === 0 ? '(no output)' : `Exit code: ${res.exit_code}`
      if (res.time_ms) out += `\n--- ${res.time_ms}ms ---`
      setOutput(out)
    } catch { setOutput('Error running code') }
    setRunning(false)
  }

  const handleSubmit = async () => {
    if (!sessionId || !question) return
    setSubmitting(true); setOutput(null); setSubmitResult(null)
    try {
      const res = await submitSolution(sessionId, code, language, question.id)
      setSubmitResult(res)
      setOutput(res.stdout + (res.stderr ? '\n' + res.stderr : ''))
      // Auto-mark complete in study plan on a passing submission
      if (res.all_passed && fromStudy && studyPlanId) {
        markQuestionComplete(studyPlanId, question.id).catch(() => {})
      }
    } catch { setOutput('Error submitting solution') }
    setSubmitting(false)
  }

  const handleNext = useCallback(() => {
    if (allQuestions.length === 0) { navigate('/'); return }
    const sameDiff = allQuestions.filter(q => q.id !== question?.id && q.difficulty === question?.difficulty)
    const pool = sameDiff.length > 0 ? sameDiff : allQuestions.filter(q => q.id !== question?.id)
    const next = pool[Math.floor(Math.random() * pool.length)]
    if (next) navigate(`/coding?id=${next.id}`)
  }, [allQuestions, question, navigate])

  const handleNoteChange = (value: string) => {
    setNote(value)
    setNoteSaved(false)
    if (noteSaveTimer.current) clearTimeout(noteSaveTimer.current)
    noteSaveTimer.current = setTimeout(() => {
      if (question?.id) {
        saveNote(question.id, value)
          .then(() => { setNoteSaved(true); setTimeout(() => setNoteSaved(false), 2000) })
          .catch(() => {})
      }
    }, 800)
  }

  const toggleCoach = () => {
    setCoachOpen(prev => !prev)
    if (!coachOpen) setUnreadCoach(0)
  }

  // ── Timer color ───────────────────────────────────────────────────────────
  const timerColor = timer.expired ? 'var(--red)'
    : timer.remaining <= 300 && timer.totalSeconds > 0 ? 'var(--red)'
    : timer.remaining <= 600 && timer.totalSeconds > 0 ? 'var(--yellow)'
    : 'var(--text-muted)'

  // ── Loading ────────────────────────────────────────────────────────────────
  if (initializing) {
    return (
      <div style={{ height: '100vh', display: 'flex', alignItems: 'center', justifyContent: 'center', background: 'var(--bg-primary)' }}>
        <p style={{ color: 'var(--text-secondary)' }}>Loading...</p>
      </div>
    )
  }

  const diffColor = question?.difficulty === 'easy' ? 'var(--green)'
    : question?.difficulty === 'medium' ? 'var(--yellow)'
    : 'var(--red)'

  const diffBg = question?.difficulty === 'easy' ? 'rgba(34,197,94,0.1)'
    : question?.difficulty === 'medium' ? 'rgba(234,179,8,0.1)'
    : 'rgba(239,68,68,0.1)'

  // ── Render ─────────────────────────────────────────────────────────────────
  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column', background: 'var(--bg-primary)' }}>

      {/* ── Top nav bar ── */}
      <div style={{
        height: 44,
        padding: '0 16px',
        borderBottom: '1px solid var(--border)',
        background: 'var(--bg-secondary)',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'space-between',
        flexShrink: 0,
        gap: 12,
      }}>
        {/* Left */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
          <button
            onClick={() => navigate(fromStudy ? '/study' : '/')}
            style={{ background: 'transparent', color: 'var(--text-muted)', fontSize: 13, padding: '4px 8px', border: '1px solid var(--border)', borderRadius: 6 }}
          >
            {fromStudy ? '← Study Plan' : '← Problems'}
          </button>
          {question && (
            <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
              <span style={{ fontSize: 14, fontWeight: 600, color: 'var(--text-primary)' }}>{question.title}</span>
              <span style={{ fontSize: 11, fontWeight: 600, padding: '2px 8px', borderRadius: 10, color: diffColor, background: diffBg }}>
                {question.difficulty}
              </span>
            </div>
          )}
        </div>

        {/* Center: Timer */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          {!timer.totalSeconds ? (
            <div style={{ position: 'relative' }}>
              <button
                onClick={() => setShowDurationPicker(p => !p)}
                style={{ background: 'transparent', color: 'var(--text-muted)', fontSize: 12, padding: '4px 10px', border: '1px solid var(--border)', borderRadius: 6, cursor: 'pointer' }}
              >
                ⏱ Timer
              </button>
              {showDurationPicker && (
                <div style={{
                  position: 'absolute', top: '110%', left: '50%', transform: 'translateX(-50%)',
                  background: 'var(--bg-secondary)', border: '1px solid var(--border)', borderRadius: 8,
                  padding: 8, display: 'flex', gap: 6, zIndex: 200, boxShadow: '0 8px 24px rgba(0,0,0,0.4)',
                }}>
                  {[20, 30, 45, 60].map(d => (
                    <button
                      key={d}
                      onClick={() => { timer.start(d); setShowDurationPicker(false) }}
                      style={{ background: 'var(--bg-surface)', color: 'var(--text-primary)', fontSize: 13, fontWeight: 600, padding: '5px 12px', borderRadius: 6, border: 'none', cursor: 'pointer' }}
                    >
                      {d}m
                    </button>
                  ))}
                </div>
              )}
            </div>
          ) : (
            <div style={{ display: 'flex', alignItems: 'center', gap: 6 }}>
              <span style={{ fontFamily: 'monospace', fontSize: 15, fontWeight: 700, color: timerColor, minWidth: 52 }}>
                {timer.expired ? '⏰ 0:00' : `⏱ ${formatTime(timer.remaining)}`}
              </span>
              {!timer.expired && (
                <button onClick={timer.running ? timer.pause : timer.resume}
                  style={{ background: 'transparent', color: 'var(--text-muted)', fontSize: 14, padding: '2px 5px', border: 'none', cursor: 'pointer' }}
                  title={timer.running ? 'Pause' : 'Resume'}
                >{timer.running ? '⏸' : '▶'}</button>
              )}
              <button onClick={timer.reset}
                style={{ background: 'transparent', color: 'var(--text-muted)', fontSize: 12, padding: '2px 4px', border: 'none', cursor: 'pointer' }}
                title="Reset"
              >✕</button>
              {submitResult?.all_passed && (
                <span style={{ fontSize: 11, color: 'var(--green)', fontWeight: 600, marginLeft: 2 }}>
                  ✓ {formatTime(timer.elapsed)}
                </span>
              )}
            </div>
          )}
        </div>

        {/* Right */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <button onClick={handleNext}
            style={{ background: 'transparent', color: 'var(--text-muted)', fontSize: 12, padding: '4px 10px', border: '1px solid var(--border)', borderRadius: 6, cursor: 'pointer' }}
          >
            Next →
          </button>
          <button
            onClick={toggleCoach}
            style={{
              background: coachOpen ? 'var(--accent)' : 'transparent',
              color: coachOpen ? '#fff' : 'var(--text-primary)',
              fontSize: 13, fontWeight: 600, padding: '4px 14px',
              border: `1px solid ${coachOpen ? 'var(--accent)' : 'var(--border)'}`,
              borderRadius: 6, cursor: 'pointer', position: 'relative',
            }}
          >
            Coach
            {unreadCoach > 0 && !coachOpen && (
              <span style={{
                position: 'absolute', top: -5, right: -5, width: 16, height: 16,
                borderRadius: '50%', background: 'var(--red)', color: '#fff',
                fontSize: 9, fontWeight: 700, display: 'flex', alignItems: 'center', justifyContent: 'center',
              }}>{unreadCoach}</span>
            )}
          </button>
        </div>
      </div>

      {/* ── Body: left panel | divider | right panel ── */}
      <div ref={containerRef} style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>

        {/* LEFT: problem statement + output */}
        <div style={{
          width: `${leftPct}%`,
          display: 'flex',
          flexDirection: 'column',
          overflow: 'hidden',
          flexShrink: 0,
        }}>
          {/* Problem statement — scrollable */}
          <div style={{ flex: 1, overflowY: 'auto', padding: '20px 24px' }}>
            {question && (
              <div className="markdown-body" style={{ fontSize: 14, lineHeight: 1.75, maxWidth: 700 }}>
                {/* Tags row */}
                <div style={{ display: 'flex', flexWrap: 'wrap', gap: 6, marginBottom: 16 }}>
                  {question.category && (
                    <span style={{ fontSize: 11, color: 'var(--accent)', background: 'rgba(99,102,241,0.1)', padding: '2px 8px', borderRadius: 10, fontWeight: 500 }}>
                      {question.category}
                    </span>
                  )}
                  {question.tags?.slice(0, 4).map((t: string) => (
                    <span key={t} style={{ fontSize: 11, color: 'var(--text-muted)', background: 'var(--bg-surface)', padding: '2px 8px', borderRadius: 10 }}>
                      {t}
                    </span>
                  ))}
                </div>
                <ReactMarkdown>{formatQuestionMd(question)}</ReactMarkdown>

                {/* Notes */}
                <div style={{ marginTop: 24, paddingTop: 16, borderTop: '1px solid var(--border)' }}>
                  <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: 8 }}>
                    <span style={{ fontSize: 11, fontWeight: 700, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: '0.08em' }}>
                      📝 My Notes
                    </span>
                    {noteSaved && (
                      <span style={{ fontSize: 11, color: 'var(--green)', fontWeight: 600 }}>Saved ✓</span>
                    )}
                  </div>
                  <textarea
                    value={note}
                    onChange={e => handleNoteChange(e.target.value)}
                    placeholder="Approach, complexity, edge cases, gotchas…"
                    style={{
                      width: '100%',
                      minHeight: 100,
                      padding: '10px 12px',
                      background: 'var(--bg-surface)',
                      color: 'var(--text-primary)',
                      border: '1px solid var(--border)',
                      borderRadius: 8,
                      fontSize: 13,
                      fontFamily: 'inherit',
                      lineHeight: 1.6,
                      resize: 'vertical',
                      outline: 'none',
                      boxSizing: 'border-box',
                    }}
                    onFocus={e => (e.target.style.borderColor = 'var(--accent)')}
                    onBlur={e => (e.target.style.borderColor = 'var(--border)')}
                  />
                </div>
              </div>
            )}
          </div>

          {/* OUTPUT panel — pinned to bottom of left column */}
          <div style={{
            borderTop: '1px solid var(--border)',
            background: 'var(--bg-secondary)',
            flexShrink: 0,
          }}>
            {/* Result banner */}
            {submitResult && (
              <div style={{
                padding: '8px 16px',
                background: submitResult.all_passed ? 'rgba(34,197,94,0.12)' : 'rgba(239,68,68,0.12)',
                borderBottom: `1px solid ${submitResult.all_passed ? 'rgba(34,197,94,0.3)' : 'rgba(239,68,68,0.3)'}`,
                display: 'flex', alignItems: 'center', justifyContent: 'space-between',
              }}>
                <span style={{ fontSize: 13, fontWeight: 700, color: submitResult.all_passed ? 'var(--green)' : 'var(--red)' }}>
                  {submitResult.all_passed
                    ? `✓ All ${submitResult.total} test cases passed!`
                    : `✗ ${submitResult.passed}/${submitResult.total} test cases passed`}
                </span>
                <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                  {submitResult.time_ms && (
                    <span style={{ fontSize: 11, color: 'var(--text-muted)' }}>{submitResult.time_ms}ms</span>
                  )}
                  <button onClick={handleNext} style={{
                    background: submitResult.all_passed ? 'var(--green)' : 'var(--bg-surface)',
                    color: submitResult.all_passed ? '#000' : 'var(--text-primary)',
                    fontSize: 12, fontWeight: 600, padding: '4px 12px', borderRadius: 6, border: 'none', cursor: 'pointer',
                  }}>Next →</button>
                </div>
              </div>
            )}

            {/* Console output */}
            <div style={{ maxHeight: 200, minHeight: 80, overflowY: 'auto' }}>
              {/* Compilation error banner */}
              {output !== null && (() => {
                const isCompileError =
                  output.includes('Compilation Error') ||
                  (output.includes('error:') && (output.includes('.java:') || output.includes('.py:'))) ||
                  output.startsWith('SyntaxError') ||
                  output.includes('IndentationError')
                return isCompileError ? (
                  <div style={{
                    padding: '7px 16px',
                    background: 'rgba(239,68,68,0.15)',
                    borderBottom: '1px solid rgba(239,68,68,0.3)',
                    display: 'flex', alignItems: 'center', gap: 6,
                  }}>
                    <span style={{ fontSize: 13 }}>⚠️</span>
                    <span style={{ fontSize: 12, fontWeight: 700, color: 'var(--red)', letterSpacing: 0.2 }}>
                      Compilation Error — fix syntax and try again
                    </span>
                  </div>
                ) : null
              })()}

              <div style={{ padding: '10px 16px' }}>
                <div style={{ fontSize: 10, color: 'var(--text-muted)', fontWeight: 600, letterSpacing: '0.08em', textTransform: 'uppercase', marginBottom: 6 }}>
                  {running ? 'Running…' : submitting ? 'Testing…' : 'Console'}
                </div>
                {output !== null ? (
                  <pre style={{ fontSize: 12, color: 'var(--text-primary)', whiteSpace: 'pre-wrap', fontFamily: 'monospace', margin: 0, lineHeight: 1.6 }}>
                    {output}
                  </pre>
                ) : (
                  <div style={{ fontSize: 12, color: 'var(--text-muted)', fontStyle: 'italic' }}>
                    {running || submitting ? '' : 'Run code or submit to see results here.'}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>

        {/* Drag divider */}
        <div
          onMouseDown={onDividerDown}
          style={{
            width: 5,
            cursor: 'col-resize',
            background: 'var(--border)',
            flexShrink: 0,
            display: 'flex',
            alignItems: 'center',
            justifyContent: 'center',
            transition: 'background 0.15s',
          }}
          onMouseEnter={e => (e.currentTarget.style.background = 'var(--accent)')}
          onMouseLeave={e => (e.currentTarget.style.background = 'var(--border)')}
        >
        </div>

        {/* RIGHT: editor (full height) + optional coach panel */}
        <div style={{ flex: 1, display: 'flex', overflow: 'hidden', minWidth: 0 }}>

          {/* Editor column */}
          <div style={{ flex: 1, display: 'flex', flexDirection: 'column', minWidth: 0, overflow: 'hidden' }}>
            <CodeEditor
              code={code}
              language={language}
              onChange={setCode}
              onLanguageChange={handleLanguageChange}
              onRun={handleRun}
              onSubmit={handleSubmit}
              onNext={handleNext}
              output={null}          /* output shown in left panel */
              running={running}
              submitting={submitting}
              submitResult={null}    /* result shown in left panel */
            />
          </div>

          {/* Coach flyout */}
          <div style={{
            width: coachOpen ? 360 : 0,
            overflow: 'hidden',
            transition: 'width 0.2s ease',
            borderLeft: coachOpen ? '1px solid var(--border)' : 'none',
            flexShrink: 0,
          }}>
            {coachOpen && (
              <div style={{ width: 360, height: '100%' }}>
                <ChatPanel
                  messages={messages}
                  onSend={handleSend}
                  loading={loading}
                  placeholder="Ask for a hint or discuss approach..."
                />
              </div>
            )}
          </div>
        </div>
      </div>
    </div>
  )
}
