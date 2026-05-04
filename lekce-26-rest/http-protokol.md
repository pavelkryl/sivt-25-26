# Lekce 25 — HTTP protokol: textová konverzace po TCP

**Téma**: Co je to HTTP. Na čem stojí, jak vypadá, jak si ho můžu sáhnout rukama. Navazuje na netcat z lekce 24 ("primitivní server/klient").

**Cíl hodiny**: studenti odejdou s pochopením, že:
- HTTP je **text** posílaný přes TCP — žádná magie,
- request a response mají definovanou strukturu (metoda, URL, hlavičky, tělo / status, hlavičky, tělo),
- status kódy říkají "kdo udělal chybu a jak moc" (2xx/3xx/4xx/5xx),
- URL má strukturu (schema, host, port, path, query),
- HTTP metody existují (GET, POST, PUT, DELETE) a každá má jinou roli — detaily příště.

**Pointa hodiny**: studenti si ručně napíšou HTTP request přes netcat a dostanou od reálného serveru odpověď. Tohle je "aha" moment, na kterém pak staví všechno ostatní.

---

## Proč tahle hodina předchází REST

V lekci 24 jsme studentům ukázali turniket API, ale HTTP pod tím jsme brali jako samozřejmost. Oni opsali `@app.get(...)` ze vzoru a úloha fungovala. Ale nevědí:

- **Co ten GET doopravdy je.** Sloveso? Anotace? Jen řetězec?
- **Proč se parametr `rfid` posílá za otazníkem.** Je to Python proměnná? Co to dělá?
- **Co se stane na síti.** Prohlížeč/curl pošle cosi, server vrátí cosi. Jak přesně to vypadá?

Bez těchto základů jim REST (další hodina) splyne s "nějakými Python funkcemi, co se volají přes internet". Dneska jim ukážeme, že HTTP je **textová konverzace přes socket** — a REST je jen **dohoda, jak v té konverzaci mluvit smysluplně**.

---

## Plán hodiny (110 min = 2× 45 + přestávka)

### 0–10 min — Motivace: jak si spolu dva počítače povídají?

**Otázka na úvod:**

> "Když napíšu do prohlížeče `example.com` a zmáčknu Enter, co se stane? Ne obecně — technicky. Co putuje po síti?"

Odpovědi budou různé ("nějaký request", "pošle se to serveru", "použije se HTTP..."). Veď je k tomu, že **odpověď nikdo přesně neví**, protože HTTP je obvykle schované za prohlížečem nebo knihovnou. Dneska tohle odkryjeme.

**Navázání na lekci 24:** Minule jsme povídali dvě netcat instance — jeden server poslouchal, druhý se připojil, něco jsme si napsali. HTTP je **přesně tohle**, jen s dohodnutým formátem zpráv.

### 10–25 min — HTTP je text. Ukaž curl -v.

Pusť u tabule:

```bash
curl -v http://example.com
```

Oni uvidí něco jako:

```
* Connected to example.com (93.184.216.34) port 80
> GET / HTTP/1.1
> Host: example.com
> User-Agent: curl/8.5.0
> Accept: */*
>
< HTTP/1.1 200 OK
< Content-Type: text/html; charset=UTF-8
< Content-Length: 1256
< Date: Mon, 20 Apr 2026 09:15:33 GMT
<
<!doctype html>
<html>
...
```

**Co zdůraznit:**

- **`>` je to, co curl posílá.** `<` je to, co přijímá. Šipky ukazují směr.
- **První řádek requestu: `GET / HTTP/1.1`** — metoda, cesta, verze. Nic jiného.
- **První řádek responsu: `HTTP/1.1 200 OK`** — verze, status kód, lidská hláška.
- **Hlavičky jsou `klíč: hodnota`** na zvláštních řádcích, oddělené od těla prázdným řádkem.
- **Po prázdném řádku jde tělo** (u requestu volitelné, u GET obvykle žádné).

Klíčový moment: **"Tohle je celý HTTP. Žádné binární formáty, žádné schované metody, žádná magie. Je to jen text, na kterém se dva počítače dohodly, jak ho číst."**

### 25–35 min — Struktura requestu a responsu

Nakresli na tabuli (nech tam viset celou hodinu):

```
REQUEST                                RESPONSE
════════                               ═════════
METODA CESTA VERZE                     VERZE STATUS HLÁŠKA
Hlavička: hodnota                      Hlavička: hodnota
Hlavička: hodnota                      Hlavička: hodnota
Hlavička: hodnota                      Hlavička: hodnota
                                       
[tělo, volitelně]                      [tělo, volitelně]

příklad:                               příklad:
GET /index.html HTTP/1.1               HTTP/1.1 200 OK
Host: example.com                      Content-Type: text/html
Accept: text/html                      Content-Length: 1256
                                       
(žádné tělo)                           <!doctype html>...
```

**Dvě věci, které si mají zapamatovat:**

1. **Prázdný řádek odděluje hlavičky od těla.** Kritické, HTTP to tak má.
2. **Každý řádek končí `\r\n`** (ne jen `\n`). Nemusí to dneska detailně řešit, ale ať to vědí — bude to důležité při ručním psaní přes netcat.

### 35–50 min — URL jako adresa

Rozepiš na tabuli kompletní URL:

```
https :// example.com : 443 / cesta/k/veci ? param=hodnota&b=c # fragment
 └─┬─┘    └────┬────┘   └┬┘  └──────┬─────┘  └───────┬───────┘  └───┬──┘
schema     host       port    path            query           fragment
```

**Projdi po částech:**

- **Schema** (`http`, `https`) — jakým protokolem mluvíme. `https` je `http` přes TLS.
- **Host** — kterou mašinu kontaktujeme. Jméno (přes DNS) nebo IP.
- **Port** — na kterém portu ta mašina poslouchá. Default 80 pro http, 443 pro https. Můžeš vynechat, když je default.
- **Path** — co v rámci serveru chceme. Tohle je to, co pak skončí jako `GET /cesta/k/veci`.
- **Query** — parametry za otazníkem. `?klic=hodnota&druhy=jiny`. **Tady mají aha moment k `/vpustit?rfid=X` z lekce 24** — tohle je ten query string.
- **Fragment** — za `#`. Zajímavost: **fragment se neposílá na server**, zpracovává ho jen prohlížeč (skok na anker na stránce). Často tohle studenti neví.

**Mini-úkol pro vlastní ruku** (5 min):

```bash
curl -v "http://httpbin.org/get?jmeno=karel&vek=20"
```

Nech je podívat se do výstupu, co server vidí a vrací. `httpbin.org` je skvělý — echo server, který ti vrátí přesně to, co jsi poslal.

### 50–55 min — Přestávka

### 55–80 min — **Ruční HTTP přes netcat (hlavní pointa hodiny)**

Tohle je "aha" hodina. Studenti si napíšou HTTP request **rukou** a pošlou ho skutečnému serveru.

**Postup:**

1. Spustí netcat jako klient na port 80:
   ```bash
   nc example.com 80
   ```
2. Napíšou **přesně** tohle (pozor na prázdný řádek na konci!):
   ```
   GET / HTTP/1.1
   Host: example.com
   
   ```
3. Zmáčknou Enter po prázdném řádku.
4. Server odpoví HTML stránkou přímo do terminálu.

**Co zdůraznit, než je pustíš:**

- **Po posledním řádku hlaviček musí být PRÁZDNÝ řádek.** Je to signál "konec hlaviček". Bez něj server čeká a nic se nestane.
- **Hlavička `Host:` je povinná v HTTP/1.1.** Jeden server může hostovat víc webů na stejné IP, tak musí vědět, který chceš.
- **Nic jiného nepotřebujete.** Žádné `User-Agent`, žádné `Accept`. HTTP je tolerantní.

**Zádrhele, na které připrav:**

- Studenti pošlou request a nic se nestane → chybí prázdný řádek. Nech je to objevit.
- Napíšou `GET example.com/ HTTP/1.1` místo `GET /` → server vrátí 400. Hezký moment ukázat "jo, server si stěžuje".
- Napíšou `GET / HTTP/2` → server řekne "neumím". Ukaž jim, že verze je součást dohody.

**Bonus (pokud zbývá čas ve dvojicích):**

Ať jeden student dělá server (`nc -l 1234`) a druhý klient (`nc localhost 1234`). Klient napíše HTTP request, server ho uvidí v plain textu. Teď student-server ručně odpoví HTTP responsem:

```
HTTP/1.1 200 OK
Content-Type: text/plain
Content-Length: 12

Ahoj svete!
```

**Tohle je moment, kdy se studentům rozsvítí, že HTTP server není nic víc než program, co umí odpovědět tímto formátem.** Pak pochopí, že FastAPI jim dělá jen to, co by mohli napsat i ručně — jen automaticky.

### 80–95 min — Status kódy a metody (přehledově)

**Status kódy — jen rodiny**. Na tabuli:

```
2xx  — OK, povedlo se           (200 OK, 201 Created, 204 No Content)
3xx  — koukni jinam             (301 Moved Permanently, 302 Found)
4xx  — TY jsi udělal chybu      (400 Bad Request, 404 Not Found, 403 Forbidden)
5xx  — JÁ jsem udělal chybu     (500 Internal Server Error, 503 Service Unavailable)
```

Řekni jim: **"Rodiny si zapamatujte, konkrétní kódy naberete postupně."** Každý kód má na [httpstatuses.com](https://httpstatuses.com) vlastní stránku s vysvětlením.

**Zajímavost, co studenty baví:**
- **418 I'm a teapot** — reálný status kód, aprílový vtip z roku 1998, který zůstal v RFC.
- **451 Unavailable For Legal Reasons** — odkaz na Fahrenheit 451. Používá se, když obsah blokuje soud.

**Metody — jen seznam.** Na tabuli:

```
GET     — "dej mi"
POST    — "tady máš něco nového"
PUT     — "ať tady je tohle"
DELETE  — "smaž to"
HEAD    — jako GET, ale jen hlavičky (bez těla)
OPTIONS — "co tahle URL umí?"
PATCH   — "změň část"
```

**Řekni jim:** "Každá metoda má svoji roli, ale **detailní pravidla si necháme na příště**, kdy budeme navrhovat vlastní API (REST). Pro dnešek stačí, že existují a každá něco trochu jiného znamená."

**Malá demonstrace, co je akorát:**

```bash
curl -X HEAD -v http://example.com      # jen hlavičky, bez HTML
curl -X OPTIONS -v http://example.com   # server řekne, co umí
```

Tohle není plýtvání časem — studenti vidí, že `curl -X` = "použij tuhle metodu" a že existují jiné metody než jen GET.

### 95–105 min — Mini úkol: prozkoumejte turniket z lekce 24 přes curl

Ať si studenti pustí svůj (nebo tvůj) turniket server z minula a **koukají, co po síti letí**. Zadání:

```bash
# Spusť server z lekce 24
uvicorn turniket_api:app

# V druhém terminálu zkoušej:
curl -v http://localhost:8000/health
curl -v "http://localhost:8000/turniket/vpustit?rfid=AAA111"
curl -v http://localhost:8000/turniket/log
```

**Otázky pro ně** (ať se nad tím zamyslí, v reflexi probereme):

1. Jaký status kód vrací `/health`?
2. Co přesně je v `Content-Type` odpovědi?
3. Kde v requestu je `rfid`? (V query stringu — teď už to umíme pojmenovat.)
4. Kdybys `rfid` dal do těla místo do query, jak by request vypadal? (Nezkoušet, jen přemýšlet.)

### 105–110 min — Reflexe a shrnutí

Tři otázky:

1. **"Kolik souborů byste museli stáhnout, aby HTTP server fungoval?"**  
   Cílová odpověď: HTTP je text, server je program, co umí poslat a přijmout ten text po TCP. Nic víc není potřeba. FastAPI/nginx/Apache jsou jen *pohodlné* programy, ale ručně bychom si ho taky napsali.

2. **"Proč je prázdný řádek mezi hlavičkami a tělem?"**  
   Cílová odpověď: Aby server věděl, kde končí hlavičky. Jinak by nemohl rozpoznat, co je metadata a co už je obsah.

3. **"Co znamená `404`?"**  
   Cílová odpověď: Klient si řekl o něco, co neexistuje. Chyba na straně klienta (4xx rodina).

**Teaser na příští hodinu:**

> "Dneska jsme viděli, že HTTP má metody GET, POST, PUT, DELETE. Příště si řekneme, **proč která kdy** — a uvidíte, že z toho plyne, jak navrhnout dobré API. A vrátíme se k turniketu — uvidíme, že `GET /vpustit?rfid=X` je vlastně podezřelé, a uděláme ho líp."

---

## Mini teorie na tabuli (nech viset celou hodinu)

```
════════ HTTP REQUEST ════════       ════════ HTTP RESPONSE ═══════
METODA CESTA VERZE                   VERZE STATUS HLÁŠKA
Host: hodnota                        Content-Type: hodnota
Content-Type: hodnota                Content-Length: číslo
                                     
[tělo]                               [tělo]


STATUS RODINY                        URL STRUKTURA
─────────────                        ─────────────
2xx  OK                              schema://host:port/path?query#fragment
3xx  Jinam
4xx  Klient pokazil                  Příklad:
5xx  Server pokazil                  https://example.com:443/api?x=1
```

---

## Curl handout pro studenty

```bash
# ============================================
# HTTP OCHUTNÁVKA — co letí po síti
# ============================================

# 1) Jednoduché GET, ukáže se request i response
curl -v http://example.com

# 2) Jen hlavičky, bez těla
curl -v -X HEAD http://example.com

# 3) Co server umí? (OPTIONS)
curl -v -X OPTIONS http://example.com

# 4) Query parametry (httpbin vrátí, co jsi poslal)
curl -v "http://httpbin.org/get?jmeno=karel&vek=20"

# 5) POST s tělem
curl -v -X POST http://httpbin.org/post \
     -H "Content-Type: application/json" \
     -d '{"ahoj":"svete"}'

# 6) Různé status kódy na vyzkoušení
curl -v http://httpbin.org/status/200
curl -v http://httpbin.org/status/404
curl -v http://httpbin.org/status/500

# 7) Přesměrování (3xx — všimni si 'Location:' hlavičky)
curl -v http://httpbin.org/redirect/1

# ============================================
# RUČNÍ HTTP PŘES NETCAT
# ============================================

# 8) Najdi si čistou stránku přes nc:
nc example.com 80
# Pak napiš (PŘESNĚ, včetně prázdného řádku!):
GET / HTTP/1.1
Host: example.com

# (prázdný řádek + Enter)

# 9) Ve dvojici si udělejte vlastní server
# Student A (server):
nc -l 1234

# Student B (klient):
nc localhost 1234
# Pak napiš:
GET /cokoliv HTTP/1.1
Host: cokoliv

# Student A odpoví RUČNĚ:
HTTP/1.1 200 OK
Content-Type: text/plain
Content-Length: 12

Ahoj svete!
```

---

## Poznámky pro sebe

- **Nepouštěj se do TCP detailů.** Studenti nemusí vědět, co je three-way handshake, ACK, nebo window size. Stačí "HTTP běží po TCP, TCP zajišťuje, že zprávy dorazí celé a ve správném pořadí". Pokud se někdo zeptá na detail, nadšeně ho odkaž do sítí na VŠ.

- **netcat na Windows může být mrcha.** Pokud jsou studenti na WSL/Linuxu, problém není. Na čistém Windows může být potřeba nainstalovat `ncat` z Nmap balíčku, nebo použít PowerShell ekvivalent. Ověř si předem, ať na tom neshoříš u tabule.

- **`httpbin.org` je pomocný** — je to live "echo server" pro HTTP, který ti vrátí přesně to, co jsi poslal. Super na demo. Alternativa: `httpbingo.org` (aktivnější udržovaná).

- **Nesnaž se o kompletnost.** Hlaviček jsou stovky, status kódů desítky, a každý má svůj nuance. Dneska se nesnaž nic dotáhnout do kompletnosti — stačí, že si studenti odnesou **mentální model** HTTP jako textové konverzace. Detaily jim doplníš, když budou potřeba.

- **Ne-cílem dneška je REST.** Opravdu tam nechoď. Když se někdo zeptá "proč tedy `GET /vpustit` ne?" řekni "skvělá otázka, přesně na ní budeme příští hodinu začínat". Vybuduj očekávání.

- **Když zbývá čas**, nech studenty zkusit poslat na server něco, čemu nerozumí, a kouknout, jak odpoví. Třeba `BANANA / HTTP/1.1` nebo `GET / HTTP/9.9`. Reakce serveru (400 Bad Request, 505 HTTP Version Not Supported) jsou poučné a studenty to baví.

- **Ruční HTTP přes netcat je srdce hodiny.** Kdyby se cokoli ubíralo, zachovej tohle. Je to ten moment, kdy HTTP přestane být abstraktní.

---

## Co se do hodiny nevešlo (a je to tak dobře)

- **HTTPS/TLS detaily** — zmiň, že existuje ("https je http přes šifrované spojení"), ale nepouštěj se do certifikátů, SNI, handshake. Samostatné téma na jindy.
- **HTTP/2, HTTP/3, QUIC** — pokud někdo slyšel, zmiň existenci, ale detaily vynech. Pro pochopení REST stačí HTTP/1.1.
- **Cookies, sessions, autentikace** — velký vlastní blok. Teď by jen přetáhly hodinu.
- **Cache hlavičky** (`Cache-Control`, `ETag`, ...) — související s GET a idempotencí, ale detailněji až v REST hodinách.
- **CORS** — Content-Security-Policy, preflight requesty, ... samostatné téma, jen pokud se dostanou k tomu, že píšou frontend.
- **REST konkrétně** — to je příští hodina, dneska ne.