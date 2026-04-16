import { useState } from 'react'
import { useNavigate } from 'react-router-dom'
import { createProfile } from '../api/client'

export default function Onboarding() {
  const navigate = useNavigate()
  const [step, setStep] = useState(1)
  const [form, setForm] = useState({
    name: '',
    email: '',
    linkedin_url: '',
    resume_text: '',
    target_role: '',
    target_companies: '',
    years_of_experience: '',
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const update = (field: string, value: string) =>
    setForm(prev => ({ ...prev, [field]: value }))

  const handleSubmit = async () => {
    if (!form.name.trim()) {
      setError('Name is required')
      return
    }
    setLoading(true)
    setError('')
    try {
      const profile = await createProfile({
        name: form.name,
        email: form.email || undefined,
        linkedin_url: form.linkedin_url || undefined,
        resume_text: form.resume_text || undefined,
        target_role: form.target_role || undefined,
        target_companies: form.target_companies
          ? form.target_companies.split(',').map(s => s.trim())
          : [],
        years_of_experience: form.years_of_experience
          ? parseInt(form.years_of_experience)
          : undefined,
      })
      localStorage.setItem('userId', profile.user_id)
      localStorage.setItem('userName', profile.name)
      navigate('/assessment')
    } catch {
      setError('Failed to create profile. Is the backend running?')
    }
    setLoading(false)
  }

  const inputStyle = {
    width: '100%',
    padding: '10px 14px',
    fontSize: 14,
    marginBottom: 12,
  }

  const labelStyle = {
    display: 'block' as const,
    fontSize: 13,
    color: 'var(--text-secondary)',
    marginBottom: 4,
  }

  return (
    <div style={{
      height: '100vh',
      display: 'flex',
      alignItems: 'center',
      justifyContent: 'center',
      padding: 20,
    }}>
      <div style={{ width: '100%', maxWidth: 500 }}>
        <h1 style={{ fontSize: 28, fontWeight: 700, marginBottom: 8 }}>
          Welcome to Interview Coach
        </h1>
        <p style={{ color: 'var(--text-secondary)', marginBottom: 32 }}>
          Let's set up your profile so the AI coach can tailor your experience.
        </p>

        {step === 1 && (
          <>
            <label style={labelStyle}>Name *</label>
            <input
              style={inputStyle}
              value={form.name}
              onChange={e => update('name', e.target.value)}
              placeholder="Your name"
            />

            <label style={labelStyle}>Email</label>
            <input
              style={inputStyle}
              value={form.email}
              onChange={e => update('email', e.target.value)}
              placeholder="your@email.com"
            />

            <label style={labelStyle}>Years of Experience</label>
            <input
              style={inputStyle}
              type="number"
              value={form.years_of_experience}
              onChange={e => update('years_of_experience', e.target.value)}
              placeholder="e.g. 3"
            />

            <label style={labelStyle}>Target Role</label>
            <input
              style={inputStyle}
              value={form.target_role}
              onChange={e => update('target_role', e.target.value)}
              placeholder="e.g. Senior SDE, Staff Engineer"
            />

            <label style={labelStyle}>Target Companies (comma-separated)</label>
            <input
              style={inputStyle}
              value={form.target_companies}
              onChange={e => update('target_companies', e.target.value)}
              placeholder="e.g. Google, Meta, Amazon"
            />

            <button
              onClick={() => setStep(2)}
              disabled={!form.name.trim()}
              style={{
                width: '100%',
                background: 'var(--accent)',
                color: 'var(--bg-primary)',
                padding: '12px',
                fontWeight: 600,
                fontSize: 15,
                marginTop: 8,
                opacity: form.name.trim() ? 1 : 0.5,
              }}
            >
              Next: Resume & LinkedIn
            </button>
          </>
        )}

        {step === 2 && (
          <>
            <p style={{ fontSize: 14, color: 'var(--text-secondary)', marginBottom: 16 }}>
              Optional — helps Claude understand your background for better coaching.
            </p>

            <label style={labelStyle}>LinkedIn URL</label>
            <input
              style={inputStyle}
              value={form.linkedin_url}
              onChange={e => update('linkedin_url', e.target.value)}
              placeholder="https://linkedin.com/in/yourprofile"
            />

            <label style={labelStyle}>Resume (paste text)</label>
            <textarea
              style={{ ...inputStyle, minHeight: 200, resize: 'vertical' as const, fontFamily: 'inherit' }}
              value={form.resume_text}
              onChange={e => update('resume_text', e.target.value)}
              placeholder="Paste your resume text here... (or skip this step)"
            />

            {error && (
              <p style={{ color: 'var(--red)', fontSize: 13, marginBottom: 8 }}>{error}</p>
            )}

            <div style={{ display: 'flex', gap: 8, marginTop: 8 }}>
              <button
                onClick={() => setStep(1)}
                style={{ flex: 1, background: 'var(--bg-surface)', color: 'var(--text-primary)' }}
              >
                Back
              </button>
              <button
                onClick={handleSubmit}
                disabled={loading}
                style={{
                  flex: 2,
                  background: 'var(--accent)',
                  color: 'var(--bg-primary)',
                  fontWeight: 600,
                  fontSize: 15,
                  opacity: loading ? 0.5 : 1,
                }}
              >
                {loading ? 'Creating profile...' : 'Start Skill Assessment'}
              </button>
            </div>

            <button
              onClick={handleSubmit}
              disabled={loading}
              style={{
                width: '100%',
                background: 'transparent',
                color: 'var(--text-muted)',
                marginTop: 8,
                fontSize: 13,
              }}
            >
              Skip — I'll add this later
            </button>
          </>
        )}
      </div>
    </div>
  )
}
