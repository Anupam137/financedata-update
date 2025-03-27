from fastapi import APIRouter, Depends, Query, BackgroundTasks, Header
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from app.services.openai_service import OpenAIService
from app.services.perplexity_service import PerplexityService
from app.services.polygon_service import PolygonService
from app.services.financial_datasets_service import FinancialDatasetsService
from app.services.redis_service import RedisService
from app.services.deepseek_service import DeepSeekService
from app.services.deepseek_v3_service import DeepSeekV3Service
from app.utils.query_analyzer import is_simple_query, get_fast_path_response
from app.utils.sanitizer import sanitize_response, sanitize_text, sanitize_url
from app.core.config import ENABLE_STREAMING
from typing import Optional, List, Dict, Any
import re
import asyncio
import time
import json
import uuid

router = APIRouter()

# Models for request and response
class SearchRequest(BaseModel):
    query: str
    mode: str = "sonar"  # 'sonar', 'deep_research', or 'deepseek'
    session_id: Optional[str] = None
    
class Source(BaseModel):
    title: Optional[str] = None
    url: Optional[str] = None
    
class SearchResponse(BaseModel):
    answer: str
    sources: Optional[List[Source]] = None
    data: Optional[Dict[str, Any]] = None
    session_id: Optional[str] = None

# Dependency Injection
def get_openai_service():
    return OpenAIService()

def get_perplexity_service():
    return PerplexityService()

def get_polygon_service():
    return PolygonService()

def get_financial_datasets_service():
    return FinancialDatasetsService()

def get_redis_service():
    return RedisService()

def get_deepseek_service():
    return DeepSeekService()

def get_deepseek_v3_service():
    return DeepSeekV3Service()

def extract_perplexity_content(perplexity_response: Dict[str, Any]) -> str:
    """Extract content from Perplexity response"""
    if "choices" in perplexity_response and len(perplexity_response["choices"]) > 0:
        return sanitize_text(perplexity_response["choices"][0]["message"]["content"])
    return ""

def extract_perplexity_sources(perplexity_response: Dict[str, Any]) -> List[Source]:
    """Extract sources from Perplexity response"""
    sources = []
    
    # Check if there are sources in the response
    if "choices" in perplexity_response and len(perplexity_response["choices"]) > 0:
        message = perplexity_response["choices"][0]["message"]
        
        # Check for sources in the context field
        if "context" in message and "documents" in message["context"]:
            for doc in message["context"]["documents"]:
                sources.append(Source(
                    title=sanitize_text(doc.get("title", doc.get("url", "Unknown Source"))),
                    url=sanitize_url(doc.get("url", ""))
                ))
        
        # Check for citations in the response
        if "citations" in perplexity_response:
            for citation in perplexity_response["citations"]:
                # Check if this citation is already in sources
                if not any(s.url == citation for s in sources):
                    sources.append(Source(
                        title=sanitize_text(citation),
                        url=sanitize_url(citation)
                    ))
    
    return sources

def extract_sources(api_results: Dict[str, Any]) -> List[Source]:
    """Extract sources from API results"""
    sources = []
    
    # Extract sources from Perplexity response
    for key, value in api_results.items():
        if key in ["perplexity_sonar", "perplexity_deep_research"] and "error" not in value:
            perplexity_sources = extract_perplexity_sources(value)
            sources.extend(perplexity_sources)
    
    # Extract sources from news data
    for key, value in api_results.items():
        if "_news" in key and "results" in value:
            for item in value["results"][:3]:
                sources.append(Source(
                    title=sanitize_text(item.get("title", "News Article")),
                    url=sanitize_url(item.get("article_url", ""))
                ))
    
    return sources

@router.post("/search", response_model=SearchResponse)
async def search(
    request: SearchRequest,
    background_tasks: BackgroundTasks,
    openai_service: OpenAIService = Depends(get_openai_service),
    perplexity_service: PerplexityService = Depends(get_perplexity_service),
    polygon_service: PolygonService = Depends(get_polygon_service),
    financial_datasets_service: FinancialDatasetsService = Depends(get_financial_datasets_service),
    deepseek_service: DeepSeekService = Depends(get_deepseek_service),
    deepseek_v3_service: DeepSeekV3Service = Depends(get_deepseek_v3_service),
    redis_service: RedisService = Depends(get_redis_service)
):
    """
    Search for financial information using multiple APIs with LLM-first approach
    """
    try:
        query = sanitize_text(request.query)
        mode = request.mode
        
        # Generate or use provided session_id
        session_id = request.session_id or str(uuid.uuid4())
        
        # Debug logging
        is_follow_up = request.session_id is not None
        print(f"Search request received - Query: '{query}', Session ID: {session_id}, Mode: {mode}, Is Follow-up: {is_follow_up}")
        
        # Add user query to conversation history
        openai_service.add_to_conversation(session_id, "user", query)
        
        # Step 1: Check for cached response
        try:
            cached_response = await redis_service.get_query_response(query)
            if cached_response:
                answer = sanitize_text(cached_response["answer"])
                # Add the cached response to conversation history
                openai_service.add_to_conversation(session_id, "assistant", answer)
                
                print(f"Returning cached response for query: '{query}', Session ID: {session_id}")
                
                return SearchResponse(
                    answer=answer,
                    sources=[Source(**source) for source in cached_response.get("sources", [])],
                    data=cached_response.get("data"),
                    session_id=session_id
                )
        except Exception as e:
            print(f"Redis get error: {str(e)}")
            # Continue with the request even if Redis fails
        
        # Handle DeepSeek mode separately
        if mode == "deepseek":
            print(f"DEBUG: Using DeepSeek mode for query: '{query}', Session ID: {session_id}")
            # Use OpenAI to analyze the query (reuse existing logic)
            api_plan = await openai_service.analyze_query(query, session_id)
            
            # Process crypto queries if detected
            is_crypto_query = api_plan.get("is_crypto_query", False)
            
            # Add a simple check for crypto queries
            for i, ticker in enumerate(api_plan.get("tickers", [])):
                # If OpenAI flagged this as a crypto query or we can detect common crypto tickers
                if is_crypto_query or ticker.upper() in ["BTC", "ETH", "XRP", "DOGE", "SOL", "ADA"]:
                    # Ensure the ticker is in the standard format
                    api_plan["tickers"][i] = ticker.upper()
                    # Set a flag to use crypto-specific handling
                    api_plan["is_crypto"] = True
            
            # Collect data from various APIs
            api_results = {}
            tasks = []
            task_keys = []
            
            # Always call Perplexity Deep Research for DeepSeek mode
            tasks.append(perplexity_service.deep_research(query))
            task_keys.append("perplexity_deep_research")
            
            # Also call Perplexity Sonar for market insights
            tasks.append(perplexity_service.sonar_search(query))
            task_keys.append("perplexity_sonar")
            
            # Extract tickers from API plan
            tickers = api_plan.get("tickers", [])
            
            # Collect data for each ticker
            for ticker in tickers:
                # Normalize ticker to uppercase
                ticker = ticker.upper()
                
                if api_plan.get("need_stock_price", False):
                    # For crypto, use the dedicated crypto price method
                    if api_plan.get("is_crypto", False):
                        tasks.append(polygon_service.get_crypto_price(ticker))
                        task_keys.append(f"{ticker}_price")
                    else:
                        tasks.append(polygon_service.get_stock_price(ticker))
                        task_keys.append(f"{ticker}_price")
                
                if api_plan.get("need_financials", False):
                    tasks.append(financial_datasets_service.get_financial_statements(ticker))
                    task_keys.append(f"{ticker}_financials")
                
                if api_plan.get("need_insider_trades", False):
                    tasks.append(financial_datasets_service.get_insider_trades(ticker))
                    task_keys.append(f"{ticker}_insider_trades")
                    
                if api_plan.get("need_sec_filings", False):
                    tasks.append(financial_datasets_service.get_sec_filings(ticker))
                    task_keys.append(f"{ticker}_sec_filings")
                
                # Always get news for tickers
                tasks.append(polygon_service.get_company_news(ticker))
                task_keys.append(f"{ticker}_news")
            
            # Execute all API calls in parallel
            if tasks:
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                # Process results
                for i, result in enumerate(results):
                    if isinstance(result, Exception):
                        print(f"Error in API call {task_keys[i]}: {result}")
                        api_results[task_keys[i]] = {"error": str(result)}
                    else:
                        api_results[task_keys[i]] = result
            
            # Generate insights using DeepSeek R1
            final_response = await deepseek_service.generate_financial_insight(query, api_results, session_id)
            
            # Extract sources
            sources = extract_sources(api_results)
            
            # Cache the response in the background
            try:
                background_tasks.add_task(
                    redis_service.set_query_response,
                    query,
                    {"answer": final_response, "sources": [s.__dict__ for s in sources], "data": api_results}
                )
            except Exception as e:
                print(f"Redis set_query_response error: {str(e)}")
                # Continue even if Redis caching fails
            
            # Add the response to conversation history
            openai_service.add_to_conversation(session_id, "assistant", final_response)
            
            # Before returning the response, sanitize it
            response = SearchResponse(
                answer=final_response,
                sources=sources,
                data=api_results,
                session_id=session_id
            )
            
            # Sanitize the entire response
            sanitized_response = sanitize_response(response.dict())
            
            # Cache the sanitized response in the background
            try:
                background_tasks.add_task(
                    redis_service.set_query_response,
                    query,
                    sanitized_response
                )
            except Exception as e:
                print(f"Redis set error: {str(e)}")
            
            return SearchResponse(**sanitized_response)
        
        # Step 2: Use OpenAI to analyze the query
        print(f"DEBUG: Analyzing query with OpenAI: '{query}', Session ID: {session_id}")
        api_plan = await openai_service.analyze_query(query, session_id)
        print(f"DEBUG: API plan: {api_plan}")
        
        # Handle Deep Research mode explicitly set by user
        if mode == "deep_research":
            print(f"DEBUG: Deep Research mode activated for query: '{query}', Session ID: {session_id}")
            api_plan["call_perplexity_deep_research"] = True
        
        # Process crypto queries if detected
        is_crypto_query = api_plan.get("is_crypto_query", False)
        
        # Add a simple check for crypto queries
        for i, ticker in enumerate(api_plan.get("tickers", [])):
            # If OpenAI flagged this as a crypto query or we can detect common crypto tickers
            if is_crypto_query or ticker.upper() in ["BTC", "ETH", "XRP", "DOGE", "SOL", "ADA"]:
                # Ensure the ticker is in the standard format
                api_plan["tickers"][i] = ticker.upper()
                # Set a flag to use crypto-specific handling
                api_plan["is_crypto"] = True
        
        # Cache the API plan
        try:
            background_tasks.add_task(
                redis_service.set_api_plan,
                query,
                api_plan
            )
        except Exception as e:
            print(f"Redis set_api_plan error: {str(e)}")
            # Continue even if Redis caching fails
        
        # Step 3: Execute API calls in parallel based on the plan
        api_results = {}
        tasks = []
        task_keys = []
        
        # Perplexity API calls
        if mode == "sonar" or api_plan.get("call_perplexity_sonar", False):
            tasks.append(perplexity_service.sonar_search(query))
            task_keys.append("perplexity_sonar")
        
        if mode == "deep_research" or api_plan.get("call_perplexity_deep_research", False):
            tasks.append(perplexity_service.deep_research(query))
            task_keys.append("perplexity_deep_research")
        
        # Extract tickers from API plan
        tickers = api_plan.get("tickers", [])
        
        # Stock-specific API calls for each ticker
        for ticker in tickers:
            # Normalize ticker to uppercase
            ticker = ticker.upper()
            
            if api_plan.get("need_stock_price", False):
                # For crypto, use the dedicated crypto price method
                if api_plan.get("is_crypto", False):
                    tasks.append(polygon_service.get_crypto_price(ticker))
                    task_keys.append(f"{ticker}_price")
                else:
                    tasks.append(polygon_service.get_stock_price(ticker))
                    task_keys.append(f"{ticker}_price")
            
            if api_plan.get("need_financials", False):
                tasks.append(financial_datasets_service.get_financial_statements(ticker))
                task_keys.append(f"{ticker}_financials")
            
            if api_plan.get("need_insider_trades", False):
                tasks.append(polygon_service.get_insider_trades(ticker))
                task_keys.append(f"{ticker}_insider_trades")
                
            if api_plan.get("need_sec_filings", False):
                tasks.append(financial_datasets_service.get_sec_filings(ticker))
                task_keys.append(f"{ticker}_sec_filings")
            
            # Always get news for tickers if we're looking for market insights
            if api_plan.get("call_perplexity_sonar", False):
                tasks.append(polygon_service.get_company_news(ticker))
                task_keys.append(f"{ticker}_news")
        
        # Execute all API calls in parallel
        if tasks:
            results = await asyncio.gather(*tasks, return_exceptions=True)
            
            # Process results
            for i, result in enumerate(results):
                if isinstance(result, Exception):
                    print(f"Error in API call {task_keys[i]}: {result}")
                    api_results[task_keys[i]] = {"error": str(result)}
                else:
                    api_results[task_keys[i]] = result
        
        # Step 4: Generate the final response using the appropriate service based on mode
        if mode == "deepseek":
            # Use DeepSeek R1 for Comprehensive Research mode
            final_response = await deepseek_service.generate_financial_insight(query, api_results, session_id)
        elif mode == "deep_research":
            # Use DeepSeek V3 for Deep Research mode
            final_response = await deepseek_v3_service.generate_narrative_insight(query, api_results, session_id)
        else:
            # Use OpenAI for Sonar mode (default)
            final_response = await openai_service.generate_financial_insight(query, api_results, session_id)
        
        # Extract sources
        sources = extract_sources(api_results)
        
        # Cache the response in the background
        try:
            background_tasks.add_task(
                redis_service.set_query_response,
                query,
                {"answer": final_response, "sources": [s.__dict__ for s in sources], "data": api_results}
            )
        except Exception as e:
            print(f"Redis set_query_response error: {str(e)}")
            # Continue even if Redis caching fails
        
        # Before returning the response, sanitize it
        response = SearchResponse(
            answer=final_response,
            sources=sources,
            data=api_results,
            session_id=session_id
        )
        
        # Sanitize the entire response
        sanitized_response = sanitize_response(response.dict())
        
        # Cache the sanitized response in the background
        try:
            background_tasks.add_task(
                redis_service.set_query_response,
                query,
                sanitized_response
            )
        except Exception as e:
            print(f"Redis set error: {str(e)}")
        
        return SearchResponse(**sanitized_response)
    except Exception as e:
        print(f"Error in search endpoint: {str(e)}")
        return SearchResponse(
            answer="I apologize, but I encountered an error while processing your request. Please try again later.",
            sources=[],
            data={},
            session_id=session_id
        )

@router.post("/search/stream")
async def stream_search(
    request: SearchRequest,
    background_tasks: BackgroundTasks,
    openai_service: OpenAIService = Depends(get_openai_service),
    perplexity_service: PerplexityService = Depends(get_perplexity_service),
    polygon_service: PolygonService = Depends(get_polygon_service),
    financial_datasets_service: FinancialDatasetsService = Depends(get_financial_datasets_service),
    deepseek_service: DeepSeekService = Depends(get_deepseek_service),
    deepseek_v3_service: DeepSeekV3Service = Depends(get_deepseek_v3_service),
    redis_service: RedisService = Depends(get_redis_service)
):
    """
    Stream search results in real-time
    """
    try:
        query = sanitize_text(request.query)
        mode = request.mode
        session_id = request.session_id or str(uuid.uuid4())
        
        async def stream_generator():
            try:
                # Initial status message
                yield f"data: {json.dumps({'type': 'status', 'content': 'Processing your query...', 'session_id': session_id})}\n\n"
                
                # Check for cached response
                try:
                    cached_response = await redis_service.get_query_response(query)
                    if cached_response:
                        answer = sanitize_text(cached_response["answer"])
                        yield f"data: {json.dumps({'type': 'result', 'content': answer, 'sources': cached_response.get('sources', []), 'session_id': session_id})}\n\n"
                        return
                except Exception as e:
                    print(f"Redis get error in stream: {str(e)}")
                
                # Analyze query
                yield f"data: {json.dumps({'type': 'status', 'content': 'Analyzing your query...', 'session_id': session_id})}\n\n"
                api_plan = await openai_service.analyze_query(query, session_id)
                
                # Collect data from APIs
                api_results = {}
                tasks = []
                task_keys = []
                
                # Add API tasks based on mode and plan
                if mode == "deepseek":
                    tasks.extend([
                        perplexity_service.deep_research(query),
                        perplexity_service.sonar_search(query)
                    ])
                    task_keys.extend(["perplexity_deep_research", "perplexity_sonar"])
                else:
                    if mode == "sonar" or api_plan.get("call_perplexity_sonar", False):
                        tasks.append(perplexity_service.sonar_search(query))
                        task_keys.append("perplexity_sonar")
                    if mode == "deep_research" or api_plan.get("call_perplexity_deep_research", False):
                        tasks.append(perplexity_service.deep_research(query))
                        task_keys.append("perplexity_deep_research")
                
                # Add ticker-specific tasks
                for ticker in api_plan.get("tickers", []):
                    ticker = ticker.upper()
                    if api_plan.get("need_stock_price", False):
                        if api_plan.get("is_crypto", False):
                            tasks.append(polygon_service.get_crypto_price(ticker))
                        else:
                            tasks.append(polygon_service.get_stock_price(ticker))
                        task_keys.append(f"{ticker}_price")
                    
                    if api_plan.get("need_financials", False):
                        tasks.append(financial_datasets_service.get_financial_statements(ticker))
                        task_keys.append(f"{ticker}_financials")
                    
                    if api_plan.get("need_insider_trades", False):
                        tasks.append(financial_datasets_service.get_insider_trades(ticker))
                        task_keys.append(f"{ticker}_insider_trades")
                    
                    if api_plan.get("need_sec_filings", False):
                        tasks.append(financial_datasets_service.get_sec_filings(ticker))
                        task_keys.append(f"{ticker}_sec_filings")
                    
                    if api_plan.get("call_perplexity_sonar", False):
                        tasks.append(polygon_service.get_company_news(ticker))
                        task_keys.append(f"{ticker}_news")
                
                # Execute API calls
                if tasks:
                    yield f"data: {json.dumps({'type': 'status', 'content': 'Gathering financial data...', 'session_id': session_id})}\n\n"
                    results = await asyncio.gather(*tasks, return_exceptions=True)
                    
                    for i, result in enumerate(results):
                        if isinstance(result, Exception):
                            print(f"Error in API call {task_keys[i]}: {result}")
                            api_results[task_keys[i]] = {"error": str(result)}
                        else:
                            api_results[task_keys[i]] = result
                
                # Generate final response
                yield f"data: {json.dumps({'type': 'status', 'content': 'Generating insights...', 'session_id': session_id})}\n\n"
                
                if mode == "deepseek":
                    final_response = await deepseek_service.generate_financial_insight(query, api_results, session_id)
                elif mode == "deep_research":
                    final_response = await deepseek_v3_service.generate_narrative_insight(query, api_results, session_id)
                else:
                    final_response = await openai_service.generate_financial_insight(query, api_results, session_id)
                
                # Extract and sanitize sources
                sources = extract_sources(api_results)
                sources_list = [{"title": s.title, "url": s.url} for s in sources]
                
                # Cache the response
                try:
                    background_tasks.add_task(
                        redis_service.set_query_response,
                        query,
                        {"answer": final_response, "sources": sources_list, "data": api_results}
                    )
                except Exception as e:
                    print(f"Redis set error in stream: {str(e)}")
                
                # Return final result
                yield f"data: {json.dumps({'type': 'result', 'content': sanitize_text(final_response), 'sources': sources_list, 'session_id': session_id})}\n\n"
                
            except Exception as e:
                print(f"Error in stream generator: {str(e)}")
                yield f"data: {json.dumps({'type': 'error', 'content': 'An error occurred while processing your request.', 'session_id': session_id})}\n\n"
        
        return StreamingResponse(
            stream_generator(),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"
            }
        )
        
    except Exception as e:
        print(f"Error in stream_search endpoint: {str(e)}")
        return StreamingResponse(
            iter([f"data: {json.dumps({'type': 'error', 'content': 'An error occurred while processing your request.', 'session_id': session_id})}\n\n"]),
            media_type="text/event-stream",
            headers={
                "Cache-Control": "no-cache",
                "Connection": "keep-alive",
                "X-Accel-Buffering": "no"
            }
        ) 