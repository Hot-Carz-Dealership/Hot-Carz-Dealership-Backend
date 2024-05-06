
from . import app
from flask import Flask, request, jsonify, session
import requests


'''ALL OF THE HTTP REQUEST  GO THRU /FORWARD IN ORDER TO USE THE FINANCIAL STUB'''

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
    if additional_params:
        full_url = forward_route + '&' + '&'.join([f"{key}={value}" for key, value in additional_params.items()])
    else:
        full_url = forward_route

    try:
        response = requests.get(full_url, json=params)
        response_data = response.json()
        return jsonify(response_data), response.status_code
    except requests.exceptions.RequestException as e:
        return jsonify({'error': str(e)}), 500


