from datetime import datetime
from pydantic import BaseModel, Field


class Adresa(BaseModel):
    ulice: str
    cislo_popisne: str
    mesto: str
    psc: str
    stat: str

class Kniha(BaseModel):
    nazev: str
    isbn: str
    strany: int = Field(ge=5, le=10000, default=100)
    stara: bool
    datum_vydani: datetime
    adresa_vydavatele: Adresa | None = None
    kapitoly: list[str] = []


kniha_1984: Kniha = Kniha(
    nazev="1984",
    isbn="978-80-98765-43-2",
    strany=328,
    stara=True,
    adresa_vydavatele=Adresa(
        ulice="Hlavní",
        cislo_popisne="123",
        mesto="Praha",
        psc="11000",
        stat="Česká republika"
    ),
    datum_vydani=datetime(1949, 6, 8)
)

kniha_1984.kapitoly.append("Velký bratr")

# ulozeni do souboru jako JSON
txt_json = kniha_1984.model_dump_json(indent=4)

soubor = open("kniha.json", "w")
soubor.write(txt_json)
soubor.close()

# nacteni ze souboru v JSON
with open("kniha.json", "r") as soubor:
    txt_json = soubor.read()

# uz soubor nepotrebujeme, je zavreny, ale text z nej mame v txt_json
kniha_1984_loaded = Kniha.model_validate_json(txt_json)

# vytiskneme objektovou reprezentaci
print(kniha_1984_loaded)
