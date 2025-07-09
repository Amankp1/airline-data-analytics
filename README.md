# Airline Booking Market Data App

This project is a full-stack web application for scraping, analyzing, and visualizing airline flight price data. It combines automated data extraction from Google Flights, advanced analytics, and AI-powered insights to help users make informed travel decisions.

---

## Features

- **Automated Scraping:** Uses Selenium and BeautifulSoup to extract flight prices, historical trends, and airline details from Google Flights.
- **Data Processing:** Cleans and structures price matrices, historical data, and airline listings for analysis.
- **Interactive Analytics:** Visualizes trends, price matrices, and statistics using Streamlit and Plotly.
- **AI Insights:** Integrates Google Gemini AI to generate actionable recommendations and trend summaries.
- **User-Friendly Interface:** Simple web UI for entering trip details and exploring results.

---

## Project Structure

```
airline-data-analytics/
├── app.py                  # Flask backend API server
├── streamlit_app.py        # Streamlit frontend app
├── scrapper1.py            # Selenium-based scraper for price history and matrix
├── scrapper2.py            # BeautifulSoup scraper for airline listings
├── process1.py             # Data cleaning and analytics functions
├── api_integration.py      # Gemini AI integration and data summary
├── requirements.txt        # Python dependencies
├── README.md               # Project documentation
```

---

## Setup Instructions

### 1. Clone the Repository

```sh
git clone https://github.com/Amankp1/airline-data-analytics.git
```

### 2. Install Dependencies

It is recommended to use a virtual environment:

```sh
python -m venv venv
# On Windows:
venv\Scripts\activate
# On macOS/Linux:
source venv/bin/activate
pip install -r requirements.txt
```

### 3. Download ChromeDriver

- Download the [ChromeDriver](https://sites.google.com/chromium.org/driver/) that matches your Chrome version.
- Place the `chromedriver` executable in your PATH or in the project root.

### 4. Run the Flask Backend

In one terminal:

```sh
python app.py
```

### 5. Run the Streamlit Frontend

In a new terminal:

```sh
streamlit run streamlit_app.py
```

---

## How to Use

1. **Open the Streamlit app** in your browser (usually at [http://localhost:8501](http://localhost:8501)).
2. **Enter trip details** (source, destination, departure, and arrival dates).
3. **Submit** the form. The backend will:
   - Scrape Google Flights for price history, price matrix, and airline listings.
   - Process and clean the data.
   - Save results as CSV and JSON files.
4. **Explore the results**:
   - **Data Trends:** View price history, price matrix heatmaps, analytics, and interactive charts.
   - **Airline Data:** Browse detailed airline listings with durations, stops, CO₂ emissions, and prices.
   - **AI Insights:** Read AI-generated recommendations and trend summaries.

---

## Approach & Architecture

### Data Collection

- **scrapper1.py:** Uses Selenium to automate Google Flights, extracting price history and date grid (matrix) data, saving as CSV.
- **scrapper2.py:** Uses BeautifulSoup to parse airline listings from the Google Flights results page, saving as JSON.

### Backend

- **app.py:** Flask API endpoint `/submit` receives trip details, triggers scrapers, and coordinates data processing.

### Data Processing

- **process1.py:** Cleans and structures CSV data, computes statistics, generates visualizations, and provides analytics functions for the frontend.
- **api_integration.py:** Summarizes data and sends it to Google Gemini AI for actionable insights.

### Frontend

- **streamlit_app.py:** Streamlit UI for user input, data visualization, and displaying AI insights.

---

## Requirements

```
Flask
streamlit
selenium
beautifulsoup4
pandas
plotly
requests
google-generativeai
atexit
```

---

## Notes

- **Google Flights scraping** may break if Google changes its page structure.
- **Google Gemini API** requires an API key. Replace the placeholder in `streamlit_app.py` with your own key.
- **ChromeDriver** must be installed and compatible with your Chrome browser.

---

## Dashboard Documentation

The Flight Price Analysis Dashboard provides a powerful interface to explore flight pricing patterns through interactive visualizations and statistical breakdowns. This documentation provides a comprehensive guide to understanding and using the key components of the dashboard.

---

### 1. Dashboard Components

#### **Flight Price Matrix**
- **Function**: Displays an interactive heatmap of flight prices across combinations of departure and return dates.
- **Design**: 
  - X-axis = Return Days  
  - Y-axis = Departure Days  
  - Cells are **color-coded** to show price intensity:
    - **Green/Cool Colors**: Lower prices (cheaper)
    - **Red/Warm Colors**: Higher prices (costlier)
- **Usage**:
  - Hover over a cell to view the exact price for a date pair.
  - Quickly spot cost-effective date combinations and price anomalies.
- **Business Value**: Instantly identify affordable travel combinations and recurring price patterns.

#### **Detailed Price Data Table**
- **Function**: Provides a full tabular breakdown of every available flight option.
- **Columns**:
  - **Departure Date**
  - **Return Date**
  - **Price**
  - **Trip Duration**
  - **Price Category** (Cheapest, Low, Regular)
  - **Is Selected**
- **Interactive Features**:
  - Column sorting
  - Filter by price or date range
  - Color-highlighted selected flights (in light green)
- **Business Value**: Offers complete transparency and enables users to compare options at a granular level.

---

### 2. Statistical Analysis

#### **Key Performance Metrics**
- Displays four primary statistics:
  - **Cheapest Price**
  - **Most Expensive Price**
  - **Average Price**
  - **Price Range**
- **Interpretation**:
  - A low price range indicates price stability.
  - A large gap between average and cheapest price shows savings potential.

#### **Day-wise Price Analysis**
- **Departure and Return Day Statistics Tables** show:
  - **Average**, **Minimum**, and **Maximum Price**
  - **Number of Flights** available for each day
- **Best Days Rankings**:
  - Highlights top 3 cheapest departure and return days.
- **Interpretation**:
  - Lower averages and narrower ranges are generally better for budget-conscious planning.

#### **Trip Duration Analysis**
- **Table** displays average, min, max prices, and counts for each duration.
- **Scatter Plot**:
  - **X-axis**: Trip duration
  - **Y-axis**: Price
  - **Colors**: Represent price categories
- **Business Value**:
  - Identifies the optimal number of travel days for best price-to-value ratio.

#### **Price Category Analysis**
- **Categories**:
  - Cheapest Price (promotional deals)
  - Low Price (below average)
  - Regular Price (standard fare)
- **Box Plot** Visualization:
  - Shows price distribution, spread, and outliers
- **Insights**:
  - Understand how fares are distributed across categories
  - Spot deals and pricing anomalies

---

### 3. Visualization Guide

#### **Price Heatmap (Matrix)**
- **Colors**:
  - Dark Green: Lowest prices
  - Light Green: Below average
  - Yellow: Average
  - Orange: Above average
  - Red: Highest prices
- **Interactions**:
  - Hover over cells for detailed info
  - Zoom into specific areas
  - Refer to the legend for interpretation

#### **Time-based Trend Lines**
- **X-axis**: Departure dates  
- **Y-axis**: Price  
- **Multiple colored lines**: Represent return dates
- **Patterns**:
  - Flat lines: Stable pricing
  - Upward trends: Increasing prices
  - Peaks/Valleys: High/low demand windows

#### **Comparison Bar Charts**
- **Types**:
  - Departure day comparison
  - Return day comparison
  - Trip duration comparison
  - Price category comparison
- **Interpretation**:
  - Taller bars = higher prices
  - Clickable elements for breakdowns
  - Color-coded consistently with other visuals

---

### Summary

This dashboard enables users to:
- Discover the most cost-effective travel dates.
- Compare price patterns by day, trip duration, or category.
- Leverage intuitive visualizations to interpret complex pricing data.
- Make informed, data-backed booking decisions for personal or business travel.



