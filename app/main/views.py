from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response
from flask_login import login_required, current_user
from . import main
from ..auth import auth
from .. import db
from ..models import Role, User
from ..decorators import admin_required, permission_required

@main.route('/', methods=['GET', 'POST'])
def index():  
	if current_user.is_authenticated is False:
		return redirect(url_for('auth.login'))
	return render_template('index.html')


@main.route('/subject', methods=['GET', 'POST'])
@login_required
@admin_required
def subject():
	return render_template('subject/edit.html')