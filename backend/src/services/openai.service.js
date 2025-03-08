const { OpenAI } = require('openai');
const apiConfig = require('../config/api.config');

// Initialize OpenAI client
let openai;
try {
  openai = new OpenAI({
    apiKey: apiConfig.openai.apiKey
  });
  console.log('OpenAI client initialized successfully');
} catch (error) {
  console.error('Error initializing OpenAI client:', error);
  console.warn('Using fallback implementation for OpenAI. Real API data will not be available.');
  
  // Fallback implementation only if initialization fails
  openai = {
    chat: {
      completions: {
        create: async () => {
          throw new Error('OpenAI API is not properly configured. Please check your API key.');
        }
      }
    }
  };
}

// Financial domain knowledge system prompt
const FINANCIAL_SYSTEM_PROMPT = `You are an expert financial assistant with deep knowledge of:
- Stock markets, indices, and trading
- Company fundamentals and financial statements
- Cryptocurrencies and blockchain technology
- Economic indicators and monetary policy
- Investment strategies and portfolio management
- Financial news and market events
- Technical and fundamental analysis
- Global markets and international finance

Provide conversational, helpful responses that are accurate and insightful. 
When discussing financial data, include relevant metrics and context.
If you're uncertain about specific data points, acknowledge the limitations.
Always maintain a balanced perspective when discussing investments.`;

/**
 * Process user query through OpenAI LLM
 * @param {string} query - User's financial query
 * @param {object} options - Additional options for the API call
 * @param {array} conversationHistory - Previous messages in the conversation
 * @returns {Promise<object>} - LLM response
 */
async function processQuery(query, options = {}, conversationHistory = []) {
  try {
    // Build messages array with conversation history
    const messages = [
      {
        role: 'system',
        content: FINANCIAL_SYSTEM_PROMPT
      }
    ];
    
    // Add conversation history if available
    if (conversationHistory && conversationHistory.length > 0) {
      // Only include the last 10 messages to stay within context limits
      const recentHistory = conversationHistory.slice(-10);
      messages.push(...recentHistory);
    }
    
    // Add the current query
    messages.push({
      role: 'user',
      content: query
    });

    const response = await openai.chat.completions.create({
      model: options.model || apiConfig.openai.model,
      messages: messages,
      max_tokens: options.maxTokens || apiConfig.openai.maxTokens,
      temperature: options.temperature || 0.7
    });

    return {
      content: response.choices[0].message.content,
      usage: response.usage,
      message: response.choices[0].message
    };
  } catch (error) {
    console.error('OpenAI API Error:', error);
    throw new Error(`Failed to process query with OpenAI: ${error.message}`);
  }
}

/**
 * Analyze which APIs should be called based on the user query
 * @param {string} query - User's financial query
 * @param {array} conversationHistory - Previous messages in the conversation
 * @returns {Promise<object>} - Analysis of which APIs to call
 */
async function analyzeQueryForApiCalls(query, conversationHistory = []) {
  try {
    // Build messages array with conversation history for context
    const messages = [
      {
        role: 'system',
        content: `You are a financial data router. Your job is to analyze a user query and determine which financial APIs should be called to answer it.
        Available APIs:
        - polygon: For stock prices, market news, SEC filings, company details, and historical price data
        - financialDatasets: For financial statements, institutional ownership, segmented financials, and historical metrics
        - perplexitySonar: For AI-powered search of financial data, quick answers, and general market information
        - perplexityDeepResearch: For in-depth company analysis, detailed comparisons, and comprehensive research
        
        Also determine if this is a comparison query where the user wants to compare multiple companies or assets.
        
        Return a JSON object with:
        1. Boolean values for each API indicating whether it should be called
        2. An "isComparisonQuery" boolean indicating if this is a comparison query
        3. An "isNewsQuery" boolean indicating if this is primarily a news-focused query
        4. An "entities" object with any detected tickers, company names, cryptocurrencies, or other financial entities
        `
      }
    ];
    
    // Add relevant conversation history for context
    if (conversationHistory && conversationHistory.length > 0) {
      // Only include the last 5 messages to stay focused on recent context
      const recentHistory = conversationHistory.slice(-5);
      messages.push(...recentHistory);
    }
    
    // Add the current query
    messages.push({
      role: 'user',
      content: query
    });

    const response = await openai.chat.completions.create({
      model: apiConfig.openai.model,
      messages: messages,
      response_format: { type: "json_object" },
      max_tokens: 500,
      temperature: 0.3
    });

    // Parse the JSON response
    const apiCallDecision = JSON.parse(response.choices[0].message.content);
    
    // Simple heuristic backup in case the LLM doesn't detect comparison properly
    if (!apiCallDecision.isComparisonQuery) {
      const comparisonKeywords = ['compare', 'comparison', 'versus', 'vs', 'vs.', 'difference between'];
      const queryLower = query.toLowerCase();
      
      if (comparisonKeywords.some(keyword => queryLower.includes(keyword))) {
        apiCallDecision.isComparisonQuery = true;
        
        // If it's a comparison query, we should use the deep research API
        apiCallDecision.perplexityDeepResearch = true;
      }
    }
    
    return apiCallDecision;
  } catch (error) {
    console.error('API Call Analysis Error:', error);
    throw new Error(`Failed to analyze query for API calls: ${error.message}`);
  }
}

/**
 * Format and combine data from multiple API responses
 * @param {object} apiResponses - Responses from various financial APIs
 * @param {string} originalQuery - User's original query
 * @param {array} conversationHistory - Previous messages in the conversation
 * @returns {Promise<object>} - Formatted and combined response
 */
async function formatCombinedResponse(apiResponses, originalQuery, conversationHistory = []) {
  try {
    // Create a context message with all API responses
    let apiResponsesContext = 'Here are the responses from various financial APIs:\n\n';
    
    for (const [apiName, response] of Object.entries(apiResponses)) {
      apiResponsesContext += `${apiName} API Response:\n${JSON.stringify(response, null, 2)}\n\n`;
    }

    // Build messages array with conversation history for context
    const messages = [
      {
        role: 'system',
        content: `You are a financial data analyst. Your job is to take data from multiple financial APIs and combine it into a coherent, conversational response for the user. 
        Focus on answering the user's original query with the most relevant information.
        
        Important guidelines:
        1. Be conversational and engaging, as if you're having a dialogue with the user
        2. Highlight the most important data points first
        3. Include relevant numbers and metrics when discussing financial information
        4. End with a subtle prompt for follow-up questions when appropriate
        5. If the data is incomplete or unavailable, acknowledge this honestly
        6. Format currency values appropriately (e.g., $1.2M, $45.3B)
        7. Use bullet points or sections for complex information
        8. Avoid overly technical jargon unless the user seems knowledgeable`
      }
    ];
    
    // Add relevant conversation history for context
    if (conversationHistory && conversationHistory.length > 0) {
      // Only include the last 3 messages to stay focused
      const recentHistory = conversationHistory.slice(-3);
      messages.push(...recentHistory);
    }
    
    // Add the current query and API responses
    messages.push({
      role: 'user',
      content: `Original user query: "${originalQuery}"\n\n${apiResponsesContext}\n\nPlease provide a comprehensive, conversational response to the user's query based on this data.`
    });

    const response = await openai.chat.completions.create({
      model: apiConfig.openai.model,
      messages: messages,
      max_tokens: 1500,
      temperature: 0.7
    });

    return {
      content: response.choices[0].message.content,
      usage: response.usage,
      message: response.choices[0].message
    };
  } catch (error) {
    console.error('Response Formatting Error:', error);
    throw new Error(`Failed to format combined response: ${error.message}`);
  }
}

/**
 * Generate follow-up question suggestions based on the conversation
 * @param {array} conversationHistory - Previous messages in the conversation
 * @returns {Promise<array>} - Array of suggested follow-up questions
 */
async function generateFollowUpSuggestions(conversationHistory) {
  try {
    if (!conversationHistory || conversationHistory.length < 2) {
      return [
        "What stocks are trending today?",
        "Tell me about recent market news",
        "How is the S&P 500 performing?"
      ];
    }

    const messages = [
      {
        role: 'system',
        content: `You are a financial conversation assistant. Based on the conversation history, suggest 3-4 relevant follow-up questions the user might want to ask.
        Make the suggestions diverse but relevant to the ongoing conversation.
        Return your response as a JSON array of strings, each representing a suggested question.`
      }
    ];
    
    // Add the conversation history
    messages.push(...conversationHistory.slice(-6));
    
    const response = await openai.chat.completions.create({
      model: apiConfig.openai.model,
      messages: messages,
      response_format: { type: "json_object" },
      max_tokens: 500,
      temperature: 0.7
    });

    // Parse the JSON response
    const suggestions = JSON.parse(response.choices[0].message.content);
    return suggestions.questions || [];
  } catch (error) {
    console.error('Follow-up Suggestions Error:', error);
    // Return default suggestions if there's an error
    return [
      "What are the top performing stocks this week?",
      "Tell me about recent market news",
      "How are tech stocks performing?"
    ];
  }
}

module.exports = {
  processQuery,
  analyzeQueryForApiCalls,
  formatCombinedResponse,
  generateFollowUpSuggestions
}; 