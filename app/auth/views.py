from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required, \
    current_user
from . import auth
from .. import db
from ..models import User
from .forms import LoginForm
import socket

@auth.route('/login', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	isEqual = 1
	exist = False

	## get local ip
	localIP = request.remote_addr
	
	if form.validate_on_submit():
		user = User.query.filter_by(username=form.username.data).first()
		if user is not None and user.verify_password(form.password.data):

			# if user.local_ip is None and User.set_local_ip(user,localIP) or \
			# 	localIP == user.local_ip:
			# 	login_user(user, form.remember_me.data)
			# 	return redirect(url_for('main.index'))
			# elif localIP != user.local_ip:
			# 	isEqual = 0                            
			
			if user.local_ip is None:
				exist = User.set_local_ip(user,localIP)
			

			if exist or user.local_ip == localIP or User.is_administrator(user):
				login_user(user, form.remember_me.data)
				return redirect(url_for('main.index'))
			else:
				isEqual = 0

		else:	
			flash('Invalid username or password.')	
	return render_template('auth/login.html', form=form,isEqual=isEqual)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.')
    return redirect(url_for('main.index'))