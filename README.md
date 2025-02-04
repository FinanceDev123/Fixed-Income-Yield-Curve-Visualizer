📈 Yield Curve Analysis Dashboard 📉

An interactive Python-based dashboard for analyzing U.S. Treasury yield curves, corporate bond yields, and credit spreads. The tool leverages FRED API to fetch Treasury yields and simulates corporate bond yields based on historical credit spread assumptions. It features yield curve fitting methods, credit spread analysis, and scenario simulation tools for risk assessment.

🚀 Project Overview

Interest rates and bond yields are fundamental to fixed-income markets, monetary policy, and macroeconomic analysis. This dashboard enables users to:

✅ Fetch real-time U.S. Treasury yield data using the FRED API.✅ Simulate a corporate yield curve by applying historical credit spreads.✅ Fit yield curves using Spline and Nelson-Siegel methods for better visualization.✅ Analyze credit spreads to compare risk-free and corporate bond yields.✅ Perform 10Y-2Y spread analysis to detect yield curve inversions.✅ Use scenario analysis tools to simulate yield shifts and credit spread widening.

🏰 How It Works

1️⃣ Fetching Treasury Yields 📈

The dashboard pulls U.S. Treasury yields from FRED (Federal Reserve Economic Data) for maturities ranging from 3 months to 30 years.

Data is stored in a structured format for further analysis.

2️⃣ Simulating Corporate Bond Yields 💳

Corporate bond yields are estimated by adding a maturity-dependent credit spread to Treasury yields.

Assumed credit spreads (based on historical averages):

2-Year Bonds: +1.0%

5-Year Bonds: +1.5%

10-Year Bonds: +2.0%

20-Year Bonds: +2.5%

30-Year Bonds: +3.0%

These spreads are interpolated to estimate corporate yields across all maturities.

3️⃣ Yield Curve Fitting Methods ⚖️

The dashboard uses two primary methods to fit the yield curve:

Cubic Spline Fit: Provides a flexible, smooth curve through the observed Treasury yields.

Nelson-Siegel Model: A parametric model that captures yield curve shape using level, slope, and curvature factors.

4️⃣ Credit Spread Analysis 📉

The spread between corporate and Treasury yields is calculated at each maturity.

A visual representation of the credit spread curve helps compare investment-grade vs. risk-free bonds.

5️⃣ 10Y-2Y Yield Spread & Inversion Detection 📅

The dashboard calculates and visualizes the 10-year minus 2-year yield spread, a key indicator for potential recessions.

A color-coded signal warns if the curve is inverted (negative spread).

6️⃣ Scenario Analysis (What-If Tool) 📏

Users can manually adjust Treasury yields and credit spreads to simulate different market conditions.

Allows for "what-if" analyses, such as rate hikes, economic downturns, or credit risk spikes.

💪 Installation & Setup

🔹 Prerequisites

Ensure you have Python 3.x installed along with the following dependencies:

pip install numpy pandas matplotlib plotly scipy fredapi dash

🔹 Clone the Repository

git clone https://github.com/yourusername/your-repository-name.git
cd your-repository-name

🔹 Set Up FRED API Key

Get an API key from FRED.

Replace YOUR_API_KEY in the script with your actual key.

🔹 Run the Application

python app.py

Open your browser and go to http://127.0.0.1:8050 to access the dashboard.

🔍 Usage

Once the dashboard is running, you can:

View the latest yield curves and their fitted models.

Compare corporate bond yields against risk-free Treasury yields.

Analyze credit spreads across different maturities.

Detect yield curve inversion using the 10Y-2Y spread analysis.

Use scenario analysis sliders to model economic changes and stress-test bond markets.

🌟 Contributing

Contributions are welcome! Feel free to open issues or submit pull requests if you have improvements, bug fixes, or additional features in mind.

⚖️ License

This project is licensed under the MIT License - see the LICENSE file for details.

