#!/usr/bin/env python
# -*- coding:utf-8 -*-
import os

from app import create_app, db

app = create_app(os.getenv('FLASK_CONFIG') or 'default')


@app.teardown_appcontext
def cleanup(resp_or_exc):
    db.session.remove()


if __name__ == '__main__':
    with app.app_context():
        from app.models.user_model import User
        from app.models.role_model import Role
        from app.models.post_model import Post

        db.drop_all()
        db.create_all()
        Role.insert_roles()
        User.create_user()
        db.session.add_all([Post(body='#默认自己关注自己支持富文本', author_id=1), Post(body='#第二条微博<i>斜体字</i>', author_id=2)])
        db.session.commit()
        User.generate_fake(30)
        Post.generate_fake(150)
        User.add_self_follows()
        app.run()
