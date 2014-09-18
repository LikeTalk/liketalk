# -*- coding: utf-8 -*-
import json
from flask import render_template, request, redirect, url_for, flash, session, g, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc, asc
from apps import app, db
from apps.forms import CommentForm, JoinForm, LoginForm
from apps.models import User, Comment, Match, Candidate, GameHistory, Winner

import random
import math
from itertools import count, izip
from person_info import uos, ajou, gachon, hanyang, kaist, khu, korea, mju, sejong, snu_yonsei, ssu, teacher

'''
@app.route('/fill_in_user_indiv_model')
def fill_in_user_indiv():
    user_email = g.user_email
    My_Match = Match.query.all()
    for each_match in My_Match:
        season = each_match.season_num
        game_round = each_match.game_round
        A_name = each_match.candidate_A_namename
        A_school = each_match.candidate_A_school
        A_photo = each_match.candidate_A_photolink
        B_name = each_match.candidate_B_namename
        B_school = each_match.candidate_B_school
        B_photo = each_match.candidate_B_photolink

        each_game = User_Indiv_Game(
            user_email = user_email,
            game_season = season,
            game_round = game_round,
            candidate_A_namename = A_name,
            candidate_A_school = A_school,
            candidate_A_photolink = A_photo,
            candidate_B_namename = B_name,
            candidate_B_school = B_school,
            candidate_B_photolink = B_photo
        )

        db.session.add(each_game)
        db.session.commit()
'''



def chunk(mylist):
    temp = zip(*[iter(mylist)] * 2)
    return [list(x) for x in temp]


@app.route('/newnew_input')
def newnew():
    # return "\n".join( [ student[0] for student in  kaist.students] )
    ajou_info = [st for st in ajou.students] + [tc for tc in ajou.teachers]
    gachon_info = [st for st in gachon.students] + [tc for tc in gachon.teachers]
    hanyang_info = [st for st in hanyang.students] + [tc for tc in hanyang.teachers]
    kaist_info = [st for st in kaist.students] + [tc for tc in kaist.teachers]
    khu_info = [st for st in khu.students] + [tc for tc in khu.teachers]
    mju_info = [st for st in mju.students] + [tc for tc in mju.teachers]
    sejong_info = [st for st in sejong.students] + [tc for tc in sejong.teachers]
    snu_yonseig_info = [st for st in snu_yonsei.students] + [tc for tc in snu_yonsei.teachers]
    ssu_info = [st for st in ssu.students] + [tc for tc in ssu.teachers]
    uos_info = [st for st in uos.students] + [tc for tc in uos.teachers]

    all_info = ajou_info + gachon_info + hanyang_info + kaist_info + khu_info + mju_info + sejong_info + snu_yonseig_info + ssu_info + uos_info
    # random.shuffle(all_info)

    idx = 0
    for each_member in all_info:
        dummy = "o"
        season = 0
        name = each_member[0]
        school = each_member[1]
        photo_link = each_member[2]

        each_match = Match(
            season_num=0,
            game_round=idx,
            candidate_A_namename=name,
            candidate_A_photolink=photo_link,
            candidate_A_school=school,
            candidate_B_namename=dummy,
            candidate_B_photolink=dummy,
            candidate_B_school=dummy
        )
        db.session.add(each_match)
        db.session.commit()
        idx += 1


# Candidate DB에 선수들을 다 집어넣는 함수
@app.route('/total_allinone')
def all_in():
    ajou_info = [st for st in ajou.students] + [tc for tc in ajou.teachers]
    gachon_info = [st for st in gachon.students] + [tc for tc in gachon.teachers]
    hanyang_info = [st for st in hanyang.students] + [tc for tc in hanyang.teachers]
    kaist_info = [st for st in kaist.students] + [tc for tc in kaist.teachers]
    khu_info = [st for st in khu.students] + [tc for tc in khu.teachers]
    mju_info = [st for st in mju.students] + [tc for tc in mju.teachers]
    sejong_info = [st for st in sejong.students] + [tc for tc in sejong.teachers]
    snu_yonseig_info = [st for st in snu_yonsei.students] + [tc for tc in snu_yonsei.teachers]
    ssu_info = [st for st in ssu.students] + [tc for tc in ssu.teachers]
    uos_info = [st for st in uos.students] + [tc for tc in uos.teachers]
    master_info = [tc for tc in teacher.master]

    all_info = ajou_info + gachon_info + hanyang_info + kaist_info + khu_info + mju_info + sejong_info + snu_yonseig_info + ssu_info + uos_info + master_info

    for each_member in all_info:
        name = each_member[0]
        school = each_member[1]
        photo_link = each_member[2]

        member = Candidate(
            name=name,
            photolink=photo_link,
            school=school
        )

        db.session.add(member)
        db.session.commit()


# Candidate DB에서 꺼내와서 선수들을 그룹별로 집어넣는 함수
@app.route('/group_likelion')
def grouping():
    ajou_info = [st for st in ajou.students] + [tc for tc in ajou.teachers]
    gachon_info = [st for st in gachon.students] + [tc for tc in gachon.teachers]
    hanyang_info = [st for st in hanyang.students] + [tc for tc in hanyang.teachers]
    kaist_info = [st for st in kaist.students] + [tc for tc in kaist.teachers]
    khu_info = [st for st in khu.students] + [tc for tc in khu.teachers]
    mju_info = [st for st in mju.students] + [tc for tc in mju.teachers]
    sejong_info = [st for st in sejong.students] + [tc for tc in sejong.teachers]
    snu_yonseig_info = [st for st in snu_yonsei.students] + [tc for tc in snu_yonsei.teachers]
    ssu_info = [st for st in ssu.students] + [tc for tc in ssu.teachers]
    uos_info = [st for st in uos.students] + [tc for tc in uos.teachers]
    master_info = [tc for tc in teacher.master]

    all_info = ajou_info + gachon_info + hanyang_info + kaist_info + khu_info + mju_info + sejong_info + snu_yonseig_info + ssu_info + uos_info + master_info

    # 이렇게 불러오는거야 ㅋㅋㅋ
    # candidate_members = Candidate.query.all()
    # candidate_members[0].photolink

    candidate_members = Candidate.query.all()
    random.shuffle(candidate_members)
    candidate_members = candidate_members[:160]
    candidate_members = chunk(candidate_members)

    idx = 0
    game_round = 1
    for each_pair in candidate_members:
        A = each_pair[0]
        B = each_pair[1]

        nameA = A.name
        orgA = A.school
        photoA = A.photolink

        nameB = B.name
        orgB = B.school
        photoB = B.photolink

        if idx < 16:
            game_group = 1
        elif idx >= 16 and idx < 32:
            game_group = 2
        elif idx >= 32 and idx < 48:
            game_group = 3
        elif idx >= 48 and idx < 60:
            game_group = 4
        #elif idx <= 128 and idx < 160:
        else:
            game_group = 5

        my_match = Match(
            season_num=32,
            game_round=game_round,
            candidate_A_namename=nameA,
            candidate_A_photolink=photoA,
            candidate_A_school=orgA,
            candidate_B_namename=nameB,
            candidate_B_photolink=photoB,
            candidate_B_school=orgB,
            group=game_group
        )
        db.session.add(my_match)
        db.session.commit()
        idx += 1
        game_round += 1
        if game_round == 17:
            game_round = 1


# 뭐하지?
'''
1. 유저가 로그인을 했습니다.
2. 32명을 랜덤으로 뿌려줌 ㅋㅋ
'''








# 한 번 들어가면 season을 입력시켜준다.
@app.route('/input_match')
def input_match():
    # return "\n".join( [ student[0] for student in  kaist.students] )
    ajou_info = [st for st in ajou.students] + [tc for tc in ajou.teachers]
    gachon_info = [st for st in gachon.students] + [tc for tc in gachon.teachers]
    hanyang_info = [st for st in hanyang.students] + [tc for tc in hanyang.teachers]
    kaist_info = [st for st in kaist.students] + [tc for tc in kaist.teachers]
    khu_info = [st for st in khu.students] + [tc for tc in khu.teachers]
    mju_info = [st for st in mju.students] + [tc for tc in mju.teachers]
    sejong_info = [st for st in sejong.students] + [tc for tc in sejong.teachers]
    snu_yonseig_info = [st for st in snu_yonsei.students] + [tc for tc in snu_yonsei.teachers]
    ssu_info = [st for st in ssu.students] + [tc for tc in ssu.teachers]
    uos_info = [st for st in uos.students] + [tc for tc in uos.teachers]

    all_info = ajou_info + gachon_info + hanyang_info + kaist_info + khu_info + mju_info + sejong_info + snu_yonseig_info + ssu_info + uos_info
    random.shuffle(all_info)
    all_info = chunk(all_info)
    random.shuffle(all_info)

    season = int(math.log(len(all_info), 2))

    all_info = all_info[:2 ** season]

    idx = 0
    for each in all_info:
        A = each[0]
        B = each[1]

        nameA = A[0]
        nameA = unicode(nameA, 'utf-8')
        orgA = A[1]
        orgA = unicode(orgA, 'utf-8')
        photoA = A[2]

        nameB = B[0]
        nameB = unicode(nameB, 'utf-8')
        orgB = B[1]
        orgB = unicode(orgB, 'utf-8')
        photoB = B[2]

        my_match = Match(
            season_num=2 ** season,
            game_round=idx,
            candidate_A_namename=nameA,
            candidate_A_photolink=photoA,
            candidate_A_school=orgA,
            candidate_B_namename=nameB,
            candidate_B_photolink=photoB,
            candidate_B_school=orgB
        )
        db.session.add(my_match)
        db.session.commit()
        idx += 1


@app.route('/new_match/<int:season>')
def new_match(season):
    new_cand = []
    idx = 0
    for idx in range(season):
        cand_num = db.session.query(Match).filter(Match.season_num == season, Match.game_round == idx)[0]
        candA_num = cand_num.candidate_A_count
        candB_num = cand_num.candidate_B_count
        if int(candA_num) >= int(candB_num):
            winner = cand_num.candidate_A_namename
            new_cand.append(winner)
            # winner = unicode(winner, 'utf-8')
        else:
            winner = cand_num.candidate_B_namename
            # winner = unicode(winner, 'utf-8')
            new_cand.append(winner)

    random.shuffle(new_cand)
    my_iter = 0
    for idx in xrange(0, len(new_cand), 2):
        my_match = Match(
            season_num=int(season / 2),
            game_round=my_iter,
            candidate_A_namename=new_cand[idx],
            candidate_B_namename=new_cand[idx + 1],
        )
        my_iter += 1
        db.session.add(my_match)
        db.session.commit()


@app.route('/test')
def test():
    roundnum = request.args.get('roundnum', 0, type=int)
    season = request.args.get('seasonnum', 0, type=int)
    cand1_selected = request.args.get('cand1_selected')
    cand2_selected = request.args.get('cand2_selected')
    cand1_count = request.args.get('cand1_count', 0, type=int)
    cand2_count = request.args.get('cand2_count', 0, type=int)

    next_game = db.session.query(Match).filter(Match.season_num == season, Match.game_round == roundnum + 1)[0]

    next_data = {"Aphotolink": str('static/') + str(next_game.candidate_A_photolink),
                 "Bphotolink": str('static/') + str(next_game.candidate_B_photolink),
                 "Acount": next_game.candidate_A_count, "Bcount": next_game.candidate_B_count,
                 "Aname": next_game.candidate_A_namename, "Bname": next_game.candidate_B_namename,
                 "Aschool": next_game.candidate_A_school,
                 "Bschool": next_game.candidate_B_school, "next_round": roundnum + 1}

    if cand1_selected == 0 and cand1_count == 0:
        # cand2 selected
        this_match = db.session.query(Match).filter(Match.season_num == season, Match.game_round == roundnum)[0]
        this_match.candidate_B_count += 1
    elif cand2_selected == 0 and cand2_count == 0:
        this_match = db.session.query(Match).filter(Match.season_num == season, Match.game_round == roundnum)[0]
        this_match.candidate_A_count += 1

    this_game = GameHistory(
        user_email=g.user_email,
        done_game=roundnum
    )
    db.session.add(this_game)
    db.session.commit()
    return jsonify(next_data=next_data)


@app.route('/group')
def testest():
    if g.user_email == None:
        flash(u'로그인 후에 이용해주세요', 'danger')
        return redirect(url_for('login'))
    else:
        return render_template("Select_Group.html", active_tab="group")


@app.route('/match_data', methods=['GET'])
def match_data():
    r = [
        [
            [{"name": "Erik Zettersten", "id": "erik-zettersten", "seed": 1, "displaySeed": "D1", "score": 47},
             {"name": "Andrew Miller", "id": "andrew-miller", "seed": 2}],
            [{"name": "James Coutry", "id": "james-coutry", "seed": 3},
             {"name": "Sam Merrill", "id": "sam-merrill", "seed": 4}],
            [{"name": "Anothy Hopkins", "id": "anthony-hopkins", "seed": 5},
             {"name": "Everett Zettersten", "id": "everett-zettersten", "seed": 6}],
            [{"name": "John Scott", "id": "john-scott", "seed": 7},
             {"name": "Teddy Koufus", "id": "teddy-koufus", "seed": 8}],
            [{"name": "Arnold Palmer", "id": "arnold-palmer", "seed": 9},
             {"name": "Ryan Anderson", "id": "ryan-anderson", "seed": 10}],
            [{"name": "Jesse James", "id": "jesse-james", "seed": 1},
             {"name": "Scott Anderson", "id": "scott-anderson", "seed": 12}],
            [{"name": "Josh Groben", "id": "josh-groben", "seed": 13},
             {"name": "Sammy Zettersten", "id": "sammy-zettersten", "seed": 14}],
            [{"name": "Jake Coutry", "id": "jake-coutry", "seed": 15},
             {"name": "Spencer Zettersten", "id": "spencer-zettersten", "seed": 16}]
        ],
        [
            [{"name": "Erik Zettersten", "id": "erik-zettersten", "seed": 1},
             {"name": "James Coutry", "id": "james-coutry", "seed": 3}],
            [{"name": "Anothy Hopkins", "id": "anthony-hopkins", "seed": 5},
             {"name": "Teddy Koufus", "id": "teddy-koufus", "seed": 8}],
            [{"name": "Ryan Anderson", "id": "ryan-anderson", "seed": 10},
             {"name": "Scott Anderson", "id": "scott-anderson", "seed": 12}],
            [{"name": "Sammy Zettersten", "id": "sammy-zettersten", "seed": 14},
             {"name": "Jake Coutry", "id": "jake-coutry", "seed": 15}]
        ],
        [
            [{"name": "Erik Zettersten", "id": "erik-zettersten", "seed": 1},
             {"name": "Anothy Hopkins", "id": "anthony-hopkins", "seed": 5}],
            [{"name": "Ryan Anderson", "id": "ryan-anderson", "seed": 10},
             {"name": "Sammy Zettersten", "id": "sammy-zettersten", "seed": 14}]
        ],
        [
            [{"name": "Erik Zettersten", "id": "erik-zettersten", "seed": 1},
             {"name": "Ryan Anderson", "id": "ryan-anderson", "seed": 10}]
        ],
        [
            [{"name": "Erik Zettersten", "id": "erik-zettersten", "seed": 1}]
        ]
    ]

    # return jsonify(name = "Erik", id = "erik", seed = 1)
    return json.dumps(r)


@app.route('/', methods=['GET', 'POST'])
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
                flash(u'로그인 완료', 'success')
                # render_template('Select_Group.html')
                # return redirect(url_for('match'))
                return redirect(url_for('testest'))
    return render_template('user/login.html', form=form, active_tab='log_in')


@app.before_request
def before_request():
    g.user_email = None
    if 'user_email' in session:
        g.user_email = session['user_email']


'''
어떤 게임을 줘야 할까?

1.

'''


def check_user_match(user_email):
    # 로그인한 유저가 했던 게임을 쪼아아아아악 나열
    user_game_history = GameHistory.query.order_by(asc(GameHistory.done_game)).filter(
        GameHistory.user_email == user_email).all()

    # 먼저 유저의 게임을 그룹별로 분류
    user_game_A = []
    user_game_B = []
    user_game_C = []
    user_game_D = []
    user_game_E = []

    for each_user_game in user_game_history:
        if each_user_game.done_game_group == 1:
            user_game_A.append(each_user_game)
        elif each_user_game.done_game_group == 2:
            user_game_B.append(each_user_game)
        elif each_user_game.done_game_group == 3:
            user_game_C.append(each_user_game)
        elif each_user_game.done_game_group == 4:
            user_game_D.append(each_user_game)
        elif each_user_game.done_game_group == 5:
            user_game_E.append(each_user_game)

    # Return 값은 List of dictionaries

    # 각각에 대해서, 한 게임, 안 한 게임을 나누는 작업 시도

    user_new_A = []
    for each_game in user_game_A:
        if each_game.done_game not in user_game_A:
            user_new_A.append(each_game.done_game)

    user_new_B = []
    for each_game in user_game_B:
        if each_game.done_game not in user_game_B:
            user_new_B.append(each_game.done_game)

    user_new_C = []
    for each_game in user_game_C:
        if each_game.done_game not in user_game_C:
            user_new_C.append(each_game.done_game)

    user_new_D = []
    for each_game in user_game_D:
        if each_game.done_game not in user_game_D:
            user_new_D.append(each_game.done_game)

    user_new_E = []
    for each_game in user_game_E:
        if each_game.done_game not in user_game_E:
            user_new_E.append(each_game.done_game)

    '''
    user_new_history = []
    for idx in user_game_history:
        # 따라서 Idx 는 각각 dictionary
        if idx.done_game not in user_new_history:
            user_new_history.append(idx.done_game)
    '''

    def missing_elements(L):
        start, end = L[0], L[-1]
        return sorted(set(range(start, end + 1)).difference(L))


    def each_game_var(user_new_list):
        if len(user_new_list) == 0:
            user_new_list.append(1)
            return 1
        else:
            A = missing_elements(user_new_list)
            if len(A) > 0:
                return A[0]
            else:
                return user_new_list[len(user_new_list) - 1] + 1

    game_A = each_game_var(user_new_A)
    game_B = each_game_var(user_new_B)
    game_C = each_game_var(user_new_C)
    game_D = each_game_var(user_new_D)
    game_E = each_game_var(user_new_E)

    return [game_A, game_B, game_C, game_D, game_E]


@app.route('/main/A', methods=['GET', 'POST'])
def match_A():
    if g.user_email is None:
        flash(u'로그인 후에 이용해주세요', 'danger')
        return redirect(url_for('login'))
    else:
        # 얘는 리스트가 되었다!
        match_id = check_user_match(g.user_email)
        player_game = Match.query.filter(Match.group == 1, Match.game_round == match_id[0]).all()
        player_game = player_game[0]
        comments = Comment.query.order_by(asc(Comment.date_created)).all()

        return render_template("home.html", player_game=player_game, active_tab="match", comments=comments)


@app.route('/main/B', methods=['GET', 'POST'])
def match_B():
    if g.user_email is None:
        flash(u'로그인 후에 이용해주세요', 'danger')
        return redirect(url_for('login'))
    else:
        match_id = check_user_match(g.user_email)
        player_game = Match.query.filter(Match.group == 2, Match.game_round == match_id[1]).all()
        player_game = player_game[0]

        comments = Comment.query.order_by(asc(Comment.date_created)).all()

        return render_template("home.html", player_game=player_game, active_tab="match", comments=comments)


@app.route('/main/C', methods=['GET', 'POST'])
def match_C():
    if g.user_email is None:
        flash(u'로그인 후에 이용해주세요', 'danger')
        return redirect(url_for('login'))
    else:
        match_id = check_user_match(g.user_email)
        player_game = Match.query.filter(Match.group == 3, Match.game_round == match_id[2]).all()
        player_game = player_game[0]

        comments = Comment.query.order_by(asc(Comment.date_created)).all()

        return render_template("home.html", player_game=player_game, active_tab="match", comments=comments)


@app.route('/main/D', methods=['GET', 'POST'])
def match_D():
    if g.user_email is None:
        flash(u'로그인 후에 이용해주세요', 'danger')
        return redirect(url_for('login'))
    else:
        match_id = check_user_match(g.user_email)
        player_game = Match.query.filter(Match.group == 4, Match.game_round == match_id[3]).all()
        player_game = player_game[0]

        comments = Comment.query.order_by(asc(Comment.date_created)).all()

        return render_template("home.html", player_game=player_game, active_tab="match", comments=comments)


@app.route('/main/E', methods=['GET', 'POST'])
def match_E():
    if g.user_email is None:
        flash(u'로그인 후에 이용해주세요', 'danger')
        return redirect(url_for('login'))
    else:
        match_id = check_user_match(g.user_email)
        # flash(match_id)
        # player_game = Match.query.filter(Match.game_round == match_id).all()
        player_game = Match.query.filter(Match.group == 5, Match.game_round == match_id[4]).all()
        player_game = player_game[0]

        comments = Comment.query.order_by(asc(Comment.date_created)).all()

        return render_template("home.html", player_game=player_game, active_tab="match", comments=comments)


@app.route('/main', methods=['GET', 'POST'])
def match():
    if g.user_email is None:
        flash(u'로그인 후에 이용해주세요', 'danger')
        return redirect(url_for('login'))
    else:

        match_id = check_user_match(g.user_email)
        # flash(match_id)
        player_game = Match.query.filter(Match.game_round == match_id).all()
        player_game = player_game[0]

        comments = Comment.query.order_by(asc(Comment.date_created)).all()

        next_data = {}
        next_data['Aphoto'] = player_game.candidate_A_photolink
        next_data['Bphoto'] = player_game.candidate_B_photolink
        next_data['Aname'] = player_game.candidate_A_namename
        next_data['Bname'] = player_game.candidate_B_namename

        return render_template("home.html", player_game=player_game, active_tab="match", comments=comments)


@app.route('/vote/<matnum>/ <int:candnum> / <int:gamegroup> ', methods=['GET'])
def vote(matnum, candnum, gamegroup):
    # # SEASON 도 뽑아오기
    matnum = int(matnum)
    # 얘는 match round
    this_match = Match.query.filter(Match.game_round == matnum).all()
    this_match = this_match[0]
    gameresult = 0
    if candnum == 1:
        this_match.candidate_A_count += 1
        gameresult = candnum
        winner_name = this_match.candidate_A_namename
        winner_school = this_match.candidate_A_school
        winner_photo = this_match.candidate_A_school
    elif candnum == 2:
        this_match.candidate_B_count += 1
        gameresult = candnum
        winner_name = this_match.candidate_B_namename
        winner_school = this_match.candidate_B_school
        winner_photo = this_match.candidate_B_school

    # 유저가 이 게임을 했다.


    user_email = g.user_email
    Game_table = GameHistory.query.filter(GameHistory.user_email == user_email)
    User_Game_Season = []

    for each in Game_table:
        User_Game_Season.append(each.done_game_season)

    if len(User_Game_Season) > 0:
        current_season = min(User_Game_Season)
    else:
        current_season = 32


    # Winner DB에 사람을 채워 넣장


    winner_data = Winner(
        user_email = user_email,
        game_season = current_season / 2,
        game_round = matnum,
        game_group = gamegroup,
        winner_A_namename = winner_name,
        winner_A_school = winner_school,
        winner_A_photolink = winner_photo
    )




    this_game = GameHistory(
        user_email=g.user_email,
        done_game=matnum,
        done_game_group=gamegroup,
        done_game_season= current_season,
        done_game_result=gameresult
    )
    db.session.add(this_game)
    db.session.add(winner_data)
    db.session.commit()

    if gamegroup == 1:
        return redirect(url_for('match_A'))
    elif gamegroup == 2:
        return redirect(url_for('match_B'))
    elif gamegroup == 3:
        return redirect(url_for('match_C'))
    elif gamegroup == 4:
        return redirect(url_for('match_D'))
    else:
        return redirect(url_for('match_E'))


@app.route('/logout', methods=['GET'])
def log_out():
    session.clear()
    return redirect(url_for('login'))


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
                flash(u'가입이 완료되었습니다.', 'success')
                return redirect(url_for('login'))
            else:
                flash(u'이미 존재하는 USER', 'danger')
                return redirect(url_for('user_join'))
        else:
            flash(u'작성형식에 맞지 않습니다.', 'success')
    else:
        return render_template('user/join.html', form=form)


@app.route('/tournament', methods=['GET', 'POST'])
def tournament():
    if g.user_email == None:
        flash(u'로그인 후에 이용해주세요', 'danger')
        return redirect(url_for('login'))
    else:
        return render_template("tournament.html", active_tab="tournament")


@app.route('/candidate_list/A', methods=['GET', 'POST'])
def candidate_list_A():
    if g.user_email == None:
        flash(u'로그인 후에 이용해주세요', 'danger')
        return redirect(url_for('login'))
    else:
        group_people = Match.query.order_by(asc(Match.game_round)).filter(Match.group == 1).all()
        total_people = []
        people = []
        people_count = 0
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

        return render_template("candidate_list.html", total_people=total_people[0])
        # return total_people[0][30]['photo']


@app.route('/candidate_list/B', methods=['GET', 'POST'])
def candidate_list_B():
    if g.user_email == None:
        flash(u'로그인 후에 이용해주세요', 'danger')
        return redirect(url_for('login'))
    else:
        group_people = Match.query.order_by(asc(Match.game_round)).filter(Match.group == 2).all()
        total_people = []
        people = []
        people_count = 0
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

        return render_template("candidate_list.html", total_people=total_people[0])


@app.route('/candidate_list/C', methods=['GET', 'POST'])
def candidate_list_C():
    if g.user_email == None:
        flash(u'로그인 후에 이용해주세요', 'danger')
        return redirect(url_for('login'))
    else:
        group_people = Match.query.order_by(asc(Match.game_round)).filter(Match.group == 3).all()
        total_people = []
        people = []
        people_count = 0
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

        return render_template("candidate_list.html", total_people=total_people[0])


@app.route('/candidate_list/D', methods=['GET', 'POST'])
def candidate_list_D():
    if g.user_email == None:
        flash(u'로그인 후에 이용해주세요', 'danger')
        return redirect(url_for('login'))
    else:
        group_people = Match.query.order_by(asc(Match.game_round)).filter(Match.group == 4).all()
        total_people = []
        people = []
        people_count = 0
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

        return render_template("candidate_list.html", total_people=total_people[0])


@app.route('/candidate_list/E', methods=['GET', 'POST'])
def candidate_list_E():
    if g.user_email == None:
        flash(u'로그인 후에 이용해주세요', 'danger')
        return redirect(url_for('login'))
    else:
        group_people = Match.query.order_by(asc(Match.game_round)).filter(Match.group == 5).all()
        total_people = []
        people = []
        people_count = 0
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

        return render_template("candidate_list.html", total_people=total_people[0])


@app.route('/candidate/<int:myseason>/<int:mygame_round>/<int:mygroup>/<int:idx>', methods=['GET', 'POST'])
def candidate(myseason, mygame_round,mygroup,idx):
    if g.user_email == None:
        flash(u'로그인 후에 이용해주세요', 'danger')
        return redirect(url_for('login'))
    else:
        cand_data = {}
        each_match = Match.query.filter(Match.group == mygroup, Match.game_round == mygame_round)[0]
        if idx % 2 == 1:
            name = each_match.candidate_A_namename
            school = each_match.candidate_A_school
            photo = each_match.candidate_A_photolink
        else:
            name = each_match.candidate_B_namename
            school = each_match.candidate_B_school
            photo = each_match.candidate_B_photolink

        cand_data['name'] = name
        cand_data['school'] = school
        cand_data['photo'] = photo
        return render_template("candidate_page.html", cand_data=cand_data, active_tab="candidate")
        #return render_template("candidate_page.html",  active_tab="candidate")
        #return name



@app.route('/debug')
def debugdebug():
    A = Match.query.filter(Match.game_round == 1, Match.group == 1)[0]
    return A.candidate_A_photolink







@app.route('/comment/create', methods=['GET', 'POST'])
def comment_create():
    if request.method == 'POST':
        comment = Comment(
            content=request.form['content']
        )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('testest'))
    return render_template('home.html')







