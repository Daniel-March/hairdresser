import typing

from app.customer.routes import setup_routes as setup_customer_routes
from app.hairdresser.routes import setup_routes as setup_hairdresser_routes
from app.organization.routes import setup_routes as setup_organization_routes
from app.administrator.routes import setup_routes as setup_administrator_routes

if typing.TYPE_CHECKING:
    from app.web.app import Application


def setup_routes(app: "Application"):
    setup_customer_routes(app)
    setup_hairdresser_routes(app)
    setup_organization_routes(app)
    setup_administrator_routes(app)
