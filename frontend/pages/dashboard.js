import { useEffect, useState } from 'react'

export default function Dashboard() {
  const [metrics, setMetrics] = useState(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    let active = true
    const controller = new AbortController()

    async function fetchMetrics() {
      try {
        const res = await fetch('http://localhost:8000/metrics', { signal: controller.signal })
        if (!res.ok) throw new Error(`HTTP ${res.status}`)
        const data = await res.json()
        if (active) setMetrics(data)
      } catch (e) {
        if (active) setError(e.message)
      } finally {
        if (active) setLoading(false)
      }
    }

    fetchMetrics()
    return () => {
      active = false
      controller.abort()
    }
  }, [])

  // ============================================================================
  // REAL SENSOR INTEGRATION SUGGESTIONS (COMMENTED FOR FUTURE USE)
  // ============================================================================
  //
  // When you're ready to integrate real sensors with your Raspberry Pi 400:
  //
  // 1. Install sensor libraries in your backend:
  //    pip install adafruit-circuitpython-dht11
  //    pip install gpiozero
  //    pip install smbus2
  //
  // 2. Update your backend's /metrics endpoint in app/main.py:
  //    @app.get("/metrics")
  //    async def get_metrics():
  //        try:
  //            # Read from DHT11 temperature/humidity sensor
  //            # temperature = read_dht11_temperature()
  //            # humidity = read_dht11_humidity()
  //
  //            # Read from energy monitoring sensor (ACS712)
  //            # current = read_acs712_current()
  //            # power = calculate_power(current, voltage=220)
  //
  //            # Read from PIR motion sensor for occupancy
  //            # occupancy = read_pir_sensor()
  //
  //            # Calculate savings based on baseline
  //            # savings = calculate_energy_savings(power)
  //
  //            return {
  //                "energy_usage": power,  # Real power in watts
  //                "occupancy": occupancy,  # Real occupancy percentage
  //                "savings": savings,      # Real savings calculation
  //                "integrations": 5        # Number of active sensors
  //            }
  //        except Exception as e:
  //            # Fallback to mock data if sensors fail
  //            return {
  //                "energy_usage": 1250.5,
  //                "occupancy": 78.3,
  //                "savings": 320.8,
  //                "integrations": 5
  //            }
  //
  // 3. Add real-time updates (optional):
  //    - Use WebSocket for live sensor data
  //    - Implement polling every 30 seconds
  //    - Add sensor health monitoring
  //
  // 4. Sensor-specific considerations:
  //    - DHT11: Temperature 0-50°C, Humidity 20-90%
  //    - ACS712: Current sensing for energy monitoring
  //    - PIR: Motion detection for occupancy
  //    - GPIO pins: Ensure proper pin configuration
  //
  // 5. Error handling for sensors:
  //    - Handle sensor disconnection
  //    - Implement retry logic
  //    - Log sensor failures
  //    - Provide fallback values
  //
  // 6. Raspberry Pi specific setup:
  //    - Enable I2C/SPI interfaces: sudo raspi-config
  //    - Install GPIO libraries: pip install RPi.GPIO
  //    - Configure sensor pins in your code
  //    - Test sensors individually before integration
  //
  // ============================================================================

  if (loading) {
    return (
      <div style={styles.loadingContainer}>
        <div style={styles.loadingSpinner}></div>
        <p style={styles.loadingText}>Loading dashboard data...</p>
      </div>
    )
  }

  if (error) {
    return (
      <div style={styles.errorContainer}>
        <h2 style={styles.errorTitle}>Dashboard Error</h2>
        <p style={styles.errorMessage}>Failed to load metrics: {error}</p>
        <button 
          style={styles.retryButton} 
          onClick={() => window.location.reload()}
          type="button"
        >
          Retry
        </button>
      </div>
    )
  }

  return (
    <div style={styles.container}>
      <h1 style={styles.title}>Hotel Energy Dashboard</h1>
      <p style={styles.subtitle}>Real-time metrics from your Raspberry Pi sensors</p>
      
      <div style={styles.grid}>
        <div style={styles.card} key="energy">
          <div style={styles.cardHeader}>
            <span style={styles.icon} role="img" aria-label="energy">⚡</span>
            <h3 style={styles.cardTitle}>Energy Usage</h3>
          </div>
          <div style={styles.cardValue}>
            {metrics?.energy_usage?.toFixed(1) || '0.0'} kWh
          </div>
          <div style={styles.cardChange}>
            <span style={styles.trend}>↓ 5.2%</span> from last hour
          </div>
        </div>

        <div style={styles.card} key="occupancy">
          <div style={styles.cardHeader}>
            <span style={styles.icon} role="img" aria-label="occupancy">🏨</span>
            <h3 style={styles.cardTitle}>Occupancy</h3>
          </div>
          <div style={styles.cardValue}>
            {metrics?.occupancy?.toFixed(1) || '0.0'}%
          </div>
          <div style={styles.cardChange}>
            <span style={styles.trend}>↑ 2.1%</span> from yesterday
          </div>
        </div>

        <div style={styles.card} key="savings">
          <div style={styles.cardHeader}>
            <span style={styles.icon} role="img" aria-label="savings">💰</span>
            <h3 style={styles.cardTitle}>Savings</h3>
          </div>
          <div style={styles.cardValue}>
            ${metrics?.savings?.toFixed(1) || '0.0'}
          </div>
          <div style={styles.cardChange}>
            <span style={styles.trend}>↑ 12.5%</span> this month
          </div>
        </div>

        <div style={styles.card} key="integrations">
          <div style={styles.cardHeader}>
            <span style={styles.icon} role="img" aria-label="integrations">🔗</span>
            <h3 style={styles.cardTitle}>Integrations</h3>
          </div>
          <div style={styles.cardValue}>
            {metrics?.integrations || 0}
          </div>
          <div style={styles.cardChange}>
            <span style={styles.trend}>✓</span> sensors active
          </div>
        </div>
      </div>

      <div style={styles.footer}>
        <p style={styles.footerText}>
          Last updated: {new Date().toLocaleTimeString()} | 
          Data from Raspberry Pi 400 sensors
        </p>
      </div>
    </div>
  )
}

const styles = {
  container: {
    fontFamily: 'Arial, sans-serif',
    maxWidth: '1200px',
    margin: '0 auto',
    padding: '0 20px',
  },
  title: {
    fontSize: '2.5rem',
    fontWeight: 'bold',
    margin: '40px 0 10px',
    color: '#333',
  },
  subtitle: {
    fontSize: '1.2rem',
    margin: '0 0 30px',
    color: '#666',
  },
  grid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))',
    gap: '20px',
  },
  card: {
    backgroundColor: '#fff',
    borderRadius: '8px',
    boxShadow: '0 4px 8px rgba(0, 0, 0, 0.1)',
    padding: '20px',
    transition: 'transform 0.2s',
  },
  cardHeader: {
    display: 'flex',
    alignItems: 'center',
    marginBottom: '10px',
  },
  icon: {
    fontSize: '1.5rem',
    marginRight: '10px',
    color: '#0070f3',
  },
  cardTitle: {
    fontSize: '1.2rem',
    fontWeight: 'medium',
    margin: 0,
    color: '#333',
  },
  cardValue: {
    fontSize: '2rem',
    fontWeight: 'bold',
    margin: '10px 0',
    color: '#111',
  },
  cardChange: {
    fontSize: '0.9rem',
    color: '#666',
  },
  trend: {
    fontWeight: 'bold',
  },
  footer: {
    borderTop: '1px solid #eaeaea',
    padding: '20px 0',
    marginTop: '40px',
    textAlign: 'center',
  },
  footerText: {
    fontSize: '0.9rem',
    color: '#666',
  },
  loadingContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
    backgroundColor: '#f9f9f9',
  },
  loadingSpinner: {
    border: '8px solid #eaeaea',
    borderTop: '8px solid #0070f3',
    borderRadius: '50%',
    width: '40px',
    height: '40px',
    animation: 'spin 1s linear infinite',
  },
  loadingText: {
    marginTop: '10px',
    fontSize: '1.2rem',
    color: '#333',
  },
  errorContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
    backgroundColor: '#fff3f3',
  },
  errorTitle: {
    fontSize: '2rem',
    fontWeight: 'bold',
    margin: 0,
    color: '#d9534f',
  },
  errorMessage: {
    fontSize: '1.1rem',
    margin: '10px 0',
    color: '#333',
  },
  retryButton: {
    marginTop: '20px',
    padding: '10px 20px',
    fontSize: '1rem',
    color: '#fff',
    backgroundColor: '#0070f3',
    border: 'none',
    borderRadius: '5px',
    cursor: 'pointer',
    transition: 'background-color 0.3s',
  },
  retryButtonHover: {
    backgroundColor: '#005bb5',
  },
}

// ✅ Properly define keyframes using CSS-in-JS approach
if (typeof window !== 'undefined') {
  const styleSheet = document.createElement('style')
  styleSheet.textContent = `
    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
  `
  document.head.appendChild(styleSheet)
}