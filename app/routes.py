from app import app
from flask import render_template, flash, redirect
from app.forms import LoginForm
from flask import request
from werkzeug.urls import url_parse
from flask_login import login_required

@app.route('/')
@app.route('/index')
@login_required
def index():
    user = {'username':'Nicholas'}

    posts = [
        {
            'author': {'username':'John'},
            'body':'Beautiful day in Boston!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Captain Marvel movie was trash'
        }
    ]
    
    return render_template('index.html', title='Home', user=user, posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('index'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            return redirect(url_for('index'))
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
