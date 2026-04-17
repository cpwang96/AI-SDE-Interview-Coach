import Editor from '@monaco-editor/react'

interface CodeEditorProps {
  code: string
  language: string
  onChange: (value: string) => void
  onLanguageChange: (lang: string) => void
  onRun: () => void
  onSubmit: () => void
  output: string | null
  running: boolean
  submitting: boolean
  submitResult?: { all_passed: boolean; passed: number; total: number; time_ms?: number } | null
}

const LANGUAGES = [
  { value: 'python', label: 'Python' },
  { value: 'javascript', label: 'JavaScript' },
  { value: 'java', label: 'Java' },
]

export default function CodeEditor({
  code,
  language,
  onChange,
  onLanguageChange,
  onRun,
  onSubmit,
  output,
  running,
  submitting,
  submitResult,
}: CodeEditorProps) {
  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%' }}>
      {/* Toolbar */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '8px 12px',
        borderBottom: '1px solid var(--border)',
        background: 'var(--bg-secondary)',
      }}>
        <select
          value={language}
          onChange={e => onLanguageChange(e.target.value)}
          style={{ padding: '4px 8px', fontSize: 13 }}
        >
          {LANGUAGES.map(l => (
            <option key={l.value} value={l.value}>{l.label}</option>
          ))}
        </select>
        <div style={{ display: 'flex', gap: 8 }}>
          <button
            onClick={onRun}
            disabled={running || submitting}
            style={{
              background: 'var(--bg-surface)',
              color: 'var(--text-primary)',
              fontWeight: 500,
              fontSize: 13,
              padding: '6px 16px',
              opacity: running || submitting ? 0.5 : 1,
            }}
          >
            {running ? 'Running...' : 'Run'}
          </button>
          <button
            onClick={onSubmit}
            disabled={submitting || running}
            style={{
              background: 'var(--green)',
              color: 'var(--bg-primary)',
              fontWeight: 600,
              fontSize: 13,
              padding: '6px 20px',
              opacity: submitting || running ? 0.5 : 1,
            }}
          >
            {submitting ? 'Testing...' : 'Submit'}
          </button>
        </div>
      </div>

      {/* Editor — takes remaining space above the always-visible bottom panel */}
      <div style={{ flex: 1, minHeight: 0 }}>
        <Editor
          height="100%"
          language={language}
          value={code}
          onChange={v => onChange(v || '')}
          theme="vs-dark"
          options={{
            fontSize: 14,
            minimap: { enabled: false },
            scrollBeyondLastLine: false,
            padding: { top: 12 },
            lineNumbers: 'on',
            tabSize: 4,
            automaticLayout: true,
          }}
        />
      </div>

      {/* Always-visible bottom panel: submit result + output */}
      <div style={{
        height: 160,
        flexShrink: 0,
        borderTop: '1px solid var(--border)',
        display: 'flex',
        flexDirection: 'column',
        overflow: 'hidden',
        background: 'var(--bg-secondary)',
      }}>
        {/* Submit result banner */}
        {submitResult && (
          <div style={{
            padding: '6px 14px',
            background: submitResult.all_passed ? 'rgba(34,197,94,0.15)' : 'rgba(239,68,68,0.15)',
            borderBottom: `2px solid ${submitResult.all_passed ? 'var(--green)' : 'var(--red)'}`,
            color: submitResult.all_passed ? 'var(--green)' : 'var(--red)',
            fontWeight: 600,
            fontSize: 13,
            display: 'flex',
            justifyContent: 'space-between',
            alignItems: 'center',
            flexShrink: 0,
          }}>
            <span>
              {submitResult.all_passed
                ? `✓ All ${submitResult.total} test cases passed!`
                : `✗ ${submitResult.passed}/${submitResult.total} test cases passed`
              }
            </span>
            {submitResult.time_ms && (
              <span style={{ fontWeight: 400, fontSize: 12, opacity: 0.8 }}>{submitResult.time_ms}ms</span>
            )}
          </div>
        )}

        {/* Output */}
        <div style={{ flex: 1, overflowY: 'auto', padding: '8px 12px' }}>
          <div style={{ fontSize: 11, color: 'var(--text-muted)', marginBottom: 4, textTransform: 'uppercase', letterSpacing: '0.05em' }}>
            {running ? 'Running…' : submitting ? 'Testing…' : 'Output'}
          </div>
          {output !== null ? (
            <pre style={{ fontSize: 13, color: 'var(--text-primary)', whiteSpace: 'pre-wrap', fontFamily: 'monospace', margin: 0 }}>
              {output}
            </pre>
          ) : (
            <div style={{ fontSize: 13, color: 'var(--text-muted)', fontStyle: 'italic' }}>
              {running || submitting ? 'Waiting for result…' : 'Run your code or submit to see output here.'}
            </div>
          )}
        </div>
      </div>
    </div>
  )
}
