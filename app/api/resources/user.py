# -*- coding: utf-8 -*-
from flask import jsonify
from flask_restful import Resource, reqparse
from validate_email import validate_email
from werkzeug.security import generate_password_hash

from app.models.user_model import User

post_parser = reqparse.RequestParser()
post_parser.add_argument('username', required=True, help='Please give me a username!')
post_parser.add_argument('password', required=True, help='Please give me a password!')
post_parser.add_argument('email', required=validate_email, help='Please give me a valid email!')


class UserApi(Resource):
    def post(self):
        args = post_parser.parse_args()
        user = User(username=args.username, email=args.email, password_hash=generate_password_hash(args.password))
        from app import db
        db.session.add(user)
        db.session.commit()
        return jsonify(user.to_json())

    def get(self, id=None):
        if id:
            user = User.query.get_or_404(id)
            return jsonify(user.to_json())
        else:
            users = User.query.all()
            return jsonify({'users': [user.to_json() for user in users]})

    def put(self):
        # ...
        pass

    def delete(self, id):
        user = User.query.get_or_404(id)
        from app import db
        db.session.delete(user)
        db.session.commit()
        return jsonify(user.to_json())
