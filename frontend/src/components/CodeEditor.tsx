import { useRef, useEffect } from 'react'
import Editor, { OnMount } from '@monaco-editor/react'

interface CodeEditorProps {
  code: string
  language: string
  onChange: (value: string) => void
  onLanguageChange: (lang: string) => void
  onRun: () => void
  onSubmit: () => void
  onNext: () => void
  output: string | null          // unused — output shown in left panel
  running: boolean
  submitting: boolean
  submitResult?: any | null      // unused — result shown in left panel
}

const LANGUAGES = [
  { value: 'java',       label: 'Java'       },
  { value: 'python',     label: 'Python'     },
  { value: 'javascript', label: 'JavaScript' },
]

export default function CodeEditor({
  code,
  language,
  onChange,
  onLanguageChange,
  onRun,
  onSubmit,
  running,
  submitting,
}: CodeEditorProps) {
  // Keep refs so Monaco keybindings always call the latest version
  const onRunRef    = useRef(onRun)
  const onSubmitRef = useRef(onSubmit)
  useEffect(() => { onRunRef.current    = onRun    }, [onRun])
  useEffect(() => { onSubmitRef.current = onSubmit }, [onSubmit])

  const handleMount: OnMount = (editor, monaco) => {
    // Ctrl/Cmd+Enter → Run
    editor.addCommand(
      monaco.KeyMod.CtrlCmd | monaco.KeyCode.Enter,
      () => onRunRef.current(),
    )
    // Ctrl/Cmd+Shift+Enter → Submit
    editor.addCommand(
      monaco.KeyMod.CtrlCmd | monaco.KeyMod.Shift | monaco.KeyCode.Enter,
      () => onSubmitRef.current(),
    )
  }

  return (
    <div style={{ display: 'flex', flexDirection: 'column', height: '100%', background: 'var(--bg-primary)' }}>

      {/* Toolbar */}
      <div style={{
        display: 'flex',
        justifyContent: 'space-between',
        alignItems: 'center',
        padding: '0 12px',
        height: 44,
        borderBottom: '1px solid var(--border)',
        background: 'var(--bg-secondary)',
        flexShrink: 0,
      }}>
        <select
          value={language}
          onChange={e => onLanguageChange(e.target.value)}
          style={{
            padding: '4px 10px', fontSize: 13, background: 'var(--bg-surface)',
            color: 'var(--text-primary)', border: '1px solid var(--border)', borderRadius: 6, cursor: 'pointer',
          }}
        >
          {LANGUAGES.map(l => (
            <option key={l.value} value={l.value}>{l.label}</option>
          ))}
        </select>

        <div style={{ display: 'flex', alignItems: 'center', gap: 8 }}>
          <span style={{ fontSize: 11, color: 'var(--text-muted)', marginRight: 4, userSelect: 'none' }}>
            ⌘↵ run · ⌘⇧↵ submit
          </span>
          <button
            onClick={onRun}
            disabled={running || submitting}
            style={{
              background: 'var(--bg-surface)',
              color: 'var(--text-primary)',
              fontWeight: 500, fontSize: 13,
              padding: '5px 18px',
              border: '1px solid var(--border)',
              borderRadius: 6,
              cursor: running || submitting ? 'not-allowed' : 'pointer',
              opacity: running || submitting ? 0.5 : 1,
            }}
          >
            {running ? 'Running…' : 'Run'}
          </button>
          <button
            onClick={onSubmit}
            disabled={submitting || running}
            style={{
              background: 'var(--green)',
              color: '#000',
              fontWeight: 700, fontSize: 13,
              padding: '5px 22px',
              border: 'none',
              borderRadius: 6,
              cursor: submitting || running ? 'not-allowed' : 'pointer',
              opacity: submitting || running ? 0.6 : 1,
            }}
          >
            {submitting ? 'Testing…' : 'Submit'}
          </button>
        </div>
      </div>

      {/* Monaco editor — fills all remaining height */}
      <div style={{ flex: 1, minHeight: 0 }}>
        <Editor
          height="100%"
          language={language === 'java' ? 'java' : language}
          value={code}
          onChange={v => onChange(v || '')}
          theme="vs-dark"
          onMount={handleMount}
          options={{
            fontSize: 14,
            minimap: { enabled: false },
            scrollBeyondLastLine: false,
            padding: { top: 16, bottom: 16 },
            lineNumbers: 'on',
            tabSize: 4,
            automaticLayout: true,
            fontFamily: "'JetBrains Mono', 'Fira Code', 'Cascadia Code', monospace",
            fontLigatures: true,
            renderLineHighlight: 'line',
            smoothScrolling: true,
            cursorBlinking: 'smooth',
            bracketPairColorization: { enabled: true },
          }}
        />
      </div>
    </div>
  )
}
