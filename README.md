**Household Appliance Carbon Footprint Calculator – Tamil Nadu**

  This project is a machine learning–powered web application that estimates and classifies household carbon emissions based on appliance usage and **Regional Emission (REM)** factors for different districts in **Tamil Nadu**. The system also offers **personalized recommendations** to reduce your carbon footprint, using statistical models and XGBoost regression.

**🌱 Project Overview**

1. **Goal:** To calculate and categorize the carbon footprint of household appliances based on REM factors.
2. **Region:** Focused on Tamil Nadu, India.
3. **Tech Stack:** Python, Streamlit, XGBoost, Pandas, NumPy, Joblib.
4. **Users:** Households, researchers, and environmental policymakers seeking emission insights and optimization suggestions.

**🔍 Features**

**Dynamic form for entering appliance details like:**
1. Type, capacity, energy consumption, and usage hours.
2. Location-based REM factor (district & sub-district of Tamil Nadu).
3. Calculates **monthly CO₂ emissions** (in tons).
4. Classifies emissions into: `Low`, `Moderate`, or `High`.
5. Displays **tailored recommendations** to reduce emissions.
6. Machine learning model: **XGBoost Regression** trained on synthetic appliance datasets and REM factors.

**🚀 How to Run the App Locally**

**1. Prerequisites:**
  1.1. Python 3.8+
  1.2. Required packages: `streamlit`, `pandas`, `numpy`, `joblib`

**2. Installation:**

'''bash
git clone https://github.com/yourusername/household-appliance-carbon-footprint-calculator-tamilnadu.git
cd household-appliance-carbon-footprint-calculator-tamilnadu
pip install -r requirements.txt
'''

**3. Start the App:**

```bash
streamlit run app.py
```

**4. Ensure the following files are in the root directory:**

 `app.py`
 `combined_xgb_model.pkl`
 `synthetic_household_appliances_data.csv`
  `REM_Factor.csv`

**🧠 Machine Learning**

1. Algorithm: XGBoost Regression, Multilayer Percepton
2. Inputs: Appliance type, energy rating, usage hours, capacity, and REM factors
3. Outputs: CO₂ emissions per appliance and classification (low/moderate/high)
4. Emission formula (per appliance):

  ```
  Emission = Energy_Consumption (kWh) × Monthly_Usage_Hours × 0.00075284
  ```

**📊 Sample Input Fields**

* **Appliance Type**: e.g., Air Conditioner, Washing Machine
* **Efficiency Rating**: 1,2,...5
* **Energy Consumption**: e.g., 1.5 kWh
* **Usage Hours**: e.g., 100 hours/month
* **Location**: Select district and sub-district

**📁 Project Structure**

```
.
├── app.py                          # Streamlit web app
├── combined_xgb_model.pkl         # Trained ML model
├── 10000_balanced_household_dataset.csv  # Appliance data
├── updated_REM_dataset_with_thresholds (1) # Regional emission data
├── requirements.txt               # Python dependencies
└── README.md                      # Project description
```




