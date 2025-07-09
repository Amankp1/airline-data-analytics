# Import necessary libraries
from bs4 import BeautifulSoup
import requests
import json

# Function to scrape listing elements from Google Flights
def scrape_listings(soup):
    return soup.select('li.pIav2d')

# Function to scrape company name from a flight listing
def scrape_company_name(listing):
    airline_element = listing.select_one('div.Ir0Voe div.sSHqwe')
    return airline_element.text.strip()

# Function to scrape flight duration from a flight listing
def scrape_flight_duration(listing):
    duration_element = listing.select_one('div.AdWm1c.gvkrdb')
    return duration_element.text.strip()

# Function to scrape price from a flight listing
def scrape_price(listing):
    price_element = listing.select_one('div.U3gSDe div.FpEdX span')
    return price_element.text.strip()

# Function to scrape departure and arrival dates from a flight listing
def scrape_departure_arrival_dates(listing):
    departure_date_element = listing.select_one('span.mv1WYe span:first-child [jscontroller="cNtv4b"] span')
    arrival_date_element = listing.select_one('span.mv1WYe span:last-child [jscontroller="cNtv4b"] span')
    return departure_date_element.text.strip(), arrival_date_element.text.strip()

# Function to scrape flight CO2 emission from a flight listing
def scrape_co2_emission(listing):
    co2_element = listing.select_one('div.V1iAHe div.AdWm1c')
    return co2_element.text.strip()

# Function to scrape flight stops from a flight listing
def scrape_flight_stops(listing):
    stops_element = listing.select_one('div.EfT7Ae span.ogfYpf')
    return stops_element.text.strip()

# Main function
def airline_data(url):
    # Make a request to Google Flights URL and parse HTML
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')

    # Scrape flight listings
    listings = scrape_listings(soup)

    # Iterate through each listing and extract flight information
    flight_data = []
    for listing in listings:
        company_name = scrape_company_name(listing)
        flight_duration = scrape_flight_duration(listing)
        price = scrape_price(listing)
        departure_date, arrival_date = scrape_departure_arrival_dates(listing)
        co2_emission = scrape_co2_emission(listing)
        stops = scrape_flight_stops(listing)

        # Store flight information in a dictionary
        flight_info = {
            'company_name': company_name,
            'flight_duration': flight_duration,
            'price': price,
            'departure_date': departure_date,
            'arrival_date': arrival_date,
            'co2_emission': co2_emission,
            'stops': stops
        }

        flight_data.append(flight_info)

    # Save results to a JSON file
    with open('google_flights_data.json', 'w') as json_file:
        json.dump(flight_data, json_file, indent=4)
