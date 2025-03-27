import asyncio
import json
import os
import httpx
from app.services.deepseek_service import DeepSeekService
from app.services.perplexity_service import PerplexityService
from app.services.polygon_service import PolygonService
from app.core.config import TOGETHER_API_KEY
from dotenv import load_dotenv

async def test_deepseek_integration():
    """
    Test the DeepSeek integration by simulating a query and API calls
    """
    print("Testing DeepSeek Integration")
    print("===========================\n")
    
    # Force reload of environment variables
    load_dotenv(override=True)
    
    # Debug: Print environment variables
    print(f"TOGETHER_API_KEY from config: {TOGETHER_API_KEY}")
    print(f"TOGETHER_API_KEY from env: {os.getenv('TOGETHER_API_KEY')}")
    print(f"Current working directory: {os.getcwd()}")
    print(f".env file exists: {os.path.exists('.env')}")
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            env_contents = f.read()
            together_line = next((line for line in env_contents.split('\n') if line.startswith('TOGETHER_API_KEY=')), None)
            if together_line:
                print(f"TOGETHER_API_KEY line in .env: {together_line}")
                
    # Try direct cURL-style call with the key from the .env file
    print("\nTrying direct call with key from .env file...")
    with open('.env', 'r') as f:
        env_contents = f.read()
        together_line = next((line for line in env_contents.split('\n') if line.startswith('TOGETHER_API_KEY=')), None)
        if together_line:
            key_from_file = together_line.split('=')[1].strip()
            print(f"Using key from file: {key_from_file[:5]}...{key_from_file[-5:]}")
            
            try:
                headers = {
                    "Authorization": f"Bearer {key_from_file}",
                    "Content-Type": "application/json"
                }
                
                payload = {
                    "model": "deepseek-ai/DeepSeek-R1",
                    "messages": [{"role": "user", "content": "Hello, can you help me with a simple test?"}],
                    "max_tokens": 100,
                    "temperature": 0.7,
                    "stream": False
                }
                
                async with httpx.AsyncClient() as client:
                    response = await client.post(
                        "https://api.together.xyz/v1/chat/completions",
                        json=payload,
                        headers=headers,
                        timeout=60.0
                    )
                    response.raise_for_status()
                    result = response.json()
                    
                    print("\nDirect API Response with key from file:")
                    print("=====================================\n")
                    if "choices" in result and len(result["choices"]) > 0:
                        print(result["choices"][0]["message"]["content"])
                    else:
                        print("No content in response")
                        print(f"Full response: {result}")
            except Exception as e:
                print(f"Error with direct API call using key from file: {e}")
    
    # Initialize services
    deepseek_service = DeepSeekService()
    perplexity_service = PerplexityService()
    polygon_service = PolygonService()
    
    # Test query
    query = "Compare Tesla and Ford in terms of financial performance and stock growth"
    print(f"Query: '{query}'\n")
    
    # Collect data from APIs
    print("Collecting data from APIs...")
    
    # Call Perplexity Sonar
    print("Calling Perplexity Sonar...")
    sonar_result = await perplexity_service.sonar_search(query)
    
    # Call Perplexity Deep Research
    print("Calling Perplexity Deep Research...")
    deep_research_result = await perplexity_service.deep_research(query)
    
    # Get stock prices for Tesla and Ford
    print("Getting stock prices for TSLA and F...")
    tesla_price = await polygon_service.get_stock_price("TSLA")
    ford_price = await polygon_service.get_stock_price("F")
    
    # Get news for Tesla and Ford
    print("Getting news for TSLA and F...")
    tesla_news = await polygon_service.get_company_news("TSLA")
    ford_news = await polygon_service.get_company_news("F")
    
    # Combine all data
    api_results = {
        "perplexity_sonar": sonar_result,
        "perplexity_deep_research": deep_research_result,
        "TSLA_price": tesla_price,
        "F_price": ford_price,
        "TSLA_news": tesla_news,
        "F_news": ford_news
    }
    
    # Call DeepSeek with the collected data
    print("\nCalling DeepSeek with collected data...")
    deepseek_response = await deepseek_service.generate_financial_insight(query, api_results)
    
    # Print the response
    print("\nDeepSeek Response:")
    print("=================\n")
    print(deepseek_response)

if __name__ == "__main__":
    asyncio.run(test_deepseek_integration()) 