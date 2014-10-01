# -*- coding: utf-8 -*-

import json
from flask import render_template, request, redirect, url_for, flash, session, g, jsonify
from apps.models import Match
from apps import app, db

import admin, candidate, comment, debug, test, tournament, user_account, view_page, what_match

# tournament (대진표) 페이지에서 대진표 정보를 계산해서 뿌려주는 함수
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
