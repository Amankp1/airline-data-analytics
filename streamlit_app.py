import streamlit as st
import pandas as pd
import requests
import os
import json
from process1 import process_price_history, load_and_clean_data, display_price_matrix, analyze_flight_statistics, create_price_comparison_chart
from api_integration import generate_gemini_insights, prepare_data_summary
import plotly.express as px
import atexit 
# register your cleanup function
def cleanup_files():
    files_to_delete = [
        "google_flights_data.json",
        "price_history_data.csv",
        "flight_price_matrix.csv"
    ]
    for file in files_to_delete:
        if os.path.exists(file):
            os.remove(file)

atexit.register(cleanup_files)

# Set the title of the app
st.title("Airlines Data")

# Create a dropdown menu for trip type selection
# trip_type = st.selectbox("Select Trip Type", ["Round Trip", "One Way"])
trip_type = "Round Trip"

def data_trends():
    st.header("Data Trends")
    try:
        if os.path.exists("price_history_data.csv"):
            PRICE_HISTORY_PATH = "price_history_data.csv"
            st.subheader(":chart_with_upwards_trend: Price History (Past 60 Days)")
            
            if not os.path.exists(PRICE_HISTORY_PATH):
                st.error("CSV file not found!")
                return

            df = pd.read_csv(PRICE_HISTORY_PATH)

            # If not already cleaned, clean it
            if 'aria-label' in df.columns:
                df = process_price_history(PRICE_HISTORY_PATH)
            else:
                df['Date'] = pd.to_datetime(df['Date'])

            df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
            df = df.dropna(subset=['Date'])
            df["Date"] = df["Date"].dt.strftime("%b %d")
            tick_labels = df["Date"].tolist()
            tickvals = [tick_labels[i] for i in range(0, len(tick_labels), 7)]
            fig = px.line(df, x="Date", y="Price", markers=True)
            fig.update_layout(
                xaxis_title="Date",
                yaxis_title="Price (A$)",
                margin=dict(l=40, r=20, t=40, b=40),
                height=400,
                xaxis=dict(
                    tickangle=0,
                    tickfont=dict(size=10),
                    tickvals=tickvals 
                )
            )

            st.plotly_chart(fig, use_container_width=True)
    except Exception as e:
        st.error(f"An error occurred while processing the price history data: {e}")
        pass

    if os.path.exists("flight_price_matrix.csv"):
        PRICE_MATRIX_PATH = "flight_price_matrix.csv"
        df = load_and_clean_data(PRICE_MATRIX_PATH)
        st.markdown("---")
        
        # Display the data
        display_price_matrix(df)
            
        st.markdown("---")
            
        # Analyze statistics
        stats = analyze_flight_statistics(df)
            
        st.markdown("---")
            
        # Create comparison chart
        create_price_comparison_chart(df)
        
        st.markdown("---")
            
        # NEW: AI-powered insights section
        api_key = "AIzaSyCaktDT344vU3_XKPZyCmFzHU4mlmkAB-k"
        st.header("🤖 AI-Powered Flight Insights")
                
        with st.spinner("Analyzing data with Gemini AI..."):
            data_summary = prepare_data_summary(df)
            ai_insights = generate_gemini_insights(data_summary, api_key)
                    
            st.subheader("Key Trends and Recommendations")
            st.write(ai_insights)
    else:
        st.error("Flight price matrix data not found.")
    

def airline_data():
    st.header("Airline Data")
    JSON_PATH = "google_flights_data.json"

        # Check if file exists
    if not os.path.exists(JSON_PATH):
        st.warning("No flight data found.")
        return

    # Load the JSON data
    with open(JSON_PATH, "r", encoding="utf-8") as f:
        flights = json.load(f)

    # Display each flight as a horizontal card
    for flight in flights:
        with st.container(border=True):
            cols = st.columns([2, 2, 2, 2, 1])

            # Airline name and logo placeholder
            with cols[0]:
                st.subheader(":airplane:")  # You can change or map logos dynamically
                st.markdown(flight.get("company_name", "-"))

            # Time range and airline
            with cols[1]:
                st.markdown(f"**{flight.get('departure_date', '-')} – {flight.get('arrival_date', '-')}**")
                # st.caption(flight.get("company_name", "-"))

            # Flight duration and stops
            with cols[2]:
                st.markdown(f"**{flight.get('flight_duration', '-')}**")
                st.caption(flight.get("stops", "-"))

            # CO2 emissions
            with cols[3]:
                st.markdown(f"**{flight.get('co2_emission', '-') }**")
                st.caption("CO2 impact")

            # Price
            with cols[4]:
                st.markdown(f"<span style='color:green; font-weight:bold;'>{flight.get('price', '-')}</span>", unsafe_allow_html=True)
                st.caption("round trip")



# Initialize input fields based on the trip type
if trip_type == "Round Trip":
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        source = st.text_input("Source")
    with col2:
        destination = st.text_input("Destination")
    with col3:
        departure = st.date_input("Departure")
    with col4:
        arrival = st.date_input("Arrival")
else:
    col1, col2, col3 = st.columns(3)
    with col1:
        source = st.text_input("Source")
    with col2:
        destination = st.text_input("Destination")
    with col3:
        departure = st.date_input("Departure")

# State to track if submission was successful
if "show_segmented" not in st.session_state:
    st.session_state.show_segmented = False

if st.button("Submit"):
    data = {
        "trip_type": trip_type,
        "source": source,
        "destination": destination,
        "departure": str(departure),
        "arrival": str(arrival) if trip_type == "Round Trip" else None
    }
    with st.spinner("⏳ Please wait while we scrape the data..."):
        response = requests.post("http://localhost:5000/submit", json=data, timeout=120)

    if response.status_code == 200:
        st.success("✅ Data received successfully!")
        st.session_state.show_segmented = True
    else:
        st.error("❌ Error occurred")
        st.text(response.text)
        st.session_state.show_segmented = False

# Show segmented control if submission was successful
if st.session_state.get("show_segmented", False):
    selected = st.segmented_control(
        "Select Data View",
        options=["Data Trends", "Airline Data"],
        default="Data Trends",
        selection_mode="single",
        key="data_view"
    )
    if selected == "Data Trends":
        data_trends()
    elif selected == "Airline Data":
        airline_data()