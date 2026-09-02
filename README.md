# www.simulacni-zkousky.cz

Specializovaný web BFK systems s.r.o. na **ověřování souladu výroben s RfG** —
simulace souladu, zkoušky na místě, dokumentace a jednání s provozovateli
distribučních soustav. Statický web bez backendu.

Barvy a typografii sdílí s cenovou nabídkou BFK (`../bfk_nabidka_html`): Roboto,
oranžová `#F08A00`, tmavě šedá `#3C3C3C`. Rozvržení a komponenty vycházejí
z webu `../bftechnology`, obsah z interní rešerše (viz `podklady/`).

## Stránky se GENERUJÍ — needituj `.html` v kořeni

Web má 27 stránek se stejnou hlavičkou, patičkou a menu. Ruční kopie hlavičky
v každém souboru (jako na webu BF technology) se při téhle velikosti neuhlídá,
takže:

```bash
python3 nastroje/build.py      # vygeneruje všechny .html + sitemap.xml
python3 nastroje/kontrola.py   # zkontroluje odkazy, kotvy, meta a párování tagů
```

**Obsah stránek je v `nastroje/obsah.py`**, šablona a menu v `nastroje/build.py`.
Když upravíš vygenerovaný `.html` v kořeni, další build to přepíše.

```
.
├── nastroje/
│   ├── obsah.py            # ← TADY se edituje obsah (1 položka PAGES = 1 stránka)
│   ├── build.py            # šablona, menu, patička, sitemap
│   ├── kontrola.py         # kontrola odkazů a struktury
│   └── generuj-obrazky.py  # zmenšeniny a WebP z originálů v assets/
├── assets/
│   ├── style.css           # všechny styly (převzato z webu BFT, přebarveno)
│   ├── nav.js              # rozbalovací menu + mobilní menu
│   ├── form.js             # odeslání poptávkového formuláře
│   ├── logo_SZ.png         # ZDROJ loga webu (originál, stránky ho nenačítají)
│   ├── logo-sz-300/600.*   # logo webu pro hlavičku a patičku (generované)
│   ├── bfk-logo*, bfk-znacka-*  # logo a značka BFK systems (generované)
│   ├── favicon.png         # oranžový čtverec s fajfkou (kreslený skriptem)
│   └── title-photo*        # titulní fotka (hero, pozadí kontaktu)
├── podklady/               # interní rešerše (v .gitignore, nepublikuje se)
├── index.html … 404.html   # GENEROVANÉ, needitovat
├── sitemap.xml             # GENEROVANÁ buildem
├── robots.txt              # ZATÍM ZAKAZUJE indexaci (staging), viz níže
└── CNAME.disabled          # doména — záměrně neaktivní, viz níže
```

## Loga

Logo webu je originál v `assets/logo_SZ.png`. Skript `nastroje/generuj-obrazky.py`
z něj udělá ořez bez bílého okraje, průhledné pozadí a zmenšeniny
`logo-sz-300/600.png|webp`, na které se odkazuje hlavička i patička.
**Po výměně originálu skript spusť znovu**, jinak zůstanou staré varianty.

Vazba na provozovatele: v hlavičce je za svislou čarou značka BFK systems
s popiskem „provozuje", v patičce logo webu a pod ním celé logo BFK. Na displejích
pod 900 px se popisek skryje a zůstane jen značka.

Favicon je oranžový čtverec s bílou fajfkou (kreslí ho stejný skript) — celá
značka s monitorem je v 16 px nečitelná.

## Struktura webu

Hub + paprsky, jedna stránka = jedna vyhledávaná fráze:

| Sekce | Stránky |
|---|---|
| Kategorie | `kategorie-a1`, `-a2`, `-b1`, `-b2`, `-c-d`, `bateriova-uloziste-zue`, `pridani-baterie-k-fve` |
| Distributoři | `cez-distribuce`, `egd`, `predistribuce` |
| Služby | `simulace-souladu`, `zkousky-na-miste`, `zkousky-ochran`, `rtu-dispecerske-rizeni`, `podklady` |
| Proces | `proces-pripojeni`, `upos`, `utp`, `dokument-vyrobniho-modulu`, `rozpadove-misto`, `slovnik-rfg` |
| Ostatní | `index`, `reference`, `faq`, `kontakt`, `zasady-zpracovani-osobnich-udaju`, `404` |

Každá stránka má drobečkovou navigaci (i jako JSON-LD `BreadcrumbList`),
kanonickou URL a Open Graph. Stránky s akordeonem dotazů mají navíc JSON-LD
`FAQPage`.

## Před spuštěním je potřeba dořešit

1. **Klíč poptávkového formuláře.** V `nastroje/obsah.py` (proměnná `FORMULAR`)
   je `access_key` s hodnotou `PLACEHOLDER-DOPLNIT-KLIC-WEB3FORMS` — formulář
   zatím nic neodešle a `form.js` na to upozorní v konzoli. Doplň klíč
   z web3forms.com registrovaný na `info@bfksystems.cz` (nebo formulář přepoj
   na vlastní Cloudflare Worker jako na webu BF technology) a spusť build.
2. **robots.txt** — teď zakazuje procházení celého webu. Před spuštěním přepnout
   podle komentáře v souboru.
3. **CNAME** — přejmenovat `CNAME.disabled` na `CNAME` až ve chvíli, kdy doména
   `simulacni-zkousky.cz` míří na hosting. Dřív ne, jinak si GitHub Pages doménu
   zabere a nepůjde použít jinde.
4. **Zásady zpracování osobních údajů** — text v `obsah.py` popisuje zpracovatele
   obecně („poskytovatel služby pro odeslání formuláře“). Až bude jasné, jaká
   služba to je, doplnit jméno.
5. **Věcné otevřené body** (co ještě nesmí na web, co je potřeba ověřit
   u distributorů, ceny) jsou v `POZNAMKY-INTERNI.md` — ten se do gitu nedává.

## Poznámky k obsahu

Texty vycházejí z interní rešerše `podklady/Reserse_web_simulacni_zkousky.pdf`
(25. 8. 2026), která cituje metodiky ČEZ Distribuce / EG.D / PREdistribuce,
PPDS přílohu 4 a nařízení (EU) 2016/631. **Nepublikovaná tvrzení označená
v rešerši jako neověřená se na web záměrně nedostala** — seznam je v prvním
komentáři `nastroje/obsah.py` a v `POZNAMKY-INTERNI.md`.

Data se v téhle agendě mění každou sezónu. Odborné stránky proto nesou větu
o průběžné změně metodik (`"reviewed": True` v obsahu) a u tabulek je vždy
uvedený zdroj s datem platnosti.
