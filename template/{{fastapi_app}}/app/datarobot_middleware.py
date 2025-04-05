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
    def __init__(self, app: ASGIApp):
        self.app = app

    async def __call__(self, scope: Scope, receive: Receive, send: Send):
        if scope["type"] not in ("http", "websocket"):
            return await self.app(scope, receive, send)
        headers = dict(scope["headers"])
        # Send Kubernetes probe requests to /health for real health checks
        user_agent = headers.get(b"user-agent", b"").decode("utf-8")
        if user_agent.startswith("kube-probe"):
            scope["path"] = scope["path"].rstrip("/") + "/health"
            scope["query_string"] = b""
            return await self.app(scope, receive, send)
        
        return await self.app(scope, receive, send)
