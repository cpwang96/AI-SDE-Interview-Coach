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

      {/* Editor */}
      <div style={{ flex: 1 }}>
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

      {/* Output */}
      {output !== null && (
        <div style={{
          borderTop: '1px solid var(--border)',
          background: 'var(--bg-secondary)',
          padding: 12,
          maxHeight: 150,
          overflowY: 'auto',
        }}>
          <div style={{ fontSize: 11, color: 'var(--text-muted)', marginBottom: 4 }}>Output</div>
          <pre style={{ fontSize: 13, color: 'var(--text-primary)', whiteSpace: 'pre-wrap', fontFamily: 'monospace' }}>
            {output}
          </pre>
        </div>
      )}
    </div>
  )
}
