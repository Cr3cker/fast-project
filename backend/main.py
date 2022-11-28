from apis.base import api_router
from core.config import settings
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles


def include_router(app):
	app.include_router(api_router)


def configure_static(app):
    app.mount("/static", StaticFiles(directory="static"), name="static")


def start_application():
    app = FastAPI(title=settings.PROJECT_NAME, version=settings.PROJECT_VERSION)
    include_router(app)
    configure_static(app)
    return app

app = start_application()
