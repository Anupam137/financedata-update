# Get Started

## Introduction
Welcome to Financial Datasets, a developer-friendly stock market API.

## 👋 Overview
We are on a mission to make financial data delightful for developers.

Our API is designed for AI financial agents, portfolio management tools, stock analysis platforms, quantitative trading algorithms, and more.

We provide a simple REST API, which delivers premium stock market data, including:

- Financial statements
- Stock prices
- Segmented financials
- Insider trades
- Institutional ownership
- SEC filings
- Market news
- Crypto prices
- and more!

We have data for 30,000+ tickers, going back 30+ years.

Our platform is built by developers for developers ❤️

## 🚀 Getting Started
Please create an account and grab your API key at financialdatasets.ai.

You will use the API key to authenticate your requests.

There are only 3 steps for making a successful API call:

1. Add your API key to the header of the request as X-API-KEY.
2. Add query params like ticker, period and limit to filter the data.
3. Execute the API request.

## 💻 Examples

### Income Statements

### Balance Sheets

### Cash Flow Statements

```python
import requests

# add your API key to the headers
headers = {
    "X-API-KEY": "your_api_key_here"
}

# set your query params
ticker = 'NVDA'     # stock ticker
period = 'ttm'      # possible values are 'annual', 'quarterly', or 'ttm'
limit = 30          # number of statements to return

# create the URL
url = (
    f'https://api.financialdatasets.ai/financials/income-statements'
    f'?ticker={ticker}'
    f'&period={period}'
    f'&limit={limit}'
)

# make API request
response = requests.get(url, headers=headers)

# parse income_statements from the response
income_statements = response.json().get('income_statements')
```

## 🗣️ Feedback
Please join our Discord community, hang out, and tell us how we can improve.

We love developer feedback ❤️

## Facts (by CIK) 