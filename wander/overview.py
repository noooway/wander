from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, url_for, current_app, jsonify
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
    plots = draw_plots()
    return render_template('overview/overview.html',
                           title='Overview',
                           plots=plots)


@bp.route('/overview/draw_plots', methods=['POST'])
@login_required
def draw_plots():
    controls = parse_controls(request)
    plots = {
        'revenue': revenue_fig(controls),
        'installs': installs_fig(controls),
        'regs': regs_fig(controls),
        'online': online_fig(controls),
        'first_sales': first_sales_fig(controls),
        'sales': sales_fig(controls),
        'virtual_currency_spent': virtual_currency_spent_fig(controls),
        'regs_to_first_sales': regs_to_first_sales_fig(controls),
        'first_sales_to_second_sales': first_sales_to_second_sales_fig(controls)
    }
    #plots['cohorts_revenue'] = cohorts_revenue_json
    if request.method and request.method == 'POST':
        return jsonify(plots)
    else:
        #todo: return only json
        return plots


def revenue_fig(controls):
    time_period = controls['time_period']
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


def installs_fig(controls):
    time_period = controls['time_period']
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


def regs_fig(controls):
    time_period = controls['time_period']
    regions = controls['regions']
    df = current_app.data_sources['regs']
    if 'total' in regions:
        df = compute_regions_total(df)
    filtered_df = df[df['region'].isin(regions)]
    grouped_df = filtered_df[[time_period, 'region', 'regs']]
    grouped_df = filtered_df.groupby([time_period, 'region']).sum()
    grouped_df = grouped_df.reset_index()
    pivoted_df = grouped_df.pivot(index=time_period,
                                  columns='region',
                                  values='regs').reset_index()
    pivoted_df.fillna(0, inplace=True)
    traces = []
    for col in pivoted_df.columns[1:]:
        traces.append(go.Scatter(x = pivoted_df[time_period],
                                 y = pivoted_df[col],
                                 mode = 'markers+lines',
                                 name = col))
    fig = go.Figure(
        data = traces,
        layout = go.Layout(title = "Registrations",
                           legend_orientation = "h",
                           margin = dict(l=0, r=0))
    )
    return fig.to_json()


def online_fig(controls):
    time_period = controls['time_period']
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


def first_sales_fig(controls):
    time_period = controls['time_period']
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


def sales_fig(controls):
    time_period = controls['time_period']
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


def virtual_currency_spent_fig(controls):
    time_period = controls['time_period']
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


def inst_to_regs_conv_plot(controls):
    time_period = controls['time_period']
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


def regs_to_first_sales_fig(controls):
    time_period = controls['time_period']
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


def first_sales_to_second_sales_fig(controls):
    time_period = controls['time_period']
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


def parse_controls(request):
    control_values = request.form.get('controls', {})
    if control_values:
        control_values = json.loads(control_values)
    controls = {
        'time_period': determine_time_period(control_values),
        'regions': determine_regions(control_values)
    }
    return controls


def determine_time_period(control_values):
    time_period_radio_to_col = {'days': 'date',
                                'weeks': 'week_start',
                                'months': 'month_start'}
    default_time_period = 'weeks'
    time_period_radio = control_values.get('time_period', default_time_period)
    time_period = time_period_radio_to_col[time_period_radio]
    return time_period


def determine_regions(control_values):
    default_region = ['total']
    regions = control_values.get('regions', default_region)
    return regions


def group_by_time_period(df, time_period, value_field):
    grouped_df = df
    grouped_df = grouped_df[[time_period, value_field]]
    grouped_df = grouped_df.groupby(time_period).sum()
    grouped_df = grouped_df.reset_index()
    return grouped_df


def compute_regions_total(df):
    grouped_df = df
    time_period = 'date'
    grouped_df = grouped_df[[time_period, 'regs']]
    grouped_df = grouped_df.groupby(time_period).sum()
    grouped_df = grouped_df.reset_index()
    grouped_df['region'] = 'total'
    grouped_df['platform'] = None
    grouped_df['week_start'] = df['week_start'][df['date'] == grouped_df['date']]
    grouped_df['month_start'] = df['month_start'][df['date'] == grouped_df['date']]
    new_df = df.append(grouped_df, sort=True)
    return new_df
