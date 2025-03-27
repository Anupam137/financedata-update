import httpx
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def test_polygon():
    api_key = os.getenv('POLYGON_API_KEY')
    base_url = 'https://api.polygon.io'
    endpoint = '/v2/aggs/ticker/TSLA/prev'
    params = {'apiKey': api_key}
    
    print(f'Using API key: {api_key[:5]}...{api_key[-5:]}')
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(f'{base_url}{endpoint}', params=params)
            response.raise_for_status()
            data = response.json()
            print('Response status:', response.status_code)
            print('Response data:', data)
        except Exception as e:
            print(f'Error: {e}')

if __name__ == "__main__":
    asyncio.run(test_polygon()) 