import { useState, useEffect } from 'react'
import { useNavigate, useSearchParams } from 'react-router-dom'
import { getStudyPlans, getStudyPlan, getStudyProgress, markQuestionComplete, startStudyPlan } from '../api/client'

export default function StudyPlan() {
  const navigate = useNavigate()
  const [searchParams] = useSearchParams()
  const planId = searchParams.get('plan')

  const [plans, setPlans] = useState<any[]>([])
  const [activePlan, setActivePlan] = useState<any>(null)
  const [progress, setProgress] = useState<any>(null)
  const [expandedWeek, setExpandedWeek] = useState<number>(1)
  const [questions, setQuestions] = useState<Record<string, string>>({}) // id → title cache

  useEffect(() => {
    getStudyPlans().then(setPlans).catch(() => {})
  }, [])

  useEffect(() => {
    if (!planId) return
    getStudyPlan(planId).then(plan => {
      setActivePlan(plan)
      // Build id→title map from all question_ids (use id as fallback title)
      const ids: Record<string, string> = {}
      for (const week of plan.weeks ?? []) {
        for (const day of week.days ?? []) {
          for (const qid of day.question_ids ?? []) {
            ids[qid] = qid.replace(/-/g, ' ').replace(/\b\w/g, (c: string) => c.toUpperCase())
          }
        }
      }
      setQuestions(ids)
    }).catch(() => {})

    // Auto-start plan (idempotent — won't overwrite if already started)
    startStudyPlan(planId)
      .then(prog => {
        setProgress(prog)
        setExpandedWeek(prog.current_week_num || 1)
      })
      .catch(() => {
        getStudyProgress(planId).then(prog => {
          setProgress(prog)
          setExpandedWeek(prog.current_week_num || 1)
        }).catch(() => {})
      })
  }, [planId])

  const completed = new Set<string>(progress?.completed || [])

  const handleMarkComplete = async (questionId: string) => {
    if (!planId) return
    const updated = await markQuestionComplete(planId, questionId)
    setProgress(updated)
  }

  const goToQuestion = (qid: string) =>
    navigate(`/coding?id=${qid}&from=study&plan=${planId}`)

  // ── Plan list view ──────────────────────────────────────────────────────────
  if (!planId) {
    return (
      <div style={{ height: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '40px 20px', overflowY: 'auto', background: 'var(--bg-primary)' }}>
        <div style={{ width: '100%', maxWidth: 800 }}>
          <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 32 }}>
            <button onClick={() => navigate('/')} style={{ background: 'var(--bg-surface)', color: 'var(--text-primary)', fontSize: 13, padding: '6px 14px', borderRadius: 6 }}>
              ← Back
            </button>
            <h1 style={{ fontSize: 28, fontWeight: 700 }}>Study Plans</h1>
          </div>
          <p style={{ color: 'var(--text-secondary)', fontSize: 14, marginBottom: 24 }}>
            Pick a plan based on your timeline. Commit to it — the streak tracker will keep you honest.
          </p>
          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            {plans.map(p => (
              <button
                key={p.id}
                onClick={() => navigate(`/study?plan=${p.id}`)}
                style={{ background: 'var(--bg-surface)', color: 'var(--text-primary)', padding: 24, textAlign: 'left', borderRadius: 12, border: '1px solid var(--border)' }}
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

  if (!activePlan || !progress) {
    return <div style={{ padding: 40, textAlign: 'center', color: 'var(--text-secondary)' }}>Loading plan...</div>
  }

  // ── Derived stats ──────────────────────────────────────────────────────────
  const totalQuestions = activePlan.weeks?.reduce(
    (s: number, w: any) => s + w.days.reduce((d: number, day: any) => d + day.question_ids.length, 0), 0
  ) || 0
  const completedCount = [...completed].filter(id =>
    activePlan.weeks?.some((w: any) => w.days.some((d: any) => d.question_ids.includes(id)))
  ).length
  const progressPct = totalQuestions > 0 ? Math.round((completedCount / totalQuestions) * 100) : 0

  const streak: number = progress.streak || 0
  const pastIncomplete: number = progress.past_incomplete_count || 0
  const currentDayNum: number = progress.current_day_num || 1
  const totalPlanDays: number = progress.total_plan_days || 0
  const todayDay: any = progress.today_day
  const todayQids: string[] = progress.today_question_ids || []
  const planFinished: boolean = progress.plan_finished || false

  const todayAllDone = todayQids.length > 0 && todayQids.every(id => completed.has(id))

  // Status label
  let statusLabel = ''
  let statusColor = 'var(--green)'
  if (planFinished) {
    statusLabel = '🎉 Plan complete!'
    statusColor = 'var(--green)'
  } else if (pastIncomplete === 0) {
    statusLabel = '✓ On track'
    statusColor = 'var(--green)'
  } else if (pastIncomplete <= 3) {
    statusLabel = `${pastIncomplete} problem${pastIncomplete > 1 ? 's' : ''} behind`
    statusColor = 'var(--yellow)'
  } else {
    statusLabel = `${pastIncomplete} problems behind`
    statusColor = 'var(--red)'
  }

  // Day status helpers for the timeline
  const flatDays: any[] = []
  for (const week of activePlan.weeks ?? []) {
    for (const day of week.days ?? []) {
      flatDays.push({ ...day, week_num: week.week })
    }
  }

  function dayStatus(globalDayIdx: number): 'done' | 'partial' | 'today' | 'overdue' | 'future' {
    const day = flatDays[globalDayIdx]
    if (!day || day.question_ids.length === 0) return 'done' // rest day
    const allDone = day.question_ids.every((id: string) => completed.has(id))
    const anyDone = day.question_ids.some((id: string) => completed.has(id))
    const elapsed = progress.days_elapsed ?? (currentDayNum - 1)
    if (globalDayIdx < elapsed) {
      return allDone ? 'done' : anyDone ? 'partial' : 'overdue'
    }
    if (globalDayIdx === elapsed) return 'today'
    return 'future'
  }

  // ── Render ──────────────────────────────────────────────────────────────────
  return (
    <div style={{ height: '100vh', display: 'flex', flexDirection: 'column', alignItems: 'center', padding: '32px 20px', overflowY: 'auto', background: 'var(--bg-primary)' }}>
      <div style={{ width: '100%', maxWidth: 800 }}>

        {/* Header */}
        <div style={{ display: 'flex', alignItems: 'center', gap: 12, marginBottom: 6 }}>
          <button onClick={() => navigate('/study')} style={{ background: 'var(--bg-surface)', color: 'var(--text-primary)', fontSize: 13, padding: '6px 14px', borderRadius: 6 }}>
            ← Plans
          </button>
          <h1 style={{ fontSize: 22, fontWeight: 700 }}>{activePlan.title}</h1>
        </div>

        {/* Motivation bar */}
        <div style={{
          display: 'flex', alignItems: 'center', gap: 20, marginBottom: 20, marginTop: 16,
          background: 'var(--bg-surface)', borderRadius: 12, padding: '14px 20px',
          border: '1px solid var(--border)',
        }}>
          {/* Streak */}
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', minWidth: 60 }}>
            <span style={{ fontSize: 22, lineHeight: 1 }}>
              {streak >= 1 ? '🔥' : '💤'}
            </span>
            <span style={{ fontSize: 13, fontWeight: 700, color: streak >= 1 ? 'var(--accent)' : 'var(--text-muted)', marginTop: 3 }}>
              {streak} day{streak !== 1 ? 's' : ''}
            </span>
            <span style={{ fontSize: 10, color: 'var(--text-muted)', marginTop: 1 }}>streak</span>
          </div>

          <div style={{ width: 1, height: 40, background: 'var(--border)' }} />

          {/* Day progress */}
          <div style={{ flex: 1 }}>
            <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'baseline', marginBottom: 6 }}>
              <span style={{ fontSize: 13, fontWeight: 600, color: 'var(--text-primary)' }}>
                {planFinished ? 'Completed!' : `Day ${currentDayNum} of ${totalPlanDays}`}
                {todayDay && !planFinished && (
                  <span style={{ fontSize: 12, color: 'var(--text-muted)', fontWeight: 400, marginLeft: 8 }}>
                    · {todayDay.topic}
                  </span>
                )}
              </span>
              <span style={{ fontSize: 12, fontWeight: 600, color: progressPct === 100 ? 'var(--green)' : 'var(--accent)' }}>
                {completedCount}/{totalQuestions} solved
              </span>
            </div>
            <div style={{ height: 6, background: 'var(--bg-hover)', borderRadius: 3, overflow: 'hidden' }}>
              <div style={{
                height: '100%', width: `${progressPct}%`,
                background: progressPct === 100 ? 'var(--green)' : 'linear-gradient(90deg, var(--accent), #8b5cf6)',
                borderRadius: 3, transition: 'width 0.4s ease',
              }} />
            </div>
          </div>

          <div style={{ width: 1, height: 40, background: 'var(--border)' }} />

          {/* Status */}
          <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', minWidth: 80 }}>
            <span style={{ fontSize: 12, fontWeight: 700, color: statusColor, textAlign: 'center' }}>{statusLabel}</span>
            {pastIncomplete > 0 && (
              <span style={{ fontSize: 10, color: 'var(--text-muted)', marginTop: 2 }}>catch up!</span>
            )}
          </div>
        </div>

        {/* ── Today's Mission ── */}
        {!planFinished && todayDay && (
          <div style={{
            marginBottom: 24,
            background: todayAllDone
              ? 'rgba(34,197,94,0.06)'
              : 'rgba(99,102,241,0.06)',
            border: `1px solid ${todayAllDone ? 'rgba(34,197,94,0.3)' : 'rgba(99,102,241,0.3)'}`,
            borderRadius: 12,
            overflow: 'hidden',
          }}>
            {/* Card header */}
            <div style={{
              padding: '12px 18px',
              background: todayAllDone ? 'rgba(34,197,94,0.1)' : 'rgba(99,102,241,0.1)',
              borderBottom: `1px solid ${todayAllDone ? 'rgba(34,197,94,0.2)' : 'rgba(99,102,241,0.2)'}`,
              display: 'flex', alignItems: 'center', justifyContent: 'space-between',
            }}>
              <div>
                <span style={{ fontSize: 11, fontWeight: 700, color: todayAllDone ? 'var(--green)' : 'var(--accent)', textTransform: 'uppercase', letterSpacing: 0.5 }}>
                  {todayAllDone ? '✓ Today Complete' : "Today's Mission"}
                </span>
                <span style={{ fontSize: 13, color: 'var(--text-secondary)', marginLeft: 10 }}>
                  Week {todayDay.week_num} · Day {todayDay.day} · {todayDay.topic}
                </span>
              </div>
              {!todayAllDone && (
                <span style={{ fontSize: 12, color: 'var(--text-muted)' }}>
                  {todayQids.filter(id => completed.has(id)).length}/{todayQids.length} done
                </span>
              )}
            </div>

            {/* Questions */}
            {todayQids.length === 0 ? (
              <div style={{ padding: '16px 18px', fontSize: 13, color: 'var(--text-muted)', fontStyle: 'italic' }}>
                Rest day — review your solutions from the week.
              </div>
            ) : (
              <div style={{ padding: '10px 12px', display: 'flex', flexDirection: 'column', gap: 6 }}>
                {todayQids.map(qid => {
                  const isDone = completed.has(qid)
                  return (
                    <div key={qid} style={{
                      display: 'flex', alignItems: 'center', gap: 10,
                      padding: '10px 14px', borderRadius: 8,
                      background: isDone ? 'rgba(34,197,94,0.08)' : 'var(--bg-surface)',
                    }}>
                      <button
                        onClick={() => handleMarkComplete(qid)}
                        style={{
                          width: 22, height: 22, borderRadius: 5, flexShrink: 0,
                          border: isDone ? '2px solid var(--green)' : '2px solid var(--text-muted)',
                          background: isDone ? 'var(--green)' : 'transparent',
                          color: isDone ? '#000' : 'transparent',
                          fontSize: 12, fontWeight: 700, padding: 0,
                          cursor: 'pointer',
                          display: 'flex', alignItems: 'center', justifyContent: 'center',
                        }}
                      >{isDone ? '✓' : ''}</button>
                      <span style={{
                        flex: 1, fontSize: 14, fontWeight: 500,
                        color: isDone ? 'var(--text-muted)' : 'var(--text-primary)',
                        textDecoration: isDone ? 'line-through' : 'none',
                      }}>
                        {questions[qid] || qid}
                      </span>
                      {!isDone && (
                        <button
                          onClick={() => goToQuestion(qid)}
                          style={{
                            background: 'var(--accent)', color: '#fff',
                            fontSize: 12, fontWeight: 600,
                            padding: '5px 14px', borderRadius: 6, border: 'none', cursor: 'pointer',
                          }}
                        >
                          Solve →
                        </button>
                      )}
                    </div>
                  )
                })}
              </div>
            )}
          </div>
        )}

        {/* Plan finished celebration */}
        {planFinished && (
          <div style={{
            marginBottom: 24, padding: 24, borderRadius: 12,
            background: 'rgba(34,197,94,0.1)', border: '1px solid rgba(34,197,94,0.3)',
            textAlign: 'center',
          }}>
            <div style={{ fontSize: 36, marginBottom: 8 }}>🎉</div>
            <div style={{ fontSize: 18, fontWeight: 700, color: 'var(--green)', marginBottom: 6 }}>
              Plan Complete!
            </div>
            <div style={{ fontSize: 13, color: 'var(--text-secondary)' }}>
              You finished all {totalQuestions} problems. Time to pick a harder plan or revisit your weak spots.
            </div>
            <button
              onClick={() => navigate('/study')}
              style={{ marginTop: 16, background: 'var(--accent)', color: '#fff', fontWeight: 600, fontSize: 13, padding: '8px 20px', borderRadius: 8, border: 'none', cursor: 'pointer' }}
            >
              Browse Plans →
            </button>
          </div>
        )}

        {/* Overdue catch-up banner */}
        {!planFinished && pastIncomplete > 0 && (
          <div style={{
            marginBottom: 18, padding: '10px 16px', borderRadius: 8,
            background: pastIncomplete > 3 ? 'rgba(239,68,68,0.1)' : 'rgba(234,179,8,0.1)',
            border: `1px solid ${pastIncomplete > 3 ? 'rgba(239,68,68,0.3)' : 'rgba(234,179,8,0.3)'}`,
            display: 'flex', alignItems: 'center', gap: 10, fontSize: 13,
          }}>
            <span style={{ fontSize: 16 }}>{pastIncomplete > 3 ? '🔴' : '🟡'}</span>
            <span style={{ color: 'var(--text-primary)', flex: 1 }}>
              You have <strong>{pastIncomplete} problem{pastIncomplete > 1 ? 's' : ''}</strong> from past days that aren't done yet. Scroll down to catch up.
            </span>
          </div>
        )}

        {/* ── Weekly accordion ── */}
        {activePlan.weeks.map((week: any) => {
          let globalDayOffset = 0
          for (const w of activePlan.weeks) {
            if (w.week === week.week) break
            globalDayOffset += w.days.length
          }

          const weekDone = week.days.reduce(
            (s: number, d: any) => s + d.question_ids.filter((id: string) => completed.has(id)).length, 0
          )
          const weekTotal = week.days.reduce((s: number, d: any) => s + d.question_ids.length, 0)
          const isExpanded = expandedWeek === week.week

          // Does this week contain today?
          const weekContainsToday = week.week === (todayDay?.week_num ?? -1)

          return (
            <div key={week.week} style={{ marginBottom: 10 }}>
              <button
                onClick={() => setExpandedWeek(isExpanded ? 0 : week.week)}
                style={{
                  width: '100%',
                  background: weekContainsToday
                    ? 'linear-gradient(135deg, rgba(99,102,241,0.18), rgba(139,92,246,0.12))'
                    : isExpanded ? 'var(--bg-surface)' : 'var(--bg-surface)',
                  border: weekContainsToday ? '1px solid rgba(99,102,241,0.4)' : '1px solid var(--border)',
                  color: 'var(--text-primary)',
                  padding: '13px 18px',
                  textAlign: 'left',
                  borderRadius: isExpanded ? '10px 10px 0 0' : 10,
                  display: 'flex', justifyContent: 'space-between', alignItems: 'center',
                  cursor: 'pointer',
                }}
              >
                <div>
                  <span style={{ fontWeight: 700, fontSize: 14 }}>Week {week.week}</span>
                  <span style={{ fontSize: 13, color: 'var(--text-secondary)', marginLeft: 8 }}>{week.theme}</span>
                  {weekContainsToday && (
                    <span style={{ fontSize: 10, fontWeight: 700, color: 'var(--accent)', background: 'rgba(99,102,241,0.15)', padding: '1px 7px', borderRadius: 10, marginLeft: 8 }}>
                      THIS WEEK
                    </span>
                  )}
                </div>
                <div style={{ display: 'flex', alignItems: 'center', gap: 10 }}>
                  <span style={{
                    fontSize: 12, fontWeight: 600,
                    color: weekDone === weekTotal && weekTotal > 0 ? 'var(--green)' : 'var(--text-muted)',
                  }}>
                    {weekDone}/{weekTotal}
                  </span>
                  <span style={{ fontSize: 11, color: 'var(--text-muted)' }}>{isExpanded ? '▲' : '▼'}</span>
                </div>
              </button>

              {isExpanded && (
                <div style={{
                  background: 'var(--bg-surface)',
                  borderRadius: '0 0 10px 10px',
                  border: '1px solid var(--border)',
                  borderTop: 'none',
                  padding: '6px 0',
                }}>
                  {week.days.map((day: any, dayLocalIdx: number) => {
                    const globalIdx = globalDayOffset + dayLocalIdx
                    const status = dayStatus(globalIdx)
                    const allDone = day.question_ids.every((id: string) => completed.has(id))

                    const statusIcon =
                      day.question_ids.length === 0 ? '—'
                      : status === 'done' ? '✅'
                      : status === 'partial' ? '🔶'
                      : status === 'overdue' ? '🔴'
                      : status === 'today' ? '▶'
                      : '○'

                    const isToday = status === 'today'

                    return (
                      <div
                        key={day.day}
                        style={{
                          padding: '10px 18px',
                          background: isToday ? 'rgba(99,102,241,0.06)' : 'transparent',
                          borderLeft: isToday ? '3px solid var(--accent)' : '3px solid transparent',
                        }}
                      >
                        <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: day.question_ids.length > 0 ? 6 : 0 }}>
                          <span style={{ fontSize: 14, minWidth: 20 }}>{statusIcon}</span>
                          <span style={{
                            fontSize: 12, fontWeight: 700,
                            color: isToday ? 'var(--accent)' : status === 'overdue' ? 'var(--red)' : 'var(--text-muted)',
                          }}>
                            Day {day.day}
                          </span>
                          <span style={{ fontSize: 12, color: 'var(--text-secondary)' }}>— {day.topic}</span>
                        </div>

                        {day.question_ids.length > 0 && (
                          <div style={{ display: 'flex', flexDirection: 'column', gap: 4, paddingLeft: 28 }}>
                            {day.question_ids.map((qid: string) => {
                              const isDone = completed.has(qid)
                              return (
                                <div key={qid} style={{ display: 'flex', alignItems: 'center', gap: 8, padding: '6px 10px', background: isDone ? 'rgba(34,197,94,0.07)' : 'var(--bg-hover)', borderRadius: 6 }}>
                                  <button
                                    onClick={(e) => { e.stopPropagation(); handleMarkComplete(qid) }}
                                    style={{
                                      width: 18, height: 18, borderRadius: 4, flexShrink: 0,
                                      border: isDone ? '2px solid var(--green)' : '2px solid var(--text-muted)',
                                      background: isDone ? 'var(--green)' : 'transparent',
                                      color: isDone ? '#000' : 'transparent', fontSize: 10, fontWeight: 700,
                                      padding: 0, cursor: 'pointer',
                                      display: 'flex', alignItems: 'center', justifyContent: 'center',
                                    }}
                                  >{isDone ? '✓' : ''}</button>
                                  <button
                                    onClick={() => goToQuestion(qid)}
                                    style={{
                                      flex: 1, background: 'none',
                                      color: isDone ? 'var(--text-muted)' : 'var(--text-primary)',
                                      textAlign: 'left', padding: 0, fontSize: 13,
                                      textDecoration: isDone ? 'line-through' : 'none',
                                    }}
                                  >
                                    {questions[qid] || qid}
                                  </button>
                                  {!isDone && (isToday || status === 'overdue') && (
                                    <button
                                      onClick={() => goToQuestion(qid)}
                                      style={{
                                        background: isToday ? 'var(--accent)' : 'rgba(239,68,68,0.15)',
                                        color: isToday ? '#fff' : 'var(--red)',
                                        fontSize: 11, fontWeight: 600,
                                        padding: '3px 10px', borderRadius: 5, border: 'none', cursor: 'pointer',
                                      }}
                                    >
                                      {isToday ? 'Start' : 'Catch up'}
                                    </button>
                                  )}
                                </div>
                              )
                            })}
                          </div>
                        )}
                        {day.question_ids.length === 0 && (
                          <div style={{ paddingLeft: 28, fontSize: 12, color: 'var(--text-muted)', fontStyle: 'italic' }}>
                            Rest day — review previous solutions
                          </div>
                        )}
                      </div>
                    )
                  })}
                </div>
              )}
            </div>
          )
        })}

      </div>
    </div>
  )
}
