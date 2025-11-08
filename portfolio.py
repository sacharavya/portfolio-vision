"""
Portfolio management: holdings, weights, statistics
"""
import numpy as np
import pandas as pd
from typing import Dict, List, Tuple, Optional
from datetime import datetime


class Portfolio:
    """Portfolio management class"""

    def __init__(self):
        self.holdings: Dict[str, float] = {}  # {ticker: quantity}
        self.prices: Dict[str, float] = {}    # {ticker: price}
        self.transactions: List[Dict] = []    # Transaction history

    def add_stock(self, ticker: str, quantity: float, price: float):
        """Add stock to portfolio"""
        if ticker in self.holdings:
            self.holdings[ticker] += quantity
        else:
            self.holdings[ticker] = quantity

        self.prices[ticker] = price

        # Record transaction
        self.transactions.append({
            'timestamp': datetime.now(),
            'action': 'BUY',
            'ticker': ticker,
            'quantity': quantity,
            'price': price,
            'value': quantity * price
        })

    def remove_stock(self, ticker: str, quantity: Optional[float] = None):
        """Remove stock from portfolio"""
        if ticker not in self.holdings:
            return

        if quantity is None or quantity >= self.holdings[ticker]:
            # Remove entire holding
            qty = self.holdings[ticker]
            del self.holdings[ticker]
            if ticker in self.prices:
                price = self.prices[ticker]
                del self.prices[ticker]
        else:
            # Remove partial
            qty = quantity
            self.holdings[ticker] -= quantity
            price = self.prices.get(ticker, 0)

        # Record transaction
        self.transactions.append({
            'timestamp': datetime.now(),
            'action': 'SELL',
            'ticker': ticker,
            'quantity': qty,
            'price': price,
            'value': qty * price
        })

    def update_prices(self, prices: Dict[str, float]):
        """Update current prices for holdings"""
        for ticker, price in prices.items():
            if ticker in self.holdings:
                self.prices[ticker] = price

    def get_total_value(self) -> float:
        """Calculate total portfolio market value"""
        total = 0
        for ticker, quantity in self.holdings.items():
            price = self.prices.get(ticker, 0)
            total += quantity * price
        return total

    def get_weights(self) -> Dict[str, float]:
        """Calculate portfolio weights"""
        total_value = self.get_total_value()
        if total_value == 0:
            return {}

        weights = {}
        for ticker, quantity in self.holdings.items():
            price = self.prices.get(ticker, 0)
            value = quantity * price
            weights[ticker] = value / total_value

        return weights

    def get_holdings_dataframe(self) -> pd.DataFrame:
        """Get portfolio holdings as DataFrame"""
        if not self.holdings:
            return pd.DataFrame()

        data = []
        for ticker, quantity in self.holdings.items():
            price = self.prices.get(ticker, 0)
            value = quantity * price
            data.append({
                'Ticker': ticker,
                'Quantity': quantity,
                'Price': price,
                'Value': value
            })

        df = pd.DataFrame(data)
        total_value = df['Value'].sum()
        df['Weight (%)'] = (df['Value'] / total_value * 100) if total_value > 0 else 0

        return df

    def get_tickers(self) -> List[str]:
        """Get list of tickers in portfolio"""
        return list(self.holdings.keys())


def calculate_portfolio_stats(returns: pd.DataFrame, weights: Dict[str, float],
                              risk_free_rate: float = 0.02) -> Dict[str, float]:
    """
    Calculate portfolio statistics

    Args:
        returns: DataFrame with daily returns for each asset
        weights: Dictionary mapping ticker to weight
        risk_free_rate: Annual risk-free rate

    Returns:
        Dictionary with portfolio metrics
    """
    if returns.empty or not weights:
        return {
            'annual_return': 0,
            'annual_volatility': 0,
            'sharpe_ratio': 0,
            'total_return': 0
        }

    # Align returns with weights
    tickers = list(weights.keys())
    available_tickers = [t for t in tickers if t in returns.columns]

    if not available_tickers:
        return {
            'annual_return': 0,
            'annual_volatility': 0,
            'sharpe_ratio': 0,
            'total_return': 0
        }

    # Filter returns and normalize weights
    returns_subset = returns[available_tickers]
    weights_array = np.array([weights[t] for t in available_tickers])
    weights_array = weights_array / weights_array.sum()  # Normalize

    # Calculate portfolio returns
    portfolio_returns = (returns_subset * weights_array).sum(axis=1)

    # Annual metrics (assuming 252 trading days)
    annual_return = portfolio_returns.mean() * 252
    annual_volatility = portfolio_returns.std() * np.sqrt(252)

    # Sharpe ratio
    excess_return = annual_return - risk_free_rate
    sharpe_ratio = excess_return / annual_volatility if annual_volatility > 0 else 0

    # Total return
    total_return = (1 + portfolio_returns).cumprod().iloc[-1] - 1 if len(portfolio_returns) > 0 else 0

    return {
        'annual_return': annual_return,
        'annual_volatility': annual_volatility,
        'sharpe_ratio': sharpe_ratio,
        'total_return': total_return
    }


def calculate_asset_stats(returns: pd.DataFrame, risk_free_rate: float = 0.02) -> pd.DataFrame:
    """
    Calculate individual asset statistics

    Args:
        returns: DataFrame with returns
        risk_free_rate: Annual risk-free rate

    Returns:
        DataFrame with asset statistics
    """
    if returns.empty:
        return pd.DataFrame()

    stats = []

    for ticker in returns.columns:
        asset_returns = returns[ticker].dropna()

        annual_return = asset_returns.mean() * 252
        annual_vol = asset_returns.std() * np.sqrt(252)
        sharpe = (annual_return - risk_free_rate) / annual_vol if annual_vol > 0 else 0

        stats.append({
            'Ticker': ticker,
            'Annual Return': annual_return,
            'Annual Volatility': annual_vol,
            'Sharpe Ratio': sharpe
        })

    return pd.DataFrame(stats)
