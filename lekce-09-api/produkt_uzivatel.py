from produkt_api import *

produkty = [
    Produkt("sekacka", 12000, Kategorie.ELEKTRONIKA),
    Produkt("tricko", 500, Kategorie.OBLECENI),
    Produkt("hrnek", 200, Kategorie.NADOBI),
    Produkt("vysavac", 3500, Kategorie.ELEKTRONIKA),
    Produkt("notebook", 25000, Kategorie.ELEKTRONIKA),
    Produkt("mikrovlnka", 4500, Kategorie.ELEKTRONIKA),
    Produkt("dziny", 1200, Kategorie.OBLECENI),
    Produkt("bunda", 2800, Kategorie.OBLECENI),
    Produkt("talir", 150, Kategorie.NADOBI),
    Produkt("panci", 800, Kategorie.NADOBI),
    Produkt("sluchatka", 1500, Kategorie.ELEKTRONIKA),
    Produkt("kosile", 900, Kategorie.OBLECENI),
    Produkt("sklenice", 80, Kategorie.NADOBI),
    Produkt("mys", 400, Kategorie.ELEKTRONIKA),
]

init_produkty(produkty)

p = vyhledej_produkt("vysavac")
print("vysavac:", p)

p = vyhledej_produkt("lzicka")
print("lzicka:", p)

pridej_produkt(Produkt("lzicka", 50, Kategorie.NADOBI))

p = vyhledej_produkt("lzicka")
print("lzicka:", p)
