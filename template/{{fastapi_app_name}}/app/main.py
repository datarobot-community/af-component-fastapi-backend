# Copyright 2025 DataRobot, Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import json
import os
from datarobot_asgi_middleware import DataRobotASGIMiddleware
from fastapi import FastAPI, APIRouter, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Any


app = FastAPI()
base_router = APIRouter()
api_router = APIRouter(prefix="/api/v1")
templates = Jinja2Templates(directory="templates")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
STATIC_DIR = os.path.join(BASE_DIR, "static")

# Add our middleware for DataRobot Custom Applications
app.add_middleware(DataRobotASGIMiddleware, health_endpoint="/health")

def get_app_base_url(api_port: str) -> str:
    """Get and normalize the application base URL."""
    app_base_url = os.getenv("BASE_PATH", "")
    notebook_id = os.getenv("NOTEBOOK_ID", "")
    if not app_base_url and notebook_id:
        app_base_url = f"notebook-sessions/{notebook_id}/ports/{api_port}"

    if app_base_url:
        return "/" + app_base_url.strip("/") + "/"
    else:
        return "/"


def get_manifest_assets(
    manifest_path: str, entry: str = "index.html", app_base_url: str = "/"
) -> dict[str, list[str]]:
    """
    Reads the Vite manifest and returns the JS and CSS files for the given entry.
    """
    with open(manifest_path, "r") as f:
        manifest = json.load(f)
    entry_data = manifest.get(entry, {})
    js_files = []
    css_files = []

    # Main JS file
    if "file" in entry_data:
        js_files.append(app_base_url + entry_data["file"])

    # CSS files
    for css in entry_data.get("css", []):
        css_files.append(app_base_url + css)

    return {"js": js_files, "css": css_files}


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

 # This is the base path for the app, used to serve static files and templates
app.mount(
    "/assets",
    StaticFiles(directory=os.path.join(STATIC_DIR, "assets")),
    name="static",
)

# This is the final path that serves the React app
@app.get("{full_path:path}")
async def serve_root(request: Request) -> HTMLResponse:
    """
    Serve the React index.html for the all routes, injecting ENV variables and fixing asset paths.
    """
    manifest_path = os.path.join(STATIC_DIR, ".vite", "manifest.json")

    api_port = os.getenv("PORT", "8080")
    app_base_url = get_app_base_url(api_port)

    env_vars = {
        "BASE_PATH": app_base_url,
        "API_PORT": api_port,
    }

    manifest_assets = get_manifest_assets(
        manifest_path,
        "index.html",
        app_base_url,
    )

    return templates.TemplateResponse(
        request=request,
        name="index.html",
        context={
            "env": env_vars,
            "app_base_url": app_base_url,
            "js_files": manifest_assets["js"],
            "css_files": manifest_assets["css"],
        },
    )
