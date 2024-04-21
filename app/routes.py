# app/routes.py

import re
import bcrypt
import random
import logging
from . import app
import sqlalchemy.sql
from .models import *
from sqlalchemy import text
from datetime import datetime, timedelta
from flask import jsonify, request, session


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


@app.route('/api/vehicles/add-ons', methods=['GET'])  # test ready
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


@app.route('/api/vehicles/search', methods=['GET'])  # test ready
# This API returns all information on all vehicles in the database based on a search function in search bar in the frontend
# TESTCASE: DONE
def vehicle_information():
    search_query = request.args.get('search_query')
    if search_query:
        # match only with cars that are from only the dealership and return them
        cars_info = db.session.query(CarInfo).join(CarVINs).filter(
            CarVINs.purchase_status == 'Dealership - Not Purchased',
            db.or_(
                CarInfo.make.ilike(f'%{search_query}%'),
                CarInfo.model.ilike(f'%{search_query}%')
            )
        ).all()
    else:
        # If no search query provided, retrieve all vehicles
        # ---- fix it to return only based on vehicles in dealership not sold -------
        cars_info = CarInfo.query.join(CarVINs).filter(
            CarVINs.purchase_status == 'Dealership - Not Purchased'
        ).all()

    # Convert the query result to a list of dictionaries
    cars_info_dicts = [car.__dict__ for car in cars_info]

    # Remove the '_sa_instance_state' key from each dictionary
    for car_dict in cars_info_dicts:
        car_dict.pop('_sa_instance_state', None)
    return jsonify(cars_info_dicts), 200


# insane im gonna go insane i have to now modify it where we also grab and can connect certain user inserted vehicles to their own cars
'''make an API to return cars to specfic people based on their memberID'''


@app.route('/api/vehicles', methods=['GET'])  # test ready
# This API returns all information on a specific vehicle based on their VIN number which is passed from the front end to the backend
# Which have not been purchased ofc
# was prev: /api/vehicles
# TESTCASE: DONE
def vehicle():
    VIN_carID = request.args.get('vin')  # get query parameter id
    vehicle_info = CarInfo.query.join(CarVINs).filter(CarVINs.VIN_carID == VIN_carID,
                                                      CarVINs.purchase_status == 'Dealership - Not Purchased').first()  # used to ensure that the cars shown are from the Dealership only and now customer private owned
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


@app.route('/api/vehicles/add', methods=['POST'])  # test ready
# This API adds a new vehicle to the database based on the information passed from the frontend
# TESTCASE: DONE
def add_vehicle():
    try:
        # ONLY MANAGERS/SUPERADMINS USE THIS NOT MEMBERS
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
        # status = data.get('status')
        price = data.get('price')

        # check if there are any duplicates before inserting
        existing_vin = CarVINs.query.filter_by(VIN_carID=VIN_carID).first()
        if existing_vin:
            return jsonify({'error': 'Vehicle with VIN already exists'}), 400

        # Create new CarVINs record
        new_vin = CarVINs(VIN_carID=VIN_carID,
                          purchase_status='Dealership - Not Purchased',
                          memberID=sqlalchemy.sql.null())
        db.session.add(new_vin)
        db.session.flush()

        # Create new CarInfo record
        new_vehicle = CarInfo(
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
            status='new',
            price=price
        )
        db.session.add(new_vehicle)
        db.session.commit()
        return jsonify({'message': 'Vehicle added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/vehicles/random', methods=['GET'])  # test ready
# This API returns all info on 2 random vehicles in the database for the homepage
# TESTCASE: DONE
def random_vehicles():
    try:
        # Get the total number of vehicles in the database from 'Dealership'
        total_vehicles = CarInfo.query.join(CarVINs).filter(
            CarVINs.purchase_status == 'Dealership - Not Purchased').count()

        # If there are less than 2 vehicles in the database from 'Dealership', return an error
        if total_vehicles < 2:
            return jsonify({'error': 'Insufficient vehicles in the dealership to select random ones.'}), 404

        # Generate two random indices within the range of total vehicles
        random_indices = random.sample(range(total_vehicles), 2)

        # Retrieve information about the two random vehicles
        random_vehicles_info = []
        for index in random_indices:
            random_vehicle = CarInfo.query.join(CarVINs).filter(
                CarVINs.purchase_status == 'Dealership - Not Purchased').offset(
                index).first()
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
        return jsonify({'error': str(e)}), 5000


@app.route('/api/employees', methods=['GET'])  # test ready
# This API returns all employees and their information
# TESTCASE: DONE
def get_all_employees():
    employees = Employee.query.all()
    employee_info = []
    for employee in employees:
        employee_data = {
            'employeeID': employee.employeeID,
            'first_name': employee.first_name,
            'last_name': employee.last_name,
            'email': employee.email,
            'phone': employee.phone,
            'address': employee.address,
            'city': employee.city,
            'state': employee.state,
            'zipcode': employee.zipcode,
            'employeeType': employee.employeeType
        }
        employee_info.append(employee_data)
    return jsonify(employee_info), 200


@app.route('/api/testdrives', methods=['GET'])  # test ready
# THIS ENDPOINT return all testdrive information and joins with the Member and Cars table for better information to view on the manager View
# TESTCASE: DONE
def get_test_drives():
    test_drive_info = []
    test_drives = db.session.query(TestDrive, Member, CarInfo). \
        join(Member, TestDrive.memberID == Member.memberID). \
        join(CarInfo, TestDrive.VIN_carID == CarInfo.VIN_carID).all()

    for test_drive, member, car in test_drives:
        test_drive_info.append({
            'fullname': f"{member.first_name} {member.last_name}",
            'phone': member.phone,
            'car_id': test_drive.VIN_carID,
            'car_make_model': f"{car.make} {car.model}",
            'appointment_date': test_drive.appointment_date
        })
    return jsonify(test_drive_info), 200


@app.route('/api/testdrives/update_confirmation', methods=['POST'])  # test ready
# this API is POST request used by the manager to Confirm or Deny confirmations
def update_confirmation():
    data = request.json

    # values to be passed from the frontend
    testdrive_id = data.get('testdrive_id')
    confirmation = int(data.get('confirmation'))

    # Check if both parameters are provided
    if testdrive_id is None or confirmation is None:
        return jsonify({'error': 'Both testdrive_id and confirmation parameters are required.'}), 400

    if confirmation == 1:
        confirmation_value = 'Confirmed'
    elif confirmation == 2:
        confirmation_value = 'Denied'
    elif confirmation == 3:
        confirmation_value = 'Cancelled'
    else:
        confirmation_value = 'Awaiting Confirmation'

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


# #Commented out for now since we have combined login for member and employee
# # depricated | delete later when know for sure won't be used and have a viable solution
# @app.route('/api/employees/login', methods=['GET', 'POST'])  # needs a test case
# # This API LOGS in the employee and returns employee information based on their email address and password which is used for auth
# def login_employee():
#     # Retrieve employee based on email and password
#     try:
#         data = request.json

#         # information needed to be passed by the frontend
#         email = data.get('email')
#         password = data.get('password')
#         employee_data = db.session.query(Employee, EmployeeSensitiveInfo). \
#             join(EmployeeSensitiveInfo, Employee.employeeID == EmployeeSensitiveInfo.employeeID). \
#             filter(Employee.email == email, EmployeeSensitiveInfo.password == password).first()

#         # Check if employee exists
#         if employee_data:
#             employee, sensitive_info = employee_data
#             # ENABLES AND STORES THE SESSIONS FOR THE NEWLY LOGGED IN EMPLPOYEE
#             session['employee_session_id'] = employee.employeeID
#             # Construct response to return back to view on frontend regarding logged in employee and their information
#             response = {
#                 'employeeID': employee.employeeID,
#                 'firstname': employee.firstname,
#                 'lastname': employee.lastname,
#                 'email': employee.email,
#                 'phone': employee.phone,
#                 'address': employee.address,
#                 'employeeType': employee.employeeType,
#             }
#             return jsonify(response), 200
#         else:
#             return jsonify({'message': 'Employee not found'}), 404
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


# This API creates an employee based on all the values passed from the front to the backend
@app.route('/api/employees/create', methods=['POST'])  # test ready
def create_employee():
    try:
        # # Check if employee is authenticated
        employee_id = session.get('employee_session_id')
        if employee_id is None:
            return jsonify({'message': 'Unauthorized access'}), 401

        # Check if authenticated employee is a super admin
        super_admin = Employee.query.get(employee_id)
        if not super_admin or super_admin.employeeType != 'superAdmin':
            return jsonify({'message': 'Only SuperAdmins can create employee accounts'}), 403

        data = request.json
        # Data needed to be passed from the frontend to the backend
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone = data.get('phone')
        address = data.get('address')
        city = data.get('city')
        zipcode = data.get('zipcode')
        # for state, it will all be in NJ
        employee_type = data.get('employeeType')
        password = data.get('password')  # Ensure password is retrieved as bytes
        driverID = data.get('driverID')
        ssn = data.get('SSN')

        # Check if email already exists, we cannot have duplicate employees
        if Employee.query.filter_by(email=email).first():
            return jsonify({'message': 'Email already exists'}), 400

        # Ensure that superAdmins can only create Manager or Technician accounts
        if employee_type not in ['Manager', 'Technician']:
            return jsonify({'message': 'Only Manager or Technician accounts can be created by SuperAdmins'}), 400

        # Hash the password
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        hashed_ssn = bcrypt.hashpw(ssn.encode('utf-8'), bcrypt.gensalt())

        # Create a new employee object/record
        new_employee = Employee(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            state='NJ',
            zipcode=zipcode,
            employeeType=employee_type
        )
        db.session.add(new_employee)
        db.session.flush()

        # Create a new EmployeeSensitiveInfo instance and associate it with the employee
        new_sensitive_info = EmployeeSensitiveInfo(
            employeeID=new_employee.employeeID,
            password=hashed_password,
            SSN=hashed_ssn,
            driverID=driverID,
            lastModified=datetime.now()
        )
        db.session.add(new_sensitive_info)
        db.session.commit()

        return jsonify({'message': 'Employee account created successfully'}), 201
    except Exception as e:
        # Rollback the session in case of any error
        db.session.rollback()
        return jsonify({'error': 'An error occurred while creating the employee account.'}), 500


@app.route('/api/employees/technicians', methods=['GET'])  # test ready
# this API is used to return all technicians in the DB from employees table
def get_technicians():
    # retrieve all technicians from the database
    technicians = Employee.query.filter_by(employeeType='Technician').all()
    technicians_data = []
    for technician in technicians:
        technician_data = {
            'employeeID': technician.employeeID,
            'first_name': technician.first_name,
            'last_name': technician.last_name,
            'email': technician.email,
            'phone': technician.phone,
            'address': technician.address,
            'city': technician.city,
            'state': technician.state,
            'zipcode': technician.zipcode,
            'employeeType': technician.employeeType
        }
        technicians_data.append(technician_data)
    return jsonify(technicians_data), 200


# depricated | delete later when know for sure won't be used and have a viable solution
# @app.route("/@emp")
# # Gets employee for active session
# def get_current_employee():
#     user_id = session.get("employee_session_id")
#
#     if not user_id:
#         return jsonify({"error": "Unauthorized"}), 401
#
#     employee = Employee.query.filter_by(employeeID=user_id).first()
#     return jsonify({
#         'employeeID': employee.employeeID,
#         'firstname': employee.firstname,
#         'lastname': employee.lastname,
#         'email': employee.email,
#         'phone': employee.phone,
#         'address': employee.address,
#         'employeeType': employee.employeeType,
#     }), 200


@app.route('/api/members', methods=['GET'])  # test ready
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
                         'address': member.address,
                         'state': member.state,
                         'zipcode': member.zipcode,
                         'join_date': member.join_date} for member in members]
        return jsonify(members_info), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# Commented out for now since we have combined login for member and employee
# depricated | delete later when know for sure won't be used and have a viable solution

# @cross_origin
# @app.route('/api/members/login', methods=['GET', 'POST'])
# # This API is used as Authentication to login a member IF their ACCOUNT EXISTS and
# # returns that members information. we need their username and password passed from the front end to the backend to login
# # TESTCASE: DONE
# def login_member():
#     try:
#         data = request.json

#         # informaton needed to login being sent from front to backend
#         username = data.get('username')
#         password = data.get('password')

#         # Joins to make it happen where the password matches with the MemberSensitiveInfo information for that member
#         member_info = db.session.query(Member, MemberSensitiveInfo). \
#             join(MemberSensitiveInfo, Member.memberID == MemberSensitiveInfo.memberID). \
#             filter(MemberSensitiveInfo.username == username, MemberSensitiveInfo.password == password).first()

#         if member_info:
#             member, sensitive_info = member_info

#             # start the session for the logged member
#             session['member_session_id'] = member.memberID
#             return jsonify({
#                 'memberID': member.memberID,
#                 'first_name': member.first_name,
#                 'last_name': member.last_name,
#                 'email': member.email,
#                 'phone': member.phone,
#                 'join_date': member.join_date,
#                 'SSN': sensitive_info.SSN,
#                 'driverID': sensitive_info.driverID,
#                 'cardInfo': sensitive_info.cardInfo
#             }), 200
#         else:
#             return jsonify({'error': 'Member not found or credentials invalid'}), 404
#     except Exception as e:
#         return jsonify({'error': str(e)}), 500


# This API creates a member account based on the information passed from the front end to the backend (here)
@app.route('/api/members/create', methods=['POST'])  # test ready
def create_member():
    try:
        data = request.json

        # data to be passed from the frontend to the backend
        # members cannot have the same username & driverID as others
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone = data.get('phone')
        driverID = data.get('driverID')
        username = data.get('username')
        password = data.get('password')
        address = data.get('address')
        city = data.get('city')
        state = data.get('state')
        zipcode = data.get('zipcode')

        # Password hash
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

        # new member insert
        new_member = Member(
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone=phone,
            address=address,
            city=city,
            state=state,
            zipcode=zipcode,
            join_date=datetime.now()
        )
        db.session.add(new_member)
        db.session.flush()  # Allows accessing the memberID before committing all changes

        # create a new MemberSensitiveInfo object and associate it with the new member
        new_sensitive_info = MemberSensitiveInfo(
            memberID=new_member.memberID,
            username=username,
            password=hashed_password,
            # SSN=", leave this commented it out, its unique so NULL is automatic my sql rules in commits
            driverID=driverID
        )
        db.session.add(new_sensitive_info)
        db.session.commit()

        # starts a session for the new member for better User experience
        session['member_session_id'] = new_member.memberID

        # Information to return based on the newly created member
        member_info = {
            'memberID': new_member.memberID,
            'first_name': new_member.first_name,
            'last_name': new_member.last_name,
            'email': new_member.email,
            'phone': new_member.phone,
            'address': new_member.address,
            'state': new_member.state,
            'zipcode': new_member.zipcode,
            'join_date': new_member.join_date,
            'username': new_sensitive_info.username
        }
        return jsonify({'message': 'Member account created successfully', 'member_info': member_info}), 201
    except Exception as e:
        # Rollback the session in case of any exception
        db.session.rollback()
        logging.exception(e)  # Log the exception for debugging purposes
        return jsonify({'error': 'An error occurred while creating the member account.'}), 500


@app.route('/api/member/add-own-car', methods=['POST'])  # test ready
# this API is used for members to be able to add their own cars into the DB, mainly for service center actions
def add_car():
    member_id = session.get('member_session_id')
    if not member_id:
        return jsonify({'message': 'Unauthorized access'}), 401

    # Ensure that the employee is a member
    member = Member.query.filter_by(memberID=member_id).first()
    if member is None:
        return jsonify({'message': 'You are not a signed up member at this Dealership'}), 401

    try:
        data = request.json

        # data to be passed from the frontend from the customer inputs
        vin = data.get('VIN_carID')
        make = data.get('make')
        model = data.get('model')
        body = data.get('body')
        year = data.get('year')
        color = data.get('color')
        mileage = data.get('mileage')

        # we dont need these values to be passed because its just a user added car for car services.
        # we just need basic details of the car
        # details = data.get('details')
        # description = data.get('description')
        # viewsOnPage = data.get('viewsOnPage')
        # pictureLibraryLink = data.get('pictureLibraryLink')
        # status = data.get('status')
        # price = data.get('price')

        # Extract other fields as needed

        # check to make sure that there are no other cars with matching VIN
        existing_vin = CarVINs.query.filter_by(VIN_carID=vin).first()
        if existing_vin:
            return jsonify({'message': 'VIN/Car already exists in the database'}), 400

        # Create new CarVINs record
        new_vin_record = CarVINs(VIN_carID=vin,
                                 purchase_status='Outside Dealership',
                                 memberID=member_id
                                 )
        db.session.add(new_vin_record)
        db.session.flush()

        # Create new CarInfo record
        new_carInfo_record = CarInfo(
            VIN_carID=vin,
            make=make,
            model=model,
            body=body,
            year=year,
            color=color,
            mileage=mileage,
            status='Outside Dealership',
            price=0
        )
        db.session.add(new_carInfo_record)
        db.session.commit()
        return jsonify({'message': 'Car added successfully'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': 'Error adding car to the database'}), 500


@app.route("/@me")  # test ready
# Gets user for active session for Members
def get_current_user():
    user_id = session.get("member_session_id")

    # if it is none, basically we then begin the login for employees and NOT members here.
    # all in one endpoint, thx patrick. This data belongs to him but it's under my commit because I fucked up.
    if not user_id:
        user_id = session.get("employee_session_id")

        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401
        employee = Employee.query.filter_by(employeeID=user_id).first()
        return jsonify({
            'employeeID': employee.employeeID,
            'first_name': employee.first_name,
            'last_name': employee.last_name,
            'email': employee.email,
            'phone': employee.phone,
            'address': employee.address,
            'city': employee.city,
            'state': employee.state,
            'zipcode': employee.zipcode,
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
        'address': member.address,
        'city': member.city,
        'state': member.state,
        'zipcode': member.zipcode,
        'driverID': sensitive_info.driverID,
        'join_date': member.join_date
    }), 200


@app.route('/api/service-appointments', methods=['GET'])  # test ready
# GET protocol return all service appointment information
# POST protocol is used for managers to cancel appointments on their views when they are logged in
# TESTCASE: DONE FOR GET AND POST
def service_appointments():
    # get request, we return all data form service appointments
    appointments = ServiceAppointment.query.all()

    appointments_info = [{
        'appointment_id': appointment.appointment_id,
        'memberID': appointment.memberID,
        'VIN_carID': appointment.VIN_carID,
        'serviceID': appointment.serviceID,
        'appointment_date': appointment.appointment_date,
        'comments': appointment.comments,
        'status': appointment.status,
        'last_modified': appointment.last_modified
    } for appointment in appointments]
    return jsonify(appointments_info), 200


@app.route('/api/manager/cancel-service-appointments', methods=['POST'])  # test ready
# this api used to be a part of the /api/service-appointments but i moved it here for better separation
# was delete, now is post. We shouldn't delete service appointments but instead just store them in case we need information on it
# to view
def delete_service_appointment():
    # ensures that the manager or superAdmin is logged in
    employee_id = session.get('employee_session_id')
    if not employee_id:
        return jsonify({'message': 'Unauthorized access'}), 401

    # Ensure that the employee exists
    employee = Employee.query.filter_by(employeeID=employee_id).first()
    if employee is None:
        return jsonify({'message': 'Employee is not in the System'}), 401

    try:
        data = request.json
        appointment_id_to_cancel = data.get('appointment_id')

        if appointment_id_to_cancel is None:
            return jsonify({'error': 'Appointment_id are required to delete.'}), 400

        # Find the appointment to cancel
        appointment_to_cancel = ServiceAppointment.query.get(appointment_id_to_cancel)
        if appointment_to_cancel is None:
            return jsonify({'error': 'Appointment not found.'}), 404

        appointment_to_cancel.status = 'Cancelled'
        db.session.commit()
        return jsonify({'message': 'Appointment canceled successfully'}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/member/book-service-appointment', methods=['POST'])  # test ready
# NEW API: this API allows for customer to book a service appointment based on cars bought from the dealership
def book_service_appointment():
    # check if the member is logged in, if not redirect them to log in
    member_id = session.get('member_session_id')
    if not member_id:
        return jsonify({'message': 'Unauthorized access. Please log in.'}), 401

    # check if the member exists
    member = Member.query.get(member_id)
    if not member:
        return jsonify({'message': 'Member not found'}), 404

    data = request.json

    # data that needs to be sent from the frontend to the backend here
    appointment_date = data.get('appointment_date')
    serviceID = data.get('serviceID')  # needed for the customer to choose what service they want on their car
    VIN_carID = data.get('VIN_carID')

    # we filter the vehicle to match with the memberID and carVIN to exist and match
    vehicle = CarVINs.query.filter_by(VIN_carID=VIN_carID).filter(CarVINs.memberID == member_id).first()
    if not vehicle:
        return jsonify({
            'message': 'Vehicle is not associated with the Member for them to be able to make a service appt. for it.'}), 400

    appointment_date = datetime.strptime(appointment_date, '%Y-%m-%d %H:%M:%S')
    if appointment_date <= datetime.now():
        return jsonify({'message': 'Appointment date must be after today'}), 400

    # Check if required data is provided
    if not VIN_carID or not appointment_date or not serviceID:
        return jsonify({'message': 'Car VIN ID, appointment date, and serviceID name are required'}), 400

    # Create a new service appointment
    appointment = ServiceAppointment(
        memberID=member_id,
        VIN_carID=VIN_carID,
        serviceID=serviceID,
        appointment_date=appointment_date,
        status='Scheduled',
        last_modified=datetime.now()
    )
    db.session.add(appointment)
    db.session.commit()

    return jsonify({'message': 'Service appointment booked successfully'}), 201


@app.route('/api/service-menu', methods=['GET'])  # test ready
# this api i hate it, it made me make another table and have to refactor everything.
# returns all values in the Services table for users to choose what services they want.
def get_services():
    if request.method == 'GET':
        try:
            services = Services.query.all()
            services_info = [{
                'serviceID': service.serviceID,
                'service_name': service.service_name
            } for service in services]
            return jsonify(services_info), 200
        except Exception as e:
            return jsonify({'error': str(e)}), 500


@app.route('/api/manager/edit-service-menu', methods=['POST', 'DELETE'])  # test ready
def edit_service_menu():
    # ensures that the manager or superAdmin is logged in
    employee_id = session.get('employee_session_id')
    if not employee_id:
        return jsonify({'message': 'Unauthorized access'}), 401

    # Ensure that the employee is a Manager
    employee = Employee.query.filter_by(employeeID=employee_id).first()
    if employee.employeeType not in ['Manager', 'superAdmin']:
        return jsonify({'message': 'Unauthorized access'}), 401

    # Only managers or superAdmins are allowed to access this endpoint from this point onward

    if request.method == 'POST':
        # here we want to make a new service
        try:
            data = request.json
            service_name = data.get('service_name')
            if service_name is None:
                return jsonify({'message': 'Service name is required'}), 400

            new_service = Services(service_name=service_name)
            db.session.add(new_service)
            db.session.commit()
            return jsonify({'message': 'Service added successfully'}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500
    elif request.method == 'DELETE':  # why doesnt delete protocol work???
        try:
            data = request.json
            service_id = data.get('service_id')

            # lots of relationships here to deal with
            # first, i have to delete the associated records from ServiceAppointmentEmployeeAssignments
            appointments = ServiceAppointment.query.filter_by(serviceID=service_id).all()
            for appointment in appointments:
                ServiceAppointmentEmployeeAssignments.query.filter_by(
                    appointment_id=appointment.appointment_id).delete()

            # next, don't delete but only change the status and serviceID in the associated records from ServiceAppointment
            appts = ServiceAppointment.query.filter_by(serviceID=service_id).all()
            for app in appts:
                app.status = 'Cancelled'
                app.serviceID = sqlalchemy.sql.null()

            # last, actually delete the service from Services table
            service = Services.query.filter_by(serviceID=service_id).first()
            if service:
                db.session.delete(service)
                db.session.commit()
                return jsonify({'message': 'Service deleted successfully'}), 200
            else:
                return jsonify({'message': 'Service not found'}), 404
        except Exception as e:
            db.session.rollback()
            return jsonify({'error': str(e)}), 500


@app.route('/api/manager/assign-service-appointments', methods=['POST'])  # test ready
def assign_service_appointments():
    # Check if the user is logged in and is a manager/superAdmin
    employee_session_id = session.get('employee_session_id')
    if not employee_session_id:
        return jsonify({'message': 'Unauthorized access'}), 401

    employee = Employee.query.get(employee_session_id)
    if not employee or employee.employeeType not in ['Manager', 'superAdmin']:
        return jsonify({'message': 'Unauthorized access'}), 403

    data = request.json

    # frontend needs to send these values to here for this to work
    appointment_id = data.get('appointment_id')
    employee_id = data.get('employee_id')

    # check if appointment_id and technician_id are provided
    if not appointment_id or not employee_id:
        return jsonify({'message': 'Appointment ID and technician ID are required'}), 400

    # check if the appointment exists
    appointment = ServiceAppointment.query.get(appointment_id)
    if not appointment:
        return jsonify({'message': 'Appointment not found'}), 404

    # check if the technician exists and is a Technician
    technician = Employee.query.filter_by(employeeID=employee_id, employeeType='Technician').first()
    if not technician:
        return jsonify({'message': 'Technician not found or not a valid Technician'}), 404

    # functionality here works where if the serviceAssignment is already assigned, we just assign it to another technician
    # if there is no one assigned to the serviceAppointment, then we just assign a technician to it and add a new row of data
    # ServiceAppointmentEmployeeAssignments table
    assignment = ServiceAppointmentEmployeeAssignments.query.get(appointment_id)
    if assignment:
        assignment.employeeID = employee_id
    else:
        # assign the appointment to the technician
        assignment = ServiceAppointmentEmployeeAssignments(appointment_id=appointment_id, employeeID=employee_id)

    db.session.add(assignment)
    db.session.commit()
    return jsonify({'message': 'Appointment assigned successfully'}), 200


@app.route('/api/technician-view-service-appointments', methods=['GET'])  # test ready
# --- NEW API ---
# this API is used for technicians to view their service appointment
def technician_view_service_appointments():
    # checks if user is logged in
    employee_id = session.get('employee_session_id')
    if not employee_id:
        return jsonify({'message': 'Unauthorized access'}), 401

    # ensures that the employee is a Technician
    employee = Employee.query.filter_by(employeeID=employee_id, employeeType='Technician').first()
    if not employee:
        return jsonify({'message': 'This employee is not a technician'}), 401

    # wow
    # here we query all the technician appointments up and if they are Done, they are still to be shown the technician
    # until 1 full day has passed. The service appointment that occured is still stored in the DB but we just no longer display it
    # to the technician
    appointments = db.session.query(ServiceAppointment, Services.service_name) \
        .join(ServiceAppointmentEmployeeAssignments,
              ServiceAppointment.appointment_id == ServiceAppointmentEmployeeAssignments.appointment_id) \
        .join(Services, ServiceAppointment.serviceID == Services.serviceID) \
        .filter(ServiceAppointmentEmployeeAssignments.employeeID == employee_id) \
        .filter(ServiceAppointment.status.in_(['Scheduled', 'Done'])) \
        .filter(((ServiceAppointment.last_modified >= datetime.now() - timedelta(days=1)) & (
            ServiceAppointment.status == 'Done')) | (ServiceAppointment.status != 'Done')).all()

    # Serialize appointments and return response
    appointments_data = []
    for appointment, service_name in appointments:
        appointment_data = {
            'appointment_id': appointment.appointment_id,
            'memberID': appointment.memberID,
            'VIN_carID': appointment.VIN_carID,
            'service_name': service_name,
            'appointment_date': appointment.appointment_date,
            'comments': appointment.comments,
            'status': appointment.status,
            'last_modified': appointment.last_modified
            if appointment.last_modified else None
        }
        appointments_data.append(appointment_data)
    return jsonify(appointments_data), 200


@app.route('/api/technician-view-service-appointments/technician-edit', methods=['POST'])  # test ready
def technician_edit():
    # checks if user is logged in
    employee_id = session.get('employee_session_id')
    if not employee_id:
        return jsonify({'message': 'Unauthorized access'}), 401

    # ensures that the employee is a Technician
    employee = Employee.query.filter_by(employeeID=employee_id, employeeType='Technician').first()
    if not employee:
        return jsonify({'message': 'Unauthorized access'}), 401

    # Retrieve data from the frontend
    data = request.json
    appointment_id = data.get('appointment_id')
    comment = data.get('comment')
    status = data.get('status')

    # check to make sure the appointment_id is provided
    if not appointment_id:
        return jsonify({'message': 'Appointment ID is required'}), 400

    # check if appointment exists
    appointment = ServiceAppointment.query.get(appointment_id)
    if not appointment:
        return jsonify({'message': 'Appointment not found'}), 404

    # ensure that the appointment is assigned to the technician to the signed in technician
    appointment_assignment = ServiceAppointmentEmployeeAssignments.query.filter_by(
        appointment_id=appointment_id, employeeID=employee_id).first()
    if not appointment_assignment:
        return jsonify({'message': 'You are not assigned to this appointment'}), 403

    # technicians can update the appointment details
    if comment:
        appointment.comments = comment

    # technicians can update the appointment status
    if status == 'Done':
        appointment.status = 'Done'
    elif status == 'Cancelled':
        appointment.status = 'Cancelled'
    elif status == 'Scheduled':
        appointment.status = 'Scheduled'
    else:
        return jsonify({'message': 'Invalid Status to Issue Service Appointment'}), 403

    db.session.commit()
    return jsonify({'message': 'Appointment updated successfully'}), 200


@app.route('/api/logout', methods=['POST'])  # test ready
def logout():
    # THE FRONTEND NEEDS TO REDIRECT WHEN U CALL THIS ENDPOINT BACK TO THE LOGIN SCREEN ON that END.
    # LMK if IT WORKS OR NOT
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200


# Route for user authentication
@app.route('/api/login', methods=['POST'])  # test ready
def login():
    re_string = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    try:
        data = request.json
        username = data.get('username')

        # the basis on this check is to better ensure who we are checking for when logging in
        # Emails = employees
        # regular Text = members
        if re.search(re_string, username) is None:
            # username is not an email, we check for member logging in

            # checks if the provided data belongs to a member
            # 'username' parameter is used interchangeably with email for employee and username for member
            password = data.get('password').encode('utf-8')

            # if none, then there is no username associated with the account
            member_match_username = db.session.query(MemberSensitiveInfo).filter(
                MemberSensitiveInfo.username == username).first()

            if member_match_username is None:
                return jsonify({'error': 'Invalid username or password.'}), 401

            stored_hash = member_match_username.password.encode('utf-8')

            # Check if password matches
            if bcrypt.checkpw(password, stored_hash):
                member_info = db.session.query(Member, MemberSensitiveInfo). \
                    join(MemberSensitiveInfo, Member.memberID == MemberSensitiveInfo.memberID). \
                    filter(MemberSensitiveInfo.username == username).first()

                if member_info:
                    member, sensitive_info = member_info
                    session['member_session_id'] = member.memberID

                    # just in case because the member create doesn't force them to enter a SSN, so if nothign returns from the DB,
                    # better to have a text to show on the frontend then just nothing.
                    return jsonify({
                        'type': 'member',
                        'memberID': member.memberID,
                        'first_name': member.first_name,
                        'last_name': member.last_name,
                        'email': member.email,
                        'phone': member.phone,
                        'address': member.address,
                        'city': member.city,
                        'state': member.state,
                        'zipcode': member.zipcode,
                        'join_date': member.join_date,
                        # 'SSN': sensitive_info.SSN, -- we can't really return the ssn because its all encrypted for usage only meant for storing.
                        'driverID': sensitive_info.driverID
                    }), 200
            else:
                return jsonify({'error': 'Invalid username or password.'}), 401
        else:
            # the username is an email, we check for employee logging in

            email = username
            password = data.get('password').encode('utf-8')

            # if none, then there is no username associated with the account
            sensitive_info_username_match = db.session.query(EmployeeSensitiveInfo). \
                join(Employee, Employee.employeeID == EmployeeSensitiveInfo.employeeID). \
                filter(Employee.email == email).first()

            if sensitive_info_username_match is None:
                return jsonify({'error': 'Invalid username or password.'}), 401

            stored_hash = sensitive_info_username_match.password.encode('utf-8')
            # Check if password matches
            if bcrypt.checkpw(password, stored_hash):
                employee_data = db.session.query(Employee, EmployeeSensitiveInfo). \
                    join(EmployeeSensitiveInfo, Employee.employeeID == EmployeeSensitiveInfo.employeeID). \
                    filter(Employee.email == email).first()

                if employee_data:
                    employee, sensitive_info = employee_data
                    session['employee_session_id'] = employee.employeeID
                    response = {
                        'employeeID': employee.employeeID,
                        'first_name': employee.first_name,
                        'last_name': employee.last_name,
                        'email': employee.email,
                        'phone': employee.phone,
                        'address': employee.address,
                        'city': employee.city,
                        'state': employee.state,
                        'zipcode': employee.zipcode,
                        'employeeType': employee.employeeType,
                    }
                    return jsonify(response), 200
            else:
                return jsonify({'error': 'Invalid username or password.'}), 401

        # If neither member nor employee, return error
        return jsonify({'error': 'Invalid credentials or user type'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500

### Just Going to code everything into here for now and move it to the financial stub if needed


@app.route('/api/member/add_to_cart', methods=['POST'])
# Route to add 
def add_to_cart():
    
    member_id = session.get('member_session_id')
    if not member_id:
        return jsonify({'message': 'Unauthorized access. Please log in.'}), 401

    # check if the member exists
    member = Member.query.get(member_id)
    if not member:
        return jsonify({'message': 'Member not found'}), 404
    
    data = request.json
    if not data:
        return jsonify({'error': 'No data provided'}), 400
    
    # Extract data from JSON request
    item_name = data.get('item_name')
    item_price = data.get('item_price')
    VIN_carID = data.get('VIN_carID')
    addon_ID = data.get('addon_ID')
    
    if not member_id or not item_name or not item_price:
        return jsonify({'error': 'Missing required fields'}), 400
    
    if VIN_carID and addon_ID:
        return jsonify({'error': 'Both VIN_carID and addon_ID cannot be provided together'}), 400
    elif not VIN_carID and not addon_ID:
        return jsonify({'error': 'Either VIN_carID or addon_ID must be provided'}), 400
    

    try:
        if VIN_carID:
            # Check if the provided VIN exists in the carinfo table
            car = CarInfo.query.filter_by(VIN_carID=VIN_carID).first()
            if not car:
                return jsonify({'error': 'Car with provided VIN not found'}), 404
            
        elif addon_ID:
            # Check if the provided addon ID exists in the addons table
            addon = Addons.query.filter_by(itemID=addon_ID).first()
            if not addon:
                return jsonify({'error': 'Addon with provided ID not found'}), 404
            
    # Create a new checkout cart item with the VIN
        new_item = CheckoutCart(
            memberID=member_id,
            item_name=item_name,
            item_price=item_price,
            VIN_carID=VIN_carID,
            addon_ID=addon_ID
            )
        
        # Add the new item to the database
        db.session.add(new_item)
        db.session.commit()
        
        return jsonify({'success': 'Item added successfully to cart'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500