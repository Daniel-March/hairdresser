import os

from app.web.app import setup_app, Application
from aiohttp.web import run_app

if __name__ == "__main__":
    app = Application()
    setup_app(app=app, config_path=os.path.join(os.path.dirname(__file__), 'config.yml'))

    run_app(app)

# ToDo отредактировать Readme.md, если необходимо
