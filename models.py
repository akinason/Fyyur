from app import db 
from datetime import date 


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Venue(db.Model):
    __tablename__ = 'Venue'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    genres = db.Column(db.ARRAY(db.String))
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    address = db.Column(db.String(120))
    phone = db.Column(db.String(120), nullable=True)
    website_link = db.Column(db.String(500), nullable=True)
    image_link = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    seeking_talent = db.Column(db.Boolean, default=True)
    seeking_description = db.Column(db.String, nullable=True)
    shows = db.relationship('Show', backref='venue', lazy=True)
    
    def num_upcoming_shows(self) -> int:
        return Show.query.filter(
                Show.venue_id == self.id, Show.start_time >= date.today()
            ).count()


class Artist(db.Model):
    __tablename__ = 'Artist'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    city = db.Column(db.String(120))
    state = db.Column(db.String(120))
    phone = db.Column(db.String(120), nullable=True)
    genres = db.Column(db.String(120))
    image_link = db.Column(db.String(500), nullable=True)
    facebook_link = db.Column(db.String(120), nullable=True)
    website_link = db.Column(db.String(500), nullable=True)
    seeking_venue = db.Column(db.Boolean, default=True)
    seeking_description = db.Column(db.String, nullable=True)
    shows = db.relationship('Show', backref='artist', lazy=True)
    
    @property
    def upcoming_shows_count(self) -> int:
        return Show.query.filter(
                Show.artist_id == self.id, Show.start_time >= date.today()
            ).count()
    
    @property
    def past_shows_count(self) -> int:
        return Show.query.filter(
                Show.artist_id == self.id, Show.start_time < date.today()
            ).count()

    @property
    def past_shows(self):
        return db.session.query(Show).join(Venue).filter(
                Show.artist_id == self.id, Show.start_time < date.today()
            ).all()
    
    @property
    def upcoming_shows(self) -> int:
        return Show.query.filter(
                Show.artist_id == self.id, Show.start_time >= date.today()
            ).all()
    
    
    
class Show(db.Model):
    __tablename__ = 'Show'
    
    id = db.Column(db.Integer, primary_key=True)
    artist_id = db.Column(db.Integer, db.ForeignKey('Artist.id'), nullable=False)
    venue_id = db.Column(db.Integer, db.ForeignKey('Venue.id'), nullable=False)
    start_time = db.Column(db.DateTime, nullable=False)
    