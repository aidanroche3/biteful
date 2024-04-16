from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


restaurants = Blueprint('restaurants', __name__)

@restaurants.route('/restaurants', methods=['GET'])
def get_restaurants():
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    # use cursor to query the database for a list of products
    cursor.execute('SELECT name, cuisine, address, website, openingTime, closingTime, images, restaurantID FROM Restaurant')

    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in 
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers. 
    if theData :
        for row in theData:
            json_data.append(dict(zip(column_headers, row)))
    else :
        return jsonify({"error": "Restaurant not found"}), 404
    return jsonify(json_data)

@restaurants.route('/restaurants/<id>', methods=['GET'])
def get_restaurants_detail(id):
    cursor = db.get_db().cursor()
    query = '''
        SELECT *
        FROM Restaurant
        WHERE restaurantID = %s
    '''
    cursor.execute(query, (id,))
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    if the_data:
        json_data.append(dict(zip(column_headers, the_data[0])))
    else:
        return jsonify({"error": "Restaurant not found"}), 404
    return jsonify(json_data)

@restaurants.route('/restaurants', methods=['POST'])
def add_restaurant():
    data = request.json
    query = '''
        INSERT INTO restaurants (name, cuisine, openingTime, closingTime, phoneNumber, dineIn, website, address)
        VALUES (%s, %s, %s, %s)
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (data['name'], data['cuisine'], data['openingTime'], data['closingTime'], data['phoneNumber'], data['dineIn'], data['website'], data['address']))
    db.get_db().commit()
    return jsonify({"success": True}), 201

@restaurants.route('/restaurants/<id>', methods=['PUT'])
def update_restaurant(id):
    data = request.json
    query = '''
        UPDATE restaurants
        SET openingTime = %s, closingTime = %s, phoneNumber = %s, dineIn = %s, website = %s
        WHERE restaurantID = %s
    '''
    cursor = db.get_db().cursor()
    cursor.execute(query, (data['openingTime'], data['closingTime'], data['phoneNumber'], data['dineIn'], data['website'], id))
    if cursor.rowcount == 0:
        return jsonify({"error": "Update failed or restaurant not found"}), 404
    db.get_db().commit()
    return jsonify({"success": True}), 201
        
    
@restaurants.route('/restaurants/<id>', methods=['DELETE'])
def delete_restaurant(id):
    cursor = db.get_db().cursor()
    query = '''
        DELETE FROM restaurants
        WHERE restaurantID = %s
    '''
    cursor.execute(query, (id,))
    db.get_db().commit()
    if cursor.rowcount > 0:
        return jsonify({"success": True}), 201
    else:
        return jsonify({"error": "Delete failed or restaurant not found"}), 404
    
@restaurants.route('/restaurants/search', methods=['GET'])
def search_restaurants():
    #get search term for query parameters
    search_term = request.args.get('query', '')
    if not search_term:
        return jsonify({"error": "No search term provided"}), 400
    life_string = f"%{search_term}%"
    cursor = db.get_db().cursor()
    query = '''
        SELECT *
        FROM restaurants
        WHERE name LIKE %s OR address LIKE %s OR cuisine LIKE %s
    '''
    cursor.execute(query, (life_string, life_string, life_string))
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)