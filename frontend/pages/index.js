import { useEffect, useState } from 'react'

export default function Home() {
  const [status, setStatus] = useState('loading...')
  const [error, setError] = useState(null)

  useEffect(() => {
    let active = true
    const controller = new AbortController()

    async function load() {
      try {
        const res = await fetch('http://localhost:8000/', { signal: controller.signal })
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        const data = await res.json()
        if (active) setStatus(data.status || 'unknown')
      } catch (e) {
        if (active) setError(e.message)
      }
    }
    load()
    return () => {
      active = false
      controller.abort()
    }
  }, [])

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Hotel Energy Dashboard</h1>
      <p style={styles.paragraph}>
        Backend status: {error ? <span style={styles.error}>error ({error})</span> : <span style={styles.ok}>{status}</span>}
      </p>
    </div>
  )
}

const styles = {
  container: {
    fontFamily: 'system-ui, Arial, sans-serif',
    maxWidth: '720px',
    margin: '40px auto',
    padding: '24px',
    lineHeight: 1.5,
    border: '1px solid #e2e8f0',
    borderRadius: '12px',
    background: '#ffffff',
    boxShadow: '0 4px 12px rgba(0,0,0,0.05)'
  },
  title: {
    margin: '0 0 16px',
    fontSize: '2.2rem',
    letterSpacing: '.5px',
    color: '#1a202c'
  },
  paragraph: {
    margin: 0,
    fontSize: '1.05rem',
    color: '#2d3748'
  },
  ok: {
    color: '#0f766e',
    fontWeight: 600
  },
  error: {
    color: '#b91c1c',
    fontWeight: 600
  }
}
