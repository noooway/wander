from flask import render_template, flash, redirect, url_for
from flask_login import current_user, login_user, logout_user, login_required
from app_pkg import app
from app_pkg.forms import LoginForm
from app_pkg.models import User
from flask import request
from werkzeug.urls import url_parse
from app_pkg import db
from app_pkg.forms import RegistrationForm

import json
import plotly
import plotly.graph_objects as go
import numpy as np


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('Logout to see login screen')
        return redirect(url_for('overview'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('overview')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('Logout to register new user')
        return redirect(url_for('overview'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/overview')
@login_required
def overview():
    revenue_json = revenue_plot()
    plots = {'revenue': revenue_json}
    return render_template('overview.html', title='Overview', plots=plots)


@app.route('/overview/revenue', methods=['POST'])
@login_required
def revenue_plot():
    default_count = 500
    default_color = 'orange'
    count = request.values.get('count', default_count)
    col = request.values.get('color', default_color)
    xScale = np.linspace(0, 100, count)
    yScale = np.random.randn(count)
    trace = go.Scatter(
        x = xScale,
        y = yScale,
        line = dict(color=col)
    )
    data = [trace]
    fig = go.Figure(data=data)
    return fig.to_json()
