import { useState, useEffect } from 'react'
import { useSearchParams, useNavigate } from 'react-router-dom'
import ChatPanel from '../components/ChatPanel'
import { startDesignSession, sendDesignMessage } from '../api/client'

interface Message {
  role: 'user' | 'assistant'
  content: string
}

export default function SystemDesignSession() {
  const [searchParams] = useSearchParams()
  const navigate = useNavigate()
  const topic = searchParams.get('topic') || undefined

  const [sessionId, setSessionId] = useState<string | null>(null)
  const [messages, setMessages] = useState<Message[]>([])
  const [loading, setLoading] = useState(false)
  const [initializing, setInitializing] = useState(true)

  useEffect(() => {
    startDesignSession(topic).then(res => {
      setSessionId(res.session_id)
      setMessages([{ role: 'assistant', content: res.coach_message }])
      setInitializing(false)
    }).catch(() => setInitializing(false))
  }, [])

  const handleSend = async (message: string) => {
    if (!sessionId) return
    setMessages(prev => [...prev, { role: 'user', content: message }])
    setLoading(true)
    try {
      const res = await sendDesignMessage(sessionId, message)
      setMessages(prev => [...prev, { role: 'assistant', content: res.response }])
    } catch {
      setMessages(prev => [...prev, { role: 'assistant', content: 'Error communicating with coach. Please try again.' }])
    }
    setLoading(false)
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
        <h2 style={{ fontSize: 16, fontWeight: 600 }}>
          System Design {topic ? `— ${topic}` : ''}
        </h2>
      </div>

      {/* Full-width chat for system design */}
      <div style={{ flex: 1, maxWidth: 900, width: '100%', margin: '0 auto' }}>
        <ChatPanel
          messages={messages}
          onSend={handleSend}
          loading={loading}
          placeholder="Discuss your design, ask questions, propose solutions..."
        />
      </div>
    </div>
  )
}
