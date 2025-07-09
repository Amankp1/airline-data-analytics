import streamlit as st
import pandas as pd
import google.generativeai as genai
import os
import plotly.express as px
import json
        
def prepare_data_summary(df):
    summary = {
        "basic_stats": {
            "total_flights": len(df),
            "price_range": {
                "min": df['Price_Numeric'].min(),
                "max": df['Price_Numeric'].max(),
                "average": df['Price_Numeric'].mean(),
                "median": df['Price_Numeric'].median(),
                "std_dev": df['Price_Numeric'].std()
            },
            "date_range": {
                "earliest_departure": df['Departure_Date'].min().strftime('%Y-%m-%d'),
                "latest_departure": df['Departure_Date'].max().strftime('%Y-%m-%d'),
                "earliest_return": df['Return_Date'].min().strftime('%Y-%m-%d'),
                "latest_return": df['Return_Date'].max().strftime('%Y-%m-%d')
            }
        },
        "departure_day_analysis": df.groupby('Departure_Day')['Price_Numeric'].agg(['mean', 'min', 'max', 'count']).round(2).to_dict(),
        "return_day_analysis": df.groupby('Return_Day')['Price_Numeric'].agg(['mean', 'min', 'max', 'count']).round(2).to_dict(),
        "duration_analysis": df.groupby('Trip_Duration')['Price_Numeric'].agg(['mean', 'min', 'max', 'count']).round(2).to_dict(),
        "price_category_analysis": df.groupby('Price_Category')['Price_Numeric'].agg(['mean', 'min', 'max', 'count']).round(2).to_dict(),
        "temporal_trends": df.sort_values('Departure_Date')[['Departure_Date', 'Price_Numeric', 'Trip_Duration']].to_dict('records')[:10],  # First 10 records for trend analysis
        "weekend_vs_weekday": {
            "weekend_avg": df[df['Departure_Day'].isin(['Saturday', 'Sunday'])]['Price_Numeric'].mean() if len(df[df['Departure_Day'].isin(['Saturday', 'Sunday'])]) > 0 else None,
            "weekday_avg": df[~df['Departure_Day'].isin(['Saturday', 'Sunday'])]['Price_Numeric'].mean() if len(df[~df['Departure_Day'].isin(['Saturday', 'Sunday'])]) > 0 else None
        }
    }
    return summary

def generate_gemini_insights(data_summary, api_key):
    try:
        # Configure Gemini API
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")
        
        # Create prompt for analysis
        prompt = f"""
        Analyze the following flight price data and provide key insights about demand trends, price changes, and patterns. 
        Focus on actionable insights for travelers and provide a concise point-wise summary.

        Data Summary:
        {json.dumps(data_summary, indent=2, default=str)}

        Please provide:
        1. Key demand trends (which days/durations are most popular)
        2. Price change patterns (seasonal, weekly, duration-based)
        3. Best booking strategies based on the data
        4. Notable price anomalies or opportunities
        5. Weekend vs weekday patterns
        6. Optimal trip duration recommendations

        Keep the response concise and point-wise. Focus only on the most relevant and actionable insights.
        """
        
        response = model.generate_content(prompt)
        return response.text
    
    except Exception as e:
        return f"Error generating AI insights: {str(e)}"

