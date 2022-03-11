from aiohttp.web_exceptions import HTTPForbidden
from aiohttp_apispec import request_schema, querystring_schema

from app.hairdresser.schemes import (HairdresserAuthorizationSchema, HairdresserDeleteReceptionSchema,
                                     HairdresserGetReceptionSchema, HairdresserGetDepartmentSchema,
                                     HairdresserGetShiftSchema, HairdresserGetAdministratorSchema,
                                     HairdresserGetCustomerSchema, HairdresserGetServiceSchema, )
from app.web.app import View
from app.web.models import Hairdresser
from app.web.schemes import ReceptionSchema, ShiftSchema, DepartmentSchema, UserSchema, ServiceSchema
from app.web.utils import check_session, json_response


class HairdresserView(View):
    @check_session(user_type=Hairdresser)
    async def get(self):
        hairdresser = self.user

        return json_response(UserSchema().dump(hairdresser))


class HairdresserAuthorizationView(View):
    @request_schema(HairdresserAuthorizationSchema)
    async def post(self):
        if self.request.cookies.get("session", None) is not None:
            await self.request.app.store.session_accessor.delete(self.request.cookies.get("session"), throw_error=False)

        hairdresser = await self.request.app.store.hairdresser_accessor.check_authorization(**self.data)
        session = await self.request.app.store.session_accessor.create(user_id=hairdresser.id, user_type=Hairdresser)

        return json_response(cookies={"session": session.key})


class HairdresserReceptionView(View):
    @querystring_schema(HairdresserGetReceptionSchema)
    @check_session(user_type=Hairdresser)
    async def get(self):
        reception_id = self.request.query.get("id")
        if reception_id is None:
            receptions = await self.request.app.store.reception_accessor.get_by_hairdresser(self.user.id)
            return json_response({"receptions": ReceptionSchema().dump(receptions, many=True)})
        reception_id = int(reception_id)
        reception = await self.request.app.store.reception_accessor.get_by_id(reception_id)
        if reception.hairdresser.id != self.user.id:
            raise HTTPForbidden
        return json_response({"reception": ReceptionSchema().dump(reception)})

    @request_schema(HairdresserDeleteReceptionSchema)
    @check_session(user_type=Hairdresser)
    async def delete(self):
        reception = await self.request.app.store.reception_accessor.get_by_id(**self.data)
        if reception.hairdresser.id != self.user.id:
            raise HTTPForbidden(text="Forbidden to delete another's reception")
        await self.request.app.store.reception_accessor.delete(reception.id)
        return json_response()


class HairdresserShiftView(View):
    @check_session(user_type=Hairdresser)
    @querystring_schema(HairdresserGetShiftSchema)
    async def get(self):
        shift_id = self.request.query.get("id")

        if shift_id is None:
            shifts = await self.request.app.store.shift_accessor.get_by_hairdresser(self.user.id)
            return json_response({"shifts": ShiftSchema().dump(shifts, many=True)})

        shift_id = int(shift_id)
        shift = await self.request.app.store.shift_accessor.get_by_id(shift_id)
        return json_response({"shift": ShiftSchema().dump(shift)})


class HairdresserDepartmentView(View):
    @check_session(user_type=Hairdresser)
    @querystring_schema(HairdresserGetDepartmentSchema)
    async def get(self):
        department_id = self.request.query.get("id")

        if department_id is None:
            departments = await self.request.app.store.organization_accessor.get_departments()
            return json_response({"departments": DepartmentSchema().dump(departments, many=True)})

        department_id = int(department_id)
        department = await self.request.app.store.department_accessor.get_by_id(department_id)
        shifts = await self.request.app.store.shift_accessor.get_by_department(department)
        return json_response({"department": DepartmentSchema().dump(department),
                              "shifts": ShiftSchema().dump(shifts, many=True)})


class HairdresserCustomerView(View):
    @check_session(user_type=Hairdresser)
    @querystring_schema(HairdresserGetCustomerSchema)
    async def get(self):
        customer = await self.request.app.store.administrator_accessor.get_by_id(**self.data)
        return json_response({"customer": UserSchema().dump(customer)})


class HairdresserAdministratorView(View):
    @check_session(user_type=Hairdresser)
    @querystring_schema(HairdresserGetAdministratorSchema)
    async def get(self):
        administrator_id = self.request.query.get("id")

        if administrator_id is None:
            administrators = await self.request.app.store.organization_accessor.get_administrators()
            return json_response({"administrators": UserSchema().dump(administrators, many=True)})

        administrator_id = int(administrator_id)
        administrator = await self.request.app.store.administrator_accessor.get_by_id(administrator_id)
        return json_response({"administrator": UserSchema().dump(administrator)})


class HairdresserServiceView(View):
    @check_session(user_type=Hairdresser)
    @querystring_schema(HairdresserGetServiceSchema)
    async def get(self):
        service_id = self.request.query.get("id")
        if service_id is None:
            services = await self.request.app.store.organization_accessor.get_services()
            return json_response({"services": ServiceSchema().dump(services, many=True)})
        service_id = int(service_id)
        service = await self.request.app.store.service_accessor.get_by_id(service_id)
        return json_response({"service": ServiceSchema().dump(service)})
