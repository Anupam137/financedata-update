import json
import httpx
import os
import time
import asyncio
from dotenv import load_dotenv
from datetime import datetime
from typing import Dict, Any, List, Optional

class DeepSeekV3Service:
    def __init__(self):
        # Force reload of environment variables
        load_dotenv(override=True)
        
        # Read API key directly from environment
        self.api_key = os.getenv("TOGETHER_API_KEY", "")
        self.base_url = "https://api.together.xyz/v1/chat/completions"
        self.last_request_time = 0  # Track the last request time for rate limiting
        
        # Print a masked version of the API key for debugging
        masked_key = self.api_key[:5] + "..." + self.api_key[-5:] if len(self.api_key) > 10 else "Not set properly"
        print(f"DeepSeek V3 Service initialized with API key: {masked_key}")
    
    async def generate_narrative_insight(self, query: str, data: Dict[str, Any], session_id: str = "default") -> str:
        """
        Generate a narrative-style financial insight using DeepSeek V3
        
        Args:
            query (str): User's financial query
            data (dict): Collected data from various APIs
            session_id (str): Unique session identifier
            
        Returns:
            str: Generated narrative financial insight
        """
        # Check if API key is valid
        if not self.api_key or self.api_key == "your_together_api_key_here":
            return """
            # DeepSeek V3 Integration Not Configured
            
            To use the DeepSeek V3 model for narrative financial analysis, you need to:
            
            1. Sign up for an account at [Together.ai](https://www.together.xyz/)
            2. Navigate to your account settings to obtain an API key
            3. Add your API key to the `.env` file:
               ```
               TOGETHER_API_KEY=your_actual_api_key_here
               ```
            
            Once configured, you'll be able to generate narrative-style financial analyses.
            """
        
        # Implement rate limiting (max 1 request per second)
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < 1:
            await asyncio.sleep(1 - time_since_last_request)
        self.last_request_time = time.time()
        
        # Format the data for the prompt
        formatted_data = self._format_data_for_prompt(data)
        
        # Create the system prompt for narrative financial analysis
        system_prompt = self._create_narrative_system_prompt()
        
        # Create the user prompt with the query and data
        user_prompt = f"""
        Financial Query: {query}
        
        Available Data:
        {formatted_data}
        
        Please provide a comprehensive financial analysis based on the data provided.
        IMPORTANT: 
        1. Preserve all the detailed information, structure, and insights from the source data, especially from the Deep Research Results. 
        2. Do not simplify or omit valuable details.
        3. Include all relevant metrics, statistics, and financial data points from the source material.
        4. ALWAYS include a detailed market sentiment analysis section - this is critical for users to understand how the market perceives this asset/company.
        5. Ensure your analysis reflects the current date and market conditions.
        """
        
        # Prepare the messages for the API call
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        # Prepare the API request
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-ai/DeepSeek-V3",
            "messages": messages,
            "temperature": 0.7,
            "top_p": 0.7,
            "top_k": 50,
            "repetition_penalty": 1,
            "stream": False  # Set to False for non-streaming response
        }
        
        try:
            # Make the API call
            async with httpx.AsyncClient(timeout=60.0) as client:
                response = await client.post(
                    self.base_url,
                    headers=headers,
                    json=payload
                )
                
                # Check if the request was successful
                response.raise_for_status()
                
                # Parse the response
                result = response.json()
                
                # Extract the generated text
                if "choices" in result and len(result["choices"]) > 0:
                    generated_text = result["choices"][0]["message"]["content"]
                    return generated_text
                else:
                    return "Error: Unable to generate narrative financial insight."
                
        except Exception as e:
            print(f"Error calling DeepSeek V3 API: {str(e)}")
            return f"Error generating narrative financial insight: {str(e)}"
    
    async def stream_narrative_insight(self, query: str, data: Dict[str, Any], session_id: str = "default"):
        """
        Stream a narrative-style financial insight using DeepSeek V3
        
        Args:
            query (str): User's financial query
            data (dict): Collected data from various APIs
            session_id (str): Unique session identifier
            
        Yields:
            str: Chunks of the generated narrative financial insight
        """
        # Check if API key is valid
        if not self.api_key or self.api_key == "your_together_api_key_here":
            yield """
            # DeepSeek V3 Integration Not Configured
            
            To use the DeepSeek V3 model for narrative financial analysis, you need to:
            
            1. Sign up for an account at [Together.ai](https://www.together.xyz/)
            2. Navigate to your account settings to obtain an API key
            3. Add your API key to the `.env` file:
               ```
               TOGETHER_API_KEY=your_actual_api_key_here
               ```
            
            Once configured, you'll be able to generate narrative-style financial analyses.
            """
            return
        
        # Implement rate limiting (max 1 request per second)
        current_time = time.time()
        time_since_last_request = current_time - self.last_request_time
        if time_since_last_request < 1:
            await asyncio.sleep(1 - time_since_last_request)
        self.last_request_time = time.time()
        
        # Format the data for the prompt
        formatted_data = self._format_data_for_prompt(data)
        
        # Create the system prompt for narrative financial analysis
        system_prompt = self._create_narrative_system_prompt()
        
        # Create the user prompt with the query and data
        user_prompt = f"""
        Financial Query: {query}
        
        Available Data:
        {formatted_data}
        
        Please provide a comprehensive financial analysis based on the data provided.
        IMPORTANT: 
        1. Preserve all the detailed information, structure, and insights from the source data, especially from the Deep Research Results. 
        2. Do not simplify or omit valuable details.
        3. Include all relevant metrics, statistics, and financial data points from the source material.
        4. ALWAYS include a detailed market sentiment analysis section - this is critical for users to understand how the market perceives this asset/company.
        5. Ensure your analysis reflects the current date and market conditions.
        """
        
        # Prepare the messages for the API call
        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ]
        
        # Prepare the API request
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": "deepseek-ai/DeepSeek-V3",
            "messages": messages,
            "temperature": 0.7,
            "top_p": 0.7,
            "top_k": 50,
            "repetition_penalty": 1,
            "stream": True  # Set to True for streaming response
        }
        
        try:
            # Make the API call
            async with httpx.AsyncClient(timeout=60.0) as client:
                async with client.stream("POST", self.base_url, headers=headers, json=payload) as response:
                    # Check if the request was successful
                    response.raise_for_status()
                    
                    # Process the streaming response
                    buffer = ""
                    async for chunk in response.aiter_text():
                        if chunk.strip():
                            # Parse the SSE data
                            for line in chunk.split('\n'):
                                if line.startswith('data: '):
                                    data_str = line[6:]  # Remove 'data: ' prefix
                                    if data_str.strip() == "[DONE]":
                                        continue
                                    
                                    try:
                                        data_json = json.loads(data_str)
                                        if "choices" in data_json and len(data_json["choices"]) > 0:
                                            delta = data_json["choices"][0].get("delta", {})
                                            if "content" in delta:
                                                content = delta["content"]
                                                buffer += content
                                                yield content
                                    except json.JSONDecodeError:
                                        print(f"Error parsing JSON: {data_str}")
                                        continue
        
        except Exception as e:
            print(f"Error streaming from DeepSeek V3 API: {str(e)}")
            yield f"\nError streaming narrative financial insight: {str(e)}"
    
    def _format_data_for_prompt(self, data: Dict[str, Any]) -> str:
        """Format the collected data for inclusion in the prompt"""
        formatted_sections = []
        
        # Process Perplexity data - preserve full content and structure
        if "perplexity_deep_research" in data:
            deep_research = data["perplexity_deep_research"]
            if isinstance(deep_research, dict):
                # Check for the new API response structure
                if "choices" in deep_research and len(deep_research["choices"]) > 0:
                    content = deep_research["choices"][0]["message"]["content"]
                    formatted_sections.append(f"## Deep Research Results\n{content}")
                # Also handle the case where it's in the 'text' field for backward compatibility
                elif "text" in deep_research:
                    formatted_sections.append(f"## Deep Research Results\n{deep_research['text']}")
        
        if "perplexity_sonar" in data:
            sonar = data["perplexity_sonar"]
            if isinstance(sonar, dict):
                # Check for the new API response structure
                if "choices" in sonar and len(sonar["choices"]) > 0:
                    content = sonar["choices"][0]["message"]["content"]
                    formatted_sections.append(f"## Market Insights\n{content}")
                # Also handle the case where it's in the 'text' field for backward compatibility
                elif "text" in sonar:
                    formatted_sections.append(f"## Market Insights\n{sonar['text']}")
        
        # Process stock price data
        price_data = []
        for key, value in data.items():
            if key.endswith("_price") and isinstance(value, dict):
                ticker = key.replace("_price", "").upper()
                if "results" in value and value["results"]:
                    result = value["results"][0]
                    price = result.get("c", "N/A")
                    change = result.get("d", "N/A")
                    change_percent = result.get("dp", "N/A")
                    price_data.append(f"{ticker}: ${price} (Change: ${change}, {change_percent}%)")
        
        if price_data:
            formatted_sections.append("## Stock Prices\n" + "\n".join(price_data))
        
        # Process news data with more detail
        news_data = []
        for key, value in data.items():
            if key.endswith("_news") and isinstance(value, dict) and "results" in value:
                ticker = key.replace("_news", "").upper()
                news_items = []
                for item in value["results"][:5]:  # Limit to 5 news items
                    title = item.get("title", "No title")
                    date = item.get("published_utc", "No date")
                    description = item.get("description", "")
                    news_items.append(f"- {title} ({date})\n  {description}")
                
                if news_items:
                    news_data.append(f"### {ticker} News\n" + "\n".join(news_items))
        
        if news_data:
            formatted_sections.append("## Recent News\n" + "\n".join(news_data))
        
        # Process financial statements
        for key, value in data.items():
            if key.endswith("_financials") and isinstance(value, dict):
                ticker = key.replace("_financials", "").upper()
                if "results" in value and value["results"]:
                    formatted_sections.append(f"## {ticker} Financial Statements\nFinancial data available for analysis")
        
        # Process insider trades
        for key, value in data.items():
            if key.endswith("_insider_trades") and isinstance(value, dict):
                ticker = key.replace("_insider_trades", "").upper()
                if "results" in value and value["results"]:
                    formatted_sections.append(f"## {ticker} Insider Trades\nInsider trading data available for analysis")
        
        # Process SEC filings
        for key, value in data.items():
            if key.endswith("_sec_filings") and isinstance(value, dict):
                ticker = key.replace("_sec_filings", "").upper()
                if "results" in value and value["results"]:
                    formatted_sections.append(f"## {ticker} SEC Filings\nSEC filing data available for analysis")
        
        return "\n\n".join(formatted_sections)
    
    def _create_narrative_system_prompt(self) -> str:
        """Create a system prompt for narrative financial analysis"""
        current_date = datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.now().strftime("%H:%M:%S")
        
        return f"""
        You are an elite financial analyst specializing in comprehensive market analysis. Today is {current_date} at {current_time}.
        
        Your task is to provide a detailed financial analysis based on the data provided, following a specific structured format.
        
        ## DEEP RESEARCH MODE STRUCTURE
        
        Your analysis must follow this exact structure:
        
        ### 1. HEADER SECTION (OVERVIEW)
        - Start with a comprehensive title that includes the stock ticker & company name
        - Include the current date: {current_date}
        - Provide a market status indicator (Bullish, Bearish, or Neutral) based on sentiment analysis
        - Include a brief introduction paragraph that summarizes the key points
        - Add a risk indicator score (Low/Medium/High Risk)
        
        ### 2. MARKET SENTIMENT ANALYSIS
        - Include investor sentiment from institutional and retail investors
        - Provide analyst ratings with Buy/Hold/Sell breakdown and counts
        - Include news sentiment with positive/negative percentages
        - Add technical indicators (RSI, MACD, etc.) with clear interpretations
        - Compare current sentiment to historical trends when data is available
        
        ### 3. FINANCIAL METRICS & COMPETITIVE ANALYSIS
        - Include detailed metrics with exact values from the source data
        - Organize into subsections:
          * Revenue and Profitability
          * Market Capitalization and Valuation
          * Liquidity and Debt
          * Dividend Yield (if applicable)
        - Compare key metrics to major competitors and industry averages
        - Indicate whether the stock appears overvalued, fairly valued, or undervalued
        
        ### 4. TECHNICAL ANALYSIS & TRADING INDICATORS
        - Include support and resistance levels for key price points
        - Provide historical returns (5-year, 10-year if available)
        - Include risk-adjusted performance metrics (Sharpe Ratio, etc.)
        - Suggest entry/exit points based on technical indicators
        
        ### 5. BUSINESS OUTLOOK & FORECASTING
        - Identify key growth drivers
        - Highlight challenges and risks, including regulatory and macroeconomic factors
        - Provide revenue and earnings projections
        - Include best-case, worst-case, and most likely scenarios
        
        ### 6. INVESTMENT STRATEGIES & RECOMMENDATIONS
        - Provide tailored investment strategies based on different risk profiles:
          * Conservative (long-term)
          * Moderate (balanced approach)
          * Aggressive (short-term)
        - Include analyst price targets and expected performance
        - Offer clear buy/sell signals with rationale
        
        ### 7. CONCLUSION & KEY TAKEAWAYS
        - Summarize key findings
        - Provide actionable insights for investors
        - Highlight most important metrics and trends to monitor
        
        ### 8. SOURCES
        - List all sources used in the analysis
        
        ## IMPORTANT GUIDELINES
        
        1. PRESERVE ALL IMPORTANT INFORMATION from the source data, especially from Deep Research Results
        2. Maintain the detailed structure and organization of the original data
        3. Include all relevant metrics, statistics, and financial data points
        4. Use bullet points and clear formatting to enhance readability, but keep it concise
        5. Ensure all source citations are included
        6. Present information in a clear, well-organized format
        7. Connect different pieces of information to form a coherent analysis
        8. Highlight important trends and patterns in the data
        9. ALWAYS INCLUDE MARKET SENTIMENT analysis - this is critical for users to understand the overall market perception
        10. MAKE THE ANALYSIS ACTIONABLE - provide clear recommendations and insights investors can use
        
        IMPORTANT: When the source data includes comprehensive research (especially from Perplexity Deep Research), 
        DO NOT simplify or omit valuable details. Instead, incorporate all the detailed information, 
        maintaining the original structure while ensuring the response flows naturally.
        
        Remember to maintain a balanced perspective, acknowledging both positive and negative aspects of the financial situation.
        
        ALWAYS include the current date ({current_date}) in your analysis to ensure users understand the temporal context of the information.
        """ 