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
    revenue_json = revenue_fig()
    installs_json = installs_fig()
    regs_json = regs_fig()
    online_json = online_fig()
    first_sales_json = first_sales_fig()
    sales_json = sales_fig()
    virtual_currency_spent_json = virtual_currency_spent_fig()
    regs_to_first_sales_json = regs_to_first_sales_fig()
    first_sales_to_second_sales_json = first_sales_to_second_sales_fig()
    #
    plots = {
        'revenue': revenue_json,
        'installs': installs_json,
        'regs': regs_json,
        'online': online_json,
        'first_sales': first_sales_json,
        'sales': sales_json,
        'virtual_currency_spent': virtual_currency_spent_json,
        'regs_to_first_sales': regs_to_first_sales_json,
        'first_sales_to_second_sales': first_sales_to_second_sales_json
    }
    #plots['cohorts_revenue'] = cohorts_revenue_json
    return render_template('overview/overview.html',
                           title='Overview',
                           plots=plots)


@bp.route('/overview/revenue', methods=['POST'])
@login_required
def revenue_fig():
    time_period = determine_time_period(request)
    grouped_df = group_by_time_period(
        current_app.data_sources['revenue'],
        time_period,
        'revenue')
    fig = go.Figure(
        data = [go.Scatter(x = grouped_df[time_period],
                           y = grouped_df['revenue'],
                           mode = 'markers+lines')],
        layout = go.Layout(title = 'Revenue',
                           margin = dict(b=0))
    )
    return fig.to_json()


@bp.route('/overview/installs', methods=['POST'])
@login_required
def installs_fig():
    time_period = determine_time_period(request)
    grouped_df = group_by_time_period(
        current_app.data_sources['installs'],
        time_period,
        'installs')
    fig = go.Figure(
        data = [go.Scatter(x = grouped_df[time_period],
                           y = grouped_df['installs'],
                           mode = 'markers+lines')],
        layout = go.Layout(title = "Installs",
                           margin = dict(l=0, r=0))
    )
    return fig.to_json()


@bp.route('/overview/regs', methods=['POST'])
@login_required
def regs_fig():
    time_period = determine_time_period(request)
    categories = determine_categories(request)
    print(time_period, categories)
    region_cats = categories['regions']
    filtered_df = current_app.data_sources['regs']

    grouped_df = group_by_time_period(
        current_app.data_sources['regs'],
        time_period,
        'regs')
    fig = go.Figure(
        data = [go.Scatter(x = grouped_df[time_period],
                           y = grouped_df['regs'],
                           mode = 'markers+lines')],
        layout = go.Layout(title = "Registrations",
                           margin = dict(l=0, r=0))
    )
    return fig.to_json()


@bp.route('/overview/online', methods=['POST'])
@login_required
def online_fig():
    time_period = determine_time_period(request)
    grouped_df = group_by_time_period(
        current_app.data_sources['online'],
        time_period,
        'online')
    fig = go.Figure(
        data = [go.Scatter(x = grouped_df[time_period],
                           y = grouped_df['online'],
                           mode = 'markers+lines')],
        layout = go.Layout(title = "Online",
                           margin = dict(l=0, r=0))
    )
    return fig.to_json()


@bp.route('/overview/first_sales', methods=['POST'])
@login_required
def first_sales_fig():
    time_period = determine_time_period(request)
    grouped_df = group_by_time_period(
        current_app.data_sources['first_sales'],
        time_period,
        'first_sales')
    fig = go.Figure(
        data = [go.Scatter(x = grouped_df[time_period],
                           y = grouped_df['first_sales'],
                           mode = 'markers+lines')],
        layout = go.Layout(title = "First Sales",
                           margin = dict(l=0, r=0))
    )
    return fig.to_json()


@bp.route('/overview/sales', methods=['POST'])
@login_required
def sales_fig():
    time_period = determine_time_period(request)
    grouped_df = group_by_time_period(
        current_app.data_sources['sales'],
        time_period,
        'sales')
    fig = go.Figure(
        data = [go.Scatter(x = grouped_df[time_period],
                           y = grouped_df['sales'],
                           mode = 'markers+lines')],
        layout = go.Layout(title = "Sales",
                           margin = dict(l=0, r=0))
    )
    return fig.to_json()


@bp.route('/overview/virtual_currency_spent', methods=['POST'])
@login_required
def virtual_currency_spent_fig():
    time_period = determine_time_period(request)
    grouped_df = group_by_time_period(
        current_app.data_sources['virtual_currency_spent'],
        time_period,
        'virtual_currency_spent')
    fig = go.Figure(
        data = [go.Scatter(x = grouped_df[time_period],
                           y = grouped_df['virtual_currency_spent'],
                           mode = 'markers+lines')],
        layout = go.Layout(title = "Virtual Currency Spent",
                           margin = dict(l=0, r=0))
    )
    return fig.to_json()


@bp.route('/overview/inst_to_regs_conv', methods=['POST'])
@login_required
def inst_to_regs_conv_plot():
    time_period = determine_time_period(request)
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


@bp.route('/overview/regs_to_first_sales', methods=['POST'])
@login_required
def regs_to_first_sales_fig():
    time_period = determine_time_period(request)
    grouped_df = current_app.data_sources['regs_to_first_sales']
    grouped_df = grouped_df[[time_period, 'first_sales', 'regs']]
    grouped_df = grouped_df.groupby(time_period).sum()
    grouped_df = grouped_df.reset_index()
    grouped_df['regs_to_first_sales'] = \
        grouped_df['first_sales'].astype(float) / grouped_df['regs'].astype(float)
    fig = go.Figure(
        data = [go.Scatter(x = grouped_df[time_period],
                           y = grouped_df['regs_to_first_sales'],
                           mode = 'markers+lines')],
        layout = go.Layout(title="Regs to First Sales",
                           margin=dict(l=0, r=0),
                           yaxis=dict(tickformat=',.0%',))
    )
    return fig.to_json()


@bp.route('/overview/first_sales_to_second_sales', methods=['POST'])
@login_required
def first_sales_to_second_sales_fig():
    time_period = determine_time_period(request)
    grouped_df = current_app.data_sources['first_sales_to_second_sales']
    grouped_df = grouped_df[[time_period, 'second_sales', 'first_sales']]
    grouped_df = grouped_df.groupby(time_period).sum()
    grouped_df = grouped_df.reset_index()
    grouped_df['first_sales_to_second_sales'] = \
        grouped_df['second_sales'] / grouped_df['first_sales']
    fig = go.Figure(
        data = [go.Scatter(x = grouped_df[time_period],
                           y = grouped_df['first_sales_to_second_sales'],
                           mode = 'markers+lines')],
        layout = go.Layout(title="First Sales to Second Sales",
                           margin=dict(l=0, r=0),
                           yaxis=dict(tickformat=',.0%',))
    )
    return fig.to_json()


def determine_time_period(request):
    time_period_radio_to_col = {'days': 'date',
                                'weeks': 'week_start',
                                'months': 'month_start'}
    default_time_period = 'weeks'
    time_period_radio = request.form.get('time_period', default_time_period)
    time_period = time_period_radio_to_col[time_period_radio]
    return time_period


def group_by_time_period(df, time_period, value_field):
    grouped_df = df
    grouped_df = grouped_df[[time_period, value_field]]
    grouped_df = grouped_df.groupby(time_period).sum()
    grouped_df = grouped_df.reset_index()
    return grouped_df


def determine_categories(request):
    default_region = 'total'
    regions = request.form.get('regions', default_region)
    print(request.form.getlist('regions'))
    print(request.form.get('data'))
    default_platform = 'total'
    platforms = request.form.get('platforms', default_platform)
    return {'regions': regions, 'platforms': platforms}
