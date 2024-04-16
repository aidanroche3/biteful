from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


flags = Blueprint('flags', __name__)

@flags.route('/flags/<review_id>', methods=['GET'])
def get_flags (review_id):

    query = 'SELECT firstName, lastName, description, createdAt, reviewedByAdmin FROM ReviewFlags JOIN Owner ON ReviewFlags.ownerID = Owner.ownerID WHERE reviewID = ' + str(review_id)
    current_app.logger.info(query)

    cursor = db.get_db().cursor()
    cursor.execute(query)
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    if the_data :
        for row in the_data:
            json_data.append(dict(zip(column_headers, row)))
    else :
        return jsonify({"error": "Review not found"}), 404
    return jsonify(json_data)

@flags.route('/flags/<review_id>', methods=['POST'])
def add_new_flag(review_id):
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    description = the_data['description']
    ownerID = the_data['ownerID']

    # Constructing the query
    query = 'insert into ReviewFlags (reviewID, description, ownerID) values ("'
    query += str(review_id) + '", "'
    query += description + '", "'
    query += str(ownerID) + '")'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

@flags.route('/flags/<review_id>', methods=['PUT'])
def update_flag(review_id):
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    adminID = the_data['adminID']
    reviewedByAdmin = the_data['reviewedByAdmin']

    # Constructing the query
    query = 'update ReviewFlags set '
    query += 'adminID = "' + str(adminID) + '",'
    query += 'reviewedByAdmin = "' + reviewedByAdmin + '" '
    query += 'where reviewID = "' + str(review_id) + '"'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

@flags.route('/flags/<review_id>', methods=['DELETE'])
def delete_flag(review_id):
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    ownerID = the_data['ownerID']

    # Constructing the query
    query = 'delete from ReviewFlags '
    query += 'where reviewID = "' + str(review_id) + '" '
    query += 'and ownerID = "' + str(ownerID) + '"'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'
