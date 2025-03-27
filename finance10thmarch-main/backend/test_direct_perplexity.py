import asyncio
from app.services.perplexity_service import PerplexityService
import json

async def test_direct_perplexity_call():
    # Initialize Perplexity service
    perplexity_service = PerplexityService()
    
    # Test query
    query = "How does Microsoft's sentiment compare to Amazon's? Include analyst ratings, stock performance, and market sentiment."
    print(f"Query: '{query}'")
    
    # Make direct call to Perplexity Sonar
    print("\nCalling Perplexity Sonar directly...")
    sonar_result = await perplexity_service.sonar_search(query)
    
    # Check if the call was successful
    if 'choices' in sonar_result and len(sonar_result['choices']) > 0:
        print("Perplexity Sonar call successful!")
        
        # Extract and print the full content
        content = sonar_result['choices'][0]['message']['content']
        print("\nFull Perplexity Sonar Response:")
        print("=" * 80)
        print(content)
        print("=" * 80)
        
        # Print citations if available
        if 'citations' in sonar_result:
            print("\nCitations:")
            for i, citation in enumerate(sonar_result['citations']):
                print(f"{i+1}. {citation}")
    else:
        print(f"Error or unexpected response format: {json.dumps(sonar_result, indent=2)}")

if __name__ == "__main__":
    asyncio.run(test_direct_perplexity_call()) 