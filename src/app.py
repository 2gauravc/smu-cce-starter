import streamlit as st

from analysis import run_analysis


st.set_page_config(page_title="Finance Explorer", page_icon="📈")
st.title("Finance Explorer")
st.write("Use a ticker symbol to explore financial data, news, and analyst ratings.")

# Input controls
ticker = st.text_input("Ticker symbol", value="AAPL", help="Example: AAPL, GOOG, MSFT").strip().upper()
analysis_type = st.selectbox(
    "Choose analysis type",
    ["filings", "news", "stock price ratings"],
)

if st.button("Run"):
    if not ticker:
        st.warning("Please enter a ticker symbol before running the analysis.")
    else:
        try:
            result = run_analysis(analysis_type, ticker)

            if analysis_type == "filings":
                st.subheader(f"Financial statements for {result['ticker']}")
                st.write("Income Statement")
                st.dataframe(result["income_statement"])
                st.write("Balance Sheet")
                st.dataframe(result["balance_sheet"])
                st.write("Cash Flow")
                st.dataframe(result["cash_flow"])

            elif analysis_type == "news":
                st.subheader(f"Latest news for {result['ticker']}")
                news_data = result["news"]
                if "message" in news_data.columns:
                    st.info(news_data.iloc[0]["message"])
                else:
                    for _, article in news_data.head(5).iterrows():
                        st.write(f"### {article['title']}")
                        st.write(article["description"])
                        if article.get("link"):
                            st.write(f"Source: {article['link']}")
                        st.write("---")

            else:
                st.subheader(f"Price and ratings for {result['ticker']}")
                price = result.get("price")
                if price is not None:
                    st.metric("Current Price", f"${price:,.2f}")

                ratings = result["ratings"]
                if "message" in ratings.columns:
                    st.info(ratings.iloc[0]["message"])
                else:
                    st.dataframe(ratings)

        except Exception as exc:
            st.error(f"Something went wrong: {exc}")
            st.write("Try a different ticker symbol or choose another analysis type.")
