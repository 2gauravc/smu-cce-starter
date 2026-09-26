"""Simple financial data helpers extracted from the project notebooks.

These functions keep the logic easy to understand for students while still
matching the notebook examples for filings, news, and stock price ratings.
"""

from __future__ import annotations

import pandas as pd
import yfinance as yf


def _clean_ticker(ticker: str) -> str:
    """Normalize a stock ticker before using it."""
    if ticker is None:
        raise ValueError("Ticker symbol is required.")

    cleaned = ticker.strip().upper()
    if not cleaned:
        raise ValueError("Ticker symbol is required.")
    return cleaned


def _empty_table(message: str) -> pd.DataFrame:
    """Create a small DataFrame for empty or missing results."""
    return pd.DataFrame([{"message": message}])


def get_financials(ticker: str) -> dict:
    """Return a beginner-friendly view of a company's financial statements."""
    ticker = _clean_ticker(ticker)
    stock = yf.Ticker(ticker)

    income_statement = stock.financials
    balance_sheet = stock.balance_sheet
    cash_flow = stock.cashflow

    if income_statement is None or income_statement.empty:
        income_statement = _empty_table(f"No income statement data found for {ticker}.")
    if balance_sheet is None or balance_sheet.empty:
        balance_sheet = _empty_table(f"No balance sheet data found for {ticker}.")
    if cash_flow is None or cash_flow.empty:
        cash_flow = _empty_table(f"No cash flow data found for {ticker}.")

    return {
        "ticker": ticker,
        "income_statement": income_statement.head(10),
        "balance_sheet": balance_sheet.head(10),
        "cash_flow": cash_flow.head(10),
    }


def get_news(ticker: str) -> dict:
    """Return the latest news items for a stock ticker."""
    ticker = _clean_ticker(ticker)
    stock = yf.Ticker(ticker)
    news = stock.news or []

    articles = []
    for article in news[:5]:
        content = article.get("content", {}) if isinstance(article, dict) else {}
        title = content.get("title") or article.get("title") or "No title"
        description = content.get("description") or article.get("summary") or "No description"
        link = content.get("canonicalUrl") or article.get("link") or ""
        articles.append(
            {
                "title": title,
                "description": description[:250],
                "link": link,
            }
        )

    if not articles:
        return {
            "ticker": ticker,
            "news": _empty_table(f"No news reported for {ticker} right now."),
        }

    return {
        "ticker": ticker,
        "news": pd.DataFrame(articles),
    }


def get_price(ticker: str) -> dict:
    """Return the latest stock price for a ticker."""
    ticker = _clean_ticker(ticker)
    stock = yf.Ticker(ticker)
    info = getattr(stock, "info", {}) or {}

    price = (
        info.get("currentPrice")
        or info.get("regularMarketPrice")
        or info.get("previousClose")
    )

    if price is None:
        raise ValueError(f"Could not find a current price for {ticker}.")

    return {
        "ticker": ticker,
        "price": float(price),
    }


def get_analyst_ratings(ticker: str) -> dict:
    """Return recent analyst recommendation history for a ticker."""
    ticker = _clean_ticker(ticker)
    stock = yf.Ticker(ticker)
    recommendations = stock.recommendations

    if recommendations is None or recommendations.empty:
        return {
            "ticker": ticker,
            "ratings": _empty_table(f"No analyst ratings found for {ticker}."),
        }

    return {
        "ticker": ticker,
        "ratings": recommendations.tail(10).reset_index(),
    }


def get_stock_price_ratings(ticker: str) -> dict:
    """Return both the current price and analyst ratings for a ticker."""
    ticker = _clean_ticker(ticker)
    price_result = get_price(ticker)
    ratings_result = get_analyst_ratings(ticker)

    return {
        "ticker": ticker,
        "price": price_result["price"],
        "ratings": ratings_result["ratings"],
    }


def run_analysis(analysis_type: str, ticker: str) -> dict:
    """Route the request to the correct notebook-based function."""
    analysis_name = (analysis_type or "").strip().lower()

    handlers = {
        "filings": get_financials,
        "news": get_news,
        "stock price ratings": get_stock_price_ratings,
    }

    if "price" in analysis_name or "rating" in analysis_name:
        analysis_name = "stock price ratings"

    if analysis_name not in handlers:
        raise ValueError("Unsupported analysis type. Choose filings, news, or stock price ratings.")

    return handlers[analysis_name](ticker)


if __name__ == "__main__":
    # Quick manual check for students.
    print(get_price("AAPL"))
