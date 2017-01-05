from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response
from flask_login import login_required, current_user
from . import main
from ..auth import auth
from .. import db
from ..models import Role, User, Select
from ..decorators import admin_required, permission_required

import json
import base64

@main.route('/', methods=['GET', 'POST'])
def index():  
	if current_user.is_authenticated is False:
		return redirect(url_for('auth.login'))
	return render_template('index.html')


@main.route('/subject', methods=['GET', 'POST'])
@login_required
@admin_required
def subject():
	maxPeriod = Select.get_max_period()
	return render_template('subject/edit.html',maxPeriod=maxPeriod,current_period=0)

@main.route('/subject/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def show_subjects(id):

	maxPeriod = Select.get_max_period()
	selects = Select.query.filter_by(period=id)

	return render_template('subject/edit.html',maxPeriod=maxPeriod,selects=selects,current_period=id)

@main.route('/subject/release', methods=['GET', 'POST'])
@login_required
@admin_required
def subject_release():

	data =  json.loads(request.form.get('list'))

	for n in data:
		select = Select(title=data[n]["title"],
			answer=data[n]["answer"],
			option=data[n]["option"],
			period=data[n]["period"])
		db.session.add(select)
		db.session.commit()

	return "True"