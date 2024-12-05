#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 10 15:25:23 2024

@author: cheukhowong
"""

from flask import get_flashed_messages, render_template, flash, redirect, url_for
from app import app, db, admin
from .forms import AccountForm, RegisterForm, QuantityForm, OrderForm
from flask_admin.contrib.sqla import ModelView
from .models import Products, Customers, Orders, Baskets, BasketItem
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime

admin.add_view(ModelView(Products, db.session))
admin.add_view(ModelView(Customers, db.session))
admin.add_view(ModelView(Orders, db.session))
admin.add_view(ModelView(Baskets, db.session))
admin.add_view(ModelView(BasketItem, db.session))

@app.route('/', methods=['GET', 'POST'])
def home():
    products = Products.query.all()
    return render_template('home.html',
                           title='Home Page', products=products)

@app.route('/classics', methods=['GET', 'POST'])
def classics():
    products = Products.query.all()
    return render_template('genre_classics.html',
                           title='Genre: Classics', products=products)

@app.route('/film_musics', methods=['GET', 'POST'])
def filmMusics():
    products = Products.query.all()
    return render_template('genre_filmMusics.html',
                           title='Genre: Film Musics', products=products)

@app.route('/anime', methods=['GET', 'POST'])
def anime():
    products = Products.query.all()
    return render_template('genre_anime.html',
                           title='Genre: Anime', products=products)

@app.route('/pop', methods=['GET', 'POST'])
def pop():
    products = Products.query.all()
    return render_template('genre_pop.html',
                           title='Genre: Pop', products=products)

@app.route('/beginner', methods=['GET', 'POST'])
def beginner():
    products = Products.query.all()
    return render_template('difficulties_beginner.html',
                           title='Difficulties: Beginner', products=products)

@app.route('/intermediate', methods=['GET', 'POST'])
def intermediate():
    products = Products.query.all()
    return render_template('difficulties_intermediate.html',
                           title='Difficulties: Intermediate', products=products)

@app.route('/advanced', methods=['GET', 'POST'])
def advanced():
    products = Products.query.all()
    return render_template('difficulties_advanced.html',
                           title='Difficulties: Advanced', products=products)

@app.route('/rating1', methods=['GET', 'POST'])
def rating1():
    products = Products.query.all()
    return render_template('rating1.html',
                           title='Rating: 1 star', products=products)

@app.route('/rating2', methods=['GET', 'POST'])
def rating2():
    products = Products.query.all()
    return render_template('rating2.html',
                           title='Rating: 2 stars', products=products)

@app.route('/rating3', methods=['GET', 'POST'])
def rating3():
    products = Products.query.all()
    return render_template('rating3.html',
                           title='Rating: 3 stars', products=products)

@app.route('/rating4', methods=['GET', 'POST'])
def rating4():
    products = Products.query.all()
    return render_template('rating4.html',
                           title='Rating: 4 stars', products=products)

@app.route('/rating5', methods=['GET', 'POST'])
def rating5():
    products = Products.query.all()
    return render_template('rating5.html',
                           title='Rating: 5 stars', products=products)

# inspired by https://flask-login.readthedocs.io/en/latest/
@app.route('/login', methods=['GET', 'POST'])
def login():

    # https://flask.palletsprojects.com/en/stable/api/#flask.get_flashed_messages
    # if no parameters are passed, it will return an empty list -> clear old flash messages
    get_flashed_messages()
    
    form = AccountForm()
    if form.validate_on_submit():
        customer = Customers.query.filter_by(email=form.email.data).first()
        # validate the password
        if customer is None or customer.password != form.password.data:
            flash('Invalid email or password', 'danger')
            return redirect(url_for('login'))
        else:
            login_user(customer)
            flash('Logged in successfully.', 'success')
            return redirect(url_for('login'))
    else:
        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{field}: {error}", 'danger')
    return render_template('login.html', title='Sign In', form=form)

@app.route('/order', methods=['GET', 'POST'])
def order():
    orders = Orders.query.filter_by(customer_id=current_user.id).all()
    return render_template('order.html',
                           title='Order', orders=orders)

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route('/settings', methods=['GET', 'POST'])
@login_required
def settings():
    currentCustomer = Customers.query.get(current_user.id)
    form = RegisterForm(obj=currentCustomer)

    if form.validate_on_submit():
        currentCustomer.fname = form.fName.data
        currentCustomer.lname = form.lName.data
        currentCustomer.email = form.email.data
        currentCustomer.password = form.password.data

        db.session.commit()
        flash('Account updated successfully.', 'success')
        return redirect(url_for('login'))
    return render_template('settings.html', title='Account settings', form=form)

@app.route('/create', methods=['GET', 'POST'])
def create():
    form = RegisterForm()
    if form.validate_on_submit():
        existCustomer = Customers.query.filter_by(email=form.email.data).first()
        # validate if the email is is new
        if existCustomer is not None:
            flash('Email already exists.', 'danger')
            return redirect(url_for('create'))
        
        newCustomer = Customers(
            fname=form.fName.data,
            lname=form.lName.data,
            email=form.email.data,
            password=form.password.data
        )
        db.session.add(newCustomer)
        db.session.commit()
        flash('Account created successfully.', 'success')
        return redirect(url_for('login'))
    else:
        if form.errors:
            for field, errors in form.errors.items():
                for error in errors:
                    flash(f"{field}: {error}", 'danger')
    return render_template('createAccount.html', title='Register', form=form)

# Create a basket item when add to the basket
@app.route('/details/<int:ID>', methods=['GET', 'POST'])
@login_required
def details(ID):
    product = Products.query.get(ID)
    form = QuantityForm()
    if form.validate_on_submit():
        quantity = form.quantity.data
        basket_item = BasketItem.query.filter_by(customer_id=current_user.id, product_id=ID).first()
        if basket_item:
            basket_item.quantity += quantity
        else:
            new_item = BasketItem(
                customer_id=current_user.id,
                product_id=ID,
                quantity=quantity
            )
            db.session.add(new_item)
        db.session.commit()
        flash('Item added to basket.', 'success')
        return redirect(url_for('basket'))
    return render_template('details.html', title='Product Details', product=product, form=form)

# Group the items into one basket and link it to an order
@app.route('/basket', methods=['GET', 'POST'])
@login_required
def basket():
    basket_items = BasketItem.query.filter_by(customer_id=current_user.id, basket_id=None).all()
    if not basket_items:
        flash('Your basket is empty.', 'light')

    form = OrderForm()
    if form.validate_on_submit():
        basket = Baskets(customer_id=current_user.id)
        db.session.add(basket)
        db.session.commit()

        for item in basket_items:
            item.basket_id = basket.id
            db.session.add(item)
        db.session.commit()

        order = Orders(
            customer_id=current_user.id,
            basket_id=basket.id,
            order_date=datetime.today().date(),
            status='Completed'
        )
        db.session.add(order)
        db.session.commit()

        flash('Order placed successfully.', 'success')
        return redirect(url_for('login'))

    return render_template('basket.html', title='Basket', basket_items=basket_items, form=form)
