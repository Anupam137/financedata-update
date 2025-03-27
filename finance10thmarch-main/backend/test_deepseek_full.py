import asyncio
import os
from dotenv import load_dotenv
from app.services.deepseek_service import DeepSeekService

async def test_deepseek_full():
    """
    Test the DeepSeek service with a simple query
    """
    print("Testing DeepSeek Service (Full)")
    print("==============================\n")
    
    # Force reload of environment variables
    load_dotenv(override=True)
    
    # Initialize the DeepSeek service
    deepseek_service = DeepSeekService()
    
    # Create a simple test query
    query = "What is the current state of Tesla's stock?"
    print(f"Query: '{query}'\n")
    
    # Create a minimal data set
    data = {
        "perplexity_sonar": {
            "choices": [
                {
                    "message": {
                        "content": "Tesla (TSLA) stock has been volatile in recent months. The company has faced challenges with delivery numbers and increasing competition in the electric vehicle market. However, they continue to innovate with new products and expand their manufacturing capacity."
                    }
                }
            ]
        },
        "TSLA_price": {
            "results": [
                {
                    "c": 235.45,
                    "o": 230.12,
                    "h": 237.80,
                    "l": 229.75,
                    "v": 12500000,
                    "n": 125000,
                    "t": 1689350400000
                }
            ]
        },
        "TSLA_news": {
            "results": [
                {
                    "title": "Tesla Announces New Battery Technology",
                    "description": "Tesla has unveiled a new battery technology that could significantly increase range and reduce costs.",
                    "published_utc": "2023-07-14T12:00:00Z",
                    "article_url": "https://example.com/tesla-battery"
                },
                {
                    "title": "Tesla Q2 Deliveries Beat Expectations",
                    "description": "Tesla delivered more vehicles than expected in the second quarter, despite market challenges.",
                    "published_utc": "2023-07-10T14:30:00Z",
                    "article_url": "https://example.com/tesla-deliveries"
                }
            ]
        }
    }
    
    # Call the DeepSeek service
    print("Calling DeepSeek service...")
    response = await deepseek_service.generate_financial_insight(query, data)
    
    # Print the response
    print("\nDeepSeek Response:")
    print("=================\n")
    print(response)

if __name__ == "__main__":
    asyncio.run(test_deepseek_full()) 