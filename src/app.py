from datetime import datetime, timezone

import pandas as pd
import streamlit as st

from analysis import run_analysis
from analysis_storage import analysis_label, list_saved_analyses, read_analysis, save_analysis


def _markdown_table(dataframe: pd.DataFrame) -> str:
    """Render a DataFrame as a Markdown table, retaining meaningful indexes."""
    table = dataframe
    if not isinstance(dataframe.index, pd.RangeIndex):
        table = dataframe.reset_index()

    headers = [str(column) for column in table.columns]
    rows = [
        [
            "" if pd.isna(value) else str(value).replace("|", r"\|").replace("\n", "<br>")
            for value in row
        ]
        for row in table.itertuples(index=False, name=None)
    ]
    markdown_rows = [
        "| " + " | ".join(headers) + " |",
        "| " + " | ".join("---" for _ in headers) + " |",
    ]
    markdown_rows.extend("| " + " | ".join(row) + " |" for row in rows)
    return "\n".join(markdown_rows)


def _analysis_markdown(result: dict, analysis_type: str, created_at: datetime) -> str:
    """Create the Markdown document saved for the displayed analysis."""
    ticker = result["ticker"]
    sections = [
        f"# {analysis_type.title()} analysis: {ticker}",
        "",
        "## Analysis details",
        f"- **Ticker:** {ticker}",
        f"- **Analysis type:** {analysis_type}",
        "- **Selected parameters:**",
        f"  - Ticker: {ticker}",
        f"  - Analysis type: {analysis_type}",
        f"- **Created:** {created_at.strftime('%Y-%m-%d %H:%M:%S UTC')}",
        "",
        "## Results",
    ]

    if analysis_type == "filings":
        for label, key in (
            ("Income Statement", "income_statement"),
            ("Balance Sheet", "balance_sheet"),
            ("Cash Flow", "cash_flow"),
        ):
            sections.extend(["", f"### {label}", _markdown_table(result[key])])
    elif analysis_type == "news":
        news_data = result["news"]
        sections.append("")
        if "message" in news_data.columns:
            sections.append(f"> {news_data.iloc[0]['message']}")
        else:
            for _, article in news_data.head(5).iterrows():
                sections.extend(
                    [
                        f"### {article['title']}",
                        "",
                        str(article["description"]),
                    ]
                )
                if article.get("link"):
                    sections.append(f"[Source]({article['link']})")
                sections.append("")
    else:
        price = result.get("price")
        if price is not None:
            sections.extend(["", f"**Current Price:** ${price:,.2f}"])
        ratings = result["ratings"]
        sections.extend(["", "### Analyst Ratings"])
        if "message" in ratings.columns:
            sections.append(f"> {ratings.iloc[0]['message']}")
        else:
            sections.append(_markdown_table(ratings))

    return "\n".join(sections).rstrip() + "\n"


def _display_analysis(result: dict, analysis_type: str) -> None:
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


@st.dialog("Saved analysis")
def _show_saved_analysis(content: str) -> None:
    st.markdown(content)


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
    st.session_state.pop("current_analysis", None)
    if not ticker:
        st.warning("Please enter a ticker symbol before running the analysis.")
    else:
        try:
            result = run_analysis(analysis_type, ticker)
            st.session_state["current_analysis"] = {
                "result": result,
                "analysis_type": analysis_type,
                "created_at": datetime.now(timezone.utc),
            }
        except Exception as exc:
            st.error(f"Something went wrong: {exc}")
            st.write("Try a different ticker symbol or choose another analysis type.")

current_analysis = st.session_state.get("current_analysis")
if current_analysis:
    _display_analysis(current_analysis["result"], current_analysis["analysis_type"])
    if st.button("Save Analysis"):
        try:
            content = _analysis_markdown(
                current_analysis["result"],
                current_analysis["analysis_type"],
                current_analysis["created_at"],
            )
            saved_path = save_analysis(
                content,
                current_analysis["result"]["ticker"],
                current_analysis["analysis_type"],
                current_analysis["created_at"],
            )
            st.success(f"Analysis saved as {saved_path.name}.")
        except (OSError, ValueError) as exc:
            st.error(f"Could not save this analysis: {exc}")

st.header("Previous Analyses")
try:
    saved_analyses = list_saved_analyses()
except OSError as exc:
    st.error(f"Could not load previous analyses: {exc}")
    saved_analyses = []

if not saved_analyses:
    st.info("No analyses have been saved yet. Run an analysis and select Save Analysis to get started.")
else:
    selected_analysis = st.selectbox(
        "Select a saved analysis",
        saved_analyses,
        format_func=analysis_label,
    )
    if st.button("Show"):
        try:
            _show_saved_analysis(read_analysis(selected_analysis))
        except (OSError, ValueError) as exc:
            st.error(f"Could not read the selected analysis: {exc}")
