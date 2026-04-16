import { useState } from 'react'
import AgentTrace from './AgentTrace'

/**
 * Renders a simple markdown-like text to HTML.
 * Handles: headers, bold, italic, lists, code, tables, and line breaks.
 */
function renderMarkdown(text) {
  if (!text) return ''
  
  const lines = text.split('\n')
  let html = ''
  let inList = false
  let inTable = false
  let tableHasHeader = false
  
  for (let i = 0; i < lines.length; i++) {
    let line = lines[i]
    
    // Table rows
    if (line.trim().startsWith('|') && line.trim().endsWith('|')) {
      if (!inTable) {
        inTable = true
        tableHasHeader = false
        html += '<table>'
      }
      
      // Check if next line is separator (|---|---|)
      const nextLine = lines[i + 1]?.trim() || ''
      const isSeparator = /^\|[\s\-:|]+\|$/.test(line.trim())
      
      if (isSeparator) continue  // Skip separator lines
      
      const cells = line.split('|').filter((c, idx, arr) => idx > 0 && idx < arr.length - 1)
      
      if (!tableHasHeader) {
        html += '<thead><tr>'
        cells.forEach(cell => { html += `<th>${inlineFormat(cell.trim())}</th>` })
        html += '</tr></thead><tbody>'
        tableHasHeader = true
      } else {
        html += '<tr>'
        cells.forEach(cell => { html += `<td>${inlineFormat(cell.trim())}</td>` })
        html += '</tr>'
      }
      continue
    } else if (inTable) {
      html += '</tbody></table>'
      inTable = false
      tableHasHeader = false
    }
    
    // Headers
    if (line.startsWith('#### ')) {
      if (inList) { html += '</ul>'; inList = false }
      html += `<h4>${inlineFormat(line.slice(5))}</h4>`
      continue
    }
    if (line.startsWith('### ')) {
      if (inList) { html += '</ul>'; inList = false }
      html += `<h3>${inlineFormat(line.slice(4))}</h3>`
      continue
    }
    if (line.startsWith('## ')) {
      if (inList) { html += '</ul>'; inList = false }
      html += `<h2>${inlineFormat(line.slice(3))}</h2>`
      continue
    }
    if (line.startsWith('# ')) {
      if (inList) { html += '</ul>'; inList = false }
      html += `<h1>${inlineFormat(line.slice(2))}</h1>`
      continue
    }
    
    // Unordered list
    if (/^[\-\*•] /.test(line.trim())) {
      if (!inList) { html += '<ul>'; inList = true }
      html += `<li>${inlineFormat(line.trim().slice(2))}</li>`
      continue
    }
    
    // Ordered list
    if (/^\d+\. /.test(line.trim())) {
      if (!inList) { html += '<ol>'; inList = true }
      html += `<li>${inlineFormat(line.trim().replace(/^\d+\. /, ''))}</li>`
      continue
    }
    
    // Close list if not a list item
    if (inList && line.trim() === '') {
      html += '</ul>'
      inList = false
    }
    
    // Empty line
    if (line.trim() === '') {
      html += '<br/>'
      continue
    }
    
    // Paragraph
    if (inList) { html += '</ul>'; inList = false }
    html += `<p>${inlineFormat(line)}</p>`
  }
  
  if (inList) html += '</ul>'
  if (inTable) html += '</tbody></table>'
  
  return html
}

function inlineFormat(text) {
  return text
    .replace(/\*\*(.+?)\*\*/g, '<strong>$1</strong>')
    .replace(/\*(.+?)\*/g, '<em>$1</em>')
    .replace(/`(.+?)`/g, '<code>$1</code>')
    .replace(/⚠️/g, '⚠️')
}


function ChatMessage({ message }) {
  const isUser = message.role === 'user'
  
  return (
    <div className={`message message-${message.role}`}>
      <div className="message-avatar">
        {isUser ? '👤' : '🤖'}
      </div>
      <div style={{ flex: 1 }}>
        <div
          className="message-content"
          dangerouslySetInnerHTML={
            isUser
              ? { __html: message.content }
              : { __html: renderMarkdown(message.content) }
          }
        />
        {!isUser && message.agentTrace && (
          <AgentTrace
            trace={message.agentTrace}
            sources={message.sources}
            totalDuration={message.totalDuration}
          />
        )}
      </div>
    </div>
  )
}

export default ChatMessage
