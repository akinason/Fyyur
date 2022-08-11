import json
from flask import jsonify, render_template, url_for, redirect, request, flash
import flask 

from app import app, db 
from forms import * 
from models import Show, Venue, Artist



#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return render_template('pages/home.html')


#  Venues
#  ----------------------------------------------------------------

@app.route('/venues')
def venues():
  
  venues = Venue.query.order_by('city', 'state').all()
  
  temp = {}
  data = []
  
  for venue in venues:
    key = f"{venue.city}{venue.state}".lower().replace(' ', '')
    v = {'id': venue.id, "name": venue.name, "num_upcoming_shows": venue.num_upcoming_shows()}
    
    if key in temp.keys():
      temp[key]['venues'].append(v)
    else:
      temp[key] = {"city": venue.city, 'state': venue.state, "venues": [v]}
  
  for _, v in temp.items():
    data.append(v)
  
  return render_template('pages/venues.html', areas=data)


@app.route('/venues/search', methods=['POST'])
def search_venues():
  # seach for Hop should return "The Musical Hop".
  # search for "Music" should return "The Musical Hop" and "Park Square Live Music & Coffee"
  
  search_term = request.form.get('search_term')
  venues = Venue.query.filter(Venue.name.ilike(f'%{search_term}%')).all()

  response = {
    "count": len(venues),
    "data": [{"id": v.id, "name": v.name, "num_upcoming_shows": v.num_upcoming_shows()} for v in venues]
  }
  
  return render_template('pages/search_venues.html', results=response, search_term=search_term)

@app.route('/venues/<int:venue_id>')
def show_venue(venue_id):
  # shows the venue page with the given venue_id
  data = Venue.query.get_or_404(venue_id)
  return render_template('pages/show_venue.html', venue=data)

#  Create Venue
#  ----------------------------------------------------------------

@app.route('/venues/create', methods=['GET'])
def create_venue_form():
  form = VenueForm()
  return render_template('forms/new_venue.html', form=form)

@app.route('/venues/create', methods=['POST'])
def create_venue_submission():
  form = VenueForm()
  if form.validate_on_submit():
    venue = Venue()
    form.populate_obj(venue)
    db.session.add(venue)
    db.session.commit()
    flash('Venue ' + request.form['name'] + ' was successfully listed!')
  else:
    flash('An error occurred. Venue ' + request.form.get('name') + ' could not be listed.')
    return render_template('forms/new_venue.html', form=form)
  
  return redirect(url_for('venues'))


@app.route('/venues/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):

  venue = Venue.query.filter_by(id=venue_id).one()
  db.session.delete(venue)
  db.session.commit()

  return redirect(url_for('index'))


#  Artists
#  ----------------------------------------------------------------
@app.route('/artists')
def artists():
  artists = Artist.query.all()
  data = [{"id": a.id, "name": a.name} for a in artists]
  return render_template('pages/artists.html', artists=data)


@app.route('/artists/search', methods=['POST'])
def search_artists():
  search_term = request.form.get('search_term', '')
  artists = Artist.query.filter(Artist.name.ilike(f'%{search_term}%'))
  response = {
    "count": artists.count(),
    "data": [{"id": a.id, "name": a.name, "num_upcoming_shows": a.upcoming_shows_count} for a in artists.all()]
  }

  return render_template('pages/search_artists.html', results=response, search_term=search_term)


@app.route('/artists/<int:artist_id>')
def show_artist(artist_id):
  artist: Artist = Artist.query.get_or_404(artist_id)
  data = {
    "id": artist.id,
    "name": artist.name,
    "city": artist.city,
    "state": artist.state,
    "phone": artist.phone,
    "website": artist.website_link,
    "facebook_link": artist.facebook_link,
    "seeking_venue": artist.seeking_venue,
    "seeking_description": artist.seeking_description,
    "image_link": artist.image_link,
    "past_shows": [{
      "venue_id": s.venue.id, "venue_name": s.venue.name, "venue_image": s.venue.image_link, "start_time": str(s.start_time)
    } for s in artist.past_shows],
    "upcoming_shows": [{
       "venue_id": s.venue.id, "venue_name": s.venue.name, "venue_image": s.venue.image_link, "start_time": str(s.start_time)
    } for s in artist.upcoming_shows],
    "past_shows_count": artist.past_shows_count,
    "upcoming_shows_count": artist.upcoming_shows_count,
  }
  
  return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@app.route('/artists/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
  artist = Artist.query.get_or_404(artist_id)
  form = ArtistForm(obj=artist)
  return render_template('forms/edit_artist.html', form=form, artist=artist)


@app.route('/artists/<int:artist_id>/edit', methods=['POST'])
def edit_artist_submission(artist_id):
  
  artist = Artist.query.get_or_404(artist_id)
  form = ArtistForm()
  if form.validate_on_submit():
    form.populate_obj(artist)
    db.session.add(artist)
    db.session.commit()
    flash(f'Artist {form.name.data} successfully updated.')
  else:
    flash('An error occured, artist {form.name.data} could not be updated.')
    render_template('forms/edit_artist.html', form=form, artist=artist)
  
  return redirect(url_for('show_artist', artist_id=artist_id))


@app.route('/venues/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
  venue = Venue.query.get_or_404(venue_id)
  form = VenueForm(obj=venue)
  return render_template('forms/edit_venue.html', form=form, venue=venue)


@app.route('/venues/<int:venue_id>/edit', methods=['POST'])
def edit_venue_submission(venue_id):
  venue = Venue.query.get_or_404(venue_id)
  form = VenueForm()
  if form.validate_on_submit():
    form.populate_obj(venue)
    db.session.add(venue)
    db.session.commit()
  else:
    flash(f"The venue {venue.name} could not be updated.")
    return redirect(url_for('edit_venue', venue_id=venue.id))
  
  return redirect(url_for('show_venue', venue_id=venue_id))


#  Create Artist
#  ----------------------------------------------------------------

@app.route('/artists/create', methods=['GET'])
def create_artist_form():
  form = ArtistForm()
  return render_template('forms/new_artist.html', form=form)


@app.route('/artists/create', methods=['POST'])
def create_artist_submission():
  # called upon submitting the new artist listing form
  # on successful db insert, flash success
  
  form = ArtistForm()
  if form.validate_on_submit():
    artist = Artist()
    form.populate_obj(artist)
    db.session.add(artist)
    db.session.commit()
    flash('Artist ' + request.form['name'] + ' was successfully listed!')
  else:
    flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
    return render_template('forms/new_artist.html', form=form)
  
  return redirect(url_for('index'))


#  Shows
#  ----------------------------------------------------------------

@app.route('/shows')
def shows():
  # displays list of shows at /shows
  shows = Show.query.order_by('id').all()
  data = [{
    "venue_id": show.venue.id, "venue_name": show.venue.name, "artist_id": show.artist_id, "artist_name": show.artist.name,
    "artist_image_link": show.artist.image_link, "start_time": str(show.start_time)
  } for show in shows]
  return render_template('pages/shows.html', shows=data)


@app.route('/shows/create')
def create_shows():
  # renders form. do not touch.
  form = ShowForm()
  return render_template('forms/new_show.html', form=form)


@app.route('/shows/create', methods=['POST'])
def create_show_submission():
  # called to create new shows in the db, upon submitting new show listing form
  # on successful db insert, flash success
  
  show = Show()
  form = ShowForm()
  if form.validate_on_submit():
    form.populate_obj(show)
    db.session.add(show)
    db.session.commit()
    flash('Show was successfully listed!')
  else:
    flash('An error occurred. Show could not be listed.')
    return render_template('forms/new_show.html', form=form)
  
  return redirect(url_for('index'))
