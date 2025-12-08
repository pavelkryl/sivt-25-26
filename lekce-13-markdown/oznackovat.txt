Rozbor kódu: Modul pro správu studentů

Dnes se podíváme na řešení vaší úlohy, které demonstruje, jak v Pythonu efektivně spravovat a organizovat data. Tento kód je skvělým příkladem, jak modulární přístup a správné datové struktury (jako je slovník pro rychlé vyhledávání) vedou k přehlednému a výkonnému kódu.


1. Architektura a Datové struktury

Váš kód používá tři klíčové prvky pro organizaci dat a chování:

A. Třída Student (dataclass)

Proč dataclass? Zjednodušuje vytváření třídy, jejíž hlavní účel je držet data. Automaticky generuje metody jako __init__, __repr__ a __eq__.

Validace (__post_init__): Tato speciální metoda se volá po inicializaci. Zajišťuje, že data, se kterými pracujeme, jsou vždy validní (např. jméno není prázdné a obor je správný Enum).

B. Enum Obor

Proč Enum? Zajišťuje, že hodnota oboru bude vždy pocházet z definovaného seznamu (INFORMATIKA, MATEMATIKA...). Tím se vyhnete překlepům.

C. Globální stav modulu

Kód používá modulární (globální) stav držený v privátních proměnných:
  x _studenti: List[Student]: Seznam pro uchování všech studentů, užitečný pro iteraci.
  x _mapa_podle_rc: Dict[str, Student]: Slovník (hash mapa), kde klíčem je unikátní rodné číslo.


2. Optimalizace a Výkon

Tento přístup s dvěma datovými strukturami je zvolen záměrně pro výkon.

x Efektivní vyhledávání: Funkce najdi_studenta_podle_rc(rc) využívá slovník _mapa_podle_rc. Vyhledávání ve slovníku probíhá v průměrném čase O(1) (konstantní čas), což znamená, že rychlost vyhledání nezávisí na počtu studentů. 
x Příklad najdi_studenty_se_stejnym_jmenem: Zde je vidět, jak slovník slouží k agregaci dat. Projdeme seznam jednou a vkládáme studenty do slovníku, kde klíčem je normalizované jméno.

---

3. Úkol: Implementace a Testování

Cíl je pochopit a úspěšně spustit příklad použití:

1. Stáhněte nebo zkopírujte kód do souboru (např. uloha_1_studenti.py).
2. Spusťte soubor a ověřte, že výstup odpovídá očekávané logice:
    x Jsou správně vypsáni studenti informatiky?
    x Byla správně nalezena duplicita jména "Jan Novák"?
    x Funguje vyhledávání podle RC (najdi_studenta_podle_rc)?
3. Bonus: Zkuste implementovat novou funkci:
    x pocet_studentu_dle_oboru() -> Dict[Obor, int]: Funkce, která vrátí slovník, kde klíčem je Obor a hodnotou je počet studentů v daném oboru.
4. Commit: Po dokončení a ověření funkčnosti nezapomeňte na git add, git commit a git push.
