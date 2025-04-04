import streamlit as st
import pickle
import pandas as pd
import numpy as np
import os

# Load model & encoders
with open('ensemble_model.pkl', 'rb') as ensemble:
    model = pickle.load(ensemble)
with open('dummy_columns.pkl', 'rb') as col:
    dummy = pickle.load(col)
with open('label_encoders.pkl', 'rb') as encod:
    encoders = pickle.load(encod)
with open('scaler.pkl', 'rb') as scala:
    scaler = pickle.load(scala)

st.title("🌍 Carbon Footprint Calculator")

tab = st.radio("Navigation", ["👤 Personal", "🚗 Travel", "🗑 Waste", "⚡ Energy", "💊 Consumption"], horizontal=True)

if tab == "👤 Personal":
    st.session_state.height = st.number_input("Height (cm)", 100, 250, 160)
    st.session_state.weight = st.number_input("Weight (kg)", 20, 300, 75)
    st.session_state.sex = st.selectbox("Sex", ["male", "female"])
    st.session_state.social_activity = st.selectbox("Social Activity", ["never", "sometimes", "often"])
    st.session_state.diet = st.selectbox("Diet", ["omnivore", "vegetarian", "pescatarian", "vegan"])

elif tab == "🚗 Travel":
    st.session_state.vehicle_type = st.selectbox("Vehicle Type", ["diesel", "walk/bicycle/publicvehicle", "petrol", "hybrid", "electric", "lpg"])
    st.session_state.transport = st.selectbox("Transportation", ["private", "public", "walk/bicycle"])
    st.session_state.vehicle_monthly_distance_km = st.slider("Monthly vehicle distance (Km)", 0, 9999, 0)
    st.session_state.air_travel_frequency = st.selectbox("Air travel frequency", ["never", "rarely", "frequently", "very frequently"])

elif tab == "🗑 Waste":
    st.session_state.waste_bag_size = st.selectbox("Waste bag size", ["small", "medium", "large", "extra large"])
    st.session_state.waste_bag_weekly_count = st.number_input("Weekly waste bag count", 1, 7, 1)
    st.session_state.recycling = st.multiselect("Recycling materials", ['Metal', 'Paper', 'Plastic', 'Glass', 'Electronics'])

elif tab == "⚡ Energy":
    st.session_state.heating_energy_source = st.selectbox("Heating power source", ["coal", "natural gas", "electricity", "wood"])
    st.session_state.cooking_with = st.multiselect("Cooking methods", ['Grill', 'Airfryer', 'Stove', 'Oven', 'Microwave'])
    st.session_state.energy_efficiency = st.selectbox("Energy-efficient devices?", ["Yes", "No"])
    st.session_state.tv_pc_daily_hours = st.slider("Daily PC/TV usage (hours)", 0, 24, 0)
    st.session_state.internet_daily_hours = st.slider("Daily internet usage (hours)", 0, 24, 0)

elif tab == "💊 Consumption":
    st.session_state.shower_frequency = st.selectbox("Shower frequency", ["daily", "twice a day", "less frequently", "more frequently"])
    st.session_state.monthly_grocery_bill = st.slider("Monthly grocery bill ($)", 50, 299, 50)
    st.session_state.new_clothes_monthly = st.slider("New clothes bought monthly", 0, 50, 0)

    if st.button("Calculate Carbon Footprint"):
        height = st.session_state.get("height", 160)
        weight = st.session_state.get("weight", 75)
        bmi = weight / ((height / 100) ** 2)

        body_type = (
            "underweight" if bmi < 18.5 else
            "normal" if bmi <= 24.9 else
            "overweight" if bmi <= 29.9 else
            "obese"
        )

        df = pd.DataFrame([{
            "Body_Type": body_type,
            "Sex": st.session_state.sex,
            "Diet": st.session_state.diet,
            "Shower_Frequency": st.session_state.shower_frequency,
            "Heating_Energy_Source": st.session_state.heating_energy_source,
            "Transport": st.session_state.transport,
            "Vehicle_Type": st.session_state.vehicle_type,
            "Social_Activity": st.session_state.social_activity,
            "Monthly_Grocery_Bill": st.session_state.monthly_grocery_bill,
            "Air_Travel_Frequency": st.session_state.air_travel_frequency,
            "Vehicle_Monthly_Distance_Km": st.session_state.vehicle_monthly_distance_km,
            "Waste_Bag_Size": st.session_state.waste_bag_size,
            "Waste_Bag_Weekly_Count": st.session_state.waste_bag_weekly_count,
            "TV_PC_Daily_Hours": st.session_state.tv_pc_daily_hours,
            "New_Clothes_Monthly": st.session_state.new_clothes_monthly,
            "Internet_Daily_Hours": st.session_state.internet_daily_hours,
            "Recycling": st.session_state.recycling,
            "Energy_Efficiency": st.session_state.energy_efficiency,
            "Cooking_With": st.session_state.cooking_with
        }])

        for col in ['Body_Type', 'Shower_Frequency', 'Social_Activity', 'Air_Travel_Frequency', 'Waste_Bag_Size', 'Energy_Efficiency']:
            if col in encoders:
                df[col] = encoders[col].transform(df[col])

        df = pd.get_dummies(df, columns=["Sex", "Diet", "Heating_Energy_Source", "Transport", "Vehicle_Type"], drop_first=True)
        for col in dummy:
            if col not in df.columns:
                df[col] = 0
        df = df[dummy]

        X_scaled = scaler.transform(df)
        pred = model.predict(X_scaled)

        st.success(f"Estimated Carbon Footprint: {pred[0]:.2f} kg CO₂e per month")
