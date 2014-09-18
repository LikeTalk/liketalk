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


class Comment(db.Model):
    Comment_id = db.Column(db.Integer, primary_key = True)
    content = db.Column(db.Text())
    date_created = db.Column(db.DateTime(), default=db.func.now())
    likecount = db.Column(db.Integer, default = 0, nullable = False)


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


