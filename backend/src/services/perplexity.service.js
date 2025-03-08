const axios = require('axios');
const apiConfig = require('../config/api.config');

// Initialize Perplexity API client
let perplexityApi;
try {
  perplexityApi = axios.create({
    baseURL: apiConfig.perplexity.baseUrl,
    headers: {
      'Authorization': `Bearer ${apiConfig.perplexity.apiKey}`,
      'Content-Type': 'application/json'
    }
  });
  console.log('Perplexity API client initialized successfully');
} catch (error) {
  console.error('Error initializing Perplexity API client:', error);
  console.warn('Using fallback implementation for Perplexity. Real API data will not be available.');
  
  // Fallback implementation only if initialization fails
  perplexityApi = {
    post: async () => {
      throw new Error('Perplexity API is not properly configured. Please check your API key.');
    }
  };
}

/**
 * Use Perplexity Sonar for AI-powered financial search with real-time web intelligence
 * @param {string} query - User's financial query
 * @param {object} options - Additional options for the search
 * @returns {Promise<object>} - Sonar search results
 */
async function searchWithSonar(query, options = {}) {
  try {
    // Enhance the query to focus on real-time financial information if needed
    let enhancedQuery = query;
    if (options.emphasizeRecent) {
      enhancedQuery = `${query} (focus on the most recent information and latest news)`;
    }
    
    // Format the request according to Perplexity API documentation
    const response = await perplexityApi.post(apiConfig.perplexity.sonarEndpoint, {
      model: apiConfig.perplexity.models.sonar,
      messages: [
        {
          role: "system",
          content: "You are a financial assistant with access to real-time web search. Provide accurate, up-to-date information about financial markets, stocks, companies, and economic news. Include relevant data points and cite your sources."
        },
        {
          role: "user",
          content: enhancedQuery
        }
      ],
      options: {
        temperature: options.temperature || 0.7,
        max_tokens: options.maxTokens || 1000
      }
    });
    
    return {
      content: response.data.choices[0].message.content,
      citations: response.data.choices[0].message.context?.citations || [],
      search_context: response.data.choices[0].message.context || {},
      metadata: {
        query: enhancedQuery,
        timestamp: new Date().toISOString(),
        source: 'perplexity_sonar'
      }
    };
  } catch (error) {
    console.error('Perplexity API Error (Sonar):', error.response?.data || error.message);
    throw new Error(`Failed to search with Perplexity Sonar: ${error.message}`);
  }
}

/**
 * Use Perplexity Deep Research for in-depth company analysis
 * @param {string} query - User's research query
 * @param {object} options - Additional options for the research
 * @returns {Promise<object>} - Deep research results
 */
async function conductDeepResearch(query, options = {}) {
  try {
    // Format the request according to Perplexity API documentation
    const response = await perplexityApi.post(apiConfig.perplexity.deepResearchEndpoint, {
      model: apiConfig.perplexity.models.deepResearch,
      messages: [
        {
          role: "system",
          content: "You are a financial analyst specializing in deep research and comprehensive analysis. Provide detailed, well-structured information about companies, markets, and financial trends. Include quantitative data, qualitative analysis, and cite your sources."
        },
        {
          role: "user",
          content: query
        }
      ],
      options: {
        temperature: options.temperature || 0.5,
        max_tokens: options.maxTokens || 2000
      }
    });
    
    return {
      content: response.data.choices[0].message.content,
      citations: response.data.choices[0].message.context?.citations || [],
      analysis: response.data.choices[0].message.context || {},
      metadata: {
        query,
        timestamp: new Date().toISOString(),
        source: 'perplexity_deep_research'
      }
    };
  } catch (error) {
    console.error('Perplexity API Error (Deep Research):', error.response?.data || error.message);
    throw new Error(`Failed to conduct deep research with Perplexity: ${error.message}`);
  }
}

/**
 * Compare multiple companies using Perplexity Deep Research
 * @param {Array<string>} tickers - Array of stock ticker symbols to compare
 * @param {Array<string>} metrics - Array of metrics to compare
 * @returns {Promise<object>} - Company comparison results
 */
async function compareCompanies(tickers, metrics = ['revenue', 'profit_margin', 'growth']) {
  try {
    const query = `Compare the following companies: ${tickers.join(', ')} based on these metrics: ${metrics.join(', ')}. Include the most recent financial data and news. Format the comparison in a structured way with sections for each metric.`;
    
    // Format the request according to Perplexity API documentation
    const response = await perplexityApi.post(apiConfig.perplexity.deepResearchEndpoint, {
      model: apiConfig.perplexity.models.deepResearch,
      messages: [
        {
          role: "system",
          content: "You are a financial analyst specializing in company comparisons. Provide detailed, data-driven comparisons between companies based on specified metrics. Include quantitative data, qualitative analysis, and cite your sources."
        },
        {
          role: "user",
          content: query
        }
      ],
      options: {
        temperature: 0.3,
        max_tokens: 3000
      }
    });
    
    return {
      content: response.data.choices[0].message.content,
      citations: response.data.choices[0].message.context?.citations || [],
      comparison_table: extractComparisonData(response.data.choices[0].message.content, tickers, metrics),
      metadata: {
        tickers,
        metrics,
        timestamp: new Date().toISOString(),
        source: 'perplexity_company_comparison'
      }
    };
  } catch (error) {
    console.error('Perplexity API Error (Company Comparison):', error.response?.data || error.message);
    throw new Error(`Failed to compare companies with Perplexity: ${error.message}`);
  }
}

/**
 * Get real-time market news and sentiment
 * @param {string} topic - Topic to get news about (e.g., "crypto", "tech stocks", "AAPL")
 * @param {object} options - Additional options
 * @returns {Promise<object>} - News and sentiment results
 */
async function getMarketNewsAndSentiment(topic, options = {}) {
  try {
    const query = `What are the latest news and current market sentiment about ${topic}? Focus on the most recent developments within the last 24 hours. Include specific data points and market reactions.`;
    
    // Format the request according to Perplexity API documentation
    const response = await perplexityApi.post(apiConfig.perplexity.sonarEndpoint, {
      model: apiConfig.perplexity.models.sonar,
      messages: [
        {
          role: "system",
          content: "You are a financial news analyst with access to real-time web search. Provide the latest news and market sentiment about financial topics. Focus on factual reporting, include relevant data points, and cite your sources."
        },
        {
          role: "user",
          content: query
        }
      ],
      options: {
        temperature: options.temperature || 0.7,
        max_tokens: options.maxTokens || 1500
      }
    });
    
    return {
      content: response.data.choices[0].message.content,
      citations: response.data.choices[0].message.context?.citations || [],
      sentiment: extractSentiment(response.data.choices[0].message.content),
      metadata: {
        topic,
        timestamp: new Date().toISOString(),
        source: 'perplexity_market_news'
      }
    };
  } catch (error) {
    console.error('Perplexity API Error (Market News):', error.response?.data || error.message);
    throw new Error(`Failed to get market news and sentiment: ${error.message}`);
  }
}

/**
 * Extract sentiment from text content
 * @param {string} content - Text content to analyze
 * @returns {string} - Sentiment (positive, negative, neutral, or mixed)
 */
function extractSentiment(content) {
  const lowerContent = content.toLowerCase();
  
  // Count sentiment indicators
  const positiveTerms = ['positive', 'bullish', 'optimistic', 'upbeat', 'growth', 'gain', 'increase', 'up', 'rally', 'outperform'];
  const negativeTerms = ['negative', 'bearish', 'pessimistic', 'downbeat', 'decline', 'loss', 'decrease', 'down', 'fall', 'underperform'];
  
  let positiveCount = 0;
  let negativeCount = 0;
  
  positiveTerms.forEach(term => {
    const regex = new RegExp(`\\b${term}\\b`, 'g');
    const matches = lowerContent.match(regex);
    if (matches) positiveCount += matches.length;
  });
  
  negativeTerms.forEach(term => {
    const regex = new RegExp(`\\b${term}\\b`, 'g');
    const matches = lowerContent.match(regex);
    if (matches) negativeCount += matches.length;
  });
  
  // Determine sentiment
  if (positiveCount > negativeCount * 2) return 'positive';
  if (negativeCount > positiveCount * 2) return 'negative';
  if (positiveCount > 0 && negativeCount > 0) return 'mixed';
  return 'neutral';
}

/**
 * Extract structured comparison data from text content
 * @param {string} content - Text content to analyze
 * @param {Array<string>} tickers - Array of ticker symbols
 * @param {Array<string>} metrics - Array of metrics
 * @returns {object} - Structured comparison data
 */
function extractComparisonData(content, tickers, metrics) {
  // Simple extraction - in a real implementation, this would be more sophisticated
  const result = {
    companies: tickers,
    metrics: {}
  };
  
  // Initialize metrics
  metrics.forEach(metric => {
    result.metrics[metric] = {};
    tickers.forEach(ticker => {
      result.metrics[metric][ticker] = 'N/A';
    });
  });
  
  // Try to extract values from content
  metrics.forEach(metric => {
    tickers.forEach(ticker => {
      // Look for patterns like "Revenue (AAPL): $365.8B" or "AAPL revenue: $365.8B"
      const patterns = [
        new RegExp(`${metric}\\s*\\(${ticker}\\)\\s*:?\\s*([\\$\\d\\.\\,\\%]+)`, 'i'),
        new RegExp(`${ticker}\\s*${metric}\\s*:?\\s*([\\$\\d\\.\\,\\%]+)`, 'i'),
        new RegExp(`${ticker}[^\\n]*${metric}[^\\n]*?([\\$\\d\\.\\,\\%]+)`, 'i')
      ];
      
      for (const pattern of patterns) {
        const match = content.match(pattern);
        if (match && match[1]) {
          result.metrics[metric][ticker] = match[1].trim();
          break;
        }
      }
    });
  });
  
  return result;
}

module.exports = {
  searchWithSonar,
  conductDeepResearch,
  compareCompanies,
  getMarketNewsAndSentiment
}; 