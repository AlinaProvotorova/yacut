from string import ascii_letters, digits
from random import sample

from flask import abort, flash, redirect, render_template, url_for

from . import app, db
from .forms import URLMapForm
from .models import URLMap


def get_unique_short_id():
    return ''.join(sample(ascii_letters + digits, 6))


def validate_short(short_link=None):
    if not short_link or short_link is None or len(short_link) == 0 or short_link == "":
        short_link = get_unique_short_id()
        while short_link in URLMap.query.filter_by(short=short_link).all():
            short_link = get_unique_short_id()
    return short_link


def db_commit(data):
    db.session.add(data)
    db.session.commit()


@app.route('/', methods=['GET', 'POST'])
def yacut_view():
    form = URLMapForm()
    if form.validate_on_submit():
        data = URLMap.query.filter_by(original=form.original_link.data).first()
        if data is not None:
            flash(url_for('new_link_view', short_id=data.short, _external=True), category='link')
            return render_template('yacut.html', form=form)
        short_link = validate_short(form.custom_id.data)
        db_commit(URLMap(
            original=form.original_link.data,
            short=short_link
        ))
        flash(url_for('new_link_view', short_id=short_link, _external=True), category='new_link')
    return render_template('yacut.html', form=form)


@app.route('/<short_id>')
def new_link_view(short_id):
    urlmap = URLMap.query.filter_by(short=short_id).first()
    if urlmap is None:
        abort(404)
    return redirect(urlmap.original)
