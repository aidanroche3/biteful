from flask import Blueprint, request, jsonify, current_app
import json
from src import db

reviews = Blueprint('reviews', __name__)

<<<<<<< HEAD
# Get all reviews for a specific restaurant
@reviews.route('/reviews/<int:restaurant_id>', methods=['GET'])
def get_reviews(restaurant_id):
    cursor = db.get_db().cursor()
    query = 'SELECT * FROM reviews WHERE restaurant_id = %s'
    cursor.execute(query, (restaurant_id,))
    column_headers = [x[0] for x in cursor.description]
    review_data = cursor.fetchall()
    json_data = [dict(zip(column_headers, row)) for row in review_data]
    return jsonify(json_data)

# Add a new review
@reviews.route('/reviews/<int:restaurant_id>', methods=['POST'])
def post_review(restaurant_id):
    review_data = request.get_json()
    cursor = db.get_db().cursor()
    query = 'INSERT INTO reviews (restaurant_id, review_text, user_id, rating) VALUES (%s, %s, %s, %s)'
    cursor.execute(query, (restaurant_id, review_data["review_text"], review_data["user_id"], review_data["rating"]))
    db.get_db().commit()
    return jsonify({"message": "Review added successfully"}), 201

# Update a specific review
@reviews.route('/reviews/<int:restaurant_id>/<int:review_id>', methods=['PUT'])
def update_review(restaurant_id, review_id):
    review_data = request.get_json()
    cursor = db.get_db().cursor()
    query = 'UPDATE reviews SET review_text = %s, rating = %s WHERE id = %s AND restaurant_id = %s'
    cursor.execute(query, (review_data["review_text"], review_data["rating"], review_id, restaurant_id))
    db.get_db().commit()
    return jsonify({"message": "Review updated successfully"}), 200

# Delete a specific review
@reviews.route('/reviews/<int:restaurant_id>/<int:review_id>', methods=['DELETE'])
def delete_review(restaurant_id, review_id):
    cursor = db.get_db().cursor()
    query = 'DELETE FROM reviews WHERE id = %s AND restaurant_id = %s'
    cursor.execute(query, (review_id, restaurant_id))
    db.get_db().commit()
    return jsonify({"message": "Review deleted successfully"}), 200

# Get average rating for a specific restaurant
@reviews.route('/reviews/average/<int:restaurant_id>', methods=['GET'])
def get_average_rating(restaurant_id):
    cursor = db.get_db().cursor()
    query = 'SELECT AVG(rating) as average_rating FROM reviews WHERE restaurant_id = %s'
    cursor.execute(query, (restaurant_id,))
    result = cursor.fetchone()
    if result:
        return jsonify({"average_rating": float(result['average_rating']) if result['average_rating'] else None})
    else:
        return jsonify({"error": "No reviews found"}), 404

# Get the most recent review for a specific restaurant
@reviews.route('/reviews/recent/<int:restaurant_id>', methods=['GET'])
def get_most_recent_review(restaurant_id):
    cursor = db.get_db().cursor()
    query = 'SELECT * FROM reviews WHERE restaurant_id = %s ORDER BY created_at DESC LIMIT 1'
    cursor.execute(query, (restaurant_id,))
    column_headers = [x[0] for x in cursor.description]
    review_data = cursor.fetchone()
    if review_data:
        json_data = dict(zip(column_headers, review_data))
        return jsonify(json_data)
    else:
        return jsonify({"error": "No reviews found"}), 404
=======
reviews = Blueprint('reviews', __name__)

@reviews.route('/reviews/<restaurant_id>', methods=['GET'])
def get_reviews(restaurant_id):
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    query = 'SELECT firstName, lastName, text, timeStamp, price, rating, images '
    query += 'FROM Review JOIN ReviewDetails ON Review.reviewID = ReviewDetails.reviewID '
    query += 'JOIN Diner ON ReviewDetails.dinerID = Diner.dinerID '
    query += 'WHERE Review.restaurantID = ' + str(restaurant_id) 

    # use cursor to query the database for a list of products
    cursor.execute(query)

    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # create an empty dictionary object to use in 
    # putting column headers together with data
    json_data = []

    # fetch all the data from the cursor
    theData = cursor.fetchall()

    # for each of the rows, zip the data elements together with
    # the column headers. 
    for row in theData:
        json_data.append(dict(zip(column_headers, row)))

    return jsonify(json_data)

@reviews.route('/reviews/<restaurant_id>', methods=['POST'])
def add_new_review(restaurant_id):
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    text = the_data['text']
    price = the_data['price']
    rating = the_data['rating']
    images = the_data['images']
    reviewID = the_data['reviewID']
    dinerID = the_data['dinerID']

    # Constructing the query
    query = 'insert into Review (text, price, rating, images, restaurantID, reviewID) values ("'
    query += text + '", "'
    query += str(price) + '", "'
    query += str(rating) + '", "'
    query += images + '", "'
    query += str(restaurant_id) + '", "'
    query += str(reviewID) + '")'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    # Constructing the query
    query = 'insert into ReviewDetails (reviewID, dinerID) values ("'
    query += str(reviewID) + '", "'
    query += str(dinerID) + '")'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

@reviews.route('/reviews', methods=['PUT'])
def update_review():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    text = the_data['text']
    price = the_data['price']
    rating = the_data['rating']
    images = the_data['images']
    reviewID = the_data['reviewID']

    # Constructing the query
    query = 'UPDATE Review SET '
    query += 'text = "' + text + '", '
    query += 'price = ' + str(price) + ', '
    query += 'rating = ' + str(rating) + ', '
    query += 'images = "' + images + '" '
    query += 'WHERE reviewID = ' + str(reviewID)
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'

@reviews.route('/reviews', methods=['DELETE'])
def delete_review():
    
    # collecting data from the request object 
    the_data = request.json
    current_app.logger.info(the_data)

    #extracting the variable
    reviewID = the_data['reviewID']

    # Constructing the query
    query = 'DELETE FROM ReviewDetails WHERE reviewID = ' + str(reviewID)
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    # Constructing the query
    query = 'DELETE FROM Review WHERE reviewID = ' + str(reviewID)
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()
    
    return 'Success!'
>>>>>>> 9c7c7392f4d0a138aa34d569b45040e4033fcf10
