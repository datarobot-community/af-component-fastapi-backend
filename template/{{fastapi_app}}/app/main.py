import os

from fastapi import FastAPI, APIRouter
from fastapi.responses import FileResponse, Response
from fastapi.staticfiles import StaticFiles
from . import datarobot_middleware

# Support our non-prefix stripping proxy, and local development by
# dynamically setting the URL prefix based on the UVICORN_ROOT_PATH environment variable.
# See: https://stackoverflow.com/a/73815704/4678316
prefix = os.getenv("UVICORN_ROOT_PATH", "")
app = FastAPI(docs_url=f"{prefix}/docs", redoc_url=f"{prefix}/redoc", openapi_url=f"{prefix}/openapi.json")
base_router = APIRouter(prefix=prefix)
api_router = APIRouter(prefix=f"{prefix}/api/v1")
# Add our middleware for DataRobot Custom Applications
app.add_middleware(datarobot_middleware.DataRobotMiddleWare)


@base_router.get("/")
async def root():
    return FileResponse("static/index.html")


@base_router.get("/health")
async def health():
    """
    Health check endpoint for Kubernetes probes.

    If you don't want this, remove DataRobotMiddleWare
    from the middleware stack above when you delete it.
    """
    return {"status": "healthy"}

   
@api_router.get("/welcome")
async def welcome():
    return {"message": "Welcome Engineer!"}


app.include_router(base_router)
app.include_router(api_router)
app.mount(f"{prefix}/assets", StaticFiles(directory="static/assets"), name="static")
