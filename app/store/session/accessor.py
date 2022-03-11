import datetime
import uuid
from aiohttp.web_exceptions import HTTPNotFound

from app.base.base_accessor import BaseAccessor
from app.web.models import Session, Customer, Administrator, Hairdresser, Organization


class SessionAccessor(BaseAccessor):
    async def get_all(self) -> list[Session]:
        sessions = await Session.query.gino.all()
        return sessions

    async def get_by_user_id(self, user_id: int) -> list[Session]:
        sessions = await Session.query.where(Session.user_id == user_id).gino.all()
        return sessions

    async def get_by_key(self, key: str, throw_error=True) -> Session | None:
        session = await Session.query.where(Session.key == key).gino.first()
        if throw_error and session is None:
            raise HTTPNotFound(text="Session not found")
        return session

    async def get_by_id(self, id_: int, throw_error=True) -> Session | None:
        session = await Session.query.where(Session.id == id_).gino.first()
        if throw_error and session is None:
            raise HTTPNotFound(text="Session not found")
        return session

    async def __new_key(self) -> str:
        key = str(uuid.uuid4())
        while await self.get_by_key(key, throw_error=False) is not None:
            key = str(uuid.uuid4())
        return key

    async def create(self, user_id: int, user_type: type) -> Session:
        if user_type not in [Customer, Administrator, Hairdresser, Organization]:
            raise ValueError(f"Unknown user type: {user_type}")
        key = await self.__new_key()
        life_time = self.app.config.session.life_time
        session = await Session.create(user_id=user_id,
                                       key=key,
                                       die_time=int(datetime.datetime.utcnow().timestamp() + life_time),
                                       user_type=user_type.__name__)
        return session

    async def update_key(self, old_key: str) -> str:
        new_key = await self.__new_key()
        session = await self.get_by_key(old_key)
        await session.update(key=new_key).apply()
        return new_key

    async def delete(self, key_or_id: str | int, throw_error=True) -> None:
        if type(key_or_id) is int:
            session = await self.get_by_id(key_or_id, throw_error=throw_error)
        else:
            session = await self.get_by_key(key_or_id, throw_error=throw_error)
        if session is not None:
            await session.delete()
