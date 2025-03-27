import asyncio
import json
from app.services.openai_service import OpenAIService
from app.services.perplexity_service import PerplexityService
from app.services.polygon_service import PolygonService
from app.services.deepseek_service import DeepSeekService

async def test_apple_analysis():
    """
    Test the full flow with a query about Apple's stock performance
    """
    print("Testing full flow with query: 'Analyze Apple's stock performance over the past year and provide future outlook'")
    print("===========================================================================================\n")
    
    # Initialize services
    openai_service = OpenAIService()
    perplexity_service = PerplexityService()
    polygon_service = PolygonService()
    deepseek_service = DeepSeekService()
    
    # Step 1: Use OpenAI to analyze the query
    query = "Analyze Apple's stock performance over the past year and provide future outlook"
    print("Step 1: Analyzing query with OpenAI...")
    api_plan = await openai_service.analyze_query(query)
    
    print("\nAPI Plan from OpenAI:")
    print(json.dumps(api_plan, indent=2))
    
    # Step 2: Collect data from APIs
    print("\nStep 2: Collecting data from APIs...")
    api_results = {}
    
    # Call Perplexity Sonar
    if api_plan.get("call_perplexity_sonar", False):
        print("Calling Perplexity Sonar...")
        api_results["perplexity_sonar"] = await perplexity_service.sonar_search(query)
    
    # Get stock data for Apple if in tickers
    if "AAPL" in api_plan.get("tickers", []):
        print("Getting AAPL stock price...")
        api_results["AAPL_price"] = await polygon_service.get_stock_price("AAPL")
        
        print("Getting AAPL news...")
        api_results["AAPL_news"] = await polygon_service.get_company_news("AAPL")
    
    # Step 3: Call DeepSeek with the collected data
    print("\nStep 3: Calling DeepSeek with collected data...")
    deepseek_response = await deepseek_service.generate_financial_insight(query, api_results)
    
    # Print the response
    print("\nDeepSeek Response:")
    print("=================\n")
    print(deepseek_response)

if __name__ == "__main__":
    asyncio.run(test_apple_analysis()) 