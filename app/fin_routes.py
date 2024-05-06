
from . import app
from flask import Flask, request, jsonify, session
import requests


#### Going to have all the Request to the financial Stub in this file
## We can name all the api the exact same so that way its easy for frontend to swap once this is completed

# Define the base URL of your financial stub
# FIN_URL = 'http://localhost:5001' local use only
FIN_URL = 'https://hot-carz-financial-service-stub-production.up.railway.app'

#  http://localhost:5000/forward?route=http://localhost:5001/example_api

@app.route('/forward', methods=['POST', 'GET'])
#  ${BASE_URL}/forward?route=${FINANCE_URL}/<REPLACE WITH FIN API ROUTE>
def forward_request():
    if request.method == 'POST':
        # Handle POST requests
        forward_route = request.args.get('route')
        if not forward_route:
            return jsonify({'error': 'No route specified in the query string'}), 400
        return forward_post_request(forward_route)
    elif request.method == 'GET':
        # Handle GET requests
        forward_route = request.args.get('route')
        if not forward_route:
            return jsonify({'error': 'No route specified in the query string'}), 400
        return forward_get_request(forward_route)

def forward_post_request(forward_route):
    request_data = request.get_json()

    # Check if a member is logged in
    member_id = session.get("member_session_id")
    if member_id:
        request_data['member_id'] = member_id
    else:
        # Check if an employee is logged in
        employee_id = session.get("employee_session_id")
        if employee_id:
            request_data['employee_id'] = employee_id

    try:
        response = requests.post(forward_route, json=request_data)
        response_data = response.json()
        return jsonify(response_data), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500

def forward_get_request(forward_route):
    # Extract additional query parameters from the request
    additional_params = {key: value for key, value in request.args.items() if key != 'route'}
    
    # Check if a member is logged in
    member_id = session.get("member_session_id")
    if member_id:
        params = {'member_id': member_id}
    else:
        # Check if an employee is logged in
        employee_id = session.get("employee_session_id")
        if employee_id:
            params = {'employee_id': employee_id}
        else:
            params = {}
# Construct the full URL including additional query parameters
    full_url = forward_route + '&' + '&'.join([f"{key}={value}" for key, value in additional_params.items()])
    try:
        response = requests.get(full_url, params=params)
        response_data = response.json()
        return jsonify(response_data), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500





# @app.route('/api/manager/current-bids', methods=['GET'])
# ### This is missing the Post but the get works I tested
# def proxy_current_bids():
#     if request.method == 'GET':
#         # URL of your financial stub's current-bids endpoint
#         stub_url = f'{FIN_URL}/api/manager/current-bids'

#         # Make a GET request to the financial stub
#         response = requests.get(stub_url)

#         # Check if the request was successful
#         if response.status_code == 200:
#             # Parse the JSON response
#             bid_data = response.json()
#             print(bid_data)
#             # Return the bid data as a response from your backend API
#             return jsonify(bid_data)
#         else:
#             # If the request was not successful, return an error response
#             error_message = f"Failed to fetch current bids from the financial stub. Status code: {response.status_code}"
#             return jsonify({'error': error_message}), response.status_code