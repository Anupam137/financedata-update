const axios = require('axios');
const apiConfig = require('../config/api.config');

// Initialize Polygon API client
let polygonApi;
try {
  polygonApi = axios.create({
    baseURL: apiConfig.polygon.baseUrl,
    params: {
      apiKey: apiConfig.polygon.apiKey
    }
  });
  console.log('Polygon API client initialized successfully');
} catch (error) {
  console.error('Error initializing Polygon API client:', error);
  console.warn('Using fallback implementation for Polygon. Real API data will not be available.');
  
  // Fallback implementation only if initialization fails
  polygonApi = {
    get: async () => {
      throw new Error('Polygon API is not properly configured. Please check your API key.');
    }
  };
}

/**
 * Get stock price data for a ticker
 * @param {string} ticker - Stock ticker symbol
 * @param {string} timespan - Timespan for data (day, minute, hour, week, month, quarter, year)
 * @param {number} limit - Number of data points to return
 * @returns {Promise<object>} - Stock price data
 */
async function getStockPrice(ticker, timespan = 'day', limit = 5) {
  try {
    // Get current date and format it
    const today = new Date();
    const endDate = today.toISOString().split('T')[0];
    
    // Calculate start date (30 days ago)
    const startDate = new Date(today);
    startDate.setDate(today.getDate() - 30);
    const formattedStartDate = startDate.toISOString().split('T')[0];
    
    const response = await polygonApi.get(`/v2/aggs/ticker/${ticker}/range/1/${timespan}/${formattedStartDate}/${endDate}`, {
      params: {
        adjusted: true,
        sort: 'desc',
        limit
      }
    });
    
    return response.data;
  } catch (error) {
    console.error('Polygon API Error (Stock Price):', error.response?.data || error.message);
    throw new Error(`Failed to get stock price for ${ticker}: ${error.message}`);
  }
}

/**
 * Get company details
 * @param {string} ticker - Stock ticker symbol
 * @returns {Promise<object>} - Company details
 */
async function getCompanyDetails(ticker) {
  try {
    const response = await polygonApi.get(`/v3/reference/tickers/${ticker}`);
    return response.data;
  } catch (error) {
    console.error('Polygon API Error (Company Details):', error.response?.data || error.message);
    throw new Error(`Failed to get company details for ${ticker}: ${error.message}`);
  }
}

/**
 * Get latest news for a ticker
 * @param {string} ticker - Stock ticker symbol
 * @param {number} limit - Number of news items to return
 * @returns {Promise<object>} - News data
 */
async function getTickerNews(ticker, limit = 5) {
  try {
    const response = await polygonApi.get('/v2/reference/news', {
      params: {
        ticker,
        limit,
        order: 'desc',
        sort: 'published_utc'
      }
    });
    
    return response.data;
  } catch (error) {
    console.error('Polygon API Error (News):', error.response?.data || error.message);
    throw new Error(`Failed to get news for ${ticker}: ${error.message}`);
  }
}

/**
 * Get financial statements for a company
 * @param {string} ticker - Stock ticker symbol
 * @param {string} type - Statement type (income, balance, cash)
 * @param {number} limit - Number of statements to return
 * @returns {Promise<object>} - Financial statement data
 */
async function getFinancialStatements(ticker, type = 'income', limit = 4) {
  try {
    const response = await polygonApi.get(`/vX/reference/financials`, {
      params: {
        ticker,
        type,
        limit,
        sort: 'filing_date',
        order: 'desc'
      }
    });
    
    return response.data;
  } catch (error) {
    console.error('Polygon API Error (Financials):', error.response?.data || error.message);
    throw new Error(`Failed to get financial statements for ${ticker}: ${error.message}`);
  }
}

module.exports = {
  getStockPrice,
  getCompanyDetails,
  getTickerNews,
  getFinancialStatements
}; 