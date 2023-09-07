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

home = Blueprint('home', __name__)

#Read all venues
@home.route('/venue/getall', methods=['GET'])
def getall_venues():
    venues = Venue.query.all()
    venue_data = {}
    for venue in venues :
        data={}
        data['id'] = venue.id
        data['name'] = venue.name                                   
        data['location'] = venue.location
        data['capacity'] = venue.capacity
        data['created_at'] = venue.created_at
        venue_data[str(venue.id)] = data
    return jsonify({'venues': venue_data})
#Get all shows in a venue
@home.route('/show/getall/<venue_id>', methods=['GET'])
def getall_shows(venue_id):
    shows = Show.query.filter_by(venue_id=venue_id).all()
    show_data = {}
    for show in shows :
        data={}
        data['id'] = show.id
        data['name'] = show.name
        data['time'] = str(show.show_time).split(' ')[1]
        data['date'] = str(show.show_time).split(' ')[0]
        data['image'] = show.img
        data['tags'] = show.tags
        data['rating'] = show.rating
        data['tickets_available'] = show.tickets_available
        data['tickets_booked'] = show.tickets_booked
        data['venue_id'] = show.venue_id
        show_data[str(show.id)] = data
    return jsonify({'shows': show_data})

#Get queried venue show and rating
@home.route('/search', methods=['GET'])
def getquery_data():
    location = request.args.get('location') 
    is_loc = not(location == 'false')
    show = request.args.get('show') 
    is_show = not (show == 'false')
    rating = request.args.get('rating')
    is_rate = not (rating == 'false')
    if is_loc or show or rating:
        if(is_loc and is_show):
            joined = db.session.query(Venue, Show).join(Show).filter(
                            Venue.location == location,
                            Show.name == show
                    )
        elif(is_loc and is_rate):
            joined = db.session.query(Venue, Show).join(Show).filter(
                            Venue.location == location,
                            Show.rating == rating
                    )
        elif(is_show and is_rate):
            joined = db.session.query(Venue, Show).join(Show).filter(
                            Show.name == show,
                            Show.rating == rating
                    )
        elif(is_loc):
            joined = db.session.query(Venue, Show).join(Show).filter(
                            Venue.location == location
                    )
        elif(is_show):
            joined = db.session.query(Venue, Show).join(Show).filter(
                            Show.name == show
                    )
        elif(is_rate):
            joined = db.session.query(Venue, Show).join(Show).filter(
                            Show.rating == rating
                    )
        elif(is_loc and is_show and is_rate):
            joined = db.session.query(Venue, Show).join(Show).filter(
                            Venue.location == location,
                            Show.name == show,
                            Show.rating == rating
                    )
        venue_data = {}
        show_data = {}
        for venue,show in joined :
            data={}
            data['id'] = venue.id
            data['name'] = venue.name                                   
            data['location'] = venue.location
            data['capacity'] = venue.capacity
            data['created_at'] = venue.created_at
            venue_data[str(venue.id)] = data
            data={}
            if str(venue.id) in show_data.keys():    
                data['id'] = show.id
                data['name'] = show.name
                data['time'] = str(show.show_time).split(' ')[1]
                data['date'] = str(show.show_time).split(' ')[0]
                data['image'] = show.img
                data['tags'] = show.tags
                data['rating'] = show.rating
                data['tickets_available'] = show.tickets_available
                data['tickets_booked'] = show.tickets_booked
                data['venue_id'] = show.venue_id
                show_data[str(venue.id)].append(data)
            else:
                data['id'] = show.id
                data['name'] = show.name
                data['time'] = str(show.show_time).split(' ')[1]
                data['date'] = str(show.show_time).split(' ')[0]
                data['image'] = show.img
                data['tags'] = show.tags
                data['rating'] = show.rating
                data['tickets_available'] = show.tickets_available
                data['tickets_booked'] = show.tickets_booked
                data['venue_id'] = show.venue_id
                show_data[str(venue.id)] = [data]
            print(data)
        return jsonify({'venues': venue_data,'shows': show_data})



    
#get-show image
@home.route("/show/get/img/<show_id>")
def return_files_tut(show_id):
    show = Show.query.filter_by(id=show_id).first()
    try:
        return send_file('../static/images/'+ show.img)
    except Exception as e:
        return str(e)

#Book Movie Tickets
@home.route('/book',methods=['POST'])
@token_required
def book_ticket(current_user):
    name = request.form.get('name') 
    seats = request.form.get('seats')
    price = request.form.get('price')
    user_id = current_user.id
    show_id = request.form.get('show_id')
    show = Show.query.filter_by(id=show_id).first()
    show.tickets_booked = show.tickets_booked + int(seats)
    show.tickets_available = show.tickets_available - int(seats)
    new_ticket = Ticket(name=name,seats=seats,price=price,user_id=user_id,show_id=show_id)
    db.session.add(new_ticket)
    db.session.commit()
    ticket_data = {
                'id': new_ticket.id,
                'price': new_ticket.price,
                'seats': new_ticket.seats,
                'show_id': new_ticket.show.id,
                'user_id':current_user.id,
                'name':new_ticket.show.name,
                'time': str(new_ticket.show.show_time).split(' ')[1],
                'date': str(new_ticket.show.show_time).split(' ')[0],
                'image': new_ticket.show.img,
                'tags': new_ticket.show.tags,
                'rating': new_ticket.show.rating,
                'venue_name': new_ticket.show.venue.name,
                'venue_location': new_ticket.show.venue.location
    }
    redis_cli.set(f'ticket:{ticket_data["id"]}', json.dumps(ticket_data))
    return {"isSuccess":True}



# #Route for Search based on Location/Rating/tag

# @home.route('/search-shows', methods=['GET'])
# @token_required
# def search_user(current_user):
#     # getting the search query from the url
#     search = request.args.get('search')
#     # using try catch for sys error and check pass
#     users = Users.query.filter(
#         Users.username.like("%" + search + "%")).all()
#     if not users:
#         return jsonify({'message': "No Users Found"})
#     output = []
#     for user in users:
#         user_data = {}
#         user_data['u_id'] = user.id
#         user_data['firstName'] = user.firstName
#         user_data['lastName'] = user.lastName
#         user_data['email'] = user.email
#         user_data['username'] = user.username
#         user_data['bio'] = user.bio
#         output.append(user_data)
#     if not len(output):
#         return jsonify({'message': "No Users Found"})
#     return jsonify({'users': output})
