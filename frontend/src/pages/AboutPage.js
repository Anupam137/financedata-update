import React from 'react';
import './AboutPage.css';

const AboutPage = () => {
  return (
    <div className="about-page">
      <div className="about-header">
        <h1>About FinSearch</h1>
        <p>Your AI-powered financial search engine</p>
      </div>
      
      <div className="about-content">
        <section className="about-section card">
          <h2>What is FinSearch?</h2>
          <p>
            FinSearch is an advanced financial search engine that integrates multiple financial data APIs with OpenAI's
            language models to provide seamless and highly relevant responses to your financial queries.
          </p>
          <p>
            Whether you're looking for real-time stock prices, financial statements, company comparisons, or in-depth
            research, FinSearch can help you find the information you need quickly and efficiently.
          </p>
        </section>
        
        <section className="about-section card">
          <h2>How It Works</h2>
          <p>
            FinSearch uses a combination of AI and financial data APIs to process your queries:
          </p>
          <ol>
            <li>
              <strong>Query Analysis:</strong> When you enter a query, our AI analyzes it to determine what type of
              financial information you're looking for.
            </li>
            <li>
              <strong>Data Retrieval:</strong> Based on the analysis, FinSearch calls the appropriate financial APIs to
              retrieve the most relevant data.
            </li>
            <li>
              <strong>Response Generation:</strong> The AI then processes the data and generates a comprehensive,
              easy-to-understand response.
            </li>
          </ol>
        </section>
        
        <section className="about-section card">
          <h2>Our Data Sources</h2>
          <p>
            FinSearch integrates with multiple financial data providers to ensure you get the most accurate and
            up-to-date information:
          </p>
          <ul>
            <li>
              <strong>Polygon.io:</strong> Real-time and historical stock data, market news, and SEC filings.
            </li>
            <li>
              <strong>Financial Datasets:</strong> Comprehensive financial statements, institutional ownership, and
              segmented financials.
            </li>
            <li>
              <strong>Perplexity:</strong> AI-powered search and deep research capabilities for financial analysis.
            </li>
          </ul>
        </section>
        
        <section className="about-section card">
          <h2>Search Modes</h2>
          <p>
            FinSearch offers two search modes to meet your needs:
          </p>
          <ul>
            <li>
              <strong>Quick Search (Sonar):</strong> Fast, concise answers to straightforward financial questions.
              Perfect for checking stock prices, basic company info, or recent news.
            </li>
            <li>
              <strong>Deep Research:</strong> Comprehensive, in-depth analysis for more complex queries. Ideal for
              detailed company analysis, industry comparisons, or investment research.
            </li>
          </ul>
        </section>
      </div>
    </div>
  );
};

export default AboutPage; 