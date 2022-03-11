import asyncpg
from aiohttp.web_exceptions import HTTPNotFound, HTTPConflict

from app.base.base_accessor import BaseAccessor
from app.store.database.gino import db
from app.web.models import Service, Department, DepartmentXService, Reception, ReceptionXService


class ServiceAccessor(BaseAccessor):
    async def get_all(self) -> list[Service]:
        services = await Service.query.gino.all()
        return services

    async def get_by_id(self, id_: int, throw_error=True) -> Service | None:
        service = await Service.query.where(Service.id == id_).gino.first()
        if throw_error and service is None:
            raise HTTPNotFound(text="Service not found")
        return service

    async def get_by_name(self, name: str, throw_error=True) -> Service | None:
        service = await Service.query.where(Service.name == name).gino.first()
        if throw_error and service is None:
            raise HTTPNotFound(text="Service not found")
        return service

    async def get_by_price(self, price: int) -> list[Service]:
        return await Service.query.where(Service.price == price).gino.all()

    async def get_by_duration(self, duration: int) -> list[Service]:
        return await Service.query.where(Service.duration == duration).gino.all()

    async def get_by_department(self, department: Department | int) -> list[Service]:
        if type(department) is not int:
            department = department.id
        relations = await DepartmentXService.query.where(DepartmentXService.department == department).gino.all()
        return [await self.get_by_id(relation.service) for relation in relations]

    async def get_by_reception(self, reception: Reception | int) -> list[Service]:
        if type(reception) is not int:
            reception = reception.id
        relations = await ReceptionXService.query.where(ReceptionXService.reception == reception).gino.all()
        return [await self.get_by_id(relation.service) for relation in relations]

    async def create(self, name: str, price: int, duration: int) -> Service:
        try:
            service = await Service.create(name=name,
                                           price=price,
                                           duration=duration)
        except asyncpg.exceptions.UniqueViolationError as e:
            raise HTTPConflict(text=e.detail)
        return service

    async def change(self, id_: int, new_name: str, new_price: int, new_duration: str) -> Service:
        service = await self.get_by_id(id_=id_)
        async with db.transaction() as transaction:
            try:
                if new_name is not None:
                    await service.update(name=new_name).apply()
                if new_price is not None:
                    await service.update(price=new_price).apply()
                if new_duration is not None:
                    await service.update(duration=new_duration).apply()
            except asyncpg.exceptions.UniqueViolationError as e:
                transaction.raise_rollback()
                raise HTTPConflict(text=e.detail)

        return service

    async def delete(self, id_: int) -> None:
        service = await self.get_by_id(id_=id_)
        await service.delete()
