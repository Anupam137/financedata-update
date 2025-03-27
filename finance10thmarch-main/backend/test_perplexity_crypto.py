import asyncio
import json
from app.services.perplexity_service import PerplexityService

async def test_perplexity_crypto():
    # Initialize services
    perplexity_service = PerplexityService()
    
    # Test query
    query = 'What is the price of Ethereum?'
    
    # Test Perplexity Sonar API for crypto price
    print(f"Testing Perplexity Sonar API for query: '{query}'")
    try:
        perplexity_response = await perplexity_service.sonar_search(query)
        print(f"Perplexity Sonar response: {json.dumps(perplexity_response, indent=2)}")
    except Exception as e:
        print(f"Error getting response from Perplexity Sonar: {e}")
    
    # Test Perplexity Deep Research API for crypto price
    print(f"\nTesting Perplexity Deep Research API for query: '{query}'")
    try:
        deep_research_response = await perplexity_service.deep_research(query)
        print(f"Perplexity Deep Research response: {json.dumps(deep_research_response, indent=2)}")
    except Exception as e:
        print(f"Error getting response from Perplexity Deep Research: {e}")
    
    print("\nTest completed!")

if __name__ == "__main__":
    asyncio.run(test_perplexity_crypto()) 