import httpx
from app.core.config import POLYGON_API_KEY, POLYGON_API_URL

class PolygonService:
    def __init__(self):
        self.api_key = POLYGON_API_KEY
        self.base_url = POLYGON_API_URL
        
    async def get_stock_price(self, ticker):
        """
        Get the current stock price for a ticker
        
        Args:
            ticker (str): Stock ticker symbol
            
        Returns:
            dict: Stock price data
        """
        endpoint = f"/v2/aggs/ticker/{ticker}/prev"
        params = {
            "apiKey": self.api_key
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.base_url}{endpoint}", params=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                print(f"HTTP error occurred: {e}")
                return {"error": str(e)}
            except Exception as e:
                print(f"An error occurred: {e}")
                return {"error": str(e)}
    
    async def get_crypto_price(self, ticker):
        """
        Get the current price for a cryptocurrency
        
        Args:
            ticker (str): Cryptocurrency ticker symbol (e.g., BTC, ETH)
            
        Returns:
            dict: Cryptocurrency price data
        """
        # Use the v2/aggs/ticker endpoint with X:{ticker}USD format
        formatted_ticker = f"X:{ticker}USD"
        endpoint = f"/v2/aggs/ticker/{formatted_ticker}/prev"
        params = {
            "apiKey": self.api_key
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.base_url}{endpoint}", params=params)
                response.raise_for_status()
                data = response.json()
                
                # Add cryptocurrency-specific information to the response
                if data.get("status") == "OK":
                    data["is_cryptocurrency"] = True
                    data["crypto_ticker"] = ticker
                
                return data
            except httpx.HTTPError as e:
                print(f"HTTP error occurred with crypto price: {e}")
                
                # If the first attempt fails, try the reference/tickers endpoint as a fallback
                try:
                    print(f"Trying fallback method for {ticker}...")
                    fallback_endpoint = f"/v3/reference/tickers"
                    fallback_params = {
                        "market": "crypto",
                        "active": "true",
                        "search": ticker,
                        "apiKey": self.api_key
                    }
                    
                    fallback_response = await client.get(f"{self.base_url}{fallback_endpoint}", params=fallback_params)
                    fallback_response.raise_for_status()
                    fallback_data = fallback_response.json()
                    
                    # Format the response to be similar to stock price data for consistency
                    if fallback_data.get("status") == "OK" and fallback_data.get("results"):
                        # Extract the first result (most relevant)
                        crypto_data = fallback_data["results"][0]
                        
                        # Create a formatted response similar to stock price data
                        formatted_response = {
                            "ticker": crypto_data.get("ticker", ticker),
                            "name": crypto_data.get("name", ""),
                            "market": crypto_data.get("market", "crypto"),
                            "currency": crypto_data.get("currency_name", "USD"),
                            "last_updated": crypto_data.get("last_updated_utc", ""),
                            "status": "OK",
                            "is_cryptocurrency": True,
                            "crypto_ticker": ticker,
                            "request_id": fallback_data.get("request_id", ""),
                            "fallback_method": True
                        }
                        
                        return formatted_response
                    return fallback_data
                except Exception as fallback_error:
                    print(f"Fallback method also failed: {fallback_error}")
                    return {"error": str(e), "fallback_error": str(fallback_error)}
                
            except Exception as e:
                print(f"An error occurred with crypto price: {e}")
                return {"error": str(e)}
    
    async def get_company_news(self, ticker, limit=5):
        """
        Get recent news for a company
        
        Args:
            ticker (str): Stock ticker symbol
            limit (int): Maximum number of news items to return
            
        Returns:
            dict: Company news data
        """
        endpoint = f"/v2/reference/news"
        params = {
            "ticker": ticker,
            "limit": limit,
            "apiKey": self.api_key
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.base_url}{endpoint}", params=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                print(f"HTTP error occurred: {e}")
                return {"error": str(e)}
            except Exception as e:
                print(f"An error occurred: {e}")
                return {"error": str(e)}
    
    async def get_historical_prices(self, ticker, from_date, to_date):
        """
        Get historical stock prices for a ticker
        
        Args:
            ticker (str): Stock ticker symbol
            from_date (str): Start date (YYYY-MM-DD)
            to_date (str): End date (YYYY-MM-DD)
            
        Returns:
            dict: Historical price data
        """
        endpoint = f"/v2/aggs/ticker/{ticker}/range/1/day/{from_date}/{to_date}"
        params = {
            "apiKey": self.api_key
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.base_url}{endpoint}", params=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                print(f"HTTP error occurred: {e}")
                return {"error": str(e)}
            except Exception as e:
                print(f"An error occurred: {e}")
                return {"error": str(e)}
                
    async def get_financials(self, ticker, limit=4):
        """
        Get financial reports for a company
        
        Args:
            ticker (str): Stock ticker symbol
            limit (int): Maximum number of reports to return
            
        Returns:
            dict: Financial report data
        """
        endpoint = f"/vX/reference/financials"
        params = {
            "ticker": ticker,
            "limit": limit,
            "apiKey": self.api_key
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.base_url}{endpoint}", params=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                print(f"HTTP error occurred: {e}")
                return {"error": str(e)}
            except Exception as e:
                print(f"An error occurred: {e}")
                return {"error": str(e)}
                
    async def get_insider_trades(self, ticker, limit=10):
        """
        Get insider trades for a company
        
        Args:
            ticker (str): Stock ticker symbol
            limit (int): Maximum number of trades to return
            
        Returns:
            dict: Insider trade data
        """
        # Polygon.io endpoint for insider transactions
        endpoint = f"/v2/reference/insiders"
        params = {
            "ticker": ticker,
            "limit": limit,
            "apiKey": self.api_key
        }
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.get(f"{self.base_url}{endpoint}", params=params)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                print(f"HTTP error occurred: {e}")
                return {"error": str(e)}
            except Exception as e:
                print(f"An error occurred: {e}")
                return {"error": str(e)} 