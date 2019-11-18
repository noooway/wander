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

# import when project is started with 'flask run' from top-level dir
from example_data import example_data

bp = Blueprint('overview', __name__)


@bp.route('/overview')
@login_required
def overview():
    revenue_json = revenue_plot()
    regs_json = regs_plot()
    inst_to_regs_conv_json = inst_to_regs_conv_plot()
    plots = {'revenue': revenue_json,
             'regs': regs_json,
             'inst_to_regs_conv': inst_to_regs_conv_json}
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
    fig.update_layout(yaxis=dict(scaleanchor="x", scaleratio=0.8))
    #fig.update_layout(width=800)
    return fig.to_json()


@bp.route('/overview/regs', methods=['POST'])
@login_required
def regs_plot():
    fig = px.line(example_data.regs_df, x="date", y="regs",
                  title="Registrations",
                  labels=dict(date="Date", regs="Registrations"))
    return fig.to_json()


@bp.route('/overview/inst_to_regs_conv', methods=['POST'])
@login_required
def inst_to_regs_conv_plot():
    fig = px.line(example_data.inst_to_regs_conv_df,
                  x="date", y="inst_to_regs_conv",
                  title="Installs to Regs Conversion",
                  labels=dict(date="Date",
                              inst_to_regs_conv="Conversion, %"))
    fig.update_layout(yaxis=dict(tickformat=',.0%',))
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
