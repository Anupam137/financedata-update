import React, { useState, useEffect, useRef } from 'react';
import { processQuery, clearConversation } from '../services/api.service';
import './SearchPage.css';

const SearchPage = () => {
  const [query, setQuery] = useState('');
  const [mode, setMode] = useState('sonar');
  const [sessionId, setSessionId] = useState(null);
  const [conversation, setConversation] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [followUpSuggestions, setFollowUpSuggestions] = useState([]);
  
  const resultsContainerRef = useRef(null);
  
  // Scroll to bottom of results when conversation updates
  useEffect(() => {
    if (resultsContainerRef.current) {
      resultsContainerRef.current.scrollTop = resultsContainerRef.current.scrollHeight;
    }
  }, [conversation]);

  const handleSubmit = async (e) => {
    if (e) e.preventDefault();
    
    if (!query.trim()) {
      setError('Please enter a query');
      return;
    }
    
    setLoading(true);
    setError(null);
    
    // Add user message to conversation immediately for better UX
    setConversation(prev => [...prev, { role: 'user', content: query }]);
    
    try {
      const response = await processQuery(query, mode, sessionId);
      
      // Save the session ID if this is the first message
      if (!sessionId && response.sessionId) {
        setSessionId(response.sessionId);
      }
      
      // Add assistant response to conversation
      setConversation(prev => [...prev, { role: 'assistant', content: response.response }]);
      
      // Set follow-up suggestions
      if (response.followUpSuggestions) {
        setFollowUpSuggestions(response.followUpSuggestions);
      }
      
      // Clear the input field
      setQuery('');
    } catch (err) {
      setError(err.message || 'An error occurred while processing your query');
      
      // Add error message to conversation
      setConversation(prev => [...prev, { 
        role: 'system', 
        content: `Error: ${err.message || 'An error occurred while processing your query'}`
      }]);
    } finally {
      setLoading(false);
    }
  };
  
  const handleFollowUpClick = (suggestion) => {
    setQuery(suggestion);
    handleSubmit();
  };
  
  const handleClearConversation = async () => {
    if (sessionId) {
      try {
        await clearConversation(sessionId);
        setConversation([]);
        setFollowUpSuggestions([]);
        setSessionId(null);
      } catch (err) {
        setError(err.message || 'Failed to clear conversation');
      }
    } else {
      setConversation([]);
      setFollowUpSuggestions([]);
    }
  };

  return (
    <div className="search-page">
      <div className="search-header">
        <h1>Financial Search Engine</h1>
        <p>Ask any financial question about companies, stocks, or markets</p>
      </div>
      
      {conversation.length > 0 && (
        <div className="conversation-container card" ref={resultsContainerRef}>
          {conversation.map((message, index) => (
            <div key={index} className={`message ${message.role}`}>
              <div className="message-content">
                {message.role === 'user' ? (
                  <p>{message.content}</p>
                ) : message.role === 'system' ? (
                  <p className="error-message">{message.content}</p>
                ) : (
                  <div dangerouslySetInnerHTML={{ __html: message.content.replace(/\n/g, '<br />') }} />
                )}
              </div>
            </div>
          ))}
          
          {followUpSuggestions.length > 0 && (
            <div className="follow-up-suggestions">
              <p>You might want to ask:</p>
              <div className="suggestions-container">
                {followUpSuggestions.map((suggestion, index) => (
                  <button 
                    key={index} 
                    className="suggestion-btn"
                    onClick={() => handleFollowUpClick(suggestion)}
                    disabled={loading}
                  >
                    {suggestion}
                  </button>
                ))}
              </div>
            </div>
          )}
        </div>
      )}
      
      <div className="search-container card">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <input
              type="text"
              className="form-control search-input"
              placeholder="e.g., What is Apple's current stock price? or Compare Tesla and Ford's profit margins"
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              disabled={loading}
            />
          </div>
          
          <div className="search-options">
            <div className="mode-selector">
              <label>
                <input
                  type="radio"
                  name="mode"
                  value="sonar"
                  checked={mode === 'sonar'}
                  onChange={() => setMode('sonar')}
                  disabled={loading}
                />
                Quick Search
              </label>
              <label>
                <input
                  type="radio"
                  name="mode"
                  value="deep-research"
                  checked={mode === 'deep-research'}
                  onChange={() => setMode('deep-research')}
                  disabled={loading}
                />
                Deep Research
              </label>
            </div>
            
            <div className="button-group">
              {conversation.length > 0 && (
                <button 
                  type="button" 
                  className="btn btn-secondary" 
                  onClick={handleClearConversation}
                  disabled={loading}
                >
                  Clear Chat
                </button>
              )}
              
              <button type="submit" className="btn btn-primary" disabled={loading}>
                {loading ? 'Searching...' : 'Search'}
              </button>
            </div>
          </div>
        </form>
      </div>
      
      {error && conversation.length === 0 && (
        <div className="error-message card">
          <p>{error}</p>
        </div>
      )}
      
      {conversation.length === 0 && (
        <div className="search-tips card">
          <h3>Search Tips</h3>
          <ul>
            <li>Use <strong>Quick Search</strong> for simple queries like stock prices or basic company info</li>
            <li>Use <strong>Deep Research</strong> for detailed analysis and comparisons</li>
            <li>Include ticker symbols (e.g., AAPL, TSLA) for more accurate results</li>
            <li>Be specific about what financial information you're looking for</li>
            <li>You can ask follow-up questions to continue the conversation</li>
          </ul>
        </div>
      )}
    </div>
  );
};

export default SearchPage; 