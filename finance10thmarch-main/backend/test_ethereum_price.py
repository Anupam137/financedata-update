import asyncio
import json
from app.services.openai_service import OpenAIService
from app.services.polygon_service import PolygonService
from app.services.perplexity_service import PerplexityService
from app.utils.query_analyzer import is_simple_query

async def test_ethereum_price_query():
    # Initialize services
    openai_service = OpenAIService()
    polygon_service = PolygonService()
    perplexity_service = PerplexityService()
    
    # Test query
    query = 'What is the price of Ethereum?'
    
    # Check if it's a simple query that can be handled by fast path
    print(f"Checking if '{query}' is a simple query...")
    simple_query_result = is_simple_query(query)
    print(f"Is simple query: {simple_query_result}")
    
    # Analyze query with OpenAI
    print("\nAnalyzing query with OpenAI...")
    query_plan = await openai_service.analyze_query(query, 'test_session')
    print(f"Query plan: {json.dumps(query_plan, indent=2)}")
    
    # Check if it's a crypto query
    is_crypto_query = query_plan.get("is_crypto_query", False)
    print(f"Is crypto query flag set: {is_crypto_query}")
    
    # Process the tickers as in the search route
    for i, ticker in enumerate(query_plan.get("tickers", [])):
        if is_crypto_query or ticker.upper() in ["BTC", "ETH", "XRP", "DOGE", "SOL", "ADA"]:
            query_plan["tickers"][i] = ticker.upper()
            query_plan["is_crypto"] = True
    
    print(f"Processed tickers: {query_plan.get('tickers', [])}")
    print(f"Is crypto flag set: {query_plan.get('is_crypto', False)}")
    
    # Test Polygon API for crypto price
    if query_plan.get("tickers") and query_plan.get("is_crypto", False):
        ticker = query_plan["tickers"][0].upper()
        formatted_ticker = f"X:{ticker}-USD"
        print(f"\nFormatted ticker for Polygon API: {formatted_ticker}")
        
        try:
            print(f"Attempting to fetch data with Polygon API using formatted ticker: {formatted_ticker}")
            crypto_price = await polygon_service.get_stock_price(formatted_ticker)
            print(f"Crypto price data from Polygon: {json.dumps(crypto_price, indent=2)}")
        except Exception as e:
            print(f"Error getting crypto price from Polygon: {e}")
    
    # Test Perplexity API for crypto price
    print("\nTesting Perplexity API for crypto price...")
    try:
        perplexity_response = await perplexity_service.search(query)
        print(f"Perplexity response: {json.dumps(perplexity_response, indent=2)}")
    except Exception as e:
        print(f"Error getting response from Perplexity: {e}")
    
    print("\nTest completed!")

if __name__ == "__main__":
    asyncio.run(test_ethereum_price_query()) 