# -*- coding: utf-8 -*-
import random

from flask import request, g, jsonify
from apps import app, db
from apps.models import Match,  GameHistory


import admin, candidate, comment, debug, test, tournament, user_account, view_page, what_match


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