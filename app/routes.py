# app/routes.py

from datetime import datetime
from flask import jsonify, request
from sqlalchemy import Text, text, func
from . import app
from .models import *

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
    sql = "select * from Addons;"
    with db.engine.connect() as connection:
        result = connection.execute(text(sql))
        result = result.fetchall()
        addon_information = [dict(row._mapping) for row in result]
        return jsonify(addon_information)


'''This API returns all information on all vehicles in the database'''
@app.route('/api/vehicles', methods=['GET'])
def vehicle_information():
    sql = "select * from Cars;"
    with db.engine.connect() as connection:
        result = connection.execute(text(sql))
        result = result.fetchall()
        addon_information = [dict(row._mapping) for row in result]
        return jsonify(addon_information)


'''This API returns all information on a specific vehicle based on their VIN number which is passed from the front end to the backend'''
@app.route('/api/vehicles/<string:VIN_carID>', methods=['GET'])
def vehicle(VIN_carID):
    sql = "select * from Cars where Cars.VIN_carID = :VIN_carID;"
    with db.engine.connect() as connection:
        result = connection.execute(text(sql), {'VIN_carID': VIN_carID})
        result = result.fetchall()
        addon_information = [dict(row._mapping) for row in result]
        return jsonify(addon_information)


'''This API returns all employees and their information'''
@app.route('/api/employees', methods=['GET'])
def get_all_employees():
    sql = "select * from Employee;"
    with db.engine.connect() as connection:
        result = connection.execute(text(sql))
        result = result.fetchall()
        addon_information = [dict(row._mapping) for row in result]
        return jsonify(addon_information)


'''This API returns a specific employee based on their email address and password.'''
@app.route('/api/employees/<string:email>/<string:passwd>', methods=['GET'])
def employee(email, passwd):
    sql = """
        SELECT * FROM Employee
        INNER JOIN EmployeeSensitiveInfo ON Employee.employeeID = EmployeeSensitiveInfo.employeeID
        WHERE Employee.email = :email AND EmployeeSensitiveInfo.password = :passwd;
        """
    with db.engine.connect() as connection:
        result = connection.execute(text(sql), {'email': email, 'passwd': passwd})
        result = result.fetchall()
        addon_information = [dict(row._mapping) for row in result]
        return jsonify(addon_information)


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

    sql = """
    INSERT INTO Employee (firstname, lastname, email, phone, address, employeeType)
    VALUES (:firstname, :lastname, :email, :phone, :address, :employeeType)
    """
    with db.engine.connect() as connection:
        connection.execute(text(sql), {
            'firstname': firstname,
            'lastname': lastname,
            'email': email,
            'phone': phone,
            'address': address,
            'employeeType': employee_type
        })

    return jsonify({'message': 'Employee account created successfully'})


'''Retrieves all the members and their information'''
@app.route('/api/members', methods=['GET'])
def get_all_members():
    sql = "select * from Member;"
    with db.engine.connect() as connection:
        result = connection.execute(text(sql))
        result = result.fetchall()
        addon_information = [dict(row._mapping) for row in result]
        return jsonify(addon_information)


'''This API returns a specific member by their username and password passed from the front end to the backend (here)'''
@app.route('/api/members/<string:username>/<string:passwd>', methods=['GET'])
def member(username, passwd):
    sql = """
        SELECT * FROM Member
        INNER JOIN MemberSensitiveInfo ON Member.memberID = MemberSensitiveInfo.memberID
        WHERE MemberSensitiveInfo.username = ? AND MemberSensitiveInfo.password = ?;
        """
    with db.engine.connect() as connection:
        result = connection.execute(text(sql), {'email': username, 'passwd': passwd})
        result = result.fetchall()
        addon_information = [dict(row._mapping) for row in result]
        return jsonify(addon_information)


'''This API creates an employee based on the information passed from the front end to the backend (here)'''
@app.route('/api/members', methods=['POST'])
def create_member():
    # Extract data from the request body
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    phone = data.get('phone')
    status = data.get('status')

    # Insert the new member into the DB
    sql = """
    INSERT INTO Member (first_name, last_name, email, phone, status)
    VALUES (:first_name, :last_name, :email, :phone, :status)
    """
    with db.engine.connect() as connection:
        connection.execute(text(sql), {
            'first_name': first_name,
            'last_name': last_name,
            'email': email,
            'phone': phone,
            'status': status
        })

    return jsonify({'message': 'Member account created successfully'})


'''This API adds an employee based on the information passed from the front end to the'''

@app.route('/api/add-employee', methods=['POST'])
def add_employee():
    data = request.json
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    email = data.get('email')
    phone = data.get('phone')
    address = data.get('address')
    employeeType = data.get('employeeType');
    sql = """
            INSERT INTO Employee (first_name, last_name, email, phone, address, employeeType)
            VALUES (:store_id, :first_name, :last_name, :email, :phone, :address_id, :employeeType)
          """

    with db.engine.connect() as connection:
        connection.execute(text(sql), {'first_name': firstname, 'last_name': lastname,
                                       'email': email, 'phone': phone, 'address': address,
                                       'employeeType': employeeType})
        connection.commit()

    return jsonify({'message': 'Customer added successfully'})


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
