import { useState, useEffect } from 'react'
import { useNavigate } from 'react-router-dom'
import ReactMarkdown from 'react-markdown'
import { getQuestions, getFilters, getSolvedQuestions, getDesignTopics, getAssessmentResults, getFlaggedQuestions } from '../api/client'

export default function Home() {
  const navigate = useNavigate()
  const userId   = localStorage.getItem('userId')
  const userName = localStorage.getItem('userName')

  const [questions, setQuestions]       = useState<any[]>([])
  const [designTopics, setDesignTopics] = useState<any[]>([])
  const [filterOptions, setFilterOptions] = useState<{ algorithms: string[]; companies: string[]; categories: string[] }>({ algorithms: [], companies: [], categories: [] })
  const [difficulty, setDifficulty]     = useState('')
  const [algorithm, setAlgorithm]       = useState('')
  const [company, setCompany]           = useState('')
  const [frequency, setFrequency]       = useState('')
  const [category, setCategory]         = useState('')
  const [solved, setSolved]             = useState<Set<string>>(new Set())
  const [flagged, setFlagged]           = useState<Set<string>>(new Set())
  const [assessment, setAssessment]     = useState<any>(null)
  const [showPlan, setShowPlan]         = useState(false)
  const [activeTab, setActiveTab]       = useState<'coding' | 'design'>('coding')

  useEffect(() => {
    getFilters().then(setFilterOptions).catch(() => {})
    getDesignTopics().then(setDesignTopics).catch(() => {})
    getSolvedQuestions().then(ids => setSolved(new Set(ids))).catch(() => {})
    getFlaggedQuestions().then(ids => setFlagged(new Set(ids))).catch(() => {})
    if (userId) getAssessmentResults(userId).then(setAssessment).catch(() => {})
  }, [])

  useEffect(() => {
    const filters: any = {}
    if (difficulty) filters.difficulty = difficulty
    if (algorithm)  filters.topic      = algorithm
    if (company)    filters.company    = company
    if (frequency)  filters.frequency  = frequency
    if (category)   filters.category   = category
    getQuestions(Object.keys(filters).length ? filters : undefined).then(setQuestions).catch(() => {})
  }, [difficulty, algorithm, company, frequency, category])

  // ── Derived counts ─────────────────────────────────────────────────────────
  const easyCount   = questions.filter(q => q.difficulty === 'easy').length
  const medCount    = questions.filter(q => q.difficulty === 'medium').length
  const hardCount   = questions.filter(q => q.difficulty === 'hard').length
  const solvedCount = questions.filter(q => solved.has(q.id)).length
  const solvedPct   = questions.length > 0 ? Math.round((solvedCount / questions.length) * 100) : 0

  const diffColor = (d: string) =>
    d === 'easy' ? 'var(--green)' : d === 'medium' ? 'var(--yellow)' : 'var(--red)'
  const diffBg = (d: string) =>
    d === 'easy'   ? 'rgba(74,222,128,0.1)'
    : d === 'medium' ? 'rgba(251,191,36,0.1)'
    : 'rgba(248,113,113,0.1)'

  // ── Render ──────────────────────────────────────────────────────────────────
  return (
    <div style={{
      height: '100vh',
      overflowY: 'auto',
      background: 'var(--bg-primary)',
    }}>
      {/* ── Hero ───────────────────────────────────────────────────────── */}
      <div style={{
        padding: '48px 20px 32px',
        background: 'linear-gradient(180deg, rgba(99,102,241,0.06) 0%, transparent 100%)',
        borderBottom: '1px solid var(--border)',
      }}>
        <div style={{ maxWidth: 960, margin: '0 auto' }}>
          {/* Title row */}
          <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 32 }}>
            <div>
              <h1 className="gradient-text" style={{ fontSize: 40, fontWeight: 800, letterSpacing: -1.5, lineHeight: 1.1, marginBottom: 10 }}>
                Interview Coach
              </h1>
              <p style={{ color: 'var(--text-secondary)', fontSize: 15 }}>
                {userName
                  ? <>Welcome back, <strong style={{ color: 'var(--accent-light)' }}>{userName}</strong> — keep the streak going 🔥</>
                  : 'AI-powered SDE interview prep · Java, Python, JavaScript'}
              </p>
            </div>
            <div style={{ display: 'flex', gap: 8, flexShrink: 0 }}>
              <button
                onClick={() => navigate('/study')}
                style={{
                  background: 'linear-gradient(135deg, var(--accent), #8b5cf6)',
                  color: '#fff', fontSize: 13, fontWeight: 700, padding: '9px 20px',
                  boxShadow: '0 0 24px rgba(99,102,241,0.35)',
                  border: 'none', borderRadius: 8,
                }}
              >
                Study Plans
              </button>
              {assessment?.study_plan && (
                <button
                  onClick={() => setShowPlan(!showPlan)}
                  style={{ background: 'var(--bg-surface)', color: 'var(--text-primary)', fontSize: 13, border: '1px solid var(--border)' }}
                >
                  {showPlan ? 'Hide' : 'View'} Plan
                </button>
              )}
              {!assessment && (
                <button
                  onClick={() => navigate('/assessment')}
                  style={{ background: 'var(--bg-surface)', color: 'var(--text-secondary)', fontSize: 13, border: '1px solid var(--border)' }}
                >
                  Take Assessment
                </button>
              )}
            </div>
          </div>

          {/* Stat cards */}
          <div style={{ display: 'flex', gap: 14 }}>
            {/* Solved — wider, shows progress bar */}
            <div className="stat-card" style={{
              flex: 2,
              background: 'var(--bg-surface)',
              borderRadius: 14,
              padding: '18px 22px',
              border: '1px solid var(--border)',
              position: 'relative', overflow: 'hidden',
            }}>
              {/* accent top line */}
              <div style={{ position: 'absolute', top: 0, left: 0, right: 0, height: 2, background: 'linear-gradient(90deg, var(--accent), #a78bfa)' }} />
              <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-end', marginBottom: 10 }}>
                <div>
                  <div style={{ fontSize: 30, fontWeight: 800, color: 'var(--accent-light)', lineHeight: 1 }}>{solvedCount}</div>
                  <div style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 4, textTransform: 'uppercase', letterSpacing: 1 }}>Solved</div>
                </div>
                <div style={{ fontSize: 13, color: 'var(--text-muted)', fontWeight: 600 }}>{solvedPct}% of {questions.length}</div>
              </div>
              <div style={{ height: 4, background: 'var(--bg-hover)', borderRadius: 2, overflow: 'hidden' }}>
                <div style={{ height: '100%', width: `${solvedPct}%`, background: 'linear-gradient(90deg, var(--accent), #a78bfa)', borderRadius: 2, transition: 'width 0.5s ease' }} />
              </div>
            </div>

            {[
              { label: 'Easy',   count: easyCount,  color: 'var(--green)',  glow: 'rgba(74,222,128,0.12)'  },
              { label: 'Medium', count: medCount,   color: 'var(--yellow)', glow: 'rgba(251,191,36,0.12)'  },
              { label: 'Hard',   count: hardCount,  color: 'var(--red)',    glow: 'rgba(248,113,113,0.12)' },
            ].map(({ label, count, color, glow }) => (
              <div key={label} className="stat-card" style={{
                flex: 1,
                background: 'var(--bg-surface)',
                borderRadius: 14,
                padding: '18px 20px',
                border: '1px solid var(--border)',
                display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
                position: 'relative', overflow: 'hidden',
              }}>
                <div style={{ position: 'absolute', top: 0, left: 0, right: 0, height: 2, background: color }} />
                <div style={{
                  fontSize: 28, fontWeight: 800, color,
                  textShadow: `0 0 20px ${glow}`,
                  lineHeight: 1,
                }}>{count}</div>
                <div style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 5, textTransform: 'uppercase', letterSpacing: 1 }}>{label}</div>
              </div>
            ))}

            {assessment?.overall_level && (
              <div className="stat-card" style={{
                flex: 1,
                background: 'var(--bg-surface)',
                borderRadius: 14,
                padding: '18px 20px',
                border: '1px solid var(--border)',
                display: 'flex', flexDirection: 'column', alignItems: 'center', justifyContent: 'center',
                position: 'relative', overflow: 'hidden',
              }}>
                <div style={{ position: 'absolute', top: 0, left: 0, right: 0, height: 2, background: 'linear-gradient(90deg, var(--accent), #c4b5fd)' }} />
                <div style={{
                  fontSize: 15, fontWeight: 800, textTransform: 'capitalize',
                  color: assessment.overall_level === 'advanced' ? 'var(--green)'
                       : assessment.overall_level === 'intermediate' ? 'var(--yellow)' : 'var(--red)',
                }}>
                  {assessment.overall_level}
                </div>
                <div style={{ fontSize: 11, color: 'var(--text-muted)', marginTop: 5, textTransform: 'uppercase', letterSpacing: 1 }}>Level</div>
              </div>
            )}
          </div>
        </div>
      </div>

      {/* ── Body ───────────────────────────────────────────────────────────── */}
      <div style={{ maxWidth: 960, margin: '0 auto', padding: '24px 20px 40px' }}>

        {/* Study plan */}
        {showPlan && assessment?.study_plan && (
          <div style={{
            background: 'var(--bg-surface)', padding: 24, borderRadius: 12, marginBottom: 24,
            border: '1px solid var(--border)', lineHeight: 1.7, fontSize: 14,
          }}>
            <ReactMarkdown>{assessment.study_plan}</ReactMarkdown>
          </div>
        )}

        {/* Topic scores */}
        {assessment?.topic_scores && Object.keys(assessment.topic_scores).length > 0 && (
          <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginBottom: 20 }}>
            {Object.entries(assessment.topic_scores).map(([topic, score]: [string, any]) => (
              <div key={topic} style={{
                background: 'var(--bg-surface)',
                border: '1px solid var(--border)',
                padding: '5px 14px', borderRadius: 20, fontSize: 12,
                display: 'flex', gap: 8, alignItems: 'center',
              }}>
                <span style={{ color: 'var(--text-secondary)' }}>{topic}</span>
                <span style={{
                  fontWeight: 700,
                  color: score >= 70 ? 'var(--green)' : score >= 40 ? 'var(--yellow)' : 'var(--red)',
                }}>{score}</span>
              </div>
            ))}
          </div>
        )}

        {/* Tabs */}
        <div style={{ display: 'flex', gap: 4, marginBottom: 20, background: 'var(--bg-surface)', borderRadius: 10, padding: 4, border: '1px solid var(--border)', width: 'fit-content' }}>
          {(['coding', 'design'] as const).map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              style={{
                background: activeTab === tab ? 'linear-gradient(135deg, var(--accent), #8b5cf6)' : 'transparent',
                color: activeTab === tab ? '#fff' : 'var(--text-muted)',
                borderRadius: 7,
                padding: '7px 20px',
                fontSize: 13,
                fontWeight: 600,
                border: 'none',
                boxShadow: activeTab === tab ? '0 0 16px rgba(99,102,241,0.3)' : 'none',
                transform: 'none',
                transition: 'all 0.18s',
              }}
            >
              {tab === 'coding'
                ? `⌨️ Coding (${questions.length})`
                : `🏗️ System Design (${designTopics.length})`}
            </button>
          ))}
        </div>

        {activeTab === 'coding' && (
          <>
            {/* Filters row */}
            <div style={{ display: 'flex', gap: 8, flexWrap: 'wrap', marginBottom: 14, alignItems: 'center' }}>
              {[
                { value: difficulty, onChange: setDifficulty, options: [['','All difficulties'],['easy','Easy'],['medium','Medium'],['hard','Hard']] },
                { value: algorithm, onChange: setAlgorithm, options: [['','All algorithms'], ...filterOptions.algorithms.map(a => [a,a])] },
                { value: company,   onChange: setCompany,   options: [['','All companies'],  ...filterOptions.companies.map(c => [c,c])] },
                { value: frequency, onChange: setFrequency, options: [['','All frequencies'],['high','High'],['medium','Medium'],['low','Low']] },
              ].map(({ value, onChange, options }, i) => (
                <select
                  key={i}
                  value={value}
                  onChange={e => onChange(e.target.value)}
                  style={{
                    padding: '7px 12px', fontSize: 12, borderRadius: 8,
                    background: 'var(--bg-surface)', color: value ? 'var(--text-primary)' : 'var(--text-muted)',
                    border: `1px solid ${value ? 'var(--accent)' : 'var(--border)'}`,
                    outline: 'none',
                  }}
                >
                  {(options as [string,string][]).map(([v, label]) => <option key={v} value={v}>{label}</option>)}
                </select>
              ))}
              {(difficulty || algorithm || company || frequency || category) && (
                <button
                  onClick={() => { setDifficulty(''); setAlgorithm(''); setCompany(''); setFrequency(''); setCategory('') }}
                  style={{ fontSize: 11, color: 'var(--text-muted)', background: 'none', border: '1px solid var(--border)', padding: '5px 10px', borderRadius: 6 }}
                >
                  Clear ×
                </button>
              )}
              <button
                onClick={() => navigate('/coding')}
                style={{
                  marginLeft: 'auto',
                  background: 'var(--bg-surface)',
                  color: 'var(--accent-light)',
                  fontSize: 12, fontWeight: 600, padding: '7px 16px',
                  border: '1px solid var(--border-bright)', borderRadius: 8,
                }}
              >
                🎲 Random
              </button>
            </div>

            {/* Category pills */}
            <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap', marginBottom: 16 }}>
              {['', ...filterOptions.categories].map(cat => {
                const active = category === cat
                return (
                  <button
                    key={cat || '__all__'}
                    onClick={() => setCategory(cat === category ? '' : cat)}
                    style={{
                      padding: '5px 16px', borderRadius: 20, fontSize: 12, fontWeight: 600,
                      background: active ? 'linear-gradient(135deg, var(--accent), #8b5cf6)' : 'var(--bg-surface)',
                      color: active ? '#fff' : 'var(--text-muted)',
                      border: `1px solid ${active ? 'transparent' : 'var(--border)'}`,
                      boxShadow: active ? '0 0 14px rgba(99,102,241,0.3)' : 'none',
                      whiteSpace: 'nowrap',
                      transform: 'none',
                      transition: 'all 0.15s',
                    }}
                  >
                    {cat || 'All'}
                  </button>
                )
              })}
            </div>

            {/* Question table */}
            <div style={{ borderRadius: 12, overflow: 'hidden', border: '1px solid var(--border)', background: 'var(--bg-surface)' }}>
              {/* Header */}
              <div style={{
                display: 'grid', gridTemplateColumns: '44px 1fr auto 80px',
                padding: '10px 18px',
                background: 'rgba(99,102,241,0.06)',
                borderBottom: '1px solid var(--border)',
                fontSize: 10, fontWeight: 700, color: 'var(--text-muted)',
                textTransform: 'uppercase', letterSpacing: 1,
              }}>
                <span>#</span>
                <span>Problem</span>
                <span style={{ textAlign: 'right', paddingRight: 12 }}>Tags</span>
                <span style={{ textAlign: 'right' }}>Difficulty</span>
              </div>

              {/* Rows */}
              {questions.map((q, i) => (
                <button
                  key={q.id}
                  className="q-row"
                  onClick={() => navigate(`/coding?id=${q.id}`)}
                  style={{
                    display: 'grid', gridTemplateColumns: '44px 1fr auto 80px',
                    width: '100%',
                    background: 'transparent',
                    color: 'var(--text-primary)',
                    padding: '11px 18px',
                    textAlign: 'left',
                    borderRadius: 0,
                    borderBottom: i < questions.length - 1 ? '1px solid rgba(99,102,241,0.06)' : 'none',
                    alignItems: 'center',
                    transform: 'none',
                  }}
                >
                  {/* Status / number */}
                  <span style={{ fontSize: 13 }}>
                    {solved.has(q.id)
                      ? <span style={{ color: 'var(--green)', fontWeight: 800 }}>✓</span>
                      : <span style={{ color: 'var(--text-muted)', fontSize: 12 }}>{i + 1}</span>}
                  </span>

                  {/* Title */}
                  <span style={{ fontSize: 13.5, fontWeight: 500, display: 'flex', alignItems: 'center', gap: 7 }}>
                    <span style={{ color: solved.has(q.id) ? 'var(--text-secondary)' : 'var(--text-primary)' }}>
                      {q.title}
                    </span>
                    {q.frequency === 'high' && (
                      <span style={{
                        fontSize: 9, fontWeight: 800, letterSpacing: 0.5,
                        color: 'var(--red)', background: 'rgba(248,113,113,0.1)',
                        padding: '1px 6px', borderRadius: 4,
                      }}>HOT</span>
                    )}
                    {flagged.has(q.id) && (
                      <span title="Needs review" style={{ fontSize: 12 }}>🔖</span>
                    )}
                  </span>

                  {/* Tags */}
                  <div style={{ display: 'flex', gap: 5, justifyContent: 'flex-end', paddingRight: 12 }}>
                    {(q.companies || []).slice(0, 2).map((c: string) => (
                      <span key={c} style={{
                        fontSize: 10, fontWeight: 600,
                        color: 'var(--accent-light)', background: 'var(--accent-dim)',
                        padding: '2px 7px', borderRadius: 4,
                      }}>{c}</span>
                    ))}
                    {q.tags.slice(0, 2).map((t: string) => (
                      <span key={t} style={{
                        fontSize: 10, color: 'var(--text-muted)',
                        background: 'rgba(99,102,241,0.06)',
                        border: '1px solid var(--border)',
                        padding: '2px 7px', borderRadius: 4,
                      }}>{t}</span>
                    ))}
                  </div>

                  {/* Difficulty */}
                  <span style={{
                    color: diffColor(q.difficulty), fontWeight: 700, fontSize: 11,
                    textAlign: 'right', background: diffBg(q.difficulty),
                    padding: '3px 10px', borderRadius: 6, justifySelf: 'end',
                    textTransform: 'capitalize',
                  }}>
                    {q.difficulty}
                  </span>
                </button>
              ))}

              {questions.length === 0 && (
                <div style={{ padding: '32px', textAlign: 'center', color: 'var(--text-muted)', fontSize: 13 }}>
                  No questions match your filters.
                </div>
              )}
            </div>
          </>
        )}

        {activeTab === 'design' && (
          <div style={{ borderRadius: 12, overflow: 'hidden', border: '1px solid var(--border)', background: 'var(--bg-surface)' }}>
            {designTopics.map((t, i) => (
              <button
                key={t.id}
                className="q-row"
                onClick={() => navigate(`/system-design?topic=${encodeURIComponent(t.title)}`)}
                style={{
                  width: '100%', background: 'transparent',
                  color: 'var(--text-primary)', padding: '14px 20px',
                  textAlign: 'left', borderRadius: 0,
                  borderBottom: i < designTopics.length - 1 ? '1px solid rgba(99,102,241,0.06)' : 'none',
                  fontSize: 14, display: 'flex', alignItems: 'center', gap: 14, transform: 'none',
                }}
              >
                <span style={{
                  color: 'var(--accent-light)', background: 'var(--accent-dim)',
                  fontSize: 11, fontWeight: 700, minWidth: 22, height: 22,
                  display: 'flex', alignItems: 'center', justifyContent: 'center',
                  borderRadius: 6,
                }}>{i + 1}</span>
                <span>{t.title}</span>
              </button>
            ))}
            <button
              onClick={() => navigate('/system-design')}
              style={{
                width: '100%',
                background: 'linear-gradient(135deg, var(--accent), #8b5cf6)',
                color: '#fff', padding: '14px 20px', fontWeight: 700,
                fontSize: 14, borderRadius: '0 0 12px 12px', border: 'none',
                boxShadow: '0 0 20px rgba(99,102,241,0.25)',
                transform: 'none',
              }}
            >
              🎲 Random Topic
            </button>
          </div>
        )}
      </div>
    </div>
  )
}
