import asyncio
import json
from app.services.openai_service import OpenAIService
from app.services.perplexity_service import PerplexityService

async def test_enhanced_response():
    # Initialize services
    openai_service = OpenAIService()
    perplexity_service = PerplexityService()
    
    # Test query with more explicit market sentiment focus
    query = "How does Microsoft's market sentiment compare to Amazon's? Include analyst ratings, stock performance, and investor perception."
    print(f"Query: '{query}'")
    
    # Step 1: Get API plan from OpenAI
    print("\n1. Getting API plan from OpenAI...")
    api_plan = await openai_service.analyze_query(query)
    print(f"API Plan: {json.dumps(api_plan, indent=2)}")
    
    # Step 2: Call Perplexity Sonar
    print("\n2. Calling Perplexity Sonar...")
    sonar_result = await perplexity_service.sonar_search(query)
    print(f"Perplexity Sonar Response Status: {'Success' if 'choices' in sonar_result else 'Failed'}")
    
    # Step 3: Generate final response with our enhanced method
    print("\n3. Generating final response with enhanced OpenAI service...")
    api_results = {"perplexity_sonar": sonar_result}
    
    final_response = await openai_service.generate_financial_insight(query, api_results)
    print(f"\nFinal Response:\n{final_response}")

if __name__ == "__main__":
    asyncio.run(test_enhanced_response()) 