from flask import Blueprint, request, jsonify, current_app
import json
from src import db

bookmarks = Blueprint('bookmarks', __name__)

# Retrieve all bookmarks for a specific user
@bookmarks.route('/bookmarks/<int:user_id>', methods=['GET'])
def get_bookmarks(user_id):
    cursor = db.get_db().cursor()
    query = 'SELECT * FROM bookmarks WHERE user_id = %s'
    cursor.execute(query, (user_id,))
    column_headers = [x[0] for x in cursor.description]
    bookmarks_data = cursor.fetchall()
    json_data = [dict(zip(column_headers, row)) for row in bookmarks_data]
    return jsonify(json_data)

# Add a new bookmark for a user to a specific restaurant
@bookmarks.route('/bookmarks/<int:user_id>/<int:restaurant_id>', methods=['POST'])
def add_bookmark(user_id, restaurant_id):
    cursor = db.get_db().cursor()
    query = 'INSERT INTO bookmarks (user_id, restaurant_id) VALUES (%s, %s)'
    cursor.execute(query, (user_id, restaurant_id))
    db.get_db().commit()
    return jsonify({"message": "Bookmark added successfully"}), 201

# Delete a specific bookmark
@bookmarks.route('/bookmarks/<int:user_id>/<int:restaurant_id>', methods=['DELETE'])
def delete_bookmark(user_id, restaurant_id):
    cursor = db.get_db().cursor()
    query = 'DELETE FROM bookmarks WHERE user_id = %s AND restaurant_id = %s'
    cursor.execute(query, (user_id, restaurant_id))
    db.get_db().commit()
    return jsonify({"message": "Bookmark deleted successfully"}), 200

# Retrieve a specific bookmark by user and restaurant
@bookmarks.route('/bookmarks/details/<int:user_id>/<int:restaurant_id>', methods=['GET'])
def get_bookmark_details(user_id, restaurant_id):
    cursor = db.get_db().cursor()
    query = 'SELECT * FROM bookmarks WHERE user_id = %s AND restaurant_id = %s'
    cursor.execute(query, (user_id, restaurant_id))
    column_headers = [x[0] for x in cursor.description]
    bookmark_data = cursor.fetchone()
    if bookmark_data:
        json_data = dict(zip(column_headers, bookmark_data))
        return jsonify(json_data)
    else:
        return jsonify({"error": "Bookmark not found"}), 404

# Count of bookmarks for a specific restaurant
@bookmarks.route('/bookmarks/count/<int:restaurant_id>', methods=['GET'])
def count_bookmarks(restaurant_id):
    cursor = db.get_db().cursor()
    query = 'SELECT COUNT(*) as count FROM bookmarks WHERE restaurant_id = %s'
    cursor.execute(query, (restaurant_id,))
    result = cursor.fetchone()
    return jsonify({"count": result['count'] if result else 0})

# List of users who bookmarked a specific restaurant
@bookmarks.route('/bookmarks/users/<int:restaurant_id>', methods=['GET'])
def users_who_bookmarked(restaurant_id):
    cursor = db.get_db().cursor()
    query = 'SELECT user_id FROM bookmarks WHERE restaurant_id = %s'
    cursor.execute(query, (restaurant_id,))
    users = cursor.fetchall()
    user_ids = [user['user_id'] for user in users]
    return jsonify({"user_ids": user_ids})

# Update a specific bookmark
@bookmarks.route('/bookmarks/<int:user_id>/<int:bookmark_id>', methods=['PUT'])
def update_bookmark(user_id, bookmark_id):
    data = request.get_json()
    new_restaurant_id = data.get('restaurant_id')
    cursor = db.get_db().cursor()

    # Check if the new restaurant ID is provided in the request, then update
    if new_restaurant_id:
        query = 'UPDATE bookmarks SET restaurant_id = %s WHERE user_id = %s AND id = %s'
        cursor.execute(query, (new_restaurant_id, user_id, bookmark_id))
        db.get_db().commit()
        return jsonify({"message": "Bookmark updated successfully"}), 200
    else:
        return jsonify({"error": "Missing new restaurant ID"}), 400

