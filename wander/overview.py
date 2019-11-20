from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, url_for, current_app
)
from werkzeug.exceptions import abort
from wander.auth import login_required

import json
import plotly
import plotly.graph_objects as go
import plotly.express as px
import numpy as np


bp = Blueprint('overview', __name__)


@bp.route('/overview')
@login_required
def overview():
    revenue_json = revenue_plot()
    regs_json = regs_plot()
    inst_to_regs_conv_json = inst_to_regs_conv_plot()
    first_sales_json = first_sales_plot()
    regs_to_first_sales_conv_json = regs_to_first_sales_conv_plot()
    sales_json = sales_plot()
    first_sales_to_second_sales_conv_json = first_sales_to_second_sales_conv_plot()
    #
    plots = {
        'revenue': revenue_json,
        'regs': regs_json,
        'inst_to_regs_conv': inst_to_regs_conv_json,
        'first_sales': first_sales_json,
        'regs_to_first_sales_conv': regs_to_first_sales_conv_json,
        'sales': sales_json,
        'first_sales_to_second_sales_conv': first_sales_to_second_sales_conv_json}
    return render_template('overview/overview.html',
                           title='Overview',
                           plots=plots)


@bp.route('/overview/revenue', methods=['POST'])
@login_required
def revenue_plot():
    default_time_period = 'weeks'
    timeperiod = request.form.get('time_period', default_time_period)
    print(timeperiod)
    fig = px.line(current_app.data_sources['revenue'], x="date", y="revenue",
                  title="Revenue",
                  labels=dict(date="Date", revenue="Revenue, $"))
    fig.update_layout(yaxis=dict(scaleanchor="x", scaleratio=0.8))
    fig.update_traces(mode='markers+lines')
    #fig.update_layout(width=800)
    return fig.to_json()


@bp.route('/overview/regs', methods=['POST'])
@login_required
def regs_plot():
    fig = px.line(current_app.data_sources['regs'], x="date", y="regs",
                  title="Registrations",
                  labels=dict(date="Date", regs="Registrations"))
    fig.update_traces(mode='markers+lines')
    return fig.to_json()


@bp.route('/overview/inst_to_regs_conv', methods=['POST'])
@login_required
def inst_to_regs_conv_plot():
    fig = px.line(current_app.data_sources['inst_to_regs_conv'],
                  x="date", y="inst_to_regs_conv",
                  title="Installs to Regs Conversion",
                  labels=dict(date="Date",
                              inst_to_regs_conv="Conversion, %"))
    fig.update_layout(yaxis=dict(tickformat=',.0%',))
    fig.update_traces(mode='markers+lines')
    return fig.to_json()


@bp.route('/overview/first_sales', methods=['POST'])
@login_required
def first_sales_plot():
    fig = px.line(current_app.data_sources['first_sales'],
                  x="date", y="first_sales",
                  title="First Sales",
                  labels=dict(date="Date", first_sales="First Sales"))
    fig.update_traces(mode='markers+lines')
    return fig.to_json()


@bp.route('/overview/regs_to_first_sales_conv', methods=['POST'])
@login_required
def regs_to_first_sales_conv_plot():
    fig = px.line(current_app.data_sources['regs_to_first_sales_conv'],
                  x="date", y="regs_to_first_sales_conv",
                  title="Regs to First Sales Conversion",
                  labels=dict(date="Date",
                              regs_to_first_sales_conv="Conversion, %"))
    fig.update_layout(yaxis=dict(tickformat=',.0%',))
    fig.update_traces(mode='markers+lines')
    return fig.to_json()


@bp.route('/overview/sales', methods=['POST'])
@login_required
def sales_plot():
    fig = px.line(current_app.data_sources['sales'],
                  x="date", y="sales",
                  title="Sales",
                  labels=dict(date="Date", sales="Sales"))
    fig.update_traces(mode='markers+lines')
    return fig.to_json()


@bp.route('/overview/first_sales_to_second_sales_conv', methods=['POST'])
@login_required
def first_sales_to_second_sales_conv_plot():
    fig = px.line(current_app.data_sources['first_sales_to_second_sales_conv'],
                  x="date", y="first_sales_to_second_sales_conv",
                  title="First Sales to Second Sales Conversion",
                  labels=dict(date="Date",
                              first_sales_to_second_sales_conv="Conversion, %"))
    fig.update_layout(yaxis=dict(tickformat=',.0%',))
    fig.update_traces(mode='markers+lines')
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
