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
    # Extract parameters from the request
    data = request.json
    testdrive_id = data.get('testdrive_id')
    confirmation = data.get('confirmation')

    # Check if both parameters are provided
    if testdrive_id is None or confirmation is None:
        return jsonify({'error': 'Both testdrive_id and confirmation parameters are required.'}), 400

    # Map confirmation string to enum value
    confirmation_value = 'Confirmed' if confirmation == '1' else 'Denied'

    # Perform the update operation
    update_sql = """
    UPDATE TestDrive
    SET confirmation = :confirmation_value
    WHERE testdrive_id = :testdrive_id;
    """

    # Execute the update operation
    with db.engine.connect() as connection:
        connection.execute(text(update_sql), {'confirmation_value': confirmation_value, 'testdrive_id': testdrive_id})

    return jsonify({'message': 'Confirmation updated successfully'})


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
        member_info = db.session.query(Member, MemberSensitiveInfo).\
            join(MemberSensitiveInfo, Member.memberID == MemberSensitiveInfo.memberID).\
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
        member_info = db.session.query(Member, MemberSensitiveInfo).\
            join(MemberSensitiveInfo, Member.memberID == MemberSensitiveInfo.memberID).\
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
        # Retrieve payment information from the retrieved memberID
        sql = """
        SELECT * FROM Payments
        WHERE memberID = :member_id
        """
        with db.engine.connect() as connection:
            result = connection.execute(text(sql), {'member_id': member_id})
            payments_info = [dict(row) for row in result]

        return jsonify(payments_info)

    elif request.method == 'POST':
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

        # Check if the member already has payment information to decide whether to modify or create a new row
        sql_check = """
        SELECT * FROM Payments
        WHERE memberID = :member_id
        """
        with db.engine.connect() as connection:
            result = connection.execute(text(sql_check), {'member_id': member_id})
            existing_payment = result.fetchone()

        if existing_payment:
            # If we're here we are updating the information as they alreayd have existiing data here
            sql_update = """
            UPDATE Payments
            SET paymentStatus = :payment_status,
                paymentPerMonth = :payment_per_month,
                financeLoanAmount = :finance_loan_amount,
                loanRatePercentage = :loan_rate_percentage,
                valuePaid = :value_paid,
                valueToPay = :value_to_pay,
                initialPurchase = :initial_purchase,
                lastPayment = :last_payment,
                creditScore = :credit_score,
                income = :income,
                paymentType = :payment_type,
                cardNumber = :card_number,
                expirationDate = :expiration_date,
                CVV = :cvv,
                routingNumber = :routing_number,
                bankAcctNumber = :bank_acct_number
            WHERE memberID = :member_id
            """
            with db.engine.connect() as connection:
                connection.execute(text(sql_update), {
                    'payment_status': payment_status,
                    'payment_per_month': payment_per_month,
                    'finance_loan_amount': finance_loan_amount,
                    'loan_rate_percentage': loan_rate_percentage,
                    'value_paid': value_paid,
                    'value_to_pay': value_to_pay,
                    'initial_purchase': initial_purchase,
                    'last_payment': last_payment,
                    'credit_score': credit_score,
                    'income': income,
                    'payment_type': payment_type,
                    'card_number': card_number,
                    'expiration_date': expiration_date,
                    'cvv': cvv,
                    'routing_number': routing_number,
                    'bank_acct_number': bank_acct_number,
                    'member_id': member_id
                })

        else:
            # If we are here we are creating a new row for new data as there is NO existing data for the user
            sql_insert = """
            INSERT INTO Payments (
                paymentStatus, paymentPerMonth, financeLoanAmount, loanRatePercentage,
                valuePaid, valueToPay, initialPurchase, lastPayment, creditScore,
                income, paymentType, cardNumber, expirationDate, CVV, routingNumber,
                bankAcctNumber, memberID
            )
            VALUES (
                :payment_status, :payment_per_month, :finance_loan_amount, :loan_rate_percentage,
                :value_paid, :value_to_pay, :initial_purchase, :last_payment, :credit_score,
                :income, :payment_type, :card_number, :expiration_date, :cvv, :routing_number,
                :bank_acct_number, :member_id
            )
            """
            with db.engine.connect() as connection:
                connection.execute(text(sql_insert), {
                    'payment_status': payment_status,
                    'payment_per_month': payment_per_month,
                    'finance_loan_amount': finance_loan_amount,
                    'loan_rate_percentage': loan_rate_percentage,
                    'value_paid': value_paid,
                    'value_to_pay': value_to_pay,
                    'initial_purchase': initial_purchase,
                    'last_payment': last_payment,
                    'credit_score': credit_score,
                    'income': income,
                    'payment_type': payment_type,
                    'card_number': card_number,
                    'expiration_date': expiration_date,
                    'cvv': cvv,
                    'routing_number': routing_number,
                    'bank_acct_number': bank_acct_number,
                    'member_id': member_id
                })

        return jsonify({'message': 'Payment information updated successfully'}), 200
