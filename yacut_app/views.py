from string import ascii_letters, digits
from random import sample

from flask import abort, flash, redirect, render_template

from . import app, db
from .forms import URLMapForm
from .models import URLMap


def get_unique_short_id():
    return ''.join(sample(ascii_letters + digits, 6))


@app.route('/', methods=['GET', 'POST'])
def yacut_view():
    form = URLMapForm()
    if form.validate_on_submit():
        data = URLMap.query.filter_by(original=form.original.data).first()
        if data is not None:
            flash("http://127.0.0.1:5000/" + data.short, category='link')
            return render_template('yacut.html', form=form)
        short_link = form.short.data
        if short_link == '':
            short_link = get_unique_short_id()
            while short_link in URLMap.query.filter_by(short=short_link).all():
                short_link = get_unique_short_id()
        if URLMap.query.filter_by(short=short_link).first() is not None:
            flash("Данный вариант короткой ссылки уже есть, придумайте другой", category='info')
            return render_template('yacut.html', form=form)
        db.session.add(URLMap(
            original=form.original.data,
            short=short_link
        ))
        db.session.commit()
        flash("http://127.0.0.1:5000/" + short_link, category='new_link')
        return render_template('yacut.html', form=form)
    return render_template('yacut.html', form=form)


@app.route('/<string:short>')
def new_link_view(short):
    urlmap = URLMap.query.filter_by(short=short).first()
    if urlmap is None:
        abort(404)
    return redirect(urlmap.original)
