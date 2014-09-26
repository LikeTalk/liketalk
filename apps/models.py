from apps import db

class User(db.Model):
    email = db.Column(db.String(255), primary_key = True)
    password = db.Column(db.String(255))
    join_date = db.Column(db.DateTime(), default = db.func.now())


class Match(db.Model):
    match_id = db.Column(db.Integer, primary_key = True)
    season_num = db.Column(db.Integer)
    game_round = db.Column(db.Integer)
    group = db.Column(db.Integer)

    candidate_A_namename = db.Column(db.String(255))
    candidate_A_school = db.Column(db.String(255))
    candidate_A_photolink = db.Column(db.String(255))
    candidate_A_count = db.Column(db.Integer, default = 0, nullable = False)

    candidate_B_namename = db.Column(db.String(255))
    candidate_B_school = db.Column(db.String(255))
    candidate_B_photolink = db.Column(db.String(255))
    candidate_B_count = db.Column(db.Integer, default = 0, nullable = False)


class Candidate(db.Model):
    candidate_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    school = db.Column(db.String(255))
    photolink = db.Column(db.String(255))



class GameHistory(db.Model):
    GameHistory_id = db.Column(db.Integer, primary_key = True)
    user = db.relationship('User')
    user_email = db.Column(db.String(255), db.ForeignKey('user.email'))
    done_game = db.Column(db.Integer, default = 0, nullable = False)
    done_game_group = db.Column(db.Integer)
    done_game_season = db.Column(db.Integer)
    done_game_result = db.Column(db.Integer)


class Winner(db.Model):
    User_Indiv_Game_id = db.Column(db.Integer, primary_key = True)
    user = db.relationship('User')
    user_email = db.Column(db.String(255), db.ForeignKey('user.email'))
    game_season = db.Column(db.Integer)
    game_group = db.Column(db.Integer)
    game_round = db.Column(db.Integer)
    winner_A_namename = db.Column(db.String(255))
    winner_A_school = db.Column(db.String(255))
    winner_A_photolink = db.Column(db.String(255))


class Comment(db.Model):
    Comment_id = db.Column(db.Integer, primary_key = True)
    user_index = db.Column(db.Integer)
    content = db.Column(db.Text())
    date_created = db.Column(db.DateTime(), default=db.func.now())
    likecount = db.Column(db.Integer, default = 0, nullable = False)
    comment_group = db.Column(db.Integer)
    comment_season = db.Column(db.Integer)
    comment_gameround = db.Column(db.Integer)
    comment_A = db.Column(db.String(255))
    comment_B = db.Column(db.String(255))


class Indiv_Comment(db.Model):
    Comment_id = db.Column(db.Integer, primary_key = True)
    user_index = db.Column(db.Integer)
    content = db.Column(db.Text())
    date_created = db.Column(db.DateTime(), default=db.func.now())
    comment_name = db.Column(db.String(255))
    comment_group = db.Column(db.Integer)
    user_index = db.Column(db.Integer)
    user_email = db.Column(db.String(255))



class UserCommentHistory(db.Model):
    UCH_id=db.Column(db.Integer, primary_key = True)
    user = db.relationship('User')
    user_email = db.Column(db.String(255), db.ForeignKey('user.email'))
    commented_match = db.Column(db.Integer, default=0, nullable = False)
    commented_group = db.Column(db.Integer)
    commented_season = db.Column(db.Integer)
    user_index = db.Column(db.Integer)


class Bulletin(db.Model):
    Comment_id = db.Column(db.Integer, primary_key = True)
    user = db.relationship('User')
    user_email = db.Column(db.String(255), db.ForeignKey('user.email'))
    user_index = db.Column(db.Integer)
    content = db.Column(db.Text())
    date_created = db.Column(db.DateTime(), default=db.func.now())
