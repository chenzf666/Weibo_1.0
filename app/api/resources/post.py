# -*- coding: utf-8 -*-
from flask import jsonify
from flask_restful import Resource, reqparse

from app.models.post_model import Post

post_parser = reqparse.RequestParser()
post_parser.add_argument('body', required=True, help='Please give me a post!')
post_parser.add_argument('author_id', required=True, type=int, help='Please give me a author_id!')


class PostApi(Resource):
    def post(self):
        args = post_parser.parse_args()
        from app.models.user_model import User
        author = User.query.get_or_404(args.author_id)
        post = Post(body=args.body, author=author)
        from app import db
        db.session.add(post)
        db.session.commit()
        return jsonify(post.to_json())

    def get(self, id=None):
        if id:
            post = Post.query.get_or_404(id)
            return jsonify(post.to_json())
        else:
            posts = Post.query.all()
            return jsonify({'posts': [post.to_json() for post in posts]})

    def put(self):
        # ...
        pass

    def delete(self, id):
        post = Post.query.get_or_404(id)
        from app import db
        db.session.delete(post)
        db.session.commit()
        return post.to_dic()
