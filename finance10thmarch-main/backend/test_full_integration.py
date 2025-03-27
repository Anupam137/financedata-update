import asyncio
import json
from app.services.openai_service import OpenAIService
from app.services.perplexity_service import PerplexityService
from app.services.polygon_service import PolygonService

async def test_full_integration():
    # Initialize services
    openai_service = OpenAIService()
    perplexity_service = PerplexityService()
    polygon_service = PolygonService()
    
    # Test cases
    test_cases = [
        {
            "name": "Stock Price Query",
            "query": "What is the current price of TSLA?",
            "expected_apis": ["need_stock_price"]
        },
        {
            "name": "Company Name Stock Price Query",
            "query": "How much is Microsoft stock trading for?",
            "expected_apis": ["need_stock_price"]
        },
        {
            "name": "Market Sentiment Comparison",
            "query": "How does Apple's market sentiment compare to Google's?",
            "expected_apis": ["call_perplexity_sonar"]
        },
        {
            "name": "Complex Query with Price and Sentiment",
            "query": "Compare Tesla and Ford stock prices and market sentiment",
            "expected_apis": ["need_stock_price", "call_perplexity_sonar"]
        }
    ]
    
    for test_case in test_cases:
        print(f"\n{'=' * 80}")
        print(f"Testing: {test_case['name']}")
        print(f"Query: '{test_case['query']}'")
        print(f"{'=' * 80}")
        
        # Step 1: Get API plan from OpenAI
        print("\n1. Getting API plan from OpenAI...")
        api_plan = await openai_service.analyze_query(test_case['query'])
        print(f"API Plan: {json.dumps(api_plan, indent=2)}")
        
        # Step 2: Check if expected APIs are called
        all_expected_apis_called = True
        for expected_api in test_case['expected_apis']:
            if api_plan.get(expected_api, False):
                print(f"✅ Success: {expected_api} is set to true")
            else:
                print(f"❌ Error: {expected_api} is not set to true")
                all_expected_apis_called = False
        
        if not all_expected_apis_called:
            print("❌ Test failed: Not all expected APIs were called")
            continue
        
        # Step 3: Make API calls based on the plan
        api_results = {}
        
        # Call Perplexity Sonar if needed
        if api_plan.get("call_perplexity_sonar", False):
            print("\n2. Calling Perplexity Sonar...")
            sonar_result = await perplexity_service.sonar_search(test_case['query'])
            if "choices" in sonar_result and len(sonar_result["choices"]) > 0:
                print("✅ Success: Perplexity Sonar returned data")
                api_results["perplexity_sonar"] = sonar_result
            else:
                print(f"❌ Error: Perplexity Sonar API call failed")
        
        # Call Polygon.io for stock prices if needed
        if api_plan.get("need_stock_price", False):
            tickers = api_plan.get("tickers", [])
            if tickers:
                for ticker in tickers:
                    if len(ticker) <= 5 and ticker.isupper():  # Only use ticker symbols, not company names
                        print(f"\n2. Calling Polygon.io for {ticker}...")
                        stock_data = await polygon_service.get_stock_price(ticker)
                        if "error" not in stock_data:
                            print(f"✅ Success: Polygon.io returned data for {ticker}")
                            if "results" in stock_data and stock_data["results"]:
                                price = stock_data["results"][0].get("c", "N/A")
                                print(f"Current price of {ticker}: ${price}")
                                api_results[f"{ticker}_price"] = stock_data
                            else:
                                print("❌ Error: No results in Polygon.io response")
                        else:
                            print(f"❌ Error: Polygon.io API call failed: {stock_data['error']}")
            else:
                print("❌ Error: No tickers identified in the query")
        
        # Step 4: Generate final response
        print("\n3. Generating final response...")
        final_response = await openai_service.generate_financial_insight(test_case['query'], api_results)
        
        # Print a preview of the response
        preview_length = min(500, len(final_response))
        print(f"\nResponse Preview (first {preview_length} chars):")
        print(f"{final_response[:preview_length]}...")

if __name__ == "__main__":
    asyncio.run(test_full_integration()) 