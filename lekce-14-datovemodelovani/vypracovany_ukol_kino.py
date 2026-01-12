from dataclasses import dataclass, field

@dataclass
class Adresa:
    ulice: str
    mesto: str
    psc: int

@dataclass
class Sal:
    jmeno_salu: str
    kapacita: int

@dataclass
class Film:
    nazev: str
    delka_minuty: int
    zanr: str
    popis: str | None

@dataclass
class Predstaveni:
    film: Film
    sal: Sal
    cas_zacatku: str 
    cena_vstupenky: float

@dataclass
class Kino: 
    nazev: str
    adresa: Adresa
    filmy: list[Film]
    # co znamená ta lambda, probereme v další lekci, pro teď tupě opíšeme
    predstaveni: list[Predstaveni] = field(default_factory=lambda: [])
    # dávalo by smysl, aby kino mělo i seznam sálů, ale nebylo to v zadání


# Pomocné proměnné pro filmy
inception = Film(nazev="Inception", delka_minuty=148, zanr="Sci-Fi", popis="A thief who steals corporate secrets through the use of dream-sharing technology.")
godfather = Film(nazev="The Godfather", delka_minuty=175, zanr="Crime", popis="The aging patriarch of an organized crime dynasty transfers control of his clandestine empire to his reluctant son.")

# Pomocné proměnné pro sály
velky_sal = Sal(jmeno_salu="Velký sál", kapacita=200)
maly_sal = Sal(jmeno_salu="Malý sál", kapacita=100)

Svetozor = Kino(
    nazev="Kino Světozor",
    adresa=Adresa(ulice="Vodičkova 41", mesto="Praha", psc=11000),
    filmy=[
        inception,
        godfather,
    ],
    predstaveni=[
        Predstaveni(
            film=inception,
            sal=velky_sal,
            cas_zacatku="2024-07-01 19:00",
            cena_vstupenky=150.0
        ),
        Predstaveni(
            film=godfather,
            sal=maly_sal,
            cas_zacatku="2024-07-01 21:30",
            cena_vstupenky=180.0
        ),
        Predstaveni(
            film=inception,
            sal=velky_sal,
            cas_zacatku="2024-07-02 19:00",
            cena_vstupenky=150.0
        ),
        Predstaveni(
            film=godfather,
            sal=maly_sal,
            cas_zacatku="2024-07-02 21:30",
            cena_vstupenky=180.0
        ),      
    ])