from datarobot_asgi_middleware import DataRobotASGIMiddleware
from fastapi import FastAPI, APIRouter, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Any


app = FastAPI()
base_router = APIRouter()
api_router = APIRouter(prefix="/api/v1")
templates = Jinja2Templates(directory="templates")
app.mount(f"/assets", StaticFiles(directory="static/assets"), name="static")

# Add our middleware for DataRobot Custom Applications
app.add_middleware(DataRobotASGIMiddleware, health_endpoint="/health")


@base_router.get("/")
async def root(request: Request) -> Any:
    return templates.TemplateResponse(request=request, name="index.html")


@base_router.get("/health")
async def health() -> Any:
    """
    Health check endpoint for Kubernetes probes.

    If you don't want this, delete `use_health=True` in the middleware.
    """
    return {"status": "healthy"}


@api_router.get("/welcome")
async def welcome() -> Any:
    return {"message": "Welcome Engineer!"}


app.include_router(base_router)
app.include_router(api_router)
