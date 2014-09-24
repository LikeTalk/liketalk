# -*- coding: utf-8 -*-
import json
from flask import render_template, request, redirect, url_for, flash, session, g, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc, asc
from apps import app, db
from apps.forms import CommentForm, JoinForm, LoginForm
from apps.models import User, Comment, Match, Candidate, GameHistory, Winner, UserCommentHistory, Indiv_Comment

import random
import math
from itertools import count, izip
from person_info import uos, ajou, gachon, hanyang, kaist, khu, korea, mju, sejong, snu_yonsei, ssu, teacher


def chunk(mylist):
    temp = zip(*[iter(mylist)] * 2)
    return [list(x) for x in temp]


@app.route('/init_cand_vote')
def init_cand_vote():
    match = Match.query.all()
    for each_match in match:
        each_match.candidate_A_count = 0
        each_match.candidate_B_count = 0

    db.session.commit()


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
        elif idx >= 48 and idx < 64:
            game_group = 4
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


    next_data = {"Aphotolink": str('static/') + str(next_game.candidate_A_photolink),
                 "Bphotolink": str('static/') + str(next_game.candidate_B_photolink),
                 "Acount": next_game.candidate_A_count, "Bcount": next_game.candidate_B_count,
                 "Aname": next_game.candidate_A_namename, "Bname": next_game.candidate_B_namename,
                 "Aschool": next_game.candidate_A_school,
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


@app.route('/group')
def testest():
    if g.user_email == None:
        flash(u'로그인 후에 이용해주세요', 'danger')
        return redirect(url_for('login'))
    else:
        return render_template("Select_Group.html", active_tab="group")


@app.route('/match_data/<int:group_sort>', methods=['GET'])
def match_data(group_sort):
    match_all = Match.query.all()
    count_data = []
    candidate_data = []
    seed_data = []
    r = [[], [], [], [], [], []]
    
    #set 32 people 
    n1 = group_sort * 16
    n2 = n1 + 16

    for i in range(n1, n2):
        name_A = match_all[i].candidate_A_namename
        name_B = match_all[i].candidate_B_namename
        seed_num_A = (i + 1) * 2 - 1
        seed_num_B = (i + 1) * 2
        add_name = [{"name": name_A, "id": name_A, "seed": seed_num_A}, {"name": name_B, "id": name_B, "seed": seed_num_B}]
        r[0].append(add_name)

        #make list(size=16) for calculation tournament
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
                # render_template('Select_Group.html')
                # return redirect(url_for('match'))
                return redirect(url_for('testest'))
    return render_template('user/login.html', form=form, active_tab='log_in')


@app.before_request
def before_request():
    g.user_email = None
    if 'user_email' in session:
        g.user_email = session['user_email']



def check_user_match(user_email, season):
    # 로그인한 유저가 했던 게임을 쪼아아아아악 나열
    user_game_history = GameHistory.query.order_by(asc(GameHistory.done_game)).filter(
        GameHistory.user_email == user_email, GameHistory.done_game_season == season).all()

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



def intersection_removal(mylist):
    new_list = []
    for elem in mylist:
        if elem not in new_list:
            new_list.append(elem)
    return new_list





@app.route('/debug')
def debugdebug():
    user_email = g.user_email
    group = 3

    def check_user_status_by_season(season):
        # for all Game History Model of Logged in USER
        logged_user_game = GameHistory.query.order_by(asc(GameHistory.done_game)).filter(GameHistory.user_email == user_email, GameHistory.done_game_season == season, GameHistory.done_game_group == group).all()

        if len(logged_user_game) == 0:
            return -1 # EMPTY
        else:
            return logged_user_game

        # 시즌별로 각 게임의 done_game을 Dict 형태로 출력
    def each_season_status():
        season = [32,16,8,4,2,1]
        season_done_game = {}
        for each_season in season:
            each_history = check_user_status_by_season(each_season)
            if each_history != -1:
                for each_game_season in each_history:
                    season_done_game.update( {each_season :  each_game_season.done_game}   )
            else:
                season_done_game.update( {each_season :  0}   )
        return season_done_game

    # 각 시즌별로 done인지 아닌지 살피고, 어떤 시즌을 돌려야하는지 알려준다.
    def which_season(season_done_game):
        season_status = {}
        status_val = season_done_game.values()
        for key in season_done_game:
            if season_done_game[key] >= key/2:
                # 이럼 이 시즌은 다 했다는 뜻
                season_status.update({key : "done"})
            elif 0< season_done_game[key] < key/2:
                season_status.update({key: "ongoing"})
            else:
                season_status.update({key:"yet"})
                # 아직 시작

        status_val = season_status.values()
        if intersection_removal(status_val)[0] == "yet":
            season_status[32] = "ongoing"

        for prev_key in season_done_game:
            next_key = prev_key / 2
            if next_key != 0 and season_status[prev_key] == "done" and season_status[next_key] == "yet":
                season_status[next_key] = "ongoing"
        for key in season_status:
            if season_status[key] == "ongoing":
                return key
            elif key == 32 and season_status[key] == 1:
                return 32


    def game_address():
        # 유저가 할 게임의 시즌과 라운드를 불러준다.
        season_done_game = each_season_status()
        season = which_season(season_done_game=season_done_game)
        if season == 32:
            match_id = check_user_match(g.user_email, season)
            player_game = Match.query.filter(Match.group == group, Match.game_round == match_id[group-1]).all()
            player_game = player_game[0]
            return player_game
        else:
            match_id = check_user_match(user_email, season)
            new_game_list = Winner.query.order_by(asc(Winner.game_round)).filter(Winner.user_email == user_email, Winner.game_group == group, Winner.game_season == season).all()
            match = chunk(new_game_list)
            if season == 1:
                return "STOP"
            else:
                player_game = {}
                player_game['season_num'] = season
                player_game['game_round'] = match_id[group-1]
                player_game['candidate_A_namename'] = match[match_id[group-1]-1][0].winner_A_namename
                player_game['candidate_A_school'] = match[match_id[group-1]-1][0].winner_A_school
                player_game['candidate_A_photolink'] = match[match_id[group-1]-1][0].winner_A_photolink
                player_game['candidate_B_namename'] = match[match_id[group-1]-1][1].winner_A_namename
                player_game['candidate_B_school'] = match[match_id[group-1]-1][1].winner_A_school
                player_game['candidate_B_photolink'] = match[match_id[group-1]-1][1].winner_A_photolink
                player_game['group'] = group
                return player_game

    season_done_game = each_season_status()
    season = which_season(season_done_game=season_done_game)
    return str(season)

@app.route('/main/congat/<int:group>', methods=['GET', 'POST'])
def END(group):
    user_email = g.user_email
    last_game = Winner.query.filter(Winner.game_season == 1, Winner.game_group == group, Winner.user_email == user_email).all()[0]
    name = last_game.winner_A_namename

    try:
        your_winner = Match.query.filter(Match.candidate_A_namename == name).all()[0]
        photo_address = your_winner.candidate_A_photolink
    except:
        your_winner = Match.query.filter(Match.candidate_B_namename == name).all()[0]
        photo_address = your_winner.candidate_B_photolink

    return render_template("end.html", last_game = last_game, photo = photo_address)



@app.route('/main/<int:group>', methods=['GET', 'POST'])
def match(group):
    user_email = g.user_email

    def check_user_status_by_season(season):
        # for all Game History Model of Logged in USER
        logged_user_game = GameHistory.query.order_by(asc(GameHistory.done_game)).filter(GameHistory.user_email == user_email, GameHistory.done_game_season == season, GameHistory.done_game_group == group).all()

        if len(logged_user_game) == 0:
            return -1 # EMPTY
        else:
            return logged_user_game

        # 시즌별로 각 게임의 done_game을 Dict 형태로 출력
    def each_season_status():
        season = [32,16,8,4,2,1]
        season_done_game = {}
        for each_season in season:
            each_history = check_user_status_by_season(each_season)
            if each_history != -1:
                for each_game_season in each_history:
                    season_done_game.update( {each_season :  each_game_season.done_game}   )
            else:
                season_done_game.update( {each_season :  0}   )
        return season_done_game

    # 각 시즌별로 done인지 아닌지 살피고, 어떤 시즌을 돌려야하는지 알려준다.
    def which_season(season_done_game):
        season_status = {}
        status_val = season_done_game.values()
        for key in season_done_game:
            if season_done_game[key] >= key/2:
                # 이럼 이 시즌은 다 했다는 뜻
                season_status.update({key : "done"})
            elif 0< season_done_game[key] < key/2:
                season_status.update({key: "ongoing"})
            else:
                season_status.update({key:"yet"})
                # 아직 시작

        status_val = season_status.values()
        if intersection_removal(status_val)[0] == "yet":
            season_status[32] = "ongoing"

        for prev_key in season_done_game:
            next_key = prev_key / 2
            if next_key != 0 and season_status[prev_key] == "done" and season_status[next_key] == "yet":
                season_status[next_key] = "ongoing"
        for key in season_status:
            if season_status[key] == "ongoing":
                return key
            elif key == 32 and season_status[key] == 1:
                return 32


    def game_address():
        # 유저가 할 게임의 시즌과 라운드를 불러준다.
        season_done_game = each_season_status()
        season = which_season(season_done_game=season_done_game)
        if season == 32:
            match_id = check_user_match(g.user_email, season)
            player_game = Match.query.filter(Match.group == group, Match.game_round == match_id[group-1]).all()
            player_game = player_game[0]
            return player_game
        else:
            match_id = check_user_match(user_email, season)
            new_game_list = Winner.query.order_by(asc(Winner.game_round)).filter(Winner.user_email == user_email, Winner.game_group == group, Winner.game_season == season).all()
            match = chunk(new_game_list)
            if season == None:
                return "STOP"
            else:
                player_game = {}
                player_game['season_num'] = season
                player_game['game_round'] = match_id[group-1]
                player_game['candidate_A_namename'] = match[match_id[group-1]-1][0].winner_A_namename
                player_game['candidate_A_school'] = match[match_id[group-1]-1][0].winner_A_school
                player_game['candidate_A_photolink'] = match[match_id[group-1]-1][0].winner_A_photolink
                player_game['candidate_B_namename'] = match[match_id[group-1]-1][1].winner_A_namename
                player_game['candidate_B_school'] = match[match_id[group-1]-1][1].winner_A_school
                player_game['candidate_B_photolink'] = match[match_id[group-1]-1][1].winner_A_photolink
                player_game['group'] = group
                return player_game
    player_game = game_address()
    if player_game == "STOP":
        return redirect(url_for("END", group = group))
    else:
        try :
            season = player_game.season_num
            season = int(season / 2)
        except:
            season = player_game['season_num']
            season = int(season / 2)
        comments = Comment.query.filter(Comment.comment_group == group).order_by(desc(Comment.date_created)).all()
        return render_template("home.html", player_game=player_game, comments = comments, active_tab="match", season = season)



@app.route('/vote/<matnum>/<int:candnum>/<int:gamegroup>/<int:season>/<name>', methods=['GET'])
def vote(matnum, candnum, gamegroup, season, name):
    # # SEASON 도 뽑아오기
    matnum = int(matnum)
    # 얘는 match round

    if season == 32:
        this_match = Match.query.filter(Match.game_round == matnum, Match.group == gamegroup).all()
        this_match = this_match[0]
    else:
        # GOAL : compute_this_match의 게임을 Match Model에서 불러오기
        try:
            this_match = Match.query.filter(Match.group == gamegroup, Match.candidate_A_namename == name).all()
            this_match = this_match[0]
        except:
            this_match = Match.query.filter(Match.group == gamegroup, Match.candidate_B_namename == name).all()
            this_match = this_match[0]
    gameresult = 0
    if name == this_match.candidate_A_namename:
        this_match.candidate_A_count += 1
        gameresult = candnum
        winner_name = this_match.candidate_A_namename
        winner_school = this_match.candidate_A_school
        winner_photo = this_match.candidate_A_photolink
    else:
        this_match.candidate_B_count += 1
        gameresult = candnum
        winner_name = this_match.candidate_B_namename
        winner_school = this_match.candidate_B_school
        winner_photo = this_match.candidate_B_photolink

    # 유저가 이 게임을 했다.


    user_email = g.user_email
    Game_table = GameHistory.query.filter(GameHistory.user_email == user_email)
    User_Game_Season = []

    for each in Game_table:
        User_Game_Season.append(each.done_game_season)

    # 다중클릭 방지
    game_history = Winner.query.filter(Winner.user_email == user_email, Winner.game_group == gamegroup, Winner.game_season == (season / 2) , Winner.game_round == matnum).all()
    if len(game_history) > 0:
        # 두번 클릭
        return redirect(url_for('match', group = gamegroup))
    else:
        winner_data = Winner(
            user_email = user_email,
            game_season = season / 2,
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
            done_game_season= season,
            done_game_result=gameresult
        )

        db.session.add(this_game)
        db.session.add(winner_data)
        db.session.commit()

        if season != 2:
            return redirect(url_for('match', group = gamegroup))
        else:
            return redirect(url_for('END', group = gamegroup))


@app.route('/logout', methods=['GET'])
def log_out():
    session.clear()
    Winner.query.filter(Winner.user_email == g.user_email).delete()
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

                session.permanent = True
                session['user_email'] = user.email
                flash(u'로그인 완료', 'success')
                return redirect(url_for('testest'))
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


@app.route('/candidate_list/<int:group>', methods=['GET', 'POST'])
def candidate_list(group):
    if g.user_email == None:
        flash(u'로그인 후에 이용해주세요', 'danger')
        return redirect(url_for('login'))
    else:
        group_people = Match.query.order_by(asc(Match.game_round)).filter(Match.group == group).all()
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
        random.shuffle(total_people[0])
        return render_template("candidate_list.html", total_people=total_people[0]. active_tab = "candidate_list")


@app.route('/candidate/<name>', methods=['GET', 'POST'])
def candidate(name):
    if g.user_email == None:
        flash(u'로그인 후에 이용해주세요', 'danger')
        return redirect(url_for('login'))
    else:
        cand_data = {}
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





@app.route('/comment/create/<int:gamegroup>/<int:season>/<int:game_round>/<comment_A>/<comment_B>', methods=['GET', 'POST'])
def comment_create(gamegroup, season, game_round, comment_A, comment_B):
    if request.method == 'POST':
        users_commented_history = UserCommentHistory.query.filter(UserCommentHistory.commented_group == gamegroup, UserCommentHistory.user_email == g.user_email).all()
        all_commens_history = UserCommentHistory.query.order_by(asc(UserCommentHistory.user_index)).filter(UserCommentHistory.commented_group == gamegroup).all()
        if len(all_commens_history) == 0:
            # 아무도 회원가입을 하지 않았으면,
            user_idx = 1
        elif len(all_commens_history) > 0 and len(users_commented_history) == 0:
            # 누군가가 회원가입을 했는데, 내가 안했으면
            existed_idx = []
            for each in all_commens_history:
                existed_idx.append(each.user_index)
            existed_idx = intersection_removal(existed_idx)
            sorted(existed_idx)
            user_idx = existed_idx[len(existed_idx)-1] + 1
        else:
            user_idx = users_commented_history[0].user_index

        user_comment_history = UserCommentHistory(
            user_email = g.user_email,
            commented_match = game_round,
            commented_group = gamegroup,
            commented_season = season,
            user_index = user_idx
        )
        db.session.add(user_comment_history)

        comment = Comment(
            content=request.form['content'],
            user_index=user_idx,
            comment_group = gamegroup,
            comment_gameround = game_round,
            comment_season = season,
            comment_A = comment_A,
            comment_B = comment_B
        )
        db.session.add(comment)
        db.session.add(user_comment_history)
        db.session.commit()

        return redirect(url_for('match', group = gamegroup))


    return render_template('home.html')



@app.route('/indiv_comments/<int:group>/<name>', methods = ['GET', 'POST'])
def candidate_comment(group, name):
    if request.method == 'POST':
        #USER INDEX Computation
        user_email = g.user_email
        all_comments = Indiv_Comment.query.order_by(asc(Indiv_Comment.user_index)).filter(Indiv_Comment.comment_group == group).all()
        user_comments = Indiv_Comment.query.filter(Indiv_Comment.user_email == user_email).all()
        # 아무도 댓글 입력 안했으면,
        if len(all_comments) == 0:
            user_idx = 1
        elif len(all_comments) > 0 and len(user_comments) == 0:
            #누군가가 댓글 입력했는데, 내가 안했으면
            existed_idx = []
            for each in all_comments:
                existed_idx.append(each.user_index)
            existed_idx = intersection_removal(existed_idx)
            sorted(existed_idx)
            user_idx = existed_idx[len(existed_idx)-1] + 1
        else:
            #누군가 댓글 입력하고, 나도 했으면
            user_idx = user_comments[0].user_index

        indiv_comment = Indiv_Comment(
            user_index = user_idx,
            content = request.form['content'],
            comment_name = name,
            comment_group = group,
            user_email = user_email
        )

        db.session.add(indiv_comment)
        db.session.commit()

        return redirect(url_for('candidate', name = name ))
    else:
        return redirect(url_for('candidate', name = name ))


@app.route('/all_comments', methods = ['GET','POST'])
def all_comments():
    comments = Comment.query.order_by(desc(Comment.date_created)).all()
    indiv_comments = Indiv_Comment.query.order_by(desc(Indiv_Comment.date_created)).all()
    return render_template('all_comment.html',indiv_comments = indiv_comments, comments = comments, active_tab = 'all_comments')


@app.route('/all_comments/<int:group>', methods=['GET', 'POST'])
def comments_group(group):
    comments = Comment.query.order_by(desc(Comment.date_created)).filter(Comment.comment_group == group).all()
    indiv_comments = Indiv_Comment.query.order_by(desc(Indiv_Comment.date_created)).filter(Indiv_Comment.comment_group == group).all()
    return render_template('all_comment.html', comments = comments, indiv_comments = indiv_comments, active_tab = 'all_comments')
