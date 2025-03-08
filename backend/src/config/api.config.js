/**
 * API Configuration for all external services
 */
const dotenv = require('dotenv');
dotenv.config();

module.exports = {
  openai: {
    apiKey: process.env.OPENAI_API_KEY,
    model: 'gpt-4-turbo', // or whichever model you prefer
    maxTokens: 2000
  },
  polygon: {
    apiKey: process.env.POLYGON_API_KEY,
    baseUrl: 'https://api.polygon.io'
  },
  financialDatasets: {
    baseUrl: 'https://api.financialdatasets.ai',
    endpoints: {
      incomeStatements: '/financials/income-statements',
      balanceSheets: '/financials/balance-sheets',
      cashFlowStatements: '/financials/cash-flow-statements',
      institutionalOwnership: '/ownership/institutional',
      insiderTrades: '/insider-trades',
      segmentedFinancials: '/financials/segmented-revenues',
      metrics: '/financial-metrics',
      companyFacts: '/company/facts',
      prices: '/prices',
      cryptoPrices: '/crypto/prices',
      news: '/company/news',
      pressReleases: '/earnings/press-releases',
      earnings: '/earnings',
      earningsCalendar: '/earnings/calendar',
      secFilings: '/sec/filings',
      availableTickers: {
        financials: '/financials/income-statements/tickers',
        crypto: '/crypto/prices/tickers',
        prices: '/prices/tickers',
        metrics: '/financial-metrics/tickers'
      }
    }
  },
  perplexity: {
    apiKey: process.env.PERPLEXITY_API_KEY,
    baseUrl: 'https://api.perplexity.ai',
    // Updated endpoints based on Perplexity API documentation
    sonarEndpoint: '/chat/completions',
    deepResearchEndpoint: '/chat/completions',
    models: {
      // Using models from https://docs.perplexity.ai/guides/model-cards
      sonar: 'sonar',  // Standard model for quick searches
      deepResearch: 'sonar-deep-research'  // Deep research model for comprehensive analysis
    }
  }
}; 