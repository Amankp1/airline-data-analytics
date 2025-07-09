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

## Contributing

Contributions are welcome! Please open an issue or submit a pull request for improvements or bug fixes.

---

## License

This project is for educational and research purposes only. Please respect the terms of service of any third-party sites you interact with.
