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
  const [category, setCategory] = useState('')
  const [solved, setSolved] = useState<Set<string>>(new Set())
  const [assessment, setAssessment] = useState<any>(null)
  const [showPlan, setShowPlan] = useState(false)
  const [activeTab, setActiveTab] = useState<'coding' | 'design'>('coding')

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
    if (category) filters.category = category
    getQuestions(Object.keys(filters).length ? filters : undefined).then(setQuestions).catch(() => {})
  }, [difficulty, algorithm, company, frequency, category])

  const difficultyColor = (d: string) =>
    d === 'easy' ? 'var(--green)' : d === 'medium' ? 'var(--yellow)' : 'var(--red)'

  const difficultyBg = (d: string) =>
    d === 'easy' ? 'rgba(166,227,161,0.1)' : d === 'medium' ? 'rgba(249,226,175,0.1)' : 'rgba(243,139,168,0.1)'

  const easyCount = questions.filter(q => q.difficulty === 'easy').length
  const medCount = questions.filter(q => q.difficulty === 'medium').length
  const hardCount = questions.filter(q => q.difficulty === 'hard').length
  const solvedCount = questions.filter(q => solved.has(q.id)).length

  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '32px 20px', overflowY: 'auto' }}>
      {/* Hero header */}
      <div style={{ width: '100%', maxWidth: 960, marginBottom: 28 }}>
        <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start' }}>
          <div>
            <h1 style={{ fontSize: 28, fontWeight: 700, marginBottom: 6, letterSpacing: -0.5 }}>
              Interview Coach
            </h1>
            <p style={{ color: 'var(--text-muted)', fontSize: 14 }}>
              {userName ? `Welcome back, ${userName}` : 'AI-powered SDE interview prep'}
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

        {/* Stats row */}
        <div style={{ display: 'flex', gap: 12, marginTop: 20 }}>
          <div style={{ background: 'var(--bg-surface)', borderRadius: 10, padding: '14px 20px', flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <span style={{ fontSize: 22, fontWeight: 700, color: 'var(--accent)' }}>{solvedCount}/{questions.length}</span>
            <span style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 2 }}>Solved</span>
          </div>
          <div style={{ background: 'var(--bg-surface)', borderRadius: 10, padding: '14px 20px', flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <span style={{ fontSize: 22, fontWeight: 700, color: 'var(--green)' }}>{easyCount}</span>
            <span style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 2 }}>Easy</span>
          </div>
          <div style={{ background: 'var(--bg-surface)', borderRadius: 10, padding: '14px 20px', flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <span style={{ fontSize: 22, fontWeight: 700, color: 'var(--yellow)' }}>{medCount}</span>
            <span style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 2 }}>Medium</span>
          </div>
          <div style={{ background: 'var(--bg-surface)', borderRadius: 10, padding: '14px 20px', flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
            <span style={{ fontSize: 22, fontWeight: 700, color: 'var(--red)' }}>{hardCount}</span>
            <span style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 2 }}>Hard</span>
          </div>
          {assessment?.overall_level && (
            <div style={{ background: 'var(--bg-surface)', borderRadius: 10, padding: '14px 20px', flex: 1, display: 'flex', flexDirection: 'column', alignItems: 'center' }}>
              <span style={{
                fontSize: 16, fontWeight: 700,
                color: assessment.overall_level === 'advanced' ? 'var(--green)' : assessment.overall_level === 'intermediate' ? 'var(--yellow)' : 'var(--red)',
              }}>
                {assessment.overall_level}
              </span>
              <span style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 2 }}>Level</span>
            </div>
          )}
        </div>
      </div>

      {/* Study Plan */}
      {showPlan && assessment?.study_plan && (
        <div style={{
          width: '100%', maxWidth: 960,
          background: 'var(--bg-surface)', padding: 24, borderRadius: 12, marginBottom: 24,
          lineHeight: 1.7, fontSize: 14,
        }}>
          <ReactMarkdown>{assessment.study_plan}</ReactMarkdown>
        </div>
      )}

      {/* Topic scores */}
      {assessment?.topic_scores && Object.keys(assessment.topic_scores).length > 0 && (
        <div style={{ width: '100%', maxWidth: 960, marginBottom: 20 }}>
          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap' }}>
            {Object.entries(assessment.topic_scores).map(([topic, score]: [string, any]) => (
              <div key={topic} style={{
                background: 'var(--bg-surface)', padding: '6px 14px', borderRadius: 6, fontSize: 13,
                display: 'flex', gap: 8, alignItems: 'center',
              }}>
                <span>{topic}</span>
                <span style={{ fontWeight: 600, color: score >= 70 ? 'var(--green)' : score >= 40 ? 'var(--yellow)' : 'var(--red)' }}>{score}</span>
              </div>
            ))}
          </div>
        </div>
      )}

      {/* Tabs */}
      <div style={{ width: '100%', maxWidth: 960 }}>
        <div style={{ display: 'flex', gap: 0, borderBottom: '2px solid var(--border)', marginBottom: 16 }}>
          {(['coding', 'design'] as const).map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              style={{
                background: 'transparent',
                color: activeTab === tab ? 'var(--accent)' : 'var(--text-muted)',
                borderRadius: 0,
                borderBottom: activeTab === tab ? '2px solid var(--accent)' : '2px solid transparent',
                marginBottom: -2,
                padding: '10px 20px',
                fontSize: 14,
                fontWeight: 600,
                transform: 'none',
              }}
            >
              {tab === 'coding' ? `Coding (${questions.length})` : `System Design (${designTopics.length})`}
            </button>
          ))}
        </div>

        {activeTab === 'coding' && (
          <>
            {/* Filters */}
            <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginBottom: 16 }}>
              <select value={difficulty} onChange={e => setDifficulty(e.target.value)} style={{ padding: '6px 12px', fontSize: 12 }}>
                <option value="">All difficulties</option>
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
              </select>
              <select value={algorithm} onChange={e => setAlgorithm(e.target.value)} style={{ padding: '6px 12px', fontSize: 12 }}>
                <option value="">All algorithms</option>
                {filterOptions.algorithms.map(a => <option key={a} value={a}>{a}</option>)}
              </select>
              <select value={company} onChange={e => setCompany(e.target.value)} style={{ padding: '6px 12px', fontSize: 12 }}>
                <option value="">All companies</option>
                {filterOptions.companies.map(c => <option key={c} value={c}>{c}</option>)}
              </select>
              <select value={frequency} onChange={e => setFrequency(e.target.value)} style={{ padding: '6px 12px', fontSize: 12 }}>
                <option value="">All frequencies</option>
                <option value="high">High</option>
                <option value="medium">Medium</option>
                <option value="low">Low</option>
              </select>
              <button
                onClick={() => navigate('/coding')}
                style={{ marginLeft: 'auto', background: 'var(--accent)', color: 'var(--bg-primary)', fontSize: 12, fontWeight: 600, padding: '6px 14px' }}
              >
                Random
              </button>
            </div>

            {/* Category pills */}
            <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 14 }}>
              {['', ...filterOptions.categories].map(cat => (
                <button
                  key={cat || '__all__'}
                  onClick={() => setCategory(cat === category ? '' : cat)}
                  style={{
                    padding: '5px 14px', borderRadius: 20, fontSize: 12, fontWeight: 600,
                    background: category === cat ? 'var(--accent)' : 'var(--bg-surface)',
                    color: category === cat ? '#fff' : 'var(--text-muted)',
                    border: `1px solid ${category === cat ? 'var(--accent)' : 'var(--border)'}`,
                    cursor: 'pointer', whiteSpace: 'nowrap', transition: 'all 0.15s',
                  }}
                >
                  {cat || 'All'}
                </button>
              ))}
            </div>

            {/* Question table */}
            <div style={{ borderRadius: 10, overflow: 'hidden', border: '1px solid var(--border)' }}>
              {/* Table header */}
              <div style={{
                display: 'grid', gridTemplateColumns: '36px 1fr auto 70px',
                padding: '10px 16px', background: 'var(--bg-secondary)',
                fontSize: 11, fontWeight: 600, color: 'var(--text-muted)', textTransform: 'uppercase', letterSpacing: 0.5,
              }}>
                <span></span>
                <span>Title</span>
                <span style={{ textAlign: 'right', paddingRight: 12 }}>Tags</span>
                <span style={{ textAlign: 'right' }}>Difficulty</span>
              </div>

              {/* Question rows */}
              {questions.map((q, i) => (
                <button
                  key={q.id}
                  onClick={() => navigate(`/coding?id=${q.id}`)}
                  style={{
                    display: 'grid', gridTemplateColumns: '36px 1fr auto 70px',
                    width: '100%',
                    background: i % 2 === 0 ? 'var(--bg-primary)' : 'rgba(49,50,68,0.3)',
                    color: 'var(--text-primary)',
                    padding: '12px 16px',
                    textAlign: 'left',
                    borderRadius: 0,
                    borderBottom: i < questions.length - 1 ? '1px solid rgba(69,71,90,0.3)' : 'none',
                    alignItems: 'center',
                    transform: 'none',
                  }}
                >
                  {/* Status */}
                  <span style={{ fontSize: 14 }}>
                    {solved.has(q.id) ? (
                      <span style={{ color: 'var(--green)', fontWeight: 700 }}>✓</span>
                    ) : (
                      <span style={{ color: 'var(--text-muted)', fontSize: 12 }}>{i + 1}</span>
                    )}
                  </span>

                  {/* Title */}
                  <span style={{ fontSize: 13.5, fontWeight: 500, display: 'flex', alignItems: 'center', gap: 8 }}>
                    {q.title}
                    {q.frequency === 'high' && (
                      <span style={{ fontSize: 9, color: 'var(--red)', background: 'rgba(243,139,168,0.12)', padding: '1px 5px', borderRadius: 3, fontWeight: 700, letterSpacing: 0.3 }}>HOT</span>
                    )}
                  </span>

                  {/* Tags */}
                  <div style={{ display: 'flex', gap: 4, justifyContent: 'flex-end', paddingRight: 12 }}>
                    {(q.companies || []).slice(0, 2).map((c: string) => (
                      <span key={c} style={{ fontSize: 10, color: 'var(--accent)', background: 'rgba(137,180,250,0.08)', padding: '2px 6px', borderRadius: 3 }}>
                        {c}
                      </span>
                    ))}
                    {q.tags.slice(0, 2).map((t: string) => (
                      <span key={t} style={{ fontSize: 10, color: 'var(--text-muted)', background: 'rgba(69,71,90,0.5)', padding: '2px 6px', borderRadius: 3 }}>
                        {t}
                      </span>
                    ))}
                  </div>

                  {/* Difficulty */}
                  <span style={{
                    color: difficultyColor(q.difficulty), fontWeight: 600, fontSize: 12, textAlign: 'right',
                    background: difficultyBg(q.difficulty), padding: '2px 8px', borderRadius: 4, justifySelf: 'end',
                  }}>
                    {q.difficulty}
                  </span>
                </button>
              ))}
            </div>
          </>
        )}

        {activeTab === 'design' && (
          <div style={{ borderRadius: 10, overflow: 'hidden', border: '1px solid var(--border)' }}>
            {designTopics.map((t, i) => (
              <button
                key={t.id}
                onClick={() => navigate(`/system-design?topic=${encodeURIComponent(t.title)}`)}
                style={{
                  width: '100%',
                  background: i % 2 === 0 ? 'var(--bg-primary)' : 'rgba(49,50,68,0.3)',
                  color: 'var(--text-primary)',
                  padding: '14px 20px',
                  textAlign: 'left',
                  borderRadius: 0,
                  borderBottom: i < designTopics.length - 1 ? '1px solid rgba(69,71,90,0.3)' : 'none',
                  fontSize: 14,
                  display: 'flex',
                  alignItems: 'center',
                  gap: 12,
                  transform: 'none',
                }}
              >
                <span style={{ color: 'var(--text-muted)', fontSize: 12, minWidth: 24 }}>{i + 1}</span>
                <span>{t.title}</span>
              </button>
            ))}
            <button
              onClick={() => navigate('/system-design')}
              style={{
                width: '100%', background: 'var(--accent)', color: 'var(--bg-primary)',
                padding: '14px 20px', fontWeight: 600, borderRadius: '0 0 10px 10px',
                transform: 'none',
              }}
            >
              Random Topic
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
