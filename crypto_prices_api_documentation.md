# Crypto Prices
Get ranged price data for a cryptocurrency to power price charts and analyze price movements.

## GET /crypto/prices

Try it

## 👋 Overview
The Crypto Prices API lets you pull historical prices for a given cryptocurrency like Bitcoin, Ethereum, and more.

You can get prices by the minute, day, week, month, or year.

The prices are pulled directly from Coinbase, Kraken, and Bitfinex.

The data is perfect for backtesting trading strategies, analyzing price patterns, rendering charts, and more.

To get started, please create an account and grab your API key at financialdatasets.ai.

You will use the API key to authenticate your API requests.

## 📊 Available Tickers
You can fetch a list of available tickers with a GET request to: https://api.financialdatasets.ai/crypto/prices/tickers/

## 🚀 Getting Started
There are only 3 steps for making a successful API call:

1. Add your API key to the header of the request as X-API-KEY.
2. Add query params like ticker to filter the data.
3. Execute the API request.

## 💻 Example
Prices

```python
import requests

# add your API key to the headers
headers = {
    "X-API-KEY": "your_api_key_here"
}

# set your query params
ticker = 'BTC-USD'
interval = 'minute'         # possible values are {'minute', 'day', 'week', 'month', 'year'}
interval_multiplier = 5     # every 5 minutes
start_date = '2025-01-02'
end_date = '2025-01-05'

# create the URL
url = (
    f'https://api.financialdatasets.ai/crypto/prices/'
    f'?ticker={ticker}'
    f'&interval={interval}'
    f'&interval_multiplier={interval_multiplier}'
    f'&start_date={start_date}'
    f'&end_date={end_date}'
)

# make API request
response = requests.get(url, headers=headers)

# parse prices from the response
prices = response.json().get('prices')
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
- The cryptocurrency ticker symbol.

**interval**
- enum<string>
- required
- The time interval for the price data.
- Available options: minute, day, week, month, year 

**interval_multiplier**
- integer
- required
- The multiplier for the interval.
- Required range: x >= 1

**start_date**
- string
- required
- The start date for the price data (format: YYYY-MM-DD).

**end_date**
- string
- required
- The end date for the price data (format: YYYY-MM-DD).

**limit**
- integer
- default: 5000
- The maximum number of price records to return (default: 5000, max: 5000).
- Required range: 1 <= x <= 5000

## Response
200

200
application/json
Price data response

**prices**
- object[]

Show child attributes

## Facts (by ticker)
## Snapshot 