import asyncpg
from aiohttp.web_exceptions import HTTPNotFound, HTTPConflict

from app.base.base_accessor import BaseAccessor
from app.store.database.gino import db
from app.web.models import Department, Hairdresser, Administrator, Service, DepartmentXAdministrator, \
    DepartmentXHairdresser, DepartmentXService


class DepartmentAccessor(BaseAccessor):
    async def get_all(self) -> list[Department]:
        departments = await Department.query.gino.all()
        for department in departments:
            department.hairdressers = await self.app.store.hairdresser_accessor.get_by_department(department)
            department.administrators = await self.app.store.administrator_accessor.get_by_department(department)
            department.services = await self.app.store.service_accessor.get_by_department(department)
        return departments

    async def get_by_id(self, id_: int, throw_error=True) -> Department | None:
        department = await Department.query.where(Department.id == id_).gino.first()
        if throw_error and department is None:
            raise HTTPNotFound(text="Department not found")
        department.hairdressers = await self.app.store.hairdresser_accessor.get_by_department(department)
        department.administrators = await self.app.store.administrator_accessor.get_by_department(department)
        department.services = await self.app.store.service_accessor.get_by_department(department)
        return department

    async def get_by_name(self, name: int, throw_error=True) -> Department | None:
        department = await Department.query.where(Department.name == name).gino.first()
        if throw_error and department is None:
            raise HTTPNotFound(text="Department not found")
        department.hairdressers = await self.app.store.hairdresser_accessor.get_by_department(department)
        department.administrators = await self.app.store.administrator_accessor.get_by_department(department)
        department.services = await self.app.store.service_accessor.get_by_department(department)
        return department

    async def get_by_address(self, address: str, throw_error=True) -> Department | None:
        department = await Department.query.where(Department.address == address).gino.first()
        if throw_error and department is None:
            raise HTTPNotFound(text="Department not found")
        department.hairdressers = await self.app.store.hairdresser_accessor.get_by_department(department)
        department.administrators = await self.app.store.administrator_accessor.get_by_department(department)
        department.services = await self.app.store.service_accessor.get_by_department(department)
        return department

    async def get_by_administrator(self, administrator: Administrator | int) -> list[Department]:
        if type(administrator) is not int:
            id_ = administrator.id
        else:
            id_ = administrator
        relations = await DepartmentXAdministrator.query.where(DepartmentXAdministrator.administrator == id_).gino.all()
        department = [await Department.query.where(Department.id == d_a.department).gino.first() for d_a in relations]
        return department

    async def get_by_hairdresser(self, hairdresser: Hairdresser | int) -> list[Department]:
        if type(hairdresser) is not int:
            id_ = hairdresser.id
        else:
            id_ = hairdresser
        relations = await DepartmentXHairdresser.query.where(DepartmentXHairdresser.hairdresser == id_).gino.all()
        department = [await Department.query.where(Department.id == d_a.department).gino.first() for d_a in relations]
        return department

    async def get_by_service(self, service: Service | int) -> list[Department]:
        if type(service) is not int:
            id_ = service.id
        else:
            id_ = service
        relations = await DepartmentXService.query.where(DepartmentXService.service == id_).gino.all()
        department = [await Department.query.where(Department.id == d_a.department).gino.first() for d_a in relations]
        return department

    async def create(self, name: str, address: str, administrators: list[Administrator] | list[int],
                     hairdressers: list[Hairdresser] | list[int], services: list[Service] | list[int]) -> Department:
        error = None
        async with db.transaction() as transaction:
            try:
                department = await Department.create(name=name, address=address)

                for administrator in administrators:
                    if type(administrator) is not int:
                        administrator = administrator.id
                    await DepartmentXAdministrator.create(department=department.id, administrator=administrator)

                for hairdresser in hairdressers:
                    if type(hairdresser) is not int:
                        hairdresser = hairdresser.id
                    await DepartmentXHairdresser.create(department=department.id, hairdresser=hairdresser)

                for service in services:
                    if type(service) is not int:
                        service = service.id
                    await DepartmentXService.create(department=department.id, service=service)

            except asyncpg.exceptions.UniqueViolationError as e:
                error = HTTPConflict(text=e.detail)
                transaction.raise_rollback()
            except Exception as e:
                error = e
                transaction.raise_rollback()
        if error is not None:
            raise error
        return department

    async def _change_administrators(self, id_: int, new_administrators: list[Administrator] | list[int]) -> Department:
        department = await self.get_by_id(id_=id_)

        if len(new_administrators) > 0 and type(new_administrators[0]) is not int:
            ids = [administrator.id for administrator in new_administrators]
        else:
            ids = new_administrators
        await DepartmentXAdministrator.delete.where(DepartmentXAdministrator.department == id_ and
                                                    DepartmentXAdministrator.administrator not in ids).gino.status()
        relations = await DepartmentXAdministrator.query.where(DepartmentXAdministrator.department == id_).gino.all()
        relation_ids = [relation.administrator for relation in relations]
        for administrator_id in new_administrators:
            if administrator_id not in relation_ids:
                await DepartmentXAdministrator.create(department=id_,
                                                      administrator=administrator_id)
        return department

    async def _change_hairdressers(self, id_: int, new_hairdressers: list[Hairdresser] | list[int]) -> Department:
        department = await self.get_by_id(id_=id_)

        if len(new_hairdressers) > 0 and type(new_hairdressers[0]) is not int:
            ids = [hairdresser.id for hairdresser in new_hairdressers]
        else:
            ids = new_hairdressers
        await DepartmentXHairdresser.delete.where(DepartmentXHairdresser.department == id_ and
                                                  DepartmentXHairdresser.hairdresser not in ids).gino.status()
        relations = await DepartmentXHairdresser.query.where(DepartmentXHairdresser.department == id_).gino.all()
        relation_ids = [relation.hairdresser for relation in relations]
        for hairdresser_id in new_hairdressers:
            if hairdresser_id not in relation_ids:
                await DepartmentXHairdresser.create(department=id_,
                                                    hairdresser=hairdresser_id)
        return department

    async def _change_services(self, id_: int, new_services: list[Hairdresser] | list[int]) -> Department:
        department = await self.get_by_id(id_=id_)

        if len(new_services) > 0 and type(new_services[0]) is not int:
            ids = [service.id for service in new_services]
        else:
            ids = new_services
        await DepartmentXService.delete.where(DepartmentXService.department == id_ and
                                              DepartmentXService.service not in ids).gino.status()
        relations = await DepartmentXService.query.where(DepartmentXService.department == id_).gino.all()
        relation_ids = [relation.service for relation in relations]
        for service_id in new_services:
            if service_id not in relation_ids:
                await DepartmentXService.create(department=id_,
                                                service=service_id)
        return department

    async def change(self, id_: int, new_name: str, new_address: int,
                     new_administrators: list[Administrator] | list[int],
                     new_hairdressers: list[Hairdresser] | list[int],
                     new_services: list[Hairdresser] | list[int]) -> Department:
        error = None
        department = await self.get_by_id(id_=id_)
        async with db.transaction() as transaction:
            try:
                await department.update(name=new_name).apply()
                await department.update(address=new_address).apply()
                await self._change_administrators(id_=id_, new_administrators=new_administrators)
                await self._change_hairdressers(id_=id_, new_hairdressers=new_hairdressers)
                await self._change_services(id_=id_, new_services=new_services)
            except asyncpg.exceptions.UniqueViolationError as e:
                error = HTTPConflict(text=e.detail)
                transaction.raise_rollback()
            except Exception as e:
                error = e
                transaction.raise_rollback()
        if error is not None:
            raise error
        return await self.get_by_id(id_=id_)

    async def delete(self, id_: int) -> None:
        department = await self.get_by_id(id_=id_)
        await department.delete()
