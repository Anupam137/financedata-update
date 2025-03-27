import httpx
import json
from app.core.config import PERPLEXITY_API_KEY, PERPLEXITY_API_URL

class PerplexityService:
    def __init__(self):
        self.api_key = PERPLEXITY_API_KEY
        self.base_url = PERPLEXITY_API_URL
        
    async def sonar_search(self, query):
        """
        Perform a search using Perplexity Sonar
        
        Args:
            query (str): Search query
            
        Returns:
            dict: Search results
        """
        endpoint = "/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        data = {
            "model": "sonar",
            "messages": [
                {"role": "system", "content": "You are a financial research assistant. Provide accurate financial information with sources."},
                {"role": "user", "content": query}
            ]
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}{endpoint}",
                    headers=headers,
                    json=data,
                    timeout=60.0
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                print(f"HTTP error occurred with Perplexity Sonar: {e}")
                return {"error": str(e)}
            except Exception as e:
                print(f"An error occurred with Perplexity Sonar: {e}")
                return {"error": str(e)}
    
    async def deep_research(self, query):
        """
        Perform deep research using Perplexity
        
        Args:
            query (str): Research query
            
        Returns:
            dict: Research results
        """
        endpoint = "/chat/completions"
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
            "Accept": "application/json"
        }
        
        data = {
            "model": "sonar",
            "messages": [
                {
                    "role": "system", 
                    "content": """You are a financial analysis expert conducting deep research. 
                    Provide detailed analysis and comparison of companies based on financial metrics, 
                    market trends, and business outlook. Include sources for your information.
                    Focus on providing in-depth, well-researched answers with specific data points and metrics.
                    Your response should be comprehensive and thorough, as if you were writing a detailed research report.
                    Include numerical data, comparisons, and specific insights whenever possible."""
                },
                {"role": "user", "content": f"Conduct a deep financial analysis on: {query}"}
            ]
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    f"{self.base_url}{endpoint}",
                    headers=headers,
                    json=data,
                    timeout=90.0
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                print(f"HTTP error occurred with Perplexity Deep Research: {e}")
                return {"error": str(e)}
            except Exception as e:
                print(f"An error occurred with Perplexity Deep Research: {e}")
                return {"error": str(e)} 