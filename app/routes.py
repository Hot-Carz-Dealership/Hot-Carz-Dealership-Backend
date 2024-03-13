# app/routes.py

from datetime import datetime
from flask import jsonify, request
from sqlalchemy import Text, text, func
from . import app
from .models import *



# Route to fetch movie list based on requested movie title
@app.route('/films_by_title', methods=['GET'])
def films_by_title():
    # Get the genre name from the request or use an empty string if not provided
    title = request.args.get('title', '')

    with db.engine.connect() as connection:
        # SQL query to retrieve films by title
        sql = """
            SELECT *
            FROM film
            WHERE title LIKE :title
        """

        # Execute the query
        result = connection.execute(text(sql), {'title': '%' + title + '%'})

        # Fetch all results
        results = result.fetchall()

        # Convert results to a list of dictionaries
        films = [dict(row._mapping)for row in results]

        return jsonify({'films': films})
    
    
# Route to add a customer
@app.route('/add_customer', methods=['POST'])
def add_customer():
    # Extracting data from the request
    data = request.json
    store_id = 1 #We are combining both stores for the sake of the project timeline
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')
    # address_id = data.get('address_id')
    address_id = 1 # Setting everyones address to 1 for the time being
    # SQL query to insert a new customer
    sql = """
        INSERT INTO customer (store_id, first_name, last_name, email, address_id)
        VALUES (:store_id, :first_name, :last_name, :email, :address_id)
    """

    with db.engine.connect() as connection:
        # Execute the query
        connection.execute(text(sql), {'store_id': store_id, 'first_name': first_name, 'last_name': last_name,
                                       'email': email, 'address_id': address_id})
        connection.commit()

    return jsonify({'message': 'Customer added successfully'})

# Route to update a customer
@app.route('/update_customer/<int:customer_id>', methods=['PUT'])
def update_customer(customer_id):
    # Extracting data from the request
    data = request.json
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    email = data.get('email')

    # SQL query to update a customer
    sql = """
        UPDATE customer
        SET first_name = :first_name, last_name = :last_name, email = :email
        WHERE customer_id = :customer_id
    """

    with db.engine.connect() as connection:
        # Execute the query
        connection.execute(text(sql), {'first_name': first_name, 'last_name': last_name,
                                       'email': email, 'customer_id': customer_id})
        connection.commit()

    return jsonify({'message': 'Customer updated successfully'})

#Route to Delete a Customer
@app.route('/delete_customer/<int:customer_id>', methods=['DELETE']) 
def delete_customer(customer_id):
    # SQL query to delete a customer
    sql = """
        DELETE FROM customer
        WHERE customer_id = :customer_id
    """

    with db.engine.connect() as connection:
        # Execute the query
        connection.execute(text(sql), {'customer_id': customer_id})
        connection.commit()

    return jsonify({'message': 'Customer deleted successfully'})


# Route to fetch rental information for a customer
@app.route('/customer_rentals/<int:customer_id>', methods=['GET'])
def get_customer_rentals(customer_id):
    # SQL query to fetch rental information for the customer
    sql = """
        SELECT 
            rental.rental_id,
            film.title,
            rental.inventory_id,
            rental.rental_date,
            rental.return_date
        FROM 
            rental
        INNER JOIN 
            inventory ON rental.inventory_id = inventory.inventory_id
        INNER JOIN 
            film ON inventory.film_id = film.film_id
        WHERE 
            rental.customer_id = :customer_id
        ORDER BY 
            rental.return_date IS NULL DESC, rental.return_date DESC
    """

    with db.engine.connect() as connection:
        # Execute the query
        result = connection.execute(text(sql), {'customer_id': customer_id})
        # Fetch all results
        results = result.fetchall()

        # Convert results to a list of dictionaries
        rentals = [dict(row._mapping)for row in results]


        return jsonify({'rentals': rentals})
    