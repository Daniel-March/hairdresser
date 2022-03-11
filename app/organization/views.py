from aiohttp_apispec import request_schema, querystring_schema

from app.organization.schemes import (OrganizationAuthorizationSchema, OrganizationGetHairdresserSchema,
                                      OrganizationGetDepartmentSchema, OrganizationDeleteHairdresserSchema,
                                      OrganizationPutHairdresserSchema, OrganizationPostHairdresserSchema,
                                      OrganizationPutDepartmentSchema, OrganizationPostDepartmentSchema,
                                      OrganizationDeleteDepartmentSchema, OrganizationGetAdministratorSchema,
                                      OrganizationPutAdministratorSchema, OrganizationPostAdministratorSchema,
                                      OrganizationDeleteAdministratorSchema, OrganizationGetServiceSchema,
                                      OrganizationPutServiceSchema, OrganizationPostServiceSchema,
                                      OrganizationDeleteServiceSchema, OrganizationGetCustomerSchema,
                                      OrganizationGetReceptionSchema, OrganizationDeleteReceptionSchema,
                                      OrganizationGetShiftSchema, OrganizationPutShiftSchema,
                                      OrganizationPostShiftSchema, OrganizationDeleteShiftSchema,
                                      OrganizationDeleteSessionSchema, OrganizationGetSessionSchema, )
from app.web.app import View
from app.web.manager import MainManager
from app.web.models import Organization
from app.web.schemes import UserSchema, DepartmentSchema, ServiceSchema, ScheduleItemSchema, ShiftSchema, \
    ReceptionSchema, SessionSchema
from app.web.utils import check_session, json_response


class OrganizationView(View):
    @check_session(user_type=Organization)
    async def get(self):
        organization = self.user

        return json_response({"name": organization.name,
                              "email": organization.email})


class OrganizationAuthorizationView(View):
    @request_schema(OrganizationAuthorizationSchema)
    async def post(self):
        if self.request.cookies.get("session", None) is not None:
            await self.request.app.store.session_accessor.delete(self.request.cookies.get("session"), throw_error=False)

        await self.request.app.store.organization_accessor.check_authorization(**self.data)
        session = await self.request.app.store.session_accessor.create(user_id=0, user_type=Organization)

        return json_response(cookies={"session": session.key})


class OrganizationCustomerView(View):
    @check_session(user_type=Organization)
    @querystring_schema(OrganizationGetCustomerSchema)
    async def get(self):
        customer_id = self.request.query.get("id")
        if customer_id is None:
            customers = await self.request.app.store.organization_accessor.get_customers()
            return json_response({"customers": UserSchema().dump(customers, many=True)})
        customer = await self.request.app.store.customer_accessor.get_by_id(customer_id)
        return json_response({"customer": UserSchema().dump(customer)})


class OrganizationHairdresserView(View):
    @check_session(user_type=Organization)
    @querystring_schema(OrganizationGetHairdresserSchema)
    async def get(self):
        hairdresser_id = self.request.query.get("id")
        if hairdresser_id is None:
            hairdressers = await self.request.app.store.organization_accessor.get_hairdressers()
            return json_response({"hairdressers": UserSchema().dump(hairdressers, many=True)})
        hairdresser = await self.request.app.store.hairdresser_accessor.get_by_id(hairdresser_id)
        return json_response({"hairdresser": UserSchema().dump(hairdresser)})

    @check_session(user_type=Organization)
    @request_schema(OrganizationPutHairdresserSchema)
    async def put(self):
        hairdresser = await self.request.app.store.hairdresser_accessor.create(**self.data)
        return json_response({"hairdresser": UserSchema().dump(hairdresser)})

    @check_session(user_type=Organization)
    @request_schema(OrganizationPostHairdresserSchema)
    async def post(self):
        hairdresser = await self.request.app.store.hairdresser_accessor.change(**self.data)
        return json_response({"hairdresser": UserSchema().dump(hairdresser)})

    @check_session(user_type=Organization)
    @request_schema(OrganizationDeleteHairdresserSchema)
    async def delete(self):
        await self.request.app.store.hairdresser_accessor.delete(**self.data)
        return json_response()


class OrganizationDepartmentView(View):
    @check_session(user_type=Organization)
    @querystring_schema(OrganizationGetDepartmentSchema)
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

    @check_session(user_type=Organization)
    @request_schema(OrganizationPutDepartmentSchema)
    async def put(self):
        department = await self.request.app.store.department_accessor.create(**self.data)
        return json_response({"department": DepartmentSchema().dump(department)})

    @check_session(user_type=Organization)
    @request_schema(OrganizationPostDepartmentSchema)
    async def post(self):
        department = await self.request.app.store.department_accessor.change(**self.data)
        return json_response({"department": DepartmentSchema().dump(department)})

    @check_session(user_type=Organization)
    @request_schema(OrganizationDeleteDepartmentSchema)
    async def delete(self):
        await self.request.app.store.department_accessor.delete(**self.data)
        return json_response()


class OrganizationAdministratorView(View):
    @check_session(user_type=Organization)
    @querystring_schema(OrganizationGetAdministratorSchema)
    async def get(self):
        administrator_id = self.request.query.get("id")
        if administrator_id is None:
            administrators = await self.request.app.store.organization_accessor.get_administrators()
            return json_response({"administrators": UserSchema().dump(administrators, many=True)})
        administrator = await self.request.app.store.administrator_accessor.get_by_id(administrator_id)
        return json_response({"administrator": UserSchema().dump(administrator)})

    @check_session(user_type=Organization)
    @request_schema(OrganizationPutAdministratorSchema)
    async def put(self):
        administrator = await self.request.app.store.administrator_accessor.create(**self.data)
        return json_response({"administrator": UserSchema().dump(administrator)})

    @check_session(user_type=Organization)
    @request_schema(OrganizationPostAdministratorSchema)
    async def post(self):
        administrator = await self.request.app.store.administrator_accessor.change(**self.data)
        return json_response({"administrator": UserSchema().dump(administrator)})

    @check_session(user_type=Organization)
    @request_schema(OrganizationDeleteAdministratorSchema)
    async def delete(self):
        await self.request.app.store.administrator_accessor.delete(**self.data)
        return json_response()


class OrganizationServiceView(View):
    @check_session(user_type=Organization)
    @querystring_schema(OrganizationGetServiceSchema)
    async def get(self):
        service_id = self.request.query.get("id")
        if service_id is None:
            services = await self.request.app.store.organization_accessor.get_services()
            return json_response(
                {"services": ServiceSchema().dump(services, many=True)})
        service = await self.request.app.store.service_accessor.get_by_id(int(service_id))
        return json_response({"service": ServiceSchema().dump(service)})

    @check_session(user_type=Organization)
    @request_schema(OrganizationPutServiceSchema)
    async def put(self):
        service = await self.request.app.store.service_accessor.create(**self.data)
        return json_response({"service": ServiceSchema().dump(service)})

    @check_session(user_type=Organization)
    @request_schema(OrganizationPostServiceSchema)
    async def post(self):
        service = await self.request.app.store.service_accessor.change(**self.data)
        return json_response({"service": ServiceSchema().dump(service)})

    @check_session(user_type=Organization)
    @request_schema(OrganizationDeleteServiceSchema)
    async def delete(self):
        await self.request.app.store.service_accessor.delete(**self.data)
        return json_response()


class OrganizationReceptionView(View):
    @querystring_schema(OrganizationGetReceptionSchema)
    @check_session(user_type=Organization)
    async def get(self):
        reception_id = self.request.query.get("id")
        if reception_id is None:
            receptions = await self.request.app.store.reception_accessor.get_by_hairdresser(self.user.id)
            return json_response({"receptions": ReceptionSchema().dump(receptions, many=True)})
        reception_id = int(reception_id)
        reception = await self.request.app.store.reception_accessor.get_by_id(reception_id)
        return json_response({"reception": ReceptionSchema().dump(reception)})

    @request_schema(OrganizationDeleteReceptionSchema)
    @check_session(user_type=Organization)
    async def delete(self):
        await self.request.app.store.reception_accessor.delete(**self.data)
        return json_response()


class OrganizationShiftView(View):
    @check_session(user_type=Organization)
    @querystring_schema(OrganizationGetShiftSchema)
    async def get(self):
        shift_id = self.request.query.get("id")

        if shift_id is None:
            shifts = await self.request.app.store.organization_accessor.get_shifts()
            return json_response({"shifts": ShiftSchema().dump(shifts, many=True)})

        shift_id = int(shift_id)
        shift = await self.request.app.store.shift_accessor.get_by_id(shift_id)
        return json_response({"shift": ShiftSchema().dump(shift)})

    @check_session(user_type=Organization)
    @request_schema(OrganizationPutShiftSchema)
    async def put(self):
        shift = await self.request.app.store.shift_accessor.create(**self.data)
        return json_response({"shift": ShiftSchema().dump(shift)})

    @check_session(user_type=Organization)
    @request_schema(OrganizationPostShiftSchema)
    async def post(self):
        shift = await self.request.app.store.shift_accessor.change(**self.data)
        return json_response({"shift": ShiftSchema().dump(shift)})

    @check_session(user_type=Organization)
    @request_schema(OrganizationDeleteShiftSchema)
    async def delete(self):
        await self.request.app.store.shift_accessor.delete(**self.data)
        return json_response()


class OrganizationSessionView(View):
    @querystring_schema(OrganizationGetSessionSchema)
    @check_session(user_type=Organization)
    async def get(self):
        sessions = await self.request.app.store.organization_accessor.get_sessions()
        return json_response({"sessions": SessionSchema().dump(sessions, many=True)})

    @check_session(user_type=Organization)
    @request_schema(OrganizationDeleteSessionSchema)
    async def delete(self):
        await self.request.app.store.session_accessor.delete(**self.data)
        return json_response()
