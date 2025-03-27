import os
import httpx
import json
import asyncio
from dotenv import load_dotenv
from pathlib import Path

async def test_deepseek_v3_connection():
    # Load environment variables from backend/.env
    backend_env_path = Path("backend/.env")
    if not backend_env_path.exists():
        # Try relative path if running from within backend directory
        backend_env_path = Path(".env")
    
    load_dotenv(dotenv_path=backend_env_path)
    
    # Get API key
    api_key = os.getenv("TOGETHER_API_KEY", "")
    if not api_key:
        print(f"Error: TOGETHER_API_KEY not found in environment variables. Checked path: {backend_env_path.absolute()}")
        return
    
    # Mask API key for display
    masked_key = api_key[:5] + "..." + api_key[-5:] if len(api_key) > 10 else "Not set properly"
    print(f"Using API key: {masked_key}")
    
    # API endpoint
    base_url = "https://api.together.xyz/v1/chat/completions"
    
    # Simple test message
    messages = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Hello, this is a test message to check if the DeepSeek V3 API connection is working. Please respond with a short confirmation."}
    ]
    
    # Prepare the API request
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    payload = {
        "model": "deepseek-ai/DeepSeek-V3",
        "messages": messages,
        "temperature": 0.7,
        "top_p": 0.7,
        "max_tokens": 100,
        "stream": False
    }
    
    print("Sending test request to DeepSeek V3 API...")
    
    try:
        # Make the API call
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.post(
                base_url,
                headers=headers,
                json=payload
            )
            
            # Check if the request was successful
            response.raise_for_status()
            
            # Parse the response
            result = response.json()
            
            # Extract the generated text
            if "choices" in result and len(result["choices"]) > 0:
                generated_text = result["choices"][0]["message"]["content"]
                print("\nAPI Connection Test Successful!")
                print(f"Response: {generated_text}")
                
                # Print additional response details
                print("\nResponse Details:")
                print(f"Model: {result.get('model', 'N/A')}")
                print(f"Usage - Prompt Tokens: {result.get('usage', {}).get('prompt_tokens', 'N/A')}")
                print(f"Usage - Completion Tokens: {result.get('usage', {}).get('completion_tokens', 'N/A')}")
                print(f"Usage - Total Tokens: {result.get('usage', {}).get('total_tokens', 'N/A')}")
            else:
                print("Error: Unexpected response format")
                print(f"Full response: {json.dumps(result, indent=2)}")
                
    except httpx.HTTPStatusError as e:
        print(f"HTTP Error: {e.response.status_code} - {e.response.text}")
    except httpx.RequestError as e:
        print(f"Request Error: {str(e)}")
    except Exception as e:
        print(f"Unexpected Error: {str(e)}")

# Run the test
if __name__ == "__main__":
    asyncio.run(test_deepseek_v3_connection()) 