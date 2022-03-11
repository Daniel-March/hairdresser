from aiohttp.web_exceptions import HTTPForbidden

from app.base.base_accessor import BaseAccessor
from app.web.models import Hairdresser, Administrator, Department, Organization, Service, Customer, Session, Shift
from app.web.utils import encode_password


class OrganizationAccessor(BaseAccessor):
    async def check_authorization(self, email: str, password: str) -> Organization:
        password = encode_password(password)
        organization = self.app.config.organization
        if organization.password != password or organization.email != email:
            raise HTTPForbidden
        return organization

    async def get_hairdressers(self) -> list[Hairdresser]:
        return await self.app.store.hairdresser_accessor.get_all()

    async def get_sessions(self) -> list[Session]:
        return await self.app.store.session_accessor.get_all()

    async def get_services(self) -> list[Service]:
        return await self.app.store.service_accessor.get_all()

    async def get_administrators(self) -> list[Administrator]:
        return await self.app.store.administrator_accessor.get_all()

    async def get_customers(self) -> list[Customer]:
        return await self.app.store.customer_accessor.get_all()

    async def get_departments(self) -> list[Department]:
        return await self.app.store.department_accessor.get_all()

    async def get_shifts(self) -> list[Shift]:
        return await self.app.store.shift_accessor.get_all()
