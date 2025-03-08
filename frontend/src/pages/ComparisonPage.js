import React, { useState, useEffect, useRef } from 'react';
import { compareCompanies, clearConversation } from '../services/api.service';
import './ComparisonPage.css';

const ComparisonPage = () => {
  const [tickers, setTickers] = useState('');
  const [metrics, setMetrics] = useState('revenue,profit_margin,growth');
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
    
    if (!tickers.trim()) {
      setError('Please enter at least two ticker symbols');
      return;
    }
    
    const tickerArray = tickers.split(',').map(ticker => ticker.trim().toUpperCase());
    
    if (tickerArray.length < 2) {
      setError('Please enter at least two ticker symbols');
      return;
    }
    
    const metricsArray = metrics.split(',').map(metric => metric.trim());
    
    setLoading(true);
    setError(null);
    
    // Add user message to conversation immediately for better UX
    const userMessage = `Compare these companies: ${tickerArray.join(', ')} based on ${metricsArray.join(', ')}`;
    setConversation(prev => [...prev, { role: 'user', content: userMessage }]);
    
    try {
      const response = await compareCompanies(tickerArray, metricsArray, sessionId);
      
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
    } catch (err) {
      setError(err.message || 'An error occurred while comparing companies');
      
      // Add error message to conversation
      setConversation(prev => [...prev, { 
        role: 'system', 
        content: `Error: ${err.message || 'An error occurred while comparing companies'}`
      }]);
    } finally {
      setLoading(false);
    }
  };
  
  const handleFollowUpClick = (suggestion) => {
    // For follow-up questions after comparison, we'll use the same format as the search page
    // by redirecting to the search page with the suggestion
    window.location.href = `/?query=${encodeURIComponent(suggestion)}&sessionId=${sessionId}`;
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
    <div className="comparison-page">
      <div className="comparison-header">
        <h1>Compare Companies</h1>
        <p>Compare financial metrics across multiple companies</p>
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
      
      <div className="comparison-form card">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label htmlFor="tickers">Ticker Symbols (comma-separated)</label>
            <input
              type="text"
              id="tickers"
              className="form-control"
              placeholder="e.g., AAPL,MSFT,GOOGL"
              value={tickers}
              onChange={(e) => setTickers(e.target.value)}
              disabled={loading}
            />
            <small>Enter at least two ticker symbols separated by commas</small>
          </div>
          
          <div className="form-group">
            <label htmlFor="metrics">Metrics to Compare (comma-separated)</label>
            <input
              type="text"
              id="metrics"
              className="form-control"
              placeholder="e.g., revenue,profit_margin,growth"
              value={metrics}
              onChange={(e) => setMetrics(e.target.value)}
              disabled={loading}
            />
            <small>Common metrics: revenue, profit_margin, growth, pe_ratio, market_cap</small>
          </div>
          
          <div className="button-group">
            {conversation.length > 0 && (
              <button 
                type="button" 
                className="btn btn-secondary" 
                onClick={handleClearConversation}
                disabled={loading}
              >
                Clear Results
              </button>
            )}
            
            <button type="submit" className="btn btn-primary" disabled={loading}>
              {loading ? 'Comparing...' : 'Compare Companies'}
            </button>
          </div>
        </form>
      </div>
      
      {error && conversation.length === 0 && (
        <div className="error-message card">
          <p>{error}</p>
        </div>
      )}
      
      {conversation.length === 0 && (
        <div className="comparison-tips card">
          <h3>Comparison Tips</h3>
          <ul>
            <li>Compare similar companies within the same industry for more meaningful insights</li>
            <li>Include 3-5 companies for optimal comparison results</li>
            <li>Choose metrics that are relevant to the industry you're analyzing</li>
            <li>For tech companies, consider metrics like R&D spending and revenue growth</li>
            <li>For retail companies, consider metrics like same-store sales and inventory turnover</li>
          </ul>
        </div>
      )}
    </div>
  );
};

export default ComparisonPage; 