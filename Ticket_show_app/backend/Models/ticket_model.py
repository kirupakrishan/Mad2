from routes import db
import datetime


class Ticket(db.Model):
    __tablename__='Ticket'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String)
    seats = db.Column(db.Integer)
    price = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False) 
    show_id = db.Column(db.Integer, db.ForeignKey('show.id'), nullable=False) 
    created_at = db.Column(db.DateTime, nullable=False,default=datetime.datetime.utcnow)
    
