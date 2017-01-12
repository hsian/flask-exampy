from flask import render_template, redirect, url_for, abort, flash, request,\
    current_app, make_response
from flask_login import login_required, current_user
from . import main
from ..auth import auth
from .. import db
from ..models import Role, User, Select, Score ,Question, Answer
from ..decorators import admin_required, permission_required

import json
import base64
import types 

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

@main.route('/edit_subject/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_subject(id):

	select = Select.query.get_or_404(id)
	data =  json.loads(request.form.get('list'))

	select.title = data["title"]
	select.answer = data["answer"]
	select.option =  data["option"]

	return "True"

@main.route('/show_subject/<int:id>',methods=['GET','POST'])
@login_required
def show_subject(id):

	selects = Select.query.filter_by(period=id)
	first = "ABCDEFGHIJK"
	index = 0
	data = []

	for n in selects:

		index = index + 1
		n.as_title = str(index) + ". " + n.title

		arr = n.option.split("###")
		for i in range(0,len(arr)):
			if arr[i].strip() is not "":
				arr[i] = first[i] + ". " + arr[i]
		n.options = arr

		if len(n.answer) >= 2:
			n.isMulit = True
		else:
			n.isMulit = False

		data.append(n) 

	questions = Question.query.filter_by(period=id)
	q_index = 0
	q_data = []

	for n in questions:
		q_index = q_index + 1
		n.as_title = str(q_index) + ". " + n.title

		q_data.append(n)
				
	return render_template('subject/list.html',selects=data,period=id,questions=q_data)

@main.route('/figure/<int:id>/<username>',methods=['GET','POST'])
@login_required
def figure_score(id,username):
	data =  json.loads(request.form.get('list'))

	if username == current_user.username:
		exist = Score.query.filter_by(period=id,u_id=current_user.id).first()
		if exist is None:
			score = 0
			selects = Select.query.filter_by(period=id)

			for n in selects:
				if data[str(n.id)] == n.answer:
					score = score + 1

			o_score = Score(u_id=current_user.id,
				username=current_user.username,
				score=score,
				period=id)
			db.session.add(o_score)
			db.session.commit()

			return str(score)
		else:
			return "不能重复提交"
	else:
		return "用户信息错误"

@main.route('/figure_quest/<int:id>/<username>',methods=['GET','POST'])
@login_required
def figure_quest(id,username):
	data =  json.loads(request.form.get('list'))

	if username == current_user.username:
		
		for n in data:
			exist = Answer.query.filter_by(period=id,u_id=current_user.id,quest_id=n).first()
			if exist is None:

				answer = Answer(u_id=current_user.id,
					username=current_user.username,
					period=id,
					quest_id=n,
					ans=data[n])
				db.session.add(answer)

		db.session.commit()

		return "True"

	else:
		return "用户信息错误"

@main.route('/question/<int:id>',methods=['GET','POST'])
@login_required
@admin_required
def question_by_period(id):
	maxPeriod = Select.get_max_period()
	questions = Question.query.filter_by(period=id)

	return render_template('subject/question.html',maxPeriod=maxPeriod,questions=questions,current_period=id)

@main.route('/question/release', methods=['GET', 'POST'])
@login_required
@admin_required
def question_release():

	data =  json.loads(request.form.get('list'))

	for n in data:
		question = Question(title=data[n]["title"],
			period=data[n]["period"])
		db.session.add(question)
		db.session.commit()

	return "True"


@main.route('/edit_question/<int:id>', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_question(id):

	question = Question.query.get_or_404(id)
	data =  json.loads(request.form.get('list'))

	question.title = data["title"]
	return "True"




