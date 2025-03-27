import asyncio
import json
from app.services.openai_service import OpenAIService
from app.services.polygon_service import PolygonService
from app.services.deepseek_service import DeepSeekService

async def test_crypto_fix():
    # Initialize services
    openai_service = OpenAIService()
    polygon_service = PolygonService()
    deepseek_service = DeepSeekService()
    
    # Test crypto query analysis with the updated OpenAI service
    print('Testing crypto query analysis with updated service...')
    crypto_query = 'What is the latest price of Bitcoin?'
    crypto_plan = await openai_service.analyze_query(crypto_query, 'test_session')
    print(json.dumps(crypto_plan, indent=2))
    
    # Check if is_crypto_query flag is set
    is_crypto_query = crypto_plan.get("is_crypto_query", False)
    print(f"Is crypto query flag set: {is_crypto_query}")
    
    # Process the tickers as in the search route
    for i, ticker in enumerate(crypto_plan.get("tickers", [])):
        if is_crypto_query or ticker.upper() in ["BTC", "ETH", "XRP", "DOGE", "SOL", "ADA"]:
            crypto_plan["tickers"][i] = ticker.upper()
            crypto_plan["is_crypto"] = True
    
    print(f"Processed tickers: {crypto_plan.get('tickers', [])}")
    print(f"Is crypto flag set: {crypto_plan.get('is_crypto', False)}")
    
    # Test formatted ticker for Polygon API
    if crypto_plan.get("tickers") and crypto_plan.get("is_crypto", False):
        ticker = crypto_plan["tickers"][0].upper()
        formatted_ticker = f"X:{ticker}-USD"
        print(f"Formatted ticker for Polygon API: {formatted_ticker}")
        
        # Try to fetch data with the formatted ticker
        try:
            print(f"Attempting to fetch data with formatted ticker: {formatted_ticker}")
            crypto_price = await polygon_service.get_stock_price(formatted_ticker)
            print(f"Crypto price data: {json.dumps(crypto_price, indent=2)[:500]}...")
        except Exception as e:
            print(f"Error getting crypto price: {e}")
    
    # Test the updated DeepSeek prompt
    print("\nTesting updated DeepSeek prompt...")
    # Create sample data with Bitcoin price
    mock_data = {
        "perplexity_sonar": {
            "choices": [
                {
                    "message": {
                        "content": "Bitcoin is currently trading at approximately $82,450. The market sentiment is bearish, with the Fear & Greed Index at 20, indicating 'Extreme Fear'."
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
        }
    }
    
    # Format the data for DeepSeek
    formatted_data = deepseek_service._format_data_for_prompt_simplified(mock_data)
    print(f"Formatted data for DeepSeek: {formatted_data[:500]}...")
    
    print("\nTest completed successfully!")

if __name__ == "__main__":
    asyncio.run(test_crypto_fix()) 