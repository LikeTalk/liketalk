from apps import db

class User(db.Model):
    _id = db.Column(db.String(255), primary_key = True)
    email = db.Column(db.String(255))
    password = db.Column(db.String(255))
    join_date = db.Column(db.DateTime(), default = db.func.now())


class Match(db.Model):
    match_id = db.Column(db.Integer, primary_key = True)
    candidate1_id = db.Column(db.Integer, db.ForeignKey('user1._id'))
    user1 = db.relationship('User', backref=db.backref('match', lazy='dynamic'))
    candidate1_count = db.Column(db.Integer, primary_key = True)
    candidate2_id = db.Column(db.Integer, db.ForeignKey('user2._id'))
    user2 = db.relationship('User', backref=db.backref('match', lazy='dynamic'))
    candidate2_count = db.Column(db.Integer, primary_key = True)

class Candidate(db.Model):
    Cand_id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(255))
    school = db.Column(db.String(255))


class Comment(db.Model):
    Comment_id = db.Column(db.Integer, primary_key = True)
    Comment_pswd = db.Column(db.String(255))
    content = db.Column(db.Text())
    date_created = db.Column(db.DateTime(), default=db.func.now())
    likecount = db.Column(db.Integer, default = 0, nullable = False)