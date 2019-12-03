from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, url_for, current_app
)
from wander.auth import login_required


bp = Blueprint('drafts', __name__)


@bp.route('/drafts/updated_src')
@login_required
def releases():
    if current_app.data_sources['updated']:
        return current_app.data_sources['updated']['vals']
    else:
        return 'please stand by'
