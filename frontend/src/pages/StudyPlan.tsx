import { useState, useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { getStudyPlans, getStudyPlan, getStudyProgress, markQuestionComplete } from '../api/client'

export default function StudyPlan() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const planId = searchParams.get('plan')

  const [plans, setPlans] = useState<any[]>([])
  const [activePlan, setActivePlan] = useState<any>(null)
  const [progress, setProgress] = useState<any>(null)
  const [expandedWeek, setExpandedWeek] = useState<number>(1)

  useEffect(() => {
    getStudyPlans().then(setPlans).catch(() => {})
  }, [])

  useEffect(() => {
    if (planId) {
      getStudyPlan(planId).then(setActivePlan).catch(() => {})
      getStudyProgress(planId).then(setProgress).catch(() => {})
    }
  }, [planId])

  const completed = new Set(progress?.completed || [])

  const totalQuestions = activePlan?.weeks?.reduce(
    (sum: number, w: any) => sum + w.days.reduce((s: number, d: any) => s + d.question_ids.length, 0), 0
  ) || 0
  const completedCount = activePlan?.weeks?.reduce(
    (sum: number, w: any) => sum + w.days.reduce(
      (s: number, d: any) => s + d.question_ids.filter((id: string) => completed.has(id)).length, 0
    ), 0
  ) || 0
  const progressPct = totalQuestions > 0 ? Math.round((completedCount / totalQuestions) * 100) : 0

  const handleMarkComplete = async (questionId: string) => {
    if (planId && !completed.has(questionId)) {
      const updated = await markQuestionComplete(planId, questionId)
      setProgress(updated)
    }
  }

  const difficultyColor = (d: string) =>
    d === 'easy' ? 'var(--green)' : d === 'medium' ? 'var(--yellow)' : 'var(--red)'

  // Plan selection view
  if (!planId) {
    return (
      <div style={{ height: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '40px 20px', overflowY: 'auto' }}>
        <div style={{ width: '100%', maxWidth: 800 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 32 }}>
            <button onClick={() => navigate('/')} style={{ background: 'var(--bg-surface)', color: 'var(--text-primary)', fontSize: 13, padding: '6px 14px' }}>
              Back
            </button>
            <h1 style={{ fontSize: 28, fontWeight: 700 }}>Study Plans</h1>
          </div>
          <p style={{ color: 'var(--text-secondary)', fontSize: 14, marginBottom: 24 }}>
            Pick a plan based on your timeline. Each plan has daily problem sets organized by topic with increasing difficulty.
          </p>

          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            {plans.map(p => (
              <button
                key={p.id}
                onClick={() => navigate(`/study?plan=${p.id}`)}
                style={{
                  background: 'var(--bg-surface)',
                  color: 'var(--text-primary)',
                  padding: '24px',
                  textAlign: 'left',
                  borderRadius: 12,
                  border: '1px solid transparent',
                }}
              >
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'flex-start', marginBottom: 8 }}>
                  <h3 style={{ fontSize: 18, fontWeight: 600 }}>{p.title}</h3>
                  <div style={{ display: 'flex', gap: 8 }}>
                    <span style={{ fontSize: 12, background: 'rgba(99,102,241,0.15)', color: 'var(--accent)', padding: '3px 10px', borderRadius: 4, fontWeight: 600 }}>
                      {p.duration_weeks} weeks
                    </span>
                    <span style={{ fontSize: 12, background: 'var(--bg-hover)', color: 'var(--text-secondary)', padding: '3px 10px', borderRadius: 4 }}>
                      {p.total_questions} problems
                    </span>
                  </div>
                </div>
                <p style={{ color: 'var(--text-secondary)', fontSize: 13, lineHeight: 1.5 }}>{p.description}</p>
                <div style={{ marginTop: 12, fontSize: 12, color: 'var(--text-muted)' }}>
                  {p.questions_per_day} problems/day · ~1 hour daily
                </div>
              </button>
            ))}
          </div>
        </div>
      </div>
    )
  }

  // Active plan view
  if (!activePlan) {
    return <div style={{ padding: 40, textAlign: 'center', color: 'var(--text-secondary)' }}>Loading plan...</div>
  }

  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '40px 20px', overflowY: 'auto' }}>
      <div style={{ width: '100%', maxWidth: 800 }}>
        {/* Header */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 8 }}>
          <button onClick={() => navigate('/study')} style={{ background: 'var(--bg-surface)', color: 'var(--text-primary)', fontSize: 13, padding: '6px 14px' }}>
            Back
          </button>
          <h1 style={{ fontSize: 24, fontWeight: 700 }}>{activePlan.title}</h1>
        </div>
        <p style={{ color: 'var(--text-secondary)', fontSize: 13, marginBottom: 16 }}>{activePlan.description}</p>

        {/* Progress bar */}
        <div style={{ marginBottom: 24 }}>
          <div style={{ display: 'flex', justifyContent: 'space-between', fontSize: 13, marginBottom: 6 }}>
            <span style={{ color: 'var(--text-secondary)' }}>{completedCount} / {totalQuestions} completed</span>
            <span style={{ fontWeight: 600, color: progressPct === 100 ? 'var(--green)' : 'var(--accent)' }}>{progressPct}%</span>
          </div>
          <div style={{ height: 8, background: 'var(--bg-surface)', borderRadius: 4, overflow: 'hidden' }}>
            <div style={{
              height: '100%',
              width: `${progressPct}%`,
              background: progressPct === 100 ? 'var(--green)' : 'var(--accent)',
              borderRadius: 4,
              transition: 'width 0.3s ease',
            }} />
          </div>
        </div>

        {/* Weeks */}
        {activePlan.weeks.map((week: any) => {
          const weekCompleted = week.days.reduce(
            (s: number, d: any) => s + d.question_ids.filter((id: string) => completed.has(id)).length, 0
          )
          const weekTotal = week.days.reduce((s: number, d: any) => s + d.question_ids.length, 0)
          const isExpanded = expandedWeek === week.week

          return (
            <div key={week.week} style={{ marginBottom: 12 }}>
              {/* Week header */}
              <button
                onClick={() => setExpandedWeek(isExpanded ? 0 : week.week)}
                style={{
                  width: '100%',
                  background: isExpanded
                    ? 'linear-gradient(135deg, rgba(99,102,241,0.15), rgba(139,92,246,0.1))'
                    : 'var(--bg-surface)',
                  border: isExpanded ? '1px solid rgba(99,102,241,0.3)' : '1px solid transparent',
                  color: 'var(--text-primary)',
                  padding: '14px 18px',
                  textAlign: 'left',
                  borderRadius: isExpanded ? '12px 12px 0 0' : 12,
                  display: 'flex',
                  justifyContent: 'space-between',
                  alignItems: 'center',
                }}
              >
                <div>
                  <span style={{ fontWeight: 600, fontSize: 15 }}>Week {week.week}: </span>
                  <span style={{ fontSize: 14, color: 'var(--text-secondary)' }}>{week.theme}</span>
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                  <span style={{
                    fontSize: 12,
                    color: weekCompleted === weekTotal && weekTotal > 0 ? 'var(--green)' : 'var(--text-muted)',
                    fontWeight: 600,
                  }}>
                    {weekCompleted}/{weekTotal}
                  </span>
                  <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>{isExpanded ? '▲' : '▼'}</span>
                </div>
              </button>

              {/* Days */}
              {isExpanded && (
                <div style={{
                  background: 'var(--bg-surface)',
                  borderRadius: '0 0 12px 12px',
                  padding: '4px 0',
                  borderTop: '1px solid var(--bg-hover)',
                }}>
                  {week.days.map((day: any) => (
                    <div key={day.day} style={{ padding: '10px 18px' }}>
                      <div style={{ fontSize: 12, fontWeight: 600, color: 'var(--text-muted)', marginBottom: 6 }}>
                        Day {day.day} — {day.topic}
                      </div>
                      {day.question_ids.length === 0 ? (
                        <div style={{ fontSize: 13, color: 'var(--text-muted)', fontStyle: 'italic', padding: '4px 0' }}>
                          Rest day — review previous problems
                        </div>
                      ) : (
                        <div style={{ display: 'flex', flexDirection: 'column', gap: 4 }}>
                          {day.question_ids.map((qid: string) => {
                            const isDone = completed.has(qid)
                            return (
                              <div
                                key={qid}
                                style={{
                                  display: 'flex',
                                  alignItems: 'center',
                                  gap: 10,
                                  padding: '8px 12px',
                                  background: isDone ? 'rgba(34,197,94,0.08)' : 'var(--bg-hover)',
                                  borderRadius: 8,
                                }}
                              >
                                <button
                                  onClick={(e) => { e.stopPropagation(); handleMarkComplete(qid) }}
                                  style={{
                                    width: 20,
                                    height: 20,
                                    borderRadius: 4,
                                    border: isDone ? '2px solid var(--green)' : '2px solid var(--text-muted)',
                                    background: isDone ? 'var(--green)' : 'transparent',
                                    color: isDone ? '#fff' : 'transparent',
                                    fontSize: 12,
                                    display: 'flex',
                                    alignItems: 'center',
                                    justifyContent: 'center',
                                    padding: 0,
                                    cursor: isDone ? 'default' : 'pointer',
                                    flexShrink: 0,
                                  }}
                                >
                                  {isDone ? '✓' : ''}
                                </button>
                                <button
                                  onClick={() => navigate(`/coding?id=${qid}`)}
                                  style={{
                                    flex: 1,
                                    background: 'none',
                                    color: isDone ? 'var(--text-muted)' : 'var(--text-primary)',
                                    textAlign: 'left',
                                    padding: 0,
                                    fontSize: 13,
                                    textDecoration: isDone ? 'line-through' : 'none',
                                  }}
                                >
                                  {qid.replace(/-/g, ' ').replace(/\b\w/g, c => c.toUpperCase())}
                                </button>
                              </div>
                            )
                          })}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>
          )
        })}
      </div>
    </div>
  )
}
