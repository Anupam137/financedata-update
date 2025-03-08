# FinSearch - AI-Powered Financial Search Engine

FinSearch is an advanced financial search engine that integrates multiple financial data APIs with OpenAI's language models to provide seamless and highly relevant responses to financial queries.

## Features

- **AI-Powered Search**: Utilizes OpenAI's language models to understand and process financial queries
- **Multiple Data Sources**: Integrates with Polygon.io, Financial Datasets, and Perplexity for comprehensive financial data
- **Real-Time Data**: Access to real-time stock prices, financial statements, and market news
- **Company Comparisons**: Compare multiple companies across various financial metrics
- **Dual Search Modes**: Choose between quick search (Sonar) and deep research for different levels of analysis

## Tech Stack

### Backend
- Node.js
- Express
- OpenAI API
- Polygon.io API
- Financial Datasets API
- Perplexity API

### Frontend
- React
- React Router
- Axios
- Chart.js

## Getting Started

### Prerequisites
- Node.js (v14 or higher)
- npm or yarn
- API keys for OpenAI, Polygon.io, Financial Datasets, and Perplexity

### Installation

1. Clone the repository
   ```
   git clone https://github.com/yourusername/finsearch.git
   cd finsearch
   ```

2. Install backend dependencies
   ```
   cd backend
   npm install
   ```

3. Configure environment variables
   - Create a `.env` file in the backend directory
   - Add your API keys and configuration:
     ```
     OPENAI_API_KEY=your_openai_api_key
     POLYGON_API_KEY=your_polygon_api_key
     FINANCIAL_DATASETS_API_KEY=your_financial_datasets_api_key
     PERPLEXITY_API_KEY=your_perplexity_api_key
     PORT=3001
     NODE_ENV=development
     ALLOWED_ORIGINS=http://localhost:3000
     ```

4. Install frontend dependencies
   ```
   cd ../frontend
   npm install
   ```

### Running the Application

1. Start the backend server
   ```
   cd backend
   npm run dev
   ```

2. Start the frontend development server
   ```
   cd frontend
   npm start
   ```

3. Open your browser and navigate to `http://localhost:3000`

## Usage

### Search Page
- Enter your financial query in the search box
- Select either "Quick Search" or "Deep Research" mode
- Click "Search" to get results

### Compare Companies Page
- Enter ticker symbols separated by commas (e.g., AAPL,MSFT,GOOGL)
- Enter metrics to compare separated by commas (e.g., revenue,profit_margin,growth)
- Click "Compare Companies" to see the comparison results

## API Endpoints

### `/api/query`
- **Method**: POST
- **Description**: Process a financial query
- **Request Body**:
  ```json
  {
    "query": "What is Apple's current stock price?",
    "mode": "sonar" // or "deep-research"
  }
  ```

### `/api/compare`
- **Method**: POST
- **Description**: Compare multiple companies
- **Request Body**:
  ```json
  {
    "tickers": ["AAPL", "MSFT", "GOOGL"],
    "metrics": ["revenue", "profit_margin", "growth"]
  }
  ```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 