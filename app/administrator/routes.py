import typing

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application"):
    from app.administrator.views import AdministratorView
    from app.administrator.views import AdministratorAuthorizationView
    from app.administrator.views import AdministratorCustomerView
    from app.administrator.views import AdministratorHairdresserView
    from app.administrator.views import AdministratorDepartmentView
    from app.administrator.views import AdministratorAdministratorView
    from app.administrator.views import AdministratorServiceView
    from app.administrator.views import AdministratorReceptionView
    from app.administrator.views import AdministratorShiftView
    from app.administrator.views import AdministratorSessionView

    app.router.add_view("/administrator", AdministratorView)
    app.router.add_view("/administrator.authorization", AdministratorAuthorizationView)
    app.router.add_view("/administrator.customer", AdministratorCustomerView)
    app.router.add_view("/administrator.hairdresser", AdministratorHairdresserView)
    app.router.add_view("/administrator.department", AdministratorDepartmentView)
    app.router.add_view("/administrator.administrator", AdministratorAdministratorView)
    app.router.add_view("/administrator.service", AdministratorServiceView)
    app.router.add_view("/administrator.reception", AdministratorReceptionView)
    app.router.add_view("/administrator.shift", AdministratorShiftView)
    app.router.add_view("/administrator.session", AdministratorSessionView)
