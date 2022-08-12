from flask import (
    Blueprint,
    render_template,
    redirect,
    request,
    url_for,
    flash
)

from models import Venue
from app import db 
from forms import VenueForm


bp = Blueprint('venue', __name__, url_prefix='/venues')


@bp.route('/')
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


@bp.route('/search', methods=['POST'])
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


@bp.route('/<int:venue_id>')
def show_venue(venue_id):
    # shows the venue page with the given venue_id
    data = Venue.query.get_or_404(venue_id)
    return render_template('pages/show_venue.html', venue=data)


#  Create Venue
#  ----------------------------------------------------------------

@bp.route('/create', methods=['GET'])
def create_venue_form():
    form = VenueForm()
    return render_template('forms/new_venue.html', form=form)


@bp.route('/create', methods=['POST'])
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


@bp.route('/<venue_id>', methods=['DELETE'])
def delete_venue(venue_id):
    venue = Venue.query.filter_by(id=venue_id).one()
    db.session.delete(venue)
    db.session.commit()

    return redirect(url_for('index'))


@bp.route('/<int:venue_id>/edit', methods=['GET'])
def edit_venue(venue_id):
    venue = Venue.query.get_or_404(venue_id)
    form = VenueForm(obj=venue)
    return render_template('forms/edit_venue.html', form=form, venue=venue)


@bp.route('/<int:venue_id>/edit', methods=['POST'])
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

