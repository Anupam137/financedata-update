from openai import OpenAI
from app.core.config import OPENAI_API_KEY
import json
import re
from typing import Dict, List, Any, Optional
from datetime import datetime
from dotenv import load_dotenv
import os

# Global conversation history dictionary to persist across requests
GLOBAL_CONVERSATION_HISTORY = {}

class OpenAIService:
    def __init__(self):
        """
        Initialize the OpenAI service
        """
        self.use_redis = False  # Flag to control whether to use Redis or in-memory storage
        
        # Common financial entities to look for
        self.common_tickers = ["AAPL", "MSFT", "GOOGL", "AMZN", "META", "TSLA", "NVDA", "AMD", "INTC", "IBM"]
        self.common_companies = ["Apple", "Microsoft", "Google", "Amazon", "Meta", "Facebook", "Tesla", "NVIDIA", "AMD", "Intel", "IBM"]
        
        # Load OpenAI API key
        load_dotenv()
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            print("Warning: OPENAI_API_KEY not found in environment variables")
            self.api_key = "dummy_key"  # Placeholder for testing
        
        self.client = OpenAI(api_key=self.api_key)
        self.model = "gpt-4-turbo"
    
    async def generate_response(self, messages, temperature=0.7, max_tokens=1500):
        """
        Generate a response using OpenAI's GPT model
        
        Args:
            messages (list): List of message dictionaries
            temperature (float): Controls randomness
            max_tokens (int): Maximum tokens to generate
            
        Returns:
            str: Generated response
        """
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content
        except Exception as e:
            print(f"Error calling OpenAI API: {e}")
            return f"Error: {str(e)}"
    
    def get_conversation_history(self, session_id: str, max_messages: int = 10) -> List[Dict[str, str]]:
        """
        Get conversation history for a session
        
        Args:
            session_id (str): Unique session identifier
            max_messages (int): Maximum number of messages to include
            
        Returns:
            List[Dict[str, str]]: List of message dictionaries
        """
        global GLOBAL_CONVERSATION_HISTORY
        
        if session_id not in GLOBAL_CONVERSATION_HISTORY:
            GLOBAL_CONVERSATION_HISTORY[session_id] = []
            print(f"DEBUG: No conversation history found for session {session_id}")
        else:
            print(f"DEBUG: Found conversation history for session {session_id} with {len(GLOBAL_CONVERSATION_HISTORY[session_id])} messages")
            for i, msg in enumerate(GLOBAL_CONVERSATION_HISTORY[session_id]):
                print(f"DEBUG: Message {i}: role={msg['role']}, content={msg['content'][:50]}...")
        
        # Return the most recent messages up to max_messages
        return GLOBAL_CONVERSATION_HISTORY[session_id][-max_messages:]
    
    def extract_entities_from_conversation(self, history: List[Dict[str, str]]) -> List[str]:
        """
        Extract key entities (companies, tickers, financial terms) from conversation history
        
        Args:
            history (List[Dict[str, str]]): Conversation history
            
        Returns:
            List[str]: List of extracted entities
        """
        if not history:
            print("DEBUG: No history provided for entity extraction")
            return []
            
        # Combine all messages into a single text for analysis
        all_text = " ".join([msg["content"] for msg in history])
        print(f"DEBUG: Analyzing text for entities: {all_text[:100]}...")
        
        # Extract entities
        entities = set()
        
        # Look for common tickers (exact match)
        for ticker in self.common_tickers:
            if re.search(r'\b' + ticker + r'\b', all_text):
                entities.add(ticker)
                
        # Look for common companies (case insensitive)
        for company in self.common_companies:
            if re.search(r'\b' + company + r'\b', all_text, re.IGNORECASE):
                entities.add(company)
                
        # Look for ticker patterns (e.g., $AAPL or AAPL:NASDAQ)
        ticker_patterns = re.findall(r'\$([A-Z]{1,5})\b|\b([A-Z]{1,5})[:\.][A-Z]+', all_text)
        for pattern_match in ticker_patterns:
            for group in pattern_match:
                if group and len(group) >= 1 and len(group) <= 5:
                    entities.add(group)
        
        # Map company names to their tickers and vice versa for better context
        company_to_ticker = {
            "APPLE": "AAPL", 
            "MICROSOFT": "MSFT", 
            "GOOGLE": "GOOGL", 
            "ALPHABET": "GOOGL", 
            "AMAZON": "AMZN", 
            "META": "META", 
            "FACEBOOK": "META", 
            "TESLA": "TSLA", 
            "NVIDIA": "NVDA", 
            "AMD": "AMD", 
            "INTEL": "INTC", 
            "IBM": "IBM"
        }
        
        # Add related entities
        entities_to_add = set()
        for entity in entities:
            upper_entity = entity.upper()
            # If we have a company name, add its ticker
            if upper_entity in company_to_ticker:
                entities_to_add.add(company_to_ticker[upper_entity])
            # If we have a ticker, add its company name
            for company, ticker in company_to_ticker.items():
                if entity == ticker:
                    entities_to_add.add(company.title())
        
        entities.update(entities_to_add)
        
        print(f"DEBUG: Extracted entities: {list(entities)}")
        return list(entities)
    
    def add_to_conversation(self, session_id: str, role: str, content: str):
        """
        Add a message to the conversation history
        
        Args:
            session_id (str): Unique session identifier
            role (str): Message role ('user' or 'assistant')
            content (str): Message content
        """
        global GLOBAL_CONVERSATION_HISTORY
        
        # Initialize conversation history for this session if it doesn't exist
        if session_id not in GLOBAL_CONVERSATION_HISTORY:
            GLOBAL_CONVERSATION_HISTORY[session_id] = []
        
        # Add the message to the conversation history
        GLOBAL_CONVERSATION_HISTORY[session_id].append({
            "role": role,
            "content": content
        })
        
        print(f"Added message to conversation {session_id}. History length: {len(GLOBAL_CONVERSATION_HISTORY[session_id])}")
        
        # Limit history size to prevent memory issues (keep last 20 messages)
        if len(GLOBAL_CONVERSATION_HISTORY[session_id]) > 20:
            GLOBAL_CONVERSATION_HISTORY[session_id] = GLOBAL_CONVERSATION_HISTORY[session_id][-20:]
    
    async def analyze_query(self, query, session_id):
        """
        Analyze a query to determine which APIs to call
        
        Args:
            query (str): User's query
            session_id (str): Unique session identifier
            
        Returns:
            dict: API call plan
        """
        print(f"\nDEBUG: analyze_query called with query='{query}', session_id='{session_id}'")
        
        # Add current date for temporal context
        current_date = datetime.now().strftime("%B %d, %Y")
        
        # Get conversation history
        history = self.get_conversation_history(session_id)
        print(f"DEBUG: Got {len(history)} messages in conversation history")
        
        # Extract entities from conversation history
        entities = self.extract_entities_from_conversation(history)
        
        # Determine if this is a follow-up question
        is_follow_up = len(history) >= 3  # At least one previous Q&A pair plus current query
        print(f"DEBUG: Is follow-up question: {is_follow_up}")
        
        # Build context information
        context_info = ""
        if is_follow_up:
            # Get the last exchange (question and answer)
            previous_exchanges = []
            print(f"DEBUG: Extracting previous exchanges from {len(history)} messages")
            
            # Debug the history array
            for i, msg in enumerate(history):
                print(f"DEBUG: History[{i}]: role={msg['role']}, content={msg['content'][:50]}...")
            
            try:
                # Extract previous exchanges - the history should be in pairs of user/assistant messages
                # The last message is the current query, so we need to look at messages before that
                for i in range(0, len(history) - 1, 2):
                    if i + 1 < len(history) and history[i]['role'] == 'user' and history[i+1]['role'] == 'assistant':
                        q = history[i]['content']
                        a = history[i+1]['content']
                        print(f"DEBUG: Found exchange: Q={q[:30]}..., A={a[:30]}...")
                        previous_exchanges.append((q, a[:300] + "..." if len(a) > 300 else a))
            except Exception as e:
                print(f"DEBUG: Error extracting previous exchanges: {e}")
            
            print(f"DEBUG: Extracted {len(previous_exchanges)} previous exchanges")
            
            if previous_exchanges and entities:
                # Create a specific instruction for the current query based on entities
                current_query_instruction = ""
                for entity in entities:
                    if entity in ["NVDA", "NVIDIA"]:
                        current_query_instruction = f"""
                        IMPORTANT INSTRUCTION FOR THIS SPECIFIC QUERY:
                        The current query "{query}" is about {entity}. You MUST interpret this query as asking about {entity}'s information.
                        You MUST include "{entity}" in the tickers list in your API plan.
                        """
                        break
                
                context_info = f"""IMPORTANT - CONVERSATION CONTEXT:
This is a follow-up question in an ongoing conversation. Previous exchanges:

{current_query_instruction}

"""
                
                for i, (q, a) in enumerate(previous_exchanges):
                    context_info += f"Exchange {i+1}:\n"
                    context_info += f"User: \"{q}\"\n"
                    context_info += f"Assistant: \"{a}\"\n\n"
                
                if entities:
                    context_info += "KEY ENTITIES DISCUSSED IN THIS CONVERSATION:\n"
                    context_info += ", ".join(entities) + "\n\n"
                
                context_info += """IMPORTANT INSTRUCTIONS FOR HANDLING THIS FOLLOW-UP QUERY:
1. When the user refers to companies, stocks, or topics mentioned in previous exchanges, maintain that context
2. Pronouns like 'it', 'they', 'their', 'them', 'its' likely refer to entities from previous exchanges
3. If the query mentions 'current', 'latest', or similar terms without specifying an entity, assume it refers to previously discussed entities
4. The query is likely related to the most recent exchange - prioritize that context
5. Make sure to include any relevant ticker symbols from the conversation in your API plan

"""
                
                print(f"DEBUG: Created context info: {context_info[:200]}...")
        
        prompt = f"""
        You are a financial search engine that needs to determine which APIs to call based on a user's query.
        
        Today's date is {current_date}. Please consider this when analyzing time-sensitive queries.
        
        {context_info}
        
        User Query: {query}
        
        Please analyze the query and determine:
        
        1. Whether to call Perplexity Sonar for real-time news and market insights
        2. Whether to call Perplexity Deep Research for in-depth financial analysis
        3. Whether to fetch stock prices using Polygon.io
        4. Whether to fetch financial statements
        5. Whether to fetch insider trades
        6. Whether to fetch SEC filings
        7. Which ticker symbols are relevant to the query
        
        If the query is about a cryptocurrency, please identify:
        1. That it's a cryptocurrency query (set is_crypto_query to true)
        2. The standard ticker symbol (e.g., BTC for Bitcoin, ETH for Ethereum)
        
        If the query is asking for trading advice, entry/exit points, or market predictions, please identify:
        1. That it's a trading-related query (set is_trading_query to true)
        2. The timeframe mentioned (e.g., "next week", "tomorrow", "long-term")
        
        Return your analysis as a JSON object with the following structure:
        {{
            "call_perplexity_sonar": boolean,
            "call_perplexity_deep_research": boolean,
            "need_stock_price": boolean,
            "need_financials": boolean,
            "need_insider_trades": boolean,
            "need_sec_filings": boolean,
            "tickers": [list of ticker symbols],
            "is_crypto_query": boolean,
            "is_trading_query": boolean,
            "trading_timeframe": string (only if is_trading_query is true),
            "reasoning": "Brief explanation of your analysis"
        }}
        
        Only include the JSON object in your response, nothing else.
        """
        
        messages = [
            {"role": "system", "content": "You are a financial query analyzer that determines which APIs to call."},
            {"role": "user", "content": prompt}
        ]
        
        response = self.client.chat.completions.create(
            model="gpt-4-turbo",
            messages=messages,
            temperature=0.1,  # Low temperature for more deterministic results
            max_tokens=500
        )
        
        result = response.choices[0].message.content
        
        try:
            # Parse the JSON response
            api_plan = json.loads(result)
            return api_plan
        except json.JSONDecodeError:
            # If the response is not valid JSON, extract it using regex
            import re
            json_match = re.search(r'({.*})', result, re.DOTALL)
            if json_match:
                try:
                    api_plan = json.loads(json_match.group(1))
                    return api_plan
                except:
                    pass
            
            # Fallback to a default plan
            return {
                "call_perplexity_sonar": True,
                "call_perplexity_deep_research": False,
                "need_stock_price": False,
                "need_financials": False,
                "need_insider_trades": False,
                "need_sec_filings": False,
                "tickers": [],
                "is_crypto_query": False,
                "is_trading_query": False,
                "reasoning": "Failed to parse API plan, using default."
            }
    
    async def generate_financial_insight(self, query: str, data: Dict[str, Any], session_id: str = "default"):
        """
        Generate financial insights based on query and data
        
        Args:
            query (str): User's query
            data (Dict[str, Any]): Financial data from various APIs
            session_id (str): Unique session identifier
            
        Returns:
            str: Generated financial insight
        """
        print(f"\nDEBUG: generate_financial_insight called with query='{query}', session_id='{session_id}'")
        
        # Get conversation history
        history = self.get_conversation_history(session_id)
        print(f"DEBUG: Got {len(history)} messages in conversation history")
        
        # Extract entities from conversation history
        entities = self.extract_entities_from_conversation(history)
        
        # Determine if this is a follow-up question
        is_follow_up = len(history) >= 3  # At least one previous Q&A pair plus current query
        print(f"DEBUG: Is follow-up question: {is_follow_up}")
        
        # Build conversation context
        conversation_context = ""
        if is_follow_up:
            # Get the previous exchanges (question and answer pairs)
            previous_exchanges = []
            print(f"DEBUG: Extracting previous exchanges from {len(history)} messages")
            
            # Debug the history array
            for i, msg in enumerate(history):
                print(f"DEBUG: History[{i}]: role={msg['role']}, content={msg['content'][:50]}...")
            
            try:
                # Extract previous exchanges - the history should be in pairs of user/assistant messages
                # The last message is the current query, so we need to look at messages before that
                for i in range(0, len(history) - 1, 2):
                    if i + 1 < len(history) and history[i]['role'] == 'user' and history[i+1]['role'] == 'assistant':
                        q = history[i]['content']
                        a = history[i+1]['content']
                        print(f"DEBUG: Found exchange: Q={q[:30]}..., A={a[:30]}...")
                        previous_exchanges.append((q, a[:300] + "..." if len(a) > 300 else a))
            except Exception as e:
                print(f"DEBUG: Error extracting previous exchanges: {e}")
            
            print(f"DEBUG: Extracted {len(previous_exchanges)} previous exchanges")
            
            if previous_exchanges:
                # Create specific instructions for handling entities in the current query
                entity_instructions = ""
                for entity in entities:
                    entity_instructions += f"- When the user refers to '{entity}' or uses pronouns like 'it', 'they', 'their', interpret them as referring to {entity}.\n"
                
                conversation_context = f"""
                # CONVERSATION CONTEXT - READ THIS FIRST
                
                This is a follow-up question in an ongoing conversation. You MUST maintain context from previous exchanges.
                
                ## Previous Exchanges:
                """
                
                for i, (q, a) in enumerate(previous_exchanges):
                    conversation_context += f"\nExchange {i+1}:\nUser: \"{q}\"\nAssistant: \"{a}\"\n"
                
                if entities:
                    conversation_context += "\n## Key Entities Discussed:\n"
                    conversation_context += ", ".join(entities) + "\n"
                
                conversation_context += f"""
                ## Current Query:
                "{query}"
                
                ## Critical Instructions:
                - This query is a FOLLOW-UP to the previous exchanges.
                - Maintain context from previous exchanges when generating your response.
                {entity_instructions}
                - If the query contains pronouns or references without specific entities, assume they refer to entities from previous exchanges.
                - Focus on providing a direct answer to the current query while maintaining the conversation context.
                """
                
                print(f"DEBUG: Created conversation context: {conversation_context[:200]}...")
        
        system_prompt = f"""
        {conversation_context}
        
        You are a specialized financial assistant that provides accurate information about stocks, 
        financial markets, and company data.
        
        IMPORTANT: The data provided to you contains COMPLETE and ACCURATE information from trusted sources.
        You MUST use this data as the primary basis for your response. DO NOT claim you lack information
        if relevant data is provided to you.
        
        CRYPTOCURRENCY DATA INSTRUCTIONS:
        - When responding to cryptocurrency price queries, ALWAYS include Polygon.io data as one of the primary sources.
        - List Polygon.io as the first source when presenting cryptocurrency prices from multiple exchanges.
        - Include the specific price data points from Polygon.io (current price, 24h high/low, volume).
        - You may then include prices from other exchanges for comparison.
        
        IMPORTANT CLARIFICATION ON FINANCIAL TERMS:
        - When users ask about "sentiment" for a company or stock, they are referring to MARKET SENTIMENT - 
          the overall attitude of investors and analysts toward a particular security or financial market.
          This includes analyst ratings, investor perception, and market outlook - NOT sentiment analysis tools.
        
        RESPONSE STRUCTURE AND FORMATTING:
        1. Use clear section headings (e.g., "Stock Prices", "Market Sentiment", "Analyst Ratings")
        2. Use bullet points for lists of information to improve readability
        3. Include specific metrics with exact numbers when available (P/E ratios, price targets, etc.)
        4. For stock price data, always include:
           - Current/recent price
           - Day range (high/low)
           - Trading volume
           - Previous close (if available)
        5. For comparative queries, include a "Key Differences" section and a "Conclusion"
        6. Add citation references like [1], [2] to specific claims when appropriate
        7. Always end with 2-3 suggested follow-up questions to encourage continued engagement
        
        TECHNICAL INDICATORS:
        - When discussing stocks, include relevant technical indicators (MACD, RSI) if available
        - Include year-to-date (YTD) performance metrics when relevant
        - For comparative analyses, mention volatility metrics and correlation data if available
        
        TRADING ADVICE GUIDELINES:
        - When users ask about trading outcomes, potential trades, or market direction, include:
          1. SPECIFIC TRADE SETUP:
             - Entry Point: Provide a specific price or price range for entering the position
             - Exit Strategy: Include multiple take-profit targets with specific price levels
             - Stop Loss: Recommend a specific stop-loss level to limit potential losses
             - Risk-Reward Ratio: Calculate and state the risk-reward ratio for the suggested trade
          
          2. TIMEFRAME CONSIDERATIONS:
             - Specify the expected duration of the trade (day trade, swing trade, position trade)
             - Identify key upcoming events that might impact the trade (earnings, economic data, etc.)
          
          3. TECHNICAL JUSTIFICATION:
             - Reference specific technical indicators (RSI, MACD, moving averages) with current values
             - Identify key support/resistance levels relevant to the trade
             - Mention chart patterns if applicable (head and shoulders, double bottom, etc.)
          
          4. ALTERNATIVE SCENARIOS:
             - Provide at least one alternative scenario if the primary prediction doesn't play out
             - Include modified entry/exit points for the alternative scenario
          
          5. DISCLAIMER:
             - Always conclude trading advice with this disclaimer:
               "DISCLAIMER: This trading suggestion is generated by an AI model based on available data and should not be considered financial advice. Always conduct your own research and consider consulting with a financial advisor before making investment decisions."
        
        You have access to the following data sources:
        1. Perplexity Sonar - For real-time news and market insights
        2. Perplexity Deep Research - For in-depth financial analysis
        3. Polygon.io - For stock prices, charts, and technical data
        4. FinancialDatasets.ai - For company filings, insider trades, and SEC filings
        
        Format your response in a clear, structured way. Use markdown formatting for better readability.
        Include relevant numbers, percentages, and dates when available.
        Always cite your sources at the end of your response.
        """
        
        # Build messages including conversation history
        messages = [
            {"role": "system", "content": system_prompt}
        ]
        
        # Add conversation history
        for msg in history:
            messages.append(msg)
        
        # Add the current query
        messages.append({"role": "user", "content": query})
        
        # Format the data in a readable way
        formatted_data = self._format_data_for_prompt(data, query)
        data_message = f"""
        Here is the financial data directly relevant to your query: "{query}"
        
        This data contains the information needed to fully answer your question:
        
        {formatted_data}
        """
        messages.append({"role": "system", "content": data_message})
        
        # Get response from OpenAI
        response = await self.generate_response(messages, temperature=0.5, max_tokens=2000)
        
        # Add the response to conversation history
        self.add_to_conversation(session_id, "assistant", response)
        
        return response
    
    def _format_data_for_prompt(self, data, query=None):
        """Format the data in a readable way for the prompt"""
        formatted_text = ""
        
        # Check for cryptocurrency data from Polygon.io
        crypto_data = {}
        for key, value in data.items():
            if "_price" in key and "error" not in value and value.get("is_cryptocurrency", False):
                ticker = value.get("crypto_ticker", key.split("_")[0])
                if "results" in value and value["results"]:
                    result = value["results"][0]
                    crypto_data[ticker] = {
                        "close": result.get('c', 'N/A'),
                        "open": result.get('o', 'N/A'),
                        "high": result.get('h', 'N/A'),
                        "low": result.get('l', 'N/A'),
                        "volume": result.get('v', 'N/A'),
                        "timestamp": result.get('t', 'N/A'),
                        "trades": result.get('n', 'N/A'),
                        "source": "Polygon.io"
                    }
        
        # Add Polygon.io cryptocurrency data at the top if available
        if crypto_data:
            formatted_text += "## Cryptocurrency Price Data from Polygon.io\n"
            for ticker, price_data in crypto_data.items():
                formatted_text += f"### {ticker} Current Price\n"
                formatted_text += f"- Current Price: ${price_data['close']}\n"
                formatted_text += f"- 24h Open: ${price_data['open']}\n"
                formatted_text += f"- 24h High: ${price_data['high']}\n"
                formatted_text += f"- 24h Low: ${price_data['low']}\n"
                formatted_text += f"- 24h Volume: {price_data['volume']:,} units\n"
                formatted_text += f"- Number of Trades: {price_data['trades']:,}\n"
                
                # Calculate price change and percentage
                if price_data['close'] != 'N/A' and price_data['open'] != 'N/A':
                    change = float(price_data['close']) - float(price_data['open'])
                    change_percent = (change / float(price_data['open'])) * 100 if float(price_data['open']) != 0 else 0
                    direction = "up" if change > 0 else "down"
                    formatted_text += f"- 24h Change: {direction} ${abs(change):.2f} ({abs(change_percent):.2f}%)\n"
                
                formatted_text += f"- Data Source: {price_data['source']}\n\n"
                
                # Add special instruction for cryptocurrency data
                formatted_text += "IMPORTANT: When responding to cryptocurrency price queries, ALWAYS include the Polygon.io price data above as one of the primary sources in your response.\n\n"
        
        # Add Perplexity content if available - ENHANCED VERSION
        for key, value in data.items():
            if key in ["perplexity_sonar", "perplexity_deep_research"] and "error" not in value:
                if "choices" in value and len(value["choices"]) > 0:
                    # Pass the FULL content without truncation or reformatting
                    content = value["choices"][0]["message"]["content"]
                    source_type = "Perplexity Sonar" if key == "perplexity_sonar" else "Perplexity Deep Research"
                    formatted_text += f"## Complete {source_type} Results\n"
                    formatted_text += content + "\n\n"
                    
                    # Add citations if available
                    if "citations" in value:
                        formatted_text += "### Sources:\n"
                        for i, citation in enumerate(value["citations"]):
                            formatted_text += f"[{i+1}] {citation}\n"
                        formatted_text += "\n"
        
        # Add stock price data with enhanced details
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
            formatted_text += "## Stock Price Data from Polygon.io\n"
            for ticker, price_data in stock_price_data.items():
                formatted_text += f"### {ticker} Stock Price\n"
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
        
        # Add news data with enhanced details
        news_data = {}
        for key, value in data.items():
            if "_news" in key and "error" not in value:
                ticker = key.split("_")[0]
                if "results" in value:
                    news_data[ticker] = value["results"][:5]  # Get top 5 news items
        
        if news_data:
            formatted_text += "## Recent News\n"
            for ticker, news_items in news_data.items():
                formatted_text += f"### {ticker} Recent News\n"
                for i, news in enumerate(news_items):
                    formatted_text += f"#### {news.get('title', 'No title')}\n"
                    formatted_text += f"- Published: {news.get('published_utc', 'N/A')}\n"
                    if news.get('description'):
                        formatted_text += f"- Summary: {news.get('description')}\n"
                    if news.get('article_url'):
                        formatted_text += f"- URL: {news.get('article_url')}\n"
                    formatted_text += "\n"
        
        # Add financial data with enhanced details
        financial_data = {}
        for key, value in data.items():
            if "_financials" in key and "error" not in value:
                ticker = key.split("_")[0]
                if "financials" in value:
                    financial_data[ticker] = value["financials"]
        
        if financial_data:
            formatted_text += "## Financial Statements\n"
            for ticker, financials in financial_data.items():
                formatted_text += f"### {ticker} Financial Data\n"
                formatted_text += json.dumps(financials, indent=2) + "\n\n"
        
        # Add insider trades data
        insider_data = {}
        for key, value in data.items():
            if "_insider_trades" in key and "error" not in value:
                ticker = key.split("_")[0]
                if "results" in value:
                    insider_data[ticker] = value["results"][:5]  # Get top 5 insider trades
        
        if insider_data:
            formatted_text += "## Insider Trading Activity\n"
            for ticker, trades in insider_data.items():
                formatted_text += f"### {ticker} Insider Trades\n"
                for trade in trades:
                    formatted_text += f"- Name: {trade.get('name', 'Unknown')}\n"
                    formatted_text += f"- Title: {trade.get('title', 'Unknown')}\n"
                    formatted_text += f"- Shares: {trade.get('shares', 'N/A')}\n"
                    formatted_text += f"- Value: ${trade.get('value', 'N/A')}\n"
                    formatted_text += f"- Date: {trade.get('date', 'N/A')}\n\n"
        
        # Add SEC filings data
        sec_data = {}
        for key, value in data.items():
            if "_sec_filings" in key and "error" not in value:
                ticker = key.split("_")[0]
                if "filings" in value:
                    sec_data[ticker] = value["filings"][:5]  # Get top 5 SEC filings
        
        if sec_data:
            formatted_text += "## SEC Filings\n"
            for ticker, filings in sec_data.items():
                formatted_text += f"### {ticker} SEC Filings\n"
                for filing in filings:
                    formatted_text += f"- Form: {filing.get('form', 'Unknown')}\n"
                    formatted_text += f"- Filed Date: {filing.get('filed_date', 'N/A')}\n"
                    formatted_text += f"- Description: {filing.get('description', 'N/A')}\n\n"
        
        return formatted_text 