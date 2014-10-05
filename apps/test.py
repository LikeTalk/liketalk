# -*- coding: utf-8 -*-
import random

from flask import request, g, jsonify, render_template
from apps import app, db
from apps.models import Match,  GameHistory
import re


import admin, candidate, comment, debug, tournament, user_account, view_page, what_match


# 이 route에서 json으로 숫자를 받아오고, 계산을 처리해준다.
@app.route('/_add_numbers', methods= ['GET','POST'])
def add_numbers():
    a = request.args.get('num', 0, type=int)
    myid = request.args.get('myid', type=str)
	# result 라는 이름으로 HTML에 쏴준다. JSON 형태로.

    # 여기서 숫자를 분리해낸다.
    r = re.compile("([a-zA-Z]+)([0-9]+)")
    m = r.match(myid)
    id_num = m.group(2)
    id_num = int(id_num) # 이건 사진 ID의 Index
    current_id_num = id_num
    id_num += 1

    all_game = ["a","b"]

    candclass = m.group(1)
    showid = candclass + str(id_num)
    hideid = candclass + str(current_id_num)
    hideid = "#" + hideid
    showid = "#" + showid

    if candclass == 'a':
        unchosen_class = 'b'
    else :
        unchosen_class = 'a'

    showid2 = "#"+ unchosen_class + str(id_num)
    hideid2 = "#"+ unchosen_class + str(current_id_num)


    #return jsonify(result=myid, show_num = id_num+1, showid = showid, hideid = hideid, showid2 = showid2, hideid2 = hideid2)
    return jsonify(showid = showid, hideid = hideid, showid2 = showid2, hideid2 = hideid2)


@app.route('/test')
def mytest():
    return render_template("testpage.html")


@app.route('/lot_photo', methods = ['GET', 'POST'])
def lot_photo():
    all_match = Match.query.all()
    A_photo = []
    B_photo = []
    for each in all_match:
        A_photo.append(each.candidate_A_photolink)
        B_photo.append(each.candidate_B_photolink)
    show_num = 1
    #disp_num = img_idx.remove(show_num)

    return render_template("lot_photo.html", A_photo = A_photo, B_photo = B_photo, shownum = show_num)

