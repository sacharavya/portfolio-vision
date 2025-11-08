"""
Advanced analytics: correlation, PCA, clustering
"""
import numpy as np
import pandas as pd
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from typing import Tuple, Dict, List


def calculate_correlation_matrix(returns: pd.DataFrame) -> pd.DataFrame:
    """
    Calculate correlation matrix between assets

    Args:
        returns: Historical returns DataFrame

    Returns:
        Correlation matrix DataFrame
    """
    return returns.corr()


def perform_pca(returns: pd.DataFrame, n_components: int = 3) -> Tuple[PCA, pd.DataFrame, np.ndarray]:
    """
    Perform Principal Component Analysis on returns

    Args:
        returns: Historical returns DataFrame
        n_components: Number of principal components

    Returns:
        Tuple of (PCA model, loadings DataFrame, explained variance ratio)
    """
    # Standardize returns
    scaler = StandardScaler()
    returns_scaled = scaler.fit_transform(returns)

    # Perform PCA
    pca = PCA(n_components=min(n_components, len(returns.columns)))
    pca.fit(returns_scaled)

    # Get loadings (components)
    loadings = pd.DataFrame(
        pca.components_.T,
        columns=[f'PC{i+1}' for i in range(pca.n_components_)],
        index=returns.columns
    )

    return pca, loadings, pca.explained_variance_ratio_


def cluster_assets(
    returns: pd.DataFrame,
    n_clusters: int = 3,
    features: str = 'returns'
) -> Tuple[np.ndarray, pd.DataFrame]:
    """
    Cluster assets using K-means

    Args:
        returns: Historical returns DataFrame
        n_clusters: Number of clusters
        features: Features to use ('returns', 'stats', or 'both')

    Returns:
        Tuple of (cluster labels, cluster centers DataFrame)
    """
    if features == 'returns':
        # Cluster based on return patterns
        X = returns.T.values  # Assets as rows, time as columns
    elif features == 'stats':
        # Cluster based on return and volatility statistics
        mean_returns = returns.mean() * 252
        volatilities = returns.std() * np.sqrt(252)
        X = np.column_stack([mean_returns, volatilities])
    else:  # 'both'
        # Combine both
        mean_returns = returns.mean() * 252
        volatilities = returns.std() * np.sqrt(252)
        corr_features = returns.T.values
        X = np.column_stack([mean_returns, volatilities, corr_features])

    # Standardize features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Perform K-means clustering
    kmeans = KMeans(n_clusters=n_clusters, random_state=42, n_init=10)
    labels = kmeans.fit_predict(X_scaled)

    # Get cluster centers (in original space)
    centers = scaler.inverse_transform(kmeans.cluster_centers_)

    # Create DataFrame with cluster assignments
    cluster_df = pd.DataFrame({
        'Ticker': returns.columns,
        'Cluster': labels,
        'Annual Return': returns.mean().values * 252,
        'Annual Volatility': returns.std().values * np.sqrt(252)
    })

    return labels, cluster_df


def calculate_diversification_ratio(returns: pd.DataFrame, weights: Dict[str, float]) -> float:
    """
    Calculate portfolio diversification ratio

    Diversification Ratio = (Weighted Average Volatility) / (Portfolio Volatility)

    Args:
        returns: Historical returns DataFrame
        weights: Portfolio weights

    Returns:
        Diversification ratio
    """
    tickers = list(weights.keys())
    available_tickers = [t for t in tickers if t in returns.columns]

    if not available_tickers:
        return 0.0

    # Align data
    returns_subset = returns[available_tickers]
    weights_array = np.array([weights[t] for t in available_tickers])
    weights_array = weights_array / weights_array.sum()

    # Individual volatilities
    volatilities = returns_subset.std().values * np.sqrt(252)

    # Weighted average volatility
    weighted_avg_vol = weights_array @ volatilities

    # Portfolio volatility
    cov_matrix = returns_subset.cov().values * 252
    portfolio_vol = np.sqrt(weights_array @ cov_matrix @ weights_array)

    if portfolio_vol > 0:
        return weighted_avg_vol / portfolio_vol
    else:
        return 0.0


def calculate_contribution_to_risk(returns: pd.DataFrame, weights: Dict[str, float]) -> pd.DataFrame:
    """
    Calculate each asset's contribution to portfolio risk

    Args:
        returns: Historical returns DataFrame
        weights: Portfolio weights

    Returns:
        DataFrame with risk contributions
    """
    tickers = list(weights.keys())
    available_tickers = [t for t in tickers if t in returns.columns]

    if not available_tickers:
        return pd.DataFrame()

    # Align data
    returns_subset = returns[available_tickers]
    weights_array = np.array([weights[t] for t in available_tickers])
    weights_array = weights_array / weights_array.sum()

    # Covariance matrix
    cov_matrix = returns_subset.cov().values * 252

    # Portfolio variance
    portfolio_variance = weights_array @ cov_matrix @ weights_array
    portfolio_vol = np.sqrt(portfolio_variance)

    # Marginal contribution to risk
    mcr = (cov_matrix @ weights_array) / portfolio_vol if portfolio_vol > 0 else np.zeros(len(weights_array))

    # Component contribution to risk
    ccr = weights_array * mcr

    # Percentage contribution
    pct_contribution = (ccr / portfolio_vol * 100) if portfolio_vol > 0 else np.zeros(len(weights_array))

    # Create DataFrame
    risk_df = pd.DataFrame({
        'Ticker': available_tickers,
        'Weight (%)': weights_array * 100,
        'Marginal Risk': mcr,
        'Risk Contribution': ccr,
        'Risk Contribution (%)': pct_contribution
    })

    return risk_df


def analyze_sector_exposure(
    tickers: List[str],
    weights: Dict[str, float],
    stock_info: Dict[str, Dict]
) -> pd.DataFrame:
    """
    Analyze portfolio exposure by sector

    Args:
        tickers: List of tickers
        weights: Portfolio weights
        stock_info: Dictionary mapping ticker to info dict

    Returns:
        DataFrame with sector exposures
    """
    sector_exposure = {}

    for ticker in tickers:
        if ticker in weights and ticker in stock_info:
            weight = weights[ticker]
            sector = stock_info[ticker].get('sector', 'Unknown')

            if sector in sector_exposure:
                sector_exposure[sector] += weight
            else:
                sector_exposure[sector] = weight

    # Create DataFrame
    df = pd.DataFrame(list(sector_exposure.items()), columns=['Sector', 'Weight'])
    df['Weight (%)'] = df['Weight'] * 100
    df = df.sort_values('Weight', ascending=False)

    return df


def calculate_rolling_correlation(
    returns: pd.DataFrame,
    ticker1: str,
    ticker2: str,
    window: int = 60
) -> pd.Series:
    """
    Calculate rolling correlation between two assets

    Args:
        returns: Historical returns DataFrame
        ticker1: First ticker
        ticker2: Second ticker
        window: Rolling window size

    Returns:
        Series with rolling correlation
    """
    if ticker1 not in returns.columns or ticker2 not in returns.columns:
        return pd.Series()

    return returns[ticker1].rolling(window=window).corr(returns[ticker2])


def calculate_beta(returns: pd.DataFrame, ticker: str, market_ticker: str = 'SPY') -> float:
    """
    Calculate beta relative to market

    Args:
        returns: Historical returns DataFrame
        ticker: Asset ticker
        market_ticker: Market benchmark ticker

    Returns:
        Beta coefficient
    """
    if ticker not in returns.columns or market_ticker not in returns.columns:
        return 0.0

    # Calculate covariance and variance
    cov = returns[[ticker, market_ticker]].cov().loc[ticker, market_ticker]
    market_var = returns[market_ticker].var()

    if market_var > 0:
        return cov / market_var
    else:
        return 0.0
