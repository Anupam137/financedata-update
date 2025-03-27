import asyncio
import json
from app.services.openai_service import OpenAIService
from app.services.polygon_service import PolygonService
from app.services.deepseek_service import DeepSeekService

async def test_query_analysis():
    # Initialize services
    openai_service = OpenAIService()
    polygon_service = PolygonService()
    deepseek_service = DeepSeekService()
    
    # Test stock query analysis
    print('Testing stock query analysis...')
    stock_query = 'What is the latest price of Tesla stock?'
    stock_plan = await openai_service.analyze_query(stock_query, 'test_session')
    print(json.dumps(stock_plan, indent=2))
    
    # Test crypto query analysis
    print('\nTesting crypto query analysis...')
    crypto_query = 'What is the latest price of Bitcoin?'
    crypto_plan = await openai_service.analyze_query(crypto_query, 'test_session')
    print(json.dumps(crypto_plan, indent=2))
    
    # Test stock data collection
    print('\nTesting stock data collection...')
    if 'tickers' in stock_plan and stock_plan['tickers']:
        ticker = stock_plan['tickers'][0].upper()
        print(f"Collecting data for stock ticker: {ticker}")
        stock_price = await polygon_service.get_stock_price(ticker)
        print(f"Stock price data: {json.dumps(stock_price, indent=2)[:500]}...")
    
    # Test crypto data collection
    print('\nTesting crypto data collection...')
    if 'tickers' in crypto_plan and crypto_plan['tickers']:
        ticker = crypto_plan['tickers'][0].upper()
        print(f"Collecting data for crypto ticker: {ticker}")
        # Check if there's a specific crypto price method
        try:
            crypto_price = await polygon_service.get_crypto_price(ticker)
            print(f"Crypto price data: {json.dumps(crypto_price, indent=2)[:500]}...")
        except Exception as e:
            print(f"Error getting crypto price: {e}")
            print("Trying stock price method instead...")
            try:
                crypto_price = await polygon_service.get_stock_price(ticker)
                print(f"Using stock price method for crypto: {json.dumps(crypto_price, indent=2)[:500]}...")
            except Exception as e:
                print(f"Error using stock price method for crypto: {e}")
    
    # Test data formatting for DeepSeek
    print('\nTesting data formatting for DeepSeek...')
    # Create sample data dictionaries
    stock_data = {}
    if 'tickers' in stock_plan and stock_plan['tickers']:
        ticker = stock_plan['tickers'][0].upper()
        stock_data[f"{ticker}_price"] = await polygon_service.get_stock_price(ticker)
    
    crypto_data = {}
    if 'tickers' in crypto_plan and crypto_plan['tickers']:
        ticker = crypto_plan['tickers'][0].upper()
        try:
            crypto_data[f"{ticker}_price"] = await polygon_service.get_stock_price(ticker)
        except Exception as e:
            print(f"Error getting crypto price: {e}")
    
    # Format data for DeepSeek
    print("Stock data formatting:")
    stock_formatted = deepseek_service._format_data_for_prompt_simplified(stock_data)
    print(stock_formatted[:500] + "...")
    
    print("\nCrypto data formatting:")
    crypto_formatted = deepseek_service._format_data_for_prompt_simplified(crypto_data)
    print(crypto_formatted[:500] + "...")

if __name__ == "__main__":
    asyncio.run(test_query_analysis()) 