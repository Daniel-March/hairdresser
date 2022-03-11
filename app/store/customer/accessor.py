import asyncpg.exceptions
from aiohttp.web_exceptions import HTTPNotFound, HTTPConflict, HTTPForbidden

from app.base.base_accessor import BaseAccessor
from app.store.database.gino import db
from app.web.models import Customer
from app.web.utils import encode_password


class CustomerAccessor(BaseAccessor):
    async def get_all(self) -> list[Customer]:
        customers = await Customer.query.gino.all()
        return customers

    async def check_authorization(self, email: str, password: str) -> Customer:
        password = encode_password(password)
        customer = await self.get_by_email(email, throw_error=False)
        if customer is None or customer.password != password:
            raise HTTPForbidden
        return customer

    async def get_by_id(self, id_: int, throw_error=True) -> Customer | None:
        customer = await Customer.query.where(Customer.id == id_).gino.first()
        if throw_error and customer is None:
            raise HTTPNotFound(text="Customer not found")
        return customer

    async def get_by_phone(self, phone: str, throw_error=True) -> Customer | None:
        customer = await Customer.query.where(Customer.phone == phone).gino.first()
        if throw_error and customer is None:
            raise HTTPNotFound(text="Customer not found")
        return customer

    async def get_by_email(self, email: str, throw_error=True) -> Customer | None:
        customer = await Customer.query.where(Customer.email == email).gino.first()
        if throw_error and customer is None:
            raise HTTPNotFound(text="Customer not found")
        return customer

    async def create(self, name: str, phone: str, email: str, password: str) -> Customer:
        password = encode_password(password)
        try:
            customer = await Customer.create(name=name,
                                             phone=phone,
                                             email=email,
                                             password=password)
        except asyncpg.exceptions.UniqueViolationError as e:
            raise HTTPConflict(text=e.detail)
        return customer

    async def change_name(self, id_: int, new_name: str) -> Customer:
        customer = await self.get_by_id(id_=id_)
        await customer.update(name=new_name).apply()
        return customer

    async def change_phone(self, id_: int, new_phone: str) -> Customer:
        customer = await self.get_by_id(id_=id_)
        try:
            await customer.update(phone=new_phone).apply()
        except asyncpg.exceptions.UniqueViolationError as e:
            raise HTTPConflict(text=e.detail)
        return customer

    async def change_email(self, id_: int, new_email: str) -> Customer:
        customer = await self.get_by_id(id_=id_)
        try:
            await customer.update(email=new_email).apply()
        except asyncpg.exceptions.UniqueViolationError as e:
            raise HTTPConflict(text=e.detail)
        return customer

    async def change_password(self, id_: int, new_password: str) -> Customer:
        customer = await self.get_by_id(id_=id_)
        await customer.update(password=encode_password(new_password)).apply()
        return customer

    async def change(self, id_: int, new_name: str, new_phone: str, new_email: str, new_password: str) -> Customer:
        customer = await self.get_by_id(id_=id_)
        error = None
        async with db.transaction() as transaction:
            try:
                if new_name is not None:
                    await customer.update(name=new_name).apply()
                if new_phone is not None:
                    await customer.update(phone=new_phone).apply()
                if new_email is not None:
                    await customer.update(email=new_email).apply()
                if new_password is not None:
                    await customer.update(password=encode_password(new_password)).apply()
            except asyncpg.exceptions.UniqueViolationError as e:
                error = HTTPConflict(text=e.detail)
                transaction.raise_rollback()
            except Exception as e:
                error = e
                transaction.raise_rollback()
        if error is not None:
            raise error
        return customer

    async def delete(self, id_: int) -> None:
        customer = await self.get_by_id(id_=id_)
        await customer.delete()
