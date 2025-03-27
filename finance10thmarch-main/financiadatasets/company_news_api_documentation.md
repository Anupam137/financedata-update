# News - Company News
Get real-time and historical news for a ticker.

## GET /news

Try it

## 👋 Overview
The News API lets you pull recent and historical news articles for a given ticker.

The data is great for understanding the latest news for a given ticker and how the sentiment for a ticker has changed over time.

Our news articles are sourced directly from publishers like The Motley Fool, Investing.com, Reuters, and more. The articles are sourced from RSS feeds.

We are actively adding more publishers to our network. If you have a publisher that you would like us to add, please reach out to us here.

To get started, please create an account and grab your API key at financialdatasets.ai.

You will use the API key to authenticate your API requests.

## 🚀 Getting Started
There are only 3 steps for making a successful API call:

1. Add your API key to the header of the request as X-API-KEY.
2. Add query params like ticker to filter the data.
3. Execute the API request.

## 💻 Example
News

```python
import requests

# add your API key to the headers
headers = {
    "X-API-KEY": "your_api_key_here"
}

# set your query params
ticker = 'AAPL'
start_date = '2024-01-02' # optional
end_date = '2024-01-05'   # optional
limit = 10                # optional, max is 100

# create the URL
url = (
    f'https://api.financialdatasets.ai/news/'
    f'?ticker={ticker}'
    f'&start_date={start_date}'
    f'&end_date={end_date}'
)

# make API request
response = requests.get(url, headers=headers)

# parse news from the response
news = response.json().get('news')
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

**start_date**
- string
- The start date for the news data (format: YYYY-MM-DD).

**end_date**
- string
- The end date for the news data (format: YYYY-MM-DD).

**limit**
- integer
- default: 100
- The maximum number of news articles to return (default: 100, max: 100).
- Required range: 1 <= x <= 100

## Response
200

200
application/json
News response

**news**
- object[]

Show child attributes

## Ownership (by ticker)
## Prices 