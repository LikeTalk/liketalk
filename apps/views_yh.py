# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, flash, session, g, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc, asc
from apps import app, db
from apps.forms import CommentForm, JoinForm, LoginForm
from apps.models import User, Comment, Match, Candidate, GameHistory

'''
처음 접속을 하면 무조건 로그인을 한다.
    1. 먼저 USER Table에 들어가서 입력된 이메일이 DB에 있는 회원가입인지 살핀다.
        1.

'''


@app.route('/', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            email = form.email.data
            pwd = form.password.data

            # 여기서부터 DB에서 로그인 정보가 있는지, 있으면 꺼내오는거야.
            try_to_login_user = User.query.filter(email == User.email).all()

            if try_to_login_user is None:
                flash(u'존재하지 않는 이메일입니다.', 'danger')
            elif not check_password_hash(try_to_login_user[0].password, pwd):
                flash(u'비밀번호가 일치하지 않습니다', 'danger')
            else:
                session.permanent = True
                session['user_email'] = try_to_login_user[0].email
                session['user_id'] = try_to_login_user[0].user_id
                flash(u'로그인 완료', 'success')
                return redirect(url_for('match'))
    return render_template('user/login.html', form=form, active_tab='log_in')


@app.before_request
def before_request():
    g.user_id = None
    if 'user_id' in session:
        g.user_id = session['user_id']



@app.route('/main', methods=['GET', 'POST'])
def match():
    match_id = 1
    if g.user_id == None:
        flash(u'로그인 후에 이용해주세요', 'danger')
        return redirect(url_for('login'))
    else:
        user_game_info = {}
        logged_user_id = g.user_id
        user_game_info['myuser'] = GameHistory.query.order_by(asc(GameHistory.done_game)).filter(
            GameHistory.user_id == logged_user_id).all()
        if user_game_info['myuser'] == None:
            match_id = 1
        else:
            it = 0
            for x in user_game_info['myuser']:
                it += 1
                if x.done_game != it:
                    match_id = it
                    break
                else:
                    if it > len(user_game_info):
                        match_id = it
        matchinfo = {}
        matchinfo['match'] = Match.query.get(match_id)
        return render_template("home_yh.html", matchinfo=matchinfo, active_tab="match", test=user_game_info)


@app.route('/vote/ <matnum>/ <int:candnum>', methods=['GET'])
def vote(matnum, candnum):
    this_match = Match.query.get(matnum)
    if candnum == 1:
        this_match.candidate_A_count += 1
    elif candnum == 2:
        this_match.candidate_B_count += 1

    logged_user_id = g.user_id

    # 유저가 이 게임을 했다.
    this_game = GameHistory(
        user_id=logged_user_id,
        done_game=matnum
    )

    db.session.add(this_game)
    db.session.commit()

    return redirect(url_for('match'))





@app.route('/logout', methods=['GET'])
def log_out():
    session.clear()
    return redirect(url_for('login'))


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
            return redirect(url_for('login'))
        else:
            flash(u'작성형식에 맞지 않습니다.', 'success')
    else:
        return render_template('user/join.html', form=form)


@app.route('/tournament', methods=['GET', 'POST'])
def tournament():
    if g.user_id == None:
        flash(u'로그인 후에 이용해주세요', 'danger')
        return redirect(url_for('login'))
    else:
        return render_template("tournament.html", active_tab="tournament")


@app.route('/candidate_list', methods=['GET', 'POST'])
def candidate_list():
    if g.user_id == None:
        flash(u'로그인 후에 이용해주세요', 'danger')
        return redirect(url_for('login'))
    else:
        return render_template("candidate_list.html")


@app.route('/candidate', methods=['GET', 'POST'])
def candidate():
    if g.user_id == None:
        flash(u'로그인 후에 이용해주세요', 'danger')
        return redirect(url_for('login'))
    else:
        return render_template("candidate_page.html", active_tab="candidate")


@app.before_request
def before_request():
    g.user_id = None
    if 'user_id' in session:
        g.user_id = session['user_id']

