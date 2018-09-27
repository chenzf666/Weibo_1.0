from flask_login import AnonymousUserMixin

from app import login_manager


class AnonymousUser(AnonymousUserMixin):
    def is_administrator(self):
        return False

    def can(self, permissions):
        return False


login_manager.anonymous_user = AnonymousUser
