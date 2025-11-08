"""
Portfolio Vision - Investment Simulation and Optimization Dashboard
A demo-friendly tool for beginner investors
"""
import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
from datetime import datetime, timedelta
import matplotlib.pyplot as plt
import seaborn as sns

# Import custom modules
from data_yf import (
    fetch_stock_data, fetch_multiple_stocks, get_current_price,
    search_ticker, get_stock_info, get_returns_dataframe, get_last_refresh_time,
    search_stock_suggestions
)
from portfolio import Portfolio, calculate_portfolio_stats, calculate_asset_stats
from simulate import monte_carlo_gbm, historical_bootstrap, calculate_percentile_bands
from optimize import (
    optimize_max_sharpe, optimize_min_variance, generate_efficient_frontier,
    calculate_portfolio_performance
)
from analytics import (
    calculate_correlation_matrix, perform_pca, cluster_assets,
    calculate_diversification_ratio, calculate_contribution_to_risk,
    analyze_sector_exposure
)
from report import generate_markdown_report, generate_weights_csv, generate_holdings_csv
from insights import (
    interpret_sharpe_ratio, interpret_volatility, interpret_annual_return,
    interpret_diversification_ratio, interpret_simulation_results,
    generate_portfolio_summary_insights, get_optimization_comparison_insights
)

# Page configuration
st.set_page_config(
    page_title="Portfolio Vision",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS - Professional Modern Theme
st.markdown("""
<style>
    /* Main Header */
    .main-header {
        font-size: 2.5rem;
        font-weight: 700;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }

    .sub-header {
        font-size: 1.1rem;
        text-align: center;
        color: #7f8c8d;
        margin-bottom: 2rem;
        font-weight: 400;
    }

    /* Warning Banner */
    .banner {
        background: linear-gradient(135deg, #fff3cd 0%, #ffeaa7 100%);
        border-left: 4px solid #f39c12;
        border-radius: 8px;
        padding: 16px 24px;
        text-align: center;
        font-weight: 600;
        color: #856404;
        margin-bottom: 2rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.08);
    }

    /* Professional Badge Styles */
    .badge {
        display: inline-block;
        padding: 6px 14px;
        border-radius: 6px;
        font-weight: 700;
        font-size: 0.75rem;
        letter-spacing: 0.5px;
        text-transform: uppercase;
        margin-bottom: 8px;
    }

    .badge-success {
        background-color: #27ae60;
        color: white;
    }

    .badge-info {
        background-color: #3498db;
        color: white;
    }

    .badge-warning {
        background-color: #f39c12;
        color: white;
    }

    .badge-danger {
        background-color: #e74c3c;
        color: white;
    }

    .badge-grade {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 8px 16px;
        font-size: 0.9rem;
    }

    /* Metric Cards */
    .metric-card {
        background-color: #ffffff;
        border-radius: 12px;
        padding: 24px;
        box-shadow: 0 4px 6px rgba(0,0,0,0.07);
        border: 1px solid #ecf0f1;
        transition: all 0.3s ease;
    }

    .metric-card:hover {
        box-shadow: 0 6px 12px rgba(0,0,0,0.1);
        transform: translateY(-2px);
    }

    /* Suggestion Items */
    .suggestion-item {
        background-color: #f8f9fa;
        border-left: 3px solid #3498db;
        padding: 14px 16px;
        margin: 8px 0;
        border-radius: 6px;
        transition: all 0.2s ease;
    }

    .suggestion-item:hover {
        background-color: #e8f4f8;
        border-left-width: 4px;
        padding-left: 18px;
    }

    /* Buttons Enhancement */
    .stButton>button {
        background: linear-gradient(135deg, #3498db 0%, #2980b9 100%);
        color: white;
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.3s ease;
        border: 2px solid #2980b9;
        padding: 0.7rem 1.5rem;
        font-size: 1rem;
        box-shadow: 0 2px 8px rgba(52, 152, 219, 0.3);
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    .stButton>button:hover {
        background: linear-gradient(135deg, #2980b9 0%, #21618c 100%);
        transform: translateY(-2px);
        box-shadow: 0 6px 16px rgba(52, 152, 219, 0.4);
        border-color: #21618c;
    }

    .stButton>button:active {
        transform: translateY(0);
        box-shadow: 0 2px 4px rgba(52, 152, 219, 0.3);
    }

    /* Primary Action Button - even more prominent */
    .stButton>button[kind="primary"] {
        background: linear-gradient(135deg, #27ae60 0%, #229954 100%);
        border-color: #229954;
        box-shadow: 0 3px 10px rgba(39, 174, 96, 0.4);
    }

    .stButton>button[kind="primary"]:hover {
        background: linear-gradient(135deg, #229954 0%, #1e8449 100%);
        border-color: #1e8449;
        box-shadow: 0 6px 18px rgba(39, 174, 96, 0.5);
    }

    /* Input Fields */
    .stTextInput > div > div > input {
        font-size: 1.05rem;
        border-radius: 8px;
        border: 2px solid #ecf0f1;
        padding: 12px;
        transition: border-color 0.2s ease;
    }

    .stTextInput > div > div > input:focus {
        border-color: #3498db;
        box-shadow: 0 0 0 3px rgba(52,152,219,0.1);
    }

    /* Number Inputs */
    .stNumberInput > div > div > input {
        border-radius: 8px;
        border: 2px solid #ecf0f1;
    }

    /* Selectbox */
    .stSelectbox > div > div {
        border-radius: 8px;
    }

    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: transparent;
    }

    .stTabs [data-baseweb="tab"] {
        border-radius: 8px 8px 0 0;
        padding: 12px 24px;
        font-weight: 600;
        background-color: #f8f9fa;
        border: none;
    }

    .stTabs [aria-selected="true"] {
        background-color: #3498db;
        color: white;
    }

    /* Expanders */
    .streamlit-expanderHeader {
        font-weight: 600;
        font-size: 1.05rem;
        border-radius: 8px;
        background-color: #f8f9fa;
        padding: 12px 16px;
    }

    /* DataFrames */
    .dataframe {
        border-radius: 8px;
        overflow: hidden;
        border: 1px solid #ecf0f1;
    }

    /* Info/Warning/Success Boxes */
    .stAlert {
        border-radius: 8px;
        border-left-width: 4px;
    }

    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 700;
        color: #2c3e50;
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.95rem;
        font-weight: 600;
        color: #7f8c8d;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: #f8f9fa;
        border-right: 1px solid #ecf0f1;
    }

    [data-testid="stSidebar"] .stButton>button {
        width: 100%;
        justify-content: center;
    }

    /* Section Headers */
    h1, h2, h3 {
        color: #2c3e50;
        font-weight: 700;
        margin-top: 1.5rem;
        margin-bottom: 1rem;
    }

    h3 {
        border-bottom: 2px solid #ecf0f1;
        padding-bottom: 0.5rem;
    }

    /* Dividers */
    hr {
        border: none;
        height: 2px;
        background: linear-gradient(to right, transparent, #ecf0f1, transparent);
        margin: 2rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'portfolio' not in st.session_state:
    st.session_state.portfolio = Portfolio()
if 'historical_data' not in st.session_state:
    st.session_state.historical_data = {}
if 'returns_data' not in st.session_state:
    st.session_state.returns_data = pd.DataFrame()
if 'last_refresh' not in st.session_state:
    st.session_state.last_refresh = None

# Sidebar
with st.sidebar:
    st.image("https://img.icons8.com/3d-fluency/94/combo-chart--v1.png", width=80)
    st.title("Portfolio Vision")
    st.markdown("---")

    # Global settings
    st.subheader("Settings")

    # Date range
    default_start = datetime.now() - timedelta(days=365)
    default_end = datetime.now()

    start_date = st.date_input("Start Date", default_start)
    end_date = st.date_input("End Date", default_end)

    # Data interval
    interval = st.selectbox("Data Interval", ["1d", "1wk", "1mo"], index=0)

    # Risk-free rate
    risk_free_rate = st.number_input(
        "Risk-Free Rate (%)",
        min_value=0.0,
        max_value=10.0,
        value=2.0,
        step=0.1
    ) / 100

    # Random seed
    random_seed = st.number_input(
        "Random Seed",
        min_value=0,
        max_value=9999,
        value=42,
        step=1
    )

    st.markdown("---")

    # Quick actions
    st.subheader("Quick Actions")
    if st.button("Refresh Data", use_container_width=True):
        st.session_state.historical_data = {}
        st.session_state.returns_data = pd.DataFrame()
        st.cache_data.clear()
        st.success("Data cache cleared!")
        st.rerun()

    if st.button("Clear Portfolio", use_container_width=True):
        st.session_state.portfolio = Portfolio()
        st.success("Portfolio cleared!")
        st.rerun()

    # Last refresh time
    if st.session_state.last_refresh:
        st.markdown(f"**Last Refresh:** {st.session_state.last_refresh}")

# Main header
st.markdown('<div class="main-header">Portfolio Vision</div>', unsafe_allow_html=True)
st.markdown('<div class="sub-header">Investment Simulation & Optimization Dashboard</div>', unsafe_allow_html=True)
st.markdown('<div class="banner"> EDUCATIONAL USE ONLY - Not Financial Advice</div>', unsafe_allow_html=True)

# Tabs
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "Home",
    "Portfolio",
    "Simulate",
    "Optimize",
    "Analytics",
    "Report"
])

# ============================================================================
# TAB 1: HOME
# ============================================================================
with tab1:
    st.header("Welcome to Portfolio Vision")

    st.markdown("""
    ### Get Started

    **Portfolio Vision** is your personal investment lab - a safe space to explore, learn, and understand
    the fundamentals of portfolio management using real market data.

    #### What You Can Do:
    - **Search & Add Stocks**: Find stocks using live data from Yahoo Finance
    - **Track Your Portfolio**: View real-time values, allocations, and performance metrics
    - **Simulate Futures**: Project portfolio value using Monte Carlo and Bootstrap simulations
    - **Optimize Allocation**: Get AI-powered suggestions using modern portfolio theory
    - **Advanced Analytics**: Explore correlations, PCA, and clustering insights
    - **Generate Reports**: Download professional investment summaries

    #### Quick Guide:
    1. Use the **Portfolio** tab to search and add stocks
    2. View metrics and allocations in real-time
    3. Head to **Simulate** to forecast future performance
    4. Click **Optimize** to get better portfolio suggestions
    5. Explore **Analytics** for deeper insights
    6. Download your **Report** when you're done

    ---
    """)

    # Display some helpful tooltips
    col1, col2, col3 = st.columns(3)

    with col1:
        with st.expander("What is Diversification?"):
            st.write("""
            **Diversification** means spreading your investments across different assets to reduce risk.
            Think of it as "not putting all your eggs in one basket."

            By holding multiple stocks, you reduce the impact of any single stock's poor performance
            on your overall portfolio.
            """)

    with col2:
        with st.expander("What is Volatility?"):
            st.write("""
            **Volatility** measures how much an investment's price fluctuates over time.
            High volatility means bigger price swings (more risk), while low volatility
            means more stable prices.

            It's typically measured as the standard deviation of returns.
            """)

    with col3:
        with st.expander("What is Sharpe Ratio?"):
            st.write("""
            The **Sharpe Ratio** measures risk-adjusted returns. It tells you how much extra return
            you're getting for the extra risk you take.

            Higher is better: a Sharpe ratio above 1 is considered good, above 2 is very good,
            and above 3 is excellent.
            """)

# ============================================================================
# TAB 2: PORTFOLIO
# ============================================================================
with tab2:
    st.header("Portfolio Management")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("Search & Add Stocks")

        # Stock search with suggestions
        search_query = st.text_input(
            "Search by Ticker or Company Name",
            placeholder="e.g., AAPL, Apple, Microsoft, TSLA...",
            key="ticker_search",
            help="Type a ticker symbol or company name to see suggestions"
        )

        # Show suggestions when user types
        if search_query:
            suggestions = search_stock_suggestions(search_query, max_results=8)

            if suggestions:
                st.markdown("**Suggestions:**")

                # Create a nice table view of suggestions
                for suggestion in suggestions:
                    col_tick, col_name, col_sector, col_select = st.columns([1, 3, 2, 1])

                    with col_tick:
                        st.markdown(f"**{suggestion['symbol']}**")

                    with col_name:
                        st.markdown(f"{suggestion['name']}")

                    with col_sector:
                        st.markdown(f"*{suggestion['sector']}*")

                    with col_select:
                        if st.button("Select", key=f"select_{suggestion['symbol']}", use_container_width=True):
                            st.session_state.selected_ticker = suggestion['symbol']
                            st.rerun()

                st.markdown("---")

        # Get the selected ticker (either from search or from suggestion selection)
        if 'selected_ticker' in st.session_state:
            ticker_input = st.session_state.selected_ticker
        else:
            ticker_input = search_query.upper() if search_query else ""

        # Display selected stock info and add controls
        if ticker_input:
            st.markdown(f"### Selected: **{ticker_input}**")

            col_a, col_b, col_c = st.columns(3)

            with col_a:
                current_price = get_current_price(ticker_input)
                if current_price:
                    st.success(f"Current Price: ${current_price:.2f}")
                    default_price = current_price
                else:
                    st.warning("Could not fetch current price")
                    default_price = 100.0

                quantity = st.number_input("Quantity", min_value=0.0, value=10.0, step=1.0, key="qty_input")

            with col_b:
                price = st.number_input("Price per Share ($)", min_value=0.01, value=default_price, step=0.01, key="price_input")

            with col_c:
                st.write("")
                st.write("")
                if st.button("Add to Portfolio", use_container_width=True):
                    st.session_state.portfolio.add_stock(ticker_input, quantity, price)
                    st.success(f"Added {quantity} shares of {ticker_input} at ${price:.2f}")
                    # Clear selected ticker
                    if 'selected_ticker' in st.session_state:
                        del st.session_state.selected_ticker
                    st.rerun()

    with col2:
        st.subheader("Quick Info")
        if ticker_input:
            info = get_stock_info(ticker_input)
            st.write(f"**Name:** {info['name']}")
            st.write(f"**Sector:** {info['sector']}")
            st.write(f"**Industry:** {info['industry']}")

    st.markdown("---")

    # Current portfolio
    st.subheader("Current Portfolio")

    holdings_df = st.session_state.portfolio.get_holdings_dataframe()

    if not holdings_df.empty:
        # Update prices with current data
        tickers = st.session_state.portfolio.get_tickers()
        current_prices = {}
        for ticker in tickers:
            price = get_current_price(ticker)
            if price:
                current_prices[ticker] = price

        if current_prices:
            st.session_state.portfolio.update_prices(current_prices)
            holdings_df = st.session_state.portfolio.get_holdings_dataframe()

        # Display holdings
        st.dataframe(holdings_df, use_container_width=True)

        # Portfolio metrics
        total_value = st.session_state.portfolio.get_total_value()

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.metric("Total Value", f"${total_value:,.2f}")

        with col2:
            st.metric("Number of Holdings", len(holdings_df))

        with col3:
            if not holdings_df.empty:
                max_weight = holdings_df['Weight (%)'].max()
                st.metric("Largest Position", f"{max_weight:.1f}%")

        with col4:
            # Fetch data for portfolio stats
            if st.button("Calculate Stats"):
                with st.spinner("Fetching data..."):
                    data = fetch_multiple_stocks(
                        tickers,
                        str(start_date),
                        str(end_date),
                        interval
                    )
                    st.session_state.historical_data = data
                    st.session_state.returns_data = get_returns_dataframe(data)
                    st.session_state.last_refresh = get_last_refresh_time()
                    st.success("Data fetched!")
                    st.rerun()

        # Calculate portfolio statistics if we have returns data
        if not st.session_state.returns_data.empty:
            weights = st.session_state.portfolio.get_weights()
            stats = calculate_portfolio_stats(
                st.session_state.returns_data,
                weights,
                risk_free_rate
            )

            st.markdown("### Portfolio Performance Metrics")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Annual Return", f"{stats['annual_return']:.2%}")

            with col2:
                st.metric("Annual Volatility", f"{stats['annual_volatility']:.2%}")

            with col3:
                st.metric("Sharpe Ratio", f"{stats['sharpe_ratio']:.3f}")

            with col4:
                st.metric("Total Return", f"{stats['total_return']:.2%}")

            # Add insights section
            st.markdown("---")
            st.markdown("### Performance Insights")

            # Generate insights
            insights = generate_portfolio_summary_insights(
                total_value=total_value,
                num_holdings=len(holdings_df),
                annual_return=stats['annual_return'],
                volatility=stats['annual_volatility'],
                sharpe_ratio=stats['sharpe_ratio'],
                risk_free_rate=risk_free_rate
            )

            # Display insights in expandable sections
            col_a, col_b, col_c = st.columns(3)

            with col_a:
                with st.expander("Return Analysis", expanded=True):
                    return_insight = interpret_annual_return(stats['annual_return'], risk_free_rate)
                    badge_class = f"badge badge-{return_insight['color']}"
                    st.markdown(f"<span class='{badge_class}'>{return_insight['badge']}</span>", unsafe_allow_html=True)
                    st.markdown(f"**{return_insight['level']}**")
                    st.write(return_insight['explanation'])
                    st.caption(return_insight['detail'])
                    if 'caution' in return_insight:
                        st.info(return_insight['caution'])

            with col_b:
                with st.expander("Risk Analysis", expanded=True):
                    vol_insight = interpret_volatility(stats['annual_volatility'])
                    badge_class = f"badge badge-{vol_insight['color']}"
                    st.markdown(f"<span class='{badge_class}'>{vol_insight['badge']}</span>", unsafe_allow_html=True)
                    st.markdown(f"**{vol_insight['level']}**")
                    st.write(vol_insight['explanation'])
                    st.caption(vol_insight['detail'])
                    if 'advice' in vol_insight:
                        st.info(vol_insight['advice'])

            with col_c:
                with st.expander("Risk-Adjusted Performance", expanded=True):
                    sharpe_insight = interpret_sharpe_ratio(stats['sharpe_ratio'])
                    badge_class = "badge badge-grade"
                    st.markdown(f"<span class='{badge_class}'>GRADE: {sharpe_insight['badge']}</span>", unsafe_allow_html=True)
                    st.markdown(f"**{sharpe_insight['level']}**")
                    st.write(sharpe_insight['explanation'])
                    st.caption(sharpe_insight['detail'])

            # Overall portfolio summary
            st.markdown("#### Portfolio Summary")
            for insight in insights:
                st.markdown(insight)

        # Allocation pie chart
        st.markdown("### Portfolio Allocation")
        fig = px.pie(
            holdings_df,
            values='Value',
            names='Ticker',
            title='Portfolio Allocation by Value'
        )
        st.plotly_chart(fig, use_container_width=True)

        # Remove stock
        st.markdown("### Remove Stock")
        col1, col2 = st.columns([3, 1])
        with col1:
            ticker_to_remove = st.selectbox("Select stock to remove", tickers)
        with col2:
            st.write("")
            st.write("")
            if st.button("Remove", use_container_width=True):
                st.session_state.portfolio.remove_stock(ticker_to_remove)
                st.success(f"Removed {ticker_to_remove}")
                st.rerun()

    else:
        st.info("Add stocks to your portfolio to get started!")

# ============================================================================
# TAB 3: SIMULATE
# ============================================================================
with tab3:
    st.header("Portfolio Simulation")

    if st.session_state.portfolio.get_tickers():
        # Simulation parameters
        st.subheader("Simulation Parameters")

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            horizon_days = st.number_input("Horizon (Days)", min_value=1, max_value=1000, value=252, step=1)

        with col2:
            n_simulations = st.number_input("Number of Paths", min_value=100, max_value=10000, value=1000, step=100)

        with col3:
            return_tilt = st.number_input("Return Tilt (%)", min_value=-10.0, max_value=10.0, value=0.0, step=0.5) / 100

        with col4:
            volatility_tilt = st.number_input("Volatility Tilt", min_value=0.1, max_value=2.0, value=1.0, step=0.1)

        # Run simulation button
        if st.button("Run Simulation", use_container_width=True):
            if st.session_state.returns_data.empty:
                st.error("Please fetch data first from the Portfolio tab")
            else:
                with st.spinner("Running simulations..."):
                    weights = st.session_state.portfolio.get_weights()
                    initial_value = st.session_state.portfolio.get_total_value()

                    # Monte Carlo
                    mc_paths, mc_stats = monte_carlo_gbm(
                        st.session_state.returns_data,
                        weights,
                        initial_value,
                        horizon_days,
                        n_simulations,
                        return_tilt,
                        volatility_tilt,
                        random_seed
                    )

                    # Historical Bootstrap
                    bs_paths, bs_stats = historical_bootstrap(
                        st.session_state.returns_data,
                        weights,
                        initial_value,
                        horizon_days,
                        n_simulations,
                        seed=random_seed
                    )

                    st.session_state.mc_paths = mc_paths
                    st.session_state.mc_stats = mc_stats
                    st.session_state.bs_paths = bs_paths
                    st.session_state.bs_stats = bs_stats

                    st.success("Simulation complete!")

        # Display results
        if 'mc_paths' in st.session_state:
            st.markdown("---")
            st.subheader("Monte Carlo (GBM) Results")

            col1, col2, col3, col4 = st.columns(4)
            stats = st.session_state.mc_stats

            with col1:
                st.metric("Median (P50)", f"${stats['p50']:,.2f}")
            with col2:
                st.metric("Pessimistic (P10)", f"${stats['p10']:,.2f}")
            with col3:
                st.metric("Optimistic (P90)", f"${stats['p90']:,.2f}")
            with col4:
                st.metric("Expected Value", f"${stats['mean']:,.2f}")

            # Add simulation insights
            st.markdown("---")
            st.markdown("### Simulation Insights")

            initial_value = st.session_state.portfolio.get_total_value()
            sim_insights = interpret_simulation_results(stats, initial_value, horizon_days)

            # Display risk level
            risk_info = sim_insights['risk_level']
            badge_class = f"badge badge-{risk_info['color']}"
            st.markdown(f"<span class='{badge_class}'>{risk_info['badge']}</span>", unsafe_allow_html=True)
            st.markdown(f"**{risk_info['level']}**")
            st.write(risk_info['explanation'])

            # Display interpretations
            col_x, col_y = st.columns(2)

            with col_x:
                st.info(f"**Median Outcome**: {sim_insights['median_interpretation']}")
                st.success(f"**Upside Potential**: {sim_insights['upside_interpretation']}")

            with col_y:
                st.warning(f"**Downside Risk**: {sim_insights['downside_interpretation']}")
                st.markdown(f"**Recommendation**: {sim_insights['recommendation']}")

            # Fan chart
            st.markdown("### Projection Fan Chart")
            st.caption("Shows the range of possible portfolio values over time. The shaded area represents the 80% confidence interval (P10 to P90).")

            percentile_df = calculate_percentile_bands(st.session_state.mc_paths, [10, 50, 90])

            fig = go.Figure()

            # Add optimistic bound (P90) - upper boundary
            fig.add_trace(go.Scatter(
                x=percentile_df['Day'],
                y=percentile_df['P90'],
                name='Optimistic (P90)',
                line=dict(color='rgba(39, 174, 96, 0)', width=0),
                mode='lines',
                showlegend=False,
                hovertemplate='Day %{x}<br>Optimistic: $%{y:,.0f}<extra></extra>'
            ))

            # Add pessimistic bound (P10) - lower boundary with fill
            fig.add_trace(go.Scatter(
                x=percentile_df['Day'],
                y=percentile_df['P10'],
                name='80% Confidence Range',
                fill='tonexty',
                fillcolor='rgba(52, 152, 219, 0.2)',
                line=dict(color='rgba(231, 76, 60, 0)', width=0),
                mode='lines',
                hovertemplate='Day %{x}<br>Pessimistic: $%{y:,.0f}<extra></extra>'
            ))

            # Add median line (P50) - most prominent
            fig.add_trace(go.Scatter(
                x=percentile_df['Day'],
                y=percentile_df['P50'],
                name='Expected (Median)',
                line=dict(color='#3498db', width=4),
                mode='lines',
                hovertemplate='Day %{x}<br>Expected: $%{y:,.0f}<extra></extra>'
            ))

            # Add boundary lines for clarity
            fig.add_trace(go.Scatter(
                x=percentile_df['Day'],
                y=percentile_df['P90'],
                name='Optimistic Scenario (P90)',
                line=dict(color='#27ae60', width=2, dash='dash'),
                mode='lines',
                hovertemplate='Day %{x}<br>Optimistic: $%{y:,.0f}<extra></extra>'
            ))

            fig.add_trace(go.Scatter(
                x=percentile_df['Day'],
                y=percentile_df['P10'],
                name='Pessimistic Scenario (P10)',
                line=dict(color='#e74c3c', width=2, dash='dash'),
                mode='lines',
                hovertemplate='Day %{x}<br>Pessimistic: $%{y:,.0f}<extra></extra>'
            ))

            fig.update_layout(
                title={
                    'text': "Portfolio Value Projection - Monte Carlo Simulation",
                    'x': 0.5,
                    'xanchor': 'center',
                    'font': {'size': 18, 'color': '#2c3e50', 'family': 'Arial, sans-serif'}
                },
                xaxis_title="Days into Future",
                yaxis_title="Portfolio Value ($)",
                hovermode='x unified',
                plot_bgcolor='white',
                paper_bgcolor='white',
                font=dict(family='Arial, sans-serif', size=12, color='#2c3e50'),
                legend=dict(
                    orientation="v",
                    yanchor="top",
                    y=0.99,
                    xanchor="left",
                    x=0.01,
                    bgcolor='rgba(255, 255, 255, 0.9)',
                    bordercolor='#bdc3c7',
                    borderwidth=1
                ),
                xaxis=dict(
                    gridcolor='#ecf0f1',
                    showgrid=True,
                    zeroline=False
                ),
                yaxis=dict(
                    gridcolor='#ecf0f1',
                    showgrid=True,
                    zeroline=False,
                    tickformat='$,.0f'
                )
            )

            st.plotly_chart(fig, use_container_width=True)

            # Histogram of terminal values
            st.markdown("### Distribution of Final Values")

            terminal_values = st.session_state.mc_paths[:, -1]

            fig = go.Figure(data=[go.Histogram(
                x=terminal_values,
                nbinsx=50,
                name='Terminal Values'
            )])

            fig.update_layout(
                title="Distribution of Portfolio Value at End of Horizon",
                xaxis_title="Portfolio Value ($)",
                yaxis_title="Frequency"
            )

            st.plotly_chart(fig, use_container_width=True)

            # Bootstrap results
            st.markdown("---")
            st.subheader("Historical Bootstrap Results")

            col1, col2, col3, col4 = st.columns(4)
            bs_stats = st.session_state.bs_stats

            with col1:
                st.metric("Median (P50)", f"${bs_stats['p50']:,.2f}")
            with col2:
                st.metric("Pessimistic (P10)", f"${bs_stats['p10']:,.2f}")
            with col3:
                st.metric("Optimistic (P90)", f"${bs_stats['p90']:,.2f}")
            with col4:
                st.metric("Expected Value", f"${bs_stats['mean']:,.2f}")

    else:
        st.info("Add stocks to your portfolio first to run simulations")

# ============================================================================
# TAB 4: OPTIMIZE
# ============================================================================
with tab4:
    st.header("Portfolio Optimization")

    if st.session_state.portfolio.get_tickers() and not st.session_state.returns_data.empty:

        st.markdown("""
        This module uses **Markowitz Mean-Variance Optimization** to suggest better portfolio allocations.
        It can optimize for:
        - **Maximum Sharpe Ratio**: Best risk-adjusted returns
        - **Minimum Variance**: Lowest risk portfolio
        """)

        col1, col2 = st.columns(2)

        with col1:
            if st.button("Optimize for Max Sharpe", use_container_width=True):
                with st.spinner("Optimizing..."):
                    max_sharpe_weights = optimize_max_sharpe(
                        st.session_state.returns_data,
                        risk_free_rate
                    )
                    st.session_state.max_sharpe_weights = max_sharpe_weights

                    if max_sharpe_weights:
                        perf = calculate_portfolio_performance(
                            max_sharpe_weights,
                            st.session_state.returns_data,
                            risk_free_rate
                        )
                        st.session_state.max_sharpe_performance = perf
                        st.success("Optimization complete!")
                    else:
                        st.error("Optimization failed")

        with col2:
            if st.button("Optimize for Min Variance", use_container_width=True):
                with st.spinner("Optimizing..."):
                    min_var_weights = optimize_min_variance(st.session_state.returns_data)
                    st.session_state.min_var_weights = min_var_weights

                    if min_var_weights:
                        perf = calculate_portfolio_performance(
                            min_var_weights,
                            st.session_state.returns_data,
                            risk_free_rate
                        )
                        st.session_state.min_var_performance = perf
                        st.success("Optimization complete!")
                    else:
                        st.error("Optimization failed")

        # Display optimized weights
        if 'max_sharpe_weights' in st.session_state:
            st.markdown("---")
            st.subheader("Maximum Sharpe Ratio Portfolio")

            col1, col2 = st.columns(2)

            with col1:
                weights_df = pd.DataFrame([
                    {'Ticker': k, 'Optimal Weight (%)': v * 100}
                    for k, v in st.session_state.max_sharpe_weights.items()
                ])
                st.dataframe(weights_df, use_container_width=True)

            with col2:
                if 'max_sharpe_performance' in st.session_state:
                    perf = st.session_state.max_sharpe_performance
                    st.metric("Expected Return", f"{perf['expected_return']:.2%}")
                    st.metric("Volatility", f"{perf['volatility']:.2%}")
                    st.metric("Sharpe Ratio", f"{perf['sharpe_ratio']:.3f}")

            # Pie chart
            fig = px.pie(
                weights_df,
                values='Optimal Weight (%)',
                names='Ticker',
                title='Optimized Allocation (Max Sharpe)'
            )
            st.plotly_chart(fig, use_container_width=True)

            # Add optimization insights
            if 'max_sharpe_performance' in st.session_state and not st.session_state.returns_data.empty:
                current_weights = st.session_state.portfolio.get_weights()
                current_perf = calculate_portfolio_performance(
                    current_weights,
                    st.session_state.returns_data,
                    risk_free_rate
                )

                comparison = get_optimization_comparison_insights(
                    current_sharpe=current_perf['sharpe_ratio'],
                    optimized_sharpe=st.session_state.max_sharpe_performance['sharpe_ratio'],
                    current_volatility=current_perf['volatility'],
                    optimized_volatility=st.session_state.max_sharpe_performance['volatility']
                )

                st.markdown("### Current vs. Optimized")
                badge_class = f"badge badge-{comparison['color']}"
                st.markdown(f"<span class='{badge_class}'>{comparison['badge']}</span>", unsafe_allow_html=True)
                st.markdown(f"**{comparison['level']}**")
                st.write(comparison['message'])
                st.caption(comparison['detail'])
                st.info(comparison['action'])

        if 'min_var_weights' in st.session_state:
            st.markdown("---")
            st.subheader("Minimum Variance Portfolio")

            col1, col2 = st.columns(2)

            with col1:
                weights_df = pd.DataFrame([
                    {'Ticker': k, 'Optimal Weight (%)': v * 100}
                    for k, v in st.session_state.min_var_weights.items()
                ])
                st.dataframe(weights_df, use_container_width=True)

            with col2:
                if 'min_var_performance' in st.session_state:
                    perf = st.session_state.min_var_performance
                    st.metric("Expected Return", f"{perf['expected_return']:.2%}")
                    st.metric("Volatility", f"{perf['volatility']:.2%}")
                    st.metric("Sharpe Ratio", f"{perf['sharpe_ratio']:.3f}")

            # Pie chart
            fig = px.pie(
                weights_df,
                values='Optimal Weight (%)',
                names='Ticker',
                title='Optimized Allocation (Min Variance)'
            )
            st.plotly_chart(fig, use_container_width=True)

        # Efficient Frontier
        st.markdown("---")
        st.subheader(" Efficient Frontier")

        if st.button("Generate Efficient Frontier"):
            with st.spinner("Generating efficient frontier..."):
                ef_returns, ef_vols, ef_sharpes = generate_efficient_frontier(
                    st.session_state.returns_data,
                    n_points=50,
                    risk_free_rate=risk_free_rate
                )

                st.session_state.ef_returns = ef_returns
                st.session_state.ef_vols = ef_vols
                st.session_state.ef_sharpes = ef_sharpes

                st.success("Efficient frontier generated!")

        if 'ef_returns' in st.session_state:
            fig = go.Figure()

            # Efficient frontier
            fig.add_trace(go.Scatter(
                x=st.session_state.ef_vols,
                y=st.session_state.ef_returns,
                mode='lines+markers',
                name='Efficient Frontier',
                line=dict(color='blue', width=2)
            ))

            # Current portfolio
            current_weights = st.session_state.portfolio.get_weights()
            current_perf = calculate_portfolio_performance(
                current_weights,
                st.session_state.returns_data,
                risk_free_rate
            )

            fig.add_trace(go.Scatter(
                x=[current_perf['volatility']],
                y=[current_perf['expected_return']],
                mode='markers',
                name='Current Portfolio',
                marker=dict(size=15, color='red', symbol='star')
            ))

            # Optimized portfolios
            if 'max_sharpe_performance' in st.session_state:
                perf = st.session_state.max_sharpe_performance
                fig.add_trace(go.Scatter(
                    x=[perf['volatility']],
                    y=[perf['expected_return']],
                    mode='markers',
                    name='Max Sharpe',
                    marker=dict(size=12, color='green', symbol='diamond')
                ))

            if 'min_var_performance' in st.session_state:
                perf = st.session_state.min_var_performance
                fig.add_trace(go.Scatter(
                    x=[perf['volatility']],
                    y=[perf['expected_return']],
                    mode='markers',
                    name='Min Variance',
                    marker=dict(size=12, color='orange', symbol='square')
                ))

            fig.update_layout(
                title="Efficient Frontier",
                xaxis_title="Volatility (Risk)",
                yaxis_title="Expected Return",
                hovermode='closest'
            )

            st.plotly_chart(fig, use_container_width=True)

    else:
        st.info("Add stocks and fetch data from the Portfolio tab first")

# ============================================================================
# TAB 5: ANALYTICS
# ============================================================================
with tab5:
    st.header("Advanced Analytics")

    if st.session_state.portfolio.get_tickers() and not st.session_state.returns_data.empty:

        # Correlation heatmap
        st.subheader("Correlation Heatmap")

        corr_matrix = calculate_correlation_matrix(st.session_state.returns_data)

        fig, ax = plt.subplots(figsize=(10, 8))
        sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', center=0, ax=ax,
                   fmt='.2f', square=True, linewidths=1)
        plt.title("Asset Correlation Matrix")
        st.pyplot(fig)

        st.markdown("""
        **Interpretation:** Values close to 1 mean assets move together (high correlation),
        values close to -1 mean they move in opposite directions, and values near 0 mean little relationship.
        """)

        st.markdown("---")

        # PCA Analysis
        st.subheader("Principal Component Analysis (PCA)")

        n_components = min(3, len(st.session_state.returns_data.columns))
        pca_model, loadings, variance_explained = perform_pca(
            st.session_state.returns_data,
            n_components=n_components
        )

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Variance Explained by Each Component:**")
            var_df = pd.DataFrame({
                'Component': [f'PC{i+1}' for i in range(len(variance_explained))],
                'Variance Explained (%)': variance_explained * 100
            })
            st.dataframe(var_df, use_container_width=True)

            st.markdown("""
            **Interpretation:** PCA reveals the main factors driving your portfolio's variance.
            The first component (PC1) captures the most variance, often representing overall market movement.
            """)

        with col2:
            # Scree plot
            fig = go.Figure(data=[
                go.Bar(x=[f'PC{i+1}' for i in range(len(variance_explained))],
                      y=variance_explained * 100)
            ])
            fig.update_layout(
                title="Variance Explained by Components",
                xaxis_title="Principal Component",
                yaxis_title="Variance Explained (%)"
            )
            st.plotly_chart(fig, use_container_width=True)

        # Component loadings
        st.markdown("**Component Loadings:**")
        st.dataframe(loadings, use_container_width=True)

        st.markdown("---")

        # Clustering
        st.subheader("Asset Clustering")

        n_clusters = st.slider("Number of Clusters", min_value=2, max_value=5, value=3)

        labels, cluster_df = cluster_assets(
            st.session_state.returns_data,
            n_clusters=n_clusters,
            features='stats'
        )

        st.dataframe(cluster_df, use_container_width=True)

        # Scatter plot
        fig = px.scatter(
            cluster_df,
            x='Annual Volatility',
            y='Annual Return',
            color='Cluster',
            text='Ticker',
            title='Asset Clustering (Return vs Volatility)',
            color_continuous_scale='viridis'
        )
        fig.update_traces(textposition='top center')
        st.plotly_chart(fig, use_container_width=True)

        st.markdown("""
        **Interpretation:** Clustering groups similar assets together based on their risk-return characteristics.
        Assets in the same cluster tend to behave similarly.
        """)

        st.markdown("---")

        # Diversification metrics
        st.subheader("Diversification Metrics")

        weights = st.session_state.portfolio.get_weights()

        div_ratio = calculate_diversification_ratio(st.session_state.returns_data, weights)

        col1, col2 = st.columns(2)

        with col1:
            st.metric("Diversification Ratio", f"{div_ratio:.3f}")

            # Add diversification insight
            div_insight = interpret_diversification_ratio(div_ratio)
            badge_class = f"badge badge-{div_insight['color']}"
            st.markdown(f"<span class='{badge_class}'>{div_insight['badge']}</span>", unsafe_allow_html=True)
            st.markdown(f"**{div_insight['level']}**")
            st.write(div_insight['explanation'])
            st.caption(div_insight['detail'])
            st.info(div_insight['advice'])

        with col2:
            # Risk contribution
            risk_contrib = calculate_contribution_to_risk(st.session_state.returns_data, weights)
            if not risk_contrib.empty:
                st.markdown("**Risk Contribution by Asset:**")
                st.dataframe(risk_contrib, use_container_width=True)

                # Find highest risk contributor
                max_contrib_idx = risk_contrib['Risk Contribution (%)'].idxmax()
                max_contributor = risk_contrib.loc[max_contrib_idx]
                st.caption(f" **{max_contributor['Ticker']}** contributes the most risk ({max_contributor['Risk Contribution (%)']:.1f}%) despite having only {max_contributor['Weight (%)']:.1f}% weight.")

    else:
        st.info("Add stocks and fetch data from the Portfolio tab first")

# ============================================================================
# TAB 6: REPORT
# ============================================================================
with tab6:
    st.header("Generate Report")

    st.markdown("""
    Download a comprehensive summary of your portfolio analysis, including:
    - Portfolio holdings and metrics
    - Simulation results
    - Optimization suggestions
    - Advanced analytics

    Perfect for sharing with mentors, investment clubs, or keeping track of your learning journey!
    """)

    st.markdown("---")

    if st.button("Generate Report", use_container_width=True):
        # Gather all data
        portfolio_data = {
            'holdings': st.session_state.portfolio.get_holdings_dataframe(),
            'metrics': {
                'total_value': st.session_state.portfolio.get_total_value()
            }
        }

        # Add portfolio stats if available
        if not st.session_state.returns_data.empty:
            weights = st.session_state.portfolio.get_weights()
            stats = calculate_portfolio_stats(
                st.session_state.returns_data,
                weights,
                risk_free_rate
            )
            portfolio_data['metrics'].update(stats)

        simulation_data = {}
        if 'mc_stats' in st.session_state:
            simulation_data = {
                'mc_stats': st.session_state.mc_stats,
                'horizon_days': horizon_days if 'horizon_days' in locals() else 252,
                'n_simulations': n_simulations if 'n_simulations' in locals() else 1000
            }

        optimization_data = {}
        if 'max_sharpe_weights' in st.session_state:
            optimization_data['max_sharpe_weights'] = st.session_state.max_sharpe_weights
            optimization_data['max_sharpe_performance'] = st.session_state.get('max_sharpe_performance', {})
        if 'min_var_weights' in st.session_state:
            optimization_data['min_var_weights'] = st.session_state.min_var_weights
            optimization_data['min_var_performance'] = st.session_state.get('min_var_performance', {})

        analytics_data = {}
        if not st.session_state.returns_data.empty:
            weights = st.session_state.portfolio.get_weights()
            div_ratio = calculate_diversification_ratio(st.session_state.returns_data, weights)
            analytics_data['diversification_ratio'] = div_ratio

            # PCA
            try:
                pca_model, loadings, variance_explained = perform_pca(st.session_state.returns_data)
                analytics_data['pca_variance_explained'] = variance_explained
            except:
                pass

            # Clustering
            try:
                labels, cluster_df = cluster_assets(st.session_state.returns_data, n_clusters=3)
                analytics_data['clusters'] = cluster_df
            except:
                pass

        # Generate report
        report_md = generate_markdown_report(
            portfolio_data,
            simulation_data,
            optimization_data,
            analytics_data
        )

        st.session_state.report = report_md
        st.success("Report generated successfully!")

    # Display and download report
    if 'report' in st.session_state:
        st.markdown("---")
        st.markdown("###  Report Preview")

        with st.expander("View Full Report"):
            st.markdown(st.session_state.report)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.download_button(
                label="Download Report (MD)",
                data=st.session_state.report,
                file_name=f"portfolio_report_{datetime.now().strftime('%Y%m%d')}.md",
                mime="text/markdown",
                use_container_width=True
            )

        with col2:
            if not st.session_state.portfolio.get_holdings_dataframe().empty:
                holdings_csv = generate_holdings_csv(st.session_state.portfolio.get_holdings_dataframe())
                st.download_button(
                    label="Download Holdings (CSV)",
                    data=holdings_csv,
                    file_name=f"holdings_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )

        with col3:
            if 'max_sharpe_weights' in st.session_state:
                weights_csv = generate_weights_csv(st.session_state.max_sharpe_weights)
                st.download_button(
                    label="Download Optimal Weights (CSV)",
                    data=weights_csv,
                    file_name=f"optimal_weights_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    use_container_width=True
                )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 20px;'>
    <p>Portfolio Vision v1.0 | Educational Use Only</p>
    <p>Built with Streamlit, yfinance, and modern portfolio theory</p>
    <p> This tool is for educational purposes only and does not constitute financial advice</p>
</div>
""", unsafe_allow_html=True)
