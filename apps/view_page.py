# -*- coding: utf-8 -*-

from flask import g, render_template, redirect, url_for, flash
from sqlalchemy import asc, desc
from apps import app, db
from apps.models import Winner, Match, Comment


import admin, candidate, comment, debug, test, tournament, user_account, view_page, what_match



# 튜토리얼 페이지를 보여준다.
# 접속하면, 가장 먼저 이 페이지가 뜬다.
@app.route('/')
def tutorial_page():
    return render_template("tutorial.html")
    #return render_template('down.html')



@app.route('/tournament', methods=['GET', 'POST'])
def tournament():
    if g.user_email == None:
        flash(u'로그인 후에 이용해주세요', 'danger')
        return redirect(url_for('login'))
    else:
        return render_template("tournament.html", active_tab="tournament")


# 어떤 그룹을 선택해서 게임을 할 것인지 페이지를 보여준다.
@app.route('/group')
def select_group():
    if g.user_email == None:
        flash(u'로그인 후에 이용해주세요', 'danger')
        return redirect(url_for('login'))
    else:
        return render_template("Select_Group.html", active_tab="group")


# 만약, 게임이 끝났다면, 개별 유저의 게임 우승자를 보여준다.
@app.route('/main/congat/<int:group>', methods=['GET', 'POST'])
def END(group):
    user_email = g.user_email
    last_game = Winner.query.filter(Winner.game_season == 1, Winner.game_group == group, Winner.user_email == user_email).all()[0]
    name = last_game.winner_A_namename

    # 승자가 candidate A에 있는지 B에 있는지 모르기 때문에, 이렇게 찾는다.
    try:
        your_winner = Match.query.filter(Match.candidate_A_namename == name).all()[0]
        photo_address = your_winner.candidate_A_photolink
    except:
        your_winner = Match.query.filter(Match.candidate_B_namename == name).all()[0]
        photo_address = your_winner.candidate_B_photolink

    return render_template("end.html", last_game = last_game, photo = photo_address)



@app.route('/two_people/<name1>/<name2>', methods = ['GET','POST'])
def two_people_show(name1,name2):
    if g.user_email == None:
        flash(u'로그인 후에 이용해주세요', 'danger')
        return redirect(url_for('login'))
    else:
        two_people = Comment.query.order_by(desc(Comment.date_created)).filter(Comment.comment_A == name1, Comment.comment_B == name2).all()
        if len(two_people) == 0:
            two_people = Comment.query.order_by(desc(Comment.date_created)).filter(Comment.comment_A == name2, Comment.comment_B == name1).all()

        try:
            cand1 = Match.query.filter(Match.candidate_A_namename == name1).all()
            cand1 = cand1[0]
            photo1 = cand1.candidate_A_photolink
        except:
            cand1 = Match.query.filter(Match.candidate_B_namename == name1).all()
            cand1 = cand1[0]
            photo1 = cand1.candidate_B_photolink

        try:
            cand2 = Match.query.filter(Match.candidate_A_namename == name2).all()
            cand2 = cand2[0]
            photo2 = cand2.candidate_A_photolink
        except:
            cand2 = Match.query.filter(Match.candidate_B_namename == name2).all()
            cand2 = cand2[0]
            photo2 = cand2.candidate_B_photolink

        return render_template('two_people.html', two_people = two_people, photo1 = photo1, photo2 = photo2, name1 = name1, name2 = name2)