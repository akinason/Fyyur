from flask import (
    Blueprint,
    render_template,
    redirect,
    url_for,
    flash
)

from models import Show
from app import db
from forms import ShowForm


bp = Blueprint('show', __name__, url_prefix='/shows')


#  Shows
#  ----------------------------------------------------------------

@bp.route('/')
def shows():
    # displays list of shows at /shows
    shows = Show.query.order_by('id').all()
    data = [{
        "venue_id": show.venue.id, "venue_name": show.venue.name, "artist_id": show.artist_id, "artist_name": show.artist.name,
        "artist_image_link": show.artist.image_link, "start_time": str(show.start_time)
    } for show in shows]
    return render_template('pages/shows.html', shows=data)


@bp.route('/create')
def create_shows():
    # renders form. do not touch.
    form = ShowForm()
    return render_template('forms/new_show.html', form=form)


@bp.route('/create', methods=['POST'])
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
