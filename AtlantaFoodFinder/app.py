from flask import Flask, request, jsonify
from flask_cors import CORS 
from GoogleAPI.GoogleRequest import get_google_restaurants


def loop_through_results(results):
    # Create an empty dictionary to store the stringified results
    stringFolder = {}

    # Loop through each item in results and assign its string representation to the dictionary
    for i, result in enumerate(results):
        stringFolder[i] = str(result)  # or result.__str__() if you want to use the method directly
        print(str(result))

    return stringFolder

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://127.0.0.1:8000"}})


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
    distance = data.get('distance')
    ratings = data.get('ratings')

    distance = float(distance)
    ratings = float(ratings)

    # Call your function
    results = get_google_restaurants(latitude, longitude, name_or_cuisine, distance*1000, ratings)

    # Return the results as JSON

    stringFolder = loop_through_results(results)

        

    return jsonify(stringFolder)

if __name__ == '__main__':
    app.run(debug=True)



