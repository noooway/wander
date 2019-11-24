from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, url_for, current_app
)
from werkzeug.exceptions import abort
from wander.auth import login_required

import json
import plotly
import plotly.graph_objects as go
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
    time_period_radio_to_col = {'days': 'date',
                                'weeks': 'weekstart',
                                'months': 'monthstart'}
    default_time_period = 'weeks'
    time_period_radio = request.form.get('time_period', default_time_period)
    time_period = time_period_radio_to_col[time_period_radio]
    grouped_df = current_app.data_sources['revenue']
    grouped_df = grouped_df[[time_period, 'revenue']]
    grouped_df = grouped_df.groupby(time_period).sum()
    grouped_df = grouped_df.reset_index()
    fig = go.Figure(
        data = [go.Scatter(x = grouped_df[time_period],
                           y = grouped_df["revenue"],
                           mode = 'markers+lines')],
        layout = go.Layout(title="Revenue")
    )
    return fig.to_json()


@bp.route('/overview/regs', methods=['POST'])
@login_required
def regs_plot():
    time_period_radio_to_col = {'days': 'date',
                                'weeks': 'weekstart',
                                'months': 'monthstart'}
    default_time_period = 'weeks'
    time_period_radio = request.form.get('time_period', default_time_period)
    time_period = time_period_radio_to_col[time_period_radio]
    grouped_df = current_app.data_sources['regs']
    grouped_df = grouped_df[[time_period, 'regs']]
    grouped_df = grouped_df.groupby(time_period).sum()
    grouped_df = grouped_df.reset_index()
    fig = go.Figure(
        data = [go.Scatter(x = grouped_df[time_period],
                           y = grouped_df['regs'],
                           mode = 'markers+lines')],
        layout = go.Layout(title="Registrations")
    )
    return fig.to_json()


@bp.route('/overview/inst_to_regs_conv', methods=['POST'])
@login_required
def inst_to_regs_conv_plot():
    time_period_radio_to_col = {'days': 'date',
                                'weeks': 'weekstart',
                                'months': 'monthstart'}
    default_time_period = 'weeks'
    time_period_radio = request.form.get('time_period', default_time_period)
    time_period = time_period_radio_to_col[time_period_radio]
    grouped_df = current_app.data_sources['inst_to_regs_conv']
    grouped_df = grouped_df[[time_period, 'installs_count', 'regs_count']]
    grouped_df = grouped_df.groupby(time_period).sum()
    grouped_df = grouped_df.reset_index()
    grouped_df['inst_to_regs_conv'] = \
        grouped_df['installs_count'] / grouped_df['regs_count']
    fig = go.Figure(
        data = [go.Scatter(x = grouped_df[time_period],
                           y = grouped_df['inst_to_regs_conv'],
                           mode = 'markers+lines')],
        layout = go.Layout(title="Installs to Regs Conversion",
                           yaxis=dict(tickformat=',.0%',))
    )
    return fig.to_json()


@bp.route('/overview/first_sales', methods=['POST'])
@login_required
def first_sales_plot():
    time_period_radio_to_col = {'days': 'date',
                                'weeks': 'weekstart',
                                'months': 'monthstart'}
    default_time_period = 'weeks'
    time_period_radio = request.form.get('time_period', default_time_period)
    time_period = time_period_radio_to_col[time_period_radio]
    grouped_df = current_app.data_sources['first_sales']
    grouped_df = grouped_df[[time_period, 'first_sales']]
    grouped_df = grouped_df.groupby(time_period).sum()
    grouped_df = grouped_df.reset_index()
    fig = go.Figure(
        data = [go.Scatter(x = grouped_df[time_period],
                           y = grouped_df['first_sales'],
                           mode = 'markers+lines')],
        layout = go.Layout(title="First Sales")
    )
    return fig.to_json()


@bp.route('/overview/regs_to_first_sales_conv', methods=['POST'])
@login_required
def regs_to_first_sales_conv_plot():
    time_period_radio_to_col = {'days': 'date',
                                'weeks': 'weekstart',
                                'months': 'monthstart'}
    default_time_period = 'weeks'
    time_period_radio = request.form.get('time_period', default_time_period)
    time_period = time_period_radio_to_col[time_period_radio]
    grouped_df = current_app.data_sources['regs_to_first_sales_conv']
    grouped_df = grouped_df[[time_period, 'first_sales', 'regs']]
    grouped_df = grouped_df.groupby(time_period).sum()
    grouped_df = grouped_df.reset_index()
    grouped_df['regs_to_first_sales_conv'] = \
        grouped_df['first_sales'] / grouped_df['regs']
    fig = go.Figure(
        data = [go.Scatter(x = grouped_df[time_period],
                           y = grouped_df['regs_to_first_sales_conv'],
                           mode = 'markers+lines')],
        layout = go.Layout(title="Regs to First Sales Conversion",
                           yaxis=dict(tickformat=',.0%',))
    )
    return fig.to_json()


@bp.route('/overview/sales', methods=['POST'])
@login_required
def sales_plot():
    time_period_radio_to_col = {'days': 'date',
                                'weeks': 'weekstart',
                                'months': 'monthstart'}
    default_time_period = 'weeks'
    time_period_radio = request.form.get('time_period', default_time_period)
    time_period = time_period_radio_to_col[time_period_radio]
    grouped_df = current_app.data_sources['sales']
    grouped_df = grouped_df[[time_period, 'sales']]
    grouped_df = grouped_df.groupby(time_period).sum()
    grouped_df = grouped_df.reset_index()
    fig = go.Figure(
        data = [go.Scatter(x = grouped_df[time_period],
                           y = grouped_df['sales'],
                           mode = 'markers+lines')],
        layout = go.Layout(title="Sales")
    )
    return fig.to_json()


@bp.route('/overview/first_sales_to_second_sales_conv', methods=['POST'])
@login_required
def first_sales_to_second_sales_conv_plot():
    time_period_radio_to_col = {'days': 'date',
                                'weeks': 'weekstart',
                                'months': 'monthstart'}
    default_time_period = 'weeks'
    time_period_radio = request.form.get('time_period', default_time_period)
    time_period = time_period_radio_to_col[time_period_radio]
    grouped_df = current_app.data_sources['first_sales_to_second_sales_conv']
    grouped_df = grouped_df[[time_period, 'second_sales', 'first_sales']]
    grouped_df = grouped_df.groupby(time_period).sum()
    grouped_df = grouped_df.reset_index()
    grouped_df['first_sales_to_second_sales_conv'] = \
        grouped_df['second_sales'] / grouped_df['first_sales']
    fig = go.Figure(
        data = [go.Scatter(x = grouped_df[time_period],
                           y = grouped_df['first_sales_to_second_sales_conv'],
                           mode = 'markers+lines')],
        layout = go.Layout(title="First Sales to Second Sales Conversion",
                           yaxis=dict(tickformat=',.0%',))
    )
    return fig.to_json()
