import asyncio
import json
from app.services.deepseek_service import DeepSeekService

async def test_deepseek_with_manual_crypto_data():
    # Initialize DeepSeek service
    deepseek_service = DeepSeekService()
    
    # Create a query about Bitcoin
    query = "What is the latest price and news on Bitcoin, include the market sentiment around it"
    
    # Create mock data with current Bitcoin price
    mock_data = {
        "perplexity_sonar": {
            "choices": [
                {
                    "message": {
                        "content": "Bitcoin is currently trading at approximately $82,450. The market sentiment is bearish, with the Fear & Greed Index at 20, indicating 'Extreme Fear'. Recent developments include Trump's Bitcoin reserve plan and technical analysis from Peter Brandt showing a bearish outlook based on a double-top pattern."
                    }
                }
            ]
        },
        "BTC_price": {
            "ticker": "BTC",
            "results": [
                {
                    "c": 82450,
                    "o": 82308,
                    "h": 82450,
                    "l": 82308,
                    "v": 1500000,
                    "t": 1687654321000,
                    "n": 50000
                }
            ]
        },
        "BTC_news": {
            "results": [
                {
                    "title": "Bitcoin Falls Amid Market Uncertainty",
                    "description": "Bitcoin has experienced a notable weekly decline of $13,561 as market sentiment turns bearish.",
                    "published_utc": "2023-06-25T12:00:00Z",
                    "article_url": "https://example.com/bitcoin-news-1"
                },
                {
                    "title": "Trump's Bitcoin Reserve Plan Impact",
                    "description": "The plan to establish a Bitcoin reserve funded by seized Bitcoin initially boosted optimism but later led to disappointment.",
                    "published_utc": "2023-06-24T10:30:00Z",
                    "article_url": "https://example.com/bitcoin-news-2"
                }
            ]
        }
    }
    
    # Call DeepSeek with the mock data
    print("Calling DeepSeek with manual Bitcoin data...")
    response = await deepseek_service.generate_financial_insight(query, mock_data)
    
    # Print the first part of the response
    print("\nDeepSeek Response (first 1000 chars):")
    print(response[:1000] + "..." if len(response) > 1000 else response)
    
    # Save the full response to a file
    with open("deepseek_bitcoin_response.txt", "w") as f:
        f.write(response)
    print("\nFull response saved to deepseek_bitcoin_response.txt")

if __name__ == "__main__":
    asyncio.run(test_deepseek_with_manual_crypto_data()) 