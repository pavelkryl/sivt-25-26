# Pizzerie API — verze 2

Refactor V1 zaměřený na **idempotenci platby**.

## Změny oproti V1

### 1. Platba je singleton, ne kolekce

V V1 jsme měli `platby: list[Platba]` a `POST /objednavky/{id}/platby`. To naznačovalo, že plateb může být víc — což ale neodpovídá realitě.

V V2:
- `Objednavka` má `platba: Platba | None` (max jedna)
- URL je `/objednavky/{id}/platba` (singulár, **bez id platby**)
- Metoda je `PUT`, ne `POST`

### 2. Platba je idempotentní

`PUT /objednavky/{id}/platba` lze bezpečně volat opakovaně:

- **1. volání**: platba vznikne → 200 OK
- **2. volání se stejnými daty**: platba existuje → 200 OK (no-op)
- **2. volání s jinými daty**: 409 Conflict (porušení idempotence)
- **Objednávka neexistuje**: 404
- **Částka < suma**: 400

**Vždy 200, nikdy 201**. Z hlediska klienta je výsledek stejný — na daném URI je daná platba. Klient se nemusí starat, jestli ji vytvořil teď, nebo už existovala. Čistá idempotence.

### 3. Nový endpoint: GET /objednavky/{id}/platba

Dotaz, zda už je objednávka zaplacená:
- vrácená platba: 200
- ještě nezaplaceno: 404
- objednávka neexistuje: 404

## Endpointy

| Metoda | URL                            | Popis                              |
|--------|--------------------------------|------------------------------------|
| POST   | `/objednavky`                  | Vytvořit objednávku                |
| GET    | `/objednavky`                  | Seznam objednávek                  |
| GET    | `/objednavky/{id}`             | Detail objednávky                  |
| POST   | `/objednavky/{id}/polozky`     | Přidat položku                     |
| PUT    | `/objednavky/{id}/platba`      | **Zaplatit (idempotentně)**        |
| GET    | `/objednavky/{id}/platba`      | **Stav platby**                    |

## Příklady volání

```bash
# Vytvořit objednávku
curl -i -X POST http://localhost:8000/objednavky \
     -H "Content-Type: application/json" \
     -d '{"zakaznik":"Karel"}'

# Přidat pizzu
curl -i -X POST http://localhost:8000/objednavky/1/polozky \
     -H "Content-Type: application/json" \
     -d '{"nazev":"Margherita","velikost":"velka"}'

# Zaplatit - 1. volání: 200 OK
curl -i -X PUT http://localhost:8000/objednavky/1/platba \
     -H "Content-Type: application/json" \
     -d '{"castka":300,"zpusob":"karta"}'

# Zaplatit - 2. volání STEJNÁ DATA: 200 OK (idempotentní no-op)
curl -i -X PUT http://localhost:8000/objednavky/1/platba \
     -H "Content-Type: application/json" \
     -d '{"castka":300,"zpusob":"karta"}'

# Zaplatit - 2. volání JINÁ DATA: 409 Conflict
curl -i -X PUT http://localhost:8000/objednavky/1/platba \
     -H "Content-Type: application/json" \
     -d '{"castka":500,"zpusob":"hotove"}'

# Detail platby
curl -i http://localhost:8000/objednavky/1/platba
```

## Spuštění

```bash
make prepare    # jednou
make run        # spustí server
```

Server běží na `http://localhost:8000`, dokumentace na `/docs`.
