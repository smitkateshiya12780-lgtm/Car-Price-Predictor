import streamlit as st
import joblib
import pandas as pd
from datetime import datetime

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Car Price Predictor",
    page_icon="🚗",
    layout="centered"
)

# ---------------- CUSTOM CSS ----------------
st.markdown("""
    <style>
        .main {
            background-color: #f7f9fc;
        }
        .title {
            text-align: center;
            font-size: 42px;
            font-weight: 700;
            color: #1f2937;
            margin-bottom: 5px;
        }
        .subtitle {
            text-align: center;
            font-size: 18px;
            color: #6b7280;
            margin-bottom: 30px;
        }
        .card {
            background: white;
            padding: 25px;
            border-radius: 18px;
            box-shadow: 0 4px 18px rgba(0,0,0,0.08);
            margin-bottom: 20px;
        }
        .result-box {
            background: linear-gradient(135deg, #16a34a, #22c55e);
            color: white;
            padding: 20px;
            border-radius: 16px;
            text-align: center;
            font-size: 24px;
            font-weight: bold;
            margin-top: 20px;
        }
    </style>
""", unsafe_allow_html=True)

# ---------------- LOAD MODEL ----------------
model = joblib.load("car_price_model.pkl")

# ---------------- HEADER ----------------
st.markdown('<div class="title">🚗 Car Price Predictor</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Estimate the resale value of your car in seconds</div>', unsafe_allow_html=True)

# ---------------- FORM CARD ----------------
st.markdown('<div class="card">', unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    car_name = st.selectbox("Car Name", ["ritz", "sx4", "ciaz", "wagon r", "swift", "i10"])
    present_price = st.number_input("Present Price (in Lakhs)", min_value=0.0, format="%.2f")
    driven_kms = st.number_input("Driven Kilometers", min_value=0, step=500)

with col2:
    fuel_type = st.selectbox("Fuel Type", ["Petrol", "Diesel", "CNG"])
    selling_type = st.selectbox("Selling Type", ["Dealer", "Individual"])
    transmission = st.selectbox("Transmission", ["Manual", "Automatic"])

owner = st.selectbox("Number of Previous Owners", [0, 1, 2, 3])
car_year = st.number_input(
    "Car Purchase Year",
    min_value=2000,
    max_value=datetime.now().year,
    step=1
)

car_age = datetime.now().year - car_year

predict_btn = st.button("Predict Price")

st.markdown('</div>', unsafe_allow_html=True)

# ---------------- PREDICTION ----------------
if predict_btn:
    try:
        input_data = pd.DataFrame([{
            "Car_Name": car_name,
            "Present_Price": present_price,
            "Driven_kms": driven_kms,
            "Fuel_Type": fuel_type,
            "Selling_type": selling_type,
            "Transmission": transmission,
            "Owner": owner,
            "Car_Age": car_age
        }])

        prediction = model.predict(input_data)

        st.markdown(
            f'<div class="result-box">Estimated Selling Price: ₹ {prediction[0]:.2f} Lakhs</div>',
            unsafe_allow_html=True
        )

    except Exception as e:
        st.error(f"Error during prediction: {e}")