# tests/test_backend_routes.py
# this file contains unit tests for the Non-Financial Backend Endpoints here in this repo in routes.py

import os
import json
import secrets
import time
import pytest
import string
import random

import sqlalchemy.sql

from app import app, db
from app.models import CarInfo, Member, MemberSensitiveInfo, Employee, EmployeeSensitiveInfo, ServiceAppointment, \
    CarVINs
from config import Config


'''

!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
!!!!DONT EVER RUN PYTEST ALONE. ALWAYS RUN WITH THIS LINE BELOW!!!!
!!!!               'FLASK_ENV=testing pytest'                  !!!!
!!!!           OR ELSE OUR PRODUCTION DB IS FUCKED             !!!! 
!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!

'''

@pytest.fixture
def client():
    with app.test_client() as client:
        with app.app_context():
            yield client


def generate_random_string():
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(17))


def generateSSN():
    characters = string.digits
    return ''.join(random.choice(characters) for _ in range(9))


def generateEmail():
    username_length = random.randint(8, 15)
    username = ''.join(random.choices(string.ascii_lowercase + string.digits, k=username_length))
    domains = ['example.com', 'test.com', 'domain.com']  # domain examples
    domain = random.choice(domains)
    email = username + '@' + domain
    return email


def generateDriverID():
    capital_letter = random.choice(string.ascii_uppercase)
    digits = string.digits
    id_digits = ''.join(random.choice(digits) for _ in range(14))
    return capital_letter + id_digits


def delete_row(new_entry):
    db.session.delete(new_entry)
    db.session.commit()


def data_reset_service_appointment():
    # function used to reset the data we used back to how it was in the DB
    changeStatus = ServiceAppointment.query.filter_by(appointment_id=1).first()
    changeStatus.status = 'Scheduled'
    db.session.commit()


def test_addon_information(client):
    # TEST API: /api/vehicles/add-ons
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
        # assert isinstance(addon_data['totalCost'], int)
    # add 500 error code here for when DB is not able to be accessed


def test_vehicle_search(client):
    # TEST API: /api/vehicles/search
    # test response and content type when no data is passed to the endpoint
    response_without_query = client.get('/api/vehicles/search')
    assert response_without_query.status_code == 200
    assert response_without_query.headers['Content-Type'] == 'application/json'

    # ensure that the data returned from nothing passed to the endpoint is indeed
    # a list of dictionaries and has data being returned
    data_without_query = response_without_query.get_json()
    assert data_without_query is not None
    assert isinstance(data_without_query, list)
    assert len(data_without_query) > 0

    # ensures that the dictionaries in data_without_query have been properly cleaned up and don't contain any
    # SQLAlchemy-specific attributes, which could potentially cause issues if included in the API response. This
    # ensures that the API response is clean and contains only relevant data.
    for car_dict in data_without_query:
        assert '_sa_instance_state' not in car_dict

    # test the endpoint with search query value
    response_with_query = client.get('/api/vehicles/search?search_query=Toyota')
    assert response_with_query.status_code == 200
    assert response_with_query.headers['Content-Type'] == 'application/json'

    data_with_query = response_with_query.get_json()
    assert data_with_query is not None
    assert isinstance(data_with_query, list)

    if len(data_with_query) > 0:
        for car_dict in data_with_query:
            assert '_sa_instance_state' not in car_dict  # Ensure _sa_instance_state is removed or else we can't really use the data
    else:
        # If no results are found for the search query, response should still be 200 because it just means that there are
        # no cars of that type in stock
        assert len(data_without_query) == 0
        assert response_with_query.status_code == 200


def test_add_vehicle(client):
    # TEST API: /api/vehicles/add
    VIN_carID = generate_random_string()

    car_data_json = {
        'VIN_carID': VIN_carID,
        'make': 'Toyota',
        'model': 'Camry',
        'body': 'Sedan',
        'year': 2023,
        'color': 'Red',
        'mileage': 10000,
        'details': 'Test Entry',
        'description': 'Test Entry',
        'viewsOnPage': 1,
        'pictureLibraryLink': 'link/to/carpic',
        # 'status': 'new',
        'price': '20000'
    }
    response = client.post('/api/vehicles/add', json=car_data_json)
    assert response.status_code == 201

    # assert that the vehicle was added successfully and the request truly was commited to the DB
    assert CarVINs.query.filter_by(VIN_carID=VIN_carID).first() is not None
    assert CarInfo.query.filter_by(VIN_carID=VIN_carID).first() is not None

    # ---- no, not to work in test db
    # manually delete the added vehicle after assertions to not pollute real data
    # with app.app_context():
    #     CarInfo.query.filter_by(VIN_carID=car_data_json['VIN_carID']).delete()
    #     db.session.commit()


def test_vehicle(client):
    # TEST API: /api/vehicles
    # this test is to test the API for returning vehicles based on the VIN number value

    response_found = client.get('/api/vehicles', query_string={'vin': '1G4HP52KX44657084'})  # valid VIN number
    assert response_found.status_code == 200
    assert response_found.headers['Content-Type'] == 'application/json'
    data_found = response_found.get_json()
    assert data_found is not None

    # iterate through the columns and confirm that the data we need to grab is there and intact
    expected_keys = ['VIN_carID', 'make', 'model', 'body', 'year', 'color', 'mileage', 'details', 'description',
                     'viewsOnPage', 'pictureLibraryLink', 'status', 'price']
    for key in expected_keys:
        assert key in data_found
        assert data_found[key] is not None

    # Assertions and testing for when an invalid VIN value is passed the endpoint (status code 404)
    response_not_found = client.get('/api/vehicles', query_string={'vin': 'INVALID-VIN123'})
    assert response_not_found.status_code == 404
    assert response_not_found.headers['Content-Type'] == 'application/json'
    data_not_found = response_not_found.get_json()
    assert 'message' in data_not_found
    assert data_not_found['message'] == 'Vehicle not found'


def test_random_vehicles(client):
    # TEST API: /api/vehicles/random
    random_car_response = client.get('/api/vehicles/random')
    assert random_car_response.status_code == 200
    assert random_car_response.headers['Content-Type'] == 'application/json'

    data_found = random_car_response.get_json()
    assert data_found is not None
    # print(data_found)
    assert isinstance(data_found, list)  # ensures that the response is a list of dictionaries
    assert len(data_found) == 2  # ensures that two vehicles' information is returned

    expected_keys = ['VIN_carID', 'make', 'model', 'body', 'year', 'color', 'mileage', 'details', 'description',
                     'viewsOnPage', 'pictureLibraryLink', 'status', 'price']
    for car_data in data_found:
        for key in expected_keys:
            assert key in car_data
            assert car_data[key] is not None


def test_get_all_employees(client):
    # TEST API: /api/employees
    response = client.get('/api/employees')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'

    data = response.get_json()
    assert data is not None
    assert isinstance(data, list)

    # Check if each dictionary in the response contains the expected keys
    expected_keys = ['employeeID', 'first_name', 'last_name', 'email', 'phone', 'address', 'city', 'state', 'zipcode', 'employeeType']
    for employee_data in data:
        for key in expected_keys:
            assert key in employee_data
            assert employee_data[key] is not None


def test_get_test_drives(client):
    # TEST API: /api/testdrives
    # this testcase tests the endpoint for retriving all of the testdrive information in the DB
    # and which member is test-driving which car

    response = client.get('/api/testdrives')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'

    data = response.get_json()
    assert data is not None
    assert isinstance(data, list)

    expected_keys = ['fullname', 'phone', 'car_id', 'car_make_model', 'appointment_date']
    for test_drive_info in data:
        for key in expected_keys:
            assert key in test_drive_info
            assert test_drive_info[key] is not None


def test_update_confirmation(client):
    # TEST API: /api/testdrives/update_confirmation
    for i in range(1, 5):
        data = {'testdrive_id': 1, 'confirmation': i}
        response = client.post('/api/testdrives/update_confirmation', json=data)
        assert response.status_code == 200
        assert response.headers['Content-Type'] == 'application/json'

        data_response = response.get_json()
        assert 'message' in data_response
        assert data_response['message'] == 'Confirmation updated successfully'


# test after the endpont works well on the frontend
def test_login(client):
    # TEST API: /api/login
    # Test scenario when employee login is successful

    # employee login
    employee_login_data = {'username': 'tsteger0@de.vu', 'password': 'on9vlvku'}
    response = client.post('/api/login', json=employee_login_data)
    assert response.status_code == 200

    data = response.get_json()
    expected_fields = ['employeeID', 'first_name', 'last_name', 'email', 'phone', 'address', 'city', 'state', 'zipcode', 'employeeType']

    assert data is not None
    for field in expected_fields:
        assert field in data  # assert that the column is in the returned data
        assert data[field] is not None  # assert that the data in the column is indeed not empty

    # logout to test the employee login
    response = client.post('/api/logout', json=employee_login_data)
    assert response.status_code == 200

    # member Login
    member_login_data = {'username': 'kscinelli0', 'password': 'gi2z9nka'}
    response = client.post('/api/login', json=member_login_data)
    assert response.status_code == 200

    data = response.get_json()
    expected_fields = ['memberID', 'first_name', 'last_name', 'email', 'phone', 'address', 'city', 'state', 'zipcode', 'join_date', 'driverID']

    assert data is not None
    for field in expected_fields:
        assert field in data  # assert that the column is in the returned data
        assert data[field] is not None  # assert that the data in the column is indeed not empty

    # logout
    response = client.post('/api/logout', json=member_login_data)
    assert response.status_code == 200


# def test_create_employee(client): -- error prone --
#     # TEST API: /api/employees/create
#     # 401 error crashes randomely
#
#     # login as or superadmin
#
#     super_admin_login_data = {
#         "username": "tsteger0@de.vu",
#         "password": "on9vlvku"
#     }
#     login_response = client.post('/api/login', json=super_admin_login_data) # errors out ahhhhhhhh
#     # time.sleep(1)
#     assert login_response.status_code == 200
#     employee_session_id = login_response.json.get('employee_session_id')
#
#     employee_data = {
#         "first_name": "testEmployee",
#         "last_name": "testEmployee",
#         "email": generateEmail(),
#         "phone": "1234567890",
#         "address": "123 Example St",
#         "city": "Test City",
#         "state": "NJ",
#         "zipcode": "99999",
#         "employeeType": secrets.choice(['Technician', 'Employee']), # why tf we can choice here???
#         "password": "a123",
#         "driverID": generateDriverID(),
#         "SSN": generateSSN()
#     }
#
#     # Sending a POST request to create an employee
#     response = client.post('/api/employees/create', json=employee_data, headers={'employee_session_id': employee_session_id})
#     assert response.status_code == 201
#
#     # verifying that the employee is created in the database
#     created_employee = Employee.query.filter_by(email=employee_data["email"]).first()
#     assert created_employee is not None
#
#     # verifying that the employee's sensitive information is created
#     created_sensitive_info = EmployeeSensitiveInfo.query.filter_by(employeeID=created_employee.employeeID).first()
#     assert created_sensitive_info is not None
#
#     login_response = client.post('/api/logout')
#     assert login_response.status_code == 200


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


def test_get_all_members(client):
    # TEST API: /api/members
    response = client.get('/api/members')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'

    data = response.get_json()
    assert data is not None
    assert isinstance(data, list)

    expected_fields = ['memberID', 'first_name', 'last_name', 'email', 'phone', 'address', 'city', 'state', 'zipcode', 'join_date']
    for member_info in data:
        for key in expected_fields:
            assert key in member_info
            assert member_info[key] is not None


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


def test_service_appointments_get(client):
    response = client.get('/api/service-appointments')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'

    data = response.get_json()
    assert data is not None
    assert isinstance(data, list)
    expected_keys = ['appointment_id', 'memberID', 'VIN_carID', 'serviceID', 'appointment_date', 'comments', 'status', 'last_modified', 'service_name', 'employeeID']

    for service_appt in data:
        for key in expected_keys:
            assert key in service_appt


def test_service_appointments_post(client):
    # TEST API: /api/manager/cancel-service-appointments
    # general test case for when there is a successful cancel value for the session appointments

    manager_login_data = {
        "username": "bprophet3@economist.com",
        "password": "kg8b4mrc"
    }
    login_response = client.post('/api/login', json=manager_login_data)  # errors out ahhhhhhhh
    # time.sleep(3)
    assert login_response.status_code == 200
    employee_session_id = login_response.json.get('employee_session_id')

    data = {'appointment_id': 1}
    response = client.post('/api/manager/cancel-service-appointments', json=data, headers={'employee_session_id': employee_session_id})
    assert response.status_code == 200
    assert response.json == {'message': 'Appointment canceled successfully'}

    # test case for missing appointment_id
    response = client.post('/api/manager/cancel-service-appointments', json={}, headers={'employee_session_id': employee_session_id})
    assert response.status_code == 400
    assert response.json == {'error': 'Appointment_id are required to delete.'}

    # test case for non-existent appointment
    data = {'appointment_id': 999}
    response = client.post('/api/manager/cancel-service-appointments', json=data, headers={'employee_session_id': employee_session_id})
    assert response.status_code == 404
    assert response.json == {'error': 'Appointment not found.'}

    # changes the appointment back to "Scheduled" to continue testing correctly the functionality
    data_reset_service_appointment()
