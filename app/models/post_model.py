import random
from datetime import datetime

import bleach
from markdown import markdown

from app import db


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.Text)
    # likes = db.Column(db.Integer)
    body_html = db.Column(db.Text)
    timestamp = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    author_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    images = db.relationship('Image', backref='post', lazy='dynamic')
    videos = db.relationship('Video', backref='post', lazy='dynamic')
    comments = db.relationship('Comment', backref='post', lazy='dynamic')

    def to_json(self):
        json = {
            'id': self.id,
            'body': self.body,
            'timestamp': self.timestamp,
            'author_id': self.author_id,
            'comments_count': self.comments.count()
            # 'comments': self.comments
        }
        return {'post': json}

    @staticmethod
    def on_changed_body(target, value, oldvalue, initiator):
        allowed_tags = ['a', 'abbr', 'acronym', 'b', 'blockquote', 'code', 'em', 'i', 'li', 'ol', 'pre', 'strong', 'ul',
                        'h1', 'h2', 'h3', 'p']
        target.body_html = bleach.linkify(
            bleach.clean(markdown(value, output_format='html'), tags=allowed_tags, strip=True))

    @staticmethod
    def generate_fake(count=100):
        from random import randint
        from .user_model import User
        import forgery_py

        user_count = len(User.query.all())
        for i in range(count):
            id = random.randint(0, user_count - 1)
            u = User.query.filter_by(id=id).first()
            p = Post(body=forgery_py.lorem_ipsum.sentences(randint(1, 3)), timestamp=forgery_py.date.date(True),
                     author=u)
            db.session.add(p)
            db.session.commit()


db.event.listen(Post.body, 'set', Post.on_changed_body)
