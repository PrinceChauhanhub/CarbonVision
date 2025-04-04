# CarbonVision 🌱

CarbonVision is an AI-powered Carbon Footprint Calculator built using Streamlit. It helps users estimate their monthly carbon emissions based on personal lifestyle choices across multiple categories like Travel, Waste, Energy, and Consumption.

## 🔍 Features

- Multi-tab navigation for different lifestyle sections:
  - 👤 Personal
  - 🚗 Travel
  - 🗑 Waste
  - ⚡ Energy
  - 💊 Consumption
- User inputs collected through clean and interactive UI
- Uses pre-trained machine learning model (ensemble_model.pkl) for prediction
- Dynamic BMI-based body type classification
- Scales and encodes inputs before prediction
- Displays the estimated carbon footprint in kg CO₂e/month

## 🚀 How to Run

1. Clone this repository:
   git clone https://github.com/PrinceChauhanhub/CarbonVision.git cd CarbonVision
2. Create a virtual environment:
   conda create -p venv python==3.11.11 -y
3. Install dependencies:
   pip install -r requirements.txt
4. Run the Streamlit app:
   streamlit run app.py

> Make sure all the required `.pkl` files are present in the root directory:
> - ensemble_model.pkl
> - dummy_columns.pkl
> - label_encoders.pkl
> - scaler.pkl

CarbonVision/ 
│ ├── app.py 
# Main Streamlit app ├── ensemble_model.pkl 
# Trained ensemble model ├── dummy_columns.pkl 
# Dummy column reference ├── label_encoders.pkl 
# Label encoders for categorical data ├── scaler.pkl 
# Feature scaler ├── requirements.txt 
# Required packages └── README.txt 
# Project documentation (this file)

## 🧠 Tech Stack

- Python 🐍
- Streamlit 🚀
- Scikit-learn 🤖
- Pandas & NumPy 🧮

## 🙌 Contribution

Feel free to fork this repository and contribute improvements or bug fixes! Pull requests are welcome.

Made with ❤️ by Prince Chauhan.
