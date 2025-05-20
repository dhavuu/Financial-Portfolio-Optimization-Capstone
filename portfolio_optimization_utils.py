import numpy as np
import pandas as pd
from cvxopt import matrix, solvers

# Suppress solver output
solvers.options['show_progress'] = False

def optimize_portfolio(returns_df, risk_free_rate, weight_bounds):
    """
    Optimizes a portfolio to find the efficient frontier, max Sharpe, and min variance portfolios.

    Args:
        returns_df (pd.DataFrame): DataFrame of asset returns.
        risk_free_rate (float): Per-period risk-free rate.
        weight_bounds (tuple or list of tuples):
            If tuple (min_w, max_w), applies to all weights.
            If list of tuples [(min_w1, max_w1), (min_w2, max_w2), ...], applies per asset.

    Returns:
        dict: Contains 'efficient_frontier' DataFrame, 'max_sharpe_portfolio' dict,
              'min_variance_portfolio' dict.
    """
    if returns_df.empty or len(returns_df) < 2:
        print("Error: Not enough data for portfolio optimization.")
        return None

    # Calculate annualized mean returns and covariance matrix
    # Note: These are for the period, not annualized yet. Annualization happens in results.
    mu = returns_df.mean().values # Expected returns (arithmetic mean)
    sigma = returns_df.cov().values # Covariance matrix

    num_assets = len(mu)

    # Convert to CVXOPT matrices
    P = matrix(sigma)
    q = matrix(0.0, (num_assets, 1)) # No direct return term in min variance objective

    # --- Equality Constraints (Sum of weights = 1) ---
    # A*w = b
    # A = [1, 1, ..., 1]
    # b = 1.0
    A = matrix(1.0, (1, num_assets))
    b = matrix(1.0)

    # --- Inequality Constraints (Min/Max Weight Constraints) ---
    # G*w <= h
    # For each asset i:
    # w_i >= min_w_i  => -w_i <= -min_w_i
    # w_i <= max_w_i

    # Determine individual bounds for each asset
    min_weights = np.zeros(num_assets)
    max_weights = np.ones(num_assets)

    if isinstance(weight_bounds, tuple) and len(weight_bounds) == 2:
        # Single (min_w, max_w) tuple for all assets
        min_weights.fill(weight_bounds[0])
        max_weights.fill(weight_bounds[1])
    elif isinstance(weight_bounds, list) and len(weight_bounds) == num_assets:
        # List of (min_w, max_w) tuples for each asset
        for i, (min_w, max_w) in enumerate(weight_bounds):
            min_weights[i] = min_w
            max_weights[i] = max_w
    else:
        # Fallback to default (0,1) if bounds are malformed, or raise error
        print("Warning: Invalid weight_bounds format. Using default (0.0, 1.0) for all assets.")
        min_weights.fill(0.0)
        max_weights.fill(1.0)

    # Construct G and h matrices for individual min/max bounds
    G = matrix(np.vstack((-np.eye(num_assets), np.eye(num_assets))))
    h = matrix(np.vstack((-min_weights.reshape(-1, 1), max_weights.reshape(-1, 1))))


    # --- Efficient Frontier Calculation ---
    # We will iterate through target returns to build the efficient frontier
    # The objective is to minimize portfolio variance for a given target return.
    # New constraint: mu_T * w = target_return

    # Range of target returns (from min individual asset return to max individual asset return)
    min_return = mu.min()
    max_return = mu.max()
    num_target_returns = 100 # Number of points on the efficient frontier

    # Create a range of target returns
    target_returns = np.linspace(min_return, max_return, num_target_returns)

    efficient_frontier = []
    max_sharpe_portfolio = None
    min_variance_portfolio = None
    max_sharpe_ratio = -np.inf # Initialize with negative infinity

    for r_target in target_returns:
        # For each target return, add an equality constraint A_eq * w = b_eq
        # A_eq = [mu_1, mu_2, ..., mu_N]
        # b_eq = target_return
        A_target_return = matrix(mu, (1, num_assets)) # Reshape mu to be a row vector
        b_target_return = matrix(r_target)

        # Combine existing A, b with the new target return constraint
        A_qp = matrix(np.vstack((A, A_target_return))) # A_qp = [[1,...1], [mu_1,...mu_N]]
        b_qp = matrix(np.vstack((b, b_target_return))) # b_qp = [[1], [target_return]]

        try:
            sol = solvers.qp(P, q, G, h, A_qp, b_qp)
            if sol['status'] == 'optimal':
                weights = np.array(sol['x']).flatten()
                portfolio_return = np.dot(weights, mu)
                portfolio_risk = np.sqrt(np.dot(weights.T, np.dot(sigma, weights)))
                sharpe_ratio = (portfolio_return - risk_free_rate) / portfolio_risk if portfolio_risk > 0 else -np.inf

                efficient_frontier.append({
                    'return': portfolio_return,
                    'risk': portfolio_risk,
                    'sharpe': sharpe_ratio,
                    **{f'weight_{returns_df.columns[i]}': w for i, w in enumerate(weights)}
                })

                if sharpe_ratio > max_sharpe_ratio:
                    max_sharpe_ratio = sharpe_ratio
                    max_sharpe_portfolio = {
                        'weights': {returns_df.columns[i]: w for i, w in enumerate(weights)},
                        'return': portfolio_return,
                        'risk': portfolio_risk,
                        'sharpe': sharpe_ratio
                    }
            else:
                pass # Skip non-optimal solutions
        except ValueError:
            pass # Skip problematic target returns


    efficient_frontier_df = pd.DataFrame(efficient_frontier)

    # --- Minimum Variance Portfolio ---
    # This is found by setting q to the expected returns and finding the minimum variance point
    # on the efficient frontier. Alternatively, it's the solution to QP with q=0 and no target return constraint.
    # The efficient frontier already contains the min variance point (leftmost point).
    if not efficient_frontier_df.empty:
        min_variance_row = efficient_frontier_df.loc[efficient_frontier_df['risk'].idxmin()]
        min_variance_portfolio = {
            'weights': {returns_df.columns[i]: min_variance_row[f'weight_{returns_df.columns[i]}'] for i in range(num_assets)},
            'return': min_variance_row['return'],
            'risk': min_variance_row['risk'],
            'sharpe': min_variance_row['sharpe']
        }

    # If the efficient frontier calculation didn't yield a max sharpe, try to explicitly find it
    if max_sharpe_portfolio is None and not efficient_frontier_df.empty:
        # Find the row with the maximum Sharpe Ratio
        max_sharpe_row = efficient_frontier_df.loc[efficient_frontier_df['sharpe'].idxmax()]
        max_sharpe_portfolio = {
            'weights': {returns_df.columns[i]: max_sharpe_row[f'weight_{returns_df.columns[i]}'] for i in range(num_assets)},
            'return': max_sharpe_row['return'],
            'risk': max_sharpe_row['risk'],
            'sharpe': max_sharpe_row['sharpe']
        }


    return {
        'efficient_frontier': efficient_frontier_df,
        'max_sharpe_portfolio': max_sharpe_portfolio,
        'min_variance_portfolio': min_variance_portfolio
    }