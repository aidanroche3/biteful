from flask import Blueprint, request, jsonify, current_app
import json
from src import db

reviews = Blueprint('reviews', __name__)

# Get all reviews for a specific restaurant
@reviews.route('/reviews/<restaurant_id>', methods=['GET'])
def get_reviews(restaurant_id):
    # get a cursor object from the database
    cursor = db.get_db().cursor()

    query = 'SELECT Review.reviewID, firstName, lastName, text, timeStamp, price, rating, images '
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
    dinerID = the_data['dinerID']

    # Constructing the query
    query = 'INSERT INTO Review (text, price, rating, images, restaurantID) VALUES ("'
    query += text + '", "'
    query += str(price) + '", "'
    query += str(rating) + '", "'
    query += images + '", '
    query += str(restaurant_id) + ')'
    current_app.logger.info(query)

    # executing and committing the insert statement 
    cursor = db.get_db().cursor()
    cursor.execute(query)
    db.get_db().commit()

    query = 'SELECT reviewID FROM Review WHERE text = %s AND restaurantID = %s'
    cursor.execute(query, (text, restaurant_id,))

    # grab the column headers from the returned data
    column_headers = [x[0] for x in cursor.description]

    # fetch all the data from the cursor
    theData = cursor.fetchone()

    json_data = dict(zip(column_headers, theData))

    reviewID = json_data["reviewID"]

    # Constructing the query
    query = 'INSERT INTO ReviewDetails (reviewID, dinerID) VALUES ('
    query += str(reviewID) + ', '
    query += str(dinerID) + ')'
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


# Get average rating for a specific restaurant
@reviews.route('/reviews/average/<restaurant_id>', methods=['GET'])
def get_average_rating(restaurant_id):
    cursor = db.get_db().cursor()
    query = 'SELECT AVG(rating) as average_rating FROM Review WHERE restaurantID = %s'
    cursor.execute(query, (restaurant_id,))
    result = cursor.fetchone()
    if result:
        return jsonify({"average_rating": str(int(result[0]))})
    else:
        return jsonify({"error": "No reviews found"}), 404

# Get the most recent review for a specific restaurant
@reviews.route('/reviews/recent/<restaurant_id>', methods=['GET'])
def get_most_recent_review(restaurant_id):
    cursor = db.get_db().cursor()
    query = 'SELECT * FROM Review WHERE restaurantID = %s ORDER BY timeStamp DESC LIMIT 1'
    cursor.execute(query, (restaurant_id,))
    column_headers = [x[0] for x in cursor.description]
    review_data = cursor.fetchone()
    if review_data:
        json_data = dict(zip(column_headers, review_data))
        return jsonify(json_data)
    else:
        return jsonify({"error": "No reviews found"}), 404