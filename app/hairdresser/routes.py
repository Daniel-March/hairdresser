import typing

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application"):
    from app.hairdresser.views import HairdresserView
    from app.hairdresser.views import HairdresserAuthorizationView
    from app.hairdresser.views import HairdresserAdministratorView
    from app.hairdresser.views import HairdresserCustomerView
    from app.hairdresser.views import HairdresserDepartmentView
    from app.hairdresser.views import HairdresserReceptionView
    from app.hairdresser.views import HairdresserShiftView

    app.router.add_view("/hairdresser", HairdresserView)
    app.router.add_view("/hairdresser.authorization", HairdresserAuthorizationView)
    app.router.add_view("/hairdresser.administrator", HairdresserAdministratorView)
    app.router.add_view("/hairdresser.customer", HairdresserCustomerView)
    app.router.add_view("/hairdresser.department", HairdresserDepartmentView)
    app.router.add_view("/hairdresser.reception", HairdresserReceptionView)
    app.router.add_view("/hairdresser.shift", HairdresserShiftView)
