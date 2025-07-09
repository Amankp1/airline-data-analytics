from flask import Flask, request, jsonify
from scrapper1 import data_scrapper
from scrapper2 import airline_data

app = Flask(__name__)

@app.route('/submit', methods=['POST'])
def submit_data():
    try:
        print("🟢 Request received")
        data = request.get_json()
        print("📦 Data received:", data)

        current_url = data_scrapper(**data)
        print("🌐 Scraper finished:", current_url)

        airline_data(current_url)
        print("✅ Data processing done")

        return jsonify({"message": "Success", "url": current_url}), 200
    except Exception as e:
        import traceback; traceback.print_exc()
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000, host='0.0.0.0')