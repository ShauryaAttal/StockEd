# 📈 StockEd

**StockEd** is an educational stock analysis application built with **Streamlit** that helps beginner investors understand investing through interactive visualizations and simple financial concepts.

Rather than focusing on advanced trading strategies, StockEd teaches users **how to interpret historical stock performance, evaluate risk, simulate long-term investments, and learn essential finance terminology**.

---

## Features

### 📊 Historical Stock Price Visualization
- Explore **5 years of historical closing prices**
- Select companies from an interactive sidebar
- View long-term trends with clean visualizations

---

### ⚠️ Risk Analysis

StockEd calculates:

- Daily Returns
- 30-Day Rolling Volatility

The application then classifies the stock's recent volatility into:

| Risk Level | Rolling Volatility |
|------------|-------------------|
| 🟢 Low | < 0.015 |
| 🟡 Moderate | 0.015 – 0.03 |
| 🔴 High | > 0.03 |

This is intended as an educational indicator—not investment advice.

---

### 💰 Investment Growth Simulator

See how much an investment would have grown over the available historical period.

Choose an initial investment between **$100 and $10,000**, and StockEd calculates:

```
Final Investment = Initial Investment × (Ending Price / Starting Price)
```

This simulator demonstrates the power of long-term investing using historical data.

---

### 📚 Interactive Finance Glossary

StockEd includes an integrated glossary containing **40+ beginner-friendly investing terms** including:

- Volatility
- Dividend Yield
- P/E Ratio
- ETF
- Diversification
- Market Capitalization
- Compound Interest
- Short Selling
- Rolling Volatility
- Earnings Per Share
- and many more.

Each definition includes:

- ✅ Plain-English explanation
- 💡 Real-world example
- 🎯 Why the concept matters

The glossary also supports:

- Alias searching
- Partial matching
- Typo-tolerant suggestions
- Alphabetical browsing

---

# Tech Stack

- Python
- Streamlit
- pandas
- NumPy
- Matplotlib

---

# Project Structure

```
StockEd/
│
├── app.py
├── stock_details_5_years.csv
├── requirements.txt
└── README.md
```

---

# How It Works

### Historical Data

StockEd reads historical stock prices from:

```
stock_details_5_years.csv
```

The application normalizes timestamps to UTC before processing to ensure compatibility with modern versions of pandas and mixed timezone datasets. 

---

### Daily Return

Daily Return measures the percentage price change from one trading day to the next.

```
(Current Close ÷ Previous Close) − 1
```

---

### Rolling Volatility

Risk is estimated using the **30-day rolling standard deviation of daily returns**.

Higher volatility indicates larger recent price swings.

---

# Educational Purpose

StockEd was built to make investing more approachable by helping users answer questions like:

- What does volatility actually mean?
- How risky has this stock been recently?
- What would my investment have grown to?
- What is a P/E ratio?
- What is an ETF?
- Why does diversification matter?

The project emphasizes **financial literacy** over stock picking.

---

# Future Improvements

Potential enhancements include:

- Company fundamentals (P/E, EPS, Market Cap)
- Benchmark comparison (S&P 500)
- Dividend-adjusted returns
- Sharpe Ratio
- Maximum Drawdown
- CAGR calculations
- Sector filtering
- Interactive Plotly charts
- Live market data integration
- Portfolio simulator

---

# Disclaimer

StockEd is intended for **educational purposes only**.

It should **not** be interpreted as financial or investment advice.

Past performance does not guarantee future results.

---

# Author

**Shaurya Attal**

GitHub: https://github.com/ShauryaAttal
