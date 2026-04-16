import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import { getQuestions, getFilters, getSolvedQuestions, getDesignTopics, getAssessmentResults } from '../api/client'

export default function Home() {
  const navigate = useNavigate()
  const userId = localStorage.getItem('userId')
  const userName = localStorage.getItem('userName')

  const [questions, setQuestions] = useState<any[]>([])
  const [designTopics, setDesignTopics] = useState<any[]>([])
  const [filterOptions, setFilterOptions] = useState<{ algorithms: string[]; companies: string[]; categories: string[] }>({ algorithms: [], companies: [], categories: [] })
  const [difficulty, setDifficulty] = useState('')
  const [algorithm, setAlgorithm] = useState('')
  const [company, setCompany] = useState('')
  const [frequency, setFrequency] = useState('')
  const [solved, setSolved] = useState<Set<string>>(new Set())
  const [assessment, setAssessment] = useState<any>(null)
  const [showPlan, setShowPlan] = useState(false)

  useEffect(() => {
    getFilters().then(setFilterOptions).catch(() => {})
    getDesignTopics().then(setDesignTopics).catch(() => {})
    getSolvedQuestions().then(ids => setSolved(new Set(ids))).catch(() => {})
    if (userId) {
      getAssessmentResults(userId).then(setAssessment).catch(() => {})
    }
  }, [])

  useEffect(() => {
    const filters: any = {}
    if (difficulty) filters.difficulty = difficulty
    if (algorithm) filters.topic = algorithm
    if (company) filters.company = company
    if (frequency) filters.frequency = frequency
    getQuestions(Object.keys(filters).length ? filters : undefined).then(setQuestions).catch(() => {})
  }, [difficulty, algorithm, company, frequency])

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
            {userName ? `Welcome back, ${userName}` : 'AI-powered interview prep'}
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
          <button
            onClick={() => navigate('/study')}
            style={{ background: 'var(--accent)', color: 'var(--bg-primary)', fontSize: 13, fontWeight: 600 }}
          >
            Study Plans
          </button>
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
              style={{ background: 'var(--bg-surface)', color: 'var(--text-primary)', fontSize: 13 }}
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
          {/* Blind 75 collection header */}
          <div style={{
            background: 'linear-gradient(135deg, rgba(99,102,241,0.15), rgba(139,92,246,0.1))',
            border: '1px solid rgba(99,102,241,0.3)',
            borderRadius: 12,
            padding: '16px 20px',
            marginBottom: 16,
          }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', marginBottom: 4 }}>
              <h2 style={{ fontSize: 20, fontWeight: 700 }}>Blind 75</h2>
              <span style={{ fontSize: 13, color: 'var(--text-secondary)' }}>
                {questions.length} question{questions.length !== 1 ? 's' : ''}
              </span>
            </div>
            <p style={{ fontSize: 13, color: 'var(--text-secondary)', marginBottom: 12 }}>
              Curated set of must-know interview problems across all major algorithm topics
            </p>
            <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
              <select value={difficulty} onChange={e => setDifficulty(e.target.value)} style={{ padding: '6px 12px', fontSize: 13 }}>
                <option value="">All difficulties</option>
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
              </select>
              <select value={algorithm} onChange={e => setAlgorithm(e.target.value)} style={{ padding: '6px 12px', fontSize: 13 }}>
                <option value="">All algorithms</option>
                {filterOptions.algorithms.map(a => <option key={a} value={a}>{a}</option>)}
              </select>
              <select value={company} onChange={e => setCompany(e.target.value)} style={{ padding: '6px 12px', fontSize: 13 }}>
                <option value="">All companies</option>
                {filterOptions.companies.map(c => <option key={c} value={c}>{c}</option>)}
              </select>
              <select value={frequency} onChange={e => setFrequency(e.target.value)} style={{ padding: '6px 12px', fontSize: 13 }}>
                <option value="">All frequencies</option>
                <option value="high">High frequency</option>
                <option value="medium">Medium frequency</option>
                <option value="low">Low frequency</option>
              </select>
            </div>
          </div>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 8 }}>
            {questions.map(q => (
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
                <span style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
                  {solved.has(q.id) && (
                    <span style={{ color: 'var(--green)', fontSize: 14, fontWeight: 700 }}>✓</span>
                  )}
                  {q.title}
                </span>
                <div style={{ display: 'flex', gap: 6, alignItems: 'center', flexWrap: 'wrap', justifyContent: 'flex-end' }}>
                  {q.frequency === 'high' && (
                    <span style={{ fontSize: 10, color: 'var(--red)', background: 'rgba(255,80,80,0.1)', padding: '2px 6px', borderRadius: 4, fontWeight: 600 }}>HOT</span>
                  )}
                  {(q.companies || []).slice(0, 2).map((c: string) => (
                    <span key={c} style={{ fontSize: 10, color: 'var(--accent)', background: 'rgba(99,102,241,0.1)', padding: '2px 6px', borderRadius: 4 }}>
                      {c}
                    </span>
                  ))}
                  {q.tags.slice(0, 2).map((t: string) => (
                    <span key={t} style={{ fontSize: 10, color: 'var(--text-muted)', background: 'var(--bg-hover)', padding: '2px 6px', borderRadius: 4 }}>
                      {t}
                    </span>
                  ))}
                  <span style={{ color: difficultyColor(q.difficulty), fontWeight: 600, fontSize: 12, minWidth: 55, textAlign: 'right' }}>
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
