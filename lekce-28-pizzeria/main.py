"""
REST API pro pizzerii.

Tato vrstva je TENKA - jen prevadi mezi HTTP a interni vrstvou Pizzerie.
Bez vlastni business logiky:
- prijme HTTP request
- zavola odpovidajici metodu na Pizzerie
- pripadne odchyti vyjimku a prelozi ji na HTTP status kod
- vrati response

Spusteni:
    uvicorn main:app --reload

Pak otevri:
    http://localhost:8000          - prazdne (nemame root endpoint)
    http://localhost:8000/docs     - automaticky generovana dokumentace
"""

from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel

from models import Objednavka, Platba, Polozka, VelikostPolozky, ZpusobPlatby
from pizzerie_impl import (
    CastkaNizka,
    NeznamaPolozka,
    ObjednavkaJizZaplacena,
    ObjednavkaNeexistuje,
    Pizzerie,
)


# Request modely - to, co prijde od klienta v tele HTTP requestu.
# Nedavame jim id, datum atp. - to si dopocita server.

class VytvoritObjednavkuRequest(BaseModel):
    zakaznik: str


class PridatPolozkuRequest(BaseModel):
    nazev: str
    velikost: VelikostPolozky


class ZaplatitRequest(BaseModel):
    castka: float
    zpusob: ZpusobPlatby


# Aplikace + jediny stav serveru: jedna instance pizzerie.
# Pri restartu serveru se ztrati - in-memory store.

app = FastAPI(title="Pizzerie API", version="1.0.0")
pizzerie = Pizzerie()


# ============================================================
# ENDPOINTY
# ============================================================

@app.post("/objednavky", response_model=Objednavka, status_code=201)
def vytvorit_objednavku(req: VytvoritObjednavkuRequest, response: Response) -> Objednavka:
    """Vytvori novou objednavku. Vraci 201 Created s Location hlavickou."""
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


@app.post("/objednavky/{id}/platby", response_model=Platba, status_code=201)
def zaplatit(id: int, req: ZaplatitRequest) -> Platba:
    """Zaplati objednavku."""
    try:
        return pizzerie.zaplat(id, castka=req.castka, zpusob=req.zpusob)
    except ObjednavkaNeexistuje:
        raise HTTPException(status_code=404, detail=f"Objednavka {id} neexistuje")
    except ObjednavkaJizZaplacena:
        raise HTTPException(status_code=409, detail="Objednavka je uz zaplacena")
    except CastkaNizka as e:
        raise HTTPException(status_code=400, detail=str(e))
