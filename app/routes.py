# app/routes.py

import random
import logging
from . import app
from .models import *
from sqlalchemy import text
from datetime import datetime
from flask_cors import CORS, cross_origin
from flask import Flask, jsonify, request, session

''' all the NON FINANCIAL route API's here. All Passwords and sensitive information use Bcrypt hash'''


@app.route('/')
def testdb():
    # This API is used to check that ur DB is working locally
    try:
        db.session.query(text('1')).from_statement(text('SELECT 1')).all()
        return '<h1>It works.</h1>'
    except Exception as e:
        # e holds description of the error
        error_text = "<p>The error:<br>" + str(e) + "</p>"
        hed = '<h1>Something is broken.</h1>'
        return hed + error_text


''' this API retrieves all of the add-on products'''


@app.route('/api/vehicles/add-ons', methods=['GET'])
# this GET protocol API is used to return all Add-on products and their information
# TESTCASE: DONE
def addon_information():
    # returns all the information of addon product one is offered when a customer purchases a car
    addons = Addons.query.all()
    addon_info = []
    for addon in addons:
        addon_data = {
            'itemID': addon.itemID,
            'itemName': addon.itemName,
            'totalCost': str(addon.totalCost)  # Converting Decimal to string for JSON serialization
        }
        addon_info.append(addon_data)
    return jsonify(addon_info), 200


@app.route('/api/vehicles/search', methods=['GET'])
# This API returns all information on all vehicles in the database based on a search function in search bar in the frontend
# TESTCASE: DONE
def vehicle_information():
    search_query = request.args.get('search_query')
    if search_query:
        # Query the database for cars matching the search query
        cars_info = db.session.query(Cars).filter(
            db.or_(
                Cars.make.ilike(f'%{search_query}%'),
                Cars.model.ilike(f'%{search_query}%')
            )
        ).all()
    else:
        # If no search query provided, retrieve all vehicles
        cars_info = Cars.query.all()

    # Convert the query result to a list of dictionaries
    cars_info_dicts = [car.__dict__ for car in cars_info]

    # Remove the '_sa_instance_state' key from each dictionary
    for car_dict in cars_info_dicts:
        car_dict.pop('_sa_instance_state', None)
    return jsonify(cars_info_dicts), 200


@app.route('/api/vehicles', methods=['GET'])
# This API returns all information on a specific vehicle based on their VIN number which is passed from the front end to the backend
# TESTCASE: DONE
def vehicle():
    VIN_carID = request.args.get('vin')  # get query parameter id
    vehicle_info = Cars.query.filter_by(VIN_carID=VIN_carID).first()
    if vehicle_info:
        vehicle_info = {
            'VIN_carID': vehicle_info.VIN_carID,
            'make': vehicle_info.make,
            'model': vehicle_info.model,
            'body': vehicle_info.body,
            'year': vehicle_info.year,
            'color': vehicle_info.color,
            'mileage': vehicle_info.mileage,
            'details': vehicle_info.details,
            'description': vehicle_info.description,
            'viewsOnPage': vehicle_info.viewsOnPage,
            'pictureLibraryLink': vehicle_info.pictureLibraryLink,
            'status': vehicle_info.status,
            'price': str(vehicle_info.price)  # Converting Decimal to string for JSON serialization
        }
        return jsonify(vehicle_info), 200
    else:
        return jsonify({'message': 'Vehicle not found'}), 404


@app.route('/api/vehicles/add', methods=['POST']) # need test case
# This API adds a new vehicle to the database based on the information passed from the frontend
# TESTCASE: DONE
def add_vehicle():
    try:
        # no manager auth yet, will add in the future
        data = request.json

        # data that needed to be passed from the frontend
        VIN_carID = data.get('VIN_carID')
        make = data.get('make')
        model = data.get('model')
        body = data.get('body')
        year = data.get('year')
        color = data.get('color')
        mileage = data.get('mileage')
        details = data.get('details')
        description = data.get('description')
        viewsOnPage = data.get('viewsOnPage')
        pictureLibraryLink = data.get('pictureLibraryLink')
        status = data.get('status')
        price = data.get('price')

        # new vehicle record inserted into the DB
        new_vehicle = Cars(
            VIN_carID=VIN_carID,
            make=make,
            model=model,
            body=body,
            year=year,
            color=color,
            mileage=mileage,
            details=details,
            description=description,
            viewsOnPage=viewsOnPage,
            pictureLibraryLink=pictureLibraryLink,
            status=status,
            price=price
        )
        db.session.add(new_vehicle)
        db.session.commit()
        return jsonify({'message': 'Vehicle added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/vehicles/random', methods=['GET'])
# This API returns all info on 2 random vehicles in the database for the homepage
# TESTCASE: DONE
def random_vehicles():
    try:
        # Get the total number of vehicles in the database
        total_vehicles = Cars.query.count()

        # If there are less than 2 vehicles in the database, return an error
        if total_vehicles < 2:
            return jsonify({'error': 'Insufficient vehicles in the database to select random ones.'}), 404

        # Generate two random indices within the range of total vehicles
        random_indices = random.sample(range(total_vehicles), 2)

        # Retrieve information about the two random vehicles
        random_vehicles_info = []
        for index in random_indices:
            random_vehicle = Cars.query.offset(index).first()
            random_vehicle_info = {
                'VIN_carID': random_vehicle.VIN_carID,
                'make': random_vehicle.make,
                'model': random_vehicle.model,
                'body': random_vehicle.body,
                'year': random_vehicle.year,
                'color': random_vehicle.color,
                'mileage': random_vehicle.mileage,
                'details': random_vehicle.details,
                'description': random_vehicle.description,
                'viewsOnPage': random_vehicle.viewsOnPage,
                'pictureLibraryLink': random_vehicle.pictureLibraryLink,
                'status': random_vehicle.status,
                'price': str(random_vehicle.price)
            }
            random_vehicles_info.append(random_vehicle_info)

        return jsonify(random_vehicles_info), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/employees', methods=['GET'])
# This API returns all employees and their information
# TESTCASE: DONE
def get_all_employees():
    employees = Employee.query.all()
    employee_info = []
    for employee in employees:
        employee_data = {
            'employeeID': employee.employeeID,
            'firstname': employee.firstname,
            'lastname': employee.lastname,
            'email': employee.email,
            'phone': employee.phone,
            'address': employee.address,
            'employeeType': employee.employeeType
        }
        employee_info.append(employee_data)
    return jsonify(employee_info), 200


@app.route('/api/testdrives', methods=['GET'])
# THIS ENDPOINT return all testdrive information and joins with the Member and Cars table for better information to view on the manager View
# TESTCASE: DONE
def get_test_drives():
    test_drive_info = []
    test_drives = db.session.query(TestDrive, Member, Cars). \
        join(Member, TestDrive.memberID == Member.memberID). \
        join(Cars, TestDrive.VIN_carID == Cars.VIN_carID).all()

    for test_drive, member, car in test_drives:
        test_drive_info.append({
            'fullname': f"{member.first_name} {member.last_name}",
            'phone': member.phone,
            'car_id': test_drive.VIN_carID,
            'car_make_model': f"{car.make} {car.model}",
            'appointment_date': test_drive.appointment_date
        })
    return jsonify(test_drive_info), 200


@app.route('/api/testdrives/update_confirmation', methods=['POST'])
# this API is POST request used by the manager to Confirm or Deny confirmations
def update_confirmation():
    data = request.json

    # values to be passed from the frontend
    testdrive_id = data.get('testdrive_id')
    confirmation = data.get('confirmation')

    # Check if both parameters are provided
    if testdrive_id is None or confirmation is None:
        return jsonify({'error': 'Both testdrive_id and confirmation parameters are required.'}), 400
    confirmation_value = 'Confirmed' if confirmation == '1' else 'Denied'

    try:
        # revised the work done here to make is follow SQL Alchemy model and rest of codebase
        testdrive = TestDrive.query.get(testdrive_id)
        if testdrive:
            testdrive.confirmation = confirmation_value
            db.session.commit()
            return jsonify({'message': 'Confirmation updated successfully'}), 200
        else:
            return jsonify({'error': 'Test drive not found'}), 404
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/employees/login', methods=['GET', 'POST']) # needs a test case
# This API LOGS in the employee and returns employee information based on their email address and password which is used for auth
def login_employee():
    # Retrieve employee based on email and password
    try:
        data = request.json

        # information needed to be passed by the frontend
        email = data.get('email')
        password = data.get('password')
        employee_data = db.session.query(Employee, EmployeeSensitiveInfo). \
            join(EmployeeSensitiveInfo, Employee.employeeID == EmployeeSensitiveInfo.employeeID). \
            filter(Employee.email == email, EmployeeSensitiveInfo.password == password).first()

        # Check if employee exists
        if employee_data:
            employee, sensitive_info = employee_data
            # ENABLES AND STORES THE SESSIONS FOR THE NEWLY LOGGED IN EMPLPOYEE
            session['employee_session_id'] = employee.employeeID
            # Construct response to return back to view on frontend regarding logged in employee and their information
            response = {
                'employeeID': employee.employeeID,
                'firstname': employee.firstname,
                'lastname': employee.lastname,
                'email': employee.email,
                'phone': employee.phone,
                'address': employee.address,
                'employeeType': employee.employeeType,
            }
            return jsonify(response), 200
        else:
            return jsonify({'message': 'Employee not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/employees/create', methods=['POST'])
# This API creates an employee based on all the values passed from the front to the backend
# TESTCASE: DONE
def create_employee():
    try:
        data = request.json

        # data needed to be passed from the frontend to the backend
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        email = data.get('email')
        phone = data.get('phone')
        address = data.get('address')
        employee_type = data.get('employeeType')
        password = data.get('password')
        driverID = data.get('driverID')
        ssn = data.get('SSN')

        # Create a new employee object/record
        new_employee = Employee(
            firstname=firstname,
            lastname=lastname,
            email=email,
            phone=phone,
            address=address,
            employeeType=employee_type
        )
        db.session.add(new_employee)
        db.session.flush()

        # added a new create EmployeeSensitiveInfo instance and associate it with the employee
        # buggy code dont use im fixing it soon.
        new_sensitive_info = EmployeeSensitiveInfo(
            employeeID=new_employee.employeeID,
            password=password,
            SSN=ssn,
            driverID=driverID,
            lastModified=datetime.now()
        )
        db.session.add(new_sensitive_info)
        db.session.commit()
        return jsonify({'message': 'Employee account created successfully'}), 201
    except Exception as e:
        # Rollback the session in case of any error
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route("/@emp")
# Gets employee for active session
# TESTCASE: DONE
def get_current_employee():
    user_id = session.get("employee_session_id")

    if not user_id:
        return jsonify({"error": "Unauthorized"}), 401

    employee = Employee.query.filter_by(employeeID=user_id).first()
    return jsonify({
        'employeeID': employee.employeeID,
        'firstname': employee.firstname,
        'lastname': employee.lastname,
        'email': employee.email,
        'phone': employee.phone,
        'address': employee.address,
        'employeeType': employee.employeeType,
    }), 200


@app.route('/api/members', methods=['GET'])
# TESTCASE: DONE
def get_all_members():
    # Retrieves all the members and their information
    try:
        # Query all members from the database
        members = Member.query.all()

        # Convert the query result to a list of dictionaries
        members_info = [{'memberID': member.memberID,
                         'first_name': member.first_name,
                         'last_name': member.last_name,
                         'email': member.email,
                         'phone': member.phone,
                         'join_date': member.join_date} for member in members]
        return jsonify(members_info), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@cross_origin
@app.route('/api/members/login', methods=['GET', 'POST'])
# This API is used as Authentication to login a member IF their ACCOUNT EXISTS and
# returns that members information. we need their username and password passed from the front end to the backend to login
# TESTCASE: DONE
def login_member():
    try:
        data = request.json

        # informaton needed to login being sent from front to backend
        username = data.get('username')
        password = data.get('password')

        # Joins to make it happen where the password matches with the MemberSensitiveInfo information for that member
        member_info = db.session.query(Member, MemberSensitiveInfo). \
            join(MemberSensitiveInfo, Member.memberID == MemberSensitiveInfo.memberID). \
            filter(MemberSensitiveInfo.username == username, MemberSensitiveInfo.password == password).first()

        if member_info:
            member, sensitive_info = member_info

            # start the session for the logged member
            session['member_session_id'] = member.memberID 
            return jsonify({
                'memberID': member.memberID,
                'first_name': member.first_name,
                'last_name': member.last_name,
                'email': member.email,
                'phone': member.phone,
                'join_date': member.join_date,
                'SSN': sensitive_info.SSN,
                'driverID': sensitive_info.driverID,
                'cardInfo': sensitive_info.cardInfo
            }), 200
        else:
            return jsonify({'error': 'Member not found or credentials invalid'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# This API creates an employee based on the information passed from the front end to the backend (here)
@app.route('/api/members/create', methods=['POST'])
# TESTCASE: DONE
def create_member():
    try:
        data = request.json

        # Extract data from the request body
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone = data.get('phone')
        driverID = data.get('driverID')
        username = data.get('username')
        password = data.get('password')

        # Create a new Member object
        new_member = Member(first_name=first_name, last_name=last_name, email=email, phone=phone,
                            join_date=datetime.now())

        # Add the new member to the database session
        db.session.add(new_member)
        db.session.commit()

        # Create a new MemberSensitiveInfo object

        # Create a new MemberSensitiveInfo object and associate it with the new member
        new_sensitive_info = MemberSensitiveInfo(sensitiveID=new_member.memberID, memberID=new_member.memberID, 
                                                 username=username, password=password, driverID=driverID)

        # Add the new sensitive info to the database session
        db.session.add(new_sensitive_info)
        db.session.commit()

        # Start a session for the new member for better User experience, LMK if it works
        session['member_session_id'] = new_member.memberID

        # information to return based on the newly created member
        member_info = {
            'memberID': new_member.memberID,
            'first_name': new_member.first_name,
            'last_name': new_member.last_name,
            'email': new_member.email,
            'phone': new_member.phone,
            'join_date': new_member.join_date,
            'username': new_sensitive_info.username
        }
        return jsonify({'message': 'Member account created successfully', 'member_info': member_info}), 201
    except Exception as e:
        # Rollback the session in case of any exception
        db.session.rollback()
        logging.exception(e)
        return jsonify({'error': str(e)}), 500



@app.route("/@me")
# Gets user for active session for Members
def get_current_user():
    user_id = session.get("member_session_id")

    if not user_id:
        user_id = session.get("employee_session_id")
        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401
        employee = Employee.query.filter_by(employeeID=user_id).first()
        return jsonify({
            'employeeID': employee.employeeID,
            'firstname': employee.firstname,
            'lastname': employee.lastname,
            'email': employee.email,
            'phone': employee.phone,
            'address': employee.address,
            'employeeType': employee.employeeType,
        }), 200
    
    member = Member.query.filter_by(memberID=user_id).first()
    sensitive_info = MemberSensitiveInfo.query.filter_by(memberID=user_id).first()  # for returning their Driver ID
    return jsonify({
        'memberID': member.memberID,
        'first_name': member.first_name,
        'last_name': member.last_name,
        'email': member.email,
        'phone': member.phone,
        'driverID': sensitive_info.driverID,
        'join_date': member.join_date
        # in the future will add Address, Zipcode and State on where the member is from
    }), 200


@app.route('/api/service-appointments', methods=['GET', 'POST'])
# GET protocol return all service appointment information
# POST protocol is used for managers to cancel appointments on their views when they are logged in
# TESTCASE: DONE FOR GET AND POST

def service_appointments():
    if request.method == 'GET':
        # get request, we return all data form service appointments
        appointments = ServiceAppointment.query.all()

        appointments_info = [{
            'appointment_id': appointment.appointment_id,
            'memberID': appointment.memberID,
            'appointment_date': appointment.appointment_date,
            'service_name': appointment.service_name
        } for appointment in appointments]

        return jsonify(appointments_info), 200

    elif request.method == 'POST':
        # post request we are deleting the row for service appointments for cancellation
        # takes in 2 values, Appointment ID and a cancellation value. make it a 1
        data = request.json

        # values to be passed from front to backend
        appointment_id_to_cancel = data.get('appointment_id')
        cancellation_value = int(data.get('cancelValue'))

        if appointment_id_to_cancel is None or cancellation_value is None:
            return jsonify({'error': 'Both appointment_id and cancelValue parameters are required.'}), 400

        # cancelation value takes in 1 to confirm it is getting cancelled or else it doesnt get removed.
        if cancellation_value != 1:
            return jsonify({'error': 'Invalid cancellation value.'}), 400

        try:
            # Find the appointment to cancel
            appointment_to_cancel = ServiceAppointment.query.get(appointment_id_to_cancel)

            if appointment_to_cancel is None:
                return jsonify({'error': 'Appointment not found.'}), 404

            # Delete the appointment
            db.session.delete(appointment_to_cancel)
            db.session.commit()

            return jsonify({'message': 'Appointment canceled successfully'}), 200

        except Exception as e:
            return jsonify({'error': str(e)}), 500


@app.route('/api/logout', methods=['POST'])
def logout():
    # THE FRONTEND NEEDS TO REDIRECT WHEN U CALL THIS ENDPOINT BACK TO THE LOGIN SCREEN ON that END.
    # LMK if IT WORKS OR NOT
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200
