from flask import abort, flash, redirect, render_template

from . import app
from .forms import URLMapForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def yacut_view():
    form = URLMapForm()
    data = URLMap.get_model_from_bd(url=form.original_link.data)
    short_link = None
    if form.validate_on_submit():
        if data is None:
            short_link = URLMap.get_unique_short_id(form.custom_id.data)
            URLMap.db_commit(URLMap(
                original=form.original_link.data,
                short=short_link
            ))
            flash('Ваша новая ссылка готова:')
        else:
            short_link = data.short
            flash('Ссылка на страницу была ранее создана:')
    context = {
        'form': form,
        'short_link': short_link
    }
    return render_template('index.html', **context)


@app.route('/<short_id>')
def new_link_view(short_id):
    urlmap = URLMap.get_model_from_bd(short_id=short_id)
    if urlmap is None:
        abort(404)
    return redirect(urlmap.original)
