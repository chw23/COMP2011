#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 15:24:07 2024

@author: cheukhowong
"""

from flask import Flask, request, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_admin import Admin
from flask_babel import Babel
from flask_login import LoginManager

def get_locale():
    if request.args.get('lang'):
        session['lang'] = request.args.get('lang')
    return session.get('lang', 'en')

app = Flask(__name__)
babel = Babel(app, locale_selector=get_locale)
admin = Admin(app, template_mode='bootstrap4')
app.config.from_object('config')
db = SQLAlchemy(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'
login_manager.init_app(app)

migrate = Migrate(app, db)

from app import views, models

@login_manager.user_loader
def load_user(user_id):
    return models.Customers.query.get(user_id)
