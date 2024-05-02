
from . import app
from flask import Flask, jsonify, request
import requests


#### Going to have all the Request to the financial Stub in this file
## We can name all the api the exact same so that way its easy for frontend to swap once this is completed

# Define the base URL of your financial stub
# FIN_URL = 'http://localhost:5001' local use only
FIN_URL = 'https://hot-carz-financial-service-stub-production.up.railway.app'



@app.route('/api/manager/current-bids', methods=['GET'])
### This is missing the Post but the get works I tested
def proxy_current_bids():
    if request.method == 'GET':
        # URL of your financial stub's current-bids endpoint
        stub_url = f'{FIN_URL}/api/manager/current-bids'

        # Make a GET request to the financial stub
        response = requests.get(stub_url)

        # Check if the request was successful
        if response.status_code == 200:
            # Parse the JSON response
            bid_data = response.json()
            print(bid_data)
            # Return the bid data as a response from your backend API
            return jsonify(bid_data)
        else:
            # If the request was not successful, return an error response
            error_message = f"Failed to fetch current bids from the financial stub. Status code: {response.status_code}"
            return jsonify({'error': error_message}), response.status_code
