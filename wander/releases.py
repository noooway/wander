from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, url_for, current_app
)
from wander.auth import login_required


bp = Blueprint('releases', __name__)


@bp.route('/releases')
@login_required
def releases():
    return render_template('releases/releases.html',
                           title='Releases',
                           releases=current_app.data_sources['releases'])
