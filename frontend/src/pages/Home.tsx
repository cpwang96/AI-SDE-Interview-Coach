import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import { getQuestions, getDesignTopics } from '../api/client'

export default function Home() {
  const navigate = useNavigate()
  const [questions, setQuestions] = useState<any[]>([])
  const [designTopics, setDesignTopics] = useState<any[]>([])
  const [filter, setFilter] = useState<string>('')

  useEffect(() => {
    getQuestions().then(setQuestions).catch(() => {})
    getDesignTopics().then(setDesignTopics).catch(() => {})
  }, [])

  const filteredQuestions = filter
    ? questions.filter(q => q.difficulty === filter)
    : questions

  const difficultyColor = (d: string) =>
    d === 'easy' ? 'var(--green)' : d === 'medium' ? 'var(--yellow)' : 'var(--red)'

  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '60px 20px', overflowY: 'auto' }}>
      <h1 style={{ fontSize: 36, fontWeight: 700, marginBottom: 8 }}>
        Interview Coach
      </h1>
      <p style={{ color: 'var(--text-secondary)', marginBottom: 48, fontSize: 16 }}>
        AI-powered interview prep — coding questions & system design
      </p>

      <div style={{ display: 'flex', gap: 32, width: '100%', maxWidth: 1000, flexWrap: 'wrap' }}>
        {/* Coding Questions */}
        <div style={{ flex: 1, minWidth: 400 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 16 }}>
            <h2 style={{ fontSize: 20, fontWeight: 600 }}>Coding Questions</h2>
            <select
              value={filter}
              onChange={e => setFilter(e.target.value)}
              style={{ padding: '6px 12px', fontSize: 13 }}
            >
              <option value="">All difficulties</option>
              <option value="easy">Easy</option>
              <option value="medium">Medium</option>
              <option value="hard">Hard</option>
            </select>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {filteredQuestions.map(q => (
              <button
                key={q.id}
                onClick={() => navigate(`/coding?id=${q.id}`)}
                style={{
                  background: 'var(--bg-surface)',
                  color: 'var(--text-primary)',
                  padding: '14px 18px',
                  textAlign: 'left',
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                }}
              >
                <span>{q.title}</span>
                <div style={{ display: 'flex', gap: 8, alignItems: 'center' }}>
                  {q.tags.map((t: string) => (
                    <span key={t} style={{ fontSize: 11, color: 'var(--text-muted)', background: 'var(--bg-hover)', padding: '2px 8px', borderRadius: 4 }}>
                      {t}
                    </span>
                  ))}
                  <span style={{ color: difficultyColor(q.difficulty), fontWeight: 600, fontSize: 13, minWidth: 60, textAlign: 'right' }}>
                    {q.difficulty}
                  </span>
                </div>
              </button>
            ))}
            <button
              onClick={() => navigate('/coding')}
              style={{
                background: 'var(--accent)',
                color: 'var(--bg-primary)',
                padding: '14px 18px',
                fontWeight: 600,
              }}
            >
              Random Question
            </button>
          </div>
        </div>

        {/* System Design */}
        <div style={{ flex: 1, minWidth: 400 }}>
          <h2 style={{ fontSize: 20, fontWeight: 600, marginBottom: 16 }}>System Design</h2>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {designTopics.map(t => (
              <button
                key={t.id}
                onClick={() => navigate(`/system-design?topic=${encodeURIComponent(t.title)}`)}
                style={{
                  background: 'var(--bg-surface)',
                  color: 'var(--text-primary)',
                  padding: '14px 18px',
                  textAlign: 'left',
                }}
              >
                {t.title}
              </button>
            ))}
            <button
              onClick={() => navigate('/system-design')}
              style={{
                background: 'var(--accent)',
                color: 'var(--bg-primary)',
                padding: '14px 18px',
                fontWeight: 600,
              }}
            >
              Random Topic
            </button>
          </div>
        </div>
      </div>
    </div>
  )
}
