from flask import Blueprint, request, jsonify, make_response, current_app
import json
from src import db


owners = Blueprint('owners', __name__)

@owners.route('/owners/<restaurantID>', methods=['GET'])
def get_owner_details(restaurantID):
    cursor = db.get_db().cursor()
    query = '''
        SELECT ownerID
        FROM OwnerDetails
        WHERE restaurantID = %s
    '''
    cursor.execute(query, (restaurantID,))
    column_headers = [x[0] for x in cursor.description]
    json_data = []
    the_data = cursor.fetchall()
    if the_data:
        json_data.append(dict(zip(column_headers, the_data[0])))
    else:
        return jsonify({"error": "Restaurant not found"}), 404
    return jsonify(json_data)