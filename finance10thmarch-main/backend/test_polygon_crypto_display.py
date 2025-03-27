import asyncio
import json
import uuid
from app.services.openai_service import OpenAIService
from app.services.polygon_service import PolygonService
from app.services.perplexity_service import PerplexityService

async def test_polygon_crypto_display():
    # Initialize services
    openai_service = OpenAIService()
    polygon_service = PolygonService()
    perplexity_service = PerplexityService()
    
    # Test query
    query = 'What is the price of Ethereum?'
    session_id = str(uuid.uuid4())
    
    print(f"Testing search for query: '{query}'")
    
    # Step 1: Analyze query with OpenAI
    print("\nAnalyzing query with OpenAI...")
    api_plan = await openai_service.analyze_query(query, session_id)
    print(f"API plan: {json.dumps(api_plan, indent=2)}")
    
    # Step 2: Process crypto queries if detected
    is_crypto_query = api_plan.get("is_crypto_query", False)
    print(f"Is crypto query: {is_crypto_query}")
    
    # Process tickers
    for i, ticker in enumerate(api_plan.get("tickers", [])):
        if is_crypto_query or ticker.upper() in ["BTC", "ETH", "XRP", "DOGE", "SOL", "ADA"]:
            api_plan["tickers"][i] = ticker.upper()
            api_plan["is_crypto"] = True
    
    print(f"Processed tickers: {api_plan.get('tickers', [])}")
    print(f"Is crypto flag: {api_plan.get('is_crypto', False)}")
    
    # Step 3: Collect data from APIs
    api_results = {}
    
    # Get cryptocurrency price data from Polygon.io
    if api_plan.get("tickers") and api_plan.get("is_crypto", False):
        ticker = api_plan["tickers"][0].upper()
        print(f"\nGetting price data for {ticker} from Polygon.io...")
        
        try:
            crypto_price = await polygon_service.get_crypto_price(ticker)
            api_results[f"{ticker}_price"] = crypto_price
            print(f"Crypto price data from Polygon.io: {json.dumps(crypto_price, indent=2)}")
        except Exception as e:
            print(f"Error getting crypto price from Polygon.io: {e}")
    
    # Get Perplexity data
    print("\nGetting data from Perplexity Sonar...")
    try:
        perplexity_response = await perplexity_service.sonar_search(query)
        api_results["perplexity_sonar"] = perplexity_response
        print(f"Perplexity data retrieved successfully.")
    except Exception as e:
        print(f"Error getting response from Perplexity: {e}")
    
    # Step 4: Generate financial insight with OpenAI
    print("\nGenerating financial insight with OpenAI...")
    try:
        response = await openai_service.generate_financial_insight(query, api_results, session_id)
        print("\nGenerated Response:")
        print("=" * 80)
        print(response)
        print("=" * 80)
    except Exception as e:
        print(f"Error generating financial insight: {e}")
    
    print("\nTest completed!")

if __name__ == "__main__":
    asyncio.run(test_polygon_crypto_display()) 