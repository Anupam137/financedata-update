import Link from 'next/link';

export default function About() {
  return (
    <main className="min-h-screen p-6 md:p-24">
      <div className="max-w-4xl mx-auto">
        <h1 className="text-3xl font-bold mb-8 bg-gradient-to-r from-blue-600 to-teal-600 text-transparent bg-clip-text">
          About Our Financial Search Engine
        </h1>
        
        <div className="prose max-w-none dark:prose-invert">
          <p className="text-lg mb-6">
            Our financial search engine integrates multiple powerful APIs with OpenAI&apos;s LLM to provide seamless and highly relevant financial insights.
          </p>
          
          <h2 className="text-2xl font-semibold mt-8 mb-4">How It Works</h2>
          <p>
            When you enter a query, our system determines the best source of information and routes your request to the appropriate API:
          </p>
          <ul className="list-disc pl-6 my-4 space-y-2">
            <li>For general financial data (stock prices, financial statements), we use Polygon.io</li>
            <li>For detailed financial metrics, we use FinancialDatasets.ai</li>
            <li>For AI-powered search, we use Perplexity Sonar</li>
            <li>For in-depth analysis, we use Perplexity Deep Research</li>
          </ul>
          <p>
            The OpenAI language model acts as the intermediary, processing your query, deciding which API to call, and formatting the responses into clear, concise answers.
          </p>
          
          <h2 className="text-2xl font-semibold mt-8 mb-4">Features</h2>
          <ul className="list-disc pl-6 my-4 space-y-2">
            <li><strong>Intelligent Search</strong>: AI-powered search for financial data</li>
            <li><strong>Deep Research</strong>: In-depth company analysis and comparisons</li>
            <li><strong>Stock Data</strong>: Real-time and historical prices</li>
            <li><strong>Financial Analysis</strong>: Comprehensive financial statements and metrics</li>
            <li><strong>Market Insights</strong>: News, trends, and forecasts</li>
          </ul>
          
          <h2 className="text-2xl font-semibold mt-8 mb-4">API Integration</h2>
          <p>
            Our platform integrates several powerful APIs to provide comprehensive financial data:
          </p>
          <ul className="list-disc pl-6 my-4 space-y-2">
            <li>
              <strong>Polygon.io</strong>: Provides real-time and historical stock data, market news, SEC filings, and more
            </li>
            <li>
              <strong>FinancialDatasets.ai</strong>: Offers comprehensive financial statements, institutional ownership data, and long-term historical data
            </li>
            <li>
              <strong>Perplexity Sonar</strong>: Delivers AI-powered search and recommendations for financial information
            </li>
            <li>
              <strong>Perplexity Deep Research</strong>: Provides in-depth analysis of companies, industries, and comparisons
            </li>
            <li>
              <strong>OpenAI LLM</strong>: Serves as the core that integrates all APIs and processes user input
            </li>
          </ul>
        </div>
        
        <div className="mt-12">
          <Link
            href="/"
            className="text-blue-600 hover:underline flex items-center"
          >
            &larr; Back to Home
          </Link>
        </div>
      </div>
    </main>
  );
} 