# 📈 Yield Curve Analysis Dashboard 💹  

This project is a **Yield Curve Analysis Dashboard** that provides an **interactive visualization of U.S. Treasury yields, corporate bond yields, and credit spreads**. The goal is to **help traders, analysts, and researchers analyze yield curve trends, detect inversions, and simulate economic scenarios.**  

---

## 🚀 **Project Overview**  

Fixed-income markets and interest rates play a crucial role in **macroeconomics, trading, and monetary policy**. This Python-based tool enables users to:  

✅ **Fetch real-time U.S. Treasury yield data** from the **FRED API**  
✅ **Simulate corporate bond yields** by applying **historical credit spreads**  
✅ **Fit yield curves using Spline and Nelson-Siegel models** for better visualization  
✅ **Analyze credit spreads** to compare risk-free and corporate bond yields  
✅ **Perform 10Y-2Y spread analysis** to detect **yield curve inversions**  
✅ **Use scenario analysis tools** to simulate yield shifts and credit spread widening  

---

## 🏗 **How It Works**  

### **1️⃣ Fetching Treasury Yields** 📊  
- The script pulls **U.S. Treasury yields** from FRED for maturities ranging from **3 months to 30 years**  
- Data is processed and structured for yield curve modeling  

### **2️⃣ Simulating Corporate Bond Yields** 💳  
- Corporate bond yields are estimated by adding a **maturity-dependent credit spread** to Treasury yields  
- Assumed credit spreads (historical averages):  
  - **2-Year Bonds:** +1.0%  
  - **5-Year Bonds:** +1.5%  
  - **10-Year Bonds:** +2.0%  
  - **20-Year Bonds:** +2.5%  
  - **30-Year Bonds:** +3.0%  

### **3️⃣ Yield Curve Fitting Methods** ⚖️  
- **Cubic Spline Fit:** A smooth, flexible model for interpolating Treasury yields  
- **Nelson-Siegel Model:** A parametric model capturing yield curve shape using **level, slope, and curvature factors**  

### **4️⃣ Credit Spread Analysis** 📉  
- Calculates the difference between **corporate bond yields** and **Treasury yields** at each maturity  
- Generates an interactive **credit spread curve** for better market analysis  

### **5️⃣ 10Y-2Y Yield Spread & Inversion Detection** 📅  
- Computes and visualizes the **10-year minus 2-year yield spread**, a key **recession indicator**  
- **Color-coded signal:** Alerts when the yield curve is **normal** (positive spread) or **inverted** (negative spread)  

### **6️⃣ Scenario Analysis (What-If Tool)** 📑  
- **Manually adjust Treasury yields and credit spreads** to simulate different market conditions  
- Conduct **"what-if" analysis**, including **rate hikes, economic downturns, or credit risk fluctuations**  

---

## 🔧 **Installation & Setup**  

### **📌 Prerequisites**  
Ensure you have **Python 3.x** installed along with the required dependencies:  

```bash
pip install numpy pandas matplotlib plotly scipy fredapi dash
