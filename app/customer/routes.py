import typing

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application"):
    from app.customer.views import CustomerView
    from app.customer.views import CustomerEditView
    from app.customer.views import CustomerRecoverPasswordView
    from app.customer.views import CustomerRegistrationView
    from app.customer.views import CustomerAuthorizationView
    from app.customer.views import CustomerReceptionView
    from app.customer.views import CustomerAdministratorView
    from app.customer.views import CustomerHairdresserView
    from app.customer.views import CustomerDepartmentView

    app.router.add_view("/customer", CustomerView)
    app.router.add_view("/customer.edit", CustomerEditView)
    app.router.add_view("/customer.recover_password", CustomerRecoverPasswordView)
    app.router.add_view("/customer.registration", CustomerRegistrationView)
    app.router.add_view("/customer.authorization", CustomerAuthorizationView)
    app.router.add_view("/customer.reception", CustomerReceptionView)
    app.router.add_view("/customer.administrator", CustomerAdministratorView)
    app.router.add_view("/customer.hairdresser", CustomerHairdresserView)
    app.router.add_view("/customer.department", CustomerDepartmentView)
