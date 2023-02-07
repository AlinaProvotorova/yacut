from flask import abort, flash, redirect, render_template, url_for

from . import app
from .forms import URLMapForm
from .models import URLMap


@app.route('/', methods=['GET', 'POST'])
def yacut_view():
    form = URLMapForm()
    if not form.validate_on_submit():
        return render_template('index.html', form=form)
    try:
        urlmap = URLMap.create(form.original_link.data, form.custom_id.data)
    except ValueError as error:
        flash(message=str(error))
        return render_template('index.html', form=form)
    return render_template(
        'index.html',
        form=form,
        short_link=url_for(
            'new_link_view',
            short_id=urlmap.short,
            _external=True)
    )


@app.route('/<short_id>')
def new_link_view(short_id):
    urlmap = URLMap.get_model_from_bd(short_id=short_id)
    if urlmap is None:
        abort(404)
    return redirect(urlmap.original)
