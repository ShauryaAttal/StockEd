import re
from difflib import get_close_matches

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


def normalize_term(value):
    value = value.casefold().strip()
    value = re.sub(r"[^a-z0-9\s]", " ", value)
    value = re.sub(r"\s+", " ", value)
    return value


def build_glossary_lookup(definitions):
    lookup = {}
    for name, entry in definitions.items():
        canonical_key = normalize_term(name)
        lookup[canonical_key] = name
        for alias in entry.get("aliases", []):
            alias_key = normalize_term(alias)
            if alias_key not in lookup:
                lookup[alias_key] = name
    return lookup


def find_glossary_matches(query, lookup):
    if not query:
        return []
    if query in lookup:
        return []

    ranked_matches = []
    for key in lookup:
        if key.startswith(query):
            ranked_matches.append(lookup[key])
        elif query in key:
            ranked_matches.append(lookup[key])

    if ranked_matches:
        return list(dict.fromkeys(ranked_matches))[:5]

    fuzzy_matches = get_close_matches(query, list(lookup.keys()), n=10, cutoff=0.5)
    if fuzzy_matches:
        return list(dict.fromkeys(lookup[match] for match in fuzzy_matches))[:5]
    return []


def display_glossary_entry(entry, display_name):
    st.markdown(f"### {display_name}")
    st.write(entry["definition"])
    st.markdown("**Example**")
    st.write(entry["example"])
    st.markdown("**Why it matters**")
    st.write(entry["why_it_matters"])

df = pd.read_csv("stock_details_5_years.csv")
# Ensure all timestamps normalize to a common timezone (UTC) to avoid
# pandas ValueError on mixed timezones (pandas 3.x).
df['Date'] = pd.to_datetime(df['Date'], utc=True)
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
definitions = {
    "Ask price": {"definition": "The ask price is the lowest price a seller is willing to accept for a stock or other asset.", "example": "If a stock has an ask price of $50, a buyer can buy it for $50 or higher if the seller accepts.", "why_it_matters": "It helps you understand what you would need to pay to buy a share.", "aliases": ["ask", "offer price"]},
    "Asset": {"definition": "An asset is something you own that may increase or decrease in value.", "example": "A house, a bond, and a stock are all examples of assets.", "why_it_matters": "Knowing what counts as an asset helps you understand what makes up your investments.", "aliases": ["investment"]},
    "Bear market": {"definition": "A bear market is a time when prices are falling and investors often feel pessimistic.", "example": "If stock prices fall by 20% or more over time, some people may say the market is in a bear market.", "why_it_matters": "It helps explain when markets are under pressure and investors may be more cautious.", "aliases": ["bear"]},
    "Beta": {"definition": "Beta measures how much a stock tends to move compared with the overall market.", "example": "A beta above 1 means the stock usually moves more than the market, while a beta below 1 often moves less.", "why_it_matters": "It is a simple way to compare a stock's risk level to the broader market.", "aliases": ["beta coefficient"]},
    "Bid price": {"definition": "The bid price is the highest price a buyer is willing to pay for a stock or other asset.", "example": "If a buyer is willing to pay $49 for a share, that is the bid price.", "why_it_matters": "It helps you understand what you might receive if you sell a share.", "aliases": ["bid", "buy price"]},
    "Bond": {"definition": "A bond is a loan made by an investor to a company or government.", "example": "When you buy a government bond, you are lending money and receiving interest over time.", "why_it_matters": "Bonds can provide income and may be less risky than stocks.", "aliases": ["government bond", "corporate bond"]},
    "Bull market": {"definition": "A bull market is a period when prices are rising and investors are feeling optimistic.", "example": "A strong upward trend in the stock market is often called a bull market.", "why_it_matters": "It helps describe periods when investors are more confident and willing to buy.", "aliases": ["bull"]},
    "Capital gain": {"definition": "A capital gain is the profit you make when you sell an investment for more than you paid.", "example": "If you bought a stock for $20 and sold it for $30, your capital gain is $10.", "why_it_matters": "It is one of the main ways investors earn money from stocks.", "aliases": ["gain"]},
    "Compound interest": {"definition": "Compound interest means you earn returns not just on your original money, but also on the returns that money has already made.", "example": "If you leave money in an account that earns interest, the interest can then earn more interest.", "why_it_matters": "It is one of the strongest reasons to invest early and leave money invested longer.", "aliases": ["compounding"]},
    "Daily return": {"definition": "A daily return is the percentage change in a stock's price from one day to the next.", "example": "If a stock rises from $100 to $103, the daily return is about 3%.", "why_it_matters": "It helps measure how much a stock moved day to day.", "aliases": ["daily change"]},
    "Diversification": {"definition": "Diversification means spreading your money across different investments so one investment does not control your overall outcome.", "example": "Holding stocks from many industries is a form of diversification.", "why_it_matters": "It can reduce risk by avoiding overexposure to one company or sector.", "aliases": ["diversify"]},
    "Dividend": {"definition": "A dividend is a payment a company may make to shareholders from its profits.", "example": "A company might pay a dividend of $1 per share each year.", "why_it_matters": "Dividends can provide income in addition to any stock price increase.", "aliases": ["dividend payment"]},
    "Dividend yield": {"definition": "Dividend yield shows how much a company pays in dividends compared with its stock price.", "example": "If a stock pays $2 in dividends and costs $40, the dividend yield is 5%.", "why_it_matters": "It helps investors compare income from different stocks.", "aliases": ["div yield", "dividend rate"]},
    "Earnings": {"definition": "Earnings are the profits a company makes after costs and expenses.", "example": "If a company makes $1 million in profit, that is its earnings.", "why_it_matters": "Earnings are a key signal of a company's financial health.", "aliases": ["profits"]},
    "Earnings per share": {"definition": "Earnings per share, or EPS, shows how much profit a company makes for each share of stock.", "example": "If a company earns $100 million and has 50 million shares, EPS is $2 per share.", "why_it_matters": "It helps investors compare companies on a per-share basis.", "aliases": ["eps", "earnings per share ratio"]},
    "ETF": {"definition": "An ETF, or exchange-traded fund, is a basket of investments that trades like a stock on an exchange.", "example": "An S&P 500 ETF holds many companies in one fund.", "why_it_matters": "ETFs can make it easier to buy a broad market exposure with one purchase.", "aliases": ["exchange traded fund"]},
    "Expense ratio": {"definition": "The expense ratio is the yearly fee a fund charges investors as a percentage of the money invested.", "example": "A fund with a 0.10% expense ratio charges 10 cents per $100 invested per year.", "why_it_matters": "Lower fees can leave more money invested for growth.", "aliases": ["fund fee"]},
    "Index": {"definition": "An index is a list or measure of many stocks that helps show how a segment of the market is performing.", "example": "The S&P 500 is an index made up of large U.S. companies.", "why_it_matters": "Indexes help investors see the broad market trend without looking at every stock individually.", "aliases": ["market index"]},
    "Liquidity": {"definition": "Liquidity means how easily an investment can be bought or sold without moving its price too much.", "example": "A very popular stock usually has high liquidity.", "why_it_matters": "Higher liquidity usually makes trading easier and can reduce costs.", "aliases": ["liquid"]},
    "Market cap": {"definition": "Market cap is the total value of a company's shares, found by multiplying the stock price by the number of shares.", "example": "If a stock costs $10 and there are 1 million shares, the market cap is $10 million.", "why_it_matters": "It helps investors understand the size of a company.", "aliases": ["market capitalization", "cap"]},
    "Market order": {"definition": "A market order is an instruction to buy or sell a stock immediately at the best available price.", "example": "If you place a market order to buy 10 shares, you will buy them at the current price if available.", "why_it_matters": "It is the fastest way to enter or exit a trade.", "aliases": ["market buy", "market sell"]},
    "Mutual fund": {"definition": "A mutual fund is a pool of money from many investors used to buy a mix of investments.", "example": "A mutual fund may own hundreds of stocks and bonds at once.", "why_it_matters": "It gives everyday investors access to broad diversification.", "aliases": ["fund"]},
    "P/E ratio": {"definition": "The P/E ratio compares a stock's price to its earnings per share.", "example": "If a stock trades at $50 and earnings per share are $5, the P/E ratio is 10.", "why_it_matters": "It helps investors judge whether a stock may be expensive or cheap compared with its earnings.", "aliases": ["PE ratio", "p e ratio", "price to earnings ratio", "price earnings ratio"]},
    "Portfolio": {"definition": "A portfolio is the collection of investments a person owns.", "example": "Your portfolio might include stocks, bonds, and savings.", "why_it_matters": "It helps you see the full picture of your investments in one place.", "aliases": ["investment portfolio"]},
    "Price return": {"definition": "Price return is the change in a stock's price over time, not including dividends.", "example": "If a stock rises from $40 to $44, the price return is 10%.", "why_it_matters": "It helps isolate how much the price itself changed.", "aliases": ["price appreciation"]},
    "Recession": {"definition": "A recession is a period when the economy shrinks for a while and many businesses struggle.", "example": "During a recession, companies may earn less and unemployment can rise.", "why_it_matters": "It helps explain why stock prices may fall when the economy is weak.", "aliases": ["economic downturn"]},
    "Risk": {"definition": "Risk is the chance that an investment may lose value or perform worse than expected.", "example": "A startup stock may have higher risk than a large, established company.", "why_it_matters": "Understanding risk helps you choose investments that fit your comfort level.", "aliases": ["risk level"]},
    "Rolling average": {"definition": "A rolling average is an average calculated over a recent window of time, such as the last 30 days.", "example": "A 30-day rolling average smooths out day-to-day ups and downs.", "why_it_matters": "It helps show the recent trend more clearly than a single day's number.", "aliases": ["moving average", "rolling mean"]},
    "Rolling volatility": {"definition": "Rolling volatility measures how much prices have moved over a recent period, often the last 30 days.", "example": "A higher rolling volatility means prices have been swinging more recently.", "why_it_matters": "It is useful for understanding recent market uncertainty.", "aliases": ["recent volatility", "moving volatility"]},
    "Share": {"definition": "A share is one small piece of ownership in a company.", "example": "If you own 10 shares of a company, you own a small part of that company.", "why_it_matters": "Shares are the basic units of stock ownership.", "aliases": ["share of stock"]},
    "Short selling": {"definition": "Short selling is a strategy where an investor borrows shares and sells them, hoping to buy them back later at a lower price.", "example": "A trader might short sell a stock that they think is about to fall.", "why_it_matters": "It shows that investors can potentially profit when prices fall.", "aliases": ["shorting"]},
    "Stock": {"definition": "A stock is a share of ownership in a company.", "example": "Buying stock means you own a tiny part of that business.", "why_it_matters": "Stocks are one of the main ways people invest in companies.", "aliases": ["shares", "equity"]},
    "Stock exchange": {"definition": "A stock exchange is a marketplace where stocks are bought and sold.", "example": "The New York Stock Exchange is a well-known stock exchange.", "why_it_matters": "It gives buyers and sellers a place to trade investments.", "aliases": ["exchange"]},
    "Stock split": {"definition": "A stock split increases the number of shares while lowering the price per share, without changing the company's overall value.", "example": "In a 2-for-1 stock split, a shareholder receives two shares for each one they owned.", "why_it_matters": "It can make a stock seem more affordable, even though the company is not worth more or less.", "aliases": ["split"]},
    "Stop-loss order": {"definition": "A stop-loss order is an instruction to sell a stock if its price falls to a certain level.", "example": "A stop-loss order can help limit losses if a stock drops quickly.", "why_it_matters": "It is a simple risk-management tool for investors.", "aliases": ["stop loss", "stop order"]},
    "Ticker symbol": {"definition": "A ticker symbol is the short code used to identify a stock on an exchange.", "example": "AAPL is the ticker symbol for Apple.", "why_it_matters": "It helps investors quickly identify a company in market data.", "aliases": ["ticker"]},
    "Total return": {"definition": "Total return includes both price changes and any income, such as dividends.", "example": "If a stock goes up 8% and pays a 2% dividend, the total return is about 10%.", "why_it_matters": "It shows the full gain from an investment, not just the price change.", "aliases": ["overall return"]},
    "Trading volume": {"definition": "Trading volume is the number of shares bought and sold in a given period.", "example": "High trading volume means many people are actively buying and selling.", "why_it_matters": "It can show how much interest there is in a stock.", "aliases": ["volume"]},
    "Valuation": {"definition": "Valuation is the estimate of what an investment or company is worth.", "example": "A company with strong growth may have a higher valuation than a slower-growing company.", "why_it_matters": "It helps investors decide whether a stock seems fairly priced.", "aliases": ["valued", "price valuation"]},
    "Volatility": {"definition": "Volatility is how much a stock's price moves up and down over time.", "example": "A stock that swings a lot from day to day is more volatile.", "why_it_matters": "It helps investors understand how much uncertainty or risk is involved.", "aliases": ["price volatility"]},
    "Yield": {"definition": "Yield is the income an investment produces as a percentage of its price.", "example": "If a bond pays $5 a year and costs $100, the yield is 5%.", "why_it_matters": "It helps investors compare the income they may receive from different investments.", "aliases": ["income yield"]},
}

lookup = build_glossary_lookup(definitions)
display_names = sorted(definitions.keys())

term = st.text_input("Search a finance term (for example: volatility, dividend, PE ratio, market):").strip()
selected_term = st.selectbox(
    "Or browse all terms:",
    ["Select a term"] + display_names,
)

if term:
    normalized_term = normalize_term(term)
    if normalized_term in lookup:
        display_glossary_entry(definitions[lookup[normalized_term]], lookup[normalized_term])
    else:
        suggestions = find_glossary_matches(normalized_term, lookup)
        if suggestions:
            st.info("No exact match found. Try one of these suggestions:")
            suggestion_choice = st.selectbox("Suggestions:", ["Select a suggestion"] + suggestions)
            if suggestion_choice != "Select a suggestion":
                display_glossary_entry(definitions[suggestion_choice], suggestion_choice)
        else:
            st.info("No exact match found. Try a simpler term or browse the list above.")
elif selected_term != "Select a term":
    display_glossary_entry(definitions[selected_term], selected_term)