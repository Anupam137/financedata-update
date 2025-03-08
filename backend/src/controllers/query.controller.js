const openaiService = require('../services/openai.service');
const polygonService = require('../services/polygon.service');
const financialDatasetsService = require('../services/financial-datasets.service');
const perplexityService = require('../services/perplexity.service');
const conversationService = require('../services/conversation.service');
const { v4: uuidv4 } = require('uuid');

/**
 * Process a user's financial query
 * @param {object} req - Express request object
 * @param {object} res - Express response object
 * @param {function} next - Express next middleware function
 */
async function processQuery(req, res, next) {
  try {
    const { query, mode = 'sonar', sessionId = uuidv4() } = req.body;
    
    if (!query) {
      return res.status(400).json({ error: 'Query is required' });
    }
    
    // Get conversation history
    const conversationHistory = conversationService.getConversationHistory(sessionId);
    
    // Add user message to conversation history
    conversationService.addMessage(sessionId, 'user', query);
    
    // Step 1: Analyze the query to determine which APIs to call
    const apiCallDecision = await openaiService.analyzeQueryForApiCalls(query, conversationHistory);
    
    // Step 2: Call the appropriate APIs based on the analysis
    const apiResponses = {};
    const apiCalls = [];
    
    // Extract entities from the API call decision
    const entities = apiCallDecision.entities || {};
    const tickers = entities.tickers || [];
    const topics = entities.topics || [];
    
    // Check if this is a comparison query
    if (apiCallDecision.isComparisonQuery && tickers.length >= 2) {
      // This is a comparison query with multiple tickers
      console.log(`Processing comparison query for tickers: ${tickers.join(', ')}`);
      
      // Extract metrics from the query or use defaults
      const metrics = entities.metrics || ['revenue', 'profit_margin', 'growth'];
      
      try {
        // Call Perplexity API to compare companies
        const comparisonResults = await perplexityService.compareCompanies(tickers, metrics);
        apiResponses.comparisonResults = comparisonResults;
      } catch (error) {
        console.error('Comparison Error:', error);
        apiResponses.comparisonError = error.message;
        
        // Fallback to individual API calls for each ticker
        for (const ticker of tickers) {
          if (apiCallDecision.polygon) {
            apiCalls.push(
              polygonService.getStockPrice(ticker)
                .then(data => { 
                  if (!apiResponses.stockPrices) apiResponses.stockPrices = {};
                  apiResponses.stockPrices[ticker] = data; 
                })
                .catch(error => { 
                  if (!apiResponses.stockPriceErrors) apiResponses.stockPriceErrors = {};
                  apiResponses.stockPriceErrors[ticker] = error.message; 
                })
            );
          }
          
          if (apiCallDecision.financialDatasets) {
            apiCalls.push(
              financialDatasetsService.getFinancialStatements(ticker)
                .then(data => { 
                  if (!apiResponses.financialStatements) apiResponses.financialStatements = {};
                  apiResponses.financialStatements[ticker] = data; 
                })
                .catch(error => { 
                  if (!apiResponses.financialStatementsErrors) apiResponses.financialStatementsErrors = {};
                  apiResponses.financialStatementsErrors[ticker] = error.message; 
                })
            );
          }
        }
      }
    } else {
      // Use the first ticker found, or null if none
      const ticker = tickers.length > 0 ? tickers[0] : null;
      
      // Determine if this is a news-focused query
      const isNewsQuery = apiCallDecision.isNewsQuery || 
                          query.toLowerCase().includes('news') || 
                          query.toLowerCase().includes('latest') ||
                          query.toLowerCase().includes('recent') ||
                          query.toLowerCase().includes('happening');
      
      // Call Polygon API if needed
      if (apiCallDecision.polygon && ticker) {
        apiCalls.push(
          polygonService.getStockPrice(ticker)
            .then(data => { apiResponses.stockPrice = data; })
            .catch(error => { apiResponses.stockPriceError = error.message; })
        );
        
        apiCalls.push(
          polygonService.getCompanyDetails(ticker)
            .then(data => { apiResponses.companyDetails = data; })
            .catch(error => { apiResponses.companyDetailsError = error.message; })
        );
        
        // Only get news from Polygon if we're not using Perplexity for news
        if (!isNewsQuery) {
          apiCalls.push(
            polygonService.getTickerNews(ticker)
              .then(data => { apiResponses.news = data; })
              .catch(error => { apiResponses.newsError = error.message; })
          );
        }
      }
      
      // Call Financial Datasets API if needed
      if (apiCallDecision.financialDatasets && ticker) {
        apiCalls.push(
          financialDatasetsService.getFinancialStatements(ticker)
            .then(data => { apiResponses.financialStatements = data; })
            .catch(error => { apiResponses.financialStatementsError = error.message; })
        );
        
        apiCalls.push(
          financialDatasetsService.getInstitutionalOwnership(ticker)
            .then(data => { apiResponses.institutionalOwnership = data; })
            .catch(error => { apiResponses.institutionalOwnershipError = error.message; })
        );
        
        // Add historical metrics if needed
        apiCalls.push(
          financialDatasetsService.getHistoricalMetrics(ticker)
            .then(data => { apiResponses.historicalMetrics = data; })
            .catch(error => { apiResponses.historicalMetricsError = error.message; })
        );
      }
      
      // Call Perplexity API based on mode and query type
      if (mode === 'sonar' && apiCallDecision.perplexitySonar) {
        // If it's a news query, use the specialized news and sentiment function
        if (isNewsQuery && (ticker || topics.length > 0)) {
          const newsTopic = ticker || topics[0] || 'financial markets';
          apiCalls.push(
            perplexityService.getMarketNewsAndSentiment(newsTopic)
              .then(data => { apiResponses.marketNewsAndSentiment = data; })
              .catch(error => { apiResponses.marketNewsError = error.message; })
          );
        } else {
          // For regular queries, use the standard Sonar search
          apiCalls.push(
            perplexityService.searchWithSonar(query, { emphasizeRecent: isNewsQuery })
              .then(data => { apiResponses.sonarResults = data; })
              .catch(error => { apiResponses.sonarError = error.message; })
          );
        }
      } else if (mode === 'deep-research' && apiCallDecision.perplexityDeepResearch) {
        apiCalls.push(
          perplexityService.conductDeepResearch(query)
            .then(data => { apiResponses.deepResearchResults = data; })
            .catch(error => { apiResponses.deepResearchError = error.message; })
        );
      }
    }
    
    // If no specific APIs were called or if it's a general question, use OpenAI directly
    if (Object.keys(apiCalls).length === 0 && Object.keys(apiResponses).length === 0) {
      const directResponse = await openaiService.processQuery(query, {}, conversationHistory);
      
      // Add assistant response to conversation history
      conversationService.addMessage(sessionId, 'assistant', directResponse.content);
      
      // Generate follow-up suggestions
      const followUpSuggestions = await openaiService.generateFollowUpSuggestions(
        conversationService.getConversationHistory(sessionId)
      );
      
      return res.json({
        query,
        mode,
        sessionId,
        response: directResponse.content,
        followUpSuggestions
      });
    }
    
    // Wait for all API calls to complete
    await Promise.all(apiCalls);
    
    // Step 3: Format the combined response using OpenAI
    const formattedResponse = await openaiService.formatCombinedResponse(
      apiResponses, 
      query, 
      conversationHistory
    );
    
    // Add assistant response to conversation history
    conversationService.addMessage(sessionId, 'assistant', formattedResponse.content);
    
    // Generate follow-up suggestions
    const followUpSuggestions = await openaiService.generateFollowUpSuggestions(
      conversationService.getConversationHistory(sessionId)
    );
    
    // Return the response
    res.json({
      query,
      mode,
      sessionId,
      response: formattedResponse.content,
      followUpSuggestions,
      apiResponses: process.env.NODE_ENV === 'development' ? apiResponses : undefined
    });
  } catch (error) {
    next(error);
  }
}

/**
 * Clear conversation history
 * @param {object} req - Express request object
 * @param {object} res - Express response object
 * @param {function} next - Express next middleware function
 */
async function clearConversation(req, res, next) {
  try {
    const { sessionId } = req.params;
    
    if (!sessionId) {
      return res.status(400).json({ error: 'Session ID is required' });
    }
    
    const success = conversationService.clearConversation(sessionId);
    
    if (success) {
      res.json({ message: 'Conversation cleared successfully', sessionId });
    } else {
      res.status(404).json({ error: 'Conversation not found', sessionId });
    }
  } catch (error) {
    next(error);
  }
}

/**
 * Get latest news and market sentiment about a topic
 * @param {object} req - Express request object
 * @param {object} res - Express response object
 * @param {function} next - Express next middleware function
 */
async function getMarketNews(req, res, next) {
  try {
    const { topic } = req.params;
    const { sessionId = uuidv4() } = req.query;
    
    if (!topic) {
      return res.status(400).json({ error: 'Topic is required' });
    }
    
    // Get conversation history
    const conversationHistory = conversationService.getConversationHistory(sessionId);
    
    // Add user message to conversation history
    const userMessage = `What are the latest news about ${topic}?`;
    conversationService.addMessage(sessionId, 'user', userMessage);
    
    // Get market news and sentiment from Perplexity
    const newsData = await perplexityService.getMarketNewsAndSentiment(topic);
    
    // Add assistant response to conversation history
    conversationService.addMessage(sessionId, 'assistant', newsData.content);
    
    // Generate follow-up suggestions
    const followUpSuggestions = await openaiService.generateFollowUpSuggestions(
      conversationService.getConversationHistory(sessionId)
    );
    
    // Return the response
    res.json({
      topic,
      sessionId,
      response: newsData.content,
      citations: newsData.citations,
      sentiment: newsData.sentiment,
      followUpSuggestions,
      timestamp: newsData.metadata.timestamp
    });
  } catch (error) {
    next(error);
  }
}

module.exports = {
  processQuery,
  clearConversation,
  getMarketNews
}; 