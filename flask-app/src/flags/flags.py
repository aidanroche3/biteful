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
    for row in the_data:
        json_data.append(dict(zip(column_headers, row)))
    return jsonify(json_data)