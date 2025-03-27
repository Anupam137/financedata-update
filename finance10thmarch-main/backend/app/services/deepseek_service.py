import json
import httpx
import os
import time
import asyncio
from dotenv import load_dotenv
from datetime import datetime

class DeepSeekService:
    def __init__(self):
        # Force reload of environment variables
        load_dotenv(override=True)
        
        # Read API key directly from environment
        self.api_key = os.getenv("TOGETHER_API_KEY", "")
        self.base_url = "https://api.together.xyz/v1/chat/completions"
        self.last_request_time = 0  # Track the last request time for rate limiting
        
        # Print a masked version of the API key for debugging
        masked_key = self.api_key[:5] + "..." + self.api_key[-5:] if len(self.api_key) > 10 else "Not set properly"
        print(f"DeepSeek Service initialized with API key: {masked_key}")
        
    async def generate_financial_insight(self, query: str, data, session_id: str = "default"):
        """
        Generate a comprehensive financial insight using DeepSeek R1
        
        Args:
            query (str): User's financial query
            data (dict): Collected data from various APIs
            session_id (str): Unique session identifier
            
        Returns:
            str: Generated financial insight
        """
        # Check if API key is valid
        if not self.api_key or self.api_key == "your_together_api_key_here":
            return """
            # DeepSeek R1 Integration Not Configured
            
            To use the DeepSeek R1 model for comprehensive financial research, you need to:
            
            1. Sign up for an account at [Together.ai](https://www.together.xyz/)
            2. Navigate to your account settings to obtain an API key
            3. Add your API key to the `.env` file:
               ```
               TOGETHER_API_KEY=your_actual_api_key_here
               ```
            
            Once configured, you'll be able to generate in-depth, professional-grade financial research reports.
            
            For now, I've used OpenAI and Perplexity to provide the best analysis possible with the available data.
            """
        
        # Format the data in a simplified way to reduce payload size
        formatted_data = self._format_data_for_prompt_simplified(data, query)
        
        # Add current date for temporal context
        current_date = datetime.now().strftime("%B %d, %Y")
        
        # Create the system prompt - enhanced for deep research
        system_prompt = f"""
        You are an elite financial analyst with expertise in creating comprehensive, in-depth research reports.
        Your task is to produce a thorough, professional-grade financial analysis that would satisfy institutional investors and financial professionals.
        
        Today's date is {current_date}. All analysis should be based on this current date.
        
        APPROACH TO DEEP RESEARCH:
        - Conduct exhaustive analysis of all available data
        - Explore multiple perspectives and potential interpretations
        - Identify connections between different data points that might not be immediately obvious
        - Consider both short-term and long-term implications
        - Evaluate risks, opportunities, and potential scenarios
        - Provide nuanced context that helps understand the broader picture
        
        AVAILABLE DATA SOURCES:
        You have access to the following data sources:
        1. Perplexity Sonar - For real-time news and market insights
        2. Perplexity Deep Research - For in-depth financial analysis
        3. Polygon.io - For stock prices, charts, and technical data
        4. FinancialDatasets.ai - For company filings, insider trades, and SEC filings
        
        IMPORTANT FOR ALL FINANCIAL DATA:
        - The provided API data contains the most current prices, metrics, and information
        - Always use this data as your primary source for current prices, trends, and news
        - Do not rely on your pre-trained knowledge for current values or recent events
        - This applies to all assets: stocks, cryptocurrencies, commodities, indices, etc.
        - If the data shows a price or metric, use that exact value in your analysis
        
        IMPORTANT GUIDELINES:
        1. BE COMPREHENSIVE - This is a deep research report, so be thorough and detailed. Don't summarize or simplify unnecessarily.
        2. USE THE DATA - The provided financial data is accurate and comprehensive. Incorporate it fully in your analysis.
        3. SHOW YOUR REASONING - Explain your thought process and how you arrived at conclusions.
        4. INCLUDE RELEVANT METRICS - Incorporate key financial metrics, ratios, and comparisons where appropriate.
        5. CONSIDER MARKET CONTEXT - Place your analysis within the broader market and economic environment.
        6. CITE SOURCES - Reference specific data points and their sources throughout your analysis.
        
        REPORT STRUCTURE:
        While you have freedom to organize your report as appropriate for the specific query, consider including these elements:
        - Executive Summary: Brief overview of key findings
        - Detailed Analysis: In-depth examination of the data, trends, and implications
        - Comparative Analysis: When relevant, compare against peers, industry benchmarks, or historical performance
        - Risk Assessment: Evaluation of potential risks and mitigating factors
        - Future Outlook: Reasoned projections based on current data and trends
        - Conclusion: Synthesis of the analysis with key takeaways
        - Follow-up Questions: Suggested areas for further research
        
        Your report should be well-structured with clear headings and logical flow, but prioritize depth and comprehensiveness over rigid formatting.
        Use markdown formatting to enhance readability of this detailed report.
        """
        
        # Create the user prompt - emphasize the deep research nature
        user_prompt = f"""
        I need a comprehensive deep research report on the following financial query:
        
        {query}
        
        Please provide an exhaustive analysis with detailed insights, data-driven conclusions, and thorough examination of all relevant factors. This should be a professional-grade financial research report.
        """
        
        # Create the messages array
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
            {"role": "system", "content": f"Here is the comprehensive financial data for your deep research report:\n\n{formatted_data}"}
        ]
        
        # Implement rate limiting - ensure at least 1 second between requests
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < 1.0:
            wait_time = 1.0 - time_since_last_request
            print(f"Rate limiting: Waiting {wait_time:.2f} seconds before making request")
            await asyncio.sleep(wait_time)
        
        # Call the Together.ai API using direct HTTP request (based on cURL example)
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-ai/DeepSeek-R1",
            "messages": messages,
            "max_tokens": 8000,  # Increased from 2000 to allow for longer responses
            "temperature": 0.7,
            "top_p": 0.95,
            "top_k": 50,
            "repetition_penalty": 1.0,
            "stream": False
        }
        
        print(f"Using model: {payload['model']}")
        
        try:
            # Update last request time
            self.last_request_time = time.time()
            
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    self.base_url,
                    json=payload,
                    headers=headers,
                    timeout=180.0
                )
                response.raise_for_status()
                result = response.json()
                
                if "choices" in result and len(result["choices"]) > 0:
                    return result["choices"][0]["message"]["content"]
                else:
                    return "Unable to generate deep research analysis with DeepSeek R1."
        except httpx.HTTPStatusError as e:
            if e.response.status_code == 401:
                print(f"Authentication error with Together.ai API: {e}")
                return """
                # DeepSeek R1 Integration Error
                
                There was an authentication error with the Together.ai API. The provided API key appears to be invalid.
                
                To fix this issue:
                
                1. Sign up for an account at [Together.ai](https://www.together.xyz/)
                2. Navigate to your account settings to obtain a valid API key
                3. Update your API key in the `.env` file:
                   ```
                   TOGETHER_API_KEY=your_actual_api_key_here
                   ```
                
                For now, I've used the data from Perplexity and other sources to provide the best analysis possible.
                """
            elif e.response.status_code == 429:
                print(f"Rate limit exceeded with Together.ai API: {e}")
                return """
                # DeepSeek R1 Rate Limit Exceeded
                
                The Together.ai API rate limit has been exceeded. This typically happens when:
                
                1. Too many requests are made in a short period of time
                2. You're using a free tier account with limited quota (60 requests per minute)
                3. The API is experiencing high demand from other users
                
                Please try again later or consider upgrading your Together.ai account for higher rate limits.
                
                For now, I've used the data from Perplexity and other sources to provide the best analysis possible.
                """
            else:
                print(f"HTTP error calling DeepSeek API: {e}")
                return f"Error: {str(e)}"
        except Exception as e:
            print(f"Error calling DeepSeek API: {e}")
            return f"Error: {str(e)}"
            
    def _format_data_for_prompt_simplified(self, data, query=None):
        """Format the data in a simplified way to reduce payload size"""
        # Add current date for temporal context
        current_date = datetime.now().strftime("%B %d, %Y")
        
        formatted_text = f"## FINANCIAL DATA SUMMARY\n\nData as of {current_date}\n\n"
        
        # Add Perplexity content with summarization
        for key, value in data.items():
            if key in ["perplexity_sonar", "perplexity_deep_research"] and "error" not in value:
                if "choices" in value and len(value["choices"]) > 0:
                    content = value["choices"][0]["message"]["content"]
                    # Truncate to first 1000 characters to reduce payload size
                    content = content[:1000] + "..." if len(content) > 1000 else content
                    source_type = "Perplexity Sonar" if key == "perplexity_sonar" else "Perplexity Deep Research"
                    formatted_text += f"## {source_type} Analysis\n"
                    formatted_text += content + "\n\n"
        
        # Add stock price data in a compact format
        stock_price_data = {}
        for key, value in data.items():
            if "_price" in key and "error" not in value:
                ticker = key.split("_")[0]
                if "results" in value and value["results"]:
                    result = value["results"][0]
                    stock_price_data[ticker] = {
                        "close": result.get('c', 'N/A'),
                        "open": result.get('o', 'N/A'),
                        "high": result.get('h', 'N/A'),
                        "low": result.get('l', 'N/A'),
                        "volume": result.get('v', 'N/A')
                    }
        
        if stock_price_data:
            formatted_text += "## Stock Price Data\n"
            for ticker, price_data in stock_price_data.items():
                formatted_text += f"### {ticker}: Close ${price_data['close']}, Open ${price_data['open']}, High ${price_data['high']}, Low ${price_data['low']}, Volume {price_data['volume']}\n\n"
        
        # Add news data in a compact format
        news_data = {}
        for key, value in data.items():
            if "_news" in key and "error" not in value:
                ticker = key.split("_")[0]
                if "results" in value:
                    # Only include top 3 news items to reduce payload size
                    news_data[ticker] = value["results"][:3]
        
        if news_data:
            formatted_text += "## Recent News\n"
            for ticker, news_items in news_data.items():
                formatted_text += f"### {ticker} News\n"
                for i, news in enumerate(news_items):
                    formatted_text += f"- {news.get('title', 'No title')}: {news.get('description', '')[:100]}...\n"
                formatted_text += "\n"
        
        return formatted_text
    
    def _format_data_for_prompt(self, data, query=None):
        """Format the data in a comprehensive way for deep research"""
        # Add current date for temporal context
        current_date = datetime.now().strftime("%B %d, %Y")
        
        formatted_text = f"## COMPREHENSIVE FINANCIAL DATA FOR DEEP RESEARCH\n\nData as of {current_date}\n\n"
        
        # Add Perplexity content with minimal summarization
        for key, value in data.items():
            if key in ["perplexity_sonar", "perplexity_deep_research"] and "error" not in value:
                if "choices" in value and len(value["choices"]) > 0:
                    content = value["choices"][0]["message"]["content"]
                    source_type = "Perplexity Sonar" if key == "perplexity_sonar" else "Perplexity Deep Research"
                    formatted_text += f"## Complete {source_type} Analysis\n"
                    formatted_text += content + "\n\n"
                    
                    # Add citations if available
                    if "citations" in value:
                        formatted_text += "### Sources:\n"
                        for i, citation in enumerate(value["citations"]):
                            formatted_text += f"[{i+1}] {citation}\n"
                        formatted_text += "\n"
        
        # Add detailed stock price data
        stock_price_data = {}
        for key, value in data.items():
            if "_price" in key and "error" not in value:
                ticker = key.split("_")[0]
                if "results" in value and value["results"]:
                    result = value["results"][0]
                    stock_price_data[ticker] = {
                        "close": result.get('c', 'N/A'),
                        "open": result.get('o', 'N/A'),
                        "high": result.get('h', 'N/A'),
                        "low": result.get('l', 'N/A'),
                        "volume": result.get('v', 'N/A'),
                        "timestamp": result.get('t', 'N/A'),
                        "trades": result.get('n', 'N/A')
                    }
        
        if stock_price_data:
            formatted_text += "## Detailed Stock Price Data\n"
            for ticker, price_data in stock_price_data.items():
                formatted_text += f"### {ticker} Stock Price Details\n"
                formatted_text += f"- Close Price: ${price_data['close']}\n"
                formatted_text += f"- Open Price: ${price_data['open']}\n"
                formatted_text += f"- High: ${price_data['high']}\n"
                formatted_text += f"- Low: ${price_data['low']}\n"
                formatted_text += f"- Volume: {price_data['volume']:,} shares\n"
                formatted_text += f"- Number of Trades: {price_data['trades']:,}\n"
                
                # Calculate price change and percentage
                if price_data['close'] != 'N/A' and price_data['open'] != 'N/A':
                    change = float(price_data['close']) - float(price_data['open'])
                    change_percent = (change / float(price_data['open'])) * 100 if float(price_data['open']) != 0 else 0
                    direction = "up" if change > 0 else "down"
                    formatted_text += f"- Price Change: {direction} ${abs(change):.2f} ({abs(change_percent):.2f}%)\n"
                
                formatted_text += "\n"
        
        # Include full news data instead of summaries
        news_data = {}
        for key, value in data.items():
            if "_news" in key and "error" not in value:
                ticker = key.split("_")[0]
                if "results" in value:
                    news_data[ticker] = value["results"]  # Include all news items
        
        if news_data:
            formatted_text += "## Comprehensive News Analysis\n"
            for ticker, news_items in news_data.items():
                formatted_text += f"### {ticker} News Coverage\n"
                for i, news in enumerate(news_items):
                    formatted_text += f"#### {news.get('title', 'No title')}\n"
                    formatted_text += f"- Published: {news.get('published_utc', 'N/A')}\n"
                    if news.get('description'):
                        formatted_text += f"- Full Summary: {news.get('description')}\n"
                    if news.get('article_url'):
                        formatted_text += f"- URL: {news.get('article_url')}\n"
                    formatted_text += "\n"
        
        # Include complete financial data
        financial_data = {}
        for key, value in data.items():
            if "_financials" in key and "error" not in value:
                ticker = key.split("_")[0]
                if "financials" in value:
                    financial_data[ticker] = value["financials"]
        
        if financial_data:
            formatted_text += "## Complete Financial Statements\n"
            for ticker, financials in financial_data.items():
                formatted_text += f"### {ticker} Detailed Financial Data\n"
                formatted_text += json.dumps(financials, indent=2) + "\n\n"
        
        # Include all insider trades data
        insider_data = {}
        for key, value in data.items():
            if "_insider_trades" in key and "error" not in value:
                ticker = key.split("_")[0]
                if "results" in value:
                    insider_data[ticker] = value["results"]  # Include all insider trades
        
        if insider_data:
            formatted_text += "## Comprehensive Insider Trading Activity\n"
            for ticker, trades in insider_data.items():
                formatted_text += f"### {ticker} Insider Trades Analysis\n"
                for trade in trades:
                    formatted_text += f"- Name: {trade.get('name', 'Unknown')}\n"
                    formatted_text += f"- Title: {trade.get('title', 'Unknown')}\n"
                    formatted_text += f"- Shares: {trade.get('shares', 'N/A')}\n"
                    formatted_text += f"- Value: ${trade.get('value', 'N/A')}\n"
                    formatted_text += f"- Date: {trade.get('date', 'N/A')}\n\n"
        
        # Include all SEC filings data
        sec_data = {}
        for key, value in data.items():
            if "_sec_filings" in key and "error" not in value:
                ticker = key.split("_")[0]
                if "filings" in value:
                    sec_data[ticker] = value["filings"]  # Include all SEC filings
        
        if sec_data:
            formatted_text += "## Complete SEC Filings Analysis\n"
            for ticker, filings in sec_data.items():
                formatted_text += f"### {ticker} SEC Filings\n"
                for filing in filings:
                    formatted_text += f"- Form: {filing.get('form', 'Unknown')}\n"
                    formatted_text += f"- Filed Date: {filing.get('filed_date', 'N/A')}\n"
                    formatted_text += f"- Description: {filing.get('description', 'N/A')}\n\n"
        
        return formatted_text 