# 📊 Portfolio Vision

**A Modern Investment Simulation and Optimization Dashboard for Beginner Investors**

Portfolio Vision is a beautiful, interactive Streamlit web application that transforms complex portfolio management concepts into an intuitive, visual learning experience. Built for curious investors and beginners, it combines real-time market data, advanced simulations, and professional-grade optimization techniques in one elegant dashboard.

![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)
![Streamlit](https://img.shields.io/badge/Streamlit-1.31+-red.svg)
![License](https://img.shields.io/badge/License-Educational-green.svg)

---

## ✨ Features

### 🔍 Live Stock Data Integration
- Search and select stocks using real-time data from Yahoo Finance
- Automatic price updates and caching for optimal performance
- Support for major stock exchanges and thousands of tickers

### 💼 Portfolio Management
- Build and manage a virtual portfolio with any combination of stocks
- Track holdings, quantities, prices, and allocations in real-time
- View comprehensive performance metrics:
  - Total market value
  - Annual return and volatility
  - Sharpe ratio (risk-adjusted returns)
  - Total return over selected period

### 🎲 Advanced Simulations
- **Monte Carlo (GBM)**: Project future portfolio values using Geometric Brownian Motion
- **Historical Bootstrap**: Simulate outcomes by resampling actual historical returns
- Fully customizable parameters:
  - Simulation horizon (days)
  - Number of simulation paths
  - Return and volatility tilts
  - Random seed for reproducibility
- Beautiful visualizations:
  - Fan charts with confidence bands (P10/P50/P90)
  - Distribution histograms of terminal values
  - Interactive Plotly charts

### 🎯 Portfolio Optimization
- **Markowitz Mean-Variance Optimization**
  - Maximum Sharpe Ratio portfolio
  - Minimum Variance portfolio
- **Efficient Frontier** visualization
- Compare current allocation vs. optimized suggestions
- No-short-selling constraints for realistic portfolios

### 📊 Advanced Analytics
- **Correlation Heatmap**: Understand how your assets move together
- **Principal Component Analysis (PCA)**: Reveal hidden factors driving portfolio variance
- **K-means Clustering**: Group similar stocks by risk-return characteristics
- **Diversification Metrics**:
  - Diversification ratio
  - Risk contribution by asset
  - Sector exposure analysis (when available)

### 📄 Professional Reports
- Generate comprehensive markdown reports
- Downloadable CSV exports:
  - Portfolio holdings
  - Optimal weights
  - Performance metrics
- Perfect for sharing with mentors, investment clubs, or personal records

---

## 🚀 Quick Start

### Prerequisites
- Python 3.11 or higher
- pip package manager

### Installation

1. **Clone or download this repository**
```bash
cd portfolio_optimization_app
```

2. **Install dependencies**
```bash
pip install -r requirements.txt
```

3. **Run the application**
```bash
streamlit run app.py
```

4. **Open your browser**
The app will automatically open at `http://localhost:8501`

---

## 📖 User Guide

### Getting Started

1. **Home Tab**: Read the welcome guide and learn about key concepts
   - Tooltips explain diversification, volatility, and Sharpe ratio

2. **Portfolio Tab**: Build your portfolio
   - Enter a ticker symbol (e.g., AAPL, MSFT, GOOGL)
   - View current price and stock information
   - Add stocks with custom quantities and prices
   - Click "Calculate Stats" to fetch historical data
   - View real-time metrics and allocation charts

3. **Simulate Tab**: Project future performance
   - Set simulation parameters (horizon, paths, tilts)
   - Click "Run Simulation" to generate projections
   - View Monte Carlo and Bootstrap results
   - Analyze fan charts and distribution histograms

4. **Optimize Tab**: Get AI-powered suggestions
   - Click "Optimize for Max Sharpe" for best risk-adjusted returns
   - Click "Optimize for Min Variance" for lowest-risk allocation
   - Generate efficient frontier to see all optimal portfolios
   - Compare current vs. optimized allocations

5. **Analytics Tab**: Dive deeper
   - Explore correlation heatmaps
   - Run PCA to understand key market factors
   - Cluster assets by similarity
   - View diversification and risk metrics

6. **Report Tab**: Export your analysis
   - Generate comprehensive markdown reports
   - Download holdings and optimal weights as CSV
   - Share with others or keep for your records

### Tips & Tricks

- **Sidebar Controls**: Adjust date range, data interval, risk-free rate, and random seed
- **Data Caching**: Stock data is cached for 1 hour to improve performance
- **Clear Cache**: Use "Refresh Data" button to fetch fresh market data
- **Multiple Holdings**: Add 5-10 stocks for meaningful diversification analysis
- **Experiment Safely**: This is a sandbox - try different combinations and learn!

---

## 🛠️ Technical Architecture

### Project Structure
```
portfolio_optimization_app/
├── app.py                 # Main Streamlit application
├── data_yf.py            # Yahoo Finance data fetching & caching
├── portfolio.py          # Portfolio management & statistics
├── simulate.py           # Monte Carlo & Bootstrap simulations
├── optimize.py           # Mean-variance optimization
├── analytics.py          # Correlation, PCA, clustering
├── report.py             # Report generation
├── requirements.txt      # Python dependencies
└── README.md            # This file
```

### Key Technologies
- **Streamlit**: Modern web framework for data apps
- **yfinance**: Real-time stock data from Yahoo Finance
- **NumPy & Pandas**: Numerical computing and data manipulation
- **Plotly & Matplotlib**: Interactive and static visualizations
- **scikit-learn**: Machine learning (PCA, clustering)
- **CVXPY**: Convex optimization for portfolio optimization

### Core Algorithms

**Monte Carlo Simulation (GBM)**
```
S(t) = S(t-1) * exp((μ - 0.5σ²)Δt + σ√Δt * Z)
```
Where μ is expected return, σ is volatility, and Z is a standard normal random variable.

**Markowitz Optimization**
```
Minimize: w^T Σ w (portfolio variance)
Subject to: w^T μ ≥ target return
            Σw = 1 (weights sum to 1)
            w ≥ 0 (no short selling)
```

**Sharpe Ratio**
```
SR = (E[R_p] - R_f) / σ_p
```
Where E[R_p] is expected portfolio return, R_f is risk-free rate, and σ_p is portfolio volatility.

---

## 📚 Educational Resources

### What You'll Learn
- **Portfolio Theory**: Diversification, risk-return tradeoff, efficient frontier
- **Risk Metrics**: Volatility, Sharpe ratio, correlation, beta
- **Simulation Techniques**: Monte Carlo, bootstrap, scenario analysis
- **Optimization**: Mean-variance optimization, constraints, objectives
- **Data Analysis**: PCA, clustering, factor models

### Recommended Reading
- "A Random Walk Down Wall Street" by Burton Malkiel
- "The Intelligent Investor" by Benjamin Graham
- Modern Portfolio Theory (Markowitz, 1952)
- Capital Asset Pricing Model (Sharpe, 1964)

---

## ⚠️ Important Disclaimers

**EDUCATIONAL USE ONLY**

This application is designed purely for educational and demonstration purposes. It is NOT intended to provide financial advice, investment recommendations, or trading signals.

**Limitations & Warnings:**
- Historical performance does NOT guarantee future results
- Simulations are based on mathematical models with inherent limitations
- Real markets are influenced by countless unpredictable factors
- Transaction costs, taxes, and liquidity are not modeled
- Optimizations assume historical patterns will continue (often false)
- No liability is assumed for any financial decisions made using this tool

**Always:**
- Consult with qualified financial advisors before investing
- Do your own research (DYOR)
- Never invest more than you can afford to lose
- Understand that all investments carry risk

---

## 🤝 Contributing

This is an educational project. Suggestions and improvements are welcome!

### Ideas for Enhancement
- Add more asset classes (bonds, crypto, commodities)
- Implement Black-Litterman model for optimization
- Add backtesting capabilities
- Include ESG (Environmental, Social, Governance) scores
- Support for options and derivatives
- Multi-currency support
- Social features (share portfolios, leaderboards)

---

## 📝 License

This project is released for educational purposes. Feel free to use, modify, and learn from the code.

---

## 🙏 Acknowledgments

Built with:
- [Streamlit](https://streamlit.io/) - Amazing framework for data apps
- [yfinance](https://github.com/ranaroussi/yfinance) - Yahoo Finance API wrapper
- [CVXPY](https://www.cvxpy.org/) - Convex optimization library
- Modern Portfolio Theory concepts from Harry Markowitz
- Inspiration from professional portfolio management tools

---

## 📞 Support

For questions, issues, or suggestions:
- Open an issue on GitHub
- Review the code and inline documentation
- Explore Streamlit and yfinance documentation

---

**Happy Investing! 📈**

*Remember: The best investment you can make is in your financial education.*
