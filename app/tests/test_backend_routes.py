# tests/test_backend_routes.py
# this file contains unit tests for the Non-Financial Backend Endpoints here in this repo in routes.py

import pytest
import string
import random
from app import app, db
from app.models import Cars, Member, MemberSensitiveInfo, Employee, EmployeeSensitiveInfo, ServiceAppointment


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        with app.app_context():
            yield client


def generate_random_string():
    characters = string.ascii_uppercase + string.digits
    return ''.join(random.choice(characters) for _ in range(17))


def test_addon_information(client):
    response = client.get('/api/vehicles/add-ons')
    assert response.status_code == 200


def test_vehicle_information(client):
    response = client.get('/api/vehicles/search')
    assert response.status_code == 200


def test_vehicle(client):
    response = client.get('/api/vehicles', query_string={'vin': 'VIN123'})
    assert response.status_code == 404


def test_add_vehicle(client):
    data = {
        'VIN_carID': generate_random_string(),
        'make': 'Toyota',
        'model': 'Camry',
        'body': 'Sedan',
        'year': 2023,
        'color': 'Red',
        'mileage': 10000,
        'details': 'Test Entry',
        'description': 'Test Entry',
        'viewsOnPage': 100,
        'pictureLibraryLink': 'link/to/carpic',
        'status': 'new',
        'price': '20000'
    }
    response = client.post('/api/vehicles/add', json=data)
    assert response.status_code == 201

    # assert that the vehicle was added successfully and the request truly was commited to the DB
    assert Cars.query.filter_by(VIN_carID=data['VIN_carID']).first() is not None

    # manually delete the added vehicle after assertions to not pollute real data
    with app.app_context():
        Cars.query.filter_by(VIN_carID=data['VIN_carID']).delete()
        db.session.commit()


def test_random_vehicles(client):
    response = client.get('/api/vehicles/random')
    assert response.status_code == 200


def test_get_all_employees(client):
    response = client.get('/api/employees')
    assert response.status_code == 200


def test_get_test_drives(client):
    response = client.get('/api/testdrives')
    assert response.status_code == 200


def test_update_confirmation(client):
    data = {'testdrive_id': 1, 'confirmation': '1'}
    response = client.post('/api/testdrives/update_confirmation', json=data)
    assert response.status_code == 200


def test_login_employee(client):
    data = {'email': 'test@example.com', 'password': 'password'}
    response = client.post('/api/employees/login', json=data)
    assert response.status_code == 404


def test_create_employee(client):
    data = {
        'firstname': 'John',
        'lastname': 'Doe',
        'email': 'john@example.com',
        'phone': '1234567890',
        'address': '123 Main St',
        'employeeType': 'Manager'
    }
    response = client.post('/api/employees/create', json=data)
    assert response.status_code == 201


def test_get_current_employee(client):
    response = client.get('/@emp')
        # verifying that the employee's sensitive information is created
        created_sensitive_info = EmployeeSensitiveInfo.query.filter_by(employeeID=created_employee.employeeID).first()
        assert created_sensitive_info is not None

        # rolls back the changes in the database and deletes the test data to not pollute the data we have
        delete_row(created_sensitive_info)
        delete_row(created_employee)


def test_get_current_user():
    # this unit test, tests login Auth to make sure the user can and does indeed login

    # no user Auth
    response = client.get('/@me')
    assert response.status_code == 401


def test_get_all_members(client):
    response = client.get('/api/members')
    assert response.status_code == 200


def test_login_member(client):
    data = {'username': 'testuser', 'password': 'password'}
    response = client.post('/api/members/login', json=data)
    assert response.status_code == 404


# def test_create_member(client): # fix later
#     data = {
#         'first_name': 'Mike',
#         'last_name': 'Joe',
#         'email': 'jane@example.com',
#         'phone': '1234567890',
#         'username': 'janedoe',
#         'password': 'password'
#     }
#     response = client.post('/api/members/create', json=data)
#     assert response.status_code == 201
def test_create_member(client):
    # Define member data for testing
    member_data = {
        "first_name": "testMember",
        "last_name": "testMember",
        "email": "testMember@example.com",
        "phone": "1234567890",
        "username": "testMember_username",
        "password": "password123"
    }

    # Send a POST request to create a member
    response = client.post('/api/members/create', json=member_data)

    # Check if the response status code is 201 (Created)
    assert response.status_code == 201

    # Check if the member and associated sensitive info are created in the database
    with app.app_context():
        created_member = Member.query.filter_by(email=member_data["email"]).first()
        assert created_member is not None

        # Check if the associated sensitive info is also created
        created_sensitive_info = MemberSensitiveInfo.query.filter_by(memberID=created_member.memberID).first()
        assert created_sensitive_info is not None
        assert created_sensitive_info.username == member_data["username"]
        assert created_sensitive_info.password == member_data["password"]

        # Delete the created member and sensitive info from the database
        delete_row(created_sensitive_info)
        delete_row(created_member)


# will test once implemented on the frontend fr
# def test_get_current_user(client):
#     # mock session to imitate an unauthorized user/session, will get to valid session another time
#     response = client.get('/@me')
#     assert response.status_code == 401
#     data = response.get_json()
#     assert 'error' in data
#     assert data['error'] == 'Unauthorized'


def test_service_appointments_get(client):
    response = client.get('/api/service-appointments')
    assert response.status_code == 200
    assert response.headers['Content-Type'] == 'application/json'

    data = response.get_json()
    assert isinstance(data, list)
    expected_keys = ['appointment_id', 'memberID', 'appointment_date', 'service_name']

    for service_appt in data:
        for key in expected_keys:
            assert key in service_appt


def test_service_appointments_post(client):
    # general test case for when there is a successful cancel value for the session appointments
    data = {'appointment_id': 1, 'cancelValue': 1}
    response = client.post('/api/service-appointments', json=data)
    assert response.status_code == 200
    assert response.json == {'message': 'Appointment canceled successfully'}

    # test case for when there are missing parameters
    data_missing_params = {'cancelValue': 1}
    response_missing_params = client.post('/api/service-appointments', json=data_missing_params)
    assert response_missing_params.status_code == 400
    assert response_missing_params.json == {'error': 'Both appointment_id and cancelValue parameters are required.'}

    # test case for when there is an invalid cancellation value
    data_invalid_cancel_value = {'appointment_id': 1, 'cancelValue': 0}
    response_invalid_cancel_value = client.post('/api/service-appointments', json=data_invalid_cancel_value)
    assert response_invalid_cancel_value.status_code == 400
    assert response_invalid_cancel_value.json == {'error': 'Invalid cancellation value.'}

    # test case for when a service appointment is not found
    data_appointment_not_found = {'appointment_id': 999, 'cancelValue': 1}
    response_appointment_not_found = client.post('/api/service-appointments', json=data_appointment_not_found)
    assert response_appointment_not_found.status_code == 404
    assert response_appointment_not_found.json == {'error': 'Appointment not found.'}

    datereset_service_appointment()


def datereset_service_appointment():
    # function used to reset the data we used back to how it was in the DB
    insertData = ServiceAppointment(
        appointment_id=1,
        memberID=1,
        appointment_date='2024-04-10 14:00:00',
        service_name='Oil Change'
    )
    db.session.add(insertData)
    db.session.commit()
