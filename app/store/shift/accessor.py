import asyncpg
from aiohttp.web_exceptions import HTTPNotFound, HTTPConflict, HTTPBadRequest

from app.base.base_accessor import BaseAccessor
from app.store.database.gino import db
from app.web.models import Shift, Hairdresser, ShiftXHairdresser, Department


class ShiftAccessor(BaseAccessor):
    async def get_all(self) -> list[Shift]:
        shifts = await Shift.query.gino.all()
        for shift in shifts:
            shift.hairdressers = await self.app.store.hairdresser_accessor.get_by_shift(shift)
        return shifts

    async def get_by_id(self, id_: int, throw_error=True) -> Shift | None:
        shift = await Shift.query.where(Shift.id == id_).gino.first()
        if throw_error and shift is None:
            raise HTTPNotFound(text="Shift not found")
        shift.hairdressers = await self.app.store.hairdresser_accessor.get_by_shift(shift)
        return shift

    async def get_by_start_day_time(self, start_day_time: int) -> list[Shift]:
        shifts = await Shift.query.where(Shift.start_day_time == start_day_time).gino.all()
        for shift in shifts:
            shift.hairdressers = await self.app.store.hairdresser_accessor.get_by_shift(shift)
        return shifts

    async def get_by_end_day_time(self, end_day_time: int) -> list[Shift]:
        shifts = await Shift.query.where(Shift.end_day_time == end_day_time).gino.all()
        for shift in shifts:
            shift.hairdressers = await self.app.store.hairdresser_accessor.get_by_shift(shift)
        return shifts

    async def get_by_day(self, day: int) -> list[Shift]:
        shifts = await Shift.query.where(Shift.day == day).all()
        for shift in shifts:
            shift.hairdressers = await self.app.store.hairdresser_accessor.get_by_shift(shift)
        return shifts

    async def get_by_hairdresser(self, hairdresser: Hairdresser | int) -> list[Shift]:
        if type(hairdresser) is not int:
            hairdresser = hairdresser.id
        relations = await ShiftXHairdresser.query.where(ShiftXHairdresser.hairdresser == hairdresser).gino.all()
        shifts = [await Shift.query.where(Shift.id == relation.shift).gino.first() for relation in relations]
        for shift in shifts:
            shift.hairdressers = await self.app.store.hairdresser_accessor.get_by_shift(shift)
        return shifts

    async def get_by_department(self, department: Department | int) -> list[Shift]:
        if type(department) is not int:
            department = department.id
        shifts = await Shift.query.where(Shift.department == department).gino.all()
        for shift in shifts:
            shift.hairdressers = await self.app.store.hairdresser_accessor.get_by_shift(shift)
        return shifts

    async def create(self, start_day_time: int, end_day_time: int, day: int,
                     hairdressers: list[Hairdresser] | list[int], department: Department | int) -> Shift:
        if type(department) is not int:
            department = department.id

        if len(hairdressers) > 0 and type(hairdressers[0]) is not int:
            hairdressers = [hairdresser.id for hairdresser in hairdressers]
        if start_day_time == end_day_time:
            raise HTTPBadRequest
        for hairdresser in hairdressers:
            for shift in await self.get_by_hairdresser(hairdresser):
                if set(range(start_day_time, end_day_time)) & set(range(shift.start_day_time, shift.end_day_time)):
                    raise HTTPConflict(text=f"Hairdresser({hairdresser}) already has a shift at this time")
        error = None
        async with db.transaction() as transaction:
            try:
                shift = await Shift.create(start_day_time=start_day_time,
                                           end_day_time=end_day_time,
                                           day=day,
                                           department=department)
                for hairdresser in hairdressers:
                    await ShiftXHairdresser.create(hairdresser=hairdresser, shift=shift.id)
            except asyncpg.exceptions.UniqueViolationError as e:
                error = HTTPConflict(text=e.detail)
                transaction.raise_rollback()
            except Exception as e:
                error = e
                transaction.raise_rollback()
        if error is not None:
            raise error
        return await self.get_by_id(shift.id)

    async def _change_hairdressers(self, id_: int, new_hairdressers: list[Hairdresser] | list[int]) -> Shift:
        shift = await self.get_by_id(id_=id_)

        if len(new_hairdressers) > 0 and type(new_hairdressers[0]) is not int:
            new_hairdressers = [hairdresser.id for hairdresser in new_hairdressers]
        await ShiftXHairdresser.delete.where(ShiftXHairdresser.shift == id_ and
                                             ShiftXHairdresser.hairdresser not in new_hairdressers).gino.status()
        relations = await ShiftXHairdresser.query.where(ShiftXHairdresser.shift == id_).gino.all()
        relation_ids = [relation.hairdresser for relation in relations]
        for hairdresser_id in new_hairdressers:
            if hairdresser_id not in relation_ids:
                await ShiftXHairdresser.create(shift=id_,
                                               hairdresser=hairdresser_id)
        return shift

    async def change(self, id_: int, new_start_day_time: int, new_end_day_time: int, new_day: int,
                     new_hairdressers: list[Hairdresser] | list[int]) -> None:
        shift = await self.get_by_id(id_=id_)
        error = None
        async with db.transaction() as transaction:
            try:
                await shift.update(start_day_time=new_start_day_time).apply()
                await shift.update(end_day_time=new_end_day_time).apply()
                await shift.update(day=new_day).apply()
                await self._change_hairdressers(id_=id_, new_hairdressers=new_hairdressers)
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
        shift = await self.get_by_id(id_=id_)
        await shift.delete()
