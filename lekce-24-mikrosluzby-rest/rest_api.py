from fastapi import FastAPI
from pydantic import BaseModel

from turniket_impl import Turniket
from turniket_kontrakt import Pristup


class HealthResponse(BaseModel):
    status: str


class VpustitResponse(BaseModel):
    povoleno: bool


app = FastAPI(title="Turniket API", version="1.0.0")

turniket = Turniket(nazev="Hlavni turniket", platne_skipasy=[])


@app.get("/health", response_model=HealthResponse)
def health() -> HealthResponse:
    return HealthResponse(status="ok")


@app.get("/turniket/vpustit", response_model=VpustitResponse)
def vpustit(rfid: str) -> VpustitResponse:
    return VpustitResponse(povoleno=turniket.vpustit(rfid))


@app.get("/turniket/log", response_model=list[Pristup])
def log_vstupu() -> list[Pristup]:
    return turniket.log_vstupu()
