import streamlit as st
import pickle
import pandas as pd
import numpy as np
import ast
import base64

# --- Check if reset button was clicked (place at the top) ---
if 'reset_clicked' in st.session_state and st.session_state.reset_clicked:
    # Reset all inputs to default values
    st.session_state.height = 170
    st.session_state.weight = 70
    st.session_state.sex = "Please select"
    st.session_state.social_activity = "Please select"
    st.session_state.diet = "Please select"
    st.session_state.transport = "Please select"
    st.session_state.vehicle_monthly_distance_km = 0
    st.session_state.air_travel_frequency = "Please select"
    st.session_state.waste_bag_size = "Please select"
    st.session_state.waste_bag_weekly_count = 1
    st.session_state.recycling = []
    st.session_state.heating_energy_source = "Please select"
    st.session_state.cooking_with = []
    st.session_state.energy_efficiency = "Please select"
    st.session_state.tv_pc_daily_hours = 0
    st.session_state.internet_daily_hours = 0
    st.session_state.shower_frequency = "Please select"
    st.session_state.monthly_grocery_bill = 50
    st.session_state.new_clothes_monthly = 0
    st.session_state.prediction = None  # Also reset the prediction
    st.session_state.input_data = None  # Also reset the input data
    
    # Reset the flag
    st.session_state.reset_clicked = False
    
    st.success("All inputs have been reset to default values!")

# --- Load models ---
try:
    with open('models/ensemble_model.pkl', 'rb') as ensemble:
        model = pickle.load(ensemble)

    with open('models/dummy_info.pkl', 'rb') as dummy:
        dummy_info = pickle.load(dummy)

    with open('models/preprocessor.pkl', 'rb') as process:
        preprocessor = pickle.load(process)

    with open('models/feature_order.pkl', 'rb') as order:
        feature_order = pickle.load(order)

except FileNotFoundError as e:
    st.error(f"Error loading model files: {str(e)}")
    st.stop()
except Exception as e:
    st.error(f"An unexpected error occurred: {str(e)}")
    st.stop()

# Function to get base64 string of the image
def get_base64(file_path):
    with open(file_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Background image
img_path = "Images/background_min.jpg"
img_base64 = get_base64(img_path)

# Inject CSS
page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] {{
    background-image: url("data:image/png;base64,{img_base64}");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
}}

.container {{
    background-color: rgba(255, 255, 255, 0.85);
    padding: 3rem;
    border-radius: 20px;
    margin: auto;
    max-width: 900px;
    font-family: 'Arial', sans-serif;
    color: #333;
}}

[data-testid="stSidebar"] {{
    background-color: black;
    color: #333;
}}
</style>
"""
st.markdown(page_bg_img, unsafe_allow_html=True)

# Main content
st.markdown('<div class="container">', unsafe_allow_html=True)

# --- App title ---
st.title("🌍 Carbon Footprint Tracker")

# --- Initialize Session State for all fields if not present ---
if 'initialized' not in st.session_state:
    st.session_state.initialized = True
    
    # Default values for all fields
    st.session_state.height = 170
    st.session_state.weight = 70
    st.session_state.sex = "Please select"
    st.session_state.social_activity = "Please select"
    st.session_state.diet = "Please select"
    st.session_state.transport = "Please select"
    st.session_state.vehicle_monthly_distance_km = 0
    st.session_state.air_travel_frequency = "Please select"
    st.session_state.waste_bag_size = "Please select"
    st.session_state.waste_bag_weekly_count = 1
    st.session_state.recycling = []
    st.session_state.heating_energy_source = "Please select"
    st.session_state.cooking_with = []
    st.session_state.energy_efficiency = "Please select"
    st.session_state.tv_pc_daily_hours = 0
    st.session_state.internet_daily_hours = 0
    st.session_state.shower_frequency = "Please select"
    st.session_state.monthly_grocery_bill = 50
    st.session_state.new_clothes_monthly = 0
    st.session_state.prediction = None
    st.session_state.input_data = None

# --- Tabs ---
tabs = ["👤 Personal", "🚗 Travel", "🗑 Waste", "⚡ Energy", "💊 Consumption"]
tab = st.radio("Navigator", tabs, horizontal=True)

# --- Callback functions for each input ---
def update_height():
    st.session_state.height = st.session_state.height_input
    
def update_weight():
    st.session_state.weight = st.session_state.weight_input
    
def update_sex():
    st.session_state.sex = st.session_state.sex_input
    
def update_social():
    st.session_state.social_activity = st.session_state.social_input
    
def update_diet():
    st.session_state.diet = st.session_state.diet_input

def update_transport():
    st.session_state.transport = st.session_state.transport_input
    
def update_vehicle_distance():
    st.session_state.vehicle_monthly_distance_km = st.session_state.vehicle_distance_input
    
def update_air_travel():
    st.session_state.air_travel_frequency = st.session_state.air_travel_input

def update_recycling():
    st.session_state.recycling = st.session_state.recycling_input
    
def update_waste_size():
    st.session_state.waste_bag_size = st.session_state.waste_size_input
    
def update_waste_count():
    st.session_state.waste_bag_weekly_count = st.session_state.waste_count_input

def update_heating():
    st.session_state.heating_energy_source = st.session_state.heating_input
    
def update_cooking():
    st.session_state.cooking_with = st.session_state.cooking_input
    
def update_energy_efficiency():
    st.session_state.energy_efficiency = st.session_state.energy_efficiency_input
    
def update_tv_pc():
    st.session_state.tv_pc_daily_hours = st.session_state.tv_pc_input
    
def update_internet():
    st.session_state.internet_daily_hours = st.session_state.internet_input

def update_shower():
    st.session_state.shower_frequency = st.session_state.shower_input
    
def update_grocery():
    st.session_state.monthly_grocery_bill = st.session_state.grocery_input
    
def update_clothes():
    st.session_state.new_clothes_monthly = st.session_state.clothes_input

# --- Handle reset button click ---
def handle_reset():
    st.session_state.reset_clicked = True
    st.rerun()

# --- Inputs with callbacks ---
if tab == "👤 Personal":
    st.number_input(
        "Height (cm)", 100, 250, 
        value=st.session_state.height,
        key="height_input", 
        on_change=update_height
    )
    
    st.number_input(
        "Weight (kg)", 20, 300, 
        value=st.session_state.weight,
        key="weight_input", 
        on_change=update_weight
    )
    
    st.selectbox(
        "Sex", ["Please select", "Male", "Female"],
        index=["Please select", "Male", "Female"].index(st.session_state.sex),
        key="sex_input",
        on_change=update_sex
    )
    
    st.selectbox(
        "Social Activity", ["Please select", "never", "sometimes", "often"],
        index=["Please select", "never", "sometimes", "often"].index(st.session_state.social_activity),
        key="social_input",
        on_change=update_social
    )
    
    st.selectbox(
        "Diet", ["Please select", "omnivore", "vegetarian", "pescatarian", "vegan"],
        index=["Please select", "omnivore", "vegetarian", "pescatarian", "vegan"].index(st.session_state.diet),
        key="diet_input",
        on_change=update_diet
    )

elif tab == "🚗 Travel":
    st.selectbox(
        "Transportation", ["Please select", "private", "public", "walk/bicycle"],
        index=["Please select", "private", "public", "walk/bicycle"].index(st.session_state.transport),
        key="transport_input",
        on_change=update_transport
    )
    
    st.slider(
        "Monthly vehicle distance (Km)", 0, 5000,
        value=st.session_state.vehicle_monthly_distance_km,
        key="vehicle_distance_input",
        on_change=update_vehicle_distance
    )
    
    st.selectbox(
        "Air travel frequency", ["Please select", "never", "rarely", "frequently", "very frequently"],
        index=["Please select", "never", "rarely", "frequently", "very frequently"].index(st.session_state.air_travel_frequency),
        key="air_travel_input",
        on_change=update_air_travel
    )

elif tab == "🗑 Waste":
    st.multiselect(
        "Recycling materials",
        ['Metal', 'Paper', 'Plastic', 'Glass', 'Electronics'],
        default=st.session_state.recycling,
        key="recycling_input",
        on_change=update_recycling
    )

    st.selectbox(
        "Waste bag size", ["Please select", "small", "medium", "large", "extra large"],
        index=["Please select", "small", "medium", "large", "extra large"].index(st.session_state.waste_bag_size),
        key="waste_size_input",
        on_change=update_waste_size
    )
    
    st.number_input(
        "Weekly waste bag count", 1, 7,
        value=st.session_state.waste_bag_weekly_count,
        key="waste_count_input",
        on_change=update_waste_count
    )

elif tab == "⚡ Energy":
    st.selectbox(
        "Heating power source", ["Please select", "coal", "natural gas", "electricity", "wood"],
        index=["Please select", "coal", "natural gas", "electricity", "wood"].index(st.session_state.heating_energy_source),
        key="heating_input",
        on_change=update_heating
    )
    
    st.multiselect(
        "Cooking methods",
        ['Grill', 'Airfryer', 'Stove', 'Oven', 'Microwave'],
        default=st.session_state.cooking_with,
        key="cooking_input",
        on_change=update_cooking
    )
    
    st.selectbox(
        "Energy-efficient devices?", ["Please select", "Yes", "No"],
        index=["Please select", "Yes", "No"].index(st.session_state.energy_efficiency),
        key="energy_efficiency_input",
        on_change=update_energy_efficiency
    )
    
    st.slider(
        "Daily PC/TV usage (hours)", 0, 16,
        value=st.session_state.tv_pc_daily_hours,
        key="tv_pc_input",
        on_change=update_tv_pc
    )
    
    st.slider(
        "Daily internet usage (hours)", 0, 16,
        value=st.session_state.internet_daily_hours,
        key="internet_input",
        on_change=update_internet
    )

elif tab == "💊 Consumption":
    st.selectbox(
        "Shower frequency", ["Please select", "daily", "twice a day", "less frequently", "more frequently"],
        index=["Please select", "daily", "twice a day", "less frequently", "more frequently"].index(st.session_state.shower_frequency),
        key="shower_input",
        on_change=update_shower
    )
    
    st.slider(
        "Monthly grocery bill ($)", 50, 299,
        value=st.session_state.monthly_grocery_bill,
        key="grocery_input",
        on_change=update_grocery
    )
    
    st.slider(
        "New clothes bought monthly", 0, 25,
        value=st.session_state.new_clothes_monthly,
        key="clothes_input",
        on_change=update_clothes
    )

    if st.button("Track Your Carbon Footprint"):
        try:
            height = st.session_state.height
            weight = st.session_state.weight
            dropdowns = [
                st.session_state.sex, st.session_state.social_activity, st.session_state.diet,
                st.session_state.transport, st.session_state.air_travel_frequency,
                st.session_state.waste_bag_size, st.session_state.heating_energy_source,
                st.session_state.energy_efficiency, st.session_state.shower_frequency
            ]

            if not height or not weight:
                st.warning("Please enter both height and weight.")
            elif "Please select" in dropdowns:
                st.warning("Please fill all required dropdowns.")
            else:
                # --- Calculate Body Type ---
                bmi = weight / ((height / 100) ** 2)
                body_type = "underweight" if bmi < 18.5 else "normal" if bmi <= 24.9 else "overweight" if bmi <= 29.9 else "obese"

                # --- Prepare Data ---
                input_data = {
                    "body_type": body_type,
                    "gender": st.session_state.sex,
                    "diet": st.session_state.diet,
                    "shower_frequency": st.session_state.shower_frequency,
                    "heating_energy_source": st.session_state.heating_energy_source,
                    "transport": st.session_state.transport,
                    "social_activity": st.session_state.social_activity,
                    "monthly_grocery_bill": st.session_state.monthly_grocery_bill,
                    "air_travel_frequency": st.session_state.air_travel_frequency,
                    "vehicle_monthly_distance_km": st.session_state.vehicle_monthly_distance_km,
                    "waste_bag_size": st.session_state.waste_bag_size,
                    "waste_bag_weekly_count": st.session_state.waste_bag_weekly_count,
                    "tv_pc_daily_hours": st.session_state.tv_pc_daily_hours,
                    "new_clothes_monthly": st.session_state.new_clothes_monthly,
                    "internet_daily_hours": st.session_state.internet_daily_hours,
                    "recycling": str(st.session_state.recycling),
                    "energy_efficiency": st.session_state.energy_efficiency,
                    "cooking_with": str(st.session_state.cooking_with)
                }

                df = pd.DataFrame([input_data])

                def transform_multilabel(df, column_name, categories):
                    df = df.copy()
                    def parse(x):
                        if isinstance(x, list) or isinstance(x, np.ndarray):
                            return x
                        if isinstance(x, str):
                            return ast.literal_eval(x)
                        if pd.isnull(x):
                            return []
                        return []
                    for value in categories:
                        df[value] = df[column_name].apply(lambda x: int(value in parse(x)))
                    df.drop(columns=column_name, inplace=True)
                    return df

                df = transform_multilabel(df, 'recycling', dummy_info['recycling'])
                df = transform_multilabel(df, 'cooking_with', dummy_info['cooking_with'])

                ordinal_cols = ['body_type', 'shower_frequency', 'social_activity', 'air_travel_frequency', 'waste_bag_size', 'energy_efficiency']
                onehot_cols = ['gender', 'diet', 'heating_energy_source', 'transport']

                def transform_input(df_raw):
                    df = df_raw.copy()
                    X_transformed = preprocessor.transform(df)
                    ohe_feature_names = preprocessor.named_transformers_['onehot'].get_feature_names_out(onehot_cols)
                    all_feature_names = ordinal_cols + list(ohe_feature_names) + [col for col in df.columns if col not in ordinal_cols + onehot_cols]
                    X_df = pd.DataFrame(X_transformed, columns=all_feature_names)
                    X_df.reset_index(drop=True, inplace=True)
                    return X_df

                transformed_input = transform_input(df)
                transformed_input = transformed_input.reindex(columns=feature_order, fill_value=0)

                prediction = model.predict(transformed_input)
                st.success(f"🌱 Your estimated carbon footprint is: **{prediction[0]:.2f} units**")

                # Save prediction
                st.session_state.prediction = prediction[0]
                st.session_state.input_data = input_data
                
                # Don't reset inputs after prediction to allow user to review and modify
                st.info("You can review and modify your inputs if needed. Your data has been saved.")

        except Exception as e:
            st.error(f"An error occurred during Tracking: {str(e)}")
            import traceback
            st.error(traceback.format_exc())

# Add a button to reset all inputs using the new handler
st.button("Reset All Inputs", on_click=handle_reset)

# Add dashboard view button if a prediction exists


st.markdown('</div>', unsafe_allow_html=True)