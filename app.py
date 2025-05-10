import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

df = pd.read_csv("stock_details_5_years.csv")
df['Date'] = pd.to_datetime(df['Date'])
df.sort_values(by=['Company', 'Date'], inplace=True)

# Calculate returns and rolling volatility
df['Daily Return'] = df.groupby('Company')['Close'].pct_change()
df['Rolling Volatility'] = df.groupby('Company')['Daily Return'].rolling(window=30).std().reset_index(0, drop=True)

st.title("📊 StockRiskEd: Invest Smarter, Not Harder")
st.markdown("Empowering beginner investors with easy tools to understand risk, growth, and smart investing.")

# Sidebar for company selection
company = st.sidebar.selectbox("Choose a Company", df['Company'].unique())

company_data = df[df['Company'] == company]

st.subheader(f"📈 5-Year Stock Price for {company}")
fig, ax = plt.subplots()
ax.plot(company_data['Date'], company_data['Close'], label='Close Price')
ax.set_xlabel("Date")
ax.set_ylabel("Price ($)")
ax.legend()
st.pyplot(fig)

st.subheader(f"⚠️ 30-Day Rolling Volatility for {company}")
fig2, ax2 = plt.subplots()
ax2.plot(company_data['Date'], company_data['Rolling Volatility'], color='orange')
ax2.set_xlabel("Date")
ax2.set_ylabel("Volatility")
st.pyplot(fig2)

# Interpret Risk
latest_vol = company_data['Rolling Volatility'].dropna().iloc[-1]
if latest_vol < 0.015:
    risk_level = "🟢 Low Risk"
elif latest_vol < 0.03:
    risk_level = "🟡 Moderate Risk"
else:
    risk_level = "🔴 High Risk"

st.markdown(f"### 📉 Current Risk Level: {risk_level}")
st.caption(f"Based on latest volatility: {latest_vol:.4f}. Low volatility means less price fluctuation.")

# Investment sim
st.subheader("💰 Investment Growth Simulator")
amount = st.slider("If you had invested this much 5 years ago...", min_value=100, max_value=10000, step=100)
start_price = company_data['Close'].iloc[0]
end_price = company_data['Close'].iloc[-1]
final_amount = amount * (end_price / start_price)

st.markdown("💵 Your initial investment would grow to $" + format(final_amount, '.2f') + ".")

# Glossary
st.subheader("📚 Finance Term Explainer")
term = st.text_input("Type a finance term (e.g., volatility, dividend, stock split):").strip().lower()
definitions = {
    "volatility": "Volatility refers to how much a stock's price moves up and down over time. More movement = more risk.",
    "dividend": "A dividend is a portion of a company's profit paid to shareholders. Not all stocks pay dividends.",
    "stock split": "A stock split increases the number of shares and lowers the price per share, but your total value stays the same.",
    "daily return": "This is the percent change in a stock's price from one day to the next.",
    "rolling volatility": "This is the average volatility over the last 30 days. It's a way to see recent trends in risk.",
    "market cap": "Market capitalization is the total value of a company's outstanding shares. It's calculated as stock price × number of shares.",
    "pe ratio": "The price-to-earnings ratio compares a company’s stock price to its earnings per share. It's used to assess valuation.",
    "beta": "Beta measures a stock’s volatility relative to the market. A beta >1 means it's more volatile than the market.",
    "portfolio": "A portfolio is a collection of financial investments like stocks, bonds, and cash managed by an individual or institution.",
    "asset": "An asset is anything of value owned by an individual or business, such as stocks, real estate, or equipment."
}
if term:
    st.markdown(term.title() + ": " + definitions.get(term, 'Sorry, definition not available.'))