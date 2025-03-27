import asyncio
import json
from app.services.polygon_service import PolygonService

async def test_crypto_price_fix():
    # Initialize the Polygon service
    polygon_service = PolygonService()
    
    # Test only two cryptocurrencies to avoid rate limits
    cryptos = ["ETH", "BTC"]
    
    for crypto in cryptos:
        print(f"\nTesting {crypto} price with new get_crypto_price method:")
        try:
            result = await polygon_service.get_crypto_price(crypto)
            print(f"{crypto} data: {json.dumps(result, indent=2)}")
        except Exception as e:
            print(f"Error getting {crypto} price with get_crypto_price: {e}")
        
        print(f"\nComparing with old method (X:{crypto}-USD format):")
        try:
            old_result = await polygon_service.get_stock_price(f"X:{crypto}-USD")
            print(f"Old method result: {json.dumps(old_result, indent=2)}")
        except Exception as e:
            print(f"Error with old method: {e}")
    
    print("\nTest completed!")

if __name__ == "__main__":
    asyncio.run(test_crypto_price_fix()) 