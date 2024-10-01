from flask import Flask, request, jsonify
from flask_cors import CORS 
from GoogleAPI.GoogleRequest import get_google_restaurants


app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route('/')
def index():
    return "Flask is running!"

# API route to call your function
@app.route('/search-restaurants', methods=['POST'])
def search_restaurants():
    data = request.get_json()
    
    # Extract parameters from the request
    latitude = data.get('latitude')
    longitude = data.get('longitude')
    name_or_cuisine = data.get('name_or_cuisine', 'restaurants')

    # Call your function
    results = get_google_restaurants(latitude, longitude, name_or_cuisine)

    # Return the results as JSON
    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
