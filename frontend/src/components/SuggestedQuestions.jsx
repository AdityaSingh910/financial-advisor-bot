const QUESTIONS = [
  {
    text: 'Should I take a home loan at 8.5% interest rate?',
    category: 'Loans',
    icon: '🏠',
  },
  {
    text: 'What is a good CIBIL score and how can I improve mine?',
    category: 'Credit Score',
    icon: '📊',
  },
  {
    text: 'Compare SIP vs Fixed Deposit for a 5-year investment',
    category: 'Investments',
    icon: '📈',
  },
  {
    text: 'How much term insurance cover do I need?',
    category: 'Insurance',
    icon: '🛡️',
  },
  {
    text: 'Best tax saving options under Section 80C',
    category: 'Tax Planning',
    icon: '💰',
  },
  {
    text: 'Is it better to prepay home loan or invest in mutual funds?',
    category: 'Financial Planning',
    icon: '🤔',
  },
]

function SuggestedQuestions({ onSelect }) {
  return (
    <div className="suggestions">
      {QUESTIONS.map((q, idx) => (
        <div
          key={idx}
          className="suggestion-card"
          onClick={() => onSelect(q.text)}
        >
          <div className="suggestion-icon">{q.icon}</div>
          <div className="suggestion-text">{q.text}</div>
          <div className="suggestion-category">{q.category}</div>
        </div>
      ))}
    </div>
  )
}

export default SuggestedQuestions
