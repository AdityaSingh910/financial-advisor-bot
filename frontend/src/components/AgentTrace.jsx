import { useState } from 'react'

const AGENT_META = {
  'Data Retriever': {
    icon: '🔍',
    color: 'retriever',
    label: 'Agent 1 — Data Retriever',
  },
  'Risk Analyst': {
    icon: '⚠️',
    color: 'risk',
    label: 'Agent 2 — Risk Analyst',
  },
  'Financial Advisor': {
    icon: '💡',
    color: 'advisor',
    label: 'Agent 3 — Financial Advisor',
  },
}

function AgentTrace({ trace, sources, totalDuration }) {
  const [isOpen, setIsOpen] = useState(false)

  if (!trace || trace.length === 0) return null

  return (
    <div className="agent-trace">
      <button
        className="agent-trace-toggle"
        onClick={() => setIsOpen(!isOpen)}
      >
        🔗 Agent Pipeline
        <span style={{ margin: '0 4px', color: 'var(--text-muted)' }}>•</span>
        {trace.length} agents
        <span style={{ margin: '0 4px', color: 'var(--text-muted)' }}>•</span>
        {totalDuration ? `${(totalDuration / 1000).toFixed(1)}s` : ''}
        <span className={`arrow ${isOpen ? 'open' : ''}`}>▼</span>
      </button>

      {isOpen && (
        <div className="agent-trace-panel">
          {trace.map((step, idx) => {
            const meta = AGENT_META[step.agent] || {
              icon: '⚙️',
              color: 'retriever',
              label: step.agent,
            }

            return (
              <div key={idx} className="agent-step">
                <div className="agent-step-header">
                  <div className="agent-step-name">
                    <div className={`agent-step-icon ${meta.color}`}>
                      {meta.icon}
                    </div>
                    {meta.label}
                  </div>
                  <div className="agent-step-duration">
                    {step.duration_ms
                      ? `${(step.duration_ms / 1000).toFixed(1)}s`
                      : ''}
                  </div>
                </div>
                <div className="agent-step-details">
                  {step.agent === 'Data Retriever' && (
                    <>
                      Retrieved {step.chunks_retrieved || 0} relevant chunks
                      {step.sources && step.sources.length > 0 && (
                        <div className="agent-step-sources">
                          {step.sources.map((src, i) => (
                            <span key={i} className="source-tag">
                              📄 {src}
                            </span>
                          ))}
                        </div>
                      )}
                    </>
                  )}
                  {step.agent === 'Risk Analyst' && (
                    <span>Analyzed financial risk factors and generated assessment</span>
                  )}
                  {step.agent === 'Financial Advisor' && (
                    <span>Generated comprehensive advisory response</span>
                  )}
                </div>
              </div>
            )
          })}
        </div>
      )}
    </div>
  )
}

export default AgentTrace
