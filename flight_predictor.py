import streamlit as st
import pandas as pd
import joblib
from datetime import date # Add this at the top with your imports

# 1. Load the "Saved Brain" and the "Map"
model = joblib.load('flight_price_model.pkl')
model_columns = joblib.load('model_columns.pkl')
scaler = joblib.load('scaler.pkl')

st.title("✈️ Flight Fare Prediction App")
st.markdown("Enter the flight details below to get an estimated price.")

# 2. Create the User Interface (Input fields)
col1, col2 = st.columns(2)

with col1:
    airline = st.selectbox("Airline", ['Air_India', 'Indigo', 'Vistara', 'SpiceJet', 'AirAsia', 'GO_FIRST'])
    source = st.selectbox("Source City", ['Delhi', 'Mumbai', 'Bangalore', 'Kolkata', 'Hyderabad', 'Chennai'])
    destination = st.selectbox("Destination City", ['Mumbai', 'Delhi', 'Bangalore', 'Kolkata', 'Hyderabad', 'Chennai'])
    stops = st.selectbox("Stops", ['non-stop', '1-stop', '2+-stop'])
    dep_time = st.selectbox("Departure Time", ['Before 6 AM', '6 AM - 12 PM', '12 PM - 6 PM', 'After 6 PM'])
    arr_time = st.selectbox("Arrival Time", ['Before 6 AM', '6 AM - 12 PM', '12 PM - 6 PM', 'After 6 PM'])


with col2:
    travel_class = st.selectbox("Class", ['Economy', 'Premium Economy', 'Business', 'First'])
    duration = st.number_input("Duration (Hours)", min_value=0.5, max_value=50.0, value=2.5)
    travel_date = st.date_input("Select Date of Journey", min_value=date.today())
    
    
   # AUTOMATIC CALCULATIONS
    today = date.today()
    days_left = (travel_date - today).days
    day = travel_date.day
    month = travel_date.month

    # Add this where you calculate days_left
day_of_week = travel_date.weekday() # 0 is Monday, 5 is Saturday, 6 is Sunday
is_weekend = 1 if day_of_week >= 5 else 0

# Then, make sure your model_columns actually includes a 'is_weekend' 
# or 'day_of_week' feature if you trained with one.

st.info(f"Calculated Days Left: {days_left}")


# 3. The Prediction Logic (Your code goes here)
if st.button("Predict Flight Price"):
    # Create the dictionary from user inputs
    new_flight = {
    'Airline': airline,
    'Source': source,
    'Destination': destination,
    'Total_stops': stops,
    'Class': travel_class,
    'Duration_in_hours': duration,
    'Days_left': days_left,
    'Journey_day': day,
    'Journey_month': month,
    'Departure_Time': dep_value, 
    'Arrival_Time': arr_value    
}
    
    # Process inputs
    input_df = pd.DataFrame([new_flight])
    
    # Apply mappings
    stops_map = {'non-stop': 0, '1-stop': 1, '2+-stop': 2}
    class_map = {'Economy': 0, 'Premium Economy': 1, 'Business': 2, 'First':3}
    input_df['Total_stops'] = input_df['Total_stops'].map(stops_map)
    input_df['Class'] = input_df['Class'].map(class_map)
    time_map = {
    'Before 6 AM': 1,
    '6 AM - 12 PM': 2,
    '12 PM - 6 PM': 3,
    'After 6 PM': 4
}

# Convert the text selection to the number your model expects
dep_value = time_map[dep_time]
arr_value = time_map[arr_time]
    
    # Encode and Align
input_encoded = pd.get_dummies(input_df)
input_final = input_encoded.reindex(columns=model_columns, fill_value=0)

input_scaled = scaler.transform(input_final)
    
    # Predict
price = model.predict(input_scaled)
    
    # Show result
    #st.success(f"The predicted fare is: ₹{price:,.2f}")
final_number= float(price[0][0])
st.success(f"The predicted fare is: ₹{final_number:,.2f}")
