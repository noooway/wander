from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, url_for, current_app
)
from wander.auth import login_required


bp = Blueprint('drafts', __name__)


@bp.route('/drafts/updated_src')
@login_required
def releases():
    print("help!")
    print(current_app.data_sources['updated'])
    if current_app.data_sources['updated'] is not None:
        print('===============')
        print (current_app.data_sources['updated']['vals'])
        return str(current_app.data_sources['updated']['vals'])
    else:
        print ('please stand by')
        return 'please stand by'
