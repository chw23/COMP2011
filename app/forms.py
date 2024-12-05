from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField
from wtforms.validators import DataRequired, ValidationError
from datetime import datetime

class AccountForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired("Email is required.")])
    password = StringField('Password', validators=[DataRequired("Password is required.")])

class RegisterForm(FlaskForm):
    fName = StringField('First Name', validators=[DataRequired("First Name is required.")])
    lName = StringField('Last Name', validators=[DataRequired("Last Name is required.")])
    email = StringField('Email', validators=[DataRequired("Email is required.")])
    password = StringField('Password', validators=[DataRequired("Password is required.")])

class QuantityForm(FlaskForm):
    quantity = IntegerField('Quantity', validators=[DataRequired("Please enter the quantity.")])

class OrderForm(FlaskForm):
    submit = SubmitField('Purchase')