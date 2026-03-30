import streamlit as st
import pandas as pd
import joblib

# 1. Load the "Saved Brain" and the "Map"
model = joblib.load('flight_price_model.pkl')
model_columns = joblib.load('model_columns.pkl')

st.title("✈️ Flight Fare Prediction App")
st.markdown("Enter the flight details below to get an estimated price.")

# 2. Create the User Interface (Input fields)
col1, col2 = st.columns(2)

with col1:
    airline = st.selectbox("Airline", ['Air_India', 'Indigo', 'Vistara', 'SpiceJet', 'AirAsia', 'GO_FIRST'])
    source = st.selectbox("Source City", ['Delhi', 'Mumbai', 'Bangalore', 'Kolkata', 'Hyderabad', 'Chennai'])
    destination = st.selectbox("Destination City", ['Mumbai', 'Delhi', 'Bangalore', 'Kolkata', 'Hyderabad', 'Chennai'])
    stops = st.selectbox("Stops", ['non-stop', '1-stop', '2+-stop'])

with col2:
    travel_class = st.selectbox("Class", ['Economy', 'Premium Economy', 'Business', 'First'])
    duration = st.number_input("Duration (Hours)", min_value=0.5, max_value=50.0, value=2.5)
    days_left = st.number_input("Days Left until Flight", min_value=1, max_value=50, value=10)
    day = st.slider("Day of Journey", 1, 31, 15)
    month = st.slider("Month of Journey", 1, 12, 5)

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
        'Journey_month': month
    }
    
    # Process inputs
    input_df = pd.DataFrame([new_flight])
    
    # Apply mappings
    stops_map = {'non-stop': 0, '1-stop': 1, '2+-stop': 2}
    class_map = {'Economy': 0, 'Premium Economy': 1, 'Business': 2, 'First':3}
    input_df['Total_stops'] = input_df['Total_stops'].map(stops_map)
    input_df['Class'] = input_df['Class'].map(class_map)
    
    # Encode and Align
    input_encoded = pd.get_dummies(input_df)
    input_final = input_encoded.reindex(columns=model_columns, fill_value=0)
    
    # Predict
    price = model.predict(input_final)
    
    # Show result
    #st.success(f"The predicted fare is: ₹{price:,.2f}")
    final_number= float(price[0][0])
    st.success(f"The predicted fare is: ₹{final_number:,.2f}")
