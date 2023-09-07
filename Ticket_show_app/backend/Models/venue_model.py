from routes import db 
import datetime
class Venue(db.Model):
    __tablename__ = 'venues'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(50), nullable=False)
    location = db.Column(db.String(50), nullable=False)
    capacity = db.Column(db.Integer, nullable=False)
    show= db.relationship("Show", backref='venue', lazy='dynamic')
    created_at = db.Column(db.DateTime, nullable=False,default=datetime.datetime.utcnow)