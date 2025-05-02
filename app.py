import streamlit as st
import pandas as pd
import numpy as np
import joblib
import random

# Load the trained model
xgb_model = joblib.load('combined_xgb_model.pkl')  # Ensure this path is correct

# Load data for input options
appliance_df = pd.read_csv('10000_balanced_household_dataset.csv')
emission_df = pd.read_csv('updated_REM_dataset_with_thresholds (1).csv')

# Define options from the dataset
categories = appliance_df['Category'].unique().tolist()
category_to_appliance_types = appliance_df.groupby('Category')['Appliance Type'].unique().to_dict()
energy_efficiency_ratings = appliance_df['Energy Efficiency Rating'].unique().tolist()
districts = emission_df['District Name'].unique().tolist()
district_to_sub_districts = emission_df.groupby('District Name')['Sub-District'].unique().to_dict()

st.title("Household Carbon Emission Calculator")

# User input for Household ID and location
household_id = st.text_input("Enter Household ID:")

# District and Sub-District selection
district_name = st.selectbox("Select District Name:", districts)
sub_districts = district_to_sub_districts[district_name].tolist()
sub_district_name = st.selectbox("Select Sub-District:", sub_districts)

# Input for number of appliances
num_appliances = st.number_input("Enter the number of appliances:", min_value=1, step=1)

# Initialize a list to store appliance data
appliance_data_list = []

# Gather input for each appliance
for i in range(num_appliances):
    st.write(f"### Appliance {i + 1}")

    # Get appliance details from the user
    category = st.selectbox(f"Select Category for Appliance {i + 1}:", categories, key=f'category_{i}')
    appliance_types = category_to_appliance_types[category].tolist()
    appliance_type = st.selectbox(f"Select Appliance Type for {category}:", appliance_types, key=f'appliance_{i}')
    specifications = appliance_df[(appliance_df['Category'] == category) & (appliance_df['Appliance Type'] == appliance_type)]['Specifications / Types'].unique().tolist()
    specification = st.selectbox(f"Select Specification/Type for {appliance_type}:", specifications, key=f'spec_{i}')
    efficiency_rating = st.selectbox(f"Select Energy Efficiency Rating:", energy_efficiency_ratings, key=f'efficiency_{i}')
    capacity = st.number_input(f"Enter Capacity for {appliance_type} (Litres/Kg/Inches):", min_value=0.0, step=0.1, key=f'capacity_{i}')
    energy_consumption = st.number_input(f"Enter Energy Consumption for {appliance_type} (kWh):", min_value=0.0, step=0.1, key=f'consumption_{i}')
    usage_hours = st.number_input(f"Enter Monthly Usage Hours for {appliance_type}:", min_value=0, step=1, key=f'usage_{i}')

    # Calculate emission per appliance and add to the list
    carbon_emission_per_month = energy_consumption * usage_hours * 0.00075284
    appliance_data_list.append({
        'Household_ID': household_id,
        'District Name': district_name,
        'Sub-District': sub_district_name,
        'Category': category,
        'Appliance Type': appliance_type,
        'Energy Efficiency Rating': efficiency_rating,
        'Capacity (Litres/Kg/Inches)': capacity,
        'Energy Consumption (kWh)': energy_consumption,
        'Monthly Usage Hours': usage_hours,
        'Carbon Emission per Month': carbon_emission_per_month
    })

# Process appliance data for prediction
if st.button("Calculate Total Emission and Classify"):
    # Convert list of appliances to DataFrame
    appliance_df = pd.DataFrame(appliance_data_list)

    # Drop non-numeric columns (like Household_ID, District Name, Sub-District)
    appliance_df = appliance_df.drop(['Household_ID', 'District Name', 'Sub-District'], axis=1)

    # One-Hot Encode Category, Appliance Type, and Energy Efficiency Rating (same as training)
    appliance_df = pd.get_dummies(appliance_df, columns=['Category', 'Appliance Type', 'Energy Efficiency Rating'], drop_first=True)

    # Ensure the input data has the same number of features as the training data
    expected_columns = xgb_model.get_booster().feature_names  # Get feature names from the model
    appliance_df = appliance_df.reindex(columns=expected_columns, fill_value=0)

    # Now you can make predictions
    predictions = xgb_model.predict(appliance_df)

    # Map predictions to labels
    emission_mapping = {0: 'low', 1: 'moderate', 2: 'high'}
    emission_category = emission_mapping[predictions[0]]  # Assuming one prediction

    # Display results
    st.write(f"### Total Carbon Emission: {sum(appliance_df['Carbon Emission per Month']):.2f} tons CO₂/month")
    st.write(f"### Emission Category: {emission_category}")

    # Provide recommendations
def get_recommendation(emission_category):
    # Define recommendations
    recommendations = {
        'low': [
            "Great! Your household has low emissions. Keep it up!",
            "Low emissions detected! You're doing an excellent job in minimizing your carbon footprint.",
            "Your emissions are low. Continue using energy-efficient appliances and maintaining low usage.",
            "You're ahead in the sustainability race with low emissions. Keep up the great work!",
            "Low carbon emissions! Consider installing smart home systems to optimize energy use even further."
        ],
        'moderate': [
            "Your emissions are moderate. Consider reducing appliance usage or opting for energy-efficient options.",
            "You're doing well, but you can still lower emissions by reducing appliance usage or switching to energy-efficient models.",
            "Moderate emissions detected. Consider upgrading to energy-efficient appliances to bring emissions down.",
            "Your household's emissions are moderate. Switching to eco-friendly appliances could help reduce the carbon footprint.",
            "Reduce the usage of appliances or look into renewable energy sources for better results."
        ],
        'high': [
            "Your emissions are high! Consider using energy-efficient appliances and reducing overall energy consumption.",
            "High emissions detected. Switching to LED lighting and reducing air conditioning use can help lower it.",
            "Your household has a high carbon footprint. Opt for renewable energy sources or upgrade to energy-efficient appliances.",
            "Try reducing unnecessary electricity usage, using smart home systems, and switching to sustainable power sources.",
            "High emissions recorded! Consider scheduling appliance usage to off-peak hours and adopting green energy alternatives."
        ]
    }

    # Select a random recommendation based on the emission category
    if emission_category in recommendations:
        selected_recommendation = random.choice(recommendations[emission_category])
    else:
        selected_recommendation = "Emission category not recognized."

    return emission_category, selected_recommendation

# Display result in Streamlit
st.write(f"### Recommendation: {recommendation}")
