from app.utils.query_analyzer import is_simple_query, extract_ticker_symbols

# Test queries
queries = [
    "What is the price of TSLA right now",
    "What is the price of Tesla right now",
    "TSLA stock price",
    "Tesla stock price",
    "How much is TSLA trading for",
    "What's the latest news on TSLA",
    "Show me TSLA financials"
]

print("Testing query analyzer fast path detection:")
print("-" * 50)

for query in queries:
    is_simple, query_type, ticker = is_simple_query(query)
    tickers = extract_ticker_symbols(query)
    
    print(f"Query: '{query}'")
    print(f"Is simple query: {is_simple}")
    print(f"Query type: {query_type}")
    print(f"Extracted ticker: {ticker}")
    print(f"All extracted tickers: {tickers}")
    print("-" * 50) 