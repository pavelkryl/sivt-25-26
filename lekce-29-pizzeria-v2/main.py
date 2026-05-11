"""
REST API pro pizzerii - verze 2.

ZMENA OPROTI V1:
- Platba je nyni SINGLETON, ne kolekce:
  * URL: /objednavky/{id}/platba (singular, BEZ id platby)
  * Metoda: PUT (idempotentni), ne POST
- GET /objednavky/{id}/platba prida moznost se zeptat na platbu
"""

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel

from models import Objednavka, Platba, Polozka, VelikostPolozky, ZpusobPlatby
from pizzerie_impl import (
    CastkaNizka,
    NeznamaPolozka,
    ObjednavkaJizZaplacena,
    ObjednavkaNeexistuje,
    PlatbaSeLisi,
    Pizzerie,
)


# Request modely

class VytvoritObjednavkuRequest(BaseModel):
    zakaznik: str


class PridatPolozkuRequest(BaseModel):
    nazev: str
    velikost: VelikostPolozky


class ZaplatitRequest(BaseModel):
    castka: float
    zpusob: ZpusobPlatby


# Aplikace + jediny stav serveru: jedna instance pizzerie.

app = FastAPI(title="Pizzerie API", version="2.0.0")
pizzerie = Pizzerie()


# ============================================================
# ENDPOINTY
# ============================================================

@app.post("/objednavky", response_model=Objednavka, status_code=201)
def vytvorit_objednavku(req: VytvoritObjednavkuRequest, response: Response) -> Objednavka:
    """Vytvori novou objednavku."""
    objednavka = pizzerie.vytvor_objednavku(zakaznik=req.zakaznik)
    response.headers["Location"] = f"/objednavky/{objednavka.id}"
    return objednavka


@app.get("/objednavky", response_model=list[Objednavka])
def seznam_objednavek() -> list[Objednavka]:
    """Vraci seznam vsech objednavek."""
    return pizzerie.seznam_objednavek()


@app.get("/objednavky/{id}", response_model=Objednavka)
def detail_objednavky(id: int) -> Objednavka:
    """Vraci detail jedne objednavky."""
    try:
        return pizzerie.ziskej_objednavku(id)
    except ObjednavkaNeexistuje:
        raise HTTPException(status_code=404, detail=f"Objednavka {id} neexistuje")


@app.post("/objednavky/{id}/polozky", response_model=Polozka, status_code=201)
def pridat_polozku(id: int, req: PridatPolozkuRequest) -> Polozka:
    """Prida polozku do objednavky."""
    try:
        return pizzerie.pridej_polozku(id, nazev=req.nazev, velikost=req.velikost)
    except ObjednavkaNeexistuje:
        raise HTTPException(status_code=404, detail=f"Objednavka {id} neexistuje")
    except ObjednavkaJizZaplacena:
        raise HTTPException(status_code=409, detail="Objednavka je uz zaplacena, nelze do ni pridavat")
    except NeznamaPolozka as e:
        raise HTTPException(status_code=422, detail=str(e))


# --- PLATBA jako SINGLETON ----------------------------------

@app.put("/objednavky/{id}/platba", response_model=Platba)
def zaplatit(id: int, req: ZaplatitRequest) -> Platba:
    """
    Zaplati objednavku - IDEMPOTENTNI.

    PUT, ne POST: klient sam urcuje URI ('/objednavky/{id}/platba'),
    a opakovane volani se stejnymi daty vrati existujici platbu (no-op).

    Status kody:
    - 200 OK: platba na danem URI existuje (at uz prave vznikla, nebo uz existovala)
    - 404 Not Found: objednavka neexistuje
    - 409 Conflict: platba uz existuje, ale nove data jsou jina
    - 400 Bad Request: castka < suma

    Vzdy 200, nikdy 201 - z hlediska klienta je vysledek stejny:
    platba na danem URI ma dane hodnoty. Cista idempotence.
    """
    try:
        return pizzerie.zaplat(id, castka=req.castka, zpusob=req.zpusob)
    except ObjednavkaNeexistuje:
        raise HTTPException(status_code=404, detail=f"Objednavka {id} neexistuje")
    except PlatbaSeLisi as e:
        raise HTTPException(status_code=409, detail=str(e))
    except CastkaNizka as e:
        raise HTTPException(status_code=400, detail=str(e))


@app.get("/objednavky/{id}/platba", response_model=Platba)
def detail_platby(id: int) -> Platba:
    """Vraci detail platby objednavky, nebo 404 pokud jeste nebyla zaplacena."""
    try:
        platba = pizzerie.ziskej_platbu(id)
    except ObjednavkaNeexistuje:
        raise HTTPException(status_code=404, detail=f"Objednavka {id} neexistuje")

    if platba is None:
        raise HTTPException(status_code=404, detail=f"Objednavka {id} jeste nebyla zaplacena")

    return platba