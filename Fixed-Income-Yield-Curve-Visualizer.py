# Cell 1: Import Libraries and Set Up API Key

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.interpolate import UnivariateSpline
from scipy.optimize import curve_fit
from fredapi import Fred
import plotly.graph_objects as go
import plotly.express as px

# Replace with your actual FRED API key
YOUR_API_KEY = "YOUR_API_KEY"



# Cell 2: Data Fetching and Corporate Yield Simulation Functions

def fetch_treasury_yield_data(api_key):
    """
    Fetch the latest U.S. Treasury yields for a range of maturities using the FRED API.
    
    Returns:
        pd.DataFrame: DataFrame with 'Maturity' (in years) and 'Yield' (in %)
    """
    fred = Fred(api_key=api_key)
    
    # Define series IDs for various Treasury maturities.
    series_ids = {
        0.25: 'DGS3MO',   # 3-Month Treasury
        0.5:  'DGS6MO',   # 6-Month Treasury
        1:    'DGS1',     # 1-Year Treasury
        2:    'DGS2',     # 2-Year Treasury
        3:    'DGS3',     # 3-Year Treasury
        5:    'DGS5',     # 5-Year Treasury
        7:    'DGS7',     # 7-Year Treasury
        10:   'DGS10',    # 10-Year Treasury
        20:   'DGS20',    # 20-Year Treasury
        30:   'DGS30'     # 30-Year Treasury
    }
    
    data = []
    for maturity, series_id in series_ids.items():
        series = fred.get_series(series_id).dropna()
        if not series.empty:
            latest_yield = series.iloc[-1]
            data.append({'Maturity': maturity, 'Yield': latest_yield})
        else:
            print(f"No data found for series {series_id}")
    
    df = pd.DataFrame(data).sort_values(by='Maturity')
    return df

def simulate_corporate_yield_curve(risk_free_df):
    """
    Simulate a corporate yield curve by adding a maturity-dependent credit spread
    to the Treasury yields. The credit spread is based on assumed historical averages.
    
    Args:
        risk_free_df (pd.DataFrame): Treasury yield curve data with columns ['Maturity', 'Yield'].
        
    Returns:
        np.array: Simulated corporate yields for each maturity.
    
    For example, we assume:
      - At 2 years: average spread of 1.0%
      - At 5 years: average spread of 1.5%
      - At 10 years: average spread of 2.0%
      - At 20 years: average spread of 2.5%
      - At 30 years: average spread of 3.0%
    
    The function interpolates these values to assign a credit spread to each maturity.
    """
    # Define known maturities and their average spreads (in %)
    known_maturities = np.array([2, 5, 10, 20, 30])
    known_spreads = np.array([1.0, 1.5, 2.0, 2.5, 3.0])
    
    # Interpolate the credit spread for each maturity in the Treasury data
    treasury_maturities = risk_free_df['Maturity'].values
    interpolated_spreads = np.interp(treasury_maturities, known_maturities, known_spreads)
    
    # Simulated corporate yields = Treasury yields + interpolated spread
    corporate_yields = risk_free_df['Yield'].values + interpolated_spreads
    return corporate_yields



# Cell 3: Yield Curve Fitting Functions

def cubic_spline_curve(maturities, yields, num_points=200):
    """
    Fit a cubic spline interpolation to the yield data.
    
    Args:
        maturities (array-like): Maturities in years.
        yields (array-like): Yield values.
        num_points (int): Number of points for the interpolated curve.
    
    Returns:
        tuple: (x_new, y_new) for the interpolated curve.
    
    Explanation:
    The cubic spline method fits a smooth curve through the observed data points,
    ensuring that the curve passes exactly through each point. It is flexible
    and useful for visualizing how yields change with maturity.
    """
    spline = UnivariateSpline(maturities, yields, s=0)
    x_new = np.linspace(min(maturities), max(maturities), num_points)
    y_new = spline(x_new)
    return x_new, y_new

def nelson_siegel(t, beta0, beta1, beta2, tau):
    """
    Nelson-Siegel model for the yield curve.
    
    Args:
        t (array-like): Maturities.
        beta0 (float): Level factor (long-term).
        beta1 (float): Slope factor (short-term).
        beta2 (float): Curvature factor (medium-term).
        tau (float): Decay factor.
    
    Returns:
        np.array: Modeled yield values.
    
    Explanation:
    The Nelson-Siegel model uses a small number of parameters to capture the
    level, slope, and curvature of the yield curve. It is widely used in practice
    for both policy analysis and asset pricing.
    """
    t = np.array(t)
    factor = np.where(t == 0, 1.0, (1 - np.exp(-t/tau)) / (t/tau))
    factor2 = factor - np.exp(-t/tau)
    return beta0 + beta1 * factor + beta2 * factor2

def fit_nelson_siegel(maturities, yields):
    """
    Fit the Nelson-Siegel model to the yield data.
    
    Args:
        maturities (array-like): Maturities in years.
        yields (array-like): Observed yields.
    
    Returns:
        tuple: Fitted parameters (beta0, beta1, beta2, tau).
    """
    initial_guess = [np.mean(yields), -1.0, 1.0, 1.0]
    params, _ = curve_fit(nelson_siegel, maturities, yields, p0=initial_guess, maxfev=10000)
    return params



# Cell 4: Spread Calculation and Interactive Visualization Functions

def compute_specific_spread(maturities, yields, short=2, long=10):
    """
    Compute the spread between yields at two specific maturities (e.g., 10Y - 2Y).
    
    Args:
        maturities (array-like): Maturities in years.
        yields (array-like): Yields corresponding to maturities.
        short (float): Short-term maturity (e.g., 2 years).
        long (float): Long-term maturity (e.g., 10 years).
    
    Returns:
        float: Spread (yield at long maturity minus yield at short maturity).
    """
    df = pd.DataFrame({'Maturity': maturities, 'Yield': yields})
    yield_short = np.interp(short, df['Maturity'], df['Yield'])
    yield_long  = np.interp(long, df['Maturity'], df['Yield'])
    return yield_long - yield_short

def compute_credit_spreads(risk_free_yields, corporate_yields):
    """
    Compute credit spreads as the difference between corporate and risk-free yields.
    
    Args:
        risk_free_yields (array-like): Risk-free yields.
        corporate_yields (array-like): Corporate bond yields.
    
    Returns:
        np.array: Credit spreads.
    """
    return np.array(corporate_yields) - np.array(risk_free_yields)

def plot_interactive_yield_curves(maturities, risk_free_yields, corporate_yields, 
                                  spline_x_rf, spline_y_rf, ns_x_rf, ns_y_rf):
    """
    Create an interactive Plotly graph showing:
      - The risk-free yield curve (observed data, cubic spline, and Nelson-Siegel fit)
      - The simulated corporate yield curve.
    """
    fig = go.Figure()
    
    # Risk-Free Observed Yields
    fig.add_trace(go.Scatter(
        x=maturities, y=risk_free_yields,
        mode='markers',
        name='Risk-Free Observed',
        marker=dict(color='blue', size=10),
        hovertemplate="Maturity: %{x} yrs<br>Yield: %{y:.2f}%"
    ))
    
    # Cubic Spline Fit for Risk-Free Yields
    fig.add_trace(go.Scatter(
        x=spline_x_rf, y=spline_y_rf,
        mode='lines',
        name='Risk-Free Spline Fit',
        line=dict(dash='dash', color='green'),
        hovertemplate="Maturity: %{x:.2f} yrs<br>Yield: %{y:.2f}%"
    ))
    
    # Nelson-Siegel Fit for Risk-Free Yields
    fig.add_trace(go.Scatter(
        x=ns_x_rf, y=ns_y_rf,
        mode='lines',
        name='Risk-Free Nelson-Siegel',
        line=dict(color='red'),
        hovertemplate="Maturity: %{x:.2f} yrs<br>Yield: %{y:.2f}%"
    ))
    
    # Simulated Corporate Yield Curve
    fig.add_trace(go.Scatter(
        x=maturities, y=corporate_yields,
        mode='markers+lines',
        name='Simulated Corporate Yields',
        marker=dict(color='orange', size=8),
        line=dict(color='orange', width=2),
        hovertemplate="Maturity: %{x} yrs<br>Yield: %{y:.2f}%"
    ))
    
    fig.update_layout(
        title="Interactive Yield Curves: Risk-Free vs. Simulated Corporate",
        xaxis_title="Maturity (Years)",
        yaxis_title="Yield (%)",
        hovermode="x unified",
        template="plotly_white"
    )
    fig.show()

def plot_interactive_credit_spread(maturities, credit_spreads):
    """
    Create an interactive Plotly graph for the credit spread (corporate minus risk-free yields) 
    across maturities.
    """
    fig = px.line(x=maturities, y=credit_spreads, markers=True, 
                  labels={'x': 'Maturity (Years)', 'y': 'Credit Spread (%)'},
                  title="Interactive Credit Spread Across Maturities")
    fig.update_traces(hovertemplate="Maturity: %{x} yrs<br>Spread: %{y:.2f}%")
    fig.update_layout(template="plotly_white")
    fig.show()

def plot_yield_inversion(maturities, yields, short=2, long=10):
    """
    Plot the 10-year minus 2-year yield spread.
    Display a message below the graph in green if the curve is normal (10Y > 2Y)
    or in red if the curve is inverted.
    """
    df = pd.DataFrame({'Maturity': maturities, 'Yield': yields})
    yield_2 = np.interp(short, df['Maturity'], df['Yield'])
    yield_10 = np.interp(long, df['Maturity'], df['Yield'])
    spread = yield_10 - yield_2
    
    fig = go.Figure()
    fig.add_trace(go.Bar(
        x=["10Y-2Y Spread"],
        y=[spread],
        text=[f"{spread:.2f}%"],
        textposition='auto',
        marker_color='teal'
    ))
    fig.update_layout(
        title="10-Year Minus 2-Year Yield Spread",
        yaxis_title="Spread (%)",
        template="plotly_white"
    )
    fig.show()
    
    # Display a colored message based on the spread
    if spread >= 0:
        message = f"Yield Curve is Normal (10Y - 2Y Spread = {spread:.2f}%)"
        color = "green"
    else:
        message = f"Yield Curve is Inverted (10Y - 2Y Spread = {spread:.2f}%)"
        color = "red"
        
    from IPython.display import display, HTML
    display(HTML(f"<h3 style='color:{color};'>{message}</h3>"))



# Cell 5: Main Execution Flow

# 1. Fetch risk-free Treasury yield data from FRED
treasury_df = fetch_treasury_yield_data(YOUR_API_KEY)
if treasury_df.empty:
    raise ValueError("No Treasury yield data was fetched. Check your API key and series IDs.")

maturities = treasury_df['Maturity'].values
risk_free_yields = treasury_df['Yield'].values

# 2. Simulate a corporate yield curve using an interpolation of assumed credit spreads
corporate_yields = simulate_corporate_yield_curve(treasury_df)

# 3. Fit the risk-free yield curve using cubic spline interpolation
spline_x_rf, spline_y_rf = cubic_spline_curve(maturities, risk_free_yields)

# 4. Fit the Nelson-Siegel model to the risk-free data
ns_params_rf = fit_nelson_siegel(maturities, risk_free_yields)
print("Fitted Nelson-Siegel parameters (Risk-Free):", ns_params_rf)
ns_x_rf = np.linspace(min(maturities), max(maturities), 200)
ns_y_rf = nelson_siegel(ns_x_rf, *ns_params_rf)

# 5. Compute the specific 10Y-2Y spread for the risk-free yield curve
spread_rf = compute_specific_spread(maturities, risk_free_yields, short=2, long=10)
print(f"Risk-Free 10Y-2Y Spread: {spread_rf:.2f}%")

# 6. Compute credit spreads (difference between simulated corporate and risk-free yields)
credit_spreads = compute_credit_spreads(risk_free_yields, corporate_yields)

# 7. Plot interactive yield curves (Risk-Free vs. Simulated Corporate)
plot_interactive_yield_curves(maturities, risk_free_yields, corporate_yields, 
                              spline_x_rf, spline_y_rf, ns_x_rf, ns_y_rf)

# 8. Plot interactive credit spread across maturities
plot_interactive_credit_spread(maturities, credit_spreads)

# 9. Plot the 10Y-2Y yield spread and display inversion message
plot_yield_inversion(maturities, risk_free_yields, short=2, long=10)

