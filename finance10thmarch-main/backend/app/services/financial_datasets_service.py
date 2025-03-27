import httpx
from app.core.config import FINANCIAL_DATASETS_API_KEY

class FinancialDatasetsService:
    def __init__(self):
        self.api_key = FINANCIAL_DATASETS_API_KEY
        self.base_url = "https://api.financialdatasets.ai"  # Removed /v1
        
    async def get_financial_statements(self, ticker, limit=4):
        """
        Get financial statements for a company
        
        Args:
            ticker (str): Stock ticker symbol
            limit (int): Maximum number of statements to return
            
        Returns:
            dict: Financial statement data
        """
        # Make three separate calls to get all financial statement types
        income_endpoint = f"/financials/income-statements"
        balance_endpoint = f"/financials/balance-sheets"
        cashflow_endpoint = f"/financials/cash-flow-statements"
        
        params = {
            "ticker": ticker,
            "period": "annual",  # Required parameter
            "limit": limit
        }
        
        headers = {
            "X-API-KEY": self.api_key  # API key in header instead of params
        }
        
        async with httpx.AsyncClient(follow_redirects=True) as client:
            try:
                # Make all three API calls
                income_response = await client.get(f"{self.base_url}{income_endpoint}", params=params, headers=headers)
                balance_response = await client.get(f"{self.base_url}{balance_endpoint}", params=params, headers=headers)
                cashflow_response = await client.get(f"{self.base_url}{cashflow_endpoint}", params=params, headers=headers)
                
                # Check if all responses are successful
                income_response.raise_for_status()
                balance_response.raise_for_status()
                cashflow_response.raise_for_status()
                
                # Parse the responses
                income_data = income_response.json()
                balance_data = balance_response.json()
                cashflow_data = cashflow_response.json()
                
                # Combine the data into a single response
                return {
                    "financials": {
                        "income_statements": income_data.get("income_statements", []),
                        "balance_sheets": balance_data.get("balance_sheets", []),
                        "cash_flow_statements": cashflow_data.get("cash_flow_statements", [])
                    }
                }
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
        endpoint = f"/insider-trades"  # This endpoint was already correct
        params = {
            "ticker": ticker,
            "limit": limit
        }
        
        headers = {
            "X-API-KEY": self.api_key  # API key in header
        }
        
        async with httpx.AsyncClient(follow_redirects=True) as client:
            try:
                response = await client.get(f"{self.base_url}{endpoint}", params=params, headers=headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                print(f"HTTP error occurred: {e}")
                return {"error": str(e)}
            except Exception as e:
                print(f"An error occurred: {e}")
                return {"error": str(e)}
    
    async def get_sec_filings(self, ticker, form_type=None, limit=5):
        """
        Get SEC filings for a company
        
        Args:
            ticker (str): Stock ticker symbol
            form_type (str, optional): Type of SEC form (e.g., '10-K', '10-Q')
            limit (int): Maximum number of filings to return
            
        Returns:
            dict: SEC filing data
        """
        endpoint = f"/filings"  # Updated to correct endpoint from documentation
        params = {
            "ticker": ticker,
            "limit": limit
        }
        
        if form_type:
            params["form_type"] = form_type
        
        headers = {
            "X-API-KEY": self.api_key  # API key in header
        }
        
        async with httpx.AsyncClient(follow_redirects=True) as client:
            try:
                response = await client.get(f"{self.base_url}{endpoint}", params=params, headers=headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                print(f"HTTP error occurred: {e}")
                # Return empty filings array on error instead of error message
                return {"ticker": ticker, "filings": []}
            except Exception as e:
                print(f"An error occurred: {e}")
                # Return empty filings array on error instead of error message
                return {"ticker": ticker, "filings": []}
                
    async def get_institutional_ownership(self, ticker):
        """
        Get institutional ownership data for a company
        
        Args:
            ticker (str): Stock ticker symbol
            
        Returns:
            dict: Institutional ownership data
        """
        endpoint = f"/institutional-ownership"  # This endpoint was already correct
        params = {
            "ticker": ticker
        }
        
        headers = {
            "X-API-KEY": self.api_key  # API key in header
        }
        
        async with httpx.AsyncClient(follow_redirects=True) as client:
            try:
                response = await client.get(f"{self.base_url}{endpoint}", params=params, headers=headers)
                response.raise_for_status()
                return response.json()
            except httpx.HTTPError as e:
                print(f"HTTP error occurred: {e}")
                return {"error": str(e)}
            except Exception as e:
                print(f"An error occurred: {e}")
                return {"error": str(e)} 