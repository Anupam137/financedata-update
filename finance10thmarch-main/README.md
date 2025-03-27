# AI Financial Search Engine

A powerful financial search engine that integrates multiple APIs with OpenAI and DeepSeek AI to provide seamless, comprehensive, and highly relevant financial insights.

## Features

- **LLM-First API Selection**: Intelligent API selection based on query analysis
- **Fast-Path for Simple Queries**: Bypasses LLM for common financial questions
- **API Response Caching**: Reduces costs and improves response times
- **Streaming Responses**: Real-time updates as data is gathered and processed
- **DeepSeek R1 Integration**: Professional-grade financial research reports
- **Multiple Financial Data Sources**:
  - **Perplexity Sonar**: Real-time news and market insights
  - **Perplexity Deep Research**: In-depth financial analysis
  - **Polygon.io**: Stock prices, charts, and technical data
  - **FinancialDatasets.ai**: Company filings, insider trades, and SEC filings

## Recent Improvements

- **DeepSeek R1 Integration**: Added support for DeepSeek's advanced reasoning model to generate comprehensive financial research reports
- **Increased Response Length**: Optimized token limits to ensure complete financial analyses without truncation
- **Enhanced Error Handling**: Improved API error handling and fallback mechanisms
- **Structured Financial Reports**: Professional-grade financial analyses with executive summaries, detailed metrics, and strategic recommendations
- **DeepSeek V3 Enhanced Deep Research Mode**: Implemented a comprehensive, actionable financial analysis structure for the Deep Research mode with the following features:
  - **Market Sentiment Analysis**: Detailed breakdown of investor sentiment, analyst ratings, and news sentiment
  - **Technical Analysis & Trading Indicators**: Support/resistance levels and entry/exit points for traders
  - **Investment Strategies & Recommendations**: Tailored strategies for different risk profiles (conservative, moderate, aggressive)
  - **Competitive Analysis**: Comparison of key metrics to major competitors and industry averages
  - **Business Outlook & Forecasting**: Revenue/earnings projections with best-case, worst-case, and most likely scenarios
  - **Actionable Insights**: Clear buy/sell signals with rationale and risk assessment

## Tech Stack

### Frontend
- **Next.js**: React framework with TypeScript
- **Tailwind CSS**: Utility-first CSS framework
- **Streaming API Consumption**: Real-time data processing
- **ReactMarkdown**: Rendering of structured financial reports

### Backend
- **FastAPI**: Modern, high-performance Python web framework
- **OpenAI API**: For LLM-based query analysis and API selection
- **DeepSeek R1**: For comprehensive financial analysis and report generation
- **Redis**: For caching API plans and responses
- **Async Processing**: Parallel API calls for faster responses

## Architecture

The system uses a hybrid approach combining OpenAI for query analysis and DeepSeek for deep financial research:

1. **Query Analysis**:
   - Simple queries bypass the LLM using pattern matching
   - Complex queries are analyzed by OpenAI to determine which APIs to call

2. **API Selection**:
   - OpenAI decides which APIs are needed based on the query
   - Only necessary APIs are called to minimize costs

3. **Parallel Execution**:
   - API calls are executed in parallel using asyncio
   - Results are collected and formatted for processing

4. **Deep Analysis**:
   - DeepSeek R1 generates comprehensive financial reports based on collected data
   - Results include detailed analysis, metrics, and strategic recommendations

5. **Response Delivery**:
   - Structured reports are delivered to the user with proper formatting
   - Results can be streamed in real-time for better user experience

## Getting Started

### Prerequisites
- Python 3.8+
- Node.js 14+
- Redis (optional, for caching)
- API keys for:
  - OpenAI
  - Together AI (for DeepSeek R1)
  - Polygon.io
  - Perplexity
  - FinancialDatasets.ai

### Installation

1. **Clone the repository**:
```bash
git clone <repository-url>
cd financial-search-engine
```

2. **Set up the backend**:
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

3. **Configure environment variables**:
```bash
cp .env.example .env
# Edit .env with your API keys
```

4. **Set up the frontend**:
```bash
cd ../frontend
npm install
```

### Running the Application

1. **Start Redis** (optional, for caching):
```bash
redis-server
```

2. **Start the backend**:
```bash
cd backend
source venv/bin/activate  # On Windows: venv\Scripts\activate
python -m uvicorn app.main:app --reload
```

3. **Start the frontend**:
```bash
cd frontend
npm run dev
```

4. **Open your browser** and navigate to `http://localhost:3000`

## Usage Examples

### Simple Queries (Fast-Path)
- "What is the current price of AAPL?"
- "Show me the latest news for TSLA"
- "What are the recent insider trades for NVDA?"

### Complex Queries (OpenAI Analysis + DeepSeek Research)
- "Analyze Apple's stock performance over the past year and provide future outlook"
- "Compare Tesla and Ford in terms of financial performance and stock growth"
- "Evaluate the semiconductor industry and identify the most promising investment opportunities"
- "Analyze the impact of recent Fed decisions on tech stocks"

## Future Roadmap

### Planned Features
- **Streaming Reasoning Process**: Real-time display of DeepSeek's reasoning process for transparency
- **Enhanced Visualization**: Interactive charts and graphs for financial data
- **Custom Report Formats**: Options for narrative-style or structured reports based on user preference
- **Multi-Modal Analysis**: Integration of image and chart analysis for financial reports
- **Portfolio Analysis**: Comprehensive analysis of user portfolios with optimization recommendations
- **Voice Interface**: Natural language voice input for queries
- **Mobile App**: Native mobile experience for on-the-go financial research

### Technical Enhancements
- **Improved Caching**: More sophisticated caching strategies for faster responses
- **Advanced Rate Limiting**: Smart handling of API rate limits across multiple providers
- **User Preferences**: Personalized settings for report format, detail level, and data sources
- **Export Options**: PDF, Excel, and other export formats for financial reports
- **API Integration**: Additional financial data sources for more comprehensive analysis

## Configuration Options

The system can be configured through environment variables:

- `ENABLE_FAST_PATH`: Enable/disable fast-path for simple queries (default: true)
- `ENABLE_CACHING`: Enable/disable Redis caching (default: true)
- `ENABLE_STREAMING`: Enable/disable streaming responses (default: true)
- `TOGETHER_API_KEY`: API key for Together AI (DeepSeek R1)

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- OpenAI for their powerful language models
- Together AI for hosting DeepSeek R1
- Perplexity for their AI-powered search technology
- Polygon.io for their comprehensive financial data API
- FinancialDatasets.ai for their financial statements and insider trading data 