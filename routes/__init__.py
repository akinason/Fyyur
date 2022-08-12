from flask import render_template

from app import app, db
from models import Venue, Artist

from routes.artists import bp as artist_bp
from routes.shows import bp as show_bp
from routes.venues import bp as venue_bp

# Register blueprints
app.register_blueprint(venue_bp)
app.register_blueprint(show_bp)
app.register_blueprint(artist_bp)


@app.route('/')
def index():
  # Show latest 5 venues and artists
  venues = Venue.query.order_by(Venue.id.desc()).limit(5).all()
  artists = Artist.query.order_by(Artist.id.desc()).limit(5).all()
  return render_template('pages/home.html', venues=venues, artists=artists)
