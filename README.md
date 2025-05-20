# Portfolio Optimization for Long-Term Growth: A Case Study for Anita

## Project Overview

This project focuses on developing a data-driven investment portfolio recommendation tailored to a specific client's long-term financial goals and risk profile. Utilizing historical stock market data and modern portfolio theory, the aim is to construct an optimized equity portfolio for wealth creation, specifically targeting funds for college education.

## Client Profile: Anita

* **Investment Goal:** Funding Kids' College Fees.
* **Time Horizon:** 20 years.
* **Investment Amount:** INR 10,00,000 in stocks from total savings of INR 20,00,000.
* **Risk Tolerance:** High, driven by the desire to accumulate substantial capital for college fees.
* **Return Objective:** Target annual return of 28%.

## Data Source & Initial Stock Universe

Historical stock data was retrieved using the `yfinance` library for 10 prominent Indian stocks across various sectors and market capitalizations.

**Initial Stock Universe:**

| Company                    | Symbol        | Capitalisation | Sector                          |
| :------------------------- | :------------ | :------------- | :------------------------------ |
| Kotak Mahindra Bank Ltd.   | KOTAKBANK.NS  | Large Cap      | Financial Services              |
| ITC Ltd                    | ITC.NS        | Large Cap      | Fast Moving Consumer Goods      |
| Tata Power Co. Ltd         | TATAPOWER.NS  | Large Cap      | Power                           |
| Tata Consultancy Services  | TCS.NS        | Large Cap      | Information Technology          |
| PETRONET LNG LTD.          | PETRONET.NS   | Mid Cap        | Oil Gas & Consumable Fuels      |
| Glenmark Pharmaceuticals ltd | GLENMARK.NS   | Mid Cap        | Healthcare                      |
| Shree Cements Ltd.         | SHREECEM.NS   | Mid Cap        | Construction Materials          |
| Blue Dart Express Ltd.     | BLUEDART.NS   | Small Cap      | Services                        |
| BASF India Ltd             | BASF.NS       | Small Cap      | Chemicals                       |
| Apollo Tyres Ltd           | APOLLOTYRE.NS | Small Cap      | Automobile and Auto Components  |


## Methodology

The project employed a multi-faceted approach to portfolio construction and optimization:

1.  **Historical Performance Analysis:** Comprehensive analysis of individual stock performance (Annualized Geometric Return, Arithmetic Return, Volatility, Sharpe Ratio) over 6 months, 5 years, and 21 years.
2.  **Strategic Stock Selection (Momentum-Based):**
    * **Momentum Persistence:** Identified stocks that were top performers (strongest returns) over the last 6 months, as these tend to continue outperforming in the short-to-medium term.
    * **Momentum Reversal:** Identified stocks that were underperformers (lowest returns) over the last 5 years, as strong long-term trends can sometimes reverse, presenting potential value opportunities.
    * Based on combining these two momentum strategies, 6 stocks were selected from the initial 10 for further portfolio optimization. The selected stocks were: APOLLOTYRE.NS, ITC.NS, KOTAKBANK.NS, PETRONET.NS, SHREECEM.NS, TCS.NS.
3.  **Correlation Analysis:** Examination of inter-stock correlations across different timeframes (6M, 5Y, 21Y) to understand diversification benefits.
4.  **Portfolio Optimization (Mean-Variance Optimization):**
    * Utilized historical data (21-year period) to simulate thousands of random portfolios.
    * Calculated the Efficient Frontier, representing optimal portfolios that offer the maximum return for a given level of risk.
    * Identified key portfolios on the Efficient Frontier: Minimum Volatility Portfolio, Maximum Sharpe Ratio Portfolio, and a custom portfolio tailored to the client's specific return objective.

## Key Findings & Portfolio Recommendation

The analysis indicates that a well-diversified and optimized portfolio can effectively meet Anita's long-term growth objectives.

### Optimized Portfolio for Target Annual Return (29.00%)

For Anita's specific goal of achieving a 28% annual return over 20 years, we recommend the following optimized portfolio, which minimizes volatility to achieve a target return of 29.00% (the closest achievable point on the efficient frontier):

* **Annualized Return (Arithmetic Mean):** 29.12%
* **Annualized Volatility (Risk):** 24.97%
* **Sharpe Ratio (Annualized):** 0.97

**Portfolio Weights:**

* APOLLOTYRE.NS: 0%
* ITC.NS: 3.76%
* KOTAKBANK.NS: 27.47%
* PETRONET.NS: 8.77%
* SHREECEM.NS: 30.0%
* TCS.NS: 30.0%

This portfolio strategically allocates significant weights to **Shree Cements (30.0%)**, **TCS (30.0%)**, and **Kotak Mahindra Bank (27.47%)**, reflecting their strong long-term performance and contribution to the optimal risk-return profile for the target.

### Other Optimized Portfolios Analyzed:

| Portfolio Type          | Annualized Return (%) | Annualized Volatility (%) | Sharpe Ratio (Annualized) |
| :---------------------- | :-------------------- | :------------------------ | :------------------------ |
| Minimum Variance (21Y)  | 25.73%                | 21.14%                    | 0.98                      |
| Maximum Sharpe (21Y)    | 26.86%                | 21.88%                    | 1.00                      |
| User Defined            | 26.81%                | 24.00%                    | 0.91                      |


## Visualizations

Key visualizations generated as part of this project include:

* **Annualized Geometric Return Comparison Across Periods:** Bar charts illustrating stock performance over 6 months, 5 years, and 21 years.
* **Annualized Volatility Comparison Across Periods:** Bar charts showing the risk (volatility) of individual stocks over the same periods.
* **Correlation Heatmaps:** Visual representation of how selected stocks move in relation to each other across different timeframes (6 months, 5 years, 21 years), highlighting diversification benefits.
* **Portfolio Optimization Plot (Efficient Frontier):** A scatter plot showcasing random portfolios, individual stocks, and the optimal Efficient Frontier curve, along with the identified Minimum Variance, Maximum Sharpe, and Target Return portfolios.

## Technologies Used

* **Python:** Programming language for analysis.
* **Pandas:** Data manipulation and analysis.
* **NumPy:** Numerical operations.
* **Matplotlib:** Data visualization.
* **`yfinance`:** To fetch historical stock data.
* **`cvxopt`:** For convex optimization to calculate the efficient frontier.
* **Jupyter Notebook:** For interactive analysis and code development.

## How to Run the Project

To replicate this analysis:

1.  **Clone the repository:**
    You can clone the repository using the following command:
    ```bash
    git clone https://github.com/dhavuu/Financial-Portfolio-Optimization-Capstone
    ```
    Then navigate into the project directory:
    ```bash
    cd Financial-Portfolio-Optimization-Capstone
    ```
2.  **Install dependencies:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Run the Jupyter Notebook:**
    ```bash
    jupyter notebook
    ```
    Open the `.ipynb` file (e.g., `Main_script.ipynb`) and run all cells to reproduce the analysis and visualizations.

## Project Files

* `Main_script.ipynb`: The main Jupyter Notebook containing all the analysis and code.
* `portfolio_optimization_utils.py`: Utility functions and classes used in the portfolio optimization process.
* `random_portfolios_gen.py`: Script for generating random portfolios to illustrate the efficient frontier.
* `requirements.txt`: Lists all Python libraries and their versions required to run the project.
* `Portfolio Recommendation.pptx`: The presentation summarizing the project and recommendations.

---
**Dhaval Padhiyar** | [LinkedIn Profile](https://www.linkedin.com/in/dhaval-padhiyar)
