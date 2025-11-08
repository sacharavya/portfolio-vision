"""
Portfolio optimization using Markowitz mean-variance optimization
"""
import numpy as np
import pandas as pd
import cvxpy as cp
from typing import Dict, Tuple, List, Optional


def calculate_expected_returns(returns: pd.DataFrame, method: str = 'mean') -> np.ndarray:
    """
    Calculate expected returns for assets

    Args:
        returns: Historical returns DataFrame
        method: Method to use ('mean', 'ewma')

    Returns:
        Array of expected annual returns
    """
    if method == 'mean':
        return returns.mean().values * 252
    elif method == 'ewma':
        # Exponentially weighted moving average
        return returns.ewm(span=60).mean().iloc[-1].values * 252
    else:
        return returns.mean().values * 252


def calculate_covariance_matrix(returns: pd.DataFrame) -> np.ndarray:
    """
    Calculate annualized covariance matrix

    Args:
        returns: Historical returns DataFrame

    Returns:
        Annualized covariance matrix
    """
    return returns.cov().values * 252


def optimize_max_sharpe(
    returns: pd.DataFrame,
    risk_free_rate: float = 0.02,
    target_return: Optional[float] = None
) -> Dict[str, float]:
    """
    Optimize portfolio for maximum Sharpe ratio

    Args:
        returns: Historical returns DataFrame
        risk_free_rate: Annual risk-free rate
        target_return: Optional target return constraint

    Returns:
        Dictionary mapping ticker to optimal weight
    """
    n_assets = len(returns.columns)

    # Calculate parameters
    mu = calculate_expected_returns(returns)
    Sigma = calculate_covariance_matrix(returns)

    # Define optimization variables
    w = cp.Variable(n_assets)

    # Objective: Maximize Sharpe ratio
    # We minimize the inverse: minimize variance / (return - rf)
    # Reformulated as: minimize w.T @ Sigma @ w subject to w.T @ mu = 1 + rf
    portfolio_return = mu @ w
    portfolio_variance = cp.quad_form(w, Sigma)

    # Constraints
    constraints = [
        cp.sum(w) == 1,  # Weights sum to 1
        w >= 0           # No short selling
    ]

    # Add target return constraint if specified
    if target_return is not None:
        constraints.append(portfolio_return >= target_return)

    # Maximize Sharpe: maximize (return - rf) / sqrt(variance)
    # Equivalent to: minimize variance, subject to return >= threshold
    # We'll use a different formulation: maximize return / sqrt(variance)

    # Alternative: Solve by maximizing (mu - rf)^T @ w / sqrt(w^T @ Sigma @ w)
    # This is non-convex, so we use a reformulation

    # Standard approach: Fix return, minimize variance, then sweep returns
    # For simplicity, we'll maximize return - lambda * variance
    risk_aversion = 1.0

    objective = cp.Minimize(portfolio_variance - risk_aversion * (portfolio_return - risk_free_rate))

    # Alternative: Use the quadratic utility formulation
    objective = cp.Maximize(portfolio_return - 0.5 * risk_aversion * portfolio_variance)

    problem = cp.Problem(objective, constraints)

    try:
        problem.solve()

        if w.value is not None:
            weights = {ticker: w.value[i] for i, ticker in enumerate(returns.columns)}
            # Filter out near-zero weights
            weights = {k: v for k, v in weights.items() if v > 1e-4}
            # Normalize
            total = sum(weights.values())
            if total > 0:
                weights = {k: v/total for k, v in weights.items()}
            return weights
        else:
            return {}
    except Exception as e:
        print(f"Optimization failed: {e}")
        return {}


def optimize_min_variance(returns: pd.DataFrame) -> Dict[str, float]:
    """
    Optimize portfolio for minimum variance

    Args:
        returns: Historical returns DataFrame

    Returns:
        Dictionary mapping ticker to optimal weight
    """
    n_assets = len(returns.columns)

    # Calculate covariance matrix
    Sigma = calculate_covariance_matrix(returns)

    # Define optimization variables
    w = cp.Variable(n_assets)

    # Objective: Minimize variance
    portfolio_variance = cp.quad_form(w, Sigma)

    # Constraints
    constraints = [
        cp.sum(w) == 1,  # Weights sum to 1
        w >= 0           # No short selling
    ]

    objective = cp.Minimize(portfolio_variance)
    problem = cp.Problem(objective, constraints)

    try:
        problem.solve()

        if w.value is not None:
            weights = {ticker: w.value[i] for i, ticker in enumerate(returns.columns)}
            # Filter out near-zero weights
            weights = {k: v for k, v in weights.items() if v > 1e-4}
            # Normalize
            total = sum(weights.values())
            if total > 0:
                weights = {k: v/total for k, v in weights.items()}
            return weights
        else:
            return {}
    except Exception as e:
        print(f"Optimization failed: {e}")
        return {}


def generate_efficient_frontier(
    returns: pd.DataFrame,
    n_points: int = 50,
    risk_free_rate: float = 0.02
) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
    """
    Generate the efficient frontier

    Args:
        returns: Historical returns DataFrame
        n_points: Number of points on the frontier
        risk_free_rate: Annual risk-free rate

    Returns:
        Tuple of (returns array, volatilities array, sharpe ratios array)
    """
    n_assets = len(returns.columns)

    # Calculate parameters
    mu = calculate_expected_returns(returns)
    Sigma = calculate_covariance_matrix(returns)

    # Define optimization variables
    w = cp.Variable(n_assets)

    # Portfolio metrics
    portfolio_return = mu @ w
    portfolio_variance = cp.quad_form(w, Sigma)

    # Target returns range
    min_return = np.min(mu)
    max_return = np.max(mu)
    target_returns = np.linspace(min_return, max_return, n_points)

    efficient_returns = []
    efficient_volatilities = []
    efficient_sharpes = []

    for target in target_returns:
        # Constraints
        constraints = [
            cp.sum(w) == 1,
            w >= 0,
            portfolio_return >= target
        ]

        # Minimize variance for target return
        objective = cp.Minimize(portfolio_variance)
        problem = cp.Problem(objective, constraints)

        try:
            problem.solve()

            if w.value is not None and problem.status == 'optimal':
                ret = mu @ w.value
                vol = np.sqrt(w.value @ Sigma @ w.value)
                sharpe = (ret - risk_free_rate) / vol if vol > 0 else 0

                efficient_returns.append(ret)
                efficient_volatilities.append(vol)
                efficient_sharpes.append(sharpe)
        except:
            continue

    return (
        np.array(efficient_returns),
        np.array(efficient_volatilities),
        np.array(efficient_sharpes)
    )


def calculate_portfolio_performance(
    weights: Dict[str, float],
    returns: pd.DataFrame,
    risk_free_rate: float = 0.02
) -> Dict[str, float]:
    """
    Calculate performance metrics for a portfolio

    Args:
        weights: Portfolio weights
        returns: Historical returns DataFrame
        risk_free_rate: Annual risk-free rate

    Returns:
        Dictionary with performance metrics
    """
    tickers = list(weights.keys())
    available_tickers = [t for t in tickers if t in returns.columns]

    if not available_tickers:
        return {
            'expected_return': 0,
            'volatility': 0,
            'sharpe_ratio': 0
        }

    # Align data
    returns_subset = returns[available_tickers]
    weights_array = np.array([weights[t] for t in available_tickers])
    weights_array = weights_array / weights_array.sum()

    # Calculate parameters
    mu = calculate_expected_returns(returns_subset)
    Sigma = calculate_covariance_matrix(returns_subset)

    # Portfolio metrics
    expected_return = weights_array @ mu
    volatility = np.sqrt(weights_array @ Sigma @ weights_array)
    sharpe_ratio = (expected_return - risk_free_rate) / volatility if volatility > 0 else 0

    return {
        'expected_return': expected_return,
        'volatility': volatility,
        'sharpe_ratio': sharpe_ratio
    }
