# -*- coding: utf-8 -*-
import json
from flask import render_template, request, redirect, url_for, flash, session, g, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc, asc
from apps import app, db
from apps.forms import CommentForm, JoinForm, LoginForm
from apps.models import User, Comment, Match, Candidate, GameHistory

import random
import math
from itertools import count, izip
from person_info import uos, ajou, gachon, hanyang, kaist, khu, korea, mju, sejong, snu_yonsei, ssu, teacher


def chunk(mylist):
    temp = zip(*[iter(mylist)] * 2)
    return [list(x) for x in temp]


@app.route('/newnew_input')
def newnew():
    # return "\n".join( [ student[0] for student in  kaist.students] )
    ajou_info = [st for st in ajou.students] + [tc for tc in ajou.teachers]
    gachon_info = [st for st in gachon.students] + \
        [tc for tc in gachon.teachers]
    hanyang_info = [st for st in hanyang.students] + \
        [tc for tc in hanyang.teachers]
    kaist_info = [st for st in kaist.students] + [tc for tc in kaist.teachers]
    khu_info = [st for st in khu.students] + [tc for tc in khu.teachers]
    mju_info = [st for st in mju.students] + [tc for tc in mju.teachers]
    sejong_info = [st for st in sejong.students] + \
        [tc for tc in sejong.teachers]
    snu_yonseig_info = [st for st in snu_yonsei.students] + [
        tc for tc in snu_yonsei.teachers]
    ssu_info = [st for st in ssu.students] + [tc for tc in ssu.teachers]
    uos_info = [st for st in uos.students] + [tc for tc in uos.teachers]

    all_info = ajou_info + gachon_info + hanyang_info + kaist_info + \
        khu_info + mju_info + sejong_info + \
        snu_yonseig_info + ssu_info + uos_info
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
            name = name,
            photolink = photo_link,
            school = school
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
    #candidate_members = Candidate.query.all()
    #candidate_members[0].photolink

    candidate_members = Candidate.query.all()
    random.shuffle(candidate_members)
    candidate_members = candidate_members[:160]
    candidate_members = chunk(candidate_members)

    idx = 0

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
            game_group = "A"
        elif idx > 15 and idx < 32:
            game_group = "B"
        elif idx > 31 and idx < 48:
            game_group = "C"
        elif idx > 47 and idx < 64:
            game_group = "D"
        #elif idx <= 128 and idx < 160:
        else:
            game_group = "E"

        my_match = Match(
            season_num=32,
            game_round=idx,
            candidate_A_namename=nameA,
            candidate_A_photolink=photoA,
            candidate_A_school=orgA,
            candidate_B_namename=nameB,
            candidate_B_photolink=photoB,
            candidate_B_school=orgB,
            group = game_group
        )
        db.session.add(my_match)
        db.session.commit()
        idx += 1









# 뭐하지?
'''
1. 유저가 로그인을 했습니다.
2. 32명을 랜덤으로 뿌려줌 ㅋㅋ
'''


# 한 번 들어가면 season을 입력시켜준다.
# 지워도 되는 부분
@app.route('/input_match')
def input_match():
    # return "\n".join( [ student[0] for student in  kaist.students] )
    ajou_info = [st for st in ajou.students] + [tc for tc in ajou.teachers]
    gachon_info = [st for st in gachon.students] + \
        [tc for tc in gachon.teachers]
    hanyang_info = [st for st in hanyang.students] + \
        [tc for tc in hanyang.teachers]
    kaist_info = [st for st in kaist.students] + [tc for tc in kaist.teachers]
    khu_info = [st for st in khu.students] + [tc for tc in khu.teachers]
    mju_info = [st for st in mju.students] + [tc for tc in mju.teachers]
    sejong_info = [st for st in sejong.students] + \
        [tc for tc in sejong.teachers]
    snu_yonseig_info = [st for st in snu_yonsei.students] + [
        tc for tc in snu_yonsei.teachers]
    ssu_info = [st for st in ssu.students] + [tc for tc in ssu.teachers]
    uos_info = [st for st in uos.students] + [tc for tc in uos.teachers]

    all_info = ajou_info + gachon_info + hanyang_info + kaist_info + \
        khu_info + mju_info + sejong_info + \
        snu_yonseig_info + ssu_info + uos_info
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
        cand_num = db.session.query(Match).filter(
            Match.season_num == season, Match.game_round == idx)[0]
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

    next_game = db.session.query(Match).filter(
        Match.season_num == season, Match.game_round == roundnum + 1)[0]

    next_data = {
        "Aphotolink": str('static/') + str(next_game.candidate_A_photolink), "Bphotolink": str('static/') + str(next_game.candidate_B_photolink),
        "Acount": next_game.candidate_A_count, "Bcount": next_game.candidate_B_count,
        "Aname": next_game.candidate_A_namename, "Bname": next_game.candidate_B_namename, "Aschool": next_game.candidate_A_school,
        "Bschool": next_game.candidate_B_school, "next_round": roundnum + 1}

    if cand1_selected == 0 and cand1_count == 0:
        # cand2 selected
        this_match = db.session.query(Match).filter(
            Match.season_num == season, Match.game_round == roundnum)[0]
        this_match.candidate_B_count += 1
    elif cand2_selected == 0 and cand2_count == 0:
        this_match = db.session.query(Match).filter(
            Match.season_num == season, Match.game_round == roundnum)[0]
        this_match.candidate_A_count += 1

    this_game = GameHistory(
        user_email=g.user_email,
        done_game=roundnum
    )
    db.session.add(this_game)
    db.session.commit()
    return jsonify(next_data=next_data)


@app.route('/testtest')
def testest():
    return "\n".join([student[0] for student in uos.students])


@app.route('/match_data', methods=['GET'])
def match_data():
    match_all = Match.query.all()
    count_data = []
    candidate_data = []
    seed_data = []
    # test_name = match_all[0].candidate_A_namename

    #일단 A그룹에 대해서만 생각해보자
    r = [[], [], [], [], [], []]

    for i in range(16):
        name_A = match_all[i].candidate_A_namename
        name_B = match_all[i].candidate_B_namename
        seed_num_A = (i + 1) * 2 - 1
        seed_num_B = (i + 1) * 2
        add_name = [{"name": name_A, "id": name_A, "seed": seed_num_A}, {"name": name_B, "id": name_B, "seed": seed_num_B}]
        r[0].append(add_name)

        if match_all[i].candidate_A_count > match_all[i].candidate_B_count:
            count_data.append(match_all[i].candidate_A_count)
            candidate_data.append(name_A)
            seed_data.append(seed_num_A)
        else:
            count_data.append(match_all[i].candidate_B_count)
            candidate_data.append(name_B)
            seed_data.append(seed_num_B)


    ### tournament
    totalgames = len(count_data)-1
    gameid = 0
    roundid = 0
    count_nextround = []
    candidate_nextround = []
    seed_nextround = []
    r_num = 1
    teamlist = count_data

    while gameid < totalgames:
        if gameid in [8, 12, 14]:
            teamlist = count_nextround
            candidate_data = candidate_nextround
            seed_data = seed_nextround
            count_nextround = []
            candidate_nextround = []
            seed_nextround = []
            roundid = 0
            r_num += 1

        homeid = teamlist[roundid]
        awayid = teamlist[roundid + 1]
        name_A = candidate_data[roundid]
        name_B = candidate_data[roundid + 1]
        seed_num_A = seed_data[roundid]
        seed_num_B = seed_data[roundid + 1]
        add_name = [{"name": name_A, "id": name_A, "seed": seed_num_A}, {"name": name_B, "id": name_B, "seed": seed_num_B}]
        r[r_num].append(add_name)

        if homeid > awayid:
            count_nextround.append(homeid)
            candidate_nextround.append(name_A)
            seed_nextround.append(seed_num_A)

        else:
            count_nextround.append(awayid)
            candidate_nextround.append(name_B)
            seed_nextround.append(seed_num_B)
    
        gameid += 1
        roundid += 2

    add_name = [{"name": candidate_nextround, "id": candidate_nextround, "seed": seed_nextround}]
    r[r_num + 1].append(add_name)


    # r = [
    #     [
    #         [{"name": test_name, "id": test_name, "seed": 1, "displaySeed": "D1", "score": 47},
    #          {"name": "Andrew Miller", "id": "andrew-miller", "seed": 2}],
    #         [{"name": "James Coutry", "id": "james-coutry", "seed": 3},
    #          {"name": "Sam Merrill", "id": "sam-merrill", "seed": 4}],
    #         [{"name": "Anothy Hopkins", "id": "anthony-hopkins", "seed": 5},
    #          {"name": "Everett Zettersten", "id": "everett-zettersten", "seed": 6}],
    #         [{"name": "John Scott", "id": "john-scott", "seed": 7},
    #          {"name": "Teddy Koufus", "id": "teddy-koufus", "seed": 8}],
    #         [{"name": "Arnold Palmer", "id": "arnold-palmer", "seed": 9},
    #          {"name": "Ryan Anderson", "id": "ryan-anderson", "seed": 10}],
    #         [{"name": "Jesse James", "id": "jesse-james", "seed": 1},
    #          {"name": "Scott Anderson", "id": "scott-anderson", "seed": 12}],
    #         [{"name": "Josh Groben", "id": "josh-groben", "seed": 13},
    #          {"name": "Sammy Zettersten", "id": "sammy-zettersten", "seed": 14}],
    #         [{"name": "Jake Coutry", "id": "jake-coutry", "seed": 15},
    #          {"name": "Spencer Zettersten", "id": "spencer-zettersten", "seed": 16}]
    #     ],
    #     [
    #         [{"name": "Erik Zettersten", "id": "erik-zettersten", "seed": 1},
    #          {"name": "James Coutry", "id": "james-coutry", "seed": 3}],
    #         [{"name": "Anothy Hopkins", "id": "anthony-hopkins", "seed": 5},
    #          {"name": "Teddy Koufus", "id": "teddy-koufus", "seed": 8}],
    #         [{"name": "Ryan Anderson", "id": "ryan-anderson", "seed": 10},
    #          {"name": "Scott Anderson", "id": "scott-anderson", "seed": 12}],
    #         [{"name": "Sammy Zettersten", "id": "sammy-zettersten", "seed": 14},
    #          {"name": "Jake Coutry", "id": "jake-coutry", "seed": 15}]
    #     ],
    #     [
    #         [{"name": "Erik Zettersten", "id": "erik-zettersten", "seed": 1},
    #          {"name": "Anothy Hopkins", "id": "anthony-hopkins", "seed": 5}],
    #         [{"name": "Ryan Anderson", "id": "ryan-anderson", "seed": 10},
    #          {"name": "Sammy Zettersten", "id": "sammy-zettersten", "seed": 14}]
    #     ],
    #     [
    #         [{"name": "Erik Zettersten", "id": "erik-zettersten", "seed": 1},
    #          {"name": "Ryan Anderson", "id": "ryan-anderson", "seed": 10}]
    #     ],
    #     [
    #         [{"name": "Erik Zettersten", "id": "erik-zettersten", "seed": 1}]
    #     ]
    # ]

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
        return render_template('user/join.html', form=form, active_tab="user_join")


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


@app.route('/comment/create', methods=['GET', 'POST'])
def comment_create():
    if request.method == 'POST':
        comment = Comment(
            content=request.form['content']
        )
        db.session.add(comment)
        db.session.commit()
        return redirect(url_for('match'))
    return render_template('home.html')
