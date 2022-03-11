from aiohttp.web_exceptions import HTTPForbidden
from aiohttp_apispec import request_schema, querystring_schema

from app.administrator.schemes import (AdministratorAuthorizationSchema, AdministratorGetCustomerSchema,
                                       AdministratorGetAdministratorSchema, AdministratorGetHairdresserSchema,
                                       AdministratorGetDepartmentSchema, AdministratorGetServiceSchema,
                                       AdministratorPostDepartmentSchema, AdministratorDeleteReceptionSchema,
                                       AdministratorGetReceptionSchema, AdministratorGetShiftSchema,
                                       AdministratorDeleteShiftSchema, AdministratorPostShiftSchema,
                                       AdministratorPutShiftSchema, AdministratorGetSessionSchema,
                                       AdministratorDeleteSessionSchema, )
from app.web.app import View
from app.web.manager import MainManager
from app.web.models import Administrator
from app.web.schemes import ServiceSchema, UserSchema, DepartmentSchema, ScheduleItemSchema, ShiftSchema, \
    ReceptionSchema, SessionSchema
from app.web.utils import check_session, json_response


class AdministratorView(View):
    @check_session(user_type=Administrator)
    async def get(self):
        administrator = self.user

        return json_response(UserSchema().dump(administrator))


class AdministratorAuthorizationView(View):
    @request_schema(AdministratorAuthorizationSchema)
    async def post(self):
        if self.request.cookies.get("session", None) is not None:
            await self.request.app.store.session_accessor.delete(self.request.cookies.get("session"), throw_error=False)
        administrator = await self.request.app.store.administrator_accessor.check_authorization(**self.data)
        session = await self.request.app.store.session_accessor.create(user_id=administrator.id,
                                                                       user_type=Administrator)

        return json_response(cookies={"session": session.key})


class AdministratorCustomerView(View):
    @check_session(user_type=Administrator)
    @querystring_schema(AdministratorGetCustomerSchema)
    async def get(self):
        customer_id = self.request.query.get("id")
        if customer_id is None:
            customers = await self.request.app.store.organization_accessor.get_customers()
            return json_response({"customers": UserSchema().dump(customers, many=True)})
        customer = await self.request.app.store.customer_accessor.get_by_id(int(customer_id))
        return json_response({"customer": UserSchema().dump(customer)})


class AdministratorHairdresserView(View):
    @check_session(user_type=Administrator)
    @querystring_schema(AdministratorGetHairdresserSchema)
    async def get(self):
        hairdresser_id = self.request.query.get("id")
        if hairdresser_id is None:
            hairdressers = await self.request.app.store.organization_accessor.get_hairdressers()
            return json_response({"hairdressers": UserSchema().dump(hairdressers, many=True)})
        hairdresser = await self.request.app.store.hairdresser_accessor.get_by_id(int(hairdresser_id))
        return json_response({"hairdresser": UserSchema().dump(hairdresser)})


class AdministratorDepartmentView(View):
    @check_session(user_type=Administrator)
    @querystring_schema(AdministratorGetDepartmentSchema)
    async def get(self):
        department_id = self.request.query.get("id")
        day = self.request.query.get("day")

        if department_id is None:
            departments = await self.request.app.store.organization_accessor.get_departments()
            return json_response({"departments": DepartmentSchema().dump(departments, many=True)})

        department_id = int(department_id)
        department = await self.request.app.store.department_accessor.get_by_id(department_id)
        shifts = await self.request.app.store.shift_accessor.get_by_department(department)
        schedule = await MainManager.make_schedule(self.request.app, department=department, day=day)
        return json_response({"department": DepartmentSchema().dump(department),
                              "schedule": ScheduleItemSchema().dump(schedule, many=True),
                              "shifts": ShiftSchema().dump(shifts, many=True)})

    @check_session(user_type=Administrator)
    @request_schema(AdministratorPostDepartmentSchema)
    async def post(self):
        administrator_departments = await self.request.app.store.department_accessor.get_by_administrator(self.user.id)
        if self.data.get("id") not in [department.id for department in administrator_departments]:
            raise HTTPForbidden
        department = await self.request.app.store.department_accessor.change(**self.data)
        return json_response({"department": DepartmentSchema().dump(department)})


class AdministratorAdministratorView(View):
    @check_session(user_type=Administrator)
    @querystring_schema(AdministratorGetAdministratorSchema)
    async def get(self):
        administrator_id = self.request.query.get("id")
        if administrator_id is None:
            administrators = await self.request.app.store.organization_accessor.get_administrators()
            return json_response({"administrators": UserSchema().dump(administrators, many=True)})
        administrator = await self.request.app.store.administrator_accessor.get_by_id(int(administrator_id))
        return json_response({"administrator": UserSchema().dump(administrator)})


class AdministratorServiceView(View):
    @check_session(user_type=Administrator)
    @querystring_schema(AdministratorGetServiceSchema)
    async def get(self):
        service_id = self.request.query.get("id")
        if service_id is None:
            services = await self.request.app.store.organization_accessor.get_services()
            return json_response({"services": ServiceSchema().dump(services, many=True)})
        service = await self.request.app.store.service_accessor.get_by_id(int(service_id))
        return json_response({"service": ServiceSchema().dump(service)})


class AdministratorReceptionView(View):
    @querystring_schema(AdministratorGetReceptionSchema)
    @check_session(user_type=Administrator)
    async def get(self):
        reception_id = self.request.query.get("id")
        if reception_id is None:
            receptions = await self.request.app.store.reception_accessor.get_by_hairdresser(self.user.id)
            return json_response({"receptions": ReceptionSchema().dump(receptions, many=True)})
        reception_id = int(reception_id)
        reception = await self.request.app.store.reception_accessor.get_by_id(reception_id)
        return json_response({"reception": ReceptionSchema().dump(reception)})

    @request_schema(AdministratorDeleteReceptionSchema)
    @check_session(user_type=Administrator)
    async def delete(self):
        reception = await self.request.app.store.reception_accessor.get_by_id(**self.data)
        await self.request.app.store.reception_accessor.delete(reception.id)
        return json_response()


class AdministratorShiftView(View):
    @check_session(user_type=Administrator)
    @querystring_schema(AdministratorGetShiftSchema)
    async def get(self):
        shift_id = self.request.query.get("id")

        if shift_id is None:
            shifts = await self.request.app.store.shift_accessor.get_by_hairdresser(self.user.id)
            return json_response({"shifts": ShiftSchema().dump(shifts, many=True)})

        shift_id = int(shift_id)
        shift = await self.request.app.store.shift_accessor.get_by_id(shift_id)
        return json_response({"shift": ShiftSchema().dump(shift)})

    @check_session(user_type=Administrator)
    @request_schema(AdministratorPutShiftSchema)
    async def put(self):
        shift = await self.request.app.store.shift_accessor.create(**self.data)
        return json_response({"shift": ShiftSchema().dump(shift)})

    @check_session(user_type=Administrator)
    @request_schema(AdministratorPostShiftSchema)
    async def post(self):
        shift = await self.request.app.store.shift_accessor.change(**self.data)
        return json_response({"shift": ShiftSchema().dump(shift)})

    @check_session(user_type=Administrator)
    @request_schema(AdministratorDeleteShiftSchema)
    async def delete(self):
        await self.request.app.store.shift_accessor.delete(**self.data)
        return json_response()


class AdministratorSessionView(View):
    @querystring_schema(AdministratorGetSessionSchema)
    @check_session(user_type=Administrator)
    async def get(self):
        sessions = await self.request.app.store.organization_accessor.get_sessions()
        return json_response({"sessions": SessionSchema().dump(sessions, many=True)})

    @check_session(user_type=Administrator)
    @request_schema(AdministratorDeleteSessionSchema)
    async def delete(self):
        await self.request.app.store.session_accessor.delete(**self.data)
        return json_response()
