# 🚀 Quick Start Guide - Portfolio Vision

Get up and running in 5 minutes!

## Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- Streamlit (web framework)
- yfinance (stock data)
- NumPy, Pandas (data processing)
- Plotly, Matplotlib, Seaborn (visualizations)
- scikit-learn (analytics)
- CVXPY (optimization)

## Step 2: Launch the App

```bash
streamlit run app.py
```

The app will open automatically in your browser at `http://localhost:8501`

## Step 3: Build Your First Portfolio

1. **Go to the Portfolio Tab**
2. **Add Some Stocks**:
   - Try: AAPL (Apple)
   - Try: MSFT (Microsoft)
   - Try: GOOGL (Google)
   - Try: AMZN (Amazon)
   - Try: TSLA (Tesla)

3. **For each stock**:
   - Enter the ticker symbol
   - See the current price
   - Enter quantity (e.g., 10 shares)
   - Click "Add to Portfolio"

4. **Click "Calculate Stats"**
   - This fetches historical data
   - You'll see performance metrics
   - View the allocation pie chart

## Step 4: Run a Simulation

1. **Go to the Simulate Tab**
2. **Set Parameters**:
   - Horizon: 252 days (1 year)
   - Paths: 1000 simulations
   - Keep tilts at default
3. **Click "Run Simulation"**
4. **Explore the Results**:
   - Fan chart shows possible futures
   - Median (P50) is the expected outcome
   - P10 = pessimistic, P90 = optimistic
   - Check the histogram

## Step 5: Optimize Your Portfolio

1. **Go to the Optimize Tab**
2. **Click "Optimize for Max Sharpe"**
   - This finds the best risk-adjusted allocation
   - Compare suggested weights vs. your current ones
3. **Try "Optimize for Min Variance"**
   - This finds the lowest-risk allocation
4. **Generate Efficient Frontier**
   - See all optimal portfolios
   - Your current portfolio is marked in red

## Step 6: Explore Analytics

1. **Go to the Analytics Tab**
2. **View Correlation Heatmap**
   - See which stocks move together
3. **Run PCA Analysis**
   - Discover hidden market factors
4. **Try Clustering**
   - Group similar stocks

## Step 7: Generate a Report

1. **Go to the Report Tab**
2. **Click "Generate Report"**
3. **Download**:
   - Full report (markdown)
   - Holdings (CSV)
   - Optimal weights (CSV)

---

## 💡 Pro Tips

- **Start Simple**: Begin with 3-5 well-known stocks
- **Compare Sectors**: Add stocks from different industries for diversity
- **Adjust Date Range**: Use the sidebar to change historical data period
- **Experiment**: This is a sandbox - try wild allocations safely!
- **Cache Refresh**: If prices seem old, click "Refresh Data" in sidebar

---

## 🎯 Sample Portfolio Ideas

### Tech-Heavy Portfolio
- AAPL, MSFT, GOOGL, META, NVDA

### Diversified Blue-Chip
- AAPL, JNJ, JPM, XOM, PG

### Growth vs. Value
- TSLA, AMZN (growth) + KO, PFE (value)

### Index ETFs
- SPY (S&P 500), QQQ (Nasdaq), DIA (Dow)

---

## ❓ Troubleshooting

**"No data found for ticker"**
- Check spelling of ticker symbol
- Ensure market is open or use previous close
- Try common tickers: AAPL, MSFT, GOOGL

**"Optimization failed"**
- Need at least 2 stocks with different characteristics
- Ensure you clicked "Calculate Stats" first
- Check that date range has enough data

**App is slow**
- First data fetch takes time (caching data)
- Reduce number of simulation paths
- Use shorter date ranges

**Charts not showing**
- Make sure you clicked the action buttons
- Scroll down - results appear below buttons
- Check that data was fetched successfully

---

## 🎓 Learning Path

1. **Week 1**: Build portfolios, understand metrics
2. **Week 2**: Run simulations, interpret results
3. **Week 3**: Try optimization, compare allocations
4. **Week 4**: Deep dive into analytics, correlations

---

## 🔗 Next Steps

- Read the full [README.md](README.md)
- Explore each module's source code
- Experiment with different stock combinations
- Share your findings with friends!

---

**Ready? Let's build your first portfolio! 📊**
