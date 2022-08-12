from datetime import datetime

from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    url_for,
    flash
)

from app import db
from forms import ArtistForm
from models import Venue, Artist, Show

bp = Blueprint('artist', __name__, url_prefix='/artists')


#  Artists
#  ----------------------------------------------------------------
@bp.route('/')
def artists():
    artists = Artist.query.all()
    data = [{"id": a.id, "name": a.name} for a in artists]
    return render_template('pages/artists.html', artists=data)


@bp.route('/search', methods=['POST'])
def search_artists():
    search_term = request.form.get('search_term', '')
    artists = Artist.query.filter(Artist.name.ilike(f'%{search_term}%'))
    response = {
        "count": artists.count(),
        "data": [{"id": a.id, "name": a.name, "num_upcoming_shows": a.upcoming_shows_count} for a in artists.all()]
    }

    return render_template('pages/search_artists.html', results=response, search_term=search_term)


@bp.route('/<int:artist_id>')
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
        "past_shows": db.session.query(
            Show.id,
            db.func.to_char(Show.start_time, "YYYY-MM-DD HH24:MI:SS").label('start_time'),
            Venue.id.label('venue_id'), Venue.name.label('venue_name'), Venue.image_link.label('venue_image_link'),
        ).join(Venue).filter(Show.artist_id == artist_id).filter(Show.start_time < datetime.today()).all(),
        "upcoming_shows": db.session.query(
            Show.id,
            db.func.to_char(Show.start_time, "YYYY-MM-DD HH24:MI:SS").label('start_time'),
            Venue.id.label('venue_id'), Venue.name.label('venue_name'), Venue.image_link.label('venue_image_link'),
        ).join(Venue).filter(Show.artist_id == artist_id).filter(Show.start_time >= datetime.today()).all(),
        "past_shows_count": db.session.query(Show).filter(
            Show.artist_id == artist_id
        ).filter(
            Show.start_time < datetime.today()
        ).count(),
        "upcoming_shows_count": db.session.query(Show).filter(
            Show.artist_id == artist_id
        ).filter(
            Show.start_time > datetime.today()
        ).count(),
    }

    return render_template('pages/show_artist.html', artist=data)


#  Update
#  ----------------------------------------------------------------
@bp.route('/<int:artist_id>/edit', methods=['GET'])
def edit_artist(artist_id):
    artist = Artist.query.get_or_404(artist_id)
    form = ArtistForm(obj=artist)
    return render_template('forms/edit_artist.html', form=form, artist=artist)


@bp.route('/<int:artist_id>/edit', methods=['POST'])
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

    return redirect(url_for('artist.show_artist', artist_id=artist_id))


#  Create Artist
#  ----------------------------------------------------------------

@bp.route('/create', methods=['GET'])
def create_artist_form():
    form = ArtistForm()
    return render_template('forms/new_artist.html', form=form)


@bp.route('/create', methods=['POST'])
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
        print(form.errors)
        flash('An error occurred. Artist ' + request.form['name'] + ' could not be listed.')
        return render_template('forms/new_artist.html', form=form)

    return redirect(url_for('index'))


