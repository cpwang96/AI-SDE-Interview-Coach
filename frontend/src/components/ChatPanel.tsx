import { useState, useRef, useEffect } from 'react'
import ReactMarkdown from 'react-markdown'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

interface ChatPanelProps {
  messages: Message[]
  onSend: (message: string) => void
  loading: boolean
  placeholder?: string
}

export default function ChatPanel({ messages, onSend, loading, placeholder }: ChatPanelProps) {
  const [input, setInput] = useState('')
  const bottomRef = useRef<HTMLDivElement>(null)

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault()
    if (!input.trim() || loading) return
    onSend(input.trim())
    setInput('')
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      {/* Messages */}
      <div style={{ flex: 1, overflowY: 'auto', padding: 16 }}>
        {messages.map((msg, i) => (
          <div
            key={i}
            style={{
              marginBottom: 16,
              display: 'flex',
              flexDirection: 'column',
              alignItems: msg.role === 'user' ? 'flex-end' : 'flex-start',
            }}
          >
            <span style={{ fontSize: 11, color: 'var(--text-muted)', marginBottom: 4 }}>
              {msg.role === 'user' ? 'You' : 'Coach'}
            </span>
            <div
              style={{
                background: msg.role === 'user' ? 'var(--accent)' : 'var(--bg-surface)',
                color: msg.role === 'user' ? 'var(--bg-primary)' : 'var(--text-primary)',
                padding: '10px 14px',
                borderRadius: 12,
                maxWidth: '85%',
                fontSize: 14,
                lineHeight: 1.6,
              }}
            >
              <ReactMarkdown
                components={{
                  code: ({ children, className }) => {
                    const isBlock = className?.startsWith('language-')
                    return isBlock ? (
                      <pre style={{ background: 'var(--bg-secondary)', padding: 12, borderRadius: 6, overflowX: 'auto', margin: '8px 0' }}>
                        <code>{children}</code>
                      </pre>
                    ) : (
                      <code style={{ background: 'rgba(0,0,0,0.2)', padding: '2px 6px', borderRadius: 4, fontSize: 13 }}>
                        {children}
                      </code>
                    )
                  },
                }}
              >
                {msg.content}
              </ReactMarkdown>
            </div>
          </div>
        ))}
        {loading && (
          <div style={{ color: 'var(--text-muted)', fontSize: 14, padding: '8px 0' }}>
            Coach is thinking...
          </div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <form onSubmit={handleSubmit} style={{ padding: 12, borderTop: '1px solid var(--border)', display: 'flex', gap: 8 }}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          placeholder={placeholder || 'Type your message...'}
          style={{ flex: 1 }}
          disabled={loading}
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          style={{
            background: 'var(--accent)',
            color: 'var(--bg-primary)',
            opacity: loading || !input.trim() ? 0.5 : 1,
          }}
        >
          Send
        </button>
      </form>
    </div>
  )
}
