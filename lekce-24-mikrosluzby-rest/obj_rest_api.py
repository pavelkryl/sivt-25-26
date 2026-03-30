from fastapi import FastAPI

from turniket_impl import Turniket
from turniket_kontrakt import Pristup


class RestApi:
    def __init__(self, turniket: Turniket) -> None:
        self._turniket = turniket
        self.app = FastAPI(title="Turniket API", version="1.0.0")
        self._register_routes()

    def _register_routes(self) -> None:
        @self.app.get("/health")
        def health() -> dict[str, str]:
            return {"status": "ok"}

        @self.app.get("/turniket/vpustit")
        def vpustit(rfid: str) -> dict[str, bool]:
            return {"povoleno": self._turniket.vpustit(rfid)}

        @self.app.get("/turniket/log", response_model=list[Pristup])
        def log_vstupu() -> list[Pristup]:
            return self._turniket.log_vstupu()


rest_api = RestApi(Turniket(nazev="Hlavni turniket", platne_skipasy=[]))
app = rest_api.app
