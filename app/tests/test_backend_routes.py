# tests/test_backend_routes.py
# this file contains unit tests for the Non-Financial Backend Endpoints here in this repo in routes.py

import os
import json
import pytest
import string
import random
from app import app, db
from app.models import CarInfo, Member, MemberSensitiveInfo, Employee, EmployeeSensitiveInfo, ServiceAppointment
from config import Config


'''

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!DONT EVER RUN PYTEST ALONE. ALWAYS RUN WITH THIS LINE BELOW!
!               'FLASK_ENV=testing pytest'                  !
!           OR ELSE OUR PRODUCTION DB IS FUCKED             ! 
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

'''

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            yield client


def generate_random_string():
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(17))


def delete_row(new_entry):
    db.session.delete(new_entry)
    db.session.commit()


def data_reset_service_appointment():
    # function used to reset the data we used back to how it was in the DB
    insertData = ServiceAppointment(
        appointment_id=1,
        memberID=1,
        appointment_date='2024-04-10 14:00:00',
        service_name='Oil Change'
    )
    db.session.add(insertData)
    db.session.commit()


def test_addon_information(client):
    response = client.get('/api/vehicles/add-ons')

    assert response.status_code == 200

    # asserts to make sure the content type returned is json
    assert response.headers['Content-Type'] == 'application/json'

    # we check to make sure the response body structure and content from the called API is exactly what we want it to return
    data = response.get_json()
    assert data is not None
    assert isinstance(data, list)  # assert that the response returned is a list of dictionaries

    # assert the data
    for addon_data in data:
        assert 'itemID' in addon_data
        assert 'itemName' in addon_data
        assert 'totalCost' in addon_data
        assert isinstance(addon_data['itemID'], int)
        assert isinstance(addon_data['itemName'], str)
        assert isinstance(addon_data['totalCost'], str)


# def test_vehicle_information(client):
#     # test response and content type when no data is passed to the endpoint
#     response_without_query = client.get('/api/vehicles/search')
#     assert response_without_query.status_code == 200
#     assert response_without_query.headers['Content-Type'] == 'application/json'
#
#     # ensure that the data returned from nothing passed to the endpoint is indeed
#     # a list of dictionaries and has data being returned
#     data_without_query = response_without_query.get_json()
#     assert data_without_query is not None
#     assert isinstance(data_without_query, list)
#     assert len(data_without_query) > 0
#
#     # ensures that the dictionaries in data_without_query have been properly cleaned up and don't contain any
#     # SQLAlchemy-specific attributes, which could potentially cause issues if included in the API response. This
#     # ensures that the API response is clean and contains only relevant data.
#     for car_dict in data_without_query:
#         assert '_sa_instance_state' not in car_dict
#
#     # test the endpoint with search query value
#     response_with_query = client.get('/api/vehicles/search?search_query=Toyota')
#     assert response_with_query.status_code == 200
#     assert response_with_query.headers['Content-Type'] == 'application/json'
#
#     data_with_query = response_with_query.get_json()
#     assert data_with_query is not None
#     assert isinstance(data_with_query, list)
#
#     if len(data_with_query) > 0:
#         for car_dict in data_with_query:
#             assert '_sa_instance_state' not in car_dict  # Ensure _sa_instance_state is removed
#     else:
#         # If no results are found for the search query, response should still be 200 because it just means that there are
#         # no cars of that type in stock
#         assert response_with_query.status_code == 200
#
#
# def test_add_vehicle(client):
#     data = {
#         'VIN_carID': generate_random_string(),
#         'make': 'Toyota',
#         'model': 'Camry',
#         'body': 'Sedan',
#         'year': 2023,
#         'color': 'Red',
#         'mileage': 10000,
#         'details': 'Test Entry',
#         'description': 'Test Entry',
#         'viewsOnPage': 100,
#         'pictureLibraryLink': 'link/to/carpic',
#         'status': 'new',
#         'price': '20000'
#     }
#     response = client.post('/api/vehicles/add', json=data)
#     assert response.status_code == 201
#
#     # assert that the vehicle was added successfully and the request truly was commited to the DB
#     assert CarInfo.query.filter_by(VIN_carID=data['VIN_carID']).first() is not None
#
#     # manually delete the added vehicle after assertions to not pollute real data
#     with app.app_context():
#         CarInfo.query.filter_by(VIN_carID=data['VIN_carID']).delete()
#         db.session.commit()
#
#
# def test_vehicle(client):
#     # this test is to test the API for returning vehicles based on the VIN number value
#
#     response_found = client.get('/api/vehicles', query_string={'vin': '1G4HP52KX44657084'})  # valid VIN number
#     assert response_found.status_code == 200
#     assert response_found.headers['Content-Type'] == 'application/json'
#     data_found = response_found.get_json()
#     assert data_found is not None
#
#     # iterate through the columns and confirm that the data we need to grab is there and intact
#     expected_keys = ['VIN_carID', 'make', 'model', 'body', 'year', 'color', 'mileage', 'details', 'description',
#                      'viewsOnPage', 'pictureLibraryLink', 'status', 'price']
#     for key in expected_keys:
#         assert key in data_found
#
#     # Assertions and testing for when an invalid VIN value is passed the endpoint (status code 404)
#     response_not_found = client.get('/api/vehicles', query_string={'vin': 'INVALID-VIN123'})
#     assert response_not_found.status_code == 404
#     assert response_not_found.headers['Content-Type'] == 'application/json'
#     data_not_found = response_not_found.get_json()
#     assert 'message' in data_not_found
#     assert data_not_found['message'] == 'Vehicle not found'
#
#
# def test_random_vehicles(client):
#     random_car_response = client.get('/api/vehicles/random')
#     assert random_car_response.status_code == 200
#     assert random_car_response.headers['Content-Type'] == 'application/json'
#
#     data_found = random_car_response.get_json()
#     assert data_found is not None
#     # print(data_found)
#     assert isinstance(data_found, list)  # ensures that the response is a list of dictionaries
#     assert len(data_found) == 2  # ensures that two vehicles' information is returned
#
#     expected_keys = ['VIN_carID', 'make', 'model', 'body', 'year', 'color', 'mileage', 'details', 'description',
#                      'viewsOnPage', 'pictureLibraryLink', 'status', 'price']
#     for car_data in data_found:
#         for key in expected_keys:
#             assert key in car_data
#
#
# def test_get_all_employees(client):
#     response = client.get('/api/employees')
#     assert response.status_code == 200
#     assert response.headers['Content-Type'] == 'application/json'
#
#     data = response.get_json()
#     assert data is not None
#     assert isinstance(data, list)
#
#     # Check if each dictionary in the response contains the expected keys
#     expected_keys = ['employeeID', 'firstname', 'lastname', 'email', 'phone', 'address', 'employeeType']
#     for employee_data in data:
#         for key in expected_keys:
#             assert key in employee_data
#
#
# def test_get_test_drives(client):
#     # this testcase tests the endpoint for retriving all of the testdrive information in the DB
#     # and which member is test-driving which car
#
#     response = client.get('/api/testdrives')
#     assert response.status_code == 200
#     assert response.headers['Content-Type'] == 'application/json'
#
#     data = response.get_json()
#     assert data is not None
#     assert isinstance(data, list)
#
#     expected_keys = ['fullname', 'phone', 'car_id', 'car_make_model', 'appointment_date']
#     for test_drive_info in data:
#         for key in expected_keys:
#             assert key in test_drive_info
#
#
def test_update_confirmation(client):
    data = {'testdrive_id': 1, 'confirmation': 3}
    response = client.post('/api/testdrives/update_confirmation', json=data)
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'

    data_response = response.get_json()
    assert 'message' in data_response
    assert data_response['message'] == 'Confirmation updated successfully'
#
#
# # test after the endpont works well on the frontend
# # def test_login_employee(client):
# #     # Test scenario when employee login is successful
# #
# #     login_data = {'email': 'tsteger0@de.vu', 'password': 'on9vlvku'}
# #     response = client.post('/api/employees/login', json=login_data)
# #     assert response.status_code == 200
# #
# #     data = response.get_json()
# #     expected_fields = ['firstname', 'lastname', 'email', 'phone', 'address', 'employeeType']
# #
# #     assert data
# #     for field in expected_fields:
# #         assert field in data  # assert that the column is in the returned data
# #         assert data[field]  # assert that the data in the column is indeed not empty
#
#
# def test_create_employee(client):
#     employee_data = {
#         "firstname": "testEmployee",
#         "lastname": "testEmployee",
#         "email": "testEmployee@example.com",
#         "phone": "1234567890",
#         "address": "123 Example St",
#         "employeeType": "Technician",
#         "password": "a123",
#         "driverID": "exampleDriverID",
#         "SSN": "exampleSSN"
#     }
#
#     # Sending a POST request to create an employee
#     response = client.post('/api/employees/create', json=employee_data)
#     assert response.status_code == 201
#
#     with app.app_context():
#         # verifying that the employee is created in the database
#         created_employee = Employee.query.filter_by(email=employee_data["email"]).first()
#         assert created_employee is not None
#
#         # verifying that the employee's sensitive information is created
#         created_sensitive_info = EmployeeSensitiveInfo.query.filter_by(employeeID=created_employee.employeeID).first()
#         assert created_sensitive_info is not None
#
#         # rolls back the changes in the database
#         delete_row(created_sensitive_info)
#         delete_row(created_employee)
#
#
# def test_get_current_user(client):
#     # this unit test, tests login Auth to make sure the user can and does indeed login
#
#     # no user Auth
#     response = client.get('/@me')
#     assert response.status_code == 401
#
#     # user with Auth logs in
#     with app.test_client() as client:
#         with client.session_transaction() as sess:
#             sess['member_session_id'] = 1  # set member ID here to get login for them
#
#         # make a request to the route and get a 200 for good login auth
#         response = client.get('/@me')
#         assert response.status_code == 200
#
#         data = json.loads(response.data.decode('utf-8'))
#         assert data is not None
#
#         columns = ['memberID', 'first_name', 'last_name', 'email', 'phone', 'driverID', 'join_date']
#         # print(data)
#         for column_data in columns:
#             assert column_data in data
#
#
# # will finish another time, i got everything else kinda done tho so its ok lol
# def test_get_all_members(client):
#     response = client.get('/api/members')
#     assert response.status_code == 200
#
#
# def test_login_member(client):
#     # test case for valid login
#     data_valid = {'username': 'kscinelli0', 'password': 'gi2z9nka'}
#     response_valid = client.post('/api/members/login', json=data_valid)
#     assert response_valid.status_code == 200
#     assert 'memberID' in response_valid.json
#
#     # test case for invalid credentials
#     data_invalid = {'username': 'invalid_username', 'password': 'invalid_password'}
#     response_invalid = client.post('/api/members/login', json=data_invalid)
#     assert response_invalid.status_code == 404
#     assert 'error' in response_invalid.json
#
#
# def test_create_member(client):
#     # Define member data for testing
#     member_data = {
#         "first_name": "testMember",
#         "last_name": "testMember",
#         "email": "testMember@example.com",
#         "phone": "1234567890",
#         "username": "testMember_username",
#         "password": "password123"
#     }
#
#     # Send a POST request to create a member
#     response = client.post('/api/members/create', json=member_data)
#
#     # Check if the response status code is 201 (Created)
#     assert response.status_code == 201
#
#     # Check if the member and associated sensitive info are created in the database
#     with app.app_context():
#         created_member = Member.query.filter_by(email=member_data["email"]).first()
#         assert created_member is not None
#
#         # Check if the associated sensitive info is also created
#         created_sensitive_info = MemberSensitiveInfo.query.filter_by(memberID=created_member.memberID).first()
#         assert created_sensitive_info is not None
#         assert created_sensitive_info.username == member_data["username"]
#         assert created_sensitive_info.password == member_data["password"]
#
#         # Delete the created member and sensitive info from the database
#         delete_row(created_sensitive_info)
#         delete_row(created_member)
#
#
# # will test once implemented on the frontend fr
# # def test_get_current_user(client):
# #     # mock session to imitate an unauthorized user/session, will get to valid session another time
# #     response = client.get('/@me')
# #     assert response.status_code == 401
# #     data = response.get_json()
# #     assert 'error' in data
# #     assert data['error'] == 'Unauthorized'
#
#
# def test_service_appointments_get(client):
#     response = client.get('/api/service-appointments')
#     assert response.status_code == 200
#     assert response.headers['Content-Type'] == 'application/json'
#
#     data = response.get_json()
#     assert data is not None
#     assert isinstance(data, list)
#     expected_keys = ['appointment_id', 'memberID', 'appointment_date', 'service_name']
#
#     for service_appt in data:
#         for key in expected_keys:
#             assert key in service_appt
#
#
# def test_service_appointments_post(client):
#     # general test case for when there is a successful cancel value for the session appointments
#     data = {'appointment_id': 1, 'cancelValue': 1}
#     response = client.post('/api/service-appointments', json=data)
#     assert response.status_code == 200
#     assert response.json == {'message': 'Appointment canceled successfully'}
#
#     # test case for when there are missing parameters
#     data_missing_params = {'cancelValue': 1}
#     response_missing_params = client.post('/api/service-appointments', json=data_missing_params)
#     assert response_missing_params.status_code == 400
#     assert response_missing_params.json == {'error': 'Both appointment_id and cancelValue parameters are required.'}
#
#     # test case for when there is an invalid cancellation value
#     data_invalid_cancel_value = {'appointment_id': 1, 'cancelValue': 0}
#     response_invalid_cancel_value = client.post('/api/service-appointments', json=data_invalid_cancel_value)
#     assert response_invalid_cancel_value.status_code == 400
#     assert response_invalid_cancel_value.json == {'error': 'Invalid cancellation value.'}
#
#     # test case for when a service appointment is not found
#     data_appointment_not_found = {'appointment_id': 999, 'cancelValue': 1}
#     response_appointment_not_found = client.post('/api/service-appointments', json=data_appointment_not_found)
#     assert response_appointment_not_found.status_code == 404
#     assert response_appointment_not_found.json == {'error': 'Appointment not found.'}
#
#     data_reset_service_appointment()
