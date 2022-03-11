import asyncpg
from aiohttp.web_exceptions import HTTPConflict, HTTPNotFound

from app.base.base_accessor import BaseAccessor
from app.store.database.gino import db
from app.web.models import Reception, Hairdresser, Customer, Department, Service, ReceptionXService


class ReceptionAccessor(BaseAccessor):
    async def get_by_id(self, id_, throw_error=True) -> Reception | None:
        reception = await Reception.query.where(Reception.id == id_).gino.first()
        if throw_error and reception is None:
            raise HTTPNotFound(text="Reception not found")
        reception.hairdresser = await self.app.store.hairdresser_accessor.get_by_id(reception.hairdresser)
        reception.department = await self.app.store.department_accessor.get_by_id(reception.department)
        reception.customer = await self.app.store.customer_accessor.get_by_id(reception.customer)
        reception.services = await self.app.store.service_accessor.get_by_reception(reception)
        return reception

    async def get_by_date(self, day: int, month: int, year: int) -> list[Reception]:
        receptions = await Reception.query.where(Reception.day == day and
                                                 Reception.month == month and
                                                 Reception.year == year).gino.all()
        for reception in receptions:
            reception.hairdresser = await self.app.store.hairdresser_accessor.get_by_id(reception.hairdresser)
            reception.department = await self.app.store.department_accessor.get_by_id(reception.department)
            reception.customer = await self.app.store.customer_accessor.get_by_id(reception.customer)
            reception.services = await self.app.store.service_accessor.get_by_reception(reception)
        return receptions

    async def get_by_customer(self, customer: Customer | int) -> list[Reception]:
        if type(customer) is not int:
            customer = customer.id
        receptions = await Reception.query.where(Reception.customer == customer).gino.all()
        for reception in receptions:
            reception.hairdresser = await self.app.store.hairdresser_accessor.get_by_id(reception.hairdresser)
            reception.department = await self.app.store.department_accessor.get_by_id(reception.department)
            reception.customer = await self.app.store.customer_accessor.get_by_id(reception.customer)
            reception.services = await self.app.store.service_accessor.get_by_reception(reception)
        return receptions

    async def get_by_hairdresser(self, hairdresser: Hairdresser | int) -> list[Reception]:
        if type(hairdresser) is not int:
            hairdresser = hairdresser.id
        receptions = await Reception.query.where(Reception.hairdresser == hairdresser).gino.all()
        for reception in receptions:
            reception.hairdresser = await self.app.store.hairdresser_accessor.get_by_id(reception.hairdresser)
            reception.department = await self.app.store.department_accessor.get_by_id(reception.department)
            reception.customer = await self.app.store.customer_accessor.get_by_id(reception.customer)
            reception.services = await self.app.store.service_accessor.get_by_reception(reception)
        return receptions

    async def get_by_department(self, department: Department | int) -> list[Reception]:
        if type(department) is not int:
            department = department.id
        receptions = await Reception.query.where(Reception.department == department).gino.all()
        for reception in receptions:
            reception.hairdresser = await self.app.store.hairdresser_accessor.get_by_id(reception.hairdresser)
            reception.department = await self.app.store.department_accessor.get_by_id(reception.department)
            reception.customer = await self.app.store.customer_accessor.get_by_id(reception.customer)
            reception.services = await self.app.store.service_accessor.get_by_reception(reception)
        return receptions

    async def create(self, department: Department | int, services: list[Service] | list[int],
                     hairdresser: Hairdresser | int, customer: Customer | int, year: int, month: int,
                     day: int, day_time: int) -> Reception:
        if type(department) is not int:
            department = department.id
        if len(services) > 0 and type(services[0]) is not int:
            services = [service.id for service in services]
        if type(hairdresser) is not int:
            hairdresser = hairdresser.id
        if type(customer) is not int:
            customer = customer.id
        error = None
        async with db.transaction() as transaction:
            try:
                reception = await Reception.create(department=department,
                                                   hairdresser=hairdresser,
                                                   customer=customer,
                                                   year=year,
                                                   month=month,
                                                   day=day,
                                                   day_time=day_time)

                for service in services:
                    if type(service) is not int:
                        service = service.id
                    await ReceptionXService.create(reception=reception.id, service=service)

            except asyncpg.exceptions.UniqueViolationError as e:
                error = HTTPConflict(text=e.detail)
                transaction.raise_rollback()
            except Exception as e:
                error = e
                transaction.raise_rollback()
        if error is not None:
            raise error
        reception.department = await self.app.store.department_accessor.get_by_id(department)
        reception.hairdresser = await self.app.store.hairdresser_accessor.get_by_id(hairdresser)
        reception.customer = await self.app.store.customer_accessor.get_by_id(customer)
        reception.services = [await self.app.store.service_accessor.get_by_id(service) for service in services]
        return reception

    async def delete(self, id_) -> None:
        reception = await self.get_by_id(id_=id_)
        await reception.delete()
