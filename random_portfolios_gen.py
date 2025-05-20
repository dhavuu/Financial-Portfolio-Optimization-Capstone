# random_portfolios_gen.py

import pandas as pd
import numpy as np

def return_portfolios(expected_returns, cov_matrix, num_portfolios=10000):
    """
    Generates random portfolios with non-negative weights summing to 1.

    Args:
        expected_returns (pd.Series or np.array): Expected returns for each asset.
                                                 Index/order should match cov_matrix rows/cols.
        cov_matrix (pd.DataFrame or np.array): Covariance matrix of asset returns.
        num_portfolios (int): The number of random portfolios to generate.

    Returns:
        pd.DataFrame: DataFrame containing returns, volatility, and weights for each random portfolio.
                      Returns and volatility are at the frequency of the input data.
    """
    # Ensure inputs are numpy arrays for consistent calculations
    if isinstance(expected_returns, pd.Series):
        asset_names = expected_returns.index
        expected_returns = expected_returns.values
    else:
        asset_names = [f'Asset_{i+1}' for i in range(len(expected_returns))] # Default names

    if isinstance(cov_matrix, pd.DataFrame):
        cov_matrix = cov_matrix.values


    num_assets = len(expected_returns)
    if cov_matrix.shape != (num_assets, num_assets):
        print("Error: Covariance matrix shape does not match the number of assets.", file=sys.stderr)
        return None

    # Ensure cov_matrix is float type
    cov_matrix = cov_matrix.astype(float)


    port_returns = []
    port_volatility = []
    stock_weights = []

    for _ in range(num_portfolios):
        # Generate random weights between 0 and 1
        weights = np.random.random(num_assets)
        # Normalize weights to sum to 1
        weights /= np.sum(weights)

        # Calculate portfolio return
        returns = np.dot(weights, expected_returns)

        # Calculate portfolio volatility
        # np.dot(weights.T, np.dot(cov_matrix, weights)) is w' * Sigma * w
        volatility = np.sqrt(np.dot(weights.T, np.dot(cov_matrix, weights)))

        port_returns.append(returns)
        port_volatility.append(volatility)
        stock_weights.append(weights)

    portfolio = {'Returns': port_returns, 'Volatility': port_volatility}

    # Add weights for each asset
    # stock_weights is a list of arrays/lists, where each inner list is weights for one portfolio
    # We need to transpose this concept to get lists of weights per asset across portfolios
    # Example: [[w1_p1, w2_p1], [w1_p2, w2_p2]] -> [[w1_p1, w1_p2], [w2_p1, w2_p2]]
    weights_per_asset = np.array(stock_weights).T # Transpose the list of weight vectors

    for i, asset_name in enumerate(asset_names):
        portfolio[f'{asset_name}Weight'] = weights_per_asset[i].tolist()


    df = pd.DataFrame(portfolio)

    # Define column order: Returns, Volatility, then asset weights
    weight_cols = [f'{asset}Weight' for asset in asset_names]
    column_order = ['Returns', 'Volatility'] + weight_cols

    return df[column_order]