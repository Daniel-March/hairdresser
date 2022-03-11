import typing

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application"):
    from app.organization.views import OrganizationView
    from app.organization.views import OrganizationCustomerView
    from app.organization.views import OrganizationAuthorizationView
    from app.organization.views import OrganizationHairdresserView
    from app.organization.views import OrganizationDepartmentView
    from app.organization.views import OrganizationAdministratorView
    from app.organization.views import OrganizationServiceView
    from app.organization.views import OrganizationReceptionView
    from app.organization.views import OrganizationShiftView
    from app.organization.views import OrganizationSessionView

    app.router.add_view("/organization", OrganizationView)
    app.router.add_view("/organization.customer", OrganizationCustomerView)
    app.router.add_view("/organization.authorization", OrganizationAuthorizationView)
    app.router.add_view("/organization.hairdresser", OrganizationHairdresserView)
    app.router.add_view("/organization.department", OrganizationDepartmentView)
    app.router.add_view("/organization.administrator", OrganizationAdministratorView)
    app.router.add_view("/organization.service", OrganizationServiceView)
    app.router.add_view("/organization.reception", OrganizationReceptionView)
    app.router.add_view("/organization.shift", OrganizationShiftView)
    app.router.add_view("/organization.session", OrganizationSessionView)
