import re
from typing import List, Dict, Any, Tuple, Optional
from app.utils.sanitizer import sanitize_text

# Patterns for simple queries
PRICE_PATTERNS = [
    r"(?:what(?:'s| is) (?:the )?(?:current |latest )?(?:stock )?price (?:of |for )?)([A-Z]{1,5})",
    r"(?:how much (?:is |does )?)([A-Z]{1,5})(?: cost| trading for| worth)",
    r"([A-Z]{1,5}) (?:stock )?price",
    r"price (?:of |for )([A-Z]{1,5})"
]

NEWS_PATTERNS = [
    r"(?:what(?:'s| is) (?:the )?(?:latest |recent )?news (?:on |about |for )?)([A-Z]{1,5})",
    r"([A-Z]{1,5}) (?:latest |recent )?news",
    r"news (?:on |about |for )([A-Z]{1,5})"
]

FINANCIALS_PATTERNS = [
    r"(?:what (?:are|is) (?:the )?(?:latest |recent )?financials (?:of |for )?)([A-Z]{1,5})",
    r"([A-Z]{1,5}) (?:financials|financial statements|balance sheet|income statement)",
    r"financials (?:of |for )([A-Z]{1,5})"
]

INSIDER_PATTERNS = [
    r"(?:what (?:are|is) (?:the )?(?:latest |recent )?insider trades (?:of |for )?)([A-Z]{1,5})",
    r"([A-Z]{1,5}) (?:insider trades|insider activity)",
    r"insider trades (?:of |for )([A-Z]{1,5})"
]

def extract_ticker_symbols(query: str) -> List[str]:
    """
    Extract potential ticker symbols from a query
    
    Args:
        query (str): User query
        
    Returns:
        List[str]: List of potential ticker symbols
    """
    # Sanitize the input query
    query = sanitize_text(query)
    
    # Look for uppercase words that might be tickers (1-5 letters)
    potential_tickers = re.findall(r'\b[A-Z]{1,5}\b', query)
    
    # Filter out common English words that might be mistaken for tickers
    common_words = {"I", "A", "AN", "THE", "AND", "OR", "FOR", "TO", "IN", "ON", "AT", "BY", "OF"}
    filtered_tickers = [ticker for ticker in potential_tickers if ticker not in common_words]
    
    return filtered_tickers

def is_simple_query(query: str) -> Tuple[bool, Optional[str], Optional[str]]:
    """
    Determine if a query is simple enough to bypass LLM analysis
    
    Args:
        query (str): User query
        
    Returns:
        Tuple[bool, Optional[str], Optional[str]]: 
            - Whether it's a simple query
            - The type of query ('price', 'news', 'financials', 'insider')
            - The ticker symbol
    """
    # Sanitize the input query
    query = sanitize_text(query.strip())
    
    # Check price patterns
    for pattern in PRICE_PATTERNS:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            return True, 'price', sanitize_text(match.group(1))
    
    # Check news patterns
    for pattern in NEWS_PATTERNS:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            return True, 'news', sanitize_text(match.group(1))
    
    # Check financials patterns
    for pattern in FINANCIALS_PATTERNS:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            return True, 'financials', sanitize_text(match.group(1))
    
    # Check insider trades patterns
    for pattern in INSIDER_PATTERNS:
        match = re.search(pattern, query, re.IGNORECASE)
        if match:
            return True, 'insider', sanitize_text(match.group(1))
    
    return False, None, None

def get_fast_path_response(query_type: str, ticker: str, data: Dict[str, Any]) -> str:
    """
    Generate a fast-path response for simple queries
    
    Args:
        query_type (str): Type of query ('price', 'news', 'financials', 'insider')
        ticker (str): Ticker symbol
        data (Dict[str, Any]): Data from API
        
    Returns:
        str: Formatted response
    """
    # Sanitize inputs
    query_type = sanitize_text(query_type)
    ticker = sanitize_text(ticker)
    
    if query_type == 'price':
        if "results" in data and data["results"]:
            result = data["results"][0]
            close_price = result.get('c', 'N/A')
            open_price = result.get('o', 'N/A')
            high = result.get('h', 'N/A')
            low = result.get('l', 'N/A')
            volume = result.get('v', 'N/A')
            
            # Calculate change and percentage
            if close_price != 'N/A' and open_price != 'N/A':
                change = close_price - open_price
                change_percent = (change / open_price) * 100 if open_price != 0 else 0
                change_str = f"{change:.2f} ({change_percent:.2f}%)"
                change_direction = "up" if change > 0 else "down"
            else:
                change_str = "N/A"
                change_direction = "unchanged"
            
            return sanitize_text(f"""
# {ticker} Stock Price

The current price of {ticker} is **${close_price:.2f}**, {change_direction} {change_str} from the opening price.

**Today's Trading Range:**
- Open: ${open_price:.2f}
- High: ${high:.2f}
- Low: ${low:.2f}
- Volume: {volume:,}

*Data provided by Polygon.io*
""")
        else:
            return sanitize_text(f"Sorry, I couldn't find the current price for {ticker}.")
    
    elif query_type == 'news':
        if "results" in data and data["results"]:
            news_items = data["results"][:3]  # Get top 3 news items
            response = f"# Latest News for {ticker}\n\n"
            
            for item in news_items:
                title = sanitize_text(item.get('title', 'No title'))
                published = sanitize_text(item.get('published_utc', 'N/A'))
                url = sanitize_text(item.get('article_url', '#'))
                description = sanitize_text(item.get('description', 'No description available.'))
                
                response += f"## {title}\n"
                response += f"*Published: {published}*\n\n"
                response += f"{description[:200]}...\n\n"
                response += f"[Read more]({url})\n\n"
            
            response += "*Data provided by Polygon.io*"
            return sanitize_text(response)
        else:
            return sanitize_text(f"Sorry, I couldn't find any recent news for {ticker}.")
    
    elif query_type == 'financials':
        return sanitize_text(f"Here are the financial statements for {ticker}. This would typically include balance sheet, income statement, and cash flow data from FinancialDatasets.ai.")
    
    elif query_type == 'insider':
        return sanitize_text(f"Here are the recent insider trades for {ticker}. This would typically include information about executives buying or selling shares from FinancialDatasets.ai.")
    
    return sanitize_text(f"I have some information about {ticker}, but I'm not sure what specific details you're looking for.") 