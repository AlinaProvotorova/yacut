from flask import abort, redirect, render_template

from . import app
from .forms import URLMapForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def yacut_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    short_link = form.custom_id.data
    if not short_link or short_link is None or len(short_link) == 0 or short_link == "":
        data = URLMap.get_model_from_bd(url=form.original_link.data)
        if data is not None:
            return render_template('index.html', form=form, short_link=data.short)
        short_link = URLMap.get_unique_short_id()
    URLMap.db_commit(URLMap(
        original=form.original_link.data,
        short=short_link
    ))
    return render_template('index.html', form=form, short_link=short_link)


@app.route('/<short_id>')
def new_link_view(short_id):
    urlmap = URLMap.get_model_from_bd(short_id=short_id)
    if urlmap is None:
        abort(404)
    return redirect(urlmap.original)
