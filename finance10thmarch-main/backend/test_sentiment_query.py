import asyncio
import json
from app.services.openai_service import OpenAIService
from app.services.perplexity_service import PerplexityService

async def test_sentiment_comparison_query():
    # Initialize services
    openai_service = OpenAIService()
    perplexity_service = PerplexityService()
    
    # Test query
    query = "How does Microsoft's sentiment compare to Amazon's"
    print(f"Query: '{query}'")
    
    # Step 1: Get API plan from OpenAI
    print("\n1. Getting API plan from OpenAI...")
    api_plan = await openai_service.analyze_query(query)
    print(f"API Plan: {json.dumps(api_plan, indent=2)}")
    
    # Step 2: Call Perplexity Sonar if indicated in the plan
    if api_plan.get("call_perplexity_sonar", False):
        print("\n2. Calling Perplexity Sonar...")
        sonar_result = await perplexity_service.sonar_search(query)
        print(f"Perplexity Sonar Response Status: {'Success' if 'choices' in sonar_result else 'Failed'}")
        
        # Print a sample of the response
        if 'choices' in sonar_result and len(sonar_result['choices']) > 0:
            content = sonar_result['choices'][0]['message']['content']
            print(f"\nSample of Perplexity Sonar content (first 300 chars):\n{content[:300]}...")
        else:
            print(f"Error or unexpected response format: {sonar_result}")
    else:
        print("\n2. API plan did not indicate to call Perplexity Sonar")
    
    # Step 3: Generate final response
    print("\n3. Generating final response with OpenAI...")
    api_results = {}
    
    if api_plan.get("call_perplexity_sonar", False):
        api_results["perplexity_sonar"] = sonar_result
    
    final_response = await openai_service.generate_financial_insight(query, api_results)
    print(f"\nFinal Response (first 500 chars):\n{final_response[:500]}...")

if __name__ == "__main__":
    asyncio.run(test_sentiment_comparison_query()) 