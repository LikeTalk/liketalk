# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, url_for, flash, session, g, jsonify
from sqlalchemy import desc, asc
from apps import app
from apps.models import User, Comment, Match, Candidate, GameHistory, Winner, UserCommentHistory, Indiv_Comment, Bulletin

import random

import admin, candidate, comment, debug, test, tournament, user_account, view_page, what_match

# 어떤 참가자들이 게임을 하는지 보여주는 페이지
@app.route('/candidate_list/<int:group>', methods=['GET', 'POST'])
def candidate_list(group):
    if g.user_email == None:
        flash(u'로그인 후에 이용해주세요', 'danger')
        return redirect(url_for('login'))
    else:
        # 원하는 그룹에 있는 사람들을 Match DB에서 불러온다.
        group_people = Match.query.order_by(asc(Match.game_round)).filter(Match.group == group).all()
        total_people = []
        people = []
        people_count = 0

        # Match DB에는 두 명이 짝을 이루어서 한 row에 있기 때문에, 얘를 각각 A,B로 쪼갠다.
        for each_people in group_people:
            A_info = {}
            B_info = {}
            A_info.update({'name': each_people.candidate_A_namename, 'school': each_people.candidate_A_school,
                           'photo': each_people.candidate_A_photolink, 'season': each_people.season_num,
                           'game_round': each_people.game_round, 'group': each_people.group})
            B_info.update({'name': each_people.candidate_B_namename, 'school': each_people.candidate_B_school,
                           'photo': each_people.candidate_B_photolink, 'season': each_people.season_num,
                           'game_round': each_people.game_round, 'group': each_people.group})

            people.append(A_info)
            people.append(B_info)
            people_count += 2
            if people_count == 6:
                people_count = 0
                total_people.append(people)
        random.shuffle(total_people[0])
        return render_template("candidate_list.html", total_people=total_people[0], active_tab = "candidate_list", group  = 1)


# Candidate list에서 한 명을 클릭하면 그 한명을 제대로 소개해주는 페이지로 이동하게 된다.
@app.route('/candidate/<name>', methods=['GET', 'POST'])
def candidate(name):
    if g.user_email == None:
        flash(u'로그인 후에 이용해주세요', 'danger')
        return redirect(url_for('login'))
    else:
        cand_data = {}

        # 유저가 A에 있는지, B에 있는지 모르기 때문에 다음의 테크닉을 쓰게 된다.
        try:
            each_match = Match.query.filter(Match.candidate_A_namename == name).all()
            each_match = each_match[0]
            cand_data['name'] = name
            cand_data['school'] = each_match.candidate_A_school
            cand_data['photo'] = each_match.candidate_A_photolink
            cand_data['group'] = each_match.group

        except:
            each_match = Match.query.filter(Match.candidate_B_namename == name).all()
            each_match = each_match[0]
            cand_data['name'] = name
            cand_data['school'] = each_match.candidate_B_school
            cand_data['photo'] = each_match.candidate_B_photolink
            cand_data['group'] = each_match.group

        comments_A = Comment.query.order_by(desc(Comment.date_created)).filter(Comment.comment_A == name).all()
        comments_B = Comment.query.order_by(desc(Comment.date_created)).filter(Comment.comment_B == name).all()
        comments_indiv = Indiv_Comment.query.order_by(desc(Indiv_Comment.date_created)).filter(Indiv_Comment.comment_name == name).all()
        comments = comments_A + comments_B


        return render_template("candidate_page.html", cand_data=cand_data, comments = comments, comments_indiv = comments_indiv, active_tab="candidate")

