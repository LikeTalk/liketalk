# -*- coding: utf-8 -*-
from flask import render_template, request, redirect, url_for, flash, session, g, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc, asc
from apps import app, db
from apps.forms import CommentForm, JoinForm, LoginForm
from apps.models import User, Comment, Match, Candidate, GameHistory

import random
import math
from itertools import count, izip
from person_info import uos, ajou, gachon, hanyang, kaist, khu, korea, mju, sejong, snu_yonsei, ssu


def chunk(mylist):
    temp = zip(*[iter(mylist)] * 2)
    return [list(x) for x in temp]


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
        photoA = A[2]

        nameB = B[0]
        nameB = unicode(nameB, 'utf-8')
        orgB = B[1]
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
        if candA_num > candB_num:
            winner = cand_num.candidate_A_namename
            # winner = unicode(winner, 'utf-8')
        else:
            winner = cand_num.candidate_B_namename
            # winner = unicode(winner, 'utf-8')

    random.shuffle(new_cand)

    for idx in xrange(0, len(new_cand), 2):
        my_match = Match(
            season_num=int(season / 2),
            game_round=idx,
            candidate_A_namename=new_cand[idx],
            candidate_B_namename=new_cand[idx + 1],
        )
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

    next_data = {"Aphotolink": str('static/')+str(next_game.candidate_A_photolink), "Bphotolink": str('static/')+str(next_game.candidate_B_photolink),
                 "Acount": next_game.candidate_A_count, "Bcount": next_game.candidate_B_count,
                 "Aname" : next_game.candidate_A_namename, "Bname" : next_game.candidate_B_namename, "Aschool" : next_game.candidate_A_school,
                 "Bschool" : next_game.candidate_B_school, "next_round" : roundnum + 1 }

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

    return jsonify(next_data = next_data)


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
                return redirect(url_for('match'))
    return render_template('user/login.html', form=form, active_tab='log_in')


@app.before_request
def before_request():
    g.user_email = None
    if 'user_email' in session:
        g.user_email = session['user_email']


def check_user_match(user_email):
    # user_id 은 로그인한 유저의 아이디
    user_game_history = GameHistory.query.order_by(asc(GameHistory.done_game)).filter(
        GameHistory.user_email == user_email).all()
    # Return 값은 List of dictionaries

    user_new_history = []
    for idx in user_game_history:
        # 따라서 Idx 는 각각 dictionary
        if idx.done_game not in user_new_history:
            user_new_history.append(idx.done_game)

    def missing_elements(L):
        start, end = L[0], L[-1]
        return sorted(set(range(start, end + 1)).difference(L))

    if len(user_new_history) == 0:
        user_new_history.append(1)
        return 1
    else:
        A = missing_elements(user_new_history)
        if len(A) > 0:
            return A[0]
        else:
            return user_new_history[len(user_new_history) - 1] + 1


@app.route('/main', methods=['GET', 'POST'])
def match():
    if g.user_email == None:
        flash(u'로그인 후에 이용해주세요', 'danger')
        return redirect(url_for('login'))
    else:
        match_id = check_user_match(g.user_email)
        #flash(match_id)
        player_game = Match.query.filter(Match.game_round == match_id).all()
        player_game = player_game[0]
        # player_game= db.session.query(Match).filter_by(Match.game_round == match_id)

        next_data = {}
        next_data['Aphoto'] = player_game.candidate_A_photolink
        next_data['Bphoto'] = player_game.candidate_B_photolink
        next_data['Aname'] = player_game.candidate_A_namename
        next_data['Bname'] = player_game.candidate_B_namename


        return render_template("home.html", player_game=player_game, active_tab="match")


'''
1. 로그인한 유저는 자기가 안 했던 게임부터 시작해야 한다.
2. 게임이 시작되면, 유저는 자신이 했던 게임의 정보를 받아서 자신이 안한 게임을 보내주게 된다.
    2-1. 이는 처음에는 match함수로 구현이 되어야 한다.
3. 그 이후로 사진을 클릭하여 투표를 하게 되면
   3-1-1. 사진이 슥슥 넘어가게 된다.
   3-1-2. 얘는 Vote 함수를 고쳐서 해결이 되어야 한다.
        3-1-1-1. 이는 JavaScript 로 구현된다.

'''

'''
유저가 클릭하는 순간!
Game의 round number 와 candidate 번호가 request.args 의 형태로 전달된다.
그럼, candidate 번호는 투표 결과로써, DB에 저장하고,
round number 는 1만 올린다.
그리고 DB에 접속해서, 필요한 사진번호, 이름 등등을 모두 뽑아내서 JSON형태로 저장한다.
그리고 얘를 다시 HTML에 보내준다.
'''


@app.route('/vote/<matnum>/ <int:candnum>', methods=['GET'])
def vote(matnum, candnum):
    matnum = int(matnum)
    # 얘는 match round
    this_match = Match.query.filter(Match.game_round == matnum).all()
    this_match = this_match[0]
    if candnum == 1:
        this_match.candidate_A_count += 1
    elif candnum == 2:
        this_match.candidate_B_count += 1


    # 유저가 이 게임을 했다.
    this_game = GameHistory(
        user_email=g.user_email,
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


@app.route('/candidate_list', methods=['GET', 'POST'])
def candidate_list():
    if g.user_email == None:
        flash(u'로그인 후에 이용해주세요', 'danger')
        return redirect(url_for('login'))
    else:
        return render_template("candidate_list.html")


@app.route('/candidate', methods=['GET', 'POST'])
def candidate():
    if g.user_email == None:
        flash(u'로그인 후에 이용해주세요', 'danger')
        return redirect(url_for('login'))
    else:
        return render_template("candidate_page.html", active_tab="candidate")



