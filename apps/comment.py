# -*- coding: utf-8 -*-
import json
from flask import render_template, request, redirect, url_for, flash, session, g, jsonify
from sqlalchemy import desc, asc
from apps import app, db
from apps.models import User, Comment, Match, Candidate, GameHistory, Winner, UserCommentHistory, Indiv_Comment, Bulletin

from datetime import datetime
from pytz import timezone


import admin, candidate, comment, debug, test, tournament, user_account, view_page, what_match


# list에서 서로 같은 element가 없도록 만들어주는 함수
# [a,a,b] --> [a,b]
def intersection_removal(mylist):
    new_list = []
    for elem in mylist:
        if elem not in new_list:
            new_list.append(elem)
    return new_list


# 미국시간을 한국시간으로 바꾸어주는 함수
def timezone_compute():
    fmt = "%Y-%m-%d %H:%M:%S %Z%z"
    now_time = datetime.now(timezone('Asia/Tokyo'))
    return now_time.strftime(fmt)


# 매치에서 댓글을 달아주는 함수
@app.route('/comment/create/<int:gamegroup>/<int:season>/<int:game_round>/<comment_A>/<comment_B>', methods=['GET', 'POST'])
def comment_create(gamegroup, season, game_round, comment_A, comment_B):
    if request.method == 'POST':

        # 다음은 "밤부서비스" 처럼 유저에게 고유의 인덱싱을 주는 방법이다.
        # 유저가 회원가입을 한 순간 인덱싱을 줄 수 있지만, 그럼 유저1, 유저100 등 순서가 엉망일 것이기 때문에 다음의 인덱싱을 한다.

        # 유저가 댓글을 남기면, UserCommmentHistory Table에 기록된다. 유저의 댓글히스토리를 가져온다.
        users_commented_history = UserCommentHistory.query.filter(UserCommentHistory.commented_group == gamegroup, UserCommentHistory.user_email == g.user_email).all()
        # 모든 유저의 댓글 히스토리도 같이 가져온다.
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
            date_created = timezone_compute(),
            comment_season = season,
            comment_A = comment_A,
            comment_B = comment_B
        )
        db.session.add(comment)
        db.session.add(user_comment_history)
        db.session.commit()

        return redirect(url_for('match', group = gamegroup))

    return render_template('home.html')


# 개인보기에도 응원댓글을 남길 수 있다. 그것을 처리한다.
# 익명은 똑같이 구현했다.
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
            date_created = timezone_compute(),
            comment_name = name,
            comment_group = group,
            user_email = user_email
        )

        db.session.add(indiv_comment)
        db.session.commit()

        return redirect(url_for('candidate', name = name ))
    else:
        return redirect(url_for('candidate', name = name ))



# 간단하게 게시판을 만들었다.
# 수정은 되지 않는다. 이것도 같이 집어넣어야 멋지게 될 것이다.
@app.route('/bulletin_create', methods = ['GET', 'POST'])
def bulletin_create():
    group = 1
    if request.method == 'POST':
        all_comments = Bulletin.query.order_by(asc(Bulletin.user_index)).all()
        user_comments = Bulletin.query.filter(Bulletin.user_email == g.user_email).all()
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

        my_all_comment = Bulletin(
            user_index = user_idx,
            date_created = timezone_compute(),
            content = request.form['content'],
            user_email = g.user_email
        )
        db.session.add(my_all_comment)
        db.session.commit()

        return redirect(url_for('bulletin'))
    else:
        return redirect(url_for('bulleti'))


# 게시판을 보여주는 함수이다.
@app.route('/bulletin', methods = ['GET', 'POST'])
def bulletin():
    if g.user_email == None:
        flash(u'로그인 후에 이용해주세요', 'danger')
        return redirect(url_for('login'))
    else:
        all_bulletin = Bulletin.query.order_by(desc(Bulletin.date_created)).all()
        return render_template('bulletin.html', bulletin = all_bulletin, active_tab = 'bulletin')


# 모든 댓글을 모아서 보여주는 "댓글 모아보기" 기능이다.
@app.route('/all_comments', methods = ['GET','POST'])
def all_comments():
    if g.user_email == None:
        flash(u'로그인 후에 이용해주세요', 'danger')
        return redirect(url_for('login'))
    else:
        comments = Comment.query.order_by(desc(Comment.date_created)).all()
        indiv_comments = Indiv_Comment.query.order_by(desc(Indiv_Comment.date_created)).all()
        return render_template('all_comment.html', indiv_comments = indiv_comments, comments = comments, active_tab = 'all_comments')


# 위의 all_comment에서 만약 그룹버튼을 누르면 그룹별로 다시 보여준다.
# 그룹이 하나라면 쓰이지 않는다.
@app.route('/all_comments/<int:group>', methods=['GET', 'POST'])
def comments_group(group):
    if g.user_email == None:
        flash(u'로그인 후에 이용해주세요', 'danger')
        return redirect(url_for('login'))
    else:
        comments = Comment.query.order_by(desc(Comment.date_created)).filter(Comment.comment_group == group).all()
        indiv_comments = Indiv_Comment.query.order_by(desc(Indiv_Comment.date_created)).filter(Indiv_Comment.comment_group == group).all()
        return render_template('all_comment.html', comments = comments, indiv_comments = indiv_comments, active_tab = 'all_comments')
