"""
Portfolio simulation: Monte Carlo (GBM) and Historical Bootstrap
"""
import numpy as np
import pandas as pd
from typing import Dict, Tuple, Optional


def monte_carlo_gbm(
    returns: pd.DataFrame,
    weights: Dict[str, float],
    initial_value: float,
    horizon_days: int,
    n_simulations: int = 1000,
    return_tilt: float = 0.0,
    volatility_tilt: float = 1.0,
    seed: Optional[int] = None
) -> Tuple[np.ndarray, Dict[str, float]]:
    """
    Monte Carlo simulation using Geometric Brownian Motion

    Args:
        returns: Historical returns DataFrame
        weights: Portfolio weights
        initial_value: Starting portfolio value
        horizon_days: Simulation horizon in days
        n_simulations: Number of simulation paths
        return_tilt: Adjustment to expected return (additive)
        volatility_tilt: Adjustment to volatility (multiplicative)
        seed: Random seed for reproducibility

    Returns:
        Tuple of (simulated paths array, statistics dict)
    """
    if seed is not None:
        np.random.seed(seed)

    # Align returns with weights
    tickers = list(weights.keys())
    available_tickers = [t for t in tickers if t in returns.columns]

    if not available_tickers:
        return np.zeros((n_simulations, horizon_days + 1)), {}

    returns_subset = returns[available_tickers]
    weights_array = np.array([weights[t] for t in available_tickers])
    weights_array = weights_array / weights_array.sum()

    # Calculate portfolio parameters
    portfolio_returns = (returns_subset * weights_array).sum(axis=1)

    mu = portfolio_returns.mean() + (return_tilt / 252)  # Daily return with tilt
    sigma = portfolio_returns.std() * volatility_tilt    # Daily volatility with tilt

    # Generate simulations
    dt = 1  # Daily steps
    paths = np.zeros((n_simulations, horizon_days + 1))
    paths[:, 0] = initial_value

    for t in range(1, horizon_days + 1):
        # Generate random shocks
        Z = np.random.standard_normal(n_simulations)

        # GBM formula: S(t) = S(t-1) * exp((mu - 0.5*sigma^2)*dt + sigma*sqrt(dt)*Z)
        paths[:, t] = paths[:, t-1] * np.exp((mu - 0.5 * sigma**2) * dt + sigma * np.sqrt(dt) * Z)

    # Calculate statistics
    terminal_values = paths[:, -1]
    stats = {
        'mean': np.mean(terminal_values),
        'median': np.median(terminal_values),
        'std': np.std(terminal_values),
        'p10': np.percentile(terminal_values, 10),
        'p25': np.percentile(terminal_values, 25),
        'p50': np.percentile(terminal_values, 50),
        'p75': np.percentile(terminal_values, 75),
        'p90': np.percentile(terminal_values, 90),
        'min': np.min(terminal_values),
        'max': np.max(terminal_values)
    }

    return paths, stats


def historical_bootstrap(
    returns: pd.DataFrame,
    weights: Dict[str, float],
    initial_value: float,
    horizon_days: int,
    n_simulations: int = 1000,
    block_size: int = 1,
    seed: Optional[int] = None
) -> Tuple[np.ndarray, Dict[str, float]]:
    """
    Historical bootstrap simulation by resampling actual returns

    Args:
        returns: Historical returns DataFrame
        weights: Portfolio weights
        initial_value: Starting portfolio value
        horizon_days: Simulation horizon in days
        n_simulations: Number of simulation paths
        block_size: Size of blocks for block bootstrap (1 = simple bootstrap)
        seed: Random seed for reproducibility

    Returns:
        Tuple of (simulated paths array, statistics dict)
    """
    if seed is not None:
        np.random.seed(seed)

    # Align returns with weights
    tickers = list(weights.keys())
    available_tickers = [t for t in tickers if t in returns.columns]

    if not available_tickers:
        return np.zeros((n_simulations, horizon_days + 1)), {}

    returns_subset = returns[available_tickers]
    weights_array = np.array([weights[t] for t in available_tickers])
    weights_array = weights_array / weights_array.sum()

    # Calculate portfolio returns
    portfolio_returns = (returns_subset * weights_array).sum(axis=1).values

    # Generate simulations
    paths = np.zeros((n_simulations, horizon_days + 1))
    paths[:, 0] = initial_value

    for sim in range(n_simulations):
        # Sample returns with replacement
        if block_size == 1:
            sampled_returns = np.random.choice(portfolio_returns, size=horizon_days, replace=True)
        else:
            # Block bootstrap
            n_blocks = int(np.ceil(horizon_days / block_size))
            sampled_returns = []
            for _ in range(n_blocks):
                start_idx = np.random.randint(0, len(portfolio_returns) - block_size + 1)
                sampled_returns.extend(portfolio_returns[start_idx:start_idx + block_size])
            sampled_returns = np.array(sampled_returns[:horizon_days])

        # Build path
        for t in range(1, horizon_days + 1):
            paths[sim, t] = paths[sim, t-1] * (1 + sampled_returns[t-1])

    # Calculate statistics
    terminal_values = paths[:, -1]
    stats = {
        'mean': np.mean(terminal_values),
        'median': np.median(terminal_values),
        'std': np.std(terminal_values),
        'p10': np.percentile(terminal_values, 10),
        'p25': np.percentile(terminal_values, 25),
        'p50': np.percentile(terminal_values, 50),
        'p75': np.percentile(terminal_values, 75),
        'p90': np.percentile(terminal_values, 90),
        'min': np.min(terminal_values),
        'max': np.max(terminal_values)
    }

    return paths, stats


def calculate_percentile_bands(paths: np.ndarray, percentiles: list = [10, 50, 90]) -> pd.DataFrame:
    """
    Calculate percentile bands from simulation paths

    Args:
        paths: Array of simulation paths (n_simulations x horizon)
        percentiles: List of percentiles to calculate

    Returns:
        DataFrame with percentile bands over time
    """
    horizon = paths.shape[1]

    data = {'Day': range(horizon)}
    for p in percentiles:
        data[f'P{p}'] = np.percentile(paths, p, axis=0)

    return pd.DataFrame(data)
