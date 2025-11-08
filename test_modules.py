"""
Quick test script to verify all modules are working correctly
Run this before launching the app to ensure all dependencies are installed
"""

import sys

def test_imports():
    """Test that all required packages can be imported"""
    print("Testing imports...")

    try:
        import streamlit as st
        print("✓ Streamlit imported successfully")
    except ImportError as e:
        print(f"✗ Streamlit import failed: {e}")
        return False

    try:
        import yfinance as yf
        print("✓ yfinance imported successfully")
    except ImportError as e:
        print(f"✗ yfinance import failed: {e}")
        return False

    try:
        import numpy as np
        print("✓ NumPy imported successfully")
    except ImportError as e:
        print(f"✗ NumPy import failed: {e}")
        return False

    try:
        import pandas as pd
        print("✓ Pandas imported successfully")
    except ImportError as e:
        print(f"✗ Pandas import failed: {e}")
        return False

    try:
        import plotly.graph_objects as go
        print("✓ Plotly imported successfully")
    except ImportError as e:
        print(f"✗ Plotly import failed: {e}")
        return False

    try:
        import matplotlib.pyplot as plt
        print("✓ Matplotlib imported successfully")
    except ImportError as e:
        print(f"✗ Matplotlib import failed: {e}")
        return False

    try:
        import seaborn as sns
        print("✓ Seaborn imported successfully")
    except ImportError as e:
        print(f"✗ Seaborn import failed: {e}")
        return False

    try:
        from sklearn.decomposition import PCA
        from sklearn.cluster import KMeans
        print("✓ scikit-learn imported successfully")
    except ImportError as e:
        print(f"✗ scikit-learn import failed: {e}")
        return False

    try:
        import cvxpy as cp
        print("✓ CVXPY imported successfully")
    except ImportError as e:
        print(f"✗ CVXPY import failed: {e}")
        return False

    return True


def test_custom_modules():
    """Test that all custom modules can be imported"""
    print("\nTesting custom modules...")

    try:
        import data_yf
        print("✓ data_yf module imported successfully")
    except ImportError as e:
        print(f"✗ data_yf import failed: {e}")
        return False

    try:
        import portfolio
        print("✓ portfolio module imported successfully")
    except ImportError as e:
        print(f"✗ portfolio import failed: {e}")
        return False

    try:
        import simulate
        print("✓ simulate module imported successfully")
    except ImportError as e:
        print(f"✗ simulate import failed: {e}")
        return False

    try:
        import optimize
        print("✓ optimize module imported successfully")
    except ImportError as e:
        print(f"✗ optimize import failed: {e}")
        return False

    try:
        import analytics
        print("✓ analytics module imported successfully")
    except ImportError as e:
        print(f"✗ analytics import failed: {e}")
        return False

    try:
        import report
        print("✓ report module imported successfully")
    except ImportError as e:
        print(f"✗ report import failed: {e}")
        return False

    return True


def test_basic_functionality():
    """Test basic functionality of core modules"""
    print("\nTesting basic functionality...")

    try:
        from portfolio import Portfolio
        p = Portfolio()
        p.add_stock("AAPL", 10, 150.0)
        assert p.get_total_value() == 1500.0
        print("✓ Portfolio class working correctly")
    except Exception as e:
        print(f"✗ Portfolio test failed: {e}")
        return False

    try:
        import numpy as np
        import pandas as pd
        from simulate import monte_carlo_gbm

        # Create dummy data
        dates = pd.date_range('2023-01-01', periods=100)
        returns = pd.DataFrame({
            'AAPL': np.random.randn(100) * 0.02,
            'MSFT': np.random.randn(100) * 0.02
        }, index=dates)

        weights = {'AAPL': 0.5, 'MSFT': 0.5}
        paths, stats = monte_carlo_gbm(returns, weights, 10000, 30, 100, seed=42)

        assert paths.shape == (100, 31)
        assert 'p50' in stats
        print("✓ Monte Carlo simulation working correctly")
    except Exception as e:
        print(f"✗ Simulation test failed: {e}")
        return False

    try:
        import numpy as np
        import pandas as pd
        from optimize import optimize_max_sharpe

        # Create dummy data
        dates = pd.date_range('2023-01-01', periods=100)
        returns = pd.DataFrame({
            'AAPL': np.random.randn(100) * 0.02 + 0.0005,
            'MSFT': np.random.randn(100) * 0.015 + 0.0004
        }, index=dates)

        weights = optimize_max_sharpe(returns, risk_free_rate=0.02)

        assert len(weights) > 0
        assert abs(sum(weights.values()) - 1.0) < 0.01
        print("✓ Portfolio optimization working correctly")
    except Exception as e:
        print(f"✗ Optimization test failed: {e}")
        return False

    return True


def main():
    """Run all tests"""
    print("=" * 60)
    print("Portfolio Vision - Module Test Suite")
    print("=" * 60)
    print()

    print(f"Python version: {sys.version}")
    print()

    # Run tests
    imports_ok = test_imports()
    if not imports_ok:
        print("\n❌ Import tests failed!")
        print("Please run: pip install -r requirements.txt")
        return False

    modules_ok = test_custom_modules()
    if not modules_ok:
        print("\n❌ Custom module tests failed!")
        print("Please ensure all .py files are in the same directory")
        return False

    functionality_ok = test_basic_functionality()
    if not functionality_ok:
        print("\n❌ Functionality tests failed!")
        return False

    print("\n" + "=" * 60)
    print("✅ All tests passed successfully!")
    print("=" * 60)
    print("\nYou're ready to run the app:")
    print("  streamlit run app.py")
    print()

    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
