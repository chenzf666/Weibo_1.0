
# from app.models import engine

import db
import typing
from ..models.user_model import User
# from .base_repository import SQLAlchemyRepository
class UserRepository():
    def __init__(self):
        pass

    def getAllUser(self)->typing.List[User]:
        list=db.UserSQL.all()
        return list
    def getUser(self,id)->User:
        user=db.UserSQL.get(pk=id)
        return user
    def getPassword(self,id)->User.password:
        password=self.getUser(id=id).password
        return password

    def getEmail(self,id)->User.email:
        email=self.getUser(id=id).email
        return email

    def getRoleID(self,id)->User.role_id:
        roleID=self.getUser(id=id).role_id
        return roleID
