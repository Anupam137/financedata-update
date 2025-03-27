# Institutional Ownership - Ownership (by investor)
Get institutional ownership by investor or ticker. Requires either investor or ticker parameter, but not both.

## GET /institutional-ownership

Try it

## 👋 Overview
The institutional ownership API provides access to the equity holdings of investment managers overseeing $100M+ in assets.

This quarterly data comes directly from Form 13F filings and includes tickers, share quantities, estimated holding prices, and market values.

When you query by investor, the API returns the holdings of the specified investor.

You can use this data to:

- Track position changes of major hedge funds and asset managers
- Identify emerging sector rotations and market themes
- Build investment strategies based on institutional money flows
- Monitor industry concentration and portfolio overlap

Note: Form 13F filings have a 45-day lag from quarter end and only include long positions in SEC-registered securities.

To get started, please create an account and grab your API key at financialdatasets.ai.

You will use the API key to authenticate your API requests.

## 📊 Available Investors
You can fetch a list of available investors with a GET request to: https://api.financialdatasets.ai/institutional-ownership/investors/

## 🚀 Getting Started
There are only 3 steps for making a successful API call:

1. Add your API key to the header of the request as X-API-KEY.
2. Add query params like investor and limit to filter the data.
3. Execute the API request.

## 🔎 Filtering the Data
You can filter the data by investor, limit, and report_period.

Note: investor is required required. By default, limit is 10 and report_period is null.

The limit parameter is used to specify the number of periods to return.

The report_period parameter is used to specify the date of the holdings. For example, you can include filters like report_period_lte=2024-09-30 and report_period_gte=2024-01-01 to get holdings between January 1, 2024 and September 30, 2024.

The available report_period operations are:

- report_period_lte
- report_period_lt
- report_period_gte
- report_period_gt
- report_period

## 💻 Example
Institutional Ownership

```python
import requests

# add your API key to the headers
headers = {
    "X-API-KEY": "your_api_key_here"
}

# set your query params
investor = 'BERKSHIRE_HATHAWAY_INC'     # investor name
limit = 100                             # number of holdings to return

# create the URL
url = (
    f'https://api.financialdatasets.ai/institutional-ownership/'
    f'?investor={investor}'
    f'&limit={limit}'
)

# make API request
response = requests.get(url, headers=headers)

# parse institutional_ownership from the response
institutional_ownership = response.json().get('institutional_ownership')
```

## 💻 Example (with report_period)
Institutional Ownership

```python
import requests

# add your API key to the headers
headers = {
    "X-API-KEY": "your_api_key_here"
}

# set your query params
investor = 'BERKSHIRE_HATHAWAY_INC'     
limit = 100      
report_period_lte = '2024-01-01' # end date
report_period_gte = '2020-01-01' # start date

# create the URL
url = (
    f'https://api.financialdatasets.ai/institutional-ownership'
    f'?investor={investor}'
    f'&limit={limit}'
    f'&report_period_lte={report_period_lte}'
    f'&report_period_gte={report_period_gte}'
)

# make API request
response = requests.get(url, headers=headers)

# parse institutional_ownership from the response
institutional_ownership = response.json().get('institutional_ownership')
```

## Authorizations

**X-API-KEY**
- string
- header
- required
- API key for authentication.

## Query Parameters

**investor**
- string
- The name of the investment manager

**ticker**
- string
- The ticker symbol, if queried by investor.

**limit**
- integer
- default: 10
- The maximum number of holdings to return (default: 10).

## Response
200

200
application/json
Institutional ownership response

**institutional_ownership**
- object[]

Show child attributes

## Trades (by ticker)
## Ownership (by ticker) 