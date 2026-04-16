import { useState, useEffect } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import CodeEditor from '../components/CodeEditor'
import ChatPanel from '../components/ChatPanel'
import { startCodingSession, sendCodingMessage, executeCode } from '../api/client'

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
  const [initializing, setInitializing] = useState(true)

  useEffect(() => {
    startCodingSession(questionId).then(res => {
      setSessionId(res.session_id)
      setQuestion(res.question)
      setCode(res.question.starter_code[language] || '')
      setMessages([{ role: 'assistant', content: res.coach_message }])
      setInitializing(false)
    }).catch(() => setInitializing(false))
  }, [])

  const handleLanguageChange = (lang: string) => {
    setLanguage(lang)
    if (question?.starter_code[lang]) {
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
    try {
      const res = await executeCode(code, language)
      let out = ''
      if (res.stdout) out += res.stdout
      if (res.stderr) out += (out ? '\n' : '') + res.stderr
      if (!out) out = res.exit_code === 0 ? '(no output)' : `Exit code: ${res.exit_code}`
      if (res.time_ms) out += `\n\n--- ${res.time_ms}ms ---`
      setOutput(out)
    } catch {
      setOutput('Error running code')
    }
    setRunning(false)
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
          </>
        )}
      </div>

      {/* Main layout: Editor + Chat side by side */}
      <div style={{ flex: 1, display: 'flex', overflow: 'hidden' }}>
        {/* Left: Problem + Code Editor */}
        <div style={{ flex: 1, display: 'flex', flexDirection: 'column', borderRight: '1px solid var(--border)' }}>
          {/* Problem description */}
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
          {/* Code editor */}
          <div style={{ flex: 1 }}>
            <CodeEditor
              code={code}
              language={language}
              onChange={setCode}
              onLanguageChange={handleLanguageChange}
              onRun={handleRun}
              output={output}
              running={running}
            />
          </div>
        </div>

        {/* Right: Chat */}
        <div style={{ width: 420, minWidth: 350 }}>
          <ChatPanel
            messages={messages}
            onSend={handleSend}
            loading={loading}
            placeholder="Ask for a hint, discuss approach, or submit code for review..."
          />
        </div>
      </div>
    </div>
  )
}
