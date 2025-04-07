import os

from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import Response
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.openapi.docs import get_swagger_ui_html, get_redoc_html
from fastapi.openapi.utils import get_openapi

from . import datarobot_middleware

# Support our non-prefix stripping proxy, and local development by
# dynamically setting the URL prefix based on the UVICORN_ROOT_PATH environment variable.
# See: https://stackoverflow.com/a/73815704/4678316
app = FastAPI()
base_router = APIRouter()
api_router = APIRouter(prefix="/api/v1")
templates = Jinja2Templates(directory="templates")
app.mount(f"/assets", StaticFiles(directory="static/assets"), name="static")

# Add our middleware for DataRobot Custom Applications
app.add_middleware(datarobot_middleware.DataRobotASGIMiddleWare, use_health=True)

@base_router.get("/")
async def root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")


@base_router.get("/health")
async def health():
    """
    Health check endpoint for Kubernetes probes.

    If you don't want this, delete `use_health=True` in the middleware.
    """
    return {"status": "healthy"}


@api_router.get("/welcome")
async def welcome():
    return {"message": "Welcome Engineer!"}

app.include_router(base_router)
app.include_router(api_router)
