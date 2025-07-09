import pandas as pd
from datetime import datetime, timedelta
import streamlit as st
import plotly.express as px



def process_price_history(PRICE_HISTORY_PATH):
    # Load original CSV
    df_raw = pd.read_csv(PRICE_HISTORY_PATH)

    today = datetime.today()
    parsed_data = []

    for row in df_raw['aria-label']:
        try:
            day_part, price_part = row.split(" - ")
            if day_part.strip() == "Today":
                date = today
            else:
                num_days = int(day_part.split()[0])
                date = today - timedelta(days=num_days)

            price = int(price_part.replace("A$", "").replace(",", ""))
            parsed_data.append({"Date": date.date(), "Price": price})
        except:
            continue  # Skip invalid rows

    # Convert to DataFrame
    df = pd.DataFrame(parsed_data)
    df.sort_values("Date", inplace=True)
    df.to_csv(PRICE_HISTORY_PATH, index=False)
    return df




def load_and_clean_data(csv_file_path):
    # Read the CSV file
    df = pd.read_csv(csv_file_path)
    
    # Clean the price column - remove 'A$' and convert to numeric
    df['Price_Numeric'] = df['Price'].str.replace('A$', '').astype(float)
    
    # Parse the dates and extract departure and return dates
    df['Departure_Date'] = df['Dates'].str.extract(r'(\w+ \d+)')
    df['Return_Date'] = df['Dates'].str.extract(r'to (\w+ \d+)')
    
    # Convert to datetime (assuming 2025 year)
    df['Departure_Date'] = pd.to_datetime(df['Departure_Date'] + ' 2025')
    df['Return_Date'] = pd.to_datetime(df['Return_Date'] + ' 2025')
    
    # Calculate trip duration
    df['Trip_Duration'] = (df['Return_Date'] - df['Departure_Date']).dt.days
    
    # Extract price category
    df['Price_Category'] = df['Dates'].str.extract(r'(cheapest price|low price)')
    df['Price_Category'] = df['Price_Category'].fillna('regular price')
    
    # Add day of week for departure and return
    df['Departure_Day'] = df['Departure_Date'].dt.day_name()
    df['Return_Day'] = df['Return_Date'].dt.day_name()
    
    # Check if it's selected
    df['Is_Selected'] = df['Dates'].str.contains('selected', na=False)
    
    return df

def display_price_matrix(df):
    st.subheader("Flight Price Matrix")
    
    # Create pivot table for the matrix
    pivot_df = df.pivot_table(
        values='Price_Numeric', 
        index='Departure_Day', 
        columns='Return_Day', 
        aggfunc='mean'
    )
    
    # Create heatmap
    fig = px.imshow(
        pivot_df,
        labels=dict(x="Return Day", y="Departure Day", color="Price (A$)"),
        x=pivot_df.columns,
        y=pivot_df.index,
        color_continuous_scale='RdYlGn_r',
        title="Average Flight Prices by Departure and Return Days"
    )
    
    fig.update_layout(
        width=800,
        height=600,
        xaxis_title="Return Day",
        yaxis_title="Departure Day"
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Display raw data with formatting
    st.subheader("Detailed Price Data")
    
    # Format the dataframe for display
    display_df = df[['Departure_Date', 'Return_Date', 'Price', 'Trip_Duration', 'Price_Category', 'Is_Selected']].copy()
    display_df['Departure_Date'] = display_df['Departure_Date'].dt.strftime('%Y-%m-%d')
    display_df['Return_Date'] = display_df['Return_Date'].dt.strftime('%Y-%m-%d')
    
    # Color code the selected row
    def highlight_selected(row):
        return ['background-color: lightgreen' if row['Is_Selected'] else '' for _ in row]
    
    styled_df = display_df.style.apply(highlight_selected, axis=1)
    st.dataframe(styled_df, use_container_width=True)

def analyze_flight_statistics(df):
    st.header("Flight Price Analytics & Insights")
    
    # Basic statistics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Cheapest Price", f"A${df['Price_Numeric'].min():.0f}")
    with col2:
        st.metric("Most Expensive", f"A${df['Price_Numeric'].max():.0f}")
    with col3:
        st.metric("Average Price", f"A${df['Price_Numeric'].mean():.0f}")
    with col4:
        st.metric("Price Range", f"A${df['Price_Numeric'].max() - df['Price_Numeric'].min():.0f}")
    
    # Day-wise analysis
    st.subheader("Day-wise Price Analysis")
    
    # Departure day analysis
    dep_day_stats = df.groupby('Departure_Day')['Price_Numeric'].agg(['mean', 'min', 'max', 'count']).round(2)
    dep_day_stats.columns = ['Average Price', 'Minimum Price', 'Maximum Price', 'Count']
    
    # Return day analysis
    ret_day_stats = df.groupby('Return_Day')['Price_Numeric'].agg(['mean', 'min', 'max', 'count']).round(2)
    ret_day_stats.columns = ['Average Price', 'Minimum Price', 'Maximum Price', 'Count']
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Departure Day Statistics**")
        st.dataframe(dep_day_stats)
        
        # Best departure days
        best_dep_days = dep_day_stats.nsmallest(3, 'Average Price')
        st.write("**Best Departure Days (Cheapest)**")
        for day in best_dep_days.index:
            st.write(f"• {day}: A${best_dep_days.loc[day, 'Average Price']:.0f}")
    
    with col2:
        st.write("**Return Day Statistics**")
        st.dataframe(ret_day_stats)
        
        # Best return days
        best_ret_days = ret_day_stats.nsmallest(3, 'Average Price')
        st.write("**Best Return Days (Cheapest)**")
        for day in best_ret_days.index:
            st.write(f"• {day}: A${best_ret_days.loc[day, 'Average Price']:.0f}")
    
    # Trip duration analysis
    st.subheader("Trip Duration Analysis")
    
    duration_stats = df.groupby('Trip_Duration')['Price_Numeric'].agg(['mean', 'min', 'max', 'count']).round(2)
    duration_stats.columns = ['Average Price', 'Minimum Price', 'Maximum Price', 'Count']
    
    # Plot duration vs price
    fig = px.scatter(
        df, 
        x='Trip_Duration', 
        y='Price_Numeric',
        color='Price_Category',
        title="Price vs Trip Duration",
        labels={'Trip_Duration': 'Trip Duration (days)', 'Price_Numeric': 'Price (A$)'},
        hover_data=['Departure_Day', 'Return_Day']
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(duration_stats)
    
    # Price category analysis
    st.subheader("Price Category Analysis")
    
    category_stats = df.groupby('Price_Category')['Price_Numeric'].agg(['mean', 'min', 'max', 'count']).round(2)
    category_stats.columns = ['Average Price', 'Minimum Price', 'Maximum Price', 'Count']
    
    fig = px.box(
        df, 
        x='Price_Category', 
        y='Price_Numeric',
        title="Price Distribution by Category",
        labels={'Price_Category': 'Price Category', 'Price_Numeric': 'Price (A$)'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(category_stats)
    
    # Time-based trends
    st.subheader("Time-based Price Trends")
    
    # Sort by departure date for trend analysis
    df_sorted = df.sort_values('Departure_Date')
    
    fig = px.line(
        df_sorted,
        x='Departure_Date',
        y='Price_Numeric',
        color='Return_Day',
        title="Price Trends by Departure Date",
        labels={'Departure_Date': 'Departure Date', 'Price_Numeric': 'Price (A$)'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Advanced insights
    st.subheader("Key Insights")
    
    insights = []
    
    # Find cheapest combination
    cheapest_flight = df.loc[df['Price_Numeric'].idxmin()]
    insights.append(f"🏆 **Cheapest Flight**: Depart {cheapest_flight['Departure_Day']}, Return {cheapest_flight['Return_Day']} - A${cheapest_flight['Price_Numeric']:.0f}")
    
    # Find most expensive combination
    expensive_flight = df.loc[df['Price_Numeric'].idxmax()]
    insights.append(f"💰 **Most Expensive**: Depart {expensive_flight['Departure_Day']}, Return {expensive_flight['Return_Day']} - A${expensive_flight['Price_Numeric']:.0f}")
    
    # Weekend vs weekday analysis
    weekend_days = ['Saturday', 'Sunday']
    weekend_flights = df[df['Departure_Day'].isin(weekend_days)]
    weekday_flights = df[~df['Departure_Day'].isin(weekend_days)]
    
    if len(weekend_flights) > 0 and len(weekday_flights) > 0:
        weekend_avg = weekend_flights['Price_Numeric'].mean()
        weekday_avg = weekday_flights['Price_Numeric'].mean()
        
        if weekend_avg > weekday_avg:
            insights.append(f"📅 **Weekend Premium**: Weekend departures cost A${weekend_avg - weekday_avg:.0f} more on average")
        else:
            insights.append(f"📅 **Weekday Premium**: Weekday departures cost A${weekday_avg - weekend_avg:.0f} more on average")
    
    # Best value duration
    best_duration = duration_stats.loc[duration_stats['Average Price'].idxmin()]
    insights.append(f"⏱️ **Best Value Duration**: {duration_stats.loc[duration_stats['Average Price'].idxmin()].name} days at A${best_duration['Average Price']:.0f} average")
    
    # Price volatility
    price_volatility = df['Price_Numeric'].std()
    insights.append(f"📊 **Price Volatility**: Standard deviation of A${price_volatility:.0f} indicates {'high' if price_volatility > 100 else 'moderate'} price variation")
    
    for insight in insights:
        st.write(insight)
    
    return {
        'departure_day_stats': dep_day_stats,
        'return_day_stats': ret_day_stats,
        'duration_stats': duration_stats,
        'category_stats': category_stats,
        'insights': insights
    }

def create_price_comparison_chart(df):
    st.subheader("Interactive Price Comparison")
    
    # Allow user to select comparison type
    comparison_type = st.selectbox(
        "Compare prices by:",
        ["Departure Day", "Return Day", "Trip Duration", "Price Category"]
    )
    
    if comparison_type == "Departure Day":
        fig = px.bar(
            df.groupby('Departure_Day')['Price_Numeric'].mean().reset_index(),
            x='Departure_Day',
            y='Price_Numeric',
            title="Average Price by Departure Day",
            labels={'Price_Numeric': 'Average Price (A$)'}
        )
    elif comparison_type == "Return Day":
        fig = px.bar(
            df.groupby('Return_Day')['Price_Numeric'].mean().reset_index(),
            x='Return_Day',
            y='Price_Numeric',
            title="Average Price by Return Day",
            labels={'Price_Numeric': 'Average Price (A$)'}
        )
    elif comparison_type == "Trip Duration":
        fig = px.bar(
            df.groupby('Trip_Duration')['Price_Numeric'].mean().reset_index(),
            x='Trip_Duration',
            y='Price_Numeric',
            title="Average Price by Trip Duration",
            labels={'Price_Numeric': 'Average Price (A$)', 'Trip_Duration': 'Trip Duration (days)'}
        )
    else:  # Price Category
        fig = px.bar(
            df.groupby('Price_Category')['Price_Numeric'].mean().reset_index(),
            x='Price_Category',
            y='Price_Numeric',
            title="Average Price by Price Category",
            labels={'Price_Numeric': 'Average Price (A$)'}
        )
    
    st.plotly_chart(fig, use_container_width=True)