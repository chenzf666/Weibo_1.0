import db
import typing
from ..models.role_model import Role
from .base_repository import SQLAlchemyRepository
class RoleRepository:
    def __init__(self):
        pass

    def getAllRole(self) -> typing.List[Role]:
        list = db.RoleSQL.all()
        return list

    def getRole(self, id) -> Role:
        user = db.RoleSQL.get(pk=id)
        return user

    def getName(self,id)->Role.name:
        return self.getRole(id=id).name

    def getID(self,id)->Role.id:
        return self.getRole(id=id).id

    def getPermission(self,id)->Role.permission:
        return self.getRole(id=id).permissiond
