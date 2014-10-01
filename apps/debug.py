# -*- coding: utf-8 -*-

import json
from flask import render_template, request, redirect, url_for, flash, session, g, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from sqlalchemy import desc, asc
from apps import app, db
from apps.forms import CommentForm, JoinForm, LoginForm
from apps.models import User, Comment, Match, Candidate, GameHistory, Winner, UserCommentHistory, Indiv_Comment, Bulletin

import random
import math
from itertools import count, izip
from person_info import uos, ajou, gachon, hanyang, kaist, khu, korea, mju, sejong, snu_yonsei, ssu
from datetime import datetime
from pytz import timezone

import admin, candidate, comment, debug, test, tournament, user_account, view_page, what_match


@app.route('/debug')
def debug():
    ajou_info = [tc for tc in ajou.teachers]
    gachon_info = [tc for tc in gachon.teachers]
    hanyang_info = [tc for tc in hanyang.teachers]
    kaist_info = [tc for tc in kaist.teachers]
    khu_info = [tc for tc in khu.teachers]
    korea_info = [tc for tc in korea.teachers]
    mju_info =  [tc for tc in mju.teachers]
    sejong_info = [tc for tc in sejong.teachers]
    snu_yonseig_info =  [tc for tc in snu_yonsei.teachers]
    ssu_info = [tc for tc in ssu.teachers]
    uos_info = [tc for tc in uos.teachers]

    all_teacher = [tc for tc in ajou.teachers] + [tc for tc in gachon.teachers] + [tc for tc in hanyang.teachers] + [tc for tc in kaist.teachers] + [tc for tc in khu.teachers] + [tc for tc in korea.teachers] + [tc for tc in mju.teachers] + [tc for tc in sejong.teachers] + [tc for tc in snu_yonsei.teachers] + [tc for tc in ssu.teachers] + [tc for tc in uos.teachers]


    return str(len(all_teacher))
