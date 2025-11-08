"""
Data fetching and caching module using yfinance
"""
import yfinance as yf
import pandas as pd
import streamlit as st
from datetime import datetime, timedelta
from typing import List, Dict, Optional, Tuple


@st.cache_data(ttl=3600)
def fetch_stock_data(ticker: str, start_date: str, end_date: str, interval: str = "1d") -> pd.DataFrame:
    """
    Fetch historical stock data from yfinance with caching

    Args:
        ticker: Stock symbol
        start_date: Start date (YYYY-MM-DD)
        end_date: End date (YYYY-MM-DD)
        interval: Data interval (1d, 1wk, 1mo)

    Returns:
        DataFrame with historical price data
    """
    try:
        stock = yf.Ticker(ticker)
        df = stock.history(start=start_date, end=end_date, interval=interval)
        if df.empty:
            st.warning(f"No data found for {ticker}")
            return pd.DataFrame()
        return df
    except Exception as e:
        st.error(f"Error fetching data for {ticker}: {str(e)}")
        return pd.DataFrame()


@st.cache_data(ttl=3600)
def fetch_multiple_stocks(tickers: List[str], start_date: str, end_date: str, interval: str = "1d") -> Dict[str, pd.DataFrame]:
    """
    Fetch data for multiple stocks

    Args:
        tickers: List of stock symbols
        start_date: Start date
        end_date: End date
        interval: Data interval

    Returns:
        Dictionary mapping ticker to DataFrame
    """
    data = {}
    for ticker in tickers:
        df = fetch_stock_data(ticker, start_date, end_date, interval)
        if not df.empty:
            data[ticker] = df
    return data


@st.cache_data(ttl=300)
def get_current_price(ticker: str) -> Optional[float]:
    """
    Get the current/latest price for a ticker

    Args:
        ticker: Stock symbol

    Returns:
        Current price or None
    """
    try:
        stock = yf.Ticker(ticker)
        # Try to get real-time quote first
        info = stock.info
        price = info.get('currentPrice') or info.get('regularMarketPrice')

        if price is None:
            # Fallback to last close
            hist = stock.history(period="5d")
            if not hist.empty:
                price = hist['Close'].iloc[-1]

        return float(price) if price else None
    except Exception as e:
        st.error(f"Error getting current price for {ticker}: {str(e)}")
        return None


# Popular stocks database for quick suggestions
POPULAR_STOCKS = {
    # Technology
    'AAPL': {'name': 'Apple Inc.', 'sector': 'Technology', 'industry': 'Consumer Electronics'},
    'MSFT': {'name': 'Microsoft Corporation', 'sector': 'Technology', 'industry': 'Software'},
    'GOOGL': {'name': 'Alphabet Inc. (Google)', 'sector': 'Technology', 'industry': 'Internet Services'},
    'GOOG': {'name': 'Alphabet Inc. Class C', 'sector': 'Technology', 'industry': 'Internet Services'},
    'AMZN': {'name': 'Amazon.com Inc.', 'sector': 'Technology', 'industry': 'E-commerce'},
    'META': {'name': 'Meta Platforms Inc. (Facebook)', 'sector': 'Technology', 'industry': 'Social Media'},
    'NVDA': {'name': 'NVIDIA Corporation', 'sector': 'Technology', 'industry': 'Semiconductors'},
    'TSLA': {'name': 'Tesla Inc.', 'sector': 'Technology', 'industry': 'Electric Vehicles'},
    'AMD': {'name': 'Advanced Micro Devices', 'sector': 'Technology', 'industry': 'Semiconductors'},
    'INTC': {'name': 'Intel Corporation', 'sector': 'Technology', 'industry': 'Semiconductors'},
    'CRM': {'name': 'Salesforce Inc.', 'sector': 'Technology', 'industry': 'Software'},
    'ORCL': {'name': 'Oracle Corporation', 'sector': 'Technology', 'industry': 'Software'},
    'ADBE': {'name': 'Adobe Inc.', 'sector': 'Technology', 'industry': 'Software'},
    'NFLX': {'name': 'Netflix Inc.', 'sector': 'Technology', 'industry': 'Streaming'},
    'PYPL': {'name': 'PayPal Holdings', 'sector': 'Technology', 'industry': 'Fintech'},
    'SQ': {'name': 'Block Inc. (Square)', 'sector': 'Technology', 'industry': 'Fintech'},
    'SHOP': {'name': 'Shopify Inc.', 'sector': 'Technology', 'industry': 'E-commerce'},
    'UBER': {'name': 'Uber Technologies', 'sector': 'Technology', 'industry': 'Ridesharing'},
    'SNOW': {'name': 'Snowflake Inc.', 'sector': 'Technology', 'industry': 'Cloud Computing'},

    # Finance
    'JPM': {'name': 'JPMorgan Chase & Co.', 'sector': 'Finance', 'industry': 'Banking'},
    'BAC': {'name': 'Bank of America', 'sector': 'Finance', 'industry': 'Banking'},
    'WFC': {'name': 'Wells Fargo', 'sector': 'Finance', 'industry': 'Banking'},
    'GS': {'name': 'Goldman Sachs', 'sector': 'Finance', 'industry': 'Investment Banking'},
    'MS': {'name': 'Morgan Stanley', 'sector': 'Finance', 'industry': 'Investment Banking'},
    'V': {'name': 'Visa Inc.', 'sector': 'Finance', 'industry': 'Payment Processing'},
    'MA': {'name': 'Mastercard Inc.', 'sector': 'Finance', 'industry': 'Payment Processing'},
    'AXP': {'name': 'American Express', 'sector': 'Finance', 'industry': 'Financial Services'},
    'BRK.B': {'name': 'Berkshire Hathaway', 'sector': 'Finance', 'industry': 'Conglomerate'},

    # Healthcare
    'JNJ': {'name': 'Johnson & Johnson', 'sector': 'Healthcare', 'industry': 'Pharmaceuticals'},
    'UNH': {'name': 'UnitedHealth Group', 'sector': 'Healthcare', 'industry': 'Health Insurance'},
    'PFE': {'name': 'Pfizer Inc.', 'sector': 'Healthcare', 'industry': 'Pharmaceuticals'},
    'ABBV': {'name': 'AbbVie Inc.', 'sector': 'Healthcare', 'industry': 'Pharmaceuticals'},
    'TMO': {'name': 'Thermo Fisher Scientific', 'sector': 'Healthcare', 'industry': 'Life Sciences'},
    'ABT': {'name': 'Abbott Laboratories', 'sector': 'Healthcare', 'industry': 'Medical Devices'},
    'CVS': {'name': 'CVS Health', 'sector': 'Healthcare', 'industry': 'Pharmacy'},
    'LLY': {'name': 'Eli Lilly and Company', 'sector': 'Healthcare', 'industry': 'Pharmaceuticals'},
    'MRK': {'name': 'Merck & Co.', 'sector': 'Healthcare', 'industry': 'Pharmaceuticals'},

    # Consumer
    'WMT': {'name': 'Walmart Inc.', 'sector': 'Consumer', 'industry': 'Retail'},
    'HD': {'name': 'Home Depot', 'sector': 'Consumer', 'industry': 'Retail'},
    'MCD': {'name': 'McDonald\'s Corporation', 'sector': 'Consumer', 'industry': 'Restaurants'},
    'NKE': {'name': 'Nike Inc.', 'sector': 'Consumer', 'industry': 'Apparel'},
    'SBUX': {'name': 'Starbucks Corporation', 'sector': 'Consumer', 'industry': 'Restaurants'},
    'KO': {'name': 'The Coca-Cola Company', 'sector': 'Consumer', 'industry': 'Beverages'},
    'PEP': {'name': 'PepsiCo Inc.', 'sector': 'Consumer', 'industry': 'Beverages'},
    'PG': {'name': 'Procter & Gamble', 'sector': 'Consumer', 'industry': 'Consumer Goods'},
    'DIS': {'name': 'The Walt Disney Company', 'sector': 'Consumer', 'industry': 'Entertainment'},
    'COST': {'name': 'Costco Wholesale', 'sector': 'Consumer', 'industry': 'Retail'},

    # Energy
    'XOM': {'name': 'Exxon Mobil', 'sector': 'Energy', 'industry': 'Oil & Gas'},
    'CVX': {'name': 'Chevron Corporation', 'sector': 'Energy', 'industry': 'Oil & Gas'},
    'COP': {'name': 'ConocoPhillips', 'sector': 'Energy', 'industry': 'Oil & Gas'},

    # ETFs
    'SPY': {'name': 'SPDR S&P 500 ETF', 'sector': 'ETF', 'industry': 'Index Fund'},
    'QQQ': {'name': 'Invesco QQQ Trust', 'sector': 'ETF', 'industry': 'Nasdaq-100 Index'},
    'DIA': {'name': 'SPDR Dow Jones Industrial Average ETF', 'sector': 'ETF', 'industry': 'Index Fund'},
    'IWM': {'name': 'iShares Russell 2000 ETF', 'sector': 'ETF', 'industry': 'Small Cap Index'},
    'VTI': {'name': 'Vanguard Total Stock Market ETF', 'sector': 'ETF', 'industry': 'Index Fund'},
    'VOO': {'name': 'Vanguard S&P 500 ETF', 'sector': 'ETF', 'industry': 'Index Fund'},
}


def search_stock_suggestions(query: str, max_results: int = 10) -> List[Dict[str, str]]:
    """
    Search for stock suggestions based on ticker or company name

    Args:
        query: Search query (ticker symbol or company name)
        max_results: Maximum number of results to return

    Returns:
        List of matching stock info dictionaries
    """
    if not query or len(query) < 1:
        # Return top popular stocks if no query
        popular = [
            {'symbol': k, **v}
            for k, v in list(POPULAR_STOCKS.items())[:max_results]
        ]
        return popular

    query_upper = query.upper()
    query_lower = query.lower()

    results = []

    # Search in popular stocks database
    for symbol, info in POPULAR_STOCKS.items():
        # Match by ticker symbol
        if query_upper in symbol:
            results.append({
                'symbol': symbol,
                'name': info['name'],
                'sector': info['sector'],
                'industry': info['industry']
            })
        # Match by company name
        elif query_lower in info['name'].lower():
            results.append({
                'symbol': symbol,
                'name': info['name'],
                'sector': info['sector'],
                'industry': info['industry']
            })

    # Sort results: exact matches first, then partial matches
    results.sort(key=lambda x: (
        0 if x['symbol'] == query_upper else 1,  # Exact ticker match first
        0 if x['symbol'].startswith(query_upper) else 1,  # Ticker starts with query
        x['symbol']  # Alphabetical
    ))

    return results[:max_results]


@st.cache_data(ttl=3600)
def search_ticker(query: str) -> List[Dict[str, str]]:
    """
    Search for ticker symbols (simplified version)

    Args:
        query: Search query

    Returns:
        List of matching ticker info
    """
    try:
        ticker = yf.Ticker(query.upper())
        info = ticker.info

        if info and 'symbol' in info:
            return [{
                'symbol': info.get('symbol', query.upper()),
                'name': info.get('longName', info.get('shortName', 'N/A')),
                'sector': info.get('sector', 'N/A'),
                'industry': info.get('industry', 'N/A')
            }]
        return []
    except:
        return []


@st.cache_data(ttl=3600)
def get_stock_info(ticker: str) -> Dict:
    """
    Get detailed stock information

    Args:
        ticker: Stock symbol

    Returns:
        Dictionary with stock info
    """
    try:
        stock = yf.Ticker(ticker)
        info = stock.info
        return {
            'name': info.get('longName', info.get('shortName', ticker)),
            'sector': info.get('sector', 'N/A'),
            'industry': info.get('industry', 'N/A'),
            'market_cap': info.get('marketCap', 0),
            'currency': info.get('currency', 'USD')
        }
    except:
        return {
            'name': ticker,
            'sector': 'N/A',
            'industry': 'N/A',
            'market_cap': 0,
            'currency': 'USD'
        }


def get_returns_dataframe(data_dict: Dict[str, pd.DataFrame]) -> pd.DataFrame:
    """
    Convert price data to returns DataFrame

    Args:
        data_dict: Dictionary mapping ticker to price DataFrame

    Returns:
        DataFrame with returns for each ticker
    """
    prices = pd.DataFrame()

    for ticker, df in data_dict.items():
        if 'Close' in df.columns:
            prices[ticker] = df['Close']

    if prices.empty:
        return pd.DataFrame()

    # Calculate daily returns
    returns = prices.pct_change().dropna()
    return returns


def get_last_refresh_time() -> str:
    """
    Get the current timestamp for data refresh tracking

    Returns:
        Formatted timestamp string
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
