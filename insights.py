"""
Insights and interpretations module
Provides plain-language explanations of portfolio metrics and results
"""
from typing import Dict, List


def interpret_sharpe_ratio(sharpe: float) -> Dict[str, str]:
    """
    Interpret Sharpe ratio with plain language explanation

    Args:
        sharpe: Sharpe ratio value

    Returns:
        Dictionary with interpretation and color
    """
    if sharpe >= 3.0:
        return {
            'level': 'Exceptional',
            'color': 'success',
            'badge': 'A+',
            'explanation': 'Outstanding risk-adjusted returns. This is considered exceptional performance.',
            'detail': 'Your portfolio is generating excellent returns relative to its risk. This is rare and indicates strong portfolio construction.'
        }
    elif sharpe >= 2.0:
        return {
            'level': 'Very Good',
            'color': 'success',
            'badge': 'A',
            'explanation': 'Very strong risk-adjusted returns. This is better than most portfolios.',
            'detail': 'You are getting very good returns for the amount of risk you are taking. Well-balanced portfolio.'
        }
    elif sharpe >= 1.0:
        return {
            'level': 'Good',
            'color': 'info',
            'badge': 'B',
            'explanation': 'Solid risk-adjusted returns. This is considered good performance.',
            'detail': 'Your returns adequately compensate for the risk. This is above average for most investors.'
        }
    elif sharpe >= 0.5:
        return {
            'level': 'Acceptable',
            'color': 'warning',
            'badge': 'C',
            'explanation': 'Moderate risk-adjusted returns. There is room for improvement.',
            'detail': 'Your returns are acceptable, but you might be taking more risk than necessary. Consider diversification.'
        }
    elif sharpe >= 0:
        return {
            'level': 'Poor',
            'color': 'warning',
            'badge': 'D',
            'explanation': 'Low risk-adjusted returns. Your portfolio could be improved.',
            'detail': 'You are not being well compensated for the risk you are taking. Consider rebalancing or diversifying.'
        }
    else:
        return {
            'level': 'Negative',
            'color': 'error',
            'badge': 'F',
            'explanation': 'Negative risk-adjusted returns. Your portfolio is underperforming.',
            'detail': 'You are earning less than risk-free investments. Significant portfolio changes recommended.'
        }


def interpret_volatility(volatility: float) -> Dict[str, str]:
    """
    Interpret annual volatility with context

    Args:
        volatility: Annual volatility (std deviation)

    Returns:
        Dictionary with interpretation
    """
    if volatility >= 0.40:
        return {
            'level': 'Very High Risk',
            'color': 'error',
            'badge': 'EXTREME',
            'explanation': 'Very high volatility. Expect large price swings.',
            'detail': 'This portfolio could lose or gain 40%+ in a year. Only suitable for very risk-tolerant investors.',
            'advice': 'Consider adding more stable assets like bonds or dividend stocks to reduce volatility.'
        }
    elif volatility >= 0.25:
        return {
            'level': 'High Risk',
            'color': 'warning',
            'badge': 'HIGH',
            'explanation': 'High volatility with significant price fluctuations.',
            'detail': 'Expect swings of 25-40% annually. This is typical of aggressive growth portfolios.',
            'advice': 'Make sure you can handle seeing your portfolio value swing significantly day-to-day.'
        }
    elif volatility >= 0.15:
        return {
            'level': 'Moderate Risk',
            'color': 'info',
            'badge': 'MODERATE',
            'explanation': 'Moderate volatility - balanced portfolio risk.',
            'detail': 'Typical of diversified stock portfolios. Expect 15-25% swings annually.',
            'advice': 'This is a reasonable level of risk for long-term growth investors.'
        }
    elif volatility >= 0.08:
        return {
            'level': 'Low Risk',
            'color': 'success',
            'badge': 'LOW',
            'explanation': 'Low volatility with relatively stable prices.',
            'detail': 'Conservative portfolio with smaller price swings (8-15% annually).',
            'advice': 'Good for risk-averse investors, but returns may be more modest.'
        }
    else:
        return {
            'level': 'Very Low Risk',
            'color': 'success',
            'badge': 'MINIMAL',
            'explanation': 'Very low volatility - highly stable portfolio.',
            'detail': 'Minimal price fluctuations (under 8% annually). Similar to bonds or money market funds.',
            'advice': 'Very safe, but may not keep up with inflation or generate significant growth.'
        }


def interpret_annual_return(annual_return: float, risk_free_rate: float = 0.02) -> Dict[str, str]:
    """
    Interpret annual return with context

    Args:
        annual_return: Annual portfolio return
        risk_free_rate: Risk-free rate for comparison

    Returns:
        Dictionary with interpretation
    """
    if annual_return >= 0.20:
        return {
            'level': 'Excellent',
            'color': 'success',
            'badge': 'EXCELLENT',
            'explanation': 'Excellent returns - well above average.',
            'detail': f'Your portfolio is returning {annual_return:.1%} annually - significantly beating the market average of approximately 10%.',
            'caution': 'Very high returns often come with high risk. Make sure this is sustainable and you understand the risks.'
        }
    elif annual_return >= 0.12:
        return {
            'level': 'Very Good',
            'color': 'success',
            'badge': 'VERY GOOD',
            'explanation': 'Very good returns - beating market average.',
            'detail': f'Your {annual_return:.1%} annual return exceeds typical market performance (approximately 10%).',
            'caution': 'Strong performance. Monitor to ensure it continues and aligns with your risk tolerance.'
        }
    elif annual_return >= 0.07:
        return {
            'level': 'Good',
            'color': 'info',
            'badge': 'GOOD',
            'explanation': 'Solid returns - around market average.',
            'detail': f'Your {annual_return:.1%} annual return is respectable and typical of diversified portfolios.',
            'caution': 'Decent performance. Consider if you could improve returns without taking excessive risk.'
        }
    elif annual_return >= risk_free_rate:
        return {
            'level': 'Below Average',
            'color': 'warning',
            'badge': 'BELOW AVG',
            'explanation': 'Below average returns, but still positive.',
            'detail': f'Your {annual_return:.1%} return is below typical market performance but beats risk-free investments ({risk_free_rate:.1%}).',
            'caution': 'Consider whether the risk you are taking is worth the returns you are getting.'
        }
    elif annual_return >= 0:
        return {
            'level': 'Poor',
            'color': 'warning',
            'badge': 'POOR',
            'explanation': 'Low returns - not beating risk-free rate.',
            'detail': f'Your {annual_return:.1%} return is below the risk-free rate ({risk_free_rate:.1%}). You would earn more in safe bonds.',
            'caution': 'Seriously consider rebalancing. You are taking risk without adequate compensation.'
        }
    else:
        return {
            'level': 'Negative',
            'color': 'error',
            'badge': 'LOSS',
            'explanation': 'Losing money - portfolio is declining.',
            'detail': f'Your portfolio is losing {abs(annual_return):.1%} annually. This needs immediate attention.',
            'caution': 'Significant losses detected. Review your holdings and consider major changes or consult an advisor.'
        }


def interpret_diversification_ratio(div_ratio: float) -> Dict[str, str]:
    """
    Interpret diversification ratio

    Args:
        div_ratio: Diversification ratio (typically 1.0 to 2.0+)

    Returns:
        Dictionary with interpretation
    """
    if div_ratio >= 1.8:
        return {
            'level': 'Excellent',
            'color': 'success',
            'badge': 'EXCELLENT',
            'explanation': 'Excellently diversified portfolio.',
            'detail': f'Diversification ratio of {div_ratio:.2f} indicates very good risk spreading across assets.',
            'advice': 'Your portfolio risk is much less than the weighted average of individual stock risks. Great diversification.'
        }
    elif div_ratio >= 1.4:
        return {
            'level': 'Good',
            'color': 'success',
            'badge': 'GOOD',
            'explanation': 'Well diversified portfolio.',
            'detail': f'Diversification ratio of {div_ratio:.2f} shows good risk reduction through diversification.',
            'advice': 'You are getting meaningful diversification benefits. Keep this balanced approach.'
        }
    elif div_ratio >= 1.1:
        return {
            'level': 'Moderate',
            'color': 'info',
            'badge': 'MODERATE',
            'explanation': 'Moderately diversified portfolio.',
            'detail': f'Diversification ratio of {div_ratio:.2f} indicates some diversification benefit.',
            'advice': 'You have some diversification, but could spread risk better across more uncorrelated assets.'
        }
    else:
        return {
            'level': 'Poor',
            'color': 'warning',
            'badge': 'LIMITED',
            'explanation': 'Limited diversification - concentrated portfolio.',
            'detail': f'Diversification ratio of {div_ratio:.2f} suggests high correlation between holdings.',
            'advice': 'Your assets are moving together. Add stocks from different sectors/industries to reduce risk.'
        }


def interpret_simulation_results(stats: Dict[str, float], initial_value: float, horizon_days: int) -> Dict[str, str]:
    """
    Interpret simulation results with insights

    Args:
        stats: Simulation statistics (p10, p50, p90, etc.)
        initial_value: Starting portfolio value
        horizon_days: Simulation horizon in days

    Returns:
        Dictionary with interpretation
    """
    median_return = (stats['p50'] - initial_value) / initial_value
    downside_risk = (stats['p10'] - initial_value) / initial_value
    upside_potential = (stats['p90'] - initial_value) / initial_value

    # Determine risk level based on spread
    spread = (stats['p90'] - stats['p10']) / initial_value

    if spread >= 1.0:
        risk_level = {
            'level': 'Very High Uncertainty',
            'color': 'error',
            'badge': 'HIGH UNCERTAINTY',
            'explanation': f'Wide range of outcomes: ${stats["p10"]:,.0f} to ${stats["p90"]:,.0f}',
        }
    elif spread >= 0.5:
        risk_level = {
            'level': 'High Uncertainty',
            'color': 'warning',
            'badge': 'MODERATE UNCERTAINTY',
            'explanation': f'Significant range of outcomes: ${stats["p10"]:,.0f} to ${stats["p90"]:,.0f}',
        }
    else:
        risk_level = {
            'level': 'Moderate Uncertainty',
            'color': 'info',
            'badge': 'NORMAL RANGE',
            'explanation': f'Reasonable range of outcomes: ${stats["p10"]:,.0f} to ${stats["p90"]:,.0f}',
        }

    return {
        'risk_level': risk_level,
        'median_interpretation': f'The median projection shows a {median_return:+.1%} return over {horizon_days} days',
        'downside_interpretation': f'In pessimistic scenarios (P10), you could see {downside_risk:+.1%} return',
        'upside_interpretation': f'In optimistic scenarios (P90), you could see {upside_potential:+.1%} return',
        'recommendation': get_simulation_recommendation(median_return, downside_risk, spread)
        }


def get_simulation_recommendation(median_return: float, downside_risk: float, spread: float) -> str:
    """Generate recommendation based on simulation results"""
    if downside_risk < -0.20:
        return "CAUTION: Significant downside risk detected. Consider more conservative allocation."
    elif spread > 0.80:
        return "WARNING: High uncertainty with wide range of outcomes. Ensure you can tolerate volatility."
    elif median_return > 0.15 and downside_risk > -0.10:
        return "FAVORABLE: Attractive risk/reward profile with good upside and manageable downside."
    elif median_return > 0 and downside_risk > -0.15:
        return "ACCEPTABLE: Reasonable outlook with positive expected return and acceptable risk."
    else:
        return "REVIEW NEEDED: Risk-return profile may need adjustment."


def generate_portfolio_summary_insights(
    total_value: float,
    num_holdings: int,
    annual_return: float,
    volatility: float,
    sharpe_ratio: float,
    risk_free_rate: float = 0.02
) -> List[str]:
    """
    Generate overall portfolio insights

    Args:
        total_value: Total portfolio value
        num_holdings: Number of holdings
        annual_return: Annual return
        volatility: Annual volatility
        sharpe_ratio: Sharpe ratio
        risk_free_rate: Risk-free rate

    Returns:
        List of insight strings
    """
    insights = []

    # Portfolio size insight
    if num_holdings < 3:
        insights.append("**Limited Holdings**: You have fewer than 3 stocks. Consider adding more for better diversification.")
    elif num_holdings <= 10:
        insights.append(f"**Good Diversification**: {num_holdings} holdings is a reasonable number for a diversified portfolio.")
    else:
        insights.append(f"**Well Diversified**: {num_holdings} holdings provides strong diversification, though 8-15 is typically optimal.")

    # Return vs risk insight
    return_interpret = interpret_annual_return(annual_return, risk_free_rate)
    insights.append(f"**Returns**: {return_interpret['explanation']}")

    vol_interpret = interpret_volatility(volatility)
    insights.append(f"**Risk Level**: {vol_interpret['explanation']}")

    sharpe_interpret = interpret_sharpe_ratio(sharpe_ratio)
    insights.append(f"**Risk-Adjusted Performance**: {sharpe_interpret['explanation']}")

    # Overall recommendation
    if sharpe_ratio >= 1.0 and num_holdings >= 5:
        insights.append("**Overall Assessment**: Well-constructed portfolio with good diversification and risk-adjusted returns.")
    elif sharpe_ratio >= 0.5:
        insights.append("**Overall Assessment**: Decent portfolio. Consider optimization to improve risk-adjusted returns.")
    else:
        insights.append("**Overall Assessment**: Portfolio could benefit from rebalancing and better diversification. Use the Optimize tab.")

    return insights


def get_optimization_comparison_insights(
    current_sharpe: float,
    optimized_sharpe: float,
    current_volatility: float,
    optimized_volatility: float
) -> Dict[str, str]:
    """
    Generate insights comparing current vs optimized portfolio

    Args:
        current_sharpe: Current Sharpe ratio
        optimized_sharpe: Optimized Sharpe ratio
        current_volatility: Current volatility
        optimized_volatility: Optimized volatility

    Returns:
        Dictionary with comparison insights
    """
    sharpe_improvement = ((optimized_sharpe - current_sharpe) / abs(current_sharpe) * 100) if current_sharpe != 0 else 0
    vol_reduction = ((current_volatility - optimized_volatility) / current_volatility * 100) if current_volatility != 0 else 0

    if sharpe_improvement > 20:
        return {
            'level': 'Significant Improvement Potential',
            'color': 'success',
            'badge': 'RECOMMENDED',
            'message': f'Optimization could improve your Sharpe ratio by {sharpe_improvement:.1f}%',
            'detail': f'This means much better risk-adjusted returns. Strongly consider rebalancing.',
            'action': 'RECOMMENDATION: Adopt the optimized weights to significantly improve your portfolio.'
        }
    elif sharpe_improvement > 10:
        return {
            'level': 'Good Improvement Potential',
            'color': 'success',
            'badge': 'BENEFICIAL',
            'message': f'Optimization could improve your Sharpe ratio by {sharpe_improvement:.1f}%',
            'detail': f'Better risk-adjusted returns available with rebalancing.',
            'action': 'RECOMMENDATION: Consider moving toward the optimized allocation.'
        }
    elif sharpe_improvement > 0:
        return {
            'level': 'Minor Improvement Potential',
            'color': 'info',
            'badge': 'OPTIONAL',
            'message': f'Optimization could improve your Sharpe ratio by {sharpe_improvement:.1f}%',
            'detail': f'Small gains available, but your current allocation is reasonable.',
            'action': 'RECOMMENDATION: Your portfolio is already fairly well optimized.'
        }
    else:
        return {
            'level': 'Already Well Optimized',
            'color': 'success',
            'badge': 'OPTIMAL',
            'message': 'Your current portfolio is already well optimized',
            'detail': 'The suggested allocation is very similar to your current holdings.',
            'action': 'RECOMMENDATION: Keep your current allocation - it is already close to optimal.'
        }
