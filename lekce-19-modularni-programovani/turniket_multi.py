from datetime import datetime
from pydantic import BaseModel


class Pristup(BaseModel):
    rfid: str
    cas_pristupu: datetime
    povoleno: bool


class Turniket(BaseModel):
    nazev: str
    platne_skipasy : list[str] = []
    log_pristupu : list[Pristup] = []


# API
def vpustit(turniket: Turniket, rfid: str) -> bool:
    r = rfid in turniket.platne_skipasy
    turniket.log_pristupu.append(Pristup(rfid=rfid, cas_pristupu=datetime.now(), povoleno=r))
    return r

def reset(turniket: Turniket) -> None:
    turniket.platne_skipasy = []
    turniket.log_pristupu = []

def iniciace(turniket: Turniket, skipasy: list[str]) -> None:
    turniket.platne_skipasy = skipasy

def pridej(turniket: Turniket, zakoupeny_skipas_rfid: str) -> None:
    turniket.platne_skipasy.append(zakoupeny_skipas_rfid)

# tohle je se stava nadbytecne, ale nechavam to zde
def log_vstupu(turniket: Turniket) -> list[Pristup]:
    return turniket.log_pristupu