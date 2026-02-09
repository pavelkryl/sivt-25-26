# Lekce 19 - Modulární programování: Turniket

Tento repozitář obsahuje ukázky kódu z lekce 19 o modulárním programování, zaměřené na simulaci turniketu.

## Shrnutí naučené látky

- modul
- API
- stavovost (stateful)/bezestavovost (stateless)

## Jednotlivé úlohy a jejich komentáře

### `turniket.py`
Nejjednodušší implementace logiky turniketu. Udržuje seznam platných RFID kódů pro skipasy (`_platne_skipasy`). Poskytuje základní funkce:
- `vpustit(rfid: str)`: Zkontroluje, zda je dané RFID v seznamu platných pasů.
- `reset()`: Vynuluje seznam platných pasů.
- `iniciace(skipasy: list[str])`: Inicializuje seznam platných pasů.
- `pridej(zakoupeny_skipas_rfid: str)`: Přidá nový ski pas do seznamu platných.

### `turniket_log_pristupu.py`
Rozšiřuje funkčnost `turniket.py` o možnost logování všech pokusů o přístup. Zavádí datový model `Pristup` (pomocí `pydantic.BaseModel`), který ukládá:
- `rfid`: RFID kód použitého pasu.
- `cas_pristupu`: Čas, kdy k pokusu o přístup došlo.
- `povoleno`: Boolean hodnota indikující, zda byl přístup povolen.

Funkce `vpustit` byla upravena tak, aby po každém pokusu o přístup zapsala záznam do interního seznamu `_log_pristupu`. Byla také přidána funkce `log_vstupu()`, která vrací celý záznam přístupů. Tento soubor demonstruje, jak lze přidat další funkcionalitu (zde logování) bez zásadní změny základní logiky turniketu.

### `turniket_multi.py`
Ukazuje, jak spravovat více instancí turniketu nezávisle na sobě. Zde je zaveden datový model `Turniket` (opět pomocí `pydantic.BaseModel`), který sdružuje:
- `nazev`: Název turniketu.
- `platne_skipasy`: Seznam platných pasů specifických pro tento turniket.
- `log_pristupu`: Seznam logů přístupů specifických pro tento turniket.

Všechny funkce (`vpustit`, `reset`, `iniciace`, `pridej`, `log_vstupu`) byly upraveny tak, aby přijímaly instanci `Turniket` jako první argument. Tím se kód stává modulárnějším a umožňuje snadné vytváření a správu několika turniketů, každý s vlastním stavem a logem, což je klíčový princip objektově orientovaného programování.
