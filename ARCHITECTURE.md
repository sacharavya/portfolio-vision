# 🏗️ Portfolio Vision - Architecture Documentation

## System Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                        STREAMLIT WEB APP                        │
│                          (app.py)                               │
└─────────────────────────────────────────────────────────────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        │                         │                         │
        ▼                         ▼                         ▼
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│   Data Layer │         │ Logic Layer  │         │  UI Layer    │
│  (data_yf)   │         │ (portfolio,  │         │ (Streamlit   │
│              │         │  simulate,   │         │  components) │
│              │         │  optimize,   │         │              │
│              │         │  analytics)  │         │              │
└──────────────┘         └──────────────┘         └──────────────┘
        │                         │                         │
        ▼                         ▼                         ▼
┌──────────────┐         ┌──────────────┐         ┌──────────────┐
│ Yahoo Finance│         │   NumPy      │         │   Plotly     │
│  (yfinance)  │         │   Pandas     │         │  Matplotlib  │
│              │         │   CVXPY      │         │   Seaborn    │
│              │         │ scikit-learn │         │              │
└──────────────┘         └──────────────┘         └──────────────┘
```

---

## Module Dependency Graph

```
app.py
├── data_yf.py
│   ├── yfinance
│   ├── pandas
│   └── streamlit (caching)
│
├── portfolio.py
│   ├── pandas
│   └── numpy
│
├── simulate.py
│   ├── numpy
│   └── pandas
│
├── optimize.py
│   ├── cvxpy
│   ├── numpy
│   └── pandas
│
├── analytics.py
│   ├── scikit-learn
│   ├── numpy
│   └── pandas
│
└── report.py
    └── pandas
```

---

## Data Flow Diagram

```
┌──────────┐
│  USER    │
└────┬─────┘
     │ 1. Enter ticker
     ▼
┌─────────────────┐
│  Search Stock   │  ──────► yfinance API
└─────────────────┘              │
     │                           │
     │ 2. Add to portfolio       │
     ▼                           ▼
┌─────────────────┐      ┌──────────────┐
│   Portfolio     │      │  Price Data  │
│   Session State │◄─────┤  (cached)    │
└─────────────────┘      └──────────────┘
     │
     │ 3. Fetch historical data
     ▼
┌─────────────────┐
│  Returns Data   │
│  (DataFrame)    │
└─────────────────┘
     │
     ├─────────────┬─────────────┬─────────────┐
     │             │             │             │
     ▼             ▼             ▼             ▼
┌─────────┐  ┌─────────┐  ┌─────────┐  ┌─────────┐
│Portfolio│  │Simulate │  │Optimize │  │Analytics│
│ Stats   │  │  Paths  │  │ Weights │  │Insights │
└─────────┘  └─────────┘  └─────────┘  └─────────┘
     │             │             │             │
     └─────────────┴─────────────┴─────────────┘
                    │
                    ▼
            ┌──────────────┐
            │   Report     │
            │  Generator   │
            └──────────────┘
                    │
                    ▼
            ┌──────────────┐
            │  Downloads   │
            │  (MD, CSV)   │
            └──────────────┘
```

---

## Tab Navigation Structure

```
Portfolio Vision App
│
├── 🏠 Home
│   ├── Welcome message
│   ├── Feature overview
│   ├── Quick guide
│   └── Educational tooltips
│
├── 💼 Portfolio
│   ├── Stock search
│   ├── Add/remove stocks
│   ├── Holdings table
│   ├── Performance metrics
│   └── Allocation chart
│
├── 🎲 Simulate
│   ├── Simulation parameters
│   ├── Monte Carlo (GBM)
│   │   ├── Fan chart
│   │   └── Terminal histogram
│   └── Historical Bootstrap
│       ├── Fan chart
│       └── Terminal histogram
│
├── 🎯 Optimize
│   ├── Max Sharpe optimization
│   ├── Min Variance optimization
│   ├── Efficient frontier
│   └── Comparison charts
│
├── 📊 Analytics
│   ├── Correlation heatmap
│   ├── PCA analysis
│   ├── Asset clustering
│   └── Diversification metrics
│
└── 📄 Report
    ├── Report generator
    ├── Report preview
    └── Download buttons
```

---

## State Management

```
Session State
├── portfolio (Portfolio object)
│   ├── holdings: Dict[str, float]
│   ├── prices: Dict[str, float]
│   └── transactions: List[Dict]
│
├── historical_data: Dict[str, DataFrame]
│   └── {ticker: price_history}
│
├── returns_data: DataFrame
│   └── Daily returns for all tickers
│
├── mc_paths: ndarray (optional)
│   └── Monte Carlo simulation results
│
├── mc_stats: Dict (optional)
│   └── Simulation statistics
│
├── bs_paths: ndarray (optional)
│   └── Bootstrap simulation results
│
├── bs_stats: Dict (optional)
│   └── Bootstrap statistics
│
├── max_sharpe_weights: Dict (optional)
│   └── Optimized weights
│
├── min_var_weights: Dict (optional)
│   └── Min variance weights
│
├── ef_returns: ndarray (optional)
│   └── Efficient frontier returns
│
├── ef_vols: ndarray (optional)
│   └── Efficient frontier volatilities
│
└── report: str (optional)
    └── Generated markdown report
```

---

## Caching Strategy

```
Cache Levels:

1. Short-term (5 min TTL)
   - get_current_price()
   Purpose: Real-time price updates

2. Medium-term (1 hour TTL)
   - fetch_stock_data()
   - fetch_multiple_stocks()
   - search_ticker()
   - get_stock_info()
   Purpose: Historical data, stable within hour

3. Session State
   - Portfolio holdings
   - Simulation results
   - Optimization results
   Purpose: Preserve during user session

4. No Cache
   - Portfolio calculations
   - Optimizations
   - Analytics
   Purpose: Always reflect current portfolio
```

---

## Key Algorithms & Complexity

### 1. Portfolio Statistics
- **Time Complexity**: O(n·m)
  - n = number of assets
  - m = number of time periods
- **Space Complexity**: O(n·m)
- **Operations**: Matrix multiplication, statistical aggregations

### 2. Monte Carlo Simulation
- **Time Complexity**: O(s·h·n)
  - s = number of simulations
  - h = horizon (days)
  - n = number of assets
- **Space Complexity**: O(s·h)
- **Operations**: Random number generation, exponential calculations

### 3. Portfolio Optimization (CVXPY)
- **Time Complexity**: O(n³) to O(n⁴)
  - n = number of assets
  - Depends on solver (ECOS, SCS, OSQP)
- **Space Complexity**: O(n²)
- **Operations**: Quadratic programming

### 4. Efficient Frontier
- **Time Complexity**: O(p·n³)
  - p = number of points (default 50)
  - n = number of assets
- **Space Complexity**: O(p·n)
- **Operations**: Multiple optimizations

### 5. PCA Analysis
- **Time Complexity**: O(min(n²·m, n·m²))
  - n = number of assets
  - m = number of observations
- **Space Complexity**: O(n²)
- **Operations**: Eigenvalue decomposition

### 6. K-means Clustering
- **Time Complexity**: O(k·n·i)
  - k = number of clusters
  - n = number of assets
  - i = iterations (until convergence)
- **Space Complexity**: O(n·k)
- **Operations**: Distance calculations, centroid updates

---

## Error Handling Strategy

```
Level 1: Input Validation
├── Check ticker format
├── Validate quantities > 0
└── Ensure prices > 0

Level 2: Data Fetching
├── Try-except blocks
├── Empty DataFrame checks
├── Warning messages
└── Graceful degradation

Level 3: Calculations
├── Division by zero checks
├── NaN/Inf handling
├── Empty data checks
└── Default values

Level 4: Optimization
├── Solver status checks
├── Feasibility validation
├── Alternative solutions
└── User notifications

Level 5: UI/UX
├── Loading indicators
├── Success/error messages
├── Helpful tooltips
└── Clear instructions
```

---

## Performance Optimizations

### 1. Data Loading
- ✅ Streamlit @cache_data decorator
- ✅ TTL-based cache expiration
- ✅ Selective cache clearing

### 2. Computations
- ✅ NumPy vectorized operations
- ✅ Pandas built-in functions
- ✅ Avoid Python loops where possible

### 3. Visualizations
- ✅ Plotly for interactive charts (client-side rendering)
- ✅ Matplotlib/Seaborn for static plots
- ✅ Lazy loading of charts

### 4. State Management
- ✅ Session state for persistence
- ✅ Minimal re-computations
- ✅ Conditional rendering

---

## Scalability Considerations

### Current Limits
- **Portfolio Size**: Up to ~50 stocks (UI remains responsive)
- **Simulation Paths**: Up to 10,000 (1-2 second compute time)
- **Time Series**: Up to 5 years daily data (manageable)
- **Efficient Frontier**: 50 points (good resolution)

### Bottlenecks
1. **Data Fetching**: yfinance API rate limits
2. **Optimization**: O(n³) complexity for large portfolios
3. **Simulation**: Memory for storing all paths
4. **UI Rendering**: Too many charts slow down browser

### Potential Improvements
- Parallel data fetching
- Progressive loading of results
- Server-side caching (Redis)
- Pagination for large tables
- Lazy chart rendering

---

## Security Considerations

### Current Implementation
- ✅ No user authentication (educational tool)
- ✅ No sensitive data storage
- ✅ No financial transactions
- ✅ Client-side only operations
- ✅ No database connections

### Best Practices Applied
- ✅ Input validation
- ✅ No SQL injection risk (no DB)
- ✅ No XSS risk (Streamlit handles escaping)
- ✅ No CSRF (no state-changing APIs)
- ✅ HTTPS in production (Streamlit Cloud)

### Disclaimer System
- ✅ Prominent educational banner
- ✅ Multiple warnings in documentation
- ✅ Clear limitations stated
- ✅ No guarantee of accuracy

---

## Deployment Architecture

```
┌──────────────────────────────────────────┐
│      Streamlit Community Cloud           │
│  ┌────────────────────────────────────┐  │
│  │     Portfolio Vision App           │  │
│  │  (Auto-deployed from GitHub)       │  │
│  └────────────────────────────────────┘  │
│               │                           │
│               ▼                           │
│  ┌────────────────────────────────────┐  │
│  │   In-Memory State (per session)    │  │
│  └────────────────────────────────────┘  │
└──────────────────────────────────────────┘
               │
               │ HTTPS
               ▼
┌──────────────────────────────────────────┐
│         External APIs                    │
│  ┌────────────────────────────────────┐  │
│  │    Yahoo Finance (yfinance)        │  │
│  │    - Stock prices                  │  │
│  │    - Historical data               │  │
│  │    - Company info                  │  │
│  └────────────────────────────────────┘  │
└──────────────────────────────────────────┘
```

---

## Testing Strategy

### Manual Testing Checklist
- [ ] Add multiple stocks
- [ ] Remove stocks
- [ ] Fetch historical data
- [ ] Run Monte Carlo simulation
- [ ] Run Bootstrap simulation
- [ ] Optimize for max Sharpe
- [ ] Optimize for min variance
- [ ] Generate efficient frontier
- [ ] View correlation heatmap
- [ ] Run PCA analysis
- [ ] Cluster assets
- [ ] Generate report
- [ ] Download CSV files
- [ ] Clear cache
- [ ] Clear portfolio

### Automated Tests
- ✅ Module import tests (test_modules.py)
- ✅ Portfolio class functionality
- ✅ Simulation convergence
- ✅ Optimization feasibility

---

## Maintenance Guidelines

### Regular Updates
- **Dependencies**: Check quarterly for updates
- **yfinance**: Monitor for API changes
- **Streamlit**: Update for new features
- **Security**: Review CVEs for dependencies

### Common Issues
1. **yfinance data not loading**
   - Check internet connection
   - Verify ticker symbol exists
   - Clear cache

2. **Optimization fails**
   - Ensure at least 2 different assets
   - Check for sufficient historical data
   - Verify date range

3. **Slow performance**
   - Reduce simulation paths
   - Use shorter date ranges
   - Clear browser cache

---

**This architecture is designed for educational use with a focus on clarity, maintainability, and user experience.**
