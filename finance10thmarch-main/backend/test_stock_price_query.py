import asyncio
import json
from app.services.openai_service import OpenAIService
from app.services.polygon_service import PolygonService

async def test_stock_price_query():
    # Initialize services
    openai_service = OpenAIService()
    polygon_service = PolygonService()
    
    # Test queries - both with ticker symbols and company names
    queries = [
        "What is the price of TSLA right now?",
        "How much is Tesla stock?",
        "Current price of Microsoft",
        "AAPL stock price"
    ]
    
    for query in queries:
        print(f"\nTesting query: '{query}'")
        
        # Step 1: Get API plan from OpenAI
        print("1. Getting API plan from OpenAI...")
        api_plan = await openai_service.analyze_query(query)
        print(f"API Plan: {json.dumps(api_plan, indent=2)}")
        
        # Step 2: Check if need_stock_price is set to true
        if api_plan.get("need_stock_price", False):
            print("✅ Success: need_stock_price is set to true")
            
            # Step 3: Extract tickers
            tickers = api_plan.get("tickers", [])
            if tickers:
                print(f"✅ Success: Tickers identified: {tickers}")
                
                # Step 4: Test Polygon.io API call for the first ticker
                ticker = tickers[0]
                print(f"3. Testing Polygon.io API call for {ticker}...")
                stock_data = await polygon_service.get_stock_price(ticker)
                
                if "error" not in stock_data:
                    print(f"✅ Success: Polygon.io returned data for {ticker}")
                    if "results" in stock_data and stock_data["results"]:
                        price = stock_data["results"][0].get("c", "N/A")
                        print(f"Current price of {ticker}: ${price}")
                    else:
                        print("❌ Error: No results in Polygon.io response")
                else:
                    print(f"❌ Error: Polygon.io API call failed: {stock_data['error']}")
            else:
                print("❌ Error: No tickers identified in the query")
        else:
            print("❌ Error: need_stock_price is not set to true")

if __name__ == "__main__":
    asyncio.run(test_stock_price_query()) 