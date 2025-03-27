from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from app.services.polygon_service import PolygonService
from typing import Optional, Dict, Any, List

router = APIRouter()

# Models for response
class StockPriceResponse(BaseModel):
    ticker: str
    price: float
    change: Optional[float] = None
    change_percent: Optional[float] = None
    data: Dict[str, Any]
    
class NewsItem(BaseModel):
    title: str
    url: str
    published_utc: str
    description: Optional[str] = None
    
class StockNewsResponse(BaseModel):
    ticker: str
    news: List[NewsItem]
    
class HistoricalPriceResponse(BaseModel):
    ticker: str
    results: List[Dict[str, Any]]
    
# Dependency Injection
def get_polygon_service():
    return PolygonService()

@router.get("/stock/price/{ticker}", response_model=StockPriceResponse)
async def get_stock_price(
    ticker: str,
    polygon_service: PolygonService = Depends(get_polygon_service)
):
    """
    Get the current stock price for a ticker
    """
    try:
        response = await polygon_service.get_stock_price(ticker)
        
        if "error" in response:
            return StockPriceResponse(
                ticker=ticker,
                price=0.0,
                data={"error": response["error"]}
            )
        
        # Process the response
        if "results" in response and len(response["results"]) > 0:
            result = response["results"][0]
            return StockPriceResponse(
                ticker=ticker,
                price=result.get("c", 0.0),  # Close price
                change=result.get("c", 0.0) - result.get("o", 0.0),  # Close - Open
                change_percent=((result.get("c", 0.0) - result.get("o", 0.0)) / result.get("o", 1.0)) * 100 if result.get("o", 0) != 0 else 0.0,
                data=result
            )
        else:
            return StockPriceResponse(
                ticker=ticker,
                price=0.0,
                data={"error": "No results found"}
            )
    except Exception as e:
        return StockPriceResponse(
            ticker=ticker,
            price=0.0,
            data={"error": str(e)}
        )

@router.get("/stock/news/{ticker}", response_model=StockNewsResponse)
async def get_stock_news(
    ticker: str,
    limit: int = Query(5, ge=1, le=50),
    polygon_service: PolygonService = Depends(get_polygon_service)
):
    """
    Get recent news for a company
    """
    try:
        response = await polygon_service.get_company_news(ticker, limit)
        
        news_items = []
        if "results" in response:
            for item in response["results"]:
                news_items.append(NewsItem(
                    title=item.get("title", ""),
                    url=item.get("article_url", ""),
                    published_utc=item.get("published_utc", ""),
                    description=item.get("description", "")
                ))
        
        return StockNewsResponse(
            ticker=ticker,
            news=news_items
        )
    except Exception as e:
        return StockNewsResponse(
            ticker=ticker,
            news=[]
        )

@router.get("/stock/historical/{ticker}", response_model=HistoricalPriceResponse)
async def get_historical_prices(
    ticker: str,
    from_date: str,
    to_date: str,
    polygon_service: PolygonService = Depends(get_polygon_service)
):
    """
    Get historical stock prices for a ticker
    """
    try:
        response = await polygon_service.get_historical_prices(ticker, from_date, to_date)
        
        results = []
        if "results" in response:
            results = response["results"]
        
        return HistoricalPriceResponse(
            ticker=ticker,
            results=results
        )
    except Exception as e:
        return HistoricalPriceResponse(
            ticker=ticker,
            results=[]
        ) 