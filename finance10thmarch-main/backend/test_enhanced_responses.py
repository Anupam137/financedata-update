import asyncio
import json
import os
from dotenv import load_dotenv
from app.services.openai_service import OpenAIService
from app.services.perplexity_service import PerplexityService
from app.services.polygon_service import PolygonService

# Load environment variables
load_dotenv()

async def test_enhanced_responses():
    """Test the enhanced response generation with various queries"""
    # Initialize services
    openai_service = OpenAIService()
    perplexity_service = PerplexityService()
    polygon_service = PolygonService()
    
    # Define test cases
    test_cases = [
        {
            "query": "What is the current price of TSLA?",
            "description": "Simple stock price query"
        },
        {
            "query": "Compare the market sentiment for Apple and Google",
            "description": "Market sentiment comparison"
        },
        {
            "query": "Compare Tesla and Ford stock prices and market sentiment",
            "description": "Complex query with stock prices and sentiment"
        }
    ]
    
    # Run each test case
    for i, case in enumerate(test_cases):
        query = case["query"]
        print(f"\n{'='*80}")
        print(f"TEST CASE {i+1}: {case['description']}")
        print(f"QUERY: {query}")
        print(f"{'='*80}")
        
        # Step 1: Analyze the query
        print("\nSTEP 1: Analyzing query...")
        api_plan = await openai_service.analyze_query(query)
        print(f"API Plan: {json.dumps(api_plan, indent=2)}")
        
        # Step 2: Collect data based on API plan
        print("\nSTEP 2: Collecting data...")
        collected_data = {}
        
        # Get stock price data if needed
        if api_plan.get("need_stock_price", False):
            tickers = api_plan.get("tickers", [])
            for ticker in tickers:
                print(f"Fetching stock price for {ticker}...")
                price_data = await polygon_service.get_stock_price(ticker)
                collected_data[f"{ticker}_price"] = price_data
        
        # Get sentiment data if needed
        if api_plan.get("need_perplexity_sonar", False):
            print("Fetching sentiment data from Perplexity Sonar...")
            sentiment_data = await perplexity_service.get_sonar_response(query)
            collected_data["perplexity_sonar"] = sentiment_data
        
        # Print collected data summary
        print("\nCollected Data Summary:")
        for key in collected_data:
            if "_price" in key and "results" in collected_data[key]:
                ticker = key.split("_")[0]
                price = collected_data[key]["results"][0]["c"] if collected_data[key]["results"] else "N/A"
                print(f"- {ticker} Price: ${price}")
            elif key == "perplexity_sonar":
                if "choices" in collected_data[key]:
                    content_length = len(collected_data[key]["choices"][0]["message"]["content"])
                    print(f"- Perplexity Sonar: {content_length} characters of content")
                    print(f"- First 200 characters: {collected_data[key]['choices'][0]['message']['content'][:200]}...")
        
        # Step 3: Format data for prompt
        print("\nSTEP 3: Formatting data for prompt...")
        formatted_data = openai_service._format_data_for_prompt(collected_data, query)
        print(f"Formatted data length: {len(formatted_data)} characters")
        print(f"First 500 characters of formatted data:\n{formatted_data[:500]}...")
        
        # Step 4: Generate financial insight
        print("\nSTEP 4: Generating financial insight...")
        response = await openai_service.generate_financial_insight(query, collected_data)
        
        # Print the final response
        print("\nFINAL RESPONSE:")
        print(f"{response}")

if __name__ == "__main__":
    asyncio.run(test_enhanced_responses()) 