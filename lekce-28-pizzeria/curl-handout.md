# Handout: Hraní si s pizzerií

Server běží na `http://<adresa>:8000` (řekne vyučující).

Můžete použít:
- **curl** v terminálu (doporučeno — uvidíte HTTP)
- **Postman** (GUI)
- **Swagger UI** na `http://<adresa>:8000/docs` (auto-generované, klikací)

## Scénář: objednávka u kasy

```bash
# 1) Karel přijde k pultu
curl -i -X POST http://<adresa>:8000/objednavky \
     -H "Content-Type: application/json" \
     -d '{"zakaznik":"Karel"}'
# Co vrátí? Jaký status? Co je v Location hlavičce?

# 2) Objedná si Margheritu velikosti L
curl -i -X POST http://<adresa>:8000/objednavky/1/polozky \
     -H "Content-Type: application/json" \
     -d '{"pizza":"Margherita","velikost":"L"}'
# Kolik to stojí?

# 3) A ještě Hawai velikosti M
curl -i -X POST http://<adresa>:8000/objednavky/1/polozky \
     -H "Content-Type: application/json" \
     -d '{"pizza":"Hawai","velikost":"M"}'

# 4) Kolik to dělá?
curl -i http://<adresa>:8000/objednavky/1
# Co všechno vidíte v odpovědi? Suma? Položky?

# 5) Karel zaplatí 500 kartou
curl -i -X POST http://<adresa>:8000/objednavky/1/platby \
     -H "Content-Type: application/json" \
     -d '{"castka":500,"zpusob":"karta"}'
# Změnil se stav? Co je v `zaplaceno_v`?

# 6) Stav po zaplacení
curl -i http://<adresa>:8000/objednavky/1
```

## Cenik

| Pizza | S | M | L |
|-------|---|---|---|
| Margherita | 130 | 160 | 190 |
| Hawai | 150 | 180 | 220 |
| Funghi | 140 | 170 | 200 |

## Schválně dělejte chyby — co server řekne?

```bash
# Neexistující objednávka
curl -i http://<adresa>:8000/objednavky/999

# Pizza, kterou nemáme v ceniku
curl -i -X POST http://<adresa>:8000/objednavky/2/polozky \
     -H "Content-Type: application/json" \
     -d '{"pizza":"Quattro Formaggi","velikost":"L"}'

# Chybějící povinné pole
curl -i -X POST http://<adresa>:8000/objednavky/2/polozky \
     -H "Content-Type: application/json" \
     -d '{"pizza":"Margherita"}'

# Zaplatit málo
curl -i -X POST http://<adresa>:8000/objednavky/2/platby \
     -H "Content-Type: application/json" \
     -d '{"castka":10,"zpusob":"karta"}'

# Přidat pizzu do už zaplacené objednávky
# (nejdřív si zaplaťte objednávku, pak zkuste přidat položku)
```

## Otázky k zamyšlení

Při hraní si všímejte:

1. **Jaké status kódy server vrací?** Jsou to ty, které jsme navrhli na tabuli?
2. **Jaké hlavičky vrací server?** Co znamená `Content-Type: application/json`?
3. **Co je v `Location` hlavičce** po vytvoření objednávky?
4. **Co když pošlete nesmysl** — server vám pomůže pochopit chybu?
5. **Co se stane, když restartujete server** (vyučující)? Co se ztratí?

## Bonus: Swagger UI

Otevřete `http://<adresa>:8000/docs` — uvidíte **automaticky vygenerovanou dokumentaci**. Můžete v ní endpointy klikat. **Vyučující nic nepsal**, FastAPI to vyrobil z typů.
