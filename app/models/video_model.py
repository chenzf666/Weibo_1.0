from app import db


class Video(db.Model):
    __tablename__ = 'videos'
    id = db.Column(db.Integer, primary_key=True)
    video_url = db.Column(db.String(2083))
    post_id = db.Column(db.Integer, db.ForeignKey('posts.id'))
