import asyncio
import typing

from app.store.database.database import Database

if typing.TYPE_CHECKING:
    from app.web.app import Application


class Store:
    def __init__(self, app: "Application"):
        from app.store.administrator.accessor import AdministratorAccessor
        from app.store.customer.accessor import CustomerAccessor
        from app.store.department.accessor import DepartmentAccessor
        from app.store.hairdresser.accessor import HairdresserAccessor
        from app.store.organization.accessor import OrganizationAccessor
        from app.store.reception.accessor import ReceptionAccessor
        from app.store.service.accessor import ServiceAccessor
        from app.store.session.accessor import SessionAccessor
        from app.store.shift.accessor import ShiftAccessor

        self.administrator_accessor = AdministratorAccessor(app)
        self.customer_accessor = CustomerAccessor(app)
        self.department_accessor = DepartmentAccessor(app)
        self.hairdresser_accessor = HairdresserAccessor(app)
        self.organization_accessor = OrganizationAccessor(app)
        self.reception_accessor = ReceptionAccessor(app)
        self.service_accessor = ServiceAccessor(app)
        self.session_accessor = SessionAccessor(app)
        self.shift_accessor = ShiftAccessor(app)


def setup_store(app: "Application"):
    app.database = Database()
    app.store = Store(app)
    app.on_startup.append(app.database.connect)
    app.on_shutdown.append(app.database.disconnect)
