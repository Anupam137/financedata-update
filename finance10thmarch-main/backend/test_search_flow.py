import asyncio
from app.utils.query_analyzer import is_simple_query, get_fast_path_response
from app.services.polygon_service import PolygonService
from app.core.config import ENABLE_FAST_PATH

async def test_search_flow():
    # Test query
    query = "What is the price of TSLA right now"
    
    print(f"Query: '{query}'")
    print(f"Fast path enabled: {ENABLE_FAST_PATH}")
    
    # Step 1: Check if it's a simple query
    is_simple, query_type, ticker = is_simple_query(query)
    print(f"Is simple query: {is_simple}")
    print(f"Query type: {query_type}")
    print(f"Extracted ticker: {ticker}")
    
    # Step 2: If it's a simple query and fast path is enabled, get data directly
    if is_simple and ENABLE_FAST_PATH:
        print("Using fast path to get data directly from Polygon.io")
        
        # Initialize Polygon service
        polygon_service = PolygonService()
        
        # Get stock price data
        if query_type == 'price' and ticker:
            print(f"Getting stock price for {ticker}")
            data = await polygon_service.get_stock_price(ticker)
            print(f"Polygon API response: {data}")
            
            # Generate fast path response
            response = get_fast_path_response(query_type, ticker, data)
            print("\nGenerated response:")
            print(response)
        else:
            print(f"Query type '{query_type}' or ticker '{ticker}' not suitable for fast path")
    else:
        print("Not using fast path, would use OpenAI to analyze query")

if __name__ == "__main__":
    asyncio.run(test_search_flow()) 