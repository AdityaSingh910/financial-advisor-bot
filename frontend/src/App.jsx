import { useState, useRef, useEffect } from 'react'
import ChatMessage from './components/ChatMessage'
import SuggestedQuestions from './components/SuggestedQuestions'
import './index.css'

const API_BASE = 'http://localhost:8000'

function App() {
  const [messages, setMessages] = useState([])
  const [input, setInput] = useState('')
  const [isLoading, setIsLoading] = useState(false)
  const [loadingAgent, setLoadingAgent] = useState('')
  const [theme, setTheme] = useState('dark')
  const [error, setError] = useState(null)
  const [backendStatus, setBackendStatus] = useState('checking')
  const chatEndRef = useRef(null)
  const inputRef = useRef(null)

  // Apply theme
  useEffect(() => {
    document.documentElement.setAttribute('data-theme', theme)
  }, [theme])

  // Auto-scroll to bottom
  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, isLoading])

  // Focus input on mount
  useEffect(() => {
    inputRef.current?.focus()
  }, [])

  // Check backend health
  useEffect(() => {
    const checkHealth = async () => {
      try {
        const res = await fetch(`${API_BASE}/api/health`)
        if (res.ok) {
          const data = await res.json()
          if (data.api_key_configured && data.vector_store_ready) {
            setBackendStatus('online')
          } else if (!data.api_key_configured) {
            setBackendStatus('no-key')
          } else {
            setBackendStatus('no-vectorstore')
          }
        } else {
          setBackendStatus('offline')
        }
      } catch {
        setBackendStatus('offline')
      }
    }
    checkHealth()
    const interval = setInterval(checkHealth, 15000)
    return () => clearInterval(interval)
  }, [])

  const toggleTheme = () => {
    setTheme(prev => prev === 'dark' ? 'light' : 'dark')
  }

  const clearChat = () => {
    setMessages([])
    setError(null)
  }

  const sendMessage = async (text) => {
    const query = text || input.trim()
    if (!query || isLoading) return

    setInput('')
    setError(null)

    // Add user message
    const userMsg = { role: 'user', content: query }
    setMessages(prev => [...prev, userMsg])

    // Start loading
    setIsLoading(true)
    setLoadingAgent('Data Retriever')

    // Simulate agent progression for UX
    const agentTimer1 = setTimeout(() => setLoadingAgent('Risk Analyst'), 2500)
    const agentTimer2 = setTimeout(() => setLoadingAgent('Financial Advisor'), 6000)

    try {
      const response = await fetch(`${API_BASE}/api/chat`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ query }),
      })

      clearTimeout(agentTimer1)
      clearTimeout(agentTimer2)

      if (!response.ok) {
        const errData = await response.json().catch(() => ({}))
        throw new Error(errData.detail || `Server error: ${response.status}`)
      }

      const data = await response.json()

      if (!data.success) {
        throw new Error(data.error || 'Pipeline failed')
      }

      const aiMsg = {
        role: 'ai',
        content: data.response,
        riskAnalysis: data.risk_analysis,
        sources: data.sources,
        agentTrace: data.agent_trace,
        totalDuration: data.total_duration_ms,
      }
      setMessages(prev => [...prev, aiMsg])
    } catch (err) {
      clearTimeout(agentTimer1)
      clearTimeout(agentTimer2)

      let errorMsg = err.message
      if (err.message === 'Failed to fetch') {
        errorMsg = 'Cannot connect to the backend server. Please make sure the backend is running: cd backend && python main.py'
      }
      setError(errorMsg)
    } finally {
      setIsLoading(false)
      setLoadingAgent('')
      inputRef.current?.focus()
    }
  }

  const handleKeyDown = (e) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault()
      sendMessage()
    }
  }

  const handleSuggestion = (text) => {
    sendMessage(text)
  }

  const getStatusText = () => {
    switch (backendStatus) {
      case 'online': return 'Connected to AI Backend'
      case 'no-key': return 'API key not configured — set GOOGLE_API_KEY in backend/.env'
      case 'no-vectorstore': return 'Vector store missing — run python ingest.py'
      case 'offline': return 'Backend offline — run: cd backend && python main.py'
      default: return 'Checking connection...'
    }
  }

  return (
    <div className="app">
      {/* Header */}
      <header className="header">
        <div className="header-brand">
          <div className="header-logo">🏦</div>
          <div>
            <div className="header-title">FinAdvisor AI</div>
            <div className="header-subtitle">Agentic RAG Assistant</div>
          </div>
        </div>
        <div className="header-actions">
          {messages.length > 0 && (
            <button className="clear-btn" onClick={clearChat}>
              Clear Chat
            </button>
          )}
          <button className="theme-toggle" onClick={toggleTheme} title="Toggle theme">
            {theme === 'dark' ? '☀️' : '🌙'}
          </button>
        </div>
      </header>

      {/* Chat Area */}
      <div className="chat-area">
        {messages.length === 0 && !isLoading ? (
          <div className="welcome">
            <div className="welcome-hero">
              <div className="welcome-icon">🏦</div>
              <div className="welcome-orbit">
                <div className="orbit-dot"></div>
                <div className="orbit-dot"></div>
                <div className="orbit-dot"></div>
              </div>
            </div>
            <h2>Financial Advisory AI</h2>
            <p>
              Powered by a 3-agent pipeline — I retrieve relevant data, 
              analyze risks, and provide comprehensive financial advice.
            </p>
            <div className="welcome-badges">
              <div className="welcome-badge">
                <span className="badge-dot"></span>
                RAG Retrieval
              </div>
              <div className="welcome-badge">
                <span className="badge-dot"></span>
                Risk Analysis
              </div>
              <div className="welcome-badge">
                <span className="badge-dot"></span>
                AI Advisory
              </div>
            </div>
            <SuggestedQuestions onSelect={handleSuggestion} />
          </div>
        ) : (
          <>
            {messages.map((msg, idx) => (
              <ChatMessage key={idx} message={msg} />
            ))}
          </>
        )}

        {/* Loading / Typing Indicator */}
        {isLoading && (
          <div className="message message-ai">
            <div className="message-avatar">🤖</div>
            <div>
              <div className="typing-indicator">
                <div className="typing-dots">
                  <div className="typing-dot"></div>
                  <div className="typing-dot"></div>
                  <div className="typing-dot"></div>
                </div>
              </div>
              <div className="typing-label" style={{ marginTop: '8px' }}>
                <span className="typing-agent">{loadingAgent}</span> is working...
              </div>
            </div>
          </div>
        )}

        {/* Error */}
        {error && (
          <div className="error-message">
            ⚠️ {error}
          </div>
        )}

        <div ref={chatEndRef} />
      </div>

      {/* Status Bar */}
      <div className="status-bar">
        <span className={`status-dot ${backendStatus !== 'online' ? 'offline' : ''}`}></span>
        <span>{getStatusText()}</span>
      </div>

      {/* Input Area */}
      <div className="input-area">
        <div className="input-container">
          <div className="input-wrapper">
            <textarea
              ref={inputRef}
              className="input-field"
              placeholder="Ask about loans, investments, credit scores, insurance..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              disabled={isLoading}
              rows={1}
            />
          </div>
          <button
            className="send-btn"
            onClick={() => sendMessage()}
            disabled={!input.trim() || isLoading}
            title="Send message"
          >
            ➤
          </button>
        </div>
      </div>
    </div>
  )
}

export default App
