import inject
import typing
from app.models.role_model import Role
from app.repositories.role_repository import RoleRepository


class UserService:
    role_repository = inject.attr(RoleRepository)

    def getRole(self, id) -> Role:
        user = self.role_repository.getRole(id=id)
        return user

    def getAll(self) -> typing.List[Role]:
        list = self.role_repository.getAll()
        return list

    def getID(self, id) -> Role.id:
        id = self.role_repository.getID(id=id)
        return id

    def getName(self, id) -> Role.name:
        name = self.role_repository.getRole(id=id)
        return name

    def getPermission(self, id) -> Role.permission:
        permission = self.role_repository.getPermission(id=id)
        return permission
