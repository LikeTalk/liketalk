# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, url_for, flash, session, g
from werkzeug.security import generate_password_hash, check_password_hash
from apps import app, db
from apps.forms import JoinForm, LoginForm
from apps.models import User, Winner


import admin, candidate, comment, debug, test, tournament, user_account, view_page, what_match

# 로그인모듈
@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            pwd = form.password.data

            # 여기서부터 DB에서 로그인 정보가 있는지, 있으면 꺼내오는거야.
            user = User.query.get(email)

            if user is None:
                flash(u'존재하지 않는 이메일입니다.', 'danger')
            elif not check_password_hash(user.password, pwd):
                flash(u'비밀번호가 일치하지 않습니다', 'danger')
            else:
                session.permanent = True
                session['user_email'] = user.email
                # flash(u'로그인 완료', 'success')
                # render_template('Select_Group.html')
                # return redirect(url_for('match'))
                return redirect(url_for('tutorial_page')) # 로그인이 완료되면 tutorial page로 이동
    return render_template('user/login.html', form=form, active_tab='log_in')

# session 을 지정해주기 위한 모듈
@app.before_request
def before_request():
    g.user_email = None
    if 'user_email' in session:
        g.user_email = session['user_email']


# 로그아웃!
@app.route('/logout', methods=['GET'])
def log_out():
    session.clear()
    return redirect(url_for('login'))

# 회원가입 모듈
@app.route('/user_join', methods=['GET', 'POST'])
def user_join():
    form = JoinForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            user_email = form.email.data
            user = User.query.get(user_email)
            if user is None:
                user = User(
                    email=form.email.data,
                    password=generate_password_hash(form.password.data)
                )
                db.session.add(user)
                db.session.commit()

                session.permanent = True
                session['user_email'] = user.email
                # flash(u'로그인 완료', 'success')
                return redirect(url_for('tutorial_page')) #회원가입이 완료되면 튜토리얼 페이지로 이동
            else:
                flash(u'이미 존재하는 USER', 'danger')
                return redirect(url_for('user_join')) # 만약 존재하는 회원이면 경고!
        else:
            flash(u'작성형식에 맞지 않습니다.', 'success')
            return redirect(url_for('user_join')) # 작성형식에 맞지 않으면 경고!

    else:
        return render_template('user/join.html', form=form, active_tab="user_join") # URL을 눌러 접속하면 user_join 으로 이동



