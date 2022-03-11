import asyncpg
from aiohttp.web_exceptions import HTTPNotFound, HTTPConflict, HTTPForbidden

from app.base.base_accessor import BaseAccessor
from app.store.database.gino import db
from app.web.models import Administrator, Department, DepartmentXAdministrator
from app.web.utils import encode_password


class AdministratorAccessor(BaseAccessor):
    async def check_authorization(self, phone: str, password: str) -> Administrator:
        password = encode_password(password)
        administrator = await self.get_by_phone(phone, throw_error=False)
        if administrator is None or administrator.password != password:
            raise HTTPForbidden
        return administrator

    async def get_by_id(self, id_: int, throw_error=True) -> Administrator | None:
        administrator = await Administrator.query.where(Administrator.id == id_).gino.first()
        if throw_error and administrator is None:
            raise HTTPNotFound(text="Administrator not found")
        return administrator

    async def get_by_phone(self, phone: str, throw_error=True) -> Administrator | None:
        administrator = await Administrator.query.where(Administrator.phone == phone).gino.first()
        if throw_error and administrator is None:
            raise HTTPNotFound(text="Administrator not found")
        return administrator

    async def get_by_department(self, department: int | Department) -> list[Administrator]:
        if type(department) is not int:
            department = department.id
        relations = await DepartmentXAdministrator.query.where(DepartmentXAdministrator.department == department).gino.all()
        administrators = [await self.get_by_id(relation.administrator) for relation in relations]
        return administrators

    async def create(self, name: str, phone: str, password: str) -> Administrator:
        password = encode_password(password)
        try:
            administrator = await Administrator.create(name=name,
                                                       phone=phone,
                                                       password=password)
        except asyncpg.exceptions.UniqueViolationError as e:
            raise HTTPConflict(text=e.detail)
        return administrator

    async def change(self, id_: int, new_name: str, new_phone: str, new_password: str) -> Administrator:
        administrator = await self.get_by_id(id_=id_)
        async with db.transaction() as transaction:
            try:
                if new_name is not None:
                    await administrator.update(name=new_name).apply()
                if new_phone is not None:
                    await administrator.update(phone=new_phone).apply()
                if new_password is not None:
                    await administrator.update(password=encode_password(new_password)).apply()
            except asyncpg.exceptions.UniqueViolationError as e:
                transaction.raise_rollback()
                raise HTTPConflict(text=e.detail)
        return administrator

    async def delete(self, id_: int) -> None:
        administrator = await self.get_by_id(id_=id_)
        await administrator.delete()
