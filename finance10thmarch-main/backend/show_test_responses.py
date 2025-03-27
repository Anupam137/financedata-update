import asyncio
import json
from app.services.openai_service import OpenAIService
from app.services.perplexity_service import PerplexityService
from app.services.polygon_service import PolygonService

async def show_test_responses():
    # Initialize services
    openai_service = OpenAIService()
    perplexity_service = PerplexityService()
    polygon_service = PolygonService()
    
    # Test queries to run
    test_queries = [
        "What is the current price of TSLA?",
        "How much is Microsoft stock trading for?",
        "How does Apple's market sentiment compare to Google's?",
        "Compare Tesla and Ford stock prices and market sentiment"
    ]
    
    for i, query in enumerate(test_queries):
        print(f"\n{'=' * 80}")
        print(f"TEST QUERY {i+1}: '{query}'")
        print(f"{'=' * 80}")
        
        # Step 1: Get API plan from OpenAI
        print("\nAPI Plan:")
        api_plan = await openai_service.analyze_query(query)
        print(json.dumps(api_plan, indent=2))
        
        # Step 2: Make API calls based on the plan
        api_results = {}
        
        # Call Perplexity Sonar if needed
        if api_plan.get("call_perplexity_sonar", False):
            print("\nCalling Perplexity Sonar...")
            sonar_result = await perplexity_service.sonar_search(query)
            if "choices" in sonar_result and len(sonar_result["choices"]) > 0:
                print("Perplexity Sonar call successful")
                api_results["perplexity_sonar"] = sonar_result
            else:
                print(f"Perplexity Sonar API call failed")
        
        # Call Polygon.io for stock prices if needed
        if api_plan.get("need_stock_price", False):
            tickers = api_plan.get("tickers", [])
            if tickers:
                for ticker in tickers:
                    if len(ticker) <= 5 and ticker.isupper():  # Only use ticker symbols, not company names
                        print(f"\nCalling Polygon.io for {ticker}...")
                        stock_data = await polygon_service.get_stock_price(ticker)
                        if "error" not in stock_data:
                            print(f"Polygon.io call successful for {ticker}")
                            if "results" in stock_data and stock_data["results"]:
                                price = stock_data["results"][0].get("c", "N/A")
                                print(f"Current price: ${price}")
                                api_results[f"{ticker}_price"] = stock_data
                            else:
                                print("No results in Polygon.io response")
                        else:
                            print(f"Polygon.io API call failed: {stock_data['error']}")
            else:
                print("No tickers identified in the query")
        
        # Step 3: Generate final response
        print("\nGenerating final response...")
        final_response = await openai_service.generate_financial_insight(query, api_results)
        
        # Print the full response
        print("\nFULL RESPONSE:")
        print("-" * 80)
        print(final_response)
        print("-" * 80)
        
        # Add a separator between tests
        print("\n" + "=" * 80)
        print("END OF TEST")
        print("=" * 80 + "\n")

if __name__ == "__main__":
    asyncio.run(show_test_responses()) 