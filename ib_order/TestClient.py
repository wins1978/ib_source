from ibapi.client import EClient

class TestClient(EClient):
    def __init__(self, wrapper):
        EClient.__init__(self, wrapper)