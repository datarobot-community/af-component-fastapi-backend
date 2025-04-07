import os
from typing import Union, cast
from starlette.types import ASGIApp, Scope, Receive, Send
from asgiref.typing import (
    HTTPScope,
    WebSocketScope,
)


class DataRobotMiddleWare:
    """
    Middleware to augment ASGI applications run by DataRobot Custom Applications.

    It routes root URL requests from Kubernetes to the base /health URL to support
    more robust health checks than just loading the root URL.
    """
    def __init__(self, app: ASGIApp, health_redirect: bool = True):
        self.app = app
        self.health_redirect = health_redirect
        # Get the script name from the environment variable to know what the internal
        # load balancer is using as the prefix for the request.
        self.internal_prefix = os.getenv("SCRIPT_NAME", None)
    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] not in ("http", "websocket"):
            return await self.app(scope, receive, send)

        headers = dict(scope["headers"])
        x_forwarded_prefix = headers.get(b"x-forwarded-prefix", b"").decode("utf-8")

        # Send Kubernetes probe requests to /health for real health checks
        user_agent = headers.get(b"user-agent", b"").decode("utf-8")
        if user_agent.startswith("kube-probe"):
            scope["path"] = f"/health"
            scope["root_path"] = ""
            return await self.app(scope, receive, send)

        if not x_forwarded_prefix and self.internal_prefix:
            # Getting a request from internal load balancer.
            scope["root_path"] = self.internal_prefix + scope["root_path"]
            return await self.app(scope, receive, send)

        # breakpoint()
        if x_forwarded_prefix:
            # Getting a request from the external load balancer.
            scope["root_path"] = x_forwarded_prefix + scope["root_path"]
            return await self.app(scope, receive, send)

        return await self.app(scope, receive, send)
