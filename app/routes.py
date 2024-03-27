# app/routes.py

from datetime import datetime
from flask import jsonify, request
from sqlalchemy import Text, text, func
from . import app
from .models import *
import re

''' all the route API's here '''

'''This API is used to check that ur DB is working locally'''


@app.route('/')
def testdb():
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


'''This API returns all information on all vehicles in the database'''


@app.route('/api/vehicles', methods=['GET'])
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


'''This API returns all information on a specific vehicle based on their VIN number which is passed from the front end to the backend'''


@app.route('/api/vehicles/<string:VIN_carID>', methods=['GET'])
def vehicle(VIN_carID):
    vehicle = Cars.query.filter_by(VIN_carID=VIN_carID).first()
    if vehicle:
        vehicle_info = {
            'VIN_carID': vehicle.VIN_carID,
            'make': vehicle.make,
            'model': vehicle.model,
            'body': vehicle.body,
            'year': vehicle.year,
            'color': vehicle.color,
            'mileage': vehicle.mileage,
            'details': vehicle.details,
            'description': vehicle.description,
            'inStock': vehicle.inStock,
            'stockAmount': vehicle.stockAmount,
            'viewsOnPage': vehicle.viewsOnPage,
            'pictureLibraryLink': vehicle.pictureLibraryLink,
            'status': vehicle.status,
            'price': str(vehicle.price)  # Converting Decimal to string for JSON serialization
        }
        return jsonify(vehicle_info)
    else:
        return jsonify({'message': 'Vehicle not found'}), 404


'''This API returns all employees and their information'''


@app.route('/api/employees', methods=['GET'])
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
def get_test_drives():
    test_drive_info = []
    test_drives = db.session.query(TestDrive, Member, Cars). \
        join(Member, TestDrive.memberID == Member.memberID). \
        join(Cars, TestDrive.car_id == Cars.VIN_carID).all()

    for test_drive, member, car in test_drives:
        test_drive_info.append({
            'fullname': f"{member.first_name} {member.last_name}",
            'phone': member.phone,
            'car_id': test_drive.car_id,
            'car_make_model': f"{car.make} {car.model}",
            'appointment_date': test_drive.appointment_date
        })

    return jsonify(test_drive_info)


# @app.route('/api/testdrives/confirmation/<string:confirmation>', methods=['POST'])
# def get_test_drives(confirmation):
#     test_drives = TestDrive.query.filter(TestDrive.confirmation == confirmation).all()
#     test_drive_info = []
#     for test_drive in test_drives:
#         member = test_drive.member
#         car = test_drive.car
#         test_drive_data = {
#             'fullname': f"{member.first_name} {member.last_name}",
#             'phone': member.phone,
#             'car_id': test_drive.car_id,
#             'car_make_model': f"{car.make} {car.model}",
#             'appointment_date': test_drive.appointment_date.strftime('%Y-%m-%d %H:%M:%S')  # Format date as string
#         }
#         test_drive_info.append(test_drive_data)
#     return jsonify(test_drive_info)
#

@app.route('/api/testdrives/update_confirmation', methods=['POST'])
def update_confirmation():
    data = request.json
    testdrive_id = data.get('testdrive_id')
    confirmation = data.get('confirmation')

    # Check if both parameters are provided
    if testdrive_id is None or confirmation is None:
        return jsonify({'error': 'Both testdrive_id and confirmation parameters are required.'}), 400

    confirmation_value = 'Confirmed' if confirmation == '1' else 'Denied'

    try:
        with db.engine.connect() as connection:
            connection.execute(
                text("UPDATE TestDrive SET confirmation = :confirmation_value WHERE testdrive_id = :testdrive_id;"),
                {'confirmation_value': confirmation_value, 'testdrive_id': testdrive_id}
            )
        return jsonify({'message': 'Confirmation updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


'''This API returns a specific employee based on their email address and password.'''


@app.route('/api/employees/<string:email>/<string:passwd>', methods=['GET'])
def employee(email, passwd):
    # Retrieve employee based on email and password
    try:
        employee_data = db.session.query(Employee, EmployeeSensitiveInfo). \
            join(EmployeeSensitiveInfo, Employee.employeeID == EmployeeSensitiveInfo.employeeID). \
            filter(Employee.email == email, EmployeeSensitiveInfo.password == passwd).first()

        # Check if employee exists
        if employee_data is not None:
            employee, sensitive_info = employee_data
            # Construct response
            response = {
                'employeeID': employee.employeeID,
                'firstname': employee.firstname,
                'lastname': employee.lastname,
                'email': employee.email,
                'phone': employee.phone,
                'address': employee.address,
                'employeeType': employee.employeeType,
                'lastModified': sensitive_info.lastModified
            }
            return jsonify(response), 200
        else:
            return jsonify({'message': 'Employee not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


'''This API creates an employee based on all the values passed from the front to the backend'''


@app.route('/api/employees', methods=['POST'])
def create_employee():
    data = request.json
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    email = data.get('email')
    phone = data.get('phone')
    address = data.get('address')
    employee_type = data.get('employeeType')

    # Create a new employee object
    new_employee = Employee(
        firstname=firstname,
        lastname=lastname,
        email=email,
        phone=phone,
        address=address,
        employeeType=employee_type
    )

    # Add the new employee to the session
    db.session.add(new_employee)

    try:
        # Commit the session to the database
        db.session.commit()
        return jsonify({'message': 'Employee account created successfully'}), 201
    except Exception as e:
        # Rollback the session in case of any error
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


'''Retrieves all the members and their information'''


@app.route('/api/members', methods=['GET'])
def get_all_members():
    try:
        # Query all members from the database
        members = Member.query.all()

        # Convert the query result to a list of dictionaries
        members_info = [{'memberID': member.memberID,
                         'first_name': member.first_name,
                         'last_name': member.last_name,
                         'email': member.email,
                         'phone': member.phone,
                         'status': member.status,
                         'join_date': member.join_date} for member in members]

        return jsonify(members_info)
    except Exception as e:
        return jsonify({'error': str(e)}), 500


'''This API returns a specific member by their username and password passed from the front end to the backend (here)'''


@app.route('/api/members/<string:username>/<string:passwd>', methods=['GET'])
def member(username, passwd):
    try:
        member_info = db.session.query(Member, MemberSensitiveInfo). \
            join(MemberSensitiveInfo, Member.memberID == MemberSensitiveInfo.memberID). \
            filter(MemberSensitiveInfo.username == username, MemberSensitiveInfo.password == passwd).first()

        if member_info:
            member, sensitive_info = member_info
            return jsonify({
                'memberID': member.memberID,
                'first_name': member.first_name,
                'last_name': member.last_name,
                'email': member.email,
                'phone': member.phone,
                'status': member.status,
                'join_date': member.join_date,
                'SSN': sensitive_info.SSN,
                'driverID': sensitive_info.driverID,
                'cardInfo': sensitive_info.cardInfo
            })
        else:
            return jsonify({'error': 'Member not found or credentials invalid'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


'''This API creates an employee based on the information passed from the front end to the backend (here)'''


@app.route('/api/members/create', methods=['POST'])
def create_member():
    try:
        # Extract data from the request body
        data = request.json
        first_name = data.get('first_name')
        last_name = data.get('last_name')
        email = data.get('email')
        phone = data.get('phone')
        status = data.get('status')

        # Create a new Member object
        new_member = Member(first_name=first_name, last_name=last_name, email=email, phone=phone, status=status)

        # Add the new member to the database session
        db.session.add(new_member)
        # Commit the session to persist the changes
        db.session.commit()

        return jsonify({'message': 'Member account created successfully'})
    except Exception as e:
        # Rollback the session in case of any exception
        db.session.rollback()
        return jsonify({'error': str(e)}), 500


'''This API adds an employee based on the information passed from the front end to the'''


@app.route('/api/add-employee', methods=['POST'])
def add_employee():
    try:
        data = request.json
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return jsonify({'error': 'Both username and password are required'}), 400

        # Query the database to find the member by username and password
        member_info = db.session.query(Member, MemberSensitiveInfo). \
            join(MemberSensitiveInfo, Member.memberID == MemberSensitiveInfo.memberID). \
            filter(MemberSensitiveInfo.username == username, MemberSensitiveInfo.password == password).first()

        # If member information is found
        if member_info:
            member, sensitive_info = member_info
            response = {
                'memberID': member.memberID,
                'first_name': member.first_name,
                'last_name': member.last_name,
                'email': member.email,
                'phone': member.phone,
                'status': member.status,
                'join_date': member.join_date,
                'SSN': sensitive_info.SSN,
                'driverID': sensitive_info.driverID,
                'cardInfo': sensitive_info.cardInfo
            }
            return jsonify(response)
        else:
            return jsonify({'error': 'Member not found or credentials invalid'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# payment

'''This API is used to insert NEW or MODIFY payment data from a customer based on the method and information passed along side of the request'''


@app.route('/api/payments/<int:member_id>', methods=['GET', 'POST'])
def manage_payments(member_id):
    if request.method == 'GET':
        try:
            # Retrieve payment information for the given memberID
            payments = Payments.query.filter_by(memberID=member_id).all()
            payments_info = [{'paymentID': payment.paymentID,
                              'paymentStatus': payment.paymentStatus,
                              'paymentPerMonth': payment.paymentPerMonth,
                              'financeLoanAmount': payment.financeLoanAmount,
                              'loanRatePercentage': payment.loanRatePercentage,
                              'valuePaid': payment.valuePaid,
                              'valueToPay': payment.valueToPay,
                              'initialPurchase': payment.initialPurchase,
                              'lastPayment': payment.lastPayment,
                              'creditScore': payment.creditScore,
                              'income': payment.income,
                              'paymentType': payment.paymentType,
                              'cardNumber': payment.cardNumber,
                              'expirationDate': payment.expirationDate,
                              'CVV': payment.CVV,
                              'routingNumber': payment.routingNumber,
                              'bankAcctNumber': payment.bankAcctNumber} for payment in payments]

            return jsonify(payments_info)
        except Exception as e:
            return jsonify({'error': str(e)}), 500

    elif request.method == 'POST':
        try:
            # Extract data from the request body
            data = request.json
            payment_status = data.get('paymentStatus')
            payment_per_month = data.get('paymentPerMonth')
            finance_loan_amount = data.get('financeLoanAmount')
            loan_rate_percentage = data.get('loanRatePercentage')
            value_paid = data.get('valuePaid')
            value_to_pay = data.get('valueToPay')
            initial_purchase = data.get('initialPurchase')
            last_payment = data.get('lastPayment')
            credit_score = data.get('creditScore')
            income = data.get('income')
            payment_type = data.get('paymentType')
            card_number = data.get('cardNumber')
            expiration_date = data.get('expirationDate')
            cvv = data.get('CVV')
            routing_number = data.get('routingNumber')
            bank_acct_number = data.get('bankAcctNumber')

            # Check if the member already has payment information
            existing_payment = Payments.query.filter_by(memberID=member_id).first()

            if existing_payment:
                # Update existing payment information
                existing_payment.paymentStatus = payment_status
                existing_payment.paymentPerMonth = payment_per_month
                existing_payment.financeLoanAmount = finance_loan_amount
                existing_payment.loanRatePercentage = loan_rate_percentage
                existing_payment.valuePaid = value_paid
                existing_payment.valueToPay = value_to_pay
                existing_payment.initialPurchase = initial_purchase
                existing_payment.lastPayment = last_payment
                existing_payment.creditScore = credit_score
                existing_payment.income = income
                existing_payment.paymentType = payment_type
                existing_payment.cardNumber = card_number
                existing_payment.expirationDate = expiration_date
                existing_payment.CVV = cvv
                existing_payment.routingNumber = routing_number
                existing_payment.bankAcctNumber = bank_acct_number

            else:
                # Create new payment information
                new_payment = Payments(memberID=member_id,
                                       paymentStatus=payment_status,
                                       paymentPerMonth=payment_per_month,
                                       financeLoanAmount=finance_loan_amount,
                                       loanRatePercentage=loan_rate_percentage,
                                       valuePaid=value_paid,
                                       valueToPay=value_to_pay,
                                       initialPurchase=initial_purchase,
                                       lastPayment=last_payment,
                                       creditScore=credit_score,
                                       income=income,
                                       paymentType=payment_type,
                                       cardNumber=card_number,
                                       expirationDate=expiration_date,
                                       CVV=cvv,
                                       routingNumber=routing_number,
                                       bankAcctNumber=bank_acct_number)
                db.session.add(new_payment)

            # Commit changes to the database
            db.session.commit()

            return jsonify({'message': 'Payment information updated successfully'}), 200
        except Exception as e:
            # Rollback the session in case of any exception
            db.session.rollback()
            return jsonify({'error': str(e)}), 500


@app.route('/api/service-appointments', methods=['GET', 'POST'])
def service_appointments():
    if request.method == 'GET':
        # get request, we return all data form service appointments
        appointments = ServiceAppointment.query.all()

        appointments_info = [{
            'appointment_id': appointment.appointment_id,
            'memberID': appointment.memberID,
            'technician_id': appointment.technician_id,
            'appointment_date': appointment.appointment_date,
            'service_name': appointment.service_name
        } for appointment in appointments]

        return jsonify(appointments_info)

    elif request.method == 'POST':
        # post request we are deleting the row for service appointments for cancellation
        # takes in 2 values, Appointment ID and a cancellation value. make it a 1
        data = request.json
        appointment_id_to_cancel = data.get('appointment_id')
        cancellation_value = data.get('cancelValue')

        if appointment_id_to_cancel is None or cancellation_value is None:
            return jsonify({'error': 'Both appointment_id and cancelValue parameters are required.'}), 400

        # cancelation value takes in 1 to confirm it is getting cancelled or else it doesnt get removed.
        if cancellation_value != '1':
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


@app.route('/api/current-bids', methods=['GET', 'POST'])
def current_bids():
    if request.method == 'GET':
        # Retrieve information about cars with active bids
        cars_with_bids = db.session.query(Cars.make, Cars.model, Cars.VIN_carID,
                                          Purchases.paymentType, Purchases.bidValue) \
            .join(Purchases, Cars.VIN_carID == Purchases.VIN_carID) \
            .filter(Purchases.paymentType == 'BID', Purchases.bidStatus == 'Processing') \
            .all()

        # Format
        response = [{
            'make': car.make,
            'model': car.model,
            'VIN_carID': car.VIN_carID,
            'paymentType': purchase.paymentType,
            'bidValue': purchase.bidValue
        } for car, purchase in cars_with_bids]

        return jsonify(response)

    elif request.method == 'POST':
        # we want to either confirm or reject the bid
        data = request.json
        VIN_carID = data.get('VIN_carID')
        bidStatus = data.get('bidStatus')  # pass "Confirmed" or "Denied"

        # Check if both parameters are provided
        if not (VIN_carID and bidStatus):
            return jsonify({'error': 'Both VIN_carID and bidStatus parameters are required.'}), 400

        # Update the bid status
        try:
            purchase = Purchases.query.filter_by(VIN_carID=VIN_carID, paymentType='BID').first()
            if purchase:
                purchase.bidStatus = bidStatus
                db.session.commit()
                return jsonify({'message': 'Bid status updated successfully'}), 200
            else:
                return jsonify({'error': 'No bid found for the specified car'}), 404
        except Exception as e:
            return jsonify({'error': str(e)}), 500
