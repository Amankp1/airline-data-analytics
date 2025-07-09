# Import required modules
from flask import Flask, request, jsonify
from scrapper1 import data_scrapper
from scrapper2 import airline_data

# Initialize the Flask app
app = Flask(__name__)

# Define route for POST request at '/submit'
@app.route('/submit', methods=['POST'])
def submit_data():
    try:
        print("Request received")

        # Parse incoming JSON data from the request
        data = request.get_json()
        print("Data received:", data)

        # Call data_scrapper function with unpacked data dictionary
        current_url = data_scrapper(**data)
        print("Scraper finished:", current_url)

        # Process the scraped data using airline_data function
        airline_data(current_url)
        print("Data processing done")

        # Return success response with the URL
        return jsonify({"message": "Success", "url": current_url}), 200
    except Exception as e:
        # Print the full stack trace for debugging in case of an error
        import traceback; traceback.print_exc()

        # Return error response with status code 500
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')
