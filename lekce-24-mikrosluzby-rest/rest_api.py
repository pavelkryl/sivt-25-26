from fastapi import FastAPI

from turniket_impl import Turniket
from turniket_kontrakt import Pristup


app = FastAPI(title="Turniket API", version="1.0.0")

turniket = Turniket(nazev="Hlavni turniket", platne_skipasy=[])


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.get("/turniket/vpustit")
def vpustit(rfid: str) -> dict[str, bool]:
    return {"povoleno": turniket.vpustit(rfid)}


@app.get("/turniket/log", response_model=list[Pristup])
def log_vstupu() -> list[Pristup]:
    return turniket.log_vstupu()
