from fastapi import APIRouter, Depends, Query
from pydantic import BaseModel
from app.services.polygon_service import PolygonService
from app.services.financial_datasets_service import FinancialDatasetsService
from typing import Optional, Dict, Any, List

router = APIRouter()

# Models for response
class FinancialsResponse(BaseModel):
    ticker: str
    financials: List[Dict[str, Any]]
    
class InsiderTradesResponse(BaseModel):
    ticker: str
    trades: List[Dict[str, Any]]
    
class SECFilingsResponse(BaseModel):
    ticker: str
    filings: List[Dict[str, Any]]
    
class InstitutionalOwnershipResponse(BaseModel):
    ticker: str
    ownership: List[Dict[str, Any]]
    
# Dependency Injection
def get_polygon_service():
    return PolygonService()

def get_financial_datasets_service():
    return FinancialDatasetsService()

@router.get("/financials/{ticker}", response_model=FinancialsResponse)
async def get_company_financials(
    ticker: str,
    limit: int = Query(4, ge=1, le=20),
    polygon_service: PolygonService = Depends(get_polygon_service)
):
    """
    Get financial reports for a company from Polygon.io
    """
    try:
        response = await polygon_service.get_financials(ticker, limit)
        
        financials = []
        if "results" in response:
            financials = response["results"]
        
        return FinancialsResponse(
            ticker=ticker,
            financials=financials
        )
    except Exception as e:
        return FinancialsResponse(
            ticker=ticker,
            financials=[]
        )

@router.get("/financials/statements/{ticker}", response_model=FinancialsResponse)
async def get_financial_statements(
    ticker: str,
    limit: int = Query(4, ge=1, le=20),
    financial_datasets_service: FinancialDatasetsService = Depends(get_financial_datasets_service)
):
    """
    Get financial statements for a company from FinancialDatasets.ai
    """
    try:
        response = await financial_datasets_service.get_financial_statements(ticker, limit)
        
        financials = []
        # Check for the correct response structure based on documentation
        if "financials" in response:
            # Combine all statement types into a single list
            if "income_statements" in response["financials"]:
                financials.extend(response["financials"]["income_statements"])
            if "balance_sheets" in response["financials"]:
                financials.extend(response["financials"]["balance_sheets"])
            if "cash_flow_statements" in response["financials"]:
                financials.extend(response["financials"]["cash_flow_statements"])
        elif "results" in response:  # Fallback to old structure
            financials = response["results"]
        
        return FinancialsResponse(
            ticker=ticker,
            financials=financials
        )
    except Exception as e:
        return FinancialsResponse(
            ticker=ticker,
            financials=[]
        )

@router.get("/insider-trades/{ticker}", response_model=InsiderTradesResponse)
async def get_insider_trades(
    ticker: str,
    limit: int = Query(10, ge=1, le=50),
    financial_datasets_service: FinancialDatasetsService = Depends(get_financial_datasets_service)
):
    """
    Get insider trades for a company from FinancialDatasets.ai
    """
    try:
        response = await financial_datasets_service.get_insider_trades(ticker, limit)
        
        trades = []
        # Check for the correct response structure based on documentation
        if "insider_trades" in response:
            trades = response["insider_trades"]
        elif "results" in response:  # Fallback to old structure
            trades = response["results"]
        
        return InsiderTradesResponse(
            ticker=ticker,
            trades=trades
        )
    except Exception as e:
        return InsiderTradesResponse(
            ticker=ticker,
            trades=[]
        )

@router.get("/sec-filings/{ticker}", response_model=SECFilingsResponse)
async def get_sec_filings(
    ticker: str,
    form_type: Optional[str] = None,
    limit: int = Query(5, ge=1, le=20),
    financial_datasets_service: FinancialDatasetsService = Depends(get_financial_datasets_service)
):
    """
    Get SEC filings for a company from FinancialDatasets.ai
    """
    try:
        response = await financial_datasets_service.get_sec_filings(ticker, form_type, limit)
        
        filings = []
        # Check for the correct response structure based on documentation
        if "filings" in response:
            filings = response["filings"]
        elif "results" in response:  # Fallback to old structure
            filings = response["results"]
        
        return SECFilingsResponse(
            ticker=ticker,
            filings=filings
        )
    except Exception as e:
        return SECFilingsResponse(
            ticker=ticker,
            filings=[]
        )

@router.get("/institutional-ownership/{ticker}", response_model=InstitutionalOwnershipResponse)
async def get_institutional_ownership(
    ticker: str,
    financial_datasets_service: FinancialDatasetsService = Depends(get_financial_datasets_service)
):
    """
    Get institutional ownership data for a company from FinancialDatasets.ai
    """
    try:
        response = await financial_datasets_service.get_institutional_ownership(ticker)
        
        ownership = []
        # Check for the correct response structure based on documentation
        if "institutional_ownership" in response:
            ownership = response["institutional_ownership"]
        elif "results" in response:  # Fallback to old structure
            ownership = response["results"]
        
        return InstitutionalOwnershipResponse(
            ticker=ticker,
            ownership=ownership
        )
    except Exception as e:
        return InstitutionalOwnershipResponse(
            ticker=ticker,
            ownership=[]
        ) 