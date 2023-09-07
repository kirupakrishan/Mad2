from routes import db 
import datetime
class Show(db.Model):
    __tablename__='show'
    id=db.Column(db.Integer , primary_key=True, autoincrement=True)
    img=db.Column(db.String)
    name=db.Column(db.String)
    tags=db.Column(db.String)
    show_time = db.Column(db.DateTime, nullable=False)
    rating=db.Column(db.Integer)
    tickets_booked = db.Column(db.Integer)
    tickets_available = db.Column(db.Integer)
    ticket = db.relationship("Ticket", backref='show', lazy='dynamic')
    venue_id = db.Column(db.Integer, db.ForeignKey('venues.id'), nullable=False)
    
    
