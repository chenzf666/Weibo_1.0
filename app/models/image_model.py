from app import db


class Image(db.Model):
    __tablename__ = 'images'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64))
    filename = db.Column(db.String(64))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
