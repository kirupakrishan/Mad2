from routes import home, db, redis_cli
from flask import request, jsonify, Response , send_file
from Models.ticket_model import Ticket
from Models.show_model import Show
from Models.venue_model import Venue
from helpers import token_required
import json
import os
import base64
import pytz
from datetime import datetime
from flask import Blueprint

booking = Blueprint('booking', __name__)


#Get all Booked shows in a venue
# @booking.route('/show/getall/<user_id>', methods=['GET'])
# @token_required
# def getall_shows(current_user,user_id):
#     tickets = Ticket.query.filter_by(user_id=user_id).all()
#     show_data = {}
#     for ticket in tickets :
#         data={}
#         data['id'] = ticket.id
#         data['price'] = ticket.price
#         data['seats'] = ticket.seats
#         data['show_id'] = ticket.show.id
#         data['name'] = ticket.show.name
#         data['time'] = str(ticket.show.show_time).split(' ')[1]
#         data['date'] = str(ticket.show.show_time).split(' ')[0]
#         data['image'] = ticket.show.img
#         data['tags'] = ticket.show.tags
#         data['rating'] = ticket.show.rating
#         data['venue_name'] = ticket.show.venue.name
#         data['venue_location'] = ticket.show.venue.location
#         show_data[str(ticket.id)] = data
#     return jsonify({'booked': show_data})


#get show Image
@booking.route("/show/get/img/<show_id>")
def return_files_tut(show_id):
    show = Show.query.filter_by(id=show_id).first()
    try:
        return send_file('../static/images/'+ show.img)
    except Exception as e:
        return str(e)


# #Route To display All Booked Shows


# #Route for All Venues with Shows
@booking.route('/show/getall', methods=['GET'])
@token_required
def get_blogs(current_user):
    cache_output = {}
    db_output = {}
    ticket_keys = redis_cli.keys(f'ticket:*')
    if ticket_keys:
        print('HIT REDIS CACHE')
        print(ticket_keys)
       # Filter the blog keys to only include those belonging to the current user
        user_ticket_keys = [key for key in ticket_keys if json.loads(
            redis_cli.get(key))['user_id'] == current_user.id]

        # Use the Redis get() method to get the values of the filtered blog keys
        show_values = [redis_cli.get(key) for key in user_ticket_keys]

        # Deserialize the blog values from JSON to Python objects
        tickets = [json.loads(value) for value in show_values]
        for ticket in tickets :
            data={}
            data['id'] = ticket['id']
            data['price'] = ticket['price']
            data['seats'] = ticket['seats']
            data['show_id'] = ticket['show_id']
            data['name'] = ticket['name']
            data['time'] = ticket['time']
            data['date'] = ticket['date']
            data['image'] = ticket['image']
            data['tags'] = ticket['tags']
            data['rating'] = ticket['rating']
            data['venue_name'] = ticket['venue_name']
            data['venue_location'] = ticket['venue_location']
            cache_output[str(ticket['id'])] = data
    if not len(cache_output):
        print('HIT DATABASE')
        tickets = Ticket.query.filter_by(user_id=current_user.id).all()
        for ticket in tickets :
            data={}
            data['id'] = ticket.id
            data['price'] = ticket.price
            data['seats'] = ticket.seats
            data['show_id'] = ticket.show.id
            data['name'] = ticket.show.name
            data['time'] = str(ticket.show.show_time).split(' ')[1]
            data['date'] = str(ticket.show.show_time).split(' ')[0]
            data['image'] = ticket.show.img
            data['tags'] = ticket.show.tags
            data['rating'] = ticket.show.rating
            data['venue_name'] = ticket.show.venue.name
            data['venue_location'] = ticket.show.venue.location
            db_output[str(ticket.id)] = data
    if not len(cache_output) and not len(db_output):
        return Response(
            response=json.dumps({"message": "No Blogs Exists"}),
            status=401,
            mimetype="application/json"
        )

    return jsonify({'booked': cache_output if len(cache_output) else db_output})
