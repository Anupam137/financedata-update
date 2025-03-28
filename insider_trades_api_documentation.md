# Insider Trades - Trades (by ticker)
Get insider trades like buys and sells for a ticker by a company insider.

## GET /insider-trades

Try it

## 👋 Overview
The insider trades API lets you access the stock buys and sales of public company insiders like CEOs, CFOs, and Directors.

In addition to the stock buys and sales, you can also access the current ownership stakes of insiders.

This data is useful for understanding the sentiment of company insiders. For example, you can answer questions like:

- How many shares of Nvidia does Jensen Huang own?
- How many shares of Microsoft did Satya Nadella buy last quarter?
- How many shares of Apple has Tim Cook sold over the past year?

To get started, please create an account and grab your API key at financialdatasets.ai.

You will use the API key to authenticate your API requests.

## 📊 Available Tickers
You can fetch a list of available tickers with a GET request to: https://api.financialdatasets.ai/insider-trades/tickers/

## 🚀 Getting Started
There are only 3 steps for making a successful API call:

1. Add your API key to the header of the request as X-API-KEY.
2. Add query params like ticker and limit to filter the data.
3. Execute the API request.

## 🔎 Filtering the Data
You can filter the data by ticker, limit, and filing_date.

Note: ticker is required required. By default, limit is 100 and filing_date is null.

The limit parameter is used to specify the number of trades to return. The maximum value is 1000.

The filing_date parameter is used to specify the date of the trades. For example, you can include filters like filing_date_lte=2024-09-30 and filing_date_gte=2024-01-01 to get trades between January 1, 2024 and September 30, 2024.

The available filing_date operations are:

- filing_date_lte
- filing_date_lt
- filing_date_gte
- filing_date_gt
- filing_date

## 💻 Example
Insider Trades

```python
import requests

# add your API key to the headers
headers = {
    "X-API-KEY": "your_api_key_here"
}

# set your query params
ticker = 'NVDA'     # stock ticker
limit = 100         # number of trades to return

# create the URL
url = (
    f'https://api.financialdatasets.ai/insider-trades'
    f'?ticker={ticker}'
    f'&limit={limit}'
)

# make API request
response = requests.get(url, headers=headers)

# parse insider_trades from the response
insider_trades = response.json().get('insider_trades')
```

## 💻 Example (with filing_date)
Insider Trades

```python
import requests

# add your API key to the headers
headers = {
    "X-API-KEY": "your_api_key_here"
}

# set your query params
ticker = 'NVDA'     
filing_date_lte = '2024-01-01' # end date
filing_date_gte = '2020-01-01' # start date

# create the URL
url = (
    f'https://api.financialdatasets.ai/insider-trades'
    f'?ticker={ticker}'
    f'&filing_date_lte={filing_date_lte}'
    f'&filing_date_gte={filing_date_gte}'
)

# make API request
response = requests.get(url, headers=headers)

# parse insider_trades from the response
insider_trades = response.json().get('insider_trades')
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
- The ticker symbol of the company.

**limit**
- integer
- default: 10
- The maximum number of transactions to return (default: 10).

## Response
200

200
application/json
Insider trades response

**insider_trades**
- object[]

Show child attributes

## All Financial Statements
## Ownership (by investor) 