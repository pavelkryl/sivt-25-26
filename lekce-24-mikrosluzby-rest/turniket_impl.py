from datetime import datetime
from typing import Optional

from turniket_kontrakt import ATurniket, Pristup


class Turniket(ATurniket):

    def __init__(self, nazev: str, platne_skipasy : Optional[list[str]]) -> None:
        self._nazev: str = nazev
        self._platne_skipasy : list[str] = platne_skipasy if platne_skipasy is not None else []
        self._log_pristupu : list[Pristup] = []

    def vpustit(self, rfid: str) -> bool:
        r = rfid in self._platne_skipasy
        self._log_pristupu.append(Pristup(rfid=rfid, cas_pristupu=datetime.now(), povoleno=r))
        return r

    def reset(self) -> None:
        self._platne_skipasy = []
        self._log_pristupu = []

    def iniciace(self, skipasy: list[str]) -> None:
        self._platne_skipasy = skipasy

    def pridej_skipas(self, zakoupeny_skipas_rfid: str) -> None:
        self._platne_skipasy.append(zakoupeny_skipas_rfid)

    # tohle je se stava nadbytecne, ale nechavam to zde
    def log_vstupu(self) -> list[Pristup]:
        return self._log_pristupu
