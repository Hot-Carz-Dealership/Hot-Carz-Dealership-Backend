# app/routes.py

import re
import bcrypt
import random
import hashlib
import logging
import string
from . import app
import sqlalchemy.sql
from .models import *
from sqlalchemy import text
from datetime import datetime, timedelta
from flask import jsonify, request, session
from decimal import Decimal, ROUND_HALF_UP

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
        return hed + error_text + str(logging.log(e))


''' this API retrieves all of the add-on products'''


@app.route('/api/vehicles/add-ons', methods=['GET'])  # TEST DONE
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
            'totalCost': int(addon.totalCost)
        }
        addon_info.append(addon_data)
    return jsonify(addon_info), 200


@app.route('/api/vehicles/search', methods=['GET'])  # TEST DONE
# This API returns all information on all vehicles in the database based on a search function in search bar in the frontend
# TESTCASE: DONE
def vehicle_information():
    search_query = request.args.get('search_query') ##this is args
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


@app.route('/api/member/vehicles', methods=['GET'])  # TEST DONE
def member_vehicles():
    # this API returns cars to specific members logged in. It returns both cars bought from the dealership and cars that
    # they inserted into the system for service appointments.
    member_id = session.get('member_session_id')
    if not member_id:
        return jsonify({'message': 'Unauthorized access'}), 401

    # Ensure that the employee is a member
    member = Member.query.filter_by(memberID=member_id).first()
    if member is None:
        return jsonify({'message': 'You are not a signed up member at this Dealership'}), 401

    # returns all the vehicles matching with the member_id
    vehicles = CarVINs.query.filter_by(memberID=member_id).all()

    vehicles_info = []
    for vehicle_info in vehicles:
        # Fetch additional information from CarInfo table using VIN_carID
        car_info = CarInfo.query.filter_by(VIN_carID=vehicle_info.VIN_carID).first()
        vehicles_info.append({
            'VIN_carID': vehicle_info.VIN_carID,
            'make': car_info.make,
            'model': car_info.model,
            'year': car_info.year,
            'color': car_info.color,
            'mileage': car_info.mileage,
        })
    return jsonify(vehicles_info), 200


@app.route('/api/vehicles', methods=['GET'])  # TEST DONE
# This API returns all information on a specific vehicle based on their VIN number which is passed from the front end to the backend
# Which have not been purchased ofc
# was prev: /api/vehicles
# TESTCASE: DONE
def vehicle():
    VIN_carID = request.args.get('vin')  # get query parameter id
    service = request.args.get('service')  # get query parameter service

    if service == '1':
        # For service 1, consider vehicles with purchase status 'Dealership - Purchased' or 'Outside Dealership'
        vehicle_info = CarInfo.query.join(CarVINs).filter(
            CarVINs.VIN_carID == VIN_carID,
            (CarVINs.purchase_status == 'Dealership - Purchased') |
            (CarVINs.purchase_status == 'Outside Dealership')
        ).first()
    else:
        # For other services or when service parameter is not provided, consider vehicles with purchase status 'Dealership - Not Purchased'
        vehicle_info = CarInfo.query.join(CarVINs).filter(
            CarVINs.VIN_carID == VIN_carID,
            CarVINs.purchase_status == 'Dealership - Not Purchased'
        ).first()    
        
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


@app.route('/api/vehicles/edit', methods=['POST', 'DELETE'])  # test ready, all of it works
def edit_vehicle():
    try:
        data = request.json

        # only have to pass this value when deleting the car
        car_vin = data.get('VIN_carID')
        if request.method == 'POST':
            # user updates the feature of the car
            car_info = CarInfo.query.filter_by(VIN_carID=car_vin).first()

            # frontend has to pass these values in or just use auto fill from values by calling /api/vehicles and then passing them into here
            car_info.make = data.get('make')
            car_info.model = data.get('model')
            car_info.body = data.get('body')
            car_info.year = data.get('year')
            car_info.color = data.get('color')
            car_info.mileage = data.get('mileage')
            car_info.details = data.get('details')
            car_info.description = data.get('description')
            car_info.status = data.get('status')
            car_info.price = data.get('price')

            db.session.commit()
            return jsonify({'message': 'Vehicle successfully updated'}), 200
        elif request.method == 'DELETE':
            # remove listing option on a vehicle | test ready it works
            car_delete_vin = CarVINs.query.filter_by(VIN_carID=car_vin).first()

            if car_delete_vin:
                test_drive = TestDrive.query.filter_by(VIN_carID=car_vin).all()
                for item in test_drive:
                    db.session.delete(item)
                db.session.flush()

                purchases = Purchases.query.filter_by(VIN_carID=car_vin).all()
                for purchase in purchases:
                    purchase.VIN_carID = sqlalchemy.sql.null()
                    db.session.commit()

                ServiceAppointments = ServiceAppointment.query.filter_by(VIN_carID=car_vin).all()
                for item in ServiceAppointments:
                    Services = ServiceAppointmentEmployeeAssignments.query.filter_by(
                        appointment_id=item.appointment_id).all()
                    for service in Services:
                        db.session.delete(service)
                    db.session.flush()
                    db.session.delete(item)
                db.session.flush()

                car_delete_info = CarInfo.query.filter_by(VIN_carID=car_vin).first()
                db.session.delete(car_delete_info)
                db.session.flush()
                db.session.delete(car_delete_vin)
                db.session.commit()
                return jsonify({'message': 'Vehicle deleted'}), 200
            else:
                return jsonify({'message': 'Vehicle not found'}), 404
        else:
            return jsonify({'message': 'Invalid Method'}), 500
    except Exception as e:
        db.session.rollback()
        return jsonify({'message': str(e)}), 500


@app.route('/api/vehicles/add', methods=['POST'])  # TEST DONE
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



@app.route('/api/vehicles/random', methods=['GET'])
def random_vehicles():
    try:
        # Get the requested number of random vehicles from the query parameters, default to 2 if not provided
        num_vehicles = int(request.args.get('num', 2))

        # Get the total number of vehicles in the database from 'Dealership'
        total_vehicles = CarInfo.query.join(CarVINs).filter(
            CarVINs.purchase_status == 'Dealership - Not Purchased').count()

        # If there are not enough vehicles in the database, return an error
        if total_vehicles < num_vehicles:
            return jsonify({'error': 'Insufficient vehicles in the dealership to select random ones.'}), 404

        # Generate random indices within the range of total vehicles
        random_indices = random.sample(range(total_vehicles), min(num_vehicles, total_vehicles))

        # Retrieve information about the random vehicles
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
                'price': int(random_vehicle.price)  # if something messes up with the car price, bruh it was this line
            }
            random_vehicles_info.append(random_vehicle_info)
        return jsonify(random_vehicles_info), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500



@app.route('/api/employees', methods=['GET'])  # TEST DONE
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


@app.route('/api/testdrives', methods=['GET'])  # TEST DONE
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
            'appointment_date': test_drive.appointment_date,
            'confirmation': test_drive.confirmation,
            'id': test_drive.testdrive_id
        })
    return jsonify(test_drive_info), 200


@app.route('/api/testdrives/update_confirmation', methods=['POST'])  # TEST DONE
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


@app.route('/api/testdrives/edit', methods=['POST', 'DELETE'])
# to cut time, both users and managers can access to delete test drives
def edit_testdrive():
    try:
        data = request.json
        testdrive_id = data.get('testdrive_id')
        testdrive_appointment = TestDrive.query.get(testdrive_id)
        if request.method == 'POST':
            # reschedule appointment
            testdrive_appointment.appointment_date = data.get('appointment_date')
            db.session.commit()
            return jsonify({'message': 'Appointment updated successfully'}), 200
        elif request.method == 'DELETE':
            # cancel test drive
            db.session.delete(testdrive_appointment)
            db.session.commit()
            return jsonify({'message': 'Test drive deleted successfully'}), 200
        else:
            return jsonify({'error': 'Method not allowed'}), 400
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


# This API creates an employee based on all the values passed from the front to the backend
@app.route('/api/employees/create', methods=['POST'])  # TEST DONE
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


@app.route('/api/employees/technicians', methods=['GET'])  # TEST DONE
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


@app.route('/api/members', methods=['GET'])  # TEST DONE
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
                         'city': member.city,
                         'zipcode': member.zipcode,
                         'join_date': member.join_date} for member in members]
        return jsonify(members_info), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# This API creates a member account based on the information passed from the front end to the backend (here)
@app.route('/api/members/create', methods=['POST'])  # TEST DONE
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
        return jsonify(member_info), 201
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

    if not user_id:
        user_id = session.get("employee_session_id")

        if not user_id:
            return jsonify({"error": "Unauthorized"}), 401

        employee = Employee.query.filter_by(employeeID=user_id).first()
        if not employee:
            return jsonify({"error": "Employee not found"}), 404

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
    if not member:
        return jsonify({"error": "Member not found"}), 404

    sensitive_info = MemberSensitiveInfo.query.filter_by(memberID=user_id).first()
    if not sensitive_info:
        return jsonify({"error": "Sensitive info not found"}), 404

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


@app.route('/api/service-appointments', methods=['GET'])  # TEST DONE
# GET protocol return all service appointment information
# TESTCASE: DONE FOR GET AND POST
def service_appointments():
    # get request, we return all data form service appointments
    # returns more info now
    appointments = db.session.query(ServiceAppointment, ServiceAppointmentEmployeeAssignments.employeeID).join(
        ServiceAppointmentEmployeeAssignments,
        ServiceAppointment.appointment_id == ServiceAppointmentEmployeeAssignments.appointment_id).all()

    appointments_info = []
    for appointment, employee_id in appointments:
        # Query Services table to get service name
        service_name = Services.query.filter_by(serviceID=appointment.serviceID).first().service_name
        appointments_info.append({
            'appointment_id': appointment.appointment_id,
            'memberID': appointment.memberID,
            'VIN_carID': appointment.VIN_carID,
            'serviceID': appointment.serviceID,
            'appointment_date': appointment.appointment_date,
            'comments': appointment.comments,
            'status': appointment.status,
            'last_modified': appointment.last_modified,
            'service_name': service_name,
            'employeeID': employee_id
        })
    return jsonify(appointments_info), 200


@app.route('/api/members/service-appointments', methods=['GET'])  # test ready
def view_service_appointments_per_member():
    member_id = session.get('member_session_id')
    if not member_id:
        return jsonify({'message': 'Unauthorized access. Please log in.'}), 401

    # check if the member exists
    member = Member.query.get(member_id)
    if not member:
        return jsonify({'message': 'Member not found'}), 404

    # we view all ths stuff through the joins for members to view the service being done
    service_appointments_query = db.session.query(
        ServiceAppointment, Services.service_name
    ).join(
        Services, ServiceAppointment.serviceID == Services.serviceID
    ).filter(
        ServiceAppointment.memberID == member_id
    ).order_by(
        ServiceAppointment.appointment_date.desc()
    )

    # seperation on query execution for better readability for debugging this long join
    service_appointments_result = service_appointments_query.all()

    # get response data
    appointments_data = []
    for appointment, service_name in service_appointments_result:
        appointment_info = {
            'appointment_id': appointment.appointment_id,
            'VIN_carID': appointment.VIN_carID,
            'service_name': service_name,
            'appointment_date': appointment.appointment_date,
            'comments': appointment.comments,
            'status': appointment.status
        }
        appointments_data.append(appointment_info)
    return jsonify(appointments_data), 200


@app.route('/api/manager/cancel-service-appointments', methods=['POST'])  # TEST DONE
# this api used to be a part of the /api/service-appointments but i moved it here for better separation
# was delete, now is post. We shouldn't delete service appointments but instead just store them in case we need information on it
# to view
def delete_service_appointment():
    # USE THIS ENDPOINT FOR WHEN MANAGER ALSO DOES NOT APPROVE SERVICE APPOINTMENT & JUST FOR CANCELLING ALREADY APPROVED APPOINTMENTS AS WELL
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
        status='Pending Confirmation',
        last_modified=datetime.now()
    )
    db.session.add(appointment)
    db.session.commit()

    return jsonify({'message': 'Service appointment booked successfully'}), 201


@app.route('/api/member/book-test-drive', methods=['POST'])  # test ready
# NEW API: this API allows for customer to book a test drive
def book_test_drive():
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
    VIN_carID = data.get('VIN_carID')

    appointment_date = datetime.strptime(appointment_date, '%Y-%m-%d %H:%M:%S')
    if appointment_date <= datetime.now():
        return jsonify({'message': 'Appointment date must be after today'}), 400

    # Check if required data is provided
    if not VIN_carID or not appointment_date:
        return jsonify({'message': 'Car VIN ID and appointment date are required'}), 400

    # Create a new service appointment
    appointment = TestDrive(
        memberID=member_id,
        VIN_carID=VIN_carID,
        appointment_date=appointment_date,
        confirmation='Awaiting Confirmation',
    )
    db.session.add(appointment)
    db.session.commit()

    return jsonify({'message': 'Service appointment booked successfully'}), 201


@app.route('/api/service-menu', methods=['GET'])  # TEST DONE
# Returns all values in the Services table for users to choose what services they want if not vin passed
# If Vin provided queries the warranties associated with that VIN. If warranties exist, it finds the associated services and marks them as free
def get_services():
    try:
        # Check if VIN is provided in the query parameters
        vin = request.args.get('vin')  ## /api/service-menu?vin=ABC123

        if vin:
            # Query warranties for the provided VIN
            warranties = Warranty.query.filter_by(VIN_carID=vin).all()
            if warranties:
                # If warranties exist, find associated services
                free_services = set()
                for warranty in warranties:
                    warranty_services = WarrantyService.query.filter_by(addon_ID=warranty.addon_ID).all()
                    for warranty_service in warranty_services:
                        free_services.add(warranty_service.serviceID)

                # Query all services
                services = Services.query.all()

                # Prepare service info, mark free services
                services_info = []
                for service in services:
                    service_info = {
                        'serviceID': service.serviceID,
                        'service_name': service.service_name,
                        'price': "0.00" if service.serviceID in free_services else service.price
                    }
                    services_info.append(service_info)
            else:
                # If no warranties found, return all services with regular prices
                services_info = [{
                    'serviceID': service.serviceID,
                    'service_name': service.service_name,
                    'price': service.price
                } for service in Services.query.all()]
        else:
            # If VIN is not provided, return all services with regular prices
            services_info = [{
                'serviceID': service.serviceID,
                'service_name': service.service_name,
                'price': service.price
            } for service in Services.query.all()]

        return jsonify(services_info), 200

    except Exception as e:
        # Return error if an exception occurs
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
            edit_or_add = data.get('edit_or_add')
            if edit_or_add == 1:  # add
                service_name = data.get('service_name')
                price = data.get('price')
                if service_name is None or price is None:
                    return jsonify({'message': 'Service name and price are required'}), 400

                new_service = Services(service_name=service_name, price=price)
                db.session.add(new_service)
                db.session.commit()
                return jsonify({'message': 'Service added successfully'}), 201
            elif edit_or_add == 2:  # edit
                serviceID = data.get('serviceID')
                service_name = data.get('service_name')
                price = data.get('price')
                if serviceID is None or service_name is None or price is None:
                    return jsonify({'message': 'Service ID, name, and price are required for editing'}), 400

                service_item = Services.query.filter_by(serviceID=serviceID).first()
                if service_item:
                    service_item.service_name = service_name
                    service_item.price = price  # Update the price as well
                    db.session.commit()
                    return jsonify({'message': 'Service Successfully Edited'}), 200
                else:
                    return jsonify({'message': 'Service not found'}), 404
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


@app.route('/api/manager/confirm-service-appointments', methods=['POST'])  # test ready
# USE FOR API WITH UC 5.1 Set Test Drive
# "Manager approves appointment from their account, Manager does not approve"
def confirm_appointments():
    employee_session_id = session.get('employee_session_id')
    if not employee_session_id:
        return jsonify({'message': 'Unauthorized access'}), 401

    employee = Employee.query.get(employee_session_id)
    if employee is None:
        return jsonify({'message': 'Unauthorized access'}), 403

    try:
        data = request.json

        # front end needs to just pass these values in
        appointmentID = data.get('appointmentID')
        confirmationStatus = data.get('confirmationStatus')
        appointment = ServiceAppointment.query.filter_by(appointment_id=appointmentID).first()
        appointment.status = confirmationStatus
        db.session.commit()
        return jsonify({'message': 'Appointment Status Changed Successfully'}), 200
    except Exception as e:
        return jsonify({'message': 'Error somewhere in Request'}), 401


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

    appointment.status = 'Scheduled'

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


@app.route('/api/technician-view-service-appointments/technician-edit', methods=['POST'])  # TEST DONE
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


@app.route('/api/logout', methods=['POST'])  # TEST DONE
def logout():
    # THE FRONTEND NEEDS TO REDIRECT WHEN U CALL THIS ENDPOINT BACK TO THE LOGIN SCREEN ON that END.
    # LMK if IT WORKS OR NOT
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200


# Route for user authentication
@app.route('/api/login', methods=['POST'])  # TEST DONE
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
## aaaaaaaa

@app.route('/api/member/add_to_cart', methods=['POST'])
# Route to add either a service, a vehicle, and/or add ons.
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
    serviceID = data.get('serviceID')
    financed_amount = data.get('financed_amount')

    if not member_id or not item_name or not item_price:
        return jsonify({'error': 'Missing required fields'}), 400

    # Ensure only one of VIN_carID, addon_ID, or serviceID is provided
    provided_ids = [VIN_carID, addon_ID, serviceID]
    if sum(id is not None for id in provided_ids) != 1:
        return jsonify({'error': 'Exactly one of VIN_carID, addon_ID, or serviceID must be provided'}), 400

    if not financed_amount:
        financed_amount = 0

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
        elif serviceID:
            # Check if the provided service ID exists in the services table
            service = Services.query.filter_by(serviceID=serviceID).first()
            if not service:
                return jsonify({'error': 'Service with provided ID not found'}), 404

        # Create a new checkout cart item with the VIN
        new_item = CheckoutCart(
            memberID=member_id,
            item_name=item_name,
            item_price=item_price,
            VIN_carID=VIN_carID,
            addon_ID=addon_ID,
            serviceID=serviceID,
            financed_amount=financed_amount

        )

        # Add the new item to the database
        db.session.add(new_item)
        db.session.commit()

        return jsonify({'success': 'Item added successfully to cart'}), 201
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/member/delete_from_cart/<int:item_id>', methods=['DELETE'])
# Route to Remove Stuff from the cart one by one
def delete_from_cart(item_id):
    member_id = session.get('member_session_id')
    if not member_id:
        return jsonify({'message': 'Unauthorized access. Please log in.'}), 401

    # Check if the member exists
    member = Member.query.get(member_id)
    if not member:
        return jsonify({'message': 'Member not found'}), 404

    # Check if the item exists in the cart
    item = CheckoutCart.query.get(item_id)
    if not item:
        return jsonify({'error': 'Item not found in the cart'}), 404

    # Check if the item belongs to the logged-in member
    if item.memberID != member_id:
        return jsonify({'error': 'Unauthorized to delete this item from the cart'}), 403

    try:
        # Delete the item from the database
        db.session.delete(item)
        db.session.commit()

        return jsonify({'success': 'Item deleted successfully from the cart'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/manager/member-delete', methods=['DELETE'])  # new one for deleting customer in manager view
# try it out, not tested.
def delete_member():
    try:
        employee_id = session.get('employee_session_id')
        if not employee_id:
            return jsonify({'message': 'Unauthorized access'}), 401

        # Ensure that the employee exists
        employee = Employee.query.filter_by(employeeID=employee_id).first()
        if employee is None:
            return jsonify({'message': 'Employee is not in the System'}), 401

        data = request.json
        member_id = data.get('memberID')
        member = Member.query.get(member_id)

        if member is None:
            return jsonify({'message': 'Member not found'}), 404

        # deletes the bought car information, first warrenty, CarInfo, CarVin Information
        car_vin_info = CarVINs.query.filter_by(memberID=member_id).all()
        if car_vin_info:
            for car in car_vin_info:
                Warranty.query.filter_by(VIN_carID=car_vin_info.VIN_carID).delete()
                CarInfo.query.filter_by(VIN_carID=car_vin_info.VIN_carID).delete()
                db.session.delete(car)

        # Deleting related data

        # test drives
        TestDrive.query.filter_by(memberID=member_id).delete()

        # all service appointments
        service_appointments = ServiceAppointment.query.filter_by(memberID=member_id).all()
        for appointment in service_appointments:
            ServiceAppointmentEmployeeAssignments.query.filter_by(appointment_id=appointment.appointment_id).delete()
        ServiceAppointment.query.filter_by(memberID=member_id).delete()

        CheckoutCart.query.filter_by(memberID=member_id).delete()

        # delete the sensitive info on the member
        MemberSensitiveInfo.query.filter_by(memberID=member_id).delete()

        # delete the stupid member that gets deleted
        db.session.delete(member)
        db.session.commit()
        return jsonify({'message': 'Member account deleted successfully'}), 200
    except Exception as e:
        # Rollback the session in case of any exception
        db.session.rollback()
        logging.exception(e)  # Log the exception for debugging purposes
        return jsonify({'error': 'An error occurred while updating the member account.'}), 500


@app.route('/api/members/update', methods=['POST'])  # test with editing members from the manager page
# Route to update logged in users account info
def update_member():
    try:
        employee_id = session.get('employee_session_id')
        if employee_id is None:
            # Customer auth for making sure they are logged in and have an account
            member_id = session.get('member_session_id')
            if member_id is None:
                return jsonify({'message': 'Invalid session'}), 400

            # Retrieve the member based on the current session
            existing_member = Member.query.get(member_id)
            if existing_member is None:
                return jsonify({'error': 'Member not found.'}), 404

        data = request.json
        if employee_id:
            member_id = data.get('memberID')
            existing_member = Member.query.get(member_id)

        # Update member information
        existing_member.first_name = data.get('first_name', existing_member.first_name)
        existing_member.last_name = data.get('last_name', existing_member.last_name)
        existing_member.email = data.get('email', existing_member.email)
        existing_member.phone = data.get('phone', existing_member.phone)
        existing_member.address = data.get('address', existing_member.address)
        existing_member.city = data.get('city', existing_member.city)
        existing_member.state = data.get('state', existing_member.state)  # Must be state code (NJ, NY, etc)
        existing_member.zipcode = data.get('zipcode', existing_member.zipcode)

        # Commit changes to the database
        db.session.commit()

        # Update driverID if provided
        driverID = data.get('driverID')
        if driverID:
            existing_sensitive_info = MemberSensitiveInfo.query.filter_by(memberID=member_id).first()
            if existing_sensitive_info:
                existing_sensitive_info.driverID = driverID
                db.session.commit()

        # Update SSN if provided
        SSN = data.get('SSN')
        if SSN:
            # Hash the SSN before storing it
            hashed_ssn = bcrypt.hashpw(SSN.encode('utf-8'), bcrypt.gensalt())

            existing_sensitive_info = MemberSensitiveInfo.query.filter_by(memberID=member_id).first()
            if existing_sensitive_info:
                existing_sensitive_info.SSN = hashed_ssn
                db.session.commit()

        # Return updated member information
        member_info = {
            'memberID': existing_member.memberID,
            'first_name': existing_member.first_name,
            'last_name': existing_member.last_name,
            'email': existing_member.email,
            'phone': existing_member.phone,
            'address': existing_member.address,
            'state': existing_member.state,  # Must be state code (NJ, NY, etc)
            'zipcode': existing_member.zipcode,
            'join_date': existing_member.join_date,
        }
        return jsonify({'message': 'Member account updated successfully', 'member_info': member_info}), 200

    except Exception as e:
        # Rollback the session in case of any exception
        db.session.rollback()
        logging.exception(e)  # Log the exception for debugging purposes
        return jsonify({'error': 'An error occurred while updating the member account.'}), 500


@app.route('/api/member/cart', methods=['GET'])
# This route displays everything in a members cart and also totals everything 
def get_cart():
    member_id = session.get('member_session_id')
    if not member_id:
        return jsonify({'message': 'Unauthorized access. Please log in.'}), 401

    # Check if the member exists
    member = Member.query.get(member_id)
    if not member:
        return jsonify({'message': 'Member not found'}), 404

    try:
        # Retrieve items in the cart for the member
        cart_items = CheckoutCart.query.filter_by(memberID=member_id).all()

        # Initialize variables for calculating totals
        subtotal = 0
        financed_total = 0

        # Serialize the cart items
        serialized_cart = []
        for item in cart_items:
            serialized_item = {
                'cart_item_id': item.cart_item_id,
                'item_name': item.item_name,
                'item_price': item.item_price,
                'VIN_carID': item.VIN_carID,
                'addon_ID': item.addon_ID,
                'serviceID': item.serviceID,
                'financed_amount': item.financed_amount
            }
            serialized_cart.append(serialized_item)
            subtotal += item.item_price
            financed_total += item.financed_amount

        # Calculate other totals and taxes
        taxes = (subtotal * Decimal('0.05')).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)  # 5% taxes as per prof
        grand_total = (subtotal + taxes).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        due_now_total = (grand_total - financed_total).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        ## quantize() is used to round the values to two decimal places, and ROUND_HALF_UP is used as the rounding mode to round halfway cases up.

        return jsonify({'cart': serialized_cart, 'Grand Total': grand_total, 'Subtotal': subtotal,
                        'Financed Amount': financed_total, 'Taxes': taxes, 'Amount Due Now': due_now_total}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/member/delete_cart', methods=['DELETE'])
# Route to Remove Entire Cart
def delete_cart():
    member_id = session.get('member_session_id')
    if not member_id:
        return jsonify({'message': 'Unauthorized access. Please log in.'}), 401

    # Check if the member exists
    member = Member.query.get(member_id)
    if not member:
        return jsonify({'message': 'Member not found'}), 404

    # Get all items in the cart of the logged-in member
    cart_items = CheckoutCart.query.filter_by(memberID=member_id).all()

    if not cart_items:
        return jsonify({'error': 'Cart is already empty'}), 404

    try:
        # Delete all items from the cart
        for item in cart_items:
            db.session.delete(item)
        db.session.commit()

        return jsonify({'success': 'Cart deleted successfully'}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/member/test_drive_data', methods=['GET'])
# Gets the 
def get_test_drive_data():
    member_id = session.get('member_session_id')
    if not member_id:
        return jsonify({'message': 'Unauthorized access. Please log in.'}), 401

    # Query the TestDrive table to get test drive data for the current user
    test_drives = TestDrive.query.filter_by(memberID=member_id).all()

    # Initialize a list to store the results
    result = []

    # Iterate through each test drive record and gather the required data
    for test_drive in test_drives:
        # Query the CarInfo table to get additional information about the car
        car_info = CarInfo.query.filter_by(VIN_carID=test_drive.VIN_carID).first()

        # Create a dictionary containing the required data
        test_drive_data = {
            'testdrive_id': test_drive.testdrive_id,
            'VIN_carID': test_drive.VIN_carID,
            'appointment_date': test_drive.appointment_date.strftime("%Y-%m-%d %H:%M:%S"),
            'confirmation': test_drive.confirmation,
            'make': car_info.make,
            'model': car_info.model,
            'year': car_info.year
        }

        # Append the dictionary to the result list
        result.append(test_drive_data)

    # Return the result as JSON
    return jsonify(result)


@app.route('/api/manager/signature-waiting', methods=['GET']) # TEST DONE
def get_awaiting_signature():
    try:
        # this gets the purchases, where only the customer signed so far.
        purchases_waiting_signature = Purchases.query.filter_by(signature='No').all()

        # Check if there are any purchases awaiting signature
        if not purchases_waiting_signature:
            return jsonify({'purchases_waiting_signature': []}), 200

        # Serialize the purchases data
        serialized_purchases = []
        for purchase in purchases_waiting_signature:
            serialized_purchase = {
                'purchaseID': purchase.purchaseID,
                'bidID': purchase.bidID,
                'memberID': purchase.memberID,
                'VIN_carID': purchase.VIN_carID,
                'addon_ID': purchase.addon_ID,
                'serviceID': purchase.serviceID,
                'confirmationNumber': purchase.confirmationNumber,
                'purchaseType': purchase.purchaseType,
                'purchaseDate': purchase.purchaseDate,
                'signature': purchase.signature
            }
            serialized_purchases.append(serialized_purchase)

        return jsonify({'purchases_waiting_signature': serialized_purchases}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/manager/signature', methods=['POST']) # TEST DONE
#this is the manager's response to the signature
def update_signature():
    try:
        data = request.json
        purchase_id = data.get('purchaseID')
        signature_status = data.get('signature')

        # Check if both parameters purchaseid and the signature status are provided
        if purchase_id is None or signature_status is None:
            return jsonify({'error': 'Both purchaseID and signature parameters are required.'}), 400

        # check if the provided signature status is valid
        if signature_status not in ['Yes', 'No']:
            return jsonify({'error': 'Invalid signature status. Must be either "Yes" or "No"'}), 400


        purchase = Purchases.query.get(purchase_id)
        # Check if the purchase exists
        if not purchase:
            return jsonify({'error': 'Purchase not found'}), 404

        # Update the signature status
        purchase.signature = signature_status
        db.session.commit()

        return jsonify({'message': 'Signature updated successfully'}), 200

    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


#THIS ENDPOINT IS FOR THE MANAGER TO GET TEST DRIVES THAT ARE WAITING FOR CONFIRMATION AND ARE THE DAY AFTER TODAY AND LATER.
@app.route('/api/pending_testdrives', methods=['GET']) # TEST DONE
def get_pending_test_drives():
    test_drive_info = []
    tomorrow = datetime.now().date() + timedelta(days=1)

    pending_test_drives = db.session.query(TestDrive, Member, CarInfo). \
        join(Member, TestDrive.memberID == Member.memberID). \
        join(CarInfo, TestDrive.VIN_carID == CarInfo.VIN_carID). \
        filter(TestDrive.confirmation == 'Awaiting Confirmation'). \
        filter(TestDrive.appointment_date >= tomorrow).all()

    for test_drive, member, car in pending_test_drives:
        test_drive_info.append({
            'fullname': f"{member.first_name} {member.last_name}",
            'phone': member.phone,
            'car_id': test_drive.VIN_carID,
            'car_make_model': f"{car.make} {car.model}",
            'appointment_date': test_drive.appointment_date,
            'confirmation': test_drive.confirmation,
            'id': test_drive.testdrive_id
        })

    return jsonify(test_drive_info), 200

# FOR MANAGER TO GET SERVICE APPOINTMENTS TO CONFIRM AND ASSIGN A TECHNICIAN TO.
@app.route('/api/pending-service-appointments', methods=['GET']) # TEST DONE
def pending_service_appointments():
    try:
        # Subquery to check for existence of appointment_id in ServiceAppointmentEmployeeAssignments
        subquery = db.session.query(ServiceAppointmentEmployeeAssignments.appointment_id). \
            filter(ServiceAppointmentEmployeeAssignments.appointment_id == ServiceAppointment.appointment_id). \
            exists()

        # Query service appointments without an entry in ServiceAppointmentEmployeeAssignments
        pending_appointments = db.session.query(ServiceAppointment). \
            filter(~subquery).filter(ServiceAppointment.status == "Pending Confirmation").all()

        pending_appointments_info = []
        for appointment in pending_appointments:
            # Query Services table to get service name
            service = Services.query.filter_by(serviceID=appointment.serviceID).first()
            if service:
                service_name = service.service_name
            else:
                service_name = "Service not found"

            pending_appointments_info.append({
                'appointment_id': appointment.appointment_id,
                'memberID': appointment.memberID,
                'VIN_carID': appointment.VIN_carID,
                'serviceID': appointment.serviceID,
                'appointment_date': appointment.appointment_date,
                'comments': appointment.comments,
                'status': appointment.status,
                'last_modified': appointment.last_modified,
                'service_name': service_name
            })
        return jsonify(pending_appointments_info), 200
    except Exception as e:
        return jsonify({'message': str(e)}), 500


#I THINK THIS WAS MADE ALREADY,BUT IF NOT, FOR MANAGER TO GET INFO ABOUT A MEMBER
@app.route('/api/manager/get_member', methods=['POST'])
def get_member_by_id():
    try:
        # Get the member ID from the request JSON data
        request_data = request.json
        member_id = request_data.get('memberID')

        # Validate the member ID
        if not member_id:
            return jsonify({'message': 'Member ID is required'}), 400

        # Query the member from the database by ID
        member = Member.query.filter_by(memberID=member_id).first()

        # Check if the member exists
        if not member:
            return jsonify({'message': 'Member not found'}), 404

        # Serialize the member data
        member_info = {
            'memberID': member.memberID,
            'first_name': member.first_name,
            'last_name': member.last_name,
            'email': member.email,
            'phone': member.phone,
            'address': member.address,
            'state': member.state,
            'city': member.city,
            'zipcode': member.zipcode,
            'join_date': member.join_date
        }

        return jsonify(member_info), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500


#needed to make account page work
#probably needs to be on financial backend
#idktho - Patrick

@app.route('/api/member/current-bids', methods=['GET', 'POST'])
def current_member_bids():
    # check if the member is logged in, if not redirect them to log in
    member_id = session.get('member_session_id')
    if not member_id:
        return jsonify({'message': 'Unauthorized access. Please log in.'}), 401

    # check if the member exists
    member = Member.query.get(member_id)
    if not member:
        return jsonify({'message': 'Member not found'}), 404

    # GET Request: returns all bid information based on the logged in member and their memberID
    if request.method == 'GET':
        bids = Bids.query.filter_by(memberID=member_id).all()
        if not bids:
            return jsonify({'message': 'No bids found for this member'}), 404
        bid_info = [{'bidID': bid.bidID,
                     'memberID': bid.memberID,
                     'VIN_carID': bid.VIN_carID,
                     'bidValue': bid.bidValue,
                     'bidStatus': bid.bidStatus,
                     'bidTimestamp': bid.bidTimestamp
                     }
                    for bid in bids]
        return jsonify(bid_info), 200
    elif request.method == 'POST':
        # frontend needs to pass these values in for it to work
        data = request.json
        bid_id = data.get('bid_id') # these should work as a button accociated with the bid value/row
        new_bid_value = data.get('new_bid_value')

        if bid_id is None or new_bid_value is None:
            return jsonify({'message': 'Bid ID and new Bid Value is required in the request'}), 400

        # finds the denied bid and then copies all other relevant meta data in a nice manner to avoid stupid overworking things
        denied_bid = Bids.query.filter_by(memberID=member_id, bidID=bid_id).first()
        if denied_bid:
            denied_bid.bidValue=new_bid_value
            denied_bid.bidStatus='Processing'
            db.session.commit()
            return jsonify({'message': 'Bid updated successfully'}), 201
        else:
            return jsonify({'message': 'Denied bid not found for this member with the provided bid ID'}), 404
        
        

''' Im Moving all the financial end point back to the stub. '''
''' Anything Below Here will now be in the financial stub and should be working'''


'''On the Fin Stub'''
# # this should be on the finacial end point 
# @app.route('/api/vehicle-purchase/new-bid-insert', methods=['POST'])
# def bid_insert_no_financing():
#     try:
#         # Extract data from the request
#         data = request.get_json()
#         required_fields = ['member_id', 'vin', 'bid_value', 'bid_status']
        
#         # Check if all required fields are present
#         missing_fields = [field for field in required_fields if field not in data]
#         if missing_fields:
#             return jsonify({'message': f'Error: Missing fields - {", ".join(missing_fields)}'}), 400
        
#         # Extract data
#         member_id = data['member_id']
#         vin = data['vin']
#         bid_value = data['bid_value']
#         bid_status = 'Processing'
        
#         # Create a new bid entry
#         new_bid = Bids(
#             memberID=member_id,
#             VIN_carID=vin,
#             bidValue=bid_value,
#             bidStatus=bid_status,
#             bidTimestamp=datetime.now()
#         )

#         db.session.add(new_bid)
#         db.session.commit()
#         return jsonify({'message': 'Bid successfully inserted.'}), 201
#     except Exception as e:
#         # Rollback the transaction in case of an error
#         db.session.rollback()
#         return jsonify({'message': f'Error: {str(e)}'}), 500



# Copied
def creditScoreGenerator(member_id: int, monthly_income: float) -> int:
    # Creates a random credit score based on id and income so that the same is always returned
    # Create a unique seed based on member_id and monthly_income
    seed = hashlib.sha256(f"{member_id}-{monthly_income}".encode()).hexdigest()
    # Convert the seed to an integer for seeding the random number generator
    seed_int = int(seed, 16) % (10 ** 8)  # Modulo to keep the number within an appropriate range
    # Seed the random number generator
    random.seed(seed_int)
    # Generate a random credit score
    return random.randint(500, 850)

# Copied
def interest_rate(creditScore: int) -> int:
    # calculates the base interest rate
    if creditScore >= 750:
        return 5
    elif creditScore >= 700:
        return 10
    elif creditScore >= 650:
        return 15
    else:
        return 20

# Copied
def adjust_loan_with_downpayment(vehicle_cost, down_payment):
    # Recalculate the loan amount based on the new down_payment
    loan_amount = vehicle_cost - down_payment
    return loan_amount

# Copied

def calculateInterest(vehicleCost: int, monthlyIncome: int, creditscore: int) -> float:
    # generates the total amount financed after interest 

    base_loan_interest_rate = interest_rate(creditscore)
    # Calculate financing value based on vehicle cost and monthly income
    final_financing_percentage = base_loan_interest_rate + ((vehicleCost / monthlyIncome) * 100)
    financing_loan_value = (final_financing_percentage / 100) * vehicleCost
    return round(financing_loan_value, 2)

# Copied

def check_loan_eligibility(loan_amount: float, monthly_income: int) -> bool:
    # Calculate yearly income from monthly income
    yearly_income = monthly_income * 12

    # Calculate the loan amount and check if it's less than 10% of the yearly income
    if loan_amount <= (yearly_income * 0.1):
        return True  # User is eligible for the loan
    else:
        return False  # User is not eligible for the loan

'''MOVED AND SUCCESFULLY TESTED'''

# @app.route('/api/vehicle-purchase/apply-for-financing', methods=['POST'])
# # Route just to apply for financing and returns terms if user is eligible
# # This wont add to any tables yet,
# # we'll have the front end send back the same terms if users accepts in another route
# ##The user will accept by typing in their name or initials(aka signing)
# def apply_for_financing():
#     try:
#         # customer auth for making sure they are logged in and have an account
#         member_id = session.get('member_session_id')
#         if member_id is None:
#             return jsonify({'message': 'Invalid session'}), 400

#         # frontend needs to send these values to the backend
#         data = request.json
#         if not data:
#             return jsonify({'error': 'No data provided'}), 400

#         Vin_carID = data.get('Vin_carID')
#         down_payment = float(data.get('down_payment'))
#         monthly_income = float(data.get('monthly_income'))
#         vehicle_cost = float(
#             data.get('vehicle_cost'))  # Front end can send this based on if the user won a bid or buying at MSRP

#         credit_score = creditScoreGenerator(member_id, monthly_income)
#         total_cost = adjust_loan_with_downpayment(vehicle_cost, down_payment)
#         finance_interest = calculateInterest(total_cost, monthly_income, credit_score)

#         # Loan eligibility
#         loan_eligibility = check_loan_eligibility(total_cost, monthly_income)
#         if not loan_eligibility:
#             return jsonify({
#                                'message': 'Your yearly income is not sufficient to take on this loan. Reapply with more down payment'}), 400

#         # downPayment_value = total_cost - financing_loan_amount
#         valueToPay_value = round(total_cost + finance_interest, 2)
#         paymentPerMonth_value = round(valueToPay_value / 48, 2)

#         # Create a dictionary with financing terms
#         financing_terms = {
#             'member_id': member_id,
#             'income': int(monthly_income) * 12,
#             'credit_score': credit_score,
#             'loan_total': valueToPay_value,
#             'down_payment': down_payment,
#             'percentage': interest_rate(credit_score),
#             'monthly_payment_sum': paymentPerMonth_value,
#             'remaining_months': 48,
#             'Vin_carID': Vin_carID,
#             'financed_amount': total_cost,
#             'interest_total': finance_interest
#         }

#         # Return the financing terms as JSON
#         # Front End should save this somewhere
#         # If the user accepts by signing then use the /insert-financing route

#         return jsonify({'financing_terms': financing_terms}), 200
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'message': f'Error: {str(e)}'}), 500

'''MOVED AND SUCCESFULLY TESTED'''

# @app.route('/api/vehicle-purchase/insert-financing', methods=['POST'])
# # Use this route whenever the user accepts the loan to add it to the db
# def insert_financing():
#     try:

#         # customer auth for making sure they are logged in and have an account
#         member_id = session.get('member_session_id')
#         if member_id is None:
#             return jsonify({'message': 'Invalid session'}), 400

#         # Validate required fields
#         data = request.json
#         required_fields = ['VIN_carID', 'income', 'credit_score', 'loan_total', 'down_payment', 'percentage',
#                            'monthly_payment_sum', 'remaining_months']
#         if not all(field in data for field in required_fields):
#             return jsonify({'message': 'Missing required fields'}), 400

#         # Retrieve data from the request
#         data = request.json
#         VIN_carID = data.get('VIN_carID')
#         income = data.get('income')
#         credit_score = data.get('credit_score')
#         loan_total = data.get('loan_total')
#         down_payment = data.get('down_payment')
#         percentage = data.get('percentage')
#         monthly_payment_sum = data.get('monthly_payment_sum')
#         remaining_months = data.get('remaining_months')

#         if VIN_carID:
#             # Check if the provided VIN exists in the carinfo table
#             car = CarInfo.query.filter_by(VIN_carID=VIN_carID).first()
#             if not car:
#                 return jsonify({'error': 'Car with provided VIN not found'}), 404

#         # Insert data into the database
#         new_financing = Financing(
#             memberID=member_id,
#             VIN_carID=VIN_carID,
#             income=income,
#             credit_score=credit_score,
#             loan_total=loan_total,
#             down_payment=down_payment,
#             percentage=percentage,
#             monthly_payment_sum=monthly_payment_sum,
#             remaining_months=remaining_months
#         )
#         db.session.add(new_financing)
#         db.session.commit()

#         return jsonify({'message': 'Financing information inserted successfully.'}), 200
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'message': f'Error: {str(e)}'}), 500


## User get sent to add ons page
## Anything they add on that page gets added to the users cart


'''Nobody was using this one anywhere'''

@app.route('/api/vehicle-purchase/get-financing', methods=['GET'])
# Returns the currently all of the currently logged in members loan
def get_financing():
    try:
        # Validate session
        member_id = session.get('member_session_id')
        if not member_id:
            return jsonify({'message': 'Invalid session'}), 401

        # Query financing information for the current member
        financing_info = Financing.query.filter_by(memberID=member_id).all()

        # Check if any financing information is found
        if not financing_info:
            return jsonify({'message': 'No financing information found'}), 404

        # Serialize the financing information
        serialized_data = []
        for financing in financing_info:
            serialized_data.append({
                'VIN_carID': financing.VIN_carID,
                'income': financing.income,
                'credit_score': financing.credit_score,
                'loan_total': financing.loan_total,
                'down_payment': financing.down_payment,
                'percentage': financing.percentage,
                'monthly_payment_sum': financing.monthly_payment_sum,
                'remaining_months': financing.remaining_months
            })

        return jsonify(serialized_data), 200
    except Exception as e:
        return jsonify({'message': f'Error: {str(e)}'}), 500


# Finally they hit the final check out
# Display all the items in the cart with /api/member/cart

# COPIED
def confirmation_number_generation() -> str:
    try:
        total_chars = string.ascii_uppercase + string.digits
        return ''.join(random.choice(total_chars) for i in range(13))
    except Exception as e:
        # Log the exception or handle it appropriately
        print(f"Error generating confirmation number: {e}")
        return None

'''MOVED AND SUCCESFULLY TESTED'''

# @app.route('/api/vehicle-purchase/make-purchase', methods=['POST'])
# # Route Where all purchases will be made for car,addons, or service center
# def make_purchase():
#     # here we deal with Purchases and Payments table    
#     try:
#         member_id = session.get('member_session_id')
#         if not member_id:
#             return jsonify({'message': 'Unauthorized access. Please log in.'}), 403

#         data = request.json
#         if not data:
#             return jsonify({'error': 'No data provided'}), 400

#         required_fields = ['routingNumber', 'bankAcctNumber', 'Amount Due Now', 'Financed Amount']
#         missing_fields = [field for field in required_fields if field not in data]
#         if missing_fields:
#             error_message = f'Missing required field(s): {", ".join(missing_fields)}'
#             return jsonify({'error': error_message}), 400

#         # Gen a single confirmation number for the purchase
#         confirmation_number = confirmation_number_generation()

#         # Retrieve cart items
#         cart_items = CheckoutCart.query.filter_by(memberID=member_id).all()

#         # Extract data from JSON request

#         # Needed for purchases table
#         VIN_carID = None
#         addon_ID = None
#         serviceID = None
#         bidID = None
#         # purchaseType = None

#         # Needed for payments table
#         financed_amount = Decimal(data.get('Financed Amount', 0))
#         valuePaid = Decimal(data.get('Amount Due Now', 0))
#         routingNumber = data.get('routingNumber')
#         bankAcctNumber = data.get('bankAcctNumber')
#         financingID = None
#         # Add validation on front end for routing and acct numbers

#         # Lists to accumulate VINs and addon IDs
#         vin_with_addons = None
#         addons = []

#         # Add cart items to the Purchases table
#         for item in cart_items:
#             bidID = None
#             addon_ID = item.addon_ID
#             # Check if VIN_carID exists in the bids table and get bidID if it does
#             VIN_carID = item.VIN_carID
#             if VIN_carID:
#                 vin_with_addons = VIN_carID
#                 bid = Bids.query.filter_by(VIN_carID=VIN_carID).first()
#                 if bid:
#                     bidID = bid.bidID
#                 if item.financed_amount:
#                     # looks up the financing id of the car being financed
#                     financing = Financing.query.filter_by(VIN_carID=VIN_carID).first()
#                     if financing:
#                         financingID = financing.financingID
#             # If the item is an addon, add addon to the lists
#             if addon_ID:
#                 addons.append(addon_ID)

#             new_purchase = Purchases(
#                 bidID=bidID,
#                 memberID=member_id,
#                 VIN_carID=VIN_carID,
#                 addon_ID=item.addon_ID,
#                 serviceID=item.serviceID,
#                 confirmationNumber=confirmation_number,
#                 purchaseType='Vehicle/Add-on Purchase' if not item.serviceID else 'Service Payment',
#                 purchaseDate=datetime.now(),
#                 signature='No'
#             )
#             # Check if provided IDs exist
#             if VIN_carID and not CarInfo.query.filter_by(VIN_carID=VIN_carID).first():
#                 return jsonify({'error': 'Car with provided VIN not found'}), 404
#             elif addon_ID and not Addons.query.filter_by(itemID=addon_ID).first():
#                 return jsonify({'error': 'Addon with provided ID not found'}), 404
#             elif serviceID and not Services.query.filter_by(serviceID=serviceID).first():
#                 return jsonify({'error': 'Service with provided ID not found'}), 404

#             # Update CarInfo status to 'sold'
#             db.session.query(CarInfo).filter_by(VIN_carID=VIN_carID).update({'status': 'sold'})
#             # Update CarVINs purchase_status to 'Dealership - Purchased' and memberID to current memberID
#             db.session.query(CarVINs).filter_by(VIN_carID=VIN_carID).update(
#                 {'purchase_status': 'Dealership - Purchased', 'memberID': member_id})

#             db.session.commit()

#             db.session.add(new_purchase)
#             db.session.commit()

#         # Create Warranty instances for each addon associated with the VIN
#         for addon in addons:
#             new_warranty = Warranty(
#                 VIN_carID=vin_with_addons,
#                 addon_ID=addon
#             )
#             db.session.add(new_warranty)

#         # Add cart items to the OrderHistory table
#         for item in cart_items:
#             new_order_history = OrderHistory(
#                 memberID=member_id,
#                 item_name=item.item_name,
#                 item_price=item.item_price,
#                 financed_amount=item.financed_amount,
#                 confirmationNumber=confirmation_number,
#                 purchaseDate=datetime.now()
#             )
#             db.session.add(new_order_history)
#             db.session.commit()

#         # Hash the bank info
#         routingNumber = bcrypt.hashpw(routingNumber.encode('utf-8'), bcrypt.gensalt())
#         bankAcctNumber = bcrypt.hashpw(bankAcctNumber.encode('utf-8'), bcrypt.gensalt())

#         new_payment = Payments(
#             paymentStatus='Completed',
#             valuePaid=valuePaid.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
#             valueToPay=financed_amount.quantize(Decimal('0.01'), rounding=ROUND_HALF_UP),
#             initialPurchase=datetime.now(),
#             lastPayment=datetime.now(),
#             routingNumber=routingNumber,
#             bankAcctNumber=bankAcctNumber,
#             memberID=member_id,
#             financingID=financingID
#         )
#         db.session.add(new_payment)
#         db.session.commit()

#         # payment stub generation can occur through the means of functions above with endpoints
#         # /api/member
#         # /api/payments

#         # need to clear the cart after wards using delete cart route on front end

#         return jsonify({'message': 'Purchase made successfully.',
#                         'confirmation_number':confirmation_number}), 200
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'error': f'Error: {str(e)}'}), 500
'''MOVED AND SUCCESFULLY TESTED'''

# # @app.route('/api/member/order_history', methods=['GET'])
# # # Route retrieves order history for a logged-in member, calculates subtotal, taxes, amount paid, and total amount financed for each order, and returns the formatted data as JSON.
# # def order_history():
#     # Get the logged-in member ID
#     member_id = session.get('member_session_id')
#     if not member_id:
#         return jsonify({'message': 'Unauthorized access. Please log in.'}), 403

#     # Query to get all orders for the logged-in member
#     orders = OrderHistory.query.filter_by(memberID=member_id).all()

#     if not orders:
#         return jsonify({'message': 'No orders found for the logged-in member.'}), 404

#     # Prepare dictionary to store order history data per confirmationNumber
#     order_history_data = {}

#     for order in orders:
#         confirmation_number = order.confirmationNumber
#         # If the confirmation number already exists in the dictionary, update the order details
#         if confirmation_number in order_history_data:
#             order_data = order_history_data[confirmation_number]
#             # Add item to the existing items list
#             order_data['items'].append({
#                 'Item Name': order.item_name,
#                 'Item Price': '{:.2f}'.format(float(order.item_price)),
#                 'Financed Amount': '{:.2f}'.format(float(order.financed_amount))
#             })
#             # Update subtotal, taxes, amount paid, and total amount financed
#             order_data['Subtotal'] += float(order.item_price)
#             order_data['Taxes'] = round(order_data['Subtotal'] * 0.05, 2)
#             order_data['Amount Paid'] = round(order_data['Subtotal'] + order_data['Taxes'], 2)
#             order_data['Total Financed'] += float(order.financed_amount)
#         # If the confirmation number does not exist in the dictionary, create a new entry
#         else:
#             # Initialize order details
#             subtotal = float(order.item_price)  # Convert to float
#             taxes = round(subtotal * 0.05, 2)
#             amount_paid = round(subtotal + taxes, 2)
#             total_financed = float(order.financed_amount)
#             order_history_data[confirmation_number] = {
#                 'Confirmation Number': confirmation_number,
#                 'Subtotal': subtotal,
#                 'Taxes': taxes,
#                 'Amount Paid': amount_paid,
#                 'Total Financed': total_financed,
#                 'items': [
#                     {
#                         'Item Name': order.item_name,
#                         'Item Price': '{:.2f}'.format(float(order.item_price)),
#                         'Financed Amount': '{:.2f}'.format(float(order.financed_amount))
#                     }
#                 ]
#             }

#     # Convert dictionary values to list for JSON serialization
#     order_history_list = list(order_history_data.values())

#     # Format Subtotal, Taxes, and Amount Paid for each order
#     for order_data in order_history_list:
#         order_data['Subtotal'] = '{:.2f}'.format(float(order_data['Subtotal']))
#         order_data['Taxes'] = '{:.2f}'.format(float(order_data['Taxes']))
#         order_data['Amount Paid'] = '{:.2f}'.format(float(order_data['Amount Paid']))
#         order_data['Total Financed'] = '{:.2f}'.format(float(order_data['Total Financed']))

#     return jsonify(order_history_list), 200

'''MOVED AND BUT NOT TESTED'''
#for manager to counter bid
# @app.route('/api/manager/counter_bid_offer', methods=['POST'])
# def counter_bid_offer():
#     if request.method == 'POST':
#         data = request.json
#         bid_id = data.get('bidID')
#         new_offer_price = data.get('newOfferPrice')

#         # Fetch the bid from the database
#         bid = Bids.query.get(bid_id)

#         if bid:
#             # Update the bid's offer price
#             bid.bidValue = new_offer_price
#             db.session.commit()
#             return jsonify({'message': 'Bid offer price updated successfully'})
#         else:
#             return jsonify({'error': 'Bid not found'}), 404
#     else:
#         return jsonify({'error': 'Method not allowed'}), 405
