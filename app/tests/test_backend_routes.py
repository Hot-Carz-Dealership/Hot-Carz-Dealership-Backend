# tests/test_backend_routes.py
# this file contains unit tests for the Non-Financial Backend Endpoints here in this repo in routes.py
# FRONTEND DONT RUN, ITS BUGGY, IT TOOK ME LIKE 4 HRS TO EVEN GET THIS WORKING, WILL FIX LATER AND ADD MORE TEST CASES

import pytest
import string
import random
from app import app, db
from app.models import Cars


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


def test_get_current_user(client):
    response = client.get('/@me')
    assert response.status_code == 401


def test_service_appointments_get(client):
    response = client.get('/api/service-appointments')
    assert response.status_code == 200

# def test_service_appointments_post(client):
#     data = {'appointment_id': 1, 'cancelValue': 1}
#     response = client.post('/api/service-appointments', json=data)
#     assert response.status_code == 200

# def test_logout(client): # test another time and make sure it is actually implemented correctly
#     response = client.post('/api/logout')
#     assert response.status_code == 200
