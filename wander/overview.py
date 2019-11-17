from flask import (
    Blueprint, flash, g, redirect, render_template, request, url_for
)
from werkzeug.exceptions import abort
from wander.auth import login_required

import json
import plotly
import plotly.graph_objects as go
import plotly.express as px
import numpy as np

from . import example_data

bp = Blueprint('overview', __name__)


@bp.route('/overview')
@login_required
def overview():
    revenue_json = revenue_plot()
    plots = {'revenue': revenue_json}
    return render_template('overview/overview.html',
                           title='Overview',
                           plots=plots)


@bp.route('/overview/revenue', methods=['POST'])
@login_required
def revenue_plot():
    default_count = 500
    default_color = 'orange'
    count = request.form.get('count', default_count)
    col = request.form.get('color', default_color)
    fig = px.line(example_data.revenue_df, x="date", y="revenue",
                  title="Revenue",
                  labels=dict(date="Date", revenue="Revenue, $"))
    return fig.to_json()





# def revenue_plot():
#     default_count = 500
#     default_color = 'orange'
#     count = request.form.get('count', default_count)
#     col = request.form.get('color', default_color)
#     xScale = np.linspace(0, 100, count)
#     yScale = np.random.randn(count)
#     trace = go.Scatter(
#         x = xScale,
#         y = yScale,
#         line = dict(color=col)
#     )
#     data = [trace]
#     fig = go.Figure(data=data)
#     return fig.to_json()
