# Financial Metrics - Historical
Get financial metrics for a ticker, including valuation, profitability, efficiency, liquidity, leverage, growth, and per share metrics.

## GET /financial-metrics

Try it

## 👋 Overview
The historical financial metrics API provides historical financial metrics and ratios for a given stock ticker.

Financial metrics include a company's valuation, profitability, efficiency, liquidity, leverage, growth, and per share metrics over a specified period.

To get started, please create an account and grab your API key at financialdatasets.ai.

You will use the API key to authenticate your API requests.

## 📊 Available Tickers
You can fetch a list of available tickers with a GET request to: https://api.financialdatasets.ai/financial-metrics/tickers/

## 🚀 Getting Started
There are only 3 steps for making a successful API call:

1. Add your API key to the header of the request as X-API-KEY.
2. Add query params like ticker to filter the data.
3. Execute the API request.

## 🔎 Filtering the Data
You can filter the data by ticker, period, limit, and report_period.

Note: ticker and period are required. By default, limit is 4 and report_period is null.

The period parameter can be set to annual, quarterly, or ttm (trailing twelve months). The limit parameter is used to specify the number of periods to return.

The report_period parameter is used to specify the date of the financial metrics. For example, you can include filters like report_period_lte=2024-09-30 and report_period_gte=2024-01-01 to get financial metrics between January 1, 2024 and September 30, 2024.

The available report_period operations are:

- report_period_lte
- report_period_lt
- report_period_gte
- report_period_gt
- report_period

## 💻 Example
Financial Metrics

```python
import requests

# add your API key to the headers
headers = {
    "X-API-KEY": "your_api_key_here"
}

# set your query params
ticker = 'NVDA'     # stock ticker
period = 'annual'   # possible values are 'annual', 'quarterly', or 'ttm'
limit = 30          # number of periods to return

# create the URL
url = (
    f'https://api.financialdatasets.ai/financial-metrics'
    f'?ticker={ticker}'
    f'&period={period}'
    f'&limit={limit}'
)

# make API request
response = requests.get(url, headers=headers)

# parse financial_metrics from the response
financial_metrics = response.json().get('financial_metrics')
```

## 💻 Example (with report_period)
Financial Metrics

```python
import requests

# add your API key to the headers
headers = {
    "X-API-KEY": "your_api_key_here"
}

# set your query params
ticker = 'NVDA'     
period = 'ttm'      
report_period_lte = '2024-01-01' # end date
report_period_gte = '2020-01-01' # start date

# create the URL
url = (
    f'https://api.financialdatasets.ai/financial-metrics'
    f'?ticker={ticker}'
    f'&period={period}'
    f'&report_period_lte={report_period_lte}'
    f'&report_period_gte={report_period_gte}'
)

# make API request
response = requests.get(url, headers=headers)

# parse financial_metrics from the response
financial_metrics = response.json().get('financial_metrics')
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

**period**
- enum<string>
- required
- The time period for the financial data.
- Available options: annual, quarterly, ttm 

**limit**
- integer
- The maximum number of results to return.

## Response
200

200
application/json
The historical financial metrics and ratios for a ticker

**ticker**
- string
- The ticker symbol of the company.

**market_cap**
- number
- The market capitalization of the company.

**enterprise_value**
- number
- The total value of the company (market cap + debt - cash).

**price_to_earnings_ratio**
- number
- Price to earnings ratio.

**price_to_book_ratio**
- number
- Price to book ratio.

**price_to_sales_ratio**
- number
- Price to sales ratio.

**enterprise_value_to_ebitda_ratio**
- number
- Enterprise value to EBITDA ratio.

**enterprise_value_to_revenue_ratio**
- number
- Enterprise value to revenue ratio.

**free_cash_flow_yield**
- number
- Free cash flow yield.

**peg_ratio**
- number
- Price to earnings growth ratio.

**gross_margin**
- number
- Gross profit as a percentage of revenue.

**operating_margin**
- number
- Operating income as a percentage of revenue.

**net_margin**
- number
- Net income as a percentage of revenue.

**return_on_equity**
- number
- Net income as a percentage of shareholders' equity.

**return_on_assets**
- number
- Net income as a percentage of total assets.

**return_on_invested_capital**
- number
- Net operating profit after taxes as a percentage of invested capital.

**asset_turnover**
- number
- Revenue divided by average total assets.

**inventory_turnover**
- number
- Cost of goods sold divided by average inventory.

**receivables_turnover**
- number
- Revenue divided by average accounts receivable.

**days_sales_outstanding**
- number
- Average accounts receivable divided by revenue over the period.

**operating_cycle**
- number
- Inventory turnover + receivables turnover.

**working_capital_turnover**
- number
- Revenue divided by average working capital.

**current_ratio**
- number
- Current assets divided by current liabilities.

**quick_ratio**
- number
- Quick assets divided by current liabilities.

**cash_ratio**
- number
- Cash and cash equivalents divided by current liabilities.

**operating_cash_flow_ratio**
- number
- Operating cash flow divided by current liabilities.

**debt_to_equity**
- number
- Total debt divided by shareholders' equity.

**debt_to_assets**
- number
- Total debt divided by total assets.

**interest_coverage**
- number
- EBIT divided by interest expense.

**revenue_growth**
- number
- Year-over-year growth in revenue.

**earnings_growth**
- number
- Year-over-year growth in earnings.

**book_value_growth**
- number
- Year-over-year growth in book value.

**earnings_per_share_growth**
- number
- Growth in earnings per share over the period.

**free_cash_flow_growth**
- number
- Growth in free cash flow over the period.

**operating_income_growth**
- number
- Growth in operating income over the period.

**ebitda_growth**
- number
- Growth in EBITDA over the period.

**payout_ratio**
- number
- Dividends paid as a percentage of net income.

**earnings_per_share**
- number
- Net income divided by weighted average shares outstanding.

**book_value_per_share**
- number
- Shareholders' equity divided by shares outstanding.

**free_cash_flow_per_share**
- number
- Free cash flow divided by shares outstanding.

## Press Releases
## Snapshot 