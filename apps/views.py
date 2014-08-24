# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, flash, session, g, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc
from apps import app, db
from apps.forms import CommentForm, JoinForm, LoginForm
from apps.models import User, Comment, Match, Candidate


@app.route('/main', methods=['GET','POST'])
def match():
    '''
    matchinfo = {}
    match_id = 1
    matchinfo['match'] = Match.query.get(match_id)'''
    try:
        return render_template("home.html", matchinfo = matchinfo, active_tab="match")
    except:
        return redirect(url_for('login'))


'''
@app.route('/cand_one_count/<int:match_num>', methods = ['GET', 'POST'])
def vote(match_num):
    candA = Match.query.
'''

@app.route('/', methods = ['GET','POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            pwd = form.password.data

            user = User.query.get(email)
            if user is None:
                flash(u'존재하지 않는 이메일입니다.', 'danger')
            elif not check_password_hash(user.password, pwd):
                flash(u'비밀번호가 일치하지 않습니다', 'danger')
            else:
                session.permanent = True
                session['user_id'] = user.email
                flash(u'로그인 완료', 'success')
                return redirect(url_for('match'))

    return render_template('user/login.html', form=form, active_tab='log_in')


@app.route('/user_join', methods=['GET', 'POST'])
def user_join():
    form = JoinForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(
                email=form.email.data,
                password=generate_password_hash(form.password.data)
            )
            db.session.add(user)
            db.session.commit()

            flash(u'가입이 완료되었습니다.', 'success')
            return redirect(url_for('match'))
        else:
            flash(u'작성형식에 맞지 않습니다.', 'success')
    else:
        return render_template('user/join.html', form=form)



@app.route('/tournament',methods=['GET','POST'])
def tournament():
	return render_template("tournament.html", active_tab="tournament")



@app.route('/candidate_list', methods=['GET', 'POST'])
def candidate_list():
    return render_template("candidate_list.html", active_tab="candidate")

'''
#
# @error Handlers
#
# Handle 404 errors
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# Handle 500 errors
@app.errorhandler(500)
def server_error(e):
    return render_template('500.html'), 500

@app.route('/comment/create/<int:Cand_id>', methods=['GET', 'POST'])
def comment_create(article_id):
    form = CommentForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            comment = Comment(
                content=form.content.data,
                candidate=Article.query.get(article_id)
            )

            db.session.add(comment)
            db.session.commit()

            flash(u'댓글을 작성하였습니다.', 'success')
        return redirect(url_for('match', id=Cand_id))
    return render_template('match', form=form)

@app.route('/user/join/', methods=['GET', 'POST'])
def user_join():
    form = JoinForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            user = User(
                email=form.email.data,
                password=generate_password_hash(form.password.data),
                name=form.name.data
            )

            db.session.add(user)
            db.session.commit()

            flash(u'가입이 완료 되었습니다.', 'success')
            return redirect(url_for('match'))
    return render_template('user/join.html', form=form, active_tab='user_join')

@app.route('/login', methods=['GET', 'POST'])
def log_in():
    form = LoginForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            pwd = form.password.data

            user = User.query.get(email)
            if user is None:
                flash(u'존재하지 않는 e-mail입니다.', 'danger')
            elif not check_password_hash(user.password, pwd):
                flash(u'pw가 일치하지 않습니다.', 'danger')
            else:
                session.permanent = True
                session['user_email'] = user.email
                session['user_name'] = user.name

                flash(u'로그인 완료.', 'success')
                return redirect(url_for('match'))

    return render_template('user/login.html', form=form, active_tab='log_in')


@app.route('/logout')
def log_out():
    session.clear()

    return redirect(url_for('article_list'))

@app.before_request
def before_request():
    g.user_name = None

    if 'user_email' in session:
        g.user_name = session['user_name']
        g.user_email = session['user_email']

'''
