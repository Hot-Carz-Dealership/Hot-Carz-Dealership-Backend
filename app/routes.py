# app/routes.py

from flask import Flask,jsonify, request, session
from sqlalchemy import text
from datetime import datetime
from . import app
from .models import *

from flask_cors import CORS, cross_origin


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
    return jsonify(addon_info)


@app.route('/api/vehicles/search', methods=['GET'])
# This API returns all information on all vehicles in the database based on a search function in search bar in the frontend
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
    return jsonify(cars_info_dicts)


@app.route('/api/vehicles', methods=['GET'])
# This API returns all information on a specific vehicle based on their VIN number which is passed from the front end to the backend
def vehicle():
    data = request.json
    VIN_carID = data.get('VIN_carID')  # needs to be passed from the frontend
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
            'stockAmount': vehicle_info.stockAmount,
            'viewsOnPage': vehicle_info.viewsOnPage,
            'pictureLibraryLink': vehicle_info.pictureLibraryLink,
            'status': vehicle_info.status,
            'price': str(vehicle_info.price)  # Converting Decimal to string for JSON serialization
        }
        return jsonify(vehicle_info)
    else:
        return jsonify({'message': 'Vehicle not found'}), 404


@app.route('/api/employees', methods=['GET'])
# This API returns all employees and their information
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
    return jsonify(employee_info)


@app.route('/api/testdrives', methods=['GET'])
# THIS ENDPOINT return all testdrive information and joins with the Member and Cars table for better information to view on the manager View
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
    return jsonify(test_drive_info)


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
        # i didn't change it, im not gonna it works i think, LMK frontend
        # makes the needed change to update said decisions on the DB
        with db.engine.connect() as connection:
            connection.execute(
                text("UPDATE TestDrive SET confirmation = :confirmation_value WHERE testdrive_id = :testdrive_id;"),
                {'confirmation_value': confirmation_value, 'testdrive_id': testdrive_id}
            )
        return jsonify({'message': 'Confirmation updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/employees/login', methods=['GET'])
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
        db.session.commit()
        return jsonify({'message': 'Employee account created successfully'}), 201
    except Exception as e:
        # Rollback the session in case of any error
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


@app.route('/api/members', methods=['GET'])
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
        return jsonify(members_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@cross_origin
@app.route('/api/members/login', methods=['GET','POST'])
# This API is used as Authentication to login a member IF their ACCOUNT EXISTS and
# returns that members information. we need their username and password passed from the front end to the backend to login
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
            })
        else:
            return jsonify({'error': 'Member not found or credentials invalid'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/members/create', methods=['POST'])
# This API creates an employee based on the information passed from the front end to the backend (here)
def create_member():
    try:
        # Extract data from the request body
        data = request.json

        # values needing to be passed from the front to the backend
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone = data.get('phone')
        username = data.get('username')
        password = data.get('password')

        # Create a new Member object
        new_member = Member(first_name=first_name, last_name=last_name, email=email, phone=phone,
                            join_date=datetime.now())

        # Create a new MemberSensitiveInfo object
        new_sensitive_info = MemberSensitiveInfo(username=username, password=password)

        # Associate MemberSensitiveInfo with the new Member
        new_member.sensitive_info = new_sensitive_info

        # Add the new member and sensitive info to the database session
        db.session.add(new_member)
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
        return jsonify({'error': str(e)}), 500


@app.route('/api/service-appointments', methods=['GET', 'POST'])
# GET protocol return all service appointment information
# POST protocol is used for managers to cancel appointments on their views when they are logged in
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

        return jsonify(appointments_info)

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

            return jsonify({'message': 'Appointment canceled successfully'})

        except Exception as e:
            return jsonify({'error': str(e)}), 500


@app.route('/api/logout')
def logout():
    # THE FRONTEND NEEDS TO REDIRECT WHEN U CALL THIS ENDPOINT BACK TO THE LOGIN SCREEN ON that END.
    # LMK if IT WORKS OR NOT
    session.clear()
    return jsonify({'message': 'Logged out successfully'}), 200
