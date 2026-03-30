# Turniket REST API

Ukázková mikroslužba turniketu pro skiareál, postavená na frameworku FastAPI. Služba umožňuje ověřit platnost skipasu (RFID) a zobrazit log přístupů.

## Endpointy

- `GET /health` — kontrola stavu služby
- `GET /turniket/vpustit?rfid=<rfid>` — ověření skipasu a záznam přístupu
- `GET /turniket/log` — výpis logu všech přístupů

## Spuštění

Příprava prostředí:

```bash
make prepare
```

Spuštění serveru:

```bash
make run
```

Alternativně objektová varianta API:

```bash
make run-obj
```

Server poběží na `http://localhost:8000`. Automatická dokumentace (Swagger UI) je dostupná na `http://localhost:8000/docs`.
