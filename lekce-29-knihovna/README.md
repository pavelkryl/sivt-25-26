# Knihovna — REST API

Cíl dnešní hodiny: nakódovat REST API pro knihovnu podle návrhu, který jsme spolu navrhli minule. Pizzerie V2 (kterou jsme dnes refaktorovali) ti slouží jako vzor.

## Co dostáváte

V repu máte kostru projektu:

```
lekce-29-knihovna/
├── Makefile          # make prepare, make run
├── requirements.txt  # FastAPI, uvicorn, pydantic
├── README.md         # tento soubor
├── models.py         # prázdné, doplníte pydantic modely
├── knihovna_impl.py  # kostra třídy Knihovna + vlastní výjimky
└── main.py           # /health endpoint jako důkaz, že to běží
```

Spuštění:

```bash
make prepare    # jednou na začátku (vytvoří venv, nainstaluje balíčky)
make run        # spustí server na http://localhost:8000
```

`/docs` ti vygeneruje Swagger dokumentaci, **ale testovat budeš v Postmanu** (znáš ho z minulé hodiny).

## Doménový model

Knihovna má tři entity:

```python
class Kniha:
    id: int
    nazev: str
    autor: str
    rok: int

class Ctenar:
    id: int
    jmeno: str
    email: str

class Vypujcka:
    id: int
    id_ctenare: int          # kdo si půjčil
    id_knih: list[int]       # co si půjčil (jedna nebo víc knih)
    pujceno_v: datetime
    vraceno_v: datetime | None    # None = ještě nevrácená
```

**Pozor: výpůjčka je top-level zdroj** (`/vypujcky/{id}`), ne sub-zdroj knihy ani čtenáře. Tři důvody:

1. Má vlastní identitu (jako objednávka v pizzerii — taky není `/zakaznici/{id}/objednavky`)
2. Váže dvě entity (čtenáře a knihy) — nepatří jedné víc než druhé
3. Chceme se na ně dotazovat napříč ("všechny aktivní výpůjčky", "kdo nevrátil")

## Endpointy (10 povinných)

| #  | Metoda  | URL                      | Popis                                |
|----|---------|--------------------------|--------------------------------------|
| 1  | POST    | `/knihy`                 | Přidat knihu do katalogu             |
| 2  | GET     | `/knihy`                 | Seznam všech knih                    |
| 3  | GET     | `/knihy/{id}`            | Detail knihy                         |
| 4  | DELETE  | `/knihy/{id}`            | Smazat knihu (409 když je půjčená)   |
| 5  | POST    | `/ctenari`               | Přidat čtenáře                       |
| 6  | GET     | `/ctenari`               | Seznam čtenářů                       |
| 7  | GET     | `/ctenari/{id}`          | Detail čtenáře                       |
| 8  | POST    | `/vypujcky`              | Vytvořit výpůjčku (více knih)        |
| 9  | GET     | `/vypujcky/{id}`         | Detail výpůjčky                      |
| 10 | PUT     | `/vypujcky/{id}`         | Vrátit knihy (idempotentně!)         |

### Bonusy (pro rychlé)

| #  | Metoda  | URL                              | Popis                          |
|----|---------|----------------------------------|--------------------------------|
| B1 | GET     | `/knihy?dostupne=true`           | Filtrace knih query parametrem |
| B2 | GET     | `/ctenari/{id}/vypujcky`         | Výpůjčky konkrétního čtenáře   |

## Klíčové detaily

### POST /vypujcky — all-or-nothing

Tělo:

```json
{
    "id_ctenare": 7,
    "id_knih": [42, 17, 5]
}
```

Server zkontroluje, že **všechny** knihy existují a jsou volné:

- pokud jakákoliv kniha je už půjčená → **409 Conflict**, výpůjčka nevznikne
- pokud kterákoliv kniha neexistuje → **404 Not Found**, výpůjčka nevznikne
- jinak → **201 Created**, výpůjčka vznikne se všemi knihami najednou

Buď půjčíš všechno, nebo nic. Žádné částečné výpůjčky.

### PUT /vypujcky/{id} — idempotentní vrácení

Po dnešní hodině víš, proč PUT a ne POST/DELETE:

- **PUT je idempotentní** — druhé volání nic neudělá, vrátí stejný stav
- vrácení = výpůjčka má vyplněné `vraceno_v` (stav, ne událost)
- síť selže, klient retry → bezpečné

Chování:

- 1. volání: výpůjčka se uzavře (`vraceno_v = now()`), knihy se vrátí do katalogu, **200 OK**
- 2. volání: výpůjčka už je vrácená, no-op, **200 OK** (stejná odpověď!)
- výpůjčka neexistuje: **404**

Tělo requestu je prázdné — `PUT /vypujcky/5` říká "ať je tato výpůjčka vrácená", víc nepotřebujeme.

### Status kódy — co kde použít

| Situace                                | Status | Kdy                                   |
|----------------------------------------|--------|---------------------------------------|
| Úspěšný GET / idempotentní PUT         | 200    | Vrací data                            |
| Úspěšný POST (vznik zdroje)            | 201    | Vznikla kniha, čtenář, výpůjčka       |
| Úspěšný DELETE                         | 204    | Bez těla odpovědi                     |
| Validace selhala (špatné JSON, typ)    | 422    | **Zadarmo od pydantic!**              |
| Zdroj neexistuje                       | 404    | `/knihy/999`, `/vypujcky/999`         |
| Konflikt stavu                         | 409    | Půjčit půjčenou, smazat půjčenou      |

## Vzor — co kde okoukat z pizzerie

| Co potřebuješ                              | Kde v pizzerii                  |
|--------------------------------------------|---------------------------------|
| Pydantic model s enum                      | `models.py` — `VelikostPolozky` |
| Třída s in-memory store + čítač            | `pizzerie_impl.py` — `__init__` |
| Vlastní výjimky (`ObjednavkaNeexistuje`)   | `pizzerie_impl.py` — vrch souboru |
| Překlad výjimek na status kódy             | `main.py` — `try/except` v endpointu |
| POST endpoint s request body               | `main.py` — `vytvor_objednavku` |
| GET s path parametrem + 404                | `main.py` — `detail_objednavky` |
| Idempotentní PUT (vzor pro vrácení knihy!) | `main.py` — `zaplatit` (V2)     |

## Postup (orientační checkpointy)

Pokud se zaseknete, zeptejte se mě/spolužáka.

**~20 minut:** Modely + POST /knihy + GET /knihy + GET /knihy/{id}

> Tady je nejjednodušší pattern — jen knihy, žádná výpůjčka. Ujistěte se, že Postman vidí 201/200/404.

**~40 minut:** DELETE /knihy/{id} + čtenáři (POST, GET, GET detail)

> DELETE potřebuje 409 (když je kniha půjčená) — to budete řešit, až bude existovat výpůjčka. Můžete to teď nechat jednodušší a vrátit se k tomu později.

**~60 minut:** POST /vypujcky (all-or-nothing) + GET /vypujcky/{id}

> Zde se to zamotá nejvíc — kontrola všech knih, evidence "tahle kniha je v této výpůjčce". Pomalu, pečlivě.

**~80 minut:** PUT /vypujcky/{id} — vrácení (idempotentně!)

> Po vrácení doplnit `vraceno_v`, knihy uvolnit. Druhé volání = no-op, vrátí stejnou odpověď.

**Konec hodiny:** Aspoň minimum hotové (POST /knihy, GET /knihy, GET /knihy/{id}, POST /ctenari, POST /vypujcky). Zbytek dotáhnout doma.

## Časté zádrhele

**Server reaguje na změny pomalu / nereaguje.** V Makefile je `--reload`, takže by měl restartovat sám. Pokud ne, zabij `make run` (Ctrl+C) a spusť znovu.

**Postman vrací 422 a já tomu nerozumím.** Otevři response body — pydantic ti přesně řekne, které pole je špatně. Většinou chybějící pole nebo špatný typ.

**Mám 500 Internal Server Error.** Padá Python kód. Mrkni do terminálu, kde běží `make run` — bude tam traceback. Nejčastěji: nevyřešená výjimka, kterou jsi zapomněl přeložit v `main.py`.

**Vrácení vrací 200 i pro neexistující výpůjčku.** Idempotence se týká jen existujících zdrojů. Neexistující výpůjčka = 404, ne 200. Stejně jako u platby v pizzerii V2.

**Kniha je v `id_knih` výpůjčky, ale `dostupne=true` ji pořád vrací.** Musíš si někde držet evidenci "kniha X je momentálně půjčená". Buď flag přímo v knize (`pujcena: bool`), nebo derivace z výpůjček. Vyber si, oboje je validní.

## Reflexe (na konec hodiny)

- Kdo zvolil jaký design pro vrácení? (PUT byl doporučený, ale šly i jiné cesty.)
- Narazil někdo na situaci, kdy by se hodilo idempotentní volání? (Retry? Dvojklik?)
- Jak jste se vyrovnali s evidencí "kniha je půjčená"?

## Odevzdání

Commit do vašeho repa na konci hodiny, zbytek do příští hodiny jako DU.