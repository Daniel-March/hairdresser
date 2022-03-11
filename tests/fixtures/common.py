import asyncio
import os
import pytest

from app.web.app import setup_app, Application


@pytest.fixture(scope="module")
def event_loop():
    loop = asyncio.get_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="class")
@pytest.mark.asyncio
async def app():
    application = Application()
    setup_app(app=application, config_path=os.path.join(os.path.dirname(__file__), "..", 'config.yml'))
    await application.database.connect(application)
    await application.database.regenerate()
    return application
