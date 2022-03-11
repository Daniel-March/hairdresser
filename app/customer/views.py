import uuid

from aiohttp.web_exceptions import HTTPForbidden, HTTPBadRequest
from aiohttp_apispec import request_schema, querystring_schema

from app.web.app import View
from app.web.manager import MainManager
from app.web.models import Customer
from app.web.schemes import (ReceptionSchema, UserSchema, DepartmentSchema, ShiftSchema, ScheduleItemSchema,
                             ServiceSchema)
from app.web.utils import check_session, json_response
from app.customer.schemes import (CustomerRegistrationSchema, CustomerAuthorizationSchema,
                                  CustomerPutReceptionSchema, CustomerDeleteReceptionSchema,
                                  CustomerEditSchema, CustomerGetDepartmentSchema,
                                  CustomerPostReceptionSchema, CustomerGetAdministratorSchema,
                                  CustomerGetHairdresserSchema, CustomerPostRecoverPasswordSchema,
                                  CustomerGetRecoverPasswordSchema)


class CustomerView(View):
    @check_session(user_type=Customer)
    async def get(self):
        return json_response(UserSchema().dump(self.user))


class CustomerEditView(View):
    @check_session(user_type=Customer)
    @request_schema(CustomerEditSchema)
    async def post(self):
        customer = await self.request.app.store.customer_accessor.change(id_=self.user.id, **self.data)
        return json_response(UserSchema().dump(customer))


class CustomerRecoverPasswordView(View):
    @querystring_schema(CustomerGetRecoverPasswordSchema)
    async def get(self):
        email = self.data["email"]
        key = str(uuid.uuid4())
        while key in self.request.app.database.recover_password_requests.keys():
            key = str(uuid.uuid4())
        self.request.app.database.recover_password_requests[key] = email
        print(f"Восстановление пароля для {email}: код {key}")
        return json_response()

    @request_schema(CustomerPostRecoverPasswordSchema)
    async def post(self):
        key = self.data["key"]
        password = self.data["password"]
        if key not in self.request.app.database.recover_password_requests.keys():
            return json_response(status_code=404)
        email = self.request.app.database.recover_password_requests[key]
        customer = self.request.app.store.customer_accessor.get_by_email(email)
        self.request.app.store.customer_accessor.change(customer.id, new_password=password)
        return json_response()


class CustomerRegistrationView(View):
    @request_schema(CustomerRegistrationSchema)
    async def post(self):
        customer = await self.request.app.store.customer_accessor.create(**self.data)
        session = await self.request.app.store.session_accessor.create(user_id=customer.id, user_type=Customer)
        return json_response(cookies={"session": session.key})


class CustomerAuthorizationView(View):
    @request_schema(CustomerAuthorizationSchema)
    async def post(self):
        if self.request.cookies.get("session", None) is not None:
            await self.request.app.store.session_accessor.delete(self.request.cookies.get("session"), throw_error=False)

        customer = await self.request.app.store.customer_accessor.check_authorization(**self.data)
        session = await self.request.app.store.session_accessor.create(user_id=customer.id, user_type=Customer)

        return json_response(cookies={"session": session.key})


class CustomerReceptionView(View):
    @check_session(user_type=Customer)
    async def get(self):
        reception_id = self.request.query.get("id")
        if reception_id is None:
            receptions = await self.request.app.store.reception_accessor.get_by_customer(self.user.id)
            return json_response({"receptions": ReceptionSchema().dump(receptions, many=True)})
        reception = await self.request.app.store.reception_accessor.get_by_id(int(reception_id))
        if reception.customer.id != self.user.id:
            raise HTTPForbidden
        return json_response({"reception": ReceptionSchema().dump(reception)})

    @check_session(user_type=Customer)
    @request_schema(CustomerPostReceptionSchema)
    async def post(self):
        department = self.data["department"]
        services = self.data.get("services")
        hairdresser = self.data.get("hairdresser")
        year = self.data["year"]
        month = self.data["month"]
        day = self.data["day"]
        day_time = self.data.get("day_time")

        available_time = await MainManager.get_available_time_for_reception(self.request.app,
                                                                            department=department,
                                                                            services=services,
                                                                            hairdresser=hairdresser,
                                                                            year=year,
                                                                            month=month,
                                                                            day=day)
        available_services = await MainManager.get_available_services_for_reception(self.request.app,
                                                                                    department=department,
                                                                                    services=services,
                                                                                    hairdresser=hairdresser,
                                                                                    year=year,
                                                                                    month=month,
                                                                                    day=day,
                                                                                    day_time=day_time)
        available_hairdressers = await MainManager.get_available_hairdressers_for_reception(self.request.app,
                                                                                            department=department,
                                                                                            services=services,
                                                                                            year=year,
                                                                                            month=month,
                                                                                            day=day,
                                                                                            day_time=day_time)

        return json_response({"available_time": available_time,
                              "available_services": ServiceSchema().dump(available_services, many=True),
                              "available_hairdressers": UserSchema().dump(available_hairdressers, many=True)})

    @check_session(user_type=Customer)
    @request_schema(CustomerPutReceptionSchema)
    async def put(self):
        department = self.data["department"]
        services = self.data.get("services")
        hairdresser = self.data.get("hairdresser")
        year = self.data["year"]
        month = self.data["month"]
        day = self.data["day"]
        day_time = self.data.get("day_time")

        available_time = await MainManager.get_available_time_for_reception(self.request.app,
                                                                            department=department,
                                                                            services=services,
                                                                            hairdresser=hairdresser,
                                                                            year=year,
                                                                            month=month,
                                                                            day=day)
        for time in available_time:
            if time[0] <= day_time <= time[1]:
                reception = await self.request.app.store.reception_accessor.create(**self.data, customer=self.user.id)
                return json_response({"reception": ReceptionSchema().dump(reception)})
        raise HTTPBadRequest

    @check_session(user_type=Customer)
    @request_schema(CustomerDeleteReceptionSchema)
    async def delete(self):
        reception = await self.request.app.store.reception_accessor.get_by_id(**self.data)
        if reception.customer.id != self.user.id:
            raise HTTPForbidden(text="Forbidden to delete another's reception")
        await self.request.app.store.reception_accessor.delete(reception.id)
        return json_response()


class CustomerAdministratorView(View):
    @check_session(user_type=Customer)
    @querystring_schema(CustomerGetAdministratorSchema)
    async def get(self):
        administrator_id = self.request.query.get("id")
        if administrator_id is None:
            administrators = await self.request.app.store.organization_accessor.get_administrators()
            return json_response({"administrators": UserSchema().dump(administrators, many=True)})
        administrator = await self.request.app.store.administrator_accessor.get_by_id(administrator_id)
        return json_response({"administrator": administrator})


class CustomerHairdresserView(View):
    @check_session(user_type=Customer)
    @querystring_schema(CustomerGetHairdresserSchema)
    async def get(self):
        hairdresser_id = self.request.query.get("id")
        if hairdresser_id is None:
            hairdressers = await self.request.app.store.organization_accessor.get_hairdressers()
            return json_response({"hairdressers": UserSchema().dump(hairdressers, many=True)})
        hairdresser = await self.request.app.store.hairdresser_accessor.get_by_id(hairdresser_id)
        return json_response({"hairdresser": hairdresser})


class CustomerDepartmentView(View):
    @check_session(user_type=Customer)
    @querystring_schema(CustomerGetDepartmentSchema)
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
