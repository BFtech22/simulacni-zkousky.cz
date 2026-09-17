# www.simulacni-zkousky.cz

Specializovaný web BFK Systems s.r.o. na **ověřování souladu výroben s RfG** —
simulace souladu, zkoušky na místě, dokumentace a jednání s provozovateli
distribučních soustav. Statický web bez backendu.

Barvy a typografii sdílí s cenovou nabídkou BFK (`../bfk_nabidka_html`): Roboto,
oranžová `#F08A00`, tmavě šedá `#3C3C3C`. Rozvržení a komponenty vycházejí
z webu `../bftechnology`, obsah z interní rešerše (viz `podklady/`).

**Písmo Roboto je hostované na webu** (`assets/fonts/`, variabilní woff2 z Google Fonts v51,
tloušťky 300–900, licence SIL Open Font License 1.1 — plný text je v repozitáři
google/fonts, složka `ofl/roboto`). Stránky nevolají fonts.googleapis.com ani
fonts.gstatic.com, takže se při načtení webu nepředává IP adresa Googlu. Hlídá to
`kontrola.py` — externí font, styl nebo skript je chyba.

## Stránky se GENERUJÍ — needituj `.html` v kořeni

Web má 19 stránek se stejnou hlavičkou, patičkou a menu. Ruční kopie hlavičky
v každém souboru (jako na webu BF technology) se neuhlídá, takže:

```bash
python3 nastroje/build.py      # vygeneruje všechny .html + sitemap.xml
python3 nastroje/kontrola.py   # odkazy, meta, JSON-LD, sitemap, zastaralé formulace, data aktualizace
python3 nastroje/kontrola.py --externi    # navíc ověří externí odkazy (chodí na síť)
python3 nastroje/kontrola.py --produkce   # před každým pushem: bez PLACEHOLDER, robots bez Disallow, CNAME
```

`kontrola.py` má seznam `ZAKAZANE` — formulace, které se v minulých kolech oprav na web
vracely (ÚPOS, „víc“, „stejných hranic“, „30 až 75 MW“…). Když se opraví další chyba,
kterou nechceme vidět znovu, přidej ji tam.

**Obsah stránek je v `nastroje/obsah.py`**, šablona a menu v `nastroje/build.py`.
Když upravíš vygenerovaný `.html` v kořeni, další build to přepíše.

```
.
├── nastroje/
│   ├── obsah.py            # ← TADY se edituje obsah (1 položka STRANKY = 1 stránka)
│   ├── build.py            # šablona, menu, patička, sitemap
│   ├── kontrola.py         # kontrola před publikací (viz výš)
│   └── generuj-obrazky.py  # zmenšeniny a WebP z originálů v assets/
├── assets/
│   ├── style.css           # všechny styly (převzato z webu BFT, přebarveno)
│   ├── nav.js              # rozbalovací menu + mobilní menu
│   ├── form.js             # odeslání poptávkového formuláře
│   ├── fonts/              # Roboto, variabilní woff2 (latin + latin-ext) — hostujeme sami
│   ├── logo_SZ.png         # ZDROJ loga webu (originál, stránky ho nenačítají)
│   ├── logo-sz-300/600.*   # logo webu pro hlavičku a patičku (generované)
│   ├── bfk-logo*, bfk-znacka-*  # logo a značka BFK Systems (generované)
│   ├── favicon.png         # oranžový čtverec s fajfkou (kreslený skriptem)
│   └── title-photo*        # titulní fotka (hero, pozadí kontaktu)
├── podklady/               # interní rešerše (v .gitignore, nepublikuje se)
├── index.html … 404.html   # GENEROVANÉ, needitovat
├── sitemap.xml             # GENEROVANÁ buildem
├── robots.txt              # povoluje indexaci, odkazuje na sitemap
└── CNAME                   # vlastní doména pro GitHub Pages, viz Provoz
```

## Loga

Logo webu je originál v `assets/logo_SZ.png`. Skript `nastroje/generuj-obrazky.py`
z něj udělá ořez bez bílého okraje, průhledné pozadí a zmenšeniny
`logo-sz-300/600.png|webp`, na které se odkazuje hlavička i patička.
**Po výměně originálu skript spusť znovu**, jinak zůstanou staré varianty.

Vazba na provozovatele: v hlavičce je za svislou čarou **celé logo BFK Systems**
(samotná čtvercová značka bez nápisu nikomu neřekne, čí web to je), v patičce logo
webu a pod ním logo BFK s popiskem „Web provozuje".

Favicon je oranžový čtverec s bílou fajfkou (kreslí ho stejný skript) — celá
značka s monitorem je v 16 px nečitelná.

## Hlavička a šířky

Do hlavičky se musí vejít logo webu (50 px vysoké), logo BFK (46 px — zhruba stejně výrazné
jako logo webu), šest položek menu a tlačítko. Nejtěsněji je při 1081 px, kde mezi logy
a menu zbývá asi 60 px. Na telefonech je logo BFK menší: 401–480 px 40 px, do 400 px 36 px
(a logo webu 40 px) — jinak by se u běžných 412px telefonů přiblížilo k hamburgeru.
Místo se uvolňuje po krocích:

| Šířka okna | Hlavička |
|---|---|
| do 1080 px | hamburger (menu i tlačítko v rozbalovacím panelu) |
| 1081–1240 px | loga, plné menu, zkrácené tlačítko „Poptávka" |
| 1241–1400 px | k tomu dlouhé „Nezávazná poptávka" |
| od 1400 px | navíc popisek „provozuje" před logem BFK |

Pozor při ladění: `body` má `overflow-x: hidden`, takže **příliš široká hlavička
nezpůsobí vodorovný posuvník** — jen se menu překryje s logem a pravá položka se
ořízne. Kontroluje se to porovnáním šířky loga a menu proti šířce hlavičky, ne
testem posuvníku. Počítej i s tím, že než se načte Roboto, kreslí se náhradní
Arial, který je asi o 6 % širší.

## Struktura webu

**13. 9. 2026 zkráceno zhruba na polovinu** — kolegům byl web příliš obsáhlý
(27 stránek → 19, text na 55 % původního). Zkoušky se popisují jen po okruzích
(činný výkon, jalový výkon, ochrany, dálkové řízení, opětovné připojení, baterie),
protože rozsah stejně určuje smlouva o připojení.

| Menu | Stránky |
|---|---|
| Kategorie ▾ | `kategorie-a1`, `-a2`, `-b1`, `-b2`, `-c-d`, `bateriova-uloziste-zue`, `pridani-baterie-k-fve` |
| Distributoři ▾ | `cez-distribuce`, `egd`, `predistribuce` |
| Služby ▾ | `simulace-souladu`, `zkousky-na-miste` |
| Postup | `proces-pripojeni` (UPOS, seznam a)–j), lhůty, DVM, UTP, podklady — kotvy `#upos`, `#podklady`) |
| Reference, Kontakt | `reference`, `kontakt` |
| mimo menu | `index`, `faq`, `zasady-zpracovani-osobnich-udaju`, `404` |

Vypadly technické detaily: slovník, rozpadové místo, RTU, zkoušky ochran, katalogy
zkoušek 5.1–5.11 a simulací 6.1–6.19, samostatné stránky UPOS/UTP/DVM/podklady.
**Podrobná verze je v gitu pod commitem `c9d4806`.**

Zkratky **UPOS** a **UTP** se píšou bez čárky, stejně jako v PPDS příloze 4.
Nadpisy sekcí, eyebrow a nadpisy karet se sázejí verzálkami — **jednotky a „A1 a A2“
do nich nepatří** (vzniká „KW“, „A1 A A2“); čísla patří do textu nebo do H1.

Každá stránka má drobečkovou navigaci (i jako JSON-LD `BreadcrumbList`),
kanonickou URL a Open Graph. Stránky s akordeonem dotazů mají navíc JSON-LD
`FAQPage`.

## Provoz (spuštěno 17. 9. 2026)

- **Hosting:** GitHub Pages z větve `main`, vlastní doména `www.simulacni-zkousky.cz`
  (soubor `CNAME`), HTTPS vynucené. Holou doménu `simulacni-zkousky.cz` přesměrovává
  GitHub na `www`, stejně jako starou adresu `bftech22.github.io/simulacni-zkousky.cz/`.
  Doména je v účtu GitHubu ověřená (TXT záznam `_github-pages-challenge-BFtech22`),
  takže ji nikdo jiný nemůže použít pro své stránky.
- **DNS spravuje Webglobe:** čtyři záznamy `A` (185.199.108.153 až 185.199.111.153),
  čtyři `AAAA` (2606:50c0:8000::153 až 2606:50c0:8003::153) a `CNAME www` → `bftech22.github.io`.
  MX záznamy a zástupný záznam `*` zůstaly od Webglobe beze změny.
- **Doména bez pomlčky `simulacnizkousky.cz`** jen přesměrovává na tenhle web — má
  vlastní repozitář `BFtech22/simulacnizkousky.cz` a stejné DNS. Přesměrování přímo
  od Webglobe se nepoužilo, protože bez hostingu funguje jen přes http.
- **Formulář** odesílá přes Web3Forms (klíč v `FORMULAR` v `nastroje/obsah.py`)
  na `simulace@bfksystems.cz`. Bezplatný tarif má 250 odeslání měsíčně a odeslané
  poptávky maže po 3 letech, stejně jak to uvádějí zásady zpracování.
- **`python3 nastroje/kontrola.py --produkce` musí projít před každým pushem.**
  Změny jsou na webu zhruba do 10 minut (GitHub Pages posílá `max-age=600`).

Otevřené zůstává:

1. **Zásady zpracování osobních údajů** popisují zpracovatele formuláře obecně
   („poskytovatel služby pro odeslání a doručení formuláře“), bez jména služby.
2. **Věcné otevřené body** (co ještě nesmí na web, co je potřeba ověřit
   u distributorů, ceny) jsou v `POZNAMKY-INTERNI.md` — ten se do gitu nedává.

## Poznámky k obsahu

Texty vycházejí z interní rešerše `podklady/Reserse_web_simulacni_zkousky.pdf`
(25. 8. 2026), která cituje metodiky ČEZ Distribuce / EG.D / PREdistribuce,
PPDS přílohu 4 a nařízení (EU) 2016/631. **Nepublikovaná tvrzení označená
v rešerši jako neověřená se na web záměrně nedostala** — seznam je v prvním
komentáři `nastroje/obsah.py` a v `POZNAMKY-INTERNI.md`.

Data se v téhle agendě mění každou sezónu. Stránky kategorií a postupu proto nesou
větu o průběžné změně metodik (`"reviewed": True` v obsahu). Podrobnosti
z metodik — čísla bodů, parametry zkoušek, přechodná data — se na zjednodušený
web záměrně nedávají: co tam není, nemůže zastarat. Zůstaly jen hranice
kategorií a lhůty 30 dnů a 12 měsíců.

**Zdroje a datum aktualizace.** Odborné stránky mají dole řádek „Aktualizováno … Zdroje: …“.
Obsah je v `obsah.ZDROJE` (datum a seznam dokumentů pro každou stránku). Datum posouvat
jen po skutečné kontrole obsahu proti uvedeným dokumentům — proto „aktualizováno“, ne
„ověřeno“. `kontrola.py` hlásí chybu, když odborné stránce řádek chybí, a upozorní, když
je datum starší než půl roku.

**Typografie.** Pomlčka se píše „–“ podle české normy, ne anglická „—“; rozsahy výkonu
slovy („30 MW až pod 75 MW“); jmenovitý výkon s dolním indexem (`P<sub>n</sub>`). Všechno tři
hlídá `kontrola.py`.
