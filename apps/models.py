from apps import db

class User(db.Model):
    email = db.Column(db.String(255), primary_key = True)
    password = db.Column(db.String(255))
    join_date = db.Column(db.DateTime(), default = db.func.now())


class Match(db.Model):
    match_id = db.Column(db.Integer, primary_key = True)
    candidate_A_namename = db.Column(db.String(255))
    candidate_A_count = db.Column(db.Integer, default = 0, nullable = False)
    candidate_B_namename = db.Column(db.String(255))
    candidate_B_count = db.Column(db.Integer, default = 0, nullable = False)


class Candidate(db.Model):
    name = db.Column(db.String(255), primary_key = True)
    school = db.Column(db.String(255))


class Comment(db.Model):
    Comment_id = db.Column(db.Integer, primary_key = True)
    Comment_pswd = db.Column(db.String(255))
    content = db.Column(db.Text())
    date_created = db.Column(db.DateTime(), default=db.func.now())
    likecount = db.Column(db.Integer, default = 0, nullable = False)