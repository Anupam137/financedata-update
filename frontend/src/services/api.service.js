import axios from 'axios';

// Create axios instance for API calls
const apiClient = axios.create({
  baseURL: process.env.REACT_APP_API_URL || 'http://localhost:3001/api',
  headers: {
    'Content-Type': 'application/json'
  }
});

/**
 * Process a financial query
 * @param {string} query - User's financial query
 * @param {string} mode - Search mode ('sonar' or 'deep-research')
 * @param {string} sessionId - Session ID for conversation tracking
 * @returns {Promise<object>} - API response
 */
export const processQuery = async (query, mode = 'sonar', sessionId = null) => {
  try {
    const response = await apiClient.post('/query', { query, mode, sessionId });
    return response.data;
  } catch (error) {
    console.error('API Error (Process Query):', error.response?.data || error.message);
    throw new Error(error.response?.data?.message || 'Failed to process query');
  }
};

/**
 * Compare multiple companies
 * @param {Array<string>} tickers - Array of stock ticker symbols to compare
 * @param {Array<string>} metrics - Array of metrics to compare
 * @param {string} sessionId - Session ID for conversation tracking
 * @returns {Promise<object>} - API response
 */
export const compareCompanies = async (tickers, metrics = ['revenue', 'profit_margin', 'growth'], sessionId = null) => {
  try {
    const response = await apiClient.post('/compare', { tickers, metrics, sessionId });
    return response.data;
  } catch (error) {
    console.error('API Error (Compare Companies):', error.response?.data || error.message);
    throw new Error(error.response?.data?.message || 'Failed to compare companies');
  }
};

/**
 * Clear conversation history
 * @param {string} sessionId - Session ID for the conversation to clear
 * @returns {Promise<object>} - API response
 */
export const clearConversation = async (sessionId) => {
  try {
    const response = await apiClient.delete(`/conversation/${sessionId}`);
    return response.data;
  } catch (error) {
    console.error('API Error (Clear Conversation):', error.response?.data || error.message);
    throw new Error(error.response?.data?.message || 'Failed to clear conversation');
  }
};

/**
 * Get latest news and market sentiment about a topic
 * @param {string} topic - Topic to get news about (e.g., "crypto", "tech stocks", "AAPL")
 * @param {string} sessionId - Session ID for conversation tracking
 * @returns {Promise<object>} - API response
 */
export const getMarketNews = async (topic, sessionId = null) => {
  try {
    const response = await apiClient.get(`/news/${encodeURIComponent(topic)}`, {
      params: { sessionId }
    });
    return response.data;
  } catch (error) {
    console.error('API Error (Market News):', error.response?.data || error.message);
    throw new Error(error.response?.data?.message || 'Failed to get market news');
  }
}; 