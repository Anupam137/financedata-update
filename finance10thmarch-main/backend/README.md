# Financial Search Engine Backend

This is the backend component of the AI Financial Search Engine, built with FastAPI and integrating multiple AI models and financial data sources.

## Architecture

The backend follows a modular service-oriented architecture:

### Core Components

- **FastAPI Application**: High-performance asynchronous web framework
- **Service Layer**: Modular services for each API and AI model
- **API Routes**: RESTful endpoints for frontend communication
- **Caching Layer**: Redis-based caching for API responses and query plans

### AI Models Integration

- **OpenAI**: Used for query analysis and API selection
- **DeepSeek R1**: Used for comprehensive financial analysis and report generation

### Data Sources

- **Perplexity Sonar**: Real-time news and market insights
- **Perplexity Deep Research**: In-depth financial analysis
- **Polygon.io**: Stock prices, charts, and technical data
- **FinancialDatasets.ai**: Company filings, insider trades, and SEC filings

## Services

### OpenAI Service

The OpenAI service is responsible for:
- Analyzing user queries to determine which APIs to call
- Generating API plans with specific data requirements
- Maintaining conversation history for context

### DeepSeek Service

The DeepSeek service is responsible for:
- Generating comprehensive financial research reports
- Processing data from multiple sources
- Providing structured analysis with executive summaries and recommendations

### Perplexity Service

The Perplexity service provides:
- Real-time market insights through Sonar
- Deep research capabilities for complex financial questions

### Polygon Service

The Polygon service provides:
- Real-time and historical stock price data
- Company news and announcements
- Technical indicators and market data

### Financial Datasets Service

The Financial Datasets service provides:
- Company financial statements
- Insider trading information
- SEC filings and regulatory data

### Redis Service

The Redis service handles:
- Caching of API responses to reduce costs
- Caching of query plans for similar queries
- Session management for conversation history

## API Endpoints

### `/api/search`

- **Method**: POST
- **Description**: Main endpoint for financial search queries
- **Request Body**:
  - `query`: User's financial query
  - `mode`: Search mode (sonar, deep_research, or deepseek)
  - `session_id`: Optional session identifier for conversation history
- **Response**: JSON with answer, sources, and session ID

### `/api/search/stream`

- **Method**: POST
- **Description**: Streaming version of the search endpoint
- **Request Body**: Same as `/api/search`
- **Response**: Server-sent events with status updates and final result

## Configuration

The backend is configured through environment variables in a `.env` file:

```
# OpenAI Configuration
OPENAI_API_KEY=your_openai_api_key

# Together AI Configuration (for DeepSeek)
TOGETHER_API_KEY=your_together_api_key

# Perplexity Configuration
PERPLEXITY_API_KEY=your_perplexity_api_key

# Polygon Configuration
POLYGON_API_KEY=your_polygon_api_key

# Financial Datasets Configuration
FINANCIAL_DATASETS_API_KEY=your_financial_datasets_api_key

# Redis Configuration
REDIS_URL=redis://localhost:6379/0

# Feature Flags
ENABLE_FAST_PATH=true
ENABLE_CACHING=true
ENABLE_STREAMING=true
```

## DeepSeek R1 Integration

The DeepSeek R1 integration is a key feature of the backend, providing professional-grade financial analysis:

### Implementation Details

- Uses the Together AI API to access DeepSeek R1
- Configurable token limit (currently set to 8000 tokens)
- Structured prompt engineering for consistent report format
- Two-phase response with reasoning process and final output

### Response Format

DeepSeek R1 responses include:
1. **Reasoning Process**: Enclosed in `<think>` tags, showing the model's analysis
2. **Structured Report**: Professional financial report with:
   - Executive Summary
   - Past Performance Analysis
   - Future Outlook
   - Risk Assessment
   - Strategic Recommendations
   - Conclusion

## DeepSeek V3 Integration for Deep Research Mode

The DeepSeek V3 integration enhances the Deep Research mode with a more actionable and comprehensive financial analysis structure:

### Implementation Details

- Uses the Together AI API to access DeepSeek V3
- Optimized for narrative-style financial analysis
- Enhanced system prompt for structured, actionable insights
- Designed specifically for the Deep Research mode

### Enhanced System Prompt Structure

The DeepSeek V3 system prompt has been structured to generate highly actionable financial analyses with the following sections:

1. **Header Section (Overview)**
   - Comprehensive title with stock ticker & company name
   - Current date and market status indicator
   - Risk indicator score (Low/Medium/High Risk)

2. **Market Sentiment Analysis**
   - Investor sentiment from institutional and retail investors
   - Analyst ratings with Buy/Hold/Sell breakdown
   - News sentiment with positive/negative percentages
   - Technical indicators with clear interpretations

3. **Financial Metrics & Competitive Analysis**
   - Detailed metrics with exact values from source data
   - Comparison to major competitors and industry averages
   - Valuation assessment (overvalued, fairly valued, or undervalued)

4. **Technical Analysis & Trading Indicators**
   - Support and resistance levels for key price points
   - Historical returns and risk-adjusted performance metrics
   - Entry/exit points based on technical indicators

5. **Business Outlook & Forecasting**
   - Key growth drivers and challenges
   - Regulatory and macroeconomic factors
   - Revenue and earnings projections with scenario analysis

6. **Investment Strategies & Recommendations**
   - Tailored strategies for different risk profiles
   - Analyst price targets and expected performance
   - Clear buy/sell signals with rationale

7. **Conclusion & Key Takeaways**
   - Summary of key findings
   - Actionable insights for investors
   - Important metrics and trends to monitor

8. **Sources**
   - List of all sources used in the analysis

### Usage in Search Flow

The DeepSeek V3 model is specifically used for the "Deep Research" mode in the search flow:

```python
if mode == "deep_research":
    # Use DeepSeek V3 for Deep Research mode
    final_response = await deepseek_v3_service.generate_narrative_insight(query, api_results, session_id)
```

## Development

### Running the Backend

```bash
# Activate virtual environment
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Run the server with auto-reload
python -m uvicorn app.main:app --reload
```

### Testing

```bash
# Run all tests
pytest

# Run specific test file
pytest tests/test_openai_service.py

# Test DeepSeek integration
python test_deepseek.py
```

### Adding New Features

1. **New Service**:
   - Create a new service file in `app/services/`
   - Implement the service class with required methods
   - Register the service in `app/main.py`

2. **New API Endpoint**:
   - Add the endpoint to `app/api/routes/`
   - Register the route in `app/api/api.py`

3. **New Data Source**:
   - Implement a new service for the data source
   - Update the OpenAI prompt to include the new data source
   - Add the data source to the API plan schema

## Future Enhancements

- **Streaming Reasoning Process**: Real-time display of DeepSeek's reasoning
- **Advanced Caching Strategies**: More sophisticated caching for faster responses
- **Custom Report Formats**: Options for different report styles
- **Additional Data Sources**: Integration with more financial APIs
- **Enhanced Error Handling**: More robust fallback mechanisms

## Troubleshooting

### Common Issues

- **401 Unauthorized**: Check your API keys in the `.env` file
- **Rate Limit Exceeded**: Implement backoff strategy or upgrade API plan
- **Timeout Errors**: Increase timeout settings for long-running queries
- **Memory Issues**: Monitor and optimize memory usage for large responses 

Initial Query Flow:
User input → OpenAI LLM → API calls → API data sent to DeepSeek R1 → Output to user
Follow-up Question Flow:
User input (follow-up) → OpenAI LLM → (calls necessary APIs if needed) → API data + conversation history → DeepSeek R1 → Output to user