# Financial Statements - All Financial Statements
Get all financial statements for a ticker.

## GET /financials

Try it

## 👋 Overview
This endpoint aggregates all financial statements for a ticker into a single API call.

So, instead of calling 3 endpoints to get income statements, balance sheets, and cash flow statements, you can call this endpoint once and get all financial statements in one go.

The endpoint returns the following financial statements:

- Income Statements
- Balance Sheets
- Cash Flow Statements

To get started, please create an account and grab your API key at financialdatasets.ai.

You will use the API key to authenticate your API requests.

## 📊 Available Tickers
You can fetch a list of available tickers with a GET request to: https://api.financialdatasets.ai/financials/tickers/

## 🚀 Getting Started
There are only 3 steps for making a successful API call:

1. Add your API key to the header of the request as X-API-KEY.
2. Add query params like ticker, period and limit to filter the data.
3. Execute the API request.

## 🔎 Filtering the Data
You can filter the data by ticker, period, limit, and report_period.

Note: ticker and period are required. Alternatively, you can use cik instead of ticker as a company identifier in your request.

By default, period is ttm,limit is 4, and report_period is null.

The period parameter can be set to annual, quarterly, or ttm (trailing twelve months). The limit parameter is used to specify the number of periods to return.

The report_period parameter is used to specify the date of the statement. For example, you can include filters like report_period_lte=2024-09-30 and report_period_gte=2024-01-01 to get statements between January 1, 2024 and September 30, 2024.

The available report_period operations are:

- report_period_lte
- report_period_lt
- report_period_gte
- report_period_gt
- report_period

## 💻 Example
All Financial Statements

```python
import requests

# add your API key to the headers
headers = {
    "X-API-KEY": "your_api_key_here"
}

# set your query params
ticker = 'NVDA'     # stock ticker
period = 'annual'   # possible values are 'annual', 'quarterly', or 'ttm'
limit = 30          # number of statements to return

# create the URL
url = (
    f'https://api.financialdatasets.ai/financials/'
    f'?ticker={ticker}'
    f'&period={period}'
    f'&limit={limit}'
)

# make API request
response = requests.get(url, headers=headers)

# parse financials from the response
financials = response.json().get('financials')

# get income statements
income_statements = financials.get('income_statements')

# get balance sheets
balance_sheets = financials.get('balance_sheets')

# get cash flow statements
cash_flow_statements = financials.get('cash_flow_statements')
```

## 💻 Example (with report_period)
All Financial Statements

```python
import requests

# add your API key to the headers
headers = {
    "X-API-KEY": "your_api_key_here"
}

# set your query params
ticker = 'NVDA'  
period = 'annual'
limit = 100 
report_period_lte = '2024-01-01' # end date
report_period_gte = '2020-01-01' # start date

# create the URL
url = (
    f'https://api.financialdatasets.ai/financials/'
    f'?ticker={ticker}'
    f'&period={period}'
    f'&limit={limit}'
    f'&report_period_lte={report_period_lte}'
    f'&report_period_gte={report_period_gte}'
)

# make API request
response = requests.get(url, headers=headers)

# parse financials from the response
financials = response.json().get('financials')
```

## Authorizations

**X-API-KEY**
- string
- header
- required
- API key for authentication.

## Query Parameters

**ticker**
- string
- required
- The ticker symbol.

**period**
- enum<string>
- required
- The time period of the financial statements.
- Available options: annual, quarterly, ttm 

**limit**
- integer
- The maximum number of financial statements to return.

**cik**
- string
- The Central Index Key (CIK) of the company.

## Response
200

200
application/json
Financial statements response

**financials**
- object

Show child attributes

## Cash Flow Statements
## Trades (by ticker) 