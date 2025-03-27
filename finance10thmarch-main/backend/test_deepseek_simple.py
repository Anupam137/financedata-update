import asyncio
import os
import httpx
from dotenv import load_dotenv

async def test_deepseek_simple():
    """
    Test the DeepSeek integration with a simple query to avoid rate limits
    """
    print("Testing DeepSeek Integration (Simple)")
    print("===================================\n")
    
    # Force reload of environment variables
    load_dotenv(override=True)
    
    # Get API key from environment
    api_key = os.getenv("TOGETHER_API_KEY", "")
    
    # Print a masked version of the API key for debugging
    masked_key = api_key[:5] + "..." + api_key[-5:] if len(api_key) > 10 else "Not set properly"
    print(f"Using API key: {masked_key}")
    
    # Create a simple test message
    messages = [
        {"role": "system", "content": "You are a financial analyst. Keep your response brief and to the point."},
        {"role": "user", "content": "What is the current state of Tesla's stock?"}
    ]
    
    # Call the Together.ai API
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-ai/DeepSeek-R1",
        "messages": messages,
        "max_tokens": 100,  # Keep this small to avoid rate limits
        "temperature": 0.7,
        "stream": False
    }
    
    print(f"Using model: {payload['model']}")
    print("Sending request to Together.ai API...")
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                "https://api.together.xyz/v1/chat/completions",
                json=payload,
                headers=headers,
                timeout=60.0
            )
            response.raise_for_status()
            result = response.json()
            
            print("\nAPI Response:")
            print("============\n")
            if "choices" in result and len(result["choices"]) > 0:
                print(result["choices"][0]["message"]["content"])
            else:
                print("No content in response")
                print(f"Full response: {result}")
    except Exception as e:
        print(f"Error with API call: {e}")

if __name__ == "__main__":
    asyncio.run(test_deepseek_simple()) 