
_platne_skipasy : list[str] = []

def vpustit(rfid: str) -> bool:
    return rfid in _platne_skipasy

def reset() -> None:
    global _platne_skipasy
    _platne_skipasy = []

def iniciace(skipasy: list[str]) -> None:
    global _platne_skipasy
    _platne_skipasy = skipasy

def pridej(zakoupeny_skipas_rfid: str) -> None:
    _platne_skipasy.append(zakoupeny_skipas_rfid)
