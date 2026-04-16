import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import { getQuestions, getDesignTopics, getAssessmentResults } from '../api/client'

export default function Home() {
  const navigate = useNavigate()
  const userId = localStorage.getItem('userId')
  const userName = localStorage.getItem('userName')

  const [questions, setQuestions] = useState<any[]>([])
  const [designTopics, setDesignTopics] = useState<any[]>([])
  const [filter, setFilter] = useState<string>('')
  const [assessment, setAssessment] = useState<any>(null)
  const [showPlan, setShowPlan] = useState(false)

  useEffect(() => {
    if (!userId) {
      navigate('/onboarding')
      return
    }
    getQuestions().then(setQuestions).catch(() => {})
    getDesignTopics().then(setDesignTopics).catch(() => {})
    getAssessmentResults(userId).then(setAssessment).catch(() => {})
  }, [])

  const filteredQuestions = filter
    ? questions.filter(q => q.difficulty === filter)
    : questions

  const difficultyColor = (d: string) =>
    d === 'easy' ? 'var(--green)' : d === 'medium' ? 'var(--yellow)' : 'var(--red)'

  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '40px 20px', overflowY: 'auto' }}>
      <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', width: '100%', maxWidth: 1000, marginBottom: 32 }}>
        <div>
          <h1 style={{ fontSize: 30, fontWeight: 700, marginBottom: 4 }}>
            Interview Coach
          </h1>
          <p style={{ color: 'var(--text-secondary)', fontSize: 14 }}>
            Welcome back, {userName}
            {assessment?.overall_level && (
              <span style={{
                marginLeft: 12,
                fontSize: 12,
                fontWeight: 600,
                padding: '2px 10px',
                borderRadius: 4,
                background: 'var(--bg-surface)',
                color: assessment.overall_level === 'advanced' ? 'var(--green)' : assessment.overall_level === 'intermediate' ? 'var(--yellow)' : 'var(--red)',
              }}>
                {assessment.overall_level}
              </span>
            )}
          </p>
        </div>
        <div style={{ display: 'flex', gap: 8 }}>
          {assessment?.study_plan && (
            <button
              onClick={() => setShowPlan(!showPlan)}
              style={{ background: 'var(--bg-surface)', color: 'var(--text-primary)', fontSize: 13 }}
            >
              {showPlan ? 'Hide' : 'View'} Study Plan
            </button>
          )}
          {!assessment && (
            <button
              onClick={() => navigate('/assessment')}
              style={{ background: 'var(--accent)', color: 'var(--bg-primary)', fontSize: 13, fontWeight: 600 }}
            >
              Take Assessment
            </button>
          )}
        </div>
      </div>

      {/* Study Plan */}
      {showPlan && assessment?.study_plan && (
        <div style={{
          width: '100%',
          maxWidth: 1000,
          background: 'var(--bg-surface)',
          padding: 24,
          borderRadius: 12,
          marginBottom: 24,
          lineHeight: 1.7,
          fontSize: 14,
        }}>
          <ReactMarkdown>{assessment.study_plan}</ReactMarkdown>
        </div>
      )}

      {/* Topic scores from assessment */}
      {assessment?.topic_scores && Object.keys(assessment.topic_scores).length > 0 && (
        <div style={{ width: '100%', maxWidth: 1000, marginBottom: 24 }}>
          <h3 style={{ fontSize: 14, fontWeight: 600, marginBottom: 8, color: 'var(--text-secondary)' }}>
            Your Topic Scores
          </h3>
          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
            {Object.entries(assessment.topic_scores).map(([topic, score]: [string, any]) => (
              <div key={topic} style={{
                background: 'var(--bg-surface)',
                padding: '6px 14px',
                borderRadius: 6,
                fontSize: 13,
                display: 'flex',
                gap: 8,
                alignItems: 'center',
              }}>
                <span>{topic}</span>
                <span style={{
                  fontWeight: 600,
                  color: score >= 70 ? 'var(--green)' : score >= 40 ? 'var(--yellow)' : 'var(--red)',
                }}>
                  {score}
                </span>
              </div>
            ))}
          </div>
        </div>
      )}

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
