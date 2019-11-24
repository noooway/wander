from flask import (
    Blueprint, flash, g, redirect, render_template,
    request, url_for, current_app
)
from werkzeug.exceptions import abort
from wander.auth import login_required

import json
import plotly
import plotly.graph_objects as go
import pandas as pd


bp = Blueprint('retention', __name__)


@bp.route('/retention')
@login_required
def retention():
    revenue_by_cohorts_json = revenue_by_cohorts_plot()
    plots = {
        'revenue_by_cohorts': revenue_by_cohorts_json
    }
    return render_template('retention/retention.html',
                           title='Retention',
                           plots=plots)


@bp.route('/retention/revenue_by_cohorts', methods=['POST'])
@login_required
def revenue_by_cohorts_plot():
    # time_period_radio_to_col = {'days': 'date',
    #                             'weeks': 'weekstart',
    #                             'months': 'monthstart'}
    # default_time_period = 'weeks'
    # time_period_radio = request.form.get('time_period', default_time_period)
    # time_period = time_period_radio_to_col[time_period_radio]
    grouped_df = current_app.data_sources['regs_purchases']
    grouped_df = grouped_df[['reg_date', 'pur_date', 'purchase_amount']]
    grouped_df = grouped_df.groupby(['reg_date', 'pur_date']).sum()
    grouped_df = grouped_df.reset_index()
    pivoted_df = grouped_df.pivot(index='pur_date',
                                  columns='reg_date',
                                  values='purchase_amount')
    fig = go.Figure()
    cols = pivoted_df.columns
    for col in cols:
        df = pivoted_df[col].reset_index()
        cohort_starts_from_0 = pd.DataFrame([(df.columns[1], 0.0)],
                                            columns=df.columns)
        df = pd.concat([cohort_starts_from_0, df]).reset_index(drop=True)
        df = df.rename(columns={col:'purchase_amount'})
        df['accumulated_purchases'] = df['purchase_amount'].fillna(0).cumsum()
        fig.add_trace(go.Scatter(x=df['pur_date'],
                                 y=df['accumulated_purchases'],
                                 name = col.strftime('%d.%m.%Y'),
                                 mode='lines+markers'))
    fig.update_layout(title="Cohorts Accumulated Revenue")
    return fig.to_json()
