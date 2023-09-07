from routes import app,db , redis_cli
from flask import request, jsonify, Response , send_file
from Models.user_model import Users
from Models.venue_model import Venue
from Models.show_model import Show
from Models.ticket_model import Ticket
from collections import defaultdict
from sqlalchemy.orm import aliased
import csv
from io import StringIO
import json
import os
import base64
import pytz
from datetime import datetime
from routes import photos
from helpers import token_required, token_generate
from flask import Blueprint

admin_routes = Blueprint('admin_routes', __name__)


# Route for admin Login
@admin_routes.route('/login', methods=["POST"])
def login():
    # getting login info from the form
    login = {
        "username": request.form["username"],
        "password": request.form["password"]
    }

    # using try catch for sys error and check pass
    try:
        user = Users.query.filter_by(username=login["username"]).first()
        if not user:
            return jsonify({'message': "Invalid Credentials"})
        if user.password == login["password"]:
            token = token_generate(login["username"])

            return jsonify({"token": token}), 200

        else:
            return jsonify({"message": "Invalid Credentials"}), 404

    except:
        return jsonify({"message": "Invalid Credentials"}), 404

# ROute for admin Logout
# Route for admin Create Venue
@admin_routes.route('/venue/create', methods=['POST'])
@token_required
def create_venue(current_user):
    venue = request.json 
    name = venue['vname']
    location = venue['vlocation']
    capacity = venue['vcapacity']
    new_venue = Venue(name=name,location = location,capacity = capacity)
    db.session.add(new_venue)
    db.session.commit()
    
    return jsonify({'message': 'Venue created'})
# Route for admin Read Venue
@admin_routes.route('/venue/get/<venue_id>', methods=['GET'])
@token_required
def get_venue(current_user,venue_id):
    venue = Venue.query.filter_by(id=venue_id).first()
    if not venue:
        return jsonify({'message': 'No Venue found!'})
    venue_data = {}
    venue_data['id'] = venue.id
    venue_data['name'] = venue.name
    venue_data['location'] = venue.location
    venue_data['capacity'] = venue.capacity
    venue_data['created_at'] = venue.created_at
    return jsonify({'venue': venue_data})
#Read all venues
@admin_routes.route('/venue/getall', methods=['GET'])
@token_required
def getall_venues(current_user):
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

# Route for admin Update Venue
@admin_routes.route('/venue/update/<venue_id>', methods=['PUT'])
@token_required
def update_venue(current_user,venue_id):
    venue = Venue.query.filter_by(id=venue_id).first()
    if not venue:
        return jsonify({'message': 'No venue found!'})
    form = request.json
    venue.name = form['vname']
    venue.location = form['vlocation']
    venue.capacity = form['vcapacity']
    db.session.commit()
    return jsonify({'message': 'Venue updated'}) , 200


# Route for admin Delete Venue

@admin_routes.route('/venue/delete/<venue_id>', methods=['DELETE'])
@token_required
def delete_venue(current_user,venue_id):
    # Check if the blog exists in Redis
    # venue_key = f'venue:{venue_id}'
    # if not redis_cli.exists(venue_key):
    #     return jsonify({'error': 'Blog not found'}), 404
    # # Delete the blog from Redis
    # redis_cli.delete(venue_key)
    venue = Venue.query.filter_by(id=venue_id).first()
    if not venue:
        return jsonify({'message': 'No Venue found!'})
    db.session.delete(venue)
    db.session.commit()
    return jsonify({'message': 'Venue deleted'})


# Route for admin Create Show
@admin_routes.route('/show/create', methods=['POST'])
@token_required
def create_show(current_user):
    vid=int(request.form.get('vid'))
    isvid = Venue.query.filter_by(id=vid).first()
    if(isvid):
        sname=request.form.get('sname')
        stags=request.form.get('stags')
        show_time =datetime.strptime(request.form.get('show_time'), '%Y-%m-%dT%H:%M:%S.%fZ')
        rating=request.form.get('rating')
        image = photos.save(request.files['simg'],name=str(vid)+"-"+sname+".jpeg")
        tickets_available = isvid.capacity 
        new_show = Show(rating=rating,name=sname,tags=stags,show_time=show_time,
                        venue_id=vid,img=image,tickets_booked = 0,tickets_available=tickets_available)
        db.session.add(new_show)
        db.session.commit()
        return jsonify({'message': 'Show Created created'})
    return {'message':'Venue ID Not present','vidAbsent':True}

# Route for admin Read Show
@admin_routes.route('/show/get/<show_id>', methods=['GET'])
@token_required
def get_show(current_user,show_id):
    show = Show.query.filter_by(id=show_id).first()
    if not  show:
        return jsonify({'message': 'No show found!'})
    show_data = {}
    show_data['id'] = show.id
    show_data['name'] = show.name
    show_data['time'] = str(show.show_time).split(' ')[0]
    show_data['date'] = str(show.show_time).split(' ')[1]
    image_path = os.path.join('static', 'images', show.img)
    with open(image_path, 'rb') as f:
        image_data = f.read()
        base64_encoded_data = base64.b64encode(image_data).decode('utf-8')
    show_data['image'] = base64_encoded_data
    show_data['tags'] = show.tags
    show_data['rating'] = show.rating
    show_data['tickets_available'] = show.tickets_available
    show_data['tickets_booked'] = show.tickets_booked
    show_data['venue_id'] = show.venue_id
    return jsonify({'show': show_data})

#Get all shows in a venue
@admin_routes.route('/show/getall/<venue_id>', methods=['GET'])
@token_required
def getall_shows(current_user,venue_id):
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
#get-show image
@admin_routes.route("/show/get/img/<show_id>")
def return_files_tut(show_id):
    show = Show.query.filter_by(id=show_id).first()
    try:
        return send_file('../static/images/'+ show.img)
    except Exception as e:
        return str(e)

# Route for admin Update Show

@admin_routes.route('/show/update/<show_id>', methods=['PUT'])
@token_required
def update_show(current_user,show_id):
    show = Show.query.filter_by(id=show_id).first()
    if not  show:
        return jsonify({'message': 'No show found!'})
    vid=int(request.form.get('vid'))
    print(request.files.get('simg'))
    isvid = Venue.query.filter_by(id=vid).first()
    if(isvid):
        show.name=request.form.get('sname')
        show.tags=request.form.get('stags')
        show.show_time =datetime.strptime(request.form.get('stime'), '%Y-%m-%dT%H:%M:%S.%fZ')
        show.rating=request.form.get('srating')
        show.img = photos.save(request.files.get('simg'),name=str(vid)+"-"+show.name+".jpeg") 
        show.venue_id = vid
        db.session.commit()
        return jsonify({'message': 'Show Created created'})
    return {'message':'Venue ID Not present','vidAbsent':True}

# Route for admin Delete Show
@admin_routes.route('/show/delete/<show_id>', methods=['DELETE'])
@token_required
def delete_show(current_user,show_id):
    # # Check if the blog exists in Redis
    # show_key = f'blog:{show_id}'
    # if not redis_cli.exists(show_key):
    #     return jsonify({'error': 'Blog not found'}), 404
    # # Delete the blog from Redis
    # redis_cli.delete(show_key)
    show = Show.query.filter_by(id=show_id).first()
    if not show:
        return jsonify({'message': 'No Show found!'})
    db.session.delete(show)
    db.session.commit()
    return jsonify({'message': 'Show deleted'})


def generate_csv_report(data, field_names):
    csv_buffer = StringIO()
    csv_writer = csv.DictWriter(csv_buffer, fieldnames=field_names)
    csv_writer.writeheader()
    for item in data:
        csv_writer.writerow(dict(zip(field_names,list(item))))
    csv_data = csv_buffer.getvalue()
    csv_buffer.close()
    return csv_data

@admin_routes.route('/reports/export', methods=['GET'])
@token_required
def export_venue_csv(current_user):
    field_names = ["id", "name", "location", "capacity", "show_count", "total_bookings", "total_revenue", "average_rating"]

    # Alias the Venue and Show tables to distinguish them in the query
    venue_alias = aliased(Venue)
    show_alias = aliased(Show)
    data = db.session.query(
        venue_alias.id,
        venue_alias.name,
        venue_alias.location,
        venue_alias.capacity,
        db.func.count(show_alias.id).label('show_count'),
        db.func.count(Ticket.id).label('total_bookings'),
        db.func.sum(Ticket.price).label('total_revenue'),
        db.func.avg(show_alias.rating).label('average_rating')
    ).join(show_alias, venue_alias.id == show_alias.venue_id).join(Ticket, show_alias.id == Ticket.show_id).group_by(venue_alias.id).all()
    csv_data = generate_csv_report(data, field_names)
    response = Response(csv_data, content_type='text/csv')
    response.headers["Content-Disposition"] = "attachment; filename=venues.csv"
    return response

@admin_routes.route('/reports/tickets_booked_per_show', methods=['GET'])
@token_required
def tickets_booked_report(current_user):
    result = defaultdict(int)
    tickets = Ticket.query.all()
    for ticket in tickets:
        result[ticket.show.name] += ticket.seats
    return {'data':result}

@admin_routes.route('/reports/total_revenue_per_show', methods=['GET'])
@token_required
def total_revenue_report(current_user):
    result = defaultdict(int)
    tickets = Ticket.query.all()
    for ticket in tickets:
        result[ticket.show.name] += ticket.price
    return {'data':result}

@admin_routes.route('/reports/top_rated_shows', methods=['GET'])
@token_required
def top_rated_shows_report(current_user):
    top_shows = Show.query.order_by(Show.rating.desc()).limit(5).all()
    shows = [[x.name,x.id] for x in top_shows]
    return {'data':shows}

@admin_routes.route('/reports/total_tickets_sold', methods=['GET'])
@token_required
def total_tickets_sold_report(current_user):
    total_tickets = db.session.query(db.func.sum(Ticket.seats)).scalar()
    return {'data': total_tickets}

@admin_routes.route('/reports/shows_by_venue', methods=['GET'])
@token_required
def shows_by_venue(current_user):
    result = defaultdict(list)
    
    # Query the Show model to group shows by venue
    shows = Show.query.all()
    for show in shows:
        result[show.venue.name].append(show.name)
    
    return result
@admin_routes.route('/reports/users_with_most_bookings', methods=['GET'])
@token_required
def users_with_most_bookings(current_user,limit=5):
    # Query the Users and Ticket models to find users with most bookings
    users = db.session.query(Users.name, db.func.count(Ticket.id).label('booking_count')) \
                     .join(Ticket) \
                     .group_by(Users.id) \
                     .order_by(db.desc('booking_count')) \
                     .limit(limit) \
                     .all()
    user_list = [list(x) for x in users]
    return {'data':user_list}
@admin_routes.route('/reports/venue_with_highest_sales', methods=['GET'])
@token_required
def venue_with_highest_sales(current_user):
    # Query the Venue and Ticket models to find the venue with the highest ticket sales
    venue = db.session.query(
        Venue.name,
        db.func.sum(Ticket.price).label('total_sales')
    ) \
    .join(Show, Venue.id == Show.venue_id)  \
    .join(Ticket, Show.id == Ticket.show_id) \
    .group_by(Venue.id) \
    .order_by(db.desc('total_sales')) \
    .first()
    venues = [x for x in venue]
    return {'data': venues}


