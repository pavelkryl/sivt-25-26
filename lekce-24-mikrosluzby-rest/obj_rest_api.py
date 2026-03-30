from fastapi import FastAPI
from pydantic import BaseModel

from turniket_impl import Turniket
from turniket_kontrakt import Pristup


class HealthResponse(BaseModel):
    status: str


class VpustitResponse(BaseModel):
    povoleno: bool


class RestApi:
    def __init__(self, turniket: Turniket) -> None:
        self._turniket = turniket
        self.app = FastAPI(title="Turniket API", version="1.0.0")
        self._register_routes()

    def _register_routes(self) -> None:
        @self.app.get("/health", response_model=HealthResponse)
        def health() -> HealthResponse:
            return HealthResponse(status="ok")

        @self.app.get("/turniket/vpustit", response_model=VpustitResponse)
        def vpustit(rfid: str) -> VpustitResponse:
            return VpustitResponse(povoleno=self._turniket.vpustit(rfid))

        @self.app.get("/turniket/log", response_model=list[Pristup])
        def log_vstupu() -> list[Pristup]:
            return self._turniket.log_vstupu()


rest_api = RestApi(Turniket(nazev="Hlavni turniket", platne_skipasy=[]))
app = rest_api.app
