const axios = require('axios');
const apiConfig = require('../config/api.config');

// Initialize Financial Datasets API client
let financialDatasetsApi;
try {
  financialDatasetsApi = axios.create({
    baseURL: apiConfig.financialDatasets.baseUrl,
    headers: {
      'X-API-KEY': process.env.FINANCIAL_DATASETS_API_KEY
    }
  });
  console.log('Financial Datasets API client initialized successfully');
} catch (error) {
  console.error('Error initializing Financial Datasets API client:', error);
  console.warn('Using fallback implementation for Financial Datasets. Real API data will not be available.');
  
  // Fallback implementation only if initialization fails
  financialDatasetsApi = {
    get: async () => {
      throw new Error('Financial Datasets API is not properly configured. Please check your API key.');
    }
  };
}

/**
 * Get financial statements for a company
 * @param {string} ticker - Stock ticker symbol
 * @param {string} statementType - Type of financial statement (income, balance, cash)
 * @param {number} years - Number of years of data to retrieve
 * @returns {Promise<object>} - Financial statement data
 */
async function getFinancialStatements(ticker, statementType = 'income', years = 5) {
  try {
    // Map statement type to the appropriate endpoint
    let endpoint;
    if (statementType === 'income') {
      endpoint = apiConfig.financialDatasets.endpoints.incomeStatements;
    } else if (statementType === 'balance') {
      endpoint = apiConfig.financialDatasets.endpoints.balanceSheets;
    } else if (statementType === 'cash') {
      endpoint = apiConfig.financialDatasets.endpoints.cashFlowStatements;
    }
    
    // Map period to API expected values
    const period = 'annual'; // possible values are 'annual', 'quarterly', or 'ttm'
    
    const response = await financialDatasetsApi.get(endpoint, {
      params: {
        ticker,
        period,
        limit: years
      }
    });
    
    // Parse statements from the response based on the statement type
    let statements;
    if (statementType === 'income') {
      statements = response.data.income_statements || [];
    } else if (statementType === 'balance') {
      statements = response.data.balance_sheets || [];
    } else if (statementType === 'cash') {
      statements = response.data.cash_flow_statements || [];
    } else {
      statements = response.data || [];
    }
    
    return {
      ticker,
      statement_type: statementType,
      years,
      statements
    };
  } catch (error) {
    // Check if it's a 401 error (unauthorized)
    if (error.response && error.response.status === 401) {
      console.error(`Financial Datasets API authorization failed. Please check your API key.`);
      return {
        error: true,
        message: "Financial statements endpoint authorization failed",
        status: 401,
        mockData: true,
        data: {
          ticker,
          statement_type: statementType,
          years,
          statements: [
            {
              year: new Date().getFullYear() - 1,
              revenue: "N/A (Mock Data - Auth Failed)",
              net_income: "N/A (Mock Data - Auth Failed)",
              total_assets: "N/A (Mock Data - Auth Failed)",
              total_liabilities: "N/A (Mock Data - Auth Failed)"
            }
          ]
        }
      };
    }
    
    // Check if it's a 404 error (endpoint not found)
    if (error.response && error.response.status === 404) {
      console.error(`Financial Datasets API endpoint '${endpoint}' not found. This might be a configuration issue.`);
      // Return a structured error response that can be handled by the controller
      return {
        error: true,
        message: "Financial statements endpoint not available",
        status: 404,
        mockData: true,
        data: {
          ticker,
          statement_type: statementType,
          years,
          statements: [
            {
              year: new Date().getFullYear() - 1,
              revenue: "N/A (Mock Data)",
              net_income: "N/A (Mock Data)",
              total_assets: "N/A (Mock Data)",
              total_liabilities: "N/A (Mock Data)"
            }
          ]
        }
      };
    }
    
    console.error('Financial Datasets API Error (Statements):', error.response?.data || error.message);
    throw new Error(`Failed to get financial statements for ${ticker}: ${error.message}`);
  }
}

/**
 * Get institutional ownership data for a company
 * @param {string} ticker - Stock ticker symbol
 * @returns {Promise<object>} - Institutional ownership data
 */
async function getInstitutionalOwnership(ticker) {
  try {
    const response = await financialDatasetsApi.get(apiConfig.financialDatasets.endpoints.institutionalOwnership, {
      params: {
        ticker
      }
    });
    
    return {
      ticker,
      institutions: response.data.institutional_ownership || response.data
    };
  } catch (error) {
    // Check if it's a 401 error (unauthorized)
    if (error.response && error.response.status === 401) {
      console.error(`Financial Datasets API authorization failed. Please check your API key.`);
      return {
        error: true,
        message: "Institutional ownership endpoint authorization failed",
        status: 401,
        mockData: true,
        data: {
          ticker,
          institutions: [
            {
              name: "Example Institution (Mock Data - Auth Failed)",
              shares: "N/A",
              value: "N/A",
              percentage: "N/A"
            }
          ]
        }
      };
    }
    
    // Check if it's a 404 error (endpoint not found)
    if (error.response && error.response.status === 404) {
      console.error(`Financial Datasets API endpoint '${apiConfig.financialDatasets.endpoints.institutionalOwnership}' not found. This might be a configuration issue.`);
      // Return a structured error response that can be handled by the controller
      return {
        error: true,
        message: "Institutional ownership endpoint not available",
        status: 404,
        mockData: true,
        data: {
          ticker,
          institutions: [
            {
              name: "Example Institution (Mock Data)",
              shares: "N/A",
              value: "N/A",
              percentage: "N/A"
            }
          ]
        }
      };
    }
    
    console.error('Financial Datasets API Error (Ownership):', error.response?.data || error.message);
    throw new Error(`Failed to get institutional ownership for ${ticker}: ${error.message}`);
  }
}

/**
 * Get segmented financial data for a company
 * @param {string} ticker - Stock ticker symbol
 * @param {string} segmentType - Type of segment (product, geographic, business)
 * @returns {Promise<object>} - Segmented financial data
 */
async function getSegmentedFinancials(ticker, segmentType = 'product') {
  try {
    const response = await financialDatasetsApi.get(apiConfig.financialDatasets.endpoints.segmentedFinancials, {
      params: {
        ticker,
        period: 'annual',
        limit: 1
      }
    });
    
    // Extract segments based on the segment type
    let segments = [];
    const segmentedRevenues = response.data.segmented_revenues || [];
    
    if (segmentedRevenues.length > 0 && segmentedRevenues[0].items) {
      // Filter items based on segment type
      const items = segmentedRevenues[0].items.filter(item => {
        if (!item.segments || item.segments.length === 0) return false;
        
        if (segmentType === 'product') {
          return item.segments.some(segment => segment.type === 'Product or Service');
        } else if (segmentType === 'geographic') {
          return item.segments.some(segment => 
            segment.type.includes('Geographic') || 
            segment.label.includes('America') || 
            segment.label.includes('Europe') || 
            segment.label.includes('Asia') ||
            segment.label.includes('China')
          );
        } else if (segmentType === 'business') {
          return item.segments.some(segment => 
            segment.type.includes('Business') || 
            segment.type.includes('Segment')
          );
        }
        
        return false;
      });
      
      // Transform items to segments
      segments = items.map(item => ({
        name: item.segments[0].label,
        revenue: item.amount,
        growth: 'N/A', // Growth data not directly available
        type: item.segments[0].type
      }));
    }
    
    return {
      ticker,
      segment_type: segmentType,
      segments
    };
  } catch (error) {
    // Check if it's a 401 error (unauthorized)
    if (error.response && error.response.status === 401) {
      console.error(`Financial Datasets API authorization failed. Please check your API key.`);
      return {
        error: true,
        message: "Segmented financials endpoint authorization failed",
        status: 401,
        mockData: true,
        data: {
          ticker,
          segment_type: segmentType,
          segments: [
            {
              name: "Segment 1 (Mock Data - Auth Failed)",
              revenue: "N/A",
              growth: "N/A"
            },
            {
              name: "Segment 2 (Mock Data - Auth Failed)",
              revenue: "N/A",
              growth: "N/A"
            }
          ]
        }
      };
    }
    
    // Check if it's a 404 error (endpoint not found)
    if (error.response && error.response.status === 404) {
      console.error(`Financial Datasets API endpoint '${apiConfig.financialDatasets.endpoints.segmentedFinancials}' not found. This might be a configuration issue.`);
      return {
        error: true,
        message: "Segmented financials not available",
        status: 404,
        mockData: true,
        data: {
          ticker,
          segment_type: segmentType,
          segments: [
            {
              name: "Segment 1 (Mock Data)",
              revenue: "N/A",
              growth: "N/A"
            },
            {
              name: "Segment 2 (Mock Data)",
              revenue: "N/A",
              growth: "N/A"
            }
          ]
        }
      };
    }
    
    console.error('Financial Datasets API Error (Segments):', error.response?.data || error.message);
    return {
      error: true,
      message: "Segmented financials not available",
      status: error.response?.status || 500,
      mockData: true,
      data: {
        ticker,
        segment_type: segmentType,
        segments: [
          {
            name: "Segment 1 (Mock Data)",
            revenue: "N/A",
            growth: "N/A"
          },
          {
            name: "Segment 2 (Mock Data)",
            revenue: "N/A",
            growth: "N/A"
          }
        ]
      }
    };
  }
}

/**
 * Get historical financial metrics for a company
 * @param {string} ticker - Stock ticker symbol
 * @param {Array<string>} metrics - List of metrics to retrieve
 * @param {number} years - Number of years of data to retrieve
 * @returns {Promise<object>} - Historical financial metrics
 */
async function getHistoricalMetrics(ticker, metrics = ['revenue', 'net_income', 'eps'], years = 5) {
  try {
    const response = await financialDatasetsApi.get(apiConfig.financialDatasets.endpoints.metrics, {
      params: {
        ticker,
        period: 'annual',
        limit: years
      }
    });
    
    // Transform the financial metrics into the expected format
    const financialMetrics = response.data.financial_metrics || [];
    const historicalData = {};
    
    // Map API metrics to our internal metrics
    const metricMapping = {
      'revenue': 'revenue',
      'net_income': 'net_income',
      'eps': 'earnings_per_share',
      'profit_margin': 'net_margin',
      'growth': 'revenue_growth'
    };
    
    // Initialize the historical data structure
    metrics.forEach(metric => {
      historicalData[metric] = [];
    });
    
    // Populate the historical data from the API response
    financialMetrics.forEach(yearData => {
      metrics.forEach(metric => {
        const apiMetric = metricMapping[metric.toLowerCase()] || metric;
        if (yearData[apiMetric] !== undefined) {
          const year = new Date(yearData.report_period).getFullYear();
          historicalData[metric].push({
            year,
            value: yearData[apiMetric]
          });
        }
      });
    });
    
    return {
      ticker,
      metrics,
      years,
      historical_data: historicalData
    };
  } catch (error) {
    // Check if it's a 401 error (unauthorized)
    if (error.response && error.response.status === 401) {
      console.error(`Financial Datasets API authorization failed. Please check your API key.`);
      return {
        error: true,
        message: "Historical metrics endpoint authorization failed",
        status: 401,
        mockData: true,
        data: {
          ticker,
          metrics,
          years,
          historical_data: metrics.reduce((acc, metric) => {
            acc[metric] = Array.from({ length: years }, (_, i) => ({
              year: new Date().getFullYear() - i - 1,
              value: "N/A (Mock Data - Auth Failed)"
            }));
            return acc;
          }, {})
        }
      };
    }
    
    // Check if it's a 404 error (endpoint not found)
    if (error.response && error.response.status === 404) {
      console.error(`Financial Datasets API endpoint '${apiConfig.financialDatasets.endpoints.metrics}' not found. This might be a configuration issue.`);
      return {
        error: true,
        message: "Historical metrics not available",
        status: 404,
        mockData: true,
        data: {
          ticker,
          metrics,
          years,
          historical_data: metrics.reduce((acc, metric) => {
            acc[metric] = Array.from({ length: years }, (_, i) => ({
              year: new Date().getFullYear() - i - 1,
              value: "N/A (Mock Data)"
            }));
            return acc;
          }, {})
        }
      };
    }
    
    console.error('Financial Datasets API Error (Metrics):', error.response?.data || error.message);
    return {
      error: true,
      message: "Historical metrics not available",
      status: error.response?.status || 500,
      mockData: true,
      data: {
        ticker,
        metrics,
        years,
        historical_data: metrics.reduce((acc, metric) => {
          acc[metric] = Array.from({ length: years }, (_, i) => ({
            year: new Date().getFullYear() - i - 1,
            value: "N/A (Mock Data)"
          }));
          return acc;
        }, {})
      }
    };
  }
}

/**
 * Get company facts for a ticker
 * @param {string} ticker - Stock ticker symbol
 * @returns {Promise<object>} - Company facts data
 */
async function getCompanyFacts(ticker) {
  try {
    const response = await financialDatasetsApi.get(apiConfig.financialDatasets.endpoints.companyFacts, {
      params: {
        ticker
      }
    });
    
    return {
      ticker,
      company_facts: response.data.company_facts || {}
    };
  } catch (error) {
    // Check if it's a 401 error (unauthorized)
    if (error.response && error.response.status === 401) {
      console.error(`Financial Datasets API authorization failed. Please check your API key.`);
      return {
        error: true,
        message: "Company facts endpoint authorization failed",
        status: 401,
        mockData: true,
        data: {
          ticker,
          company_facts: {
            name: `${ticker} Inc. (Mock Data - Auth Failed)`,
            sector: "N/A",
            industry: "N/A",
            employees: "N/A",
            website: "N/A"
          }
        }
      };
    }
    
    // Check if it's a 404 error (endpoint not found)
    if (error.response && error.response.status === 404) {
      console.error(`Financial Datasets API endpoint '${apiConfig.financialDatasets.endpoints.companyFacts}' not found. This might be a configuration issue.`);
      return {
        error: true,
        message: "Company facts not available",
        status: 404,
        mockData: true,
        data: {
          ticker,
          company_facts: {
            name: `${ticker} Inc. (Mock Data)`,
            sector: "N/A",
            industry: "N/A",
            employees: "N/A",
            website: "N/A"
          }
        }
      };
    }
    
    console.error('Financial Datasets API Error (Company Facts):', error.response?.data || error.message);
    return {
      error: true,
      message: "Company facts not available",
      status: error.response?.status || 500,
      mockData: true,
      data: {
        ticker,
        company_facts: {
          name: `${ticker} Inc. (Mock Data)`,
          sector: "N/A",
          industry: "N/A",
          employees: "N/A",
          website: "N/A"
        }
      }
    };
  }
}

/**
 * Get cryptocurrency price data
 * @param {string} ticker - Cryptocurrency ticker symbol (e.g., 'BTC-USD')
 * @param {string} interval - Time interval for the price data (minute, day, week, month, year)
 * @param {number} intervalMultiplier - Multiplier for the interval
 * @param {string} startDate - Start date for the price data (YYYY-MM-DD)
 * @param {string} endDate - End date for the price data (YYYY-MM-DD)
 * @param {number} limit - Maximum number of price records to return
 * @returns {Promise<object>} - Cryptocurrency price data
 */
async function getCryptoPrices(ticker, interval = 'day', intervalMultiplier = 1, startDate, endDate, limit = 100) {
  try {
    // Set default dates if not provided
    if (!startDate) {
      const date = new Date();
      date.setMonth(date.getMonth() - 1);
      startDate = date.toISOString().split('T')[0]; // One month ago
    }
    
    if (!endDate) {
      const date = new Date();
      endDate = date.toISOString().split('T')[0]; // Today
    }
    
    const response = await financialDatasetsApi.get(apiConfig.financialDatasets.endpoints.cryptoPrices, {
      params: {
        ticker,
        interval,
        interval_multiplier: intervalMultiplier,
        start_date: startDate,
        end_date: endDate,
        limit
      }
    });
    
    return {
      ticker,
      interval,
      interval_multiplier: intervalMultiplier,
      start_date: startDate,
      end_date: endDate,
      prices: response.data.prices || []
    };
  } catch (error) {
    // Check if it's a 401 error (unauthorized)
    if (error.response && error.response.status === 401) {
      console.error(`Financial Datasets API authorization failed. Please check your API key.`);
      return {
        error: true,
        message: "Crypto prices endpoint authorization failed",
        status: 401,
        mockData: true,
        data: {
          ticker,
          interval,
          interval_multiplier: intervalMultiplier,
          start_date: startDate,
          end_date: endDate,
          prices: [
            {
              date: new Date().toISOString(),
              open: "N/A (Mock Data - Auth Failed)",
              high: "N/A (Mock Data - Auth Failed)",
              low: "N/A (Mock Data - Auth Failed)",
              close: "N/A (Mock Data - Auth Failed)",
              volume: "N/A (Mock Data - Auth Failed)"
            }
          ]
        }
      };
    }
    
    // Check if it's a 404 error (endpoint not found)
    if (error.response && error.response.status === 404) {
      console.error(`Financial Datasets API endpoint '${apiConfig.financialDatasets.endpoints.cryptoPrices}' not found. This might be a configuration issue.`);
      return {
        error: true,
        message: "Crypto prices endpoint not available",
        status: 404,
        mockData: true,
        data: {
          ticker,
          interval,
          interval_multiplier: intervalMultiplier,
          start_date: startDate,
          end_date: endDate,
          prices: [
            {
              date: new Date().toISOString(),
              open: "N/A (Mock Data)",
              high: "N/A (Mock Data)",
              low: "N/A (Mock Data)",
              close: "N/A (Mock Data)",
              volume: "N/A (Mock Data)"
            }
          ]
        }
      };
    }
    
    console.error('Financial Datasets API Error (Crypto Prices):', error.response?.data || error.message);
    return {
      error: true,
      message: "Crypto prices not available",
      status: error.response?.status || 500,
      mockData: true,
      data: {
        ticker,
        interval,
        interval_multiplier: intervalMultiplier,
        start_date: startDate,
        end_date: endDate,
        prices: [
          {
            date: new Date().toISOString(),
            open: "N/A (Mock Data)",
            high: "N/A (Mock Data)",
            low: "N/A (Mock Data)",
            close: "N/A (Mock Data)",
            volume: "N/A (Mock Data)"
          }
        ]
      }
    };
  }
}

/**
 * Get stock price data
 * @param {string} ticker - Stock ticker symbol
 * @param {string} interval - Time interval for the price data (second, minute, day, week, month, year)
 * @param {number} intervalMultiplier - Multiplier for the interval
 * @param {string} startDate - Start date for the price data (YYYY-MM-DD)
 * @param {string} endDate - End date for the price data (YYYY-MM-DD)
 * @param {number} limit - Maximum number of price records to return
 * @returns {Promise<object>} - Stock price data
 */
async function getStockPrices(ticker, interval = 'day', intervalMultiplier = 1, startDate, endDate, limit = 100) {
  try {
    // Set default dates if not provided
    if (!startDate) {
      const date = new Date();
      date.setMonth(date.getMonth() - 1);
      startDate = date.toISOString().split('T')[0]; // One month ago
    }
    
    if (!endDate) {
      const date = new Date();
      endDate = date.toISOString().split('T')[0]; // Today
    }
    
    const response = await financialDatasetsApi.get(apiConfig.financialDatasets.endpoints.prices, {
      params: {
        ticker,
        interval,
        interval_multiplier: intervalMultiplier,
        start_date: startDate,
        end_date: endDate,
        limit
      }
    });
    
    return {
      ticker,
      interval,
      interval_multiplier: intervalMultiplier,
      start_date: startDate,
      end_date: endDate,
      prices: response.data.prices || []
    };
  } catch (error) {
    // Check if it's a 401 error (unauthorized)
    if (error.response && error.response.status === 401) {
      console.error(`Financial Datasets API authorization failed. Please check your API key.`);
      return {
        error: true,
        message: "Stock prices endpoint authorization failed",
        status: 401,
        mockData: true,
        data: {
          ticker,
          interval,
          interval_multiplier: intervalMultiplier,
          start_date: startDate,
          end_date: endDate,
          prices: [
            {
              date: new Date().toISOString(),
              open: "N/A (Mock Data - Auth Failed)",
              high: "N/A (Mock Data - Auth Failed)",
              low: "N/A (Mock Data - Auth Failed)",
              close: "N/A (Mock Data - Auth Failed)",
              volume: "N/A (Mock Data - Auth Failed)"
            }
          ]
        }
      };
    }
    
    // Check if it's a 404 error (endpoint not found)
    if (error.response && error.response.status === 404) {
      console.error(`Financial Datasets API endpoint '${apiConfig.financialDatasets.endpoints.prices}' not found. This might be a configuration issue.`);
      return {
        error: true,
        message: "Stock prices endpoint not available",
        status: 404,
        mockData: true,
        data: {
          ticker,
          interval,
          interval_multiplier: intervalMultiplier,
          start_date: startDate,
          end_date: endDate,
          prices: [
            {
              date: new Date().toISOString(),
              open: "N/A (Mock Data)",
              high: "N/A (Mock Data)",
              low: "N/A (Mock Data)",
              close: "N/A (Mock Data)",
              volume: "N/A (Mock Data)"
            }
          ]
        }
      };
    }
    
    console.error('Financial Datasets API Error (Stock Prices):', error.response?.data || error.message);
    return {
      error: true,
      message: "Stock prices not available",
      status: error.response?.status || 500,
      mockData: true,
      data: {
        ticker,
        interval,
        interval_multiplier: intervalMultiplier,
        start_date: startDate,
        end_date: endDate,
        prices: [
          {
            date: new Date().toISOString(),
            open: "N/A (Mock Data)",
            high: "N/A (Mock Data)",
            low: "N/A (Mock Data)",
            close: "N/A (Mock Data)",
            volume: "N/A (Mock Data)"
          }
        ]
      }
    };
  }
}

/**
 * Get insider trades for a company
 * @param {string} ticker - Stock ticker symbol
 * @param {number} limit - Maximum number of trades to return
 * @param {string} filingDateStart - Start date for filing date filter (YYYY-MM-DD)
 * @param {string} filingDateEnd - End date for filing date filter (YYYY-MM-DD)
 * @returns {Promise<object>} - Insider trades data
 */
async function getInsiderTrades(ticker, limit = 100, filingDateStart, filingDateEnd) {
  try {
    const params = {
      ticker,
      limit
    };
    
    // Add filing date filters if provided
    if (filingDateStart) {
      params.filing_date_gte = filingDateStart;
    }
    
    if (filingDateEnd) {
      params.filing_date_lte = filingDateEnd;
    }
    
    const response = await financialDatasetsApi.get(apiConfig.financialDatasets.endpoints.insiderTrades, {
      params
    });
    
    return {
      ticker,
      insider_trades: response.data.insider_trades || []
    };
  } catch (error) {
    // Check if it's a 401 error (unauthorized)
    if (error.response && error.response.status === 401) {
      console.error(`Financial Datasets API authorization failed. Please check your API key.`);
      return {
        error: true,
        message: "Insider trades endpoint authorization failed",
        status: 401,
        mockData: true,
        data: {
          ticker,
          insider_trades: [
            {
              name: "Example Insider (Mock Data - Auth Failed)",
              title: "CEO",
              transaction_type: "Buy",
              shares: "N/A",
              price: "N/A",
              filing_date: new Date().toISOString().split('T')[0]
            }
          ]
        }
      };
    }
    
    // Check if it's a 404 error (endpoint not found)
    if (error.response && error.response.status === 404) {
      console.error(`Financial Datasets API endpoint '${apiConfig.financialDatasets.endpoints.insiderTrades}' not found. This might be a configuration issue.`);
      return {
        error: true,
        message: "Insider trades endpoint not available",
        status: 404,
        mockData: true,
        data: {
          ticker,
          insider_trades: [
            {
              name: "Example Insider (Mock Data)",
              title: "CEO",
              transaction_type: "Buy",
              shares: "N/A",
              price: "N/A",
              filing_date: new Date().toISOString().split('T')[0]
            }
          ]
        }
      };
    }
    
    console.error('Financial Datasets API Error (Insider Trades):', error.response?.data || error.message);
    return {
      error: true,
      message: "Insider trades not available",
      status: error.response?.status || 500,
      mockData: true,
      data: {
        ticker,
        insider_trades: [
          {
            name: "Example Insider (Mock Data)",
            title: "CEO",
            transaction_type: "Buy",
            shares: "N/A",
            price: "N/A",
            filing_date: new Date().toISOString().split('T')[0]
          }
        ]
      }
    };
  }
}

/**
 * Get SEC filings for a company
 * @param {string} ticker - Stock ticker symbol
 * @param {number} limit - Maximum number of filings to return
 * @returns {Promise<object>} - SEC filings data
 */
async function getSecFilings(ticker, limit = 100) {
  try {
    const response = await financialDatasetsApi.get(apiConfig.financialDatasets.endpoints.secFilings, {
      params: {
        ticker,
        limit
      }
    });
    
    return {
      ticker,
      sec_filings: response.data.sec_filings || []
    };
  } catch (error) {
    // Check if it's a 401 error (unauthorized)
    if (error.response && error.response.status === 401) {
      console.error(`Financial Datasets API authorization failed. Please check your API key.`);
      return {
        error: true,
        message: "SEC filings endpoint authorization failed",
        status: 401,
        mockData: true,
        data: {
          ticker,
          sec_filings: [
            {
              form_type: "10-K",
              filing_date: new Date().toISOString().split('T')[0],
              description: "Annual Report (Mock Data - Auth Failed)",
              url: "N/A"
            }
          ]
        }
      };
    }
    
    // Check if it's a 404 error (endpoint not found)
    if (error.response && error.response.status === 404) {
      console.error(`Financial Datasets API endpoint '${apiConfig.financialDatasets.endpoints.secFilings}' not found. This might be a configuration issue.`);
      return {
        error: true,
        message: "SEC filings endpoint not available",
        status: 404,
        mockData: true,
        data: {
          ticker,
          sec_filings: [
            {
              form_type: "10-K",
              filing_date: new Date().toISOString().split('T')[0],
              description: "Annual Report (Mock Data)",
              url: "N/A"
            }
          ]
        }
      };
    }
    
    console.error('Financial Datasets API Error (SEC Filings):', error.response?.data || error.message);
    return {
      error: true,
      message: "SEC filings not available",
      status: error.response?.status || 500,
      mockData: true,
      data: {
        ticker,
        sec_filings: [
          {
            form_type: "10-K",
            filing_date: new Date().toISOString().split('T')[0],
            description: "Annual Report (Mock Data)",
            url: "N/A"
          }
        ]
      }
    };
  }
}

/**
 * Get company news
 * @param {string} ticker - Stock ticker symbol
 * @param {number} limit - Maximum number of news articles to return
 * @returns {Promise<object>} - Company news data
 */
async function getCompanyNews(ticker, limit = 10) {
  try {
    const response = await financialDatasetsApi.get(apiConfig.financialDatasets.endpoints.news, {
      params: {
        ticker,
        limit
      }
    });
    
    return {
      ticker,
      news: response.data.news || []
    };
  } catch (error) {
    // Check if it's a 401 error (unauthorized)
    if (error.response && error.response.status === 401) {
      console.error(`Financial Datasets API authorization failed. Please check your API key.`);
      return {
        error: true,
        message: "Company news endpoint authorization failed",
        status: 401,
        mockData: true,
        data: {
          ticker,
          news: [
            {
              title: "Example News Article (Mock Data - Auth Failed)",
              date: new Date().toISOString(),
              source: "Mock News Source",
              url: "N/A",
              summary: "This is a mock news article due to authorization failure."
            }
          ]
        }
      };
    }
    
    // Check if it's a 404 error (endpoint not found)
    if (error.response && error.response.status === 404) {
      console.error(`Financial Datasets API endpoint '${apiConfig.financialDatasets.endpoints.news}' not found. This might be a configuration issue.`);
      return {
        error: true,
        message: "Company news endpoint not available",
        status: 404,
        mockData: true,
        data: {
          ticker,
          news: [
            {
              title: "Example News Article (Mock Data)",
              date: new Date().toISOString(),
              source: "Mock News Source",
              url: "N/A",
              summary: "This is a mock news article due to endpoint not being available."
            }
          ]
        }
      };
    }
    
    console.error('Financial Datasets API Error (Company News):', error.response?.data || error.message);
    return {
      error: true,
      message: "Company news not available",
      status: error.response?.status || 500,
      mockData: true,
      data: {
        ticker,
        news: [
          {
            title: "Example News Article (Mock Data)",
            date: new Date().toISOString(),
            source: "Mock News Source",
            url: "N/A",
            summary: "This is a mock news article due to an error."
          }
        ]
      }
    };
  }
}

/**
 * Get press releases
 * @param {string} ticker - Stock ticker symbol
 * @returns {Promise<object>} - Press releases data
 */
async function getPressReleases(ticker) {
  try {
    const response = await financialDatasetsApi.get(apiConfig.financialDatasets.endpoints.pressReleases, {
      params: {
        ticker
      }
    });
    
    return {
      ticker,
      press_releases: response.data.press_releases || []
    };
  } catch (error) {
    // Check if it's a 401 error (unauthorized)
    if (error.response && error.response.status === 401) {
      console.error(`Financial Datasets API authorization failed. Please check your API key.`);
      return {
        error: true,
        message: "Press releases endpoint authorization failed",
        status: 401,
        mockData: true,
        data: {
          ticker,
          press_releases: [
            {
              title: "Example Press Release (Mock Data - Auth Failed)",
              date: new Date().toISOString(),
              url: "N/A",
              content: "This is a mock press release due to authorization failure."
            }
          ]
        }
      };
    }
    
    // Check if it's a 404 error (endpoint not found)
    if (error.response && error.response.status === 404) {
      console.error(`Financial Datasets API endpoint '${apiConfig.financialDatasets.endpoints.pressReleases}' not found. This might be a configuration issue.`);
      return {
        error: true,
        message: "Press releases endpoint not available",
        status: 404,
        mockData: true,
        data: {
          ticker,
          press_releases: [
            {
              title: "Example Press Release (Mock Data)",
              date: new Date().toISOString(),
              url: "N/A",
              content: "This is a mock press release due to endpoint not being available."
            }
          ]
        }
      };
    }
    
    console.error('Financial Datasets API Error (Press Releases):', error.response?.data || error.message);
    return {
      error: true,
      message: "Press releases not available",
      status: error.response?.status || 500,
      mockData: true,
      data: {
        ticker,
        press_releases: [
          {
            title: "Example Press Release (Mock Data)",
            date: new Date().toISOString(),
            url: "N/A",
            content: "This is a mock press release due to an error."
          }
        ]
      }
    };
  }
}

/**
 * Get available tickers for a specific data type
 * @param {string} dataType - Type of data (financials, crypto, prices, metrics)
 * @returns {Promise<object>} - Available tickers
 */
async function getAvailableTickers(dataType = 'financials') {
  try {
    let endpoint;
    
    // Map data type to the appropriate endpoint
    if (dataType === 'financials') {
      endpoint = apiConfig.financialDatasets.endpoints.availableTickers.financials;
    } else if (dataType === 'crypto') {
      endpoint = apiConfig.financialDatasets.endpoints.availableTickers.crypto;
    } else if (dataType === 'prices') {
      endpoint = apiConfig.financialDatasets.endpoints.availableTickers.prices;
    } else if (dataType === 'metrics') {
      endpoint = apiConfig.financialDatasets.endpoints.availableTickers.metrics;
    } else {
      throw new Error(`Invalid data type: ${dataType}`);
    }
    
    const response = await financialDatasetsApi.get(endpoint);
    
    return {
      data_type: dataType,
      tickers: response.data.tickers || []
    };
  } catch (error) {
    // Check if it's a 401 error (unauthorized)
    if (error.response && error.response.status === 401) {
      console.error(`Financial Datasets API authorization failed. Please check your API key.`);
      return {
        error: true,
        message: "Available tickers endpoint authorization failed",
        status: 401,
        mockData: true,
        data: {
          data_type: dataType,
          tickers: ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]
        }
      };
    }
    
    // Check if it's a 404 error (endpoint not found)
    if (error.response && error.response.status === 404) {
      console.error(`Financial Datasets API endpoint for available tickers (${dataType}) not found. This might be a configuration issue.`);
      return {
        error: true,
        message: "Available tickers endpoint not available",
        status: 404,
        mockData: true,
        data: {
          data_type: dataType,
          tickers: ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]
        }
      };
    }
    
    console.error('Financial Datasets API Error (Available Tickers):', error.response?.data || error.message);
    return {
      error: true,
      message: "Available tickers not available",
      status: error.response?.status || 500,
      mockData: true,
      data: {
        data_type: dataType,
        tickers: ["AAPL", "MSFT", "GOOGL", "AMZN", "META"]
      }
    };
  }
}

module.exports = {
  getFinancialStatements,
  getInstitutionalOwnership,
  getSegmentedFinancials,
  getHistoricalMetrics,
  getCompanyFacts,
  getCryptoPrices,
  getStockPrices,
  getInsiderTrades,
  getSecFilings,
  getCompanyNews,
  getPressReleases,
  getAvailableTickers
}; 