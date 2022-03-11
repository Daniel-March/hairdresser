import asyncpg
from aiohttp.web_exceptions import HTTPNotFound, HTTPConflict, HTTPForbidden

from app.base.base_accessor import BaseAccessor
from app.store.database.gino import db
from app.web.models import Hairdresser, Department, DepartmentXHairdresser, ShiftXHairdresser, Shift
from app.web.utils import encode_password


class HairdresserAccessor(BaseAccessor):
    async def get_all(self) -> list[Hairdresser]:
        hairdressers = await Hairdresser.query.gino.all()
        return hairdressers

    async def check_authorization(self, phone: str, password: str) -> Hairdresser:
        password = encode_password(password)
        hairdresser = await self.get_by_phone(phone, throw_error=False)
        if hairdresser is None or hairdresser.password != password:
            raise HTTPForbidden
        return hairdresser

    async def get_by_id(self, id_: int, throw_error=True) -> Hairdresser | None:
        hairdresser = await Hairdresser.query.where(Hairdresser.id == id_).gino.first()
        if throw_error and hairdresser is None:
            raise HTTPNotFound(text="Hairdresser not found")
        return hairdresser

    async def get_by_phone(self, phone: str, throw_error=True) -> Hairdresser | None:
        hairdresser = await Hairdresser.query.where(Hairdresser.phone == phone).gino.first()
        if throw_error and hairdresser is None:
            raise HTTPNotFound(text="Hairdresser not found")
        return hairdresser

    async def get_by_department(self, department: int | Department) -> list[Hairdresser]:
        if type(department) is not int:
            department = department.id
        relations = await DepartmentXHairdresser.query.where(DepartmentXHairdresser.department == department).gino.all()
        hairdressers = [await self.get_by_id(relation.hairdresser) for relation in relations]
        return hairdressers

    async def get_by_shift(self, shift: int | Shift) -> list[Hairdresser]:
        if type(shift) is not int:
            shift = shift.id
        relations = await ShiftXHairdresser.query.where(ShiftXHairdresser.shift == shift).gino.all()
        hairdressers = [await self.get_by_id(relation.hairdresser) for relation in relations]
        return hairdressers

    async def create(self, name: str, phone: str, password: str) -> Hairdresser:
        password = encode_password(password)
        try:
            hairdresser = await Hairdresser.create(name=name,
                                                   phone=phone,
                                                   password=password)
        except asyncpg.exceptions.UniqueViolationError as e:
            raise HTTPConflict(text=e.detail)
        return hairdresser

    async def change(self, id_: int, new_name: str, new_phone: str, new_password: str) -> Hairdresser:
        hairdresser = await self.get_by_id(id_=id_)
        async with db.transaction() as transaction:
            try:
                if new_name is not None:
                    await hairdresser.update(name=new_name).apply()
                if new_phone is not None:
                    await hairdresser.update(phone=new_phone).apply()
                if new_password is not None:
                    await hairdresser.update(password=encode_password(new_password)).apply()
            except asyncpg.exceptions.UniqueViolationError as e:
                transaction.raise_rollback()
                raise HTTPConflict(text=e.detail)

        return hairdresser

    async def delete(self, id_: int) -> None:
        hairdresser = await self.get_by_id(id_=id_)
        await hairdresser.delete()
