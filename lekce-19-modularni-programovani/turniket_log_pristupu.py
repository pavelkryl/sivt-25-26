from datetime import datetime
from pydantic import BaseModel

class Pristup(BaseModel):
    rfid: str
    cas_pristupu: datetime
    povoleno: bool

# stav
_platne_skipasy : list[str] = []
_log_pristupu : list[Pristup] = []


# API
def vpustit(rfid: str) -> bool:
    r = rfid in _platne_skipasy
    _log_pristupu.append(Pristup(rfid=rfid, cas_pristupu=datetime.now(), povoleno=r))
    return r

def reset() -> None:
    global _platne_skipasy
    global _log_pristupu
    _platne_skipasy = []
    _log_pristupu = []

def iniciace(skipasy: list[str]) -> None:
    global _platne_skipasy
    _platne_skipasy = skipasy

def pridej(zakoupeny_skipas_rfid: str) -> None:
    _platne_skipasy.append(zakoupeny_skipas_rfid)

def log_vstupu() -> list[Pristup]:
    return _log_pristupu