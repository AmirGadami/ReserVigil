import streamlit as st
import joblib

# Load your model
model = joblib.load("artifact/models/lgbm_model_pkl")

st.title("🏨 Hotel Cancellation Predictor")

# Inputs
lead_time = st.number_input("Lead Time", 0)
special_requests = st.number_input("Special Requests", 0)
avg_price = st.number_input("Avg Price per Room", 0.0)
arrival_month = st.number_input("Arrival Month (1-12)", 1, 12)
arrival_date = st.number_input("Arrival Date (1-31)", 1, 31)
market_segment = st.selectbox("Market Segment", ["Aviation", "Complimentary", "Corporate", "Offline", "Online"])
week_nights = st.number_input("Week Nights", 0)
weekend_nights = st.number_input("Weekend Nights", 0)
meal_plan = st.selectbox("Meal Plan", ["Meal Plan 1", "Meal Plan 2", "Meal Plan 3", "Not Selected"])
room_type = st.selectbox("Room Type", ["Room Type 1", "Room Type 2", "Room Type 3", "Room Type 4", "Room Type 5", "Room Type 6", "Room Type 7"])

# Map categories to numbers
market_map = {"Aviation": 0, "Complimentary": 1, "Corporate": 2, "Offline": 3, "Online": 4}
meal_map = {"Meal Plan 1": 0, "Meal Plan 2": 1, "Meal Plan 3": 2, "Not Selected": 3}
room_map = {
    "Room Type 1": 0, "Room Type 2": 1, "Room Type 3": 2,
    "Room Type 4": 3, "Room Type 5": 4, "Room Type 6": 5, "Room Type 7": 6
}

# Predict button
if st.button("Predict"):
    X = [[
        lead_time,
        special_requests,
        avg_price,
        arrival_month,
        arrival_date,
        market_map[market_segment],
        week_nights,
        weekend_nights,
        meal_map[meal_plan],
        room_map[room_type]
    ]]
    
    pred = model.predict(X)[0]
    if pred == 0:
        st.error("❌ Likely to CANCEL the reservation.")
    else:
        st.success("✅ Likely to KEEP the reservation.")