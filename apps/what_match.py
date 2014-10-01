# -*- coding: utf-8 -*-

from flask import g, render_template, redirect, url_for, flash
from apps import app, db
from apps.models import Match, GameHistory, Comment, Winner
from sqlalchemy import desc, asc
import admin, candidate, comment, debug, test, tournament, user_account, view_page, what_match

# list에서 서로 같은 element가 없도록 만들어주는 함수
def intersection_removal(mylist):
    new_list = []
    for elem in mylist:
        if elem not in new_list:
            new_list.append(elem)
    return new_list


def chunk(mylist):
    temp = zip(*[iter(mylist)] * 2)
    return [list(x) for x in temp]



# 유저의 정보와 몇강인지 (시즌) 정보를 받아서, 어떤 게임을 해야 하는지 라운드번호와 시즌을 보내주는 함수
# 6개 그룹에 대해서 라운드 번호를 계산해준다.
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
    user_game_F = []

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
        elif each_user_game.done_game_group == 6:
            user_game_F.append(each_user_game)

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

    user_new_F = []
    for each_game in user_game_F:
        if each_game.done_game not in user_game_F:
            user_new_F.append(each_game.done_game)

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
    game_F = each_game_var(user_new_F)

    return [game_A, game_B, game_C, game_D, game_E, game_F]




@app.route('/main/<int:group>', methods=['GET', 'POST'])
def match(group):
    if g.user_email == None:
        flash(u'로그인 후에 이용해주세요', 'danger')
        return redirect(url_for('login'))
    else:

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
            return render_template("home.html", player_game=player_game, comments = comments, active_tab="match", season = season, group = group)






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
