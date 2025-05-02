import streamlit as st
import pandas as pd
import numpy as np
import joblib
import random

# Load the trained model
xgb_model = joblib.load('combined_xgb_model.pkl')  # Ensure this path is correct

# Load data for input options
appliance_df = pd.read_csv('synthetic_household_appliances_data.csv')
emission_df = pd.read_csv('REM_Factor.csv')

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

# Function to classify based on number of appliances
def classify_by_appliances(num_appliances):
    if num_appliances >= 10:
        return 'high', [
            "High emissions detected! Consider reducing the number of appliances, switching to energy-efficient models, or optimizing usage.",
            "Your household has a high carbon footprint. Try using fewer appliances or choosing more energy-efficient options.",
            "High emissions detected! Consider smart home systems to optimize usage and energy consumption.",
            "You have a lot of appliances. Try reducing usage or opting for better energy ratings to lower emissions.",
            "Your emission levels are high. Think about upgrading to eco-friendly, energy-efficient appliances."
        ]
    elif num_appliances >= 5:
        return 'moderate', [
            "Your emissions are moderate. Consider reducing appliance usage or opting for energy-efficient options.",
            "You're doing well, but you can still lower emissions by reducing appliance usage or switching to energy-efficient models.",
            "Moderate emissions detected. Consider upgrading to energy-efficient appliances to bring emissions down.",
            "Your household's emissions are moderate. Switching to eco-friendly appliances could help reduce the carbon footprint.",
            "Reduce the usage of appliances or look into renewable energy sources for better results."
        ]
    else:
        return 'low', [
            "Great! Your household has low emissions. Keep it up!",
            "Low emissions detected! You're doing an excellent job in minimizing your carbon footprint.",
            "Your emissions are low. Continue using energy-efficient appliances and maintaining low usage.",
            "You're ahead in the sustainability race with low emissions. Keep up the great work!",
            "Low carbon emissions! Consider installing smart home systems to optimize energy use even further."
        ]

# Process appliance data for prediction when user clicks "Calculate Total Emission and Classify"
if st.button("Calculate Total Emission and Classify"):
    # Classify emission based on number of appliances
    emission_category, recommendation_list = classify_by_appliances(num_appliances)

    # Calculate total carbon emission for the household
    total_emission = sum([appliance['Carbon Emission per Month'] for appliance in appliance_data_list])

    # Select a random recommendation from the list based on the emission category
    random_recommendation = random.choice(recommendation_list)

    # Display the total emission and classification result
    st.write(f"### Total Carbon Emission: {total_emission:.2f} tons CO₂/month")
    st.write(f"### Emission Category: {emission_category}")

    # Provide the recommendation based on appliance classification
    st.write(f"### Recommendation: {random_recommendation}")

  
