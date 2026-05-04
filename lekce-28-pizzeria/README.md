# Pizzerie API

Vyukova implementace REST API pro pizzerii. Demonstruje:

- **Oddeleni vrstev**: interni business logika vs. REST API
- **Pydantic modely** pro request/response validaci
- **HTTP status kody** (201, 404, 409, 422, 400)
- **In-memory store** (po restartu se data ztrati)

## Struktura

```
pizzerie/
├── models.py          # pydantic modely (sdilene mezi vrstvami)
├── pizzerie_impl.py   # interni API pizzerie (business logika)
├── main.py            # REST API (tenka obalujici vrstva)
└── README.md
```

**Architektura ve vrstvach:**

```
HTTP klient (curl, Postman, prohlizec)
        │
        ▼
   main.py             ← REST API: HTTP + status kody
        │
        ▼
 pizzerie_impl.py      ← Business logika: bez HTTP
        │
        ▼
    models.py          ← Datovy model
```

Tahle separace umoznuje:
- testovat business logiku bez HTTP
- vymenit REST za GraphQL/gRPC bez prepisu logiky
- mit nad jednou logikou nekolik API soucasne

## Instalace

```bash
make prepare
```

## Spusteni

```bash
make run
```

Otevre se na `http://localhost:8000`.

Automaticky generovana dokumentace: `http://localhost:8000/docs`

## Endpointy

| Metoda | URL | Popis |
|--------|-----|-------|
| POST   | `/objednavky` | Vytvorit objednavku |
| GET    | `/objednavky` | Seznam vsech objednavek |
| GET    | `/objednavky/{id}` | Detail objednavky |
| POST   | `/objednavky/{id}/polozky` | Pridat pizzu |
| POST   | `/objednavky/{id}/platby` | Zaplatit |

## Priklady volani

```bash
# Vytvorit objednavku
curl -i -X POST http://localhost:8000/objednavky \
     -H "Content-Type: application/json" \
     -d '{"zakaznik":"Karel"}'

# Pridat pizzu
curl -i -X POST http://localhost:8000/objednavky/1/polozky \
     -H "Content-Type: application/json" \
     -d '{"pizza":"Margherita","velikost":"L"}'

# Zaplatit
curl -i -X POST http://localhost:8000/objednavky/1/platby \
     -H "Content-Type: application/json" \
     -d '{"castka":300,"zpusob":"karta"}'

# Detail
curl -i http://localhost:8000/objednavky/1

# Seznam vsech
curl -i http://localhost:8000/objednavky
```

## Cenik

| Pizza | S | M | L |
|-------|---|---|---|
| Margherita | 130 | 160 | 190 |
| Hawai | 150 | 180 | 220 |
| Funghi | 140 | 170 | 200 |
