import pytest
from fastapi import FastAPI
from fastapi.testclient import TestClient
from app.datarobot_middleware import DataRobotMiddleWare

@pytest.fixture
def app(request):
    app = FastAPI()
    # Add our middleware
    app.add_middleware(DataRobotMiddleWare)


    # Add a test health endpoint
    @app.get("/health")
    async def health():
        return {"status": "healthy"}


    @app.get("/")
    async def root():
        return {"message": "hello"}


    return app


def test_kubernetes_probe_redirect(app):
    # Create a test client
    client = TestClient(app)
 
    # Make a request that simulates the Kubernetes probe
    response = client.get(
        "/",
        headers={
            "user-agent": "kube-probe/1.30+",
            "accept": "*/*",
            "connection": "close",
            "host": "10.190.91.26:8080"
        }
    )
    
    # Verify the response
    assert response.status_code == 200
    assert response.request.url.path == "/", "It should not redirect to /health"
    assert response.json() == {"status": "healthy"}


def test_normal_request(app):
    # Create a test client
    client = TestClient(app)

    # Make a normal request to the apps endpoint
    response = client.get("/")
    
    # Verify the response
    assert response.status_code == 200
    assert response.json() == {"message": "hello"}


