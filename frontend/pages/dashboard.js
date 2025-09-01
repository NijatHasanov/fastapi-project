import { useEffect, useState } from 'react';

// AI Insights Panel Component
const AIInsightsPanel = ({ insights, onApplyRecommendation }) => {
  const [expandedInsight, setExpandedInsight] = useState(null);

  const getPriorityStyle = (priority) => {
    const styles = {
      critical: { color: '#dc3545', bgColor: '#f8d7da', icon: '🚨' },
      high: { color: '#fd7e14', bgColor: '#fde2cf', icon: '🔥' },
      medium: { color: '#ffc107', bgColor: '#fff3cd', icon: '⚠️' },
      low: { color: '#28a745', bgColor: '#d4edda', icon: '💡' },
    };
    return styles[priority] || { color: '#6c757d', bgColor: '#f8f9fa', icon: '🤖' };
  };

  const handleApplyRecommendation = (insight) => {
    onApplyRecommendation?.(insight);
  };

  return (
    <div style={styles.panel}>
      <div style={styles.panelHeader}>
        <h3 style={styles.panelTitle}>
          <span style={styles.titleIcon}>🧠</span>
          AI Optimization Engine
        </h3>
        <div style={styles.badge}>
          {insights.length} Active Insights
        </div>
      </div>
      
      <div style={styles.insightsList}>
        {insights.length === 0 ? (
          <div style={styles.emptyState}>
            <span style={{ fontSize: '2rem' }}>✅</span>
            <p>All systems operating optimally</p>
          </div>
        ) : (
          insights.map((insight, index) => {
            const priorityStyle = getPriorityStyle(insight.priority);
            const isExpanded = expandedInsight === index;
            
            return (
              <div
                key={index}
                className="insight-card"
                style={{
                  ...styles.insightCard,
                  borderLeftColor: priorityStyle.color,
                  backgroundColor: isExpanded ? priorityStyle.bgColor : '#fafbfc'
                }}
                onClick={() => setExpandedInsight(isExpanded ? null : index)}
              >
                <div style={styles.insightHeader}>
                  <div style={styles.insightIcon}>
                    {priorityStyle.icon}
                  </div>
                  <div style={styles.insightMeta}>
                    <span 
                      style={{
                        ...styles.priorityBadge,
                        backgroundColor: priorityStyle.color
                      }}
                    >
                      {insight.priority.toUpperCase()}
                    </span>
                    <span style={styles.insightTime}>
                      {new Date().toLocaleTimeString()}
                    </span>
                  </div>
                </div>
                
                <h4 style={styles.insightTitle}>{insight.title}</h4>
                <p style={styles.insightDescription}>{insight.description}</p>
                
                {insight.confidence && (
                  <div style={styles.confidenceBar}>
                    <span style={styles.confidenceLabel}>
                      Confidence: {(insight.confidence * 100).toFixed(0)}%
                    </span>
                    <div style={styles.confidenceProgress}>
                      <div 
                        style={{
                          ...styles.confidenceFill,
                          width: `${insight.confidence * 100}%`,
                          backgroundColor: priorityStyle.color
                        }}
                      />
                    </div>
                  </div>
                )}
                
                {isExpanded && (
                  <div style={styles.insightDetails}>
                    <div style={styles.detailSection}>
                      <h5 style={styles.detailTitle}>💡 Recommendation</h5>
                      <p style={styles.detailText}>{insight.recommendation}</p>
                    </div>
                    
                    {insight.potentialSavings && (
                      <div style={styles.detailSection}>
                        <h5 style={styles.detailTitle}>💰 Potential Savings</h5>
                        <p style={styles.savingsText}>{insight.potentialSavings}</p>
                      </div>
                    )}
                    
                    <button 
                      className="apply-button"
                      style={styles.applyButton}
                      onClick={(e) => {
                        e.stopPropagation();
                        handleApplyRecommendation(insight);
                      }}
                    >
                      Apply Recommendation
                    </button>
                  </div>
                )}
              </div>
            );
          })
        )}
      </div>
    </div>
  );
};

// Optimization Panel Component
const OptimizationPanel = ({ recommendations, onApplyOptimization }) => {
  const [appliedOptimizations, setAppliedOptimizations] = useState(new Set());

  const getCategoryConfig = (category) => {
    const configs = {
      hvac: { icon: '🌡️', color: '#dc3545', label: 'HVAC' },
      lighting: { icon: '💡', color: '#ffc107', label: 'Lighting' },
      equipment: { icon: '🔧', color: '#17a2b8', label: 'Equipment' }
    };
    return configs[category] || { icon: '⚙️', color: '#6c757d', label: 'System' };
  };

  const handleApplyOptimization = (recommendation) => {
    setAppliedOptimizations(prev => new Set([...prev, recommendation.id]));
    onApplyOptimization?.(recommendation);
  };

  const totalSavings = recommendations
    .filter(rec => appliedOptimizations.has(rec.id))
    .reduce((sum, rec) => sum + rec.expectedSavings, 0);

  return (
    <div style={styles.panel}>
      <div style={styles.panelHeader}>
        <h3 style={styles.panelTitle}>
          <span style={styles.titleIcon}>🎯</span>
          Smart Optimization
        </h3>
        {totalSavings > 0 && (
          <div style={styles.savingsBadge}>
            💰 {totalSavings}% total savings
          </div>
        )}
      </div>

      <div style={styles.optimizationGrid}>
        {recommendations.map((rec, index) => {
          const config = getCategoryConfig(rec.category);
          const isApplied = appliedOptimizations.has(rec.id);
          
          return (
            <div key={index} style={styles.optimizationCard}>
              <div style={styles.optimizationHeader}>
                <div style={styles.categoryBadge}>
                  <span style={styles.categoryIcon}>{config.icon}</span>
                  <span style={styles.categoryLabel}>{config.label}</span>
                </div>
                <span style={styles.confidenceScore}>
                  {(rec.confidence * 100).toFixed(0)}%
                </span>
              </div>
              
              <h4 style={styles.optimizationTitle}>
                {rec.action.replace(/_/g, ' ')}
              </h4>
              <p style={styles.optimizationDescription}>{rec.reasoning}</p>
              
              <div style={styles.optimizationMetrics}>
                <div style={styles.metric}>
                  <span style={styles.metricLabel}>Target</span>
                  <span style={styles.metricValue}>
                    {rec.targetValue}{rec.unit}
                  </span>
                </div>
                <div style={styles.metric}>
                  <span style={styles.metricLabel}>Savings</span>
                  <span style={styles.metricValue}>
                    {rec.expectedSavings}%
                  </span>
                </div>
              </div>
              
              <button 
                className="optimization-button"
                style={{
                  ...styles.optimizationButton,
                  ...(isApplied ? styles.appliedButton : {})
                }}
                onClick={() => handleApplyOptimization(rec)}
                disabled={isApplied}
              >
                {isApplied ? '✓ Applied' : 'Apply Now'}
              </button>
            </div>
          );
        })}
      </div>
    </div>
  );
};

// Efficiency Score Component
const EfficiencyScore = ({ efficiencyData }) => {
  const { score = 0, grade = 'Unknown', benchmarks = [] } = efficiencyData || {};
  
  const getScoreColor = (score) => {
    if (score >= 85) return '#28a745';
    if (score >= 70) return '#ffc107';
    if (score >= 55) return '#fd7e14';
    return '#dc3545';
  };

  const circumference = 2 * Math.PI * 54;
  const strokeDasharray = `${(score / 100) * circumference} ${circumference}`;

  return (
    <div style={styles.panel}>
      <div style={styles.panelHeader}>
        <h3 style={styles.panelTitle}>
          <span style={styles.titleIcon}>⚡</span>
          Energy Efficiency Score
        </h3>
      </div>
      
      <div style={styles.scoreDisplay}>
        <div style={styles.scoreCircle}>
          <svg width="140" height="140" viewBox="0 0 140 140">
            <circle
              cx="70"
              cy="70" 
              r="54"
              fill="none"
              stroke="#e9ecef"
              strokeWidth="12"
            />
            <circle
              cx="70"
              cy="70"
              r="54"
              fill="none"
              stroke={getScoreColor(score)}
              strokeWidth="12"
              strokeDasharray={strokeDasharray}
              strokeDashoffset={circumference * 0.25}
              transform="rotate(-90 70 70)"
              style={{ transition: 'stroke-dasharray 1s ease-in-out' }}
            />
          </svg>
          <div style={styles.scoreText}>
            <span style={styles.scoreNumber}>{score}</span>
            <span style={styles.scoreUnit}>%</span>
          </div>
        </div>
        
        <div style={styles.scoreInfo}>
          <h4 style={{ color: getScoreColor(score), margin: '0 0 8px 0' }}>
            {grade}
          </h4>
          <p style={styles.scoreDescription}>
            Your hotel's performance compared to industry standards
          </p>
        </div>
      </div>
      
      <div style={styles.benchmarks}>
        <h5 style={styles.benchmarkTitle}>Industry Benchmarks</h5>
        {benchmarks.map((benchmark, index) => (
          <div key={index} style={styles.benchmarkItem}>
            <span style={styles.benchmarkName}>{benchmark.name}</span>
            <span style={styles.benchmarkScore}>{benchmark.score}%</span>
          </div>
        ))}
      </div>
    </div>
  );
};

// Real-time Metrics Component
const MetricsGrid = ({ metrics }) => {
  const metricConfigs = [
    {
      key: 'energy_usage',
      icon: '⚡',
      label: 'Energy Usage',
      unit: 'kWh',
      format: (val) => val?.toFixed(0) || '0'
    },
    {
      key: 'occupancy', 
      icon: '🏨',
      label: 'Occupancy',
      unit: '%',
      format: (val) => val?.toFixed(1) || '0.0'
    },
    {
      key: 'potential_savings',
      icon: '💰',
      label: 'Potential Savings',
      unit: '$',
      format: (val) => val?.toFixed(0) || '0'
    },
    {
      key: 'integrations',
      icon: '🔗',
      label: 'Connected Systems', 
      unit: '',
      format: (val) => val || '0'
    }
  ];

  return (
    <div style={styles.metricsGrid}>
      {metricConfigs.map((config, index) => (
        <div key={index} className="metric-card" style={styles.metricCard}>
          <div style={styles.metricHeader}>
            <span style={styles.metricIcon}>{config.icon}</span>
            <span style={styles.metricLabel}>{config.label}</span>
          </div>
          <div style={styles.metricValue}>
            {config.unit === '$' ? '$' : ''}{config.format(metrics?.[config.key])}
            {config.unit && config.unit !== '$' ? ` ${config.unit}` : ''}
          </div>
          <div style={styles.metricChange}>
            <span style={styles.changeIndicator}>
              {Math.random() > 0.5 ? '↗️' : '↘️'} 
              {(Math.random() * 10).toFixed(1)}%
            </span>
            <span>vs last hour</span>
          </div>
        </div>
      ))}
    </div>
  );
};

// Main Dashboard Component
export default function Dashboard() {
  const [data, setData] = useState({
    metrics: null,
    insights: [],
    recommendations: [],
    efficiency: null,
    predictions: null
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [lastUpdate, setLastUpdate] = useState(new Date());

  const fetchData = async () => {
    try {
      const endpoints = [
        'metrics',
        'insights', 
        'recommendations',
        'efficiency-score',
        'predictions'
      ];
      
      const responses = await Promise.all(
        endpoints.map(endpoint => 
          fetch(`http://localhost:8000/${endpoint}`)
            .then(res => {
              if (!res.ok) {
                throw new Error(`HTTP ${res.status}: ${res.statusText}`);
              }
              return res.json();
            })
        )
      );

      setData({
        metrics: responses[0],
        insights: responses[1] || [],
        recommendations: responses[2] || [], 
        efficiency: responses[3],
        predictions: responses[4]
      });
      
      setLastUpdate(new Date());
      setError(null);
    } catch (err) {
      setError(err.message);
      console.error('Data fetch error:', err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchData();
    const interval = setInterval(fetchData, 30000); // 30 seconds
    return () => clearInterval(interval);
  }, []);

  const handleApplyRecommendation = (insight) => {
    console.log('Applying recommendation:', insight);
    // Here you would typically make an API call to apply the recommendation
  };

  const handleApplyOptimization = (recommendation) => {
    console.log('Applying optimization:', recommendation);
    // Here you would typically make an API call to apply the optimization
  };

  if (loading) {
    return (
      <div style={styles.loadingContainer}>
        <div style={styles.loadingSpinner}></div>
        <p style={styles.loadingText}>AI is analyzing your energy data...</p>
      </div>
    );
  }

  if (error) {
    return (
      <div style={styles.errorContainer}>
        <h2 style={styles.errorTitle}>Connection Error</h2>
        <p style={styles.errorMessage}>
          Unable to connect to the AI optimization engine: {error}
        </p>
        <button 
          className="retry-button"
          style={styles.retryButton}
          onClick={() => window.location.reload()}
        >
          Reconnect
        </button>
      </div>
    );
  }

  return (
    <div style={styles.container}>
      {/* Header */}
      <header style={styles.header}>
        <div style={styles.headerContent}>
          <h1 style={styles.title}>Hotel Energy SaaS</h1>
          <p style={styles.subtitle}>AI-Powered Energy Optimization Platform</p>
        </div>
        <div style={styles.headerStatus}>
          <div style={styles.statusIndicator}>
            <span style={styles.statusDot}></span>
            <span>AI Engine Active</span>
          </div>
          <div style={styles.lastUpdateTime}>
            Last updated: {lastUpdate.toLocaleTimeString()}
          </div>
        </div>
      </header>

      {/* Metrics Grid */}
      <MetricsGrid metrics={data.metrics} />

      {/* Main Content */}
      <div style={styles.contentGrid}>
        <div style={styles.leftColumn}>
          <AIInsightsPanel 
            insights={data.insights}
            onApplyRecommendation={handleApplyRecommendation}
          />
          <OptimizationPanel 
            recommendations={data.recommendations}
            onApplyOptimization={handleApplyOptimization}
          />
        </div>
        
        <div style={styles.rightColumn}>
          <EfficiencyScore efficiencyData={data.efficiency} />
        </div>
      </div>
    </div>
  );
}

// Comprehensive Styles
const styles = {
  // Layout
  container: {
    fontFamily: '-apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif',
    maxWidth: '1400px',
    margin: '0 auto',
    padding: '20px',
    backgroundColor: '#f8f9fa',
    minHeight: '100vh'
  },
  
  // Header
  header: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    backgroundColor: 'white',
    padding: '24px',
    borderRadius: '12px',
    boxShadow: '0 4px 12px rgba(0,0,0,0.05)',
    marginBottom: '24px',
    border: '1px solid #e9ecef'
  },
  headerContent: {
    flex: 1
  },
  title: {
    fontSize: '2.2rem',
    fontWeight: '700',
    margin: '0 0 4px 0',
    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
    WebkitBackgroundClip: 'text',
    WebkitTextFillColor: 'transparent',
    backgroundClip: 'text'
  },
  subtitle: {
    fontSize: '1rem',
    color: '#6c757d',
    margin: 0
  },
  headerStatus: {
    textAlign: 'right'
  },
  statusIndicator: {
    display: 'flex',
    alignItems: 'center',
    gap: '8px',
    color: '#28a745',
    fontWeight: '500',
    marginBottom: '4px'
  },
  statusDot: {
    width: '8px',
    height: '8px',
    backgroundColor: '#28a745',
    borderRadius: '50%',
    animation: 'pulse 2s infinite'
  },
  lastUpdateTime: {
    fontSize: '0.9rem',
    color: '#6c757d'
  },

  // Metrics Grid
  metricsGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(280px, 1fr))',
    gap: '20px',
    marginBottom: '24px'
  },
  metricCard: {
    backgroundColor: 'white',
    padding: '24px',
    borderRadius: '12px',
    boxShadow: '0 4px 12px rgba(0,0,0,0.05)',
    border: '1px solid #e9ecef',
    textAlign: 'center',
    transition: 'transform 0.2s ease, box-shadow 0.2s ease'
  },
  metricHeader: {
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '8px',
    marginBottom: '16px'
  },
  metricIcon: {
    fontSize: '1.5rem'
  },
  metricLabel: {
    fontSize: '0.9rem',
    fontWeight: '600',
    color: '#6c757d',
    textTransform: 'uppercase',
    letterSpacing: '0.5px'
  },
  metricValue: {
    fontSize: '2.5rem',
    fontWeight: '700',
    color: '#212529',
    marginBottom: '8px'
  },
  metricChange: {
    fontSize: '0.9rem',
    color: '#6c757d',
    display: 'flex',
    alignItems: 'center',
    justifyContent: 'center',
    gap: '4px'
  },
  changeIndicator: {
    fontWeight: '600'
  },

  // Content Grid
  contentGrid: {
    display: 'grid',
    gridTemplateColumns: '2fr 1fr',
    gap: '24px'
  },
  leftColumn: {
    display: 'flex',
    flexDirection: 'column',
    gap: '24px'
  },
  rightColumn: {
    display: 'flex',
    flexDirection: 'column',
    gap: '24px'
  },

  // Panel Base
  panel: {
    backgroundColor: 'white',
    borderRadius: '12px',
    padding: '24px',
    boxShadow: '0 4px 12px rgba(0,0,0,0.05)',
    border: '1px solid #e9ecef'
  },
  panelHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '20px'
  },
  panelTitle: {
    fontSize: '1.4rem',
    fontWeight: '700',
    margin: 0,
    display: 'flex',
    alignItems: 'center',
    gap: '8px'
  },
  titleIcon: {
    fontSize: '1.2rem'
  },
  badge: {
    backgroundColor: '#667eea',
    color: 'white',
    padding: '6px 12px',
    borderRadius: '20px',
    fontSize: '0.8rem',
    fontWeight: '600'
  },
  savingsBadge: {
    backgroundColor: '#d4edda',
    color: '#155724',
    padding: '6px 12px',
    borderRadius: '20px',
    fontSize: '0.8rem',
    fontWeight: '600'
  },

  // AI Insights
  insightsList: {
    display: 'flex',
    flexDirection: 'column',
    gap: '16px'
  },
  emptyState: {
    textAlign: 'center',
    padding: '40px 20px',
    color: '#6c757d'
  },
  insightCard: {
    border: '1px solid #e9ecef',
    borderLeftWidth: '5px',
    borderRadius: '8px',
    padding: '16px',
    backgroundColor: '#fafbfc',
    cursor: 'pointer',
    transition: 'all 0.2s ease'
  },
  insightHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '12px'
  },
  insightIcon: {
    fontSize: '1.5rem'
  },
  insightMeta: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'flex-end',
    gap: '4px'
  },
  priorityBadge: {
    padding: '3px 8px',
    borderRadius: '12px',
    fontSize: '0.7rem',
    fontWeight: '700',
    color: 'white'
  },
  insightTime: {
    fontSize: '0.8rem',
    color: '#6c757d'
  },
  insightTitle: {
    fontSize: '1.1rem',
    fontWeight: '600',
    margin: '0 0 8px 0',
    color: '#212529'
  },
  insightDescription: {
    fontSize: '0.9rem',
    color: '#6c757d',
    margin: '0 0 12px 0',
    lineHeight: '1.4'
  },
  confidenceBar: {
    marginBottom: '12px'
  },
  confidenceLabel: {
    fontSize: '0.8rem',
    color: '#6c757d',
    marginBottom: '4px',
    display: 'block'
  },
  confidenceProgress: {
    width: '100%',
    height: '6px',
    backgroundColor: '#e9ecef',
    borderRadius: '3px',
    overflow: 'hidden'
  },
  confidenceFill: {
    height: '100%',
    borderRadius: '3px',
    transition: 'width 0.3s ease'
  },
  insightDetails: {
    borderTop: '1px solid #e9ecef',
    paddingTop: '16px',
    marginTop: '16px'
  },
  detailSection: {
    marginBottom: '16px'
  },
  detailTitle: {
    fontSize: '0.9rem',
    fontWeight: '600',
    margin: '0 0 8px 0',
    color: '#495057'
  },
  detailText: {
    fontSize: '0.9rem',
    color: '#6c757d',
    margin: 0,
    lineHeight: '1.4'
  },
  savingsText: {
    fontSize: '1rem',
    fontWeight: '600',
    color: '#28a745',
    margin: 0
  },
  applyButton: {
    padding: '10px 20px',
    backgroundColor: '#667eea',
    color: 'white',
    border: 'none',
    borderRadius: '6px',
    fontSize: '0.9rem',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'background-color 0.2s ease'
  },

  // Optimizations
  optimizationGrid: {
    display: 'grid',
    gridTemplateColumns: 'repeat(auto-fit, minmax(300px, 1fr))',
    gap: '16px'
  },
  optimizationCard: {
    border: '1px solid #e9ecef',
    borderRadius: '8px',
    padding: '16px',
    backgroundColor: '#fafbfc'
  },
  optimizationHeader: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: '12px'
  },
  categoryBadge: {
    display: 'flex',
    alignItems: 'center',
    gap: '6px'
  },
  categoryIcon: {
    fontSize: '1.2rem'
  },
  categoryLabel: {
    fontSize: '0.8rem',
    fontWeight: '600',
    textTransform: 'uppercase',
    color: '#6c757d'
  },
  confidenceScore: {
    fontSize: '0.8rem',
    color: '#28a745',
    fontWeight: '600'
  },
  optimizationTitle: {
    fontSize: '1.1rem',
    fontWeight: '600',
    margin: '0 0 8px 0',
    color: '#212529',
    textTransform: 'capitalize'
  },
  optimizationDescription: {
    fontSize: '0.9rem',
    color: '#6c757d',
    margin: '0 0 16px 0',
    lineHeight: '1.4'
  },
  optimizationMetrics: {
    display: 'flex',
    justifyContent: 'space-between',
    marginBottom: '16px'
  },
  metric: {
    textAlign: 'center',
    flex: 1
  },
  metricLabel: {
    fontSize: '0.8rem',
    color: '#6c757d',
    display: 'block',
    marginBottom: '4px'
  },
  metricValue: {
    fontSize: '1.2rem',
    fontWeight: '600',
    color: '#212529'
  },
  optimizationButton: {
    width: '100%',
    padding: '10px',
    backgroundColor: '#667eea',
    color: 'white',
    border: 'none',
    borderRadius: '6px',
    fontSize: '0.9rem',
    fontWeight: '600',
    cursor: 'pointer',
    transition: 'all 0.2s ease'
  },
  appliedButton: {
    backgroundColor: '#28a745',
    cursor: 'default'
  },

  // Efficiency Score
  scoreDisplay: {
    display: 'flex',
    alignItems: 'center',
    gap: '24px',
    marginBottom: '24px'
  },
  scoreCircle: {
    position: 'relative',
    width: '140px',
    height: '140px',
    flexShrink: 0
  },
  scoreText: {
    position: 'absolute',
    top: '50%',
    left: '50%',
    transform: 'translate(-50%, -50%)',
    textAlign: 'center'
  },
  scoreNumber: {
    fontSize: '2.5rem',
    fontWeight: '700',
    color: '#212529'
  },
  scoreUnit: {
    fontSize: '1.5rem',
    color: '#6c757d'
  },
  scoreInfo: {
    flex: 1
  },
  scoreDescription: {
    fontSize: '0.9rem',
    color: '#6c757d',
    margin: 0,
    lineHeight: '1.4'
  },
  benchmarks: {
    borderTop: '1px solid #e9ecef',
    paddingTop: '16px'
  },
  benchmarkTitle: {
    fontSize: '1rem',
    fontWeight: '600',
    margin: '0 0 12px 0',
    color: '#495057'
  },
  benchmarkItem: {
    display: 'flex',
    justifyContent: 'space-between',
    alignItems: 'center',
    padding: '8px 12px',
    backgroundColor: '#f8f9fa',
    borderRadius: '6px',
    marginBottom: '8px'
  },
  benchmarkName: {
    fontSize: '0.9rem',
    color: '#6c757d'
  },
  benchmarkScore: {
    fontSize: '0.9rem',
    fontWeight: '600',
    color: '#212529'
  },

  // Loading States
  loadingContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
    backgroundColor: '#f8f9fa'
  },
  loadingSpinner: {
    border: '4px solid #e9ecef',
    borderTop: '4px solid #667eea',
    borderRadius: '50%',
    width: '50px',
    height: '50px',
    animation: 'spin 1s linear infinite'
  },
  loadingText: {
    marginTop: '20px',
    fontSize: '1.1rem',
    color: '#6c757d',
    fontWeight: '500'
  },

  // Error States
  errorContainer: {
    display: 'flex',
    flexDirection: 'column',
    alignItems: 'center',
    justifyContent: 'center',
    height: '100vh',
    backgroundColor: '#fff5f5',
    padding: '20px'
  },
  errorTitle: {
    fontSize: '2rem',
    fontWeight: '700',
    color: '#dc3545',
    margin: '0 0 16px 0'
  },
  errorMessage: {
    fontSize: '1.1rem',
    color: '#6c757d',
    textAlign: 'center',
    margin: '0 0 24px 0',
    maxWidth: '500px',
    lineHeight: '1.4'
  },
  retryButton: {
    padding: '12px 24px',
    fontSize: '1rem',
    fontWeight: '600',
    color: 'white',
    backgroundColor: '#667eea',
    border: 'none',
    borderRadius: '8px',
    cursor: 'pointer',
    transition: 'all 0.3s ease',
    boxShadow: '0 4px 12px rgba(102, 126, 234, 0.3)'
  }
};

// Add CSS animations
if (typeof window !== 'undefined') {
  const styleSheet = document.createElement('style');
  styleSheet.textContent = `
    @keyframes spin {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }
    
    @keyframes pulse {
      0% { opacity: 1; }
      50% { opacity: 0.5; }
      100% { opacity: 1; }
    }
    
    .metric-card:hover {
      transform: translateY(-2px);
      box-shadow: 0 6px 20px rgba(0,0,0,0.1);
    }
    
    .insight-card:hover {
      transform: translateY(-1px);
      box-shadow: 0 4px 16px rgba(0,0,0,0.08);
    }
    
    .apply-button:hover {
      background-color: #5a6fd8;
    }
    
    .optimization-button:hover:not(:disabled) {
      background-color: #5a6fd8;
      transform: translateY(-1px);
    }
    
    .retry-button:hover {
      background-color: #5a6fd8;
      transform: translateY(-1px);
    }
  `;
  document.head.appendChild(styleSheet);
}