#!/usr/bin/env python3
"""Kontrola vygenerovaneho webu pred publikaci.

    python3 nastroje/kontrola.py              # bezna kontrola (staging)
    python3 nastroje/kontrola.py --produkce   # navic: zadny PLACEHOLDER, robots bez Disallow: /, CNAME
    python3 nastroje/kontrola.py --externi    # navic: dostupnost externich odkazu (chodi na sit)

Hlida odkazy a kotvy, zakladni meta, jeden H1, canonical, parovani tagu, sitemap,
JSON-LD (validni JSON a FAQ shodne s viditelnym textem), zastarale formulace
a datum aktualizace na odbornych strankach.
"""

import html
import json
import re
import sys
from datetime import date
from pathlib import Path
from urllib import error, request

KOREN = Path(__file__).resolve().parent.parent
DOMENA = "https://www.simulacni-zkousky.cz"
STARI_AKTUALIZACE_DNU = 183

CHYBY = []
UPOZORNENI = []

# Formulace, ktere se v minulych kolech oprav na web vracely: (vzor, spravne).
ZAKAZANE = [
    (r"\bÚPOS\b|\bÚTP\b", "UPOS a UTP se píšou bez čárky"),
    (r"\bvíc\b|\bnejvíc\b|\bdřív\b|\bnejdřív\b", "v odborném textu více / dříve"),
    (r"\ba výš\b", "„B2 a vyšších kategorií“"),
    (r"\bvn\b|\bvvn\b", "VN / VVN velkými"),
    (r"30 až 75 MW", "kategorie C je 30 MW až pod 75 MW"),
    (r"A1 — do 11 kW|A1 \(do 11 kW\)", "kategorie A1 začíná na 0,8 kW"),
    (r"Souvisejicí", "překlep — Související"),
    (r"stejných hranic|stejnými výkonovými hranicemi", "baterie se nezařazují automaticky jako výrobny"),
    (r"se nedělají|Žádné zkoušky", "u A1/A2 bez absolutních tvrzení"),
    (r"dokládá většina požadavků", "u B2 se kombinuje zkouška, simulace a certifikát"),
    (r"nejčastěji zastaví|v milionech|zlomek toho|[Ll]evnější|málokdo", "tvrzení bez podkladu"),
    (r"od stolu|skutečně měří|Skok proti", "hovorová formulace"),
    (r"žádají akreditaci u ČIA", "ČIA jen jako požadavek konkrétního dokumentu"),
    (r"automatického připojení výrobny po výpadku", "u typu D je automatické připojení zakázané"),
    (r"je tedy stejné|se tedy neliší", "společné jsou jen základní metodiky"),
]


def chyba(soubor, text):
    CHYBY.append(f"{soubor}: {text}")


def upozorneni(soubor, text):
    UPOZORNENI.append(f"{soubor}: {text}")


def prosty_text(html_text):
    """Stejne pravidlo jako build.prosty_text — text odpovedi ve FAQ JSON-LD."""
    t = re.sub(r"<a [^>]*>[^<]*→</a>", "", html_text)
    t = re.sub(r"</?(p|br|li|ul|ol)\b[^>]*>", " ", t)
    t = re.sub(r"<[^>]+>", "", t)
    t = re.sub(r"\s+", " ", html.unescape(t))
    return re.sub(r"\s+([,.;:!?)])", r"\1", t).strip()


def viditelny_text(obsah):
    """Text stranky, jak ho vidi ctenar i vyhledavac (vcetne title a meta description)."""
    titulek = " ".join(re.findall(r"<title>(.*?)</title>", obsah, re.S))
    popis = " ".join(re.findall(r'name="description" content="([^"]*)"', obsah))
    telo = re.sub(r"(?is)<(script|style)[^>]*>.*?</\1>", " ", obsah)
    telo = re.sub(r"<[^>]+>", " ", telo)
    return re.sub(r"\s+", " ", html.unescape(f"{titulek} {popis} {telo}"))


def zkontroluj_stranku(cesta, jmena):
    obsah = cesta.read_text(encoding="utf-8")
    jmeno = cesta.name

    # zakladni meta
    for co, vzor in (("<title>", r"<title>[^<]{10,}</title>"),
                     ("meta description", r'name="description" content="[^"]{40,}"'),
                     ("canonical", r'rel="canonical"'),
                     ("h1", r"<h1[ >]")):
        if not re.search(vzor, obsah):
            chyba(jmeno, f"chybí {co}")
    if len(re.findall(r"<h1[ >]", obsah)) > 1:
        chyba(jmeno, "víc než jeden <h1>")

    # canonical musi mirit na finalni domenu a na tuhle stranku
    kanon = re.search(r'<link rel="canonical" href="([^"]+)"', obsah)
    ocekavany = f"{DOMENA}/" if jmeno == "index.html" else f"{DOMENA}/{jmeno}"
    if kanon and kanon.group(1) != ocekavany:
        chyba(jmeno, f"canonical {kanon.group(1)} místo {ocekavany}")

    # parovani zakladnich tagu
    for tag in ("section", "div", "article", "table", "details"):
        otev = len(re.findall(rf"<{tag}[ >]", obsah))
        zavr = len(re.findall(rf"</{tag}>", obsah))
        if otev != zavr:
            chyba(jmeno, f"nepárový <{tag}>: {otev} otevřených, {zavr} zavřených")

    # odkazy a zdroje
    for href in re.findall(r'(?:href|src)="([^"]+)"', obsah):
        if href.startswith(("http://", "https://", "mailto:", "tel:", "#", "data:", "./")):
            continue
        soubor, _, kotva = href.partition("#")
        if not soubor:
            continue
        if soubor.endswith(".html"):
            if soubor not in jmena:
                chyba(jmeno, f"odkaz na neexistující stránku {soubor}")
            elif kotva and f'id="{kotva}"' not in (KOREN / soubor).read_text(encoding="utf-8"):
                chyba(jmeno, f"odkaz na neexistující kotvu {soubor}#{kotva}")
        elif not (KOREN / soubor).exists():
            chyba(jmeno, f"chybí soubor {soubor}")
    for kotva in re.findall(r'href="#([^"]+)"', obsah):
        if f'id="{kotva}"' not in obsah:
            chyba(jmeno, f"kotva #{kotva} na stránce neexistuje")

    # JSON-LD: validni JSON, FAQ shodne s viditelnym textem
    for blok in re.findall(r'<script type="application/ld\+json">\s*(.*?)\s*</script>', obsah, re.S):
        try:
            data = json.loads(blok)
        except json.JSONDecodeError as e:
            chyba(jmeno, f"nevalidní JSON-LD: {e}")
            continue
        if data.get("@type") != "FAQPage":
            continue
        viditelne = re.findall(r'<summary>(.*?)</summary>\s*<div class="answer">(.*?)</div>\s*</details>',
                               obsah, re.S)
        v_ld = [(q["name"], q["acceptedAnswer"]["text"]) for q in data.get("mainEntity", [])]
        if len(viditelne) != len(v_ld):
            chyba(jmeno, f"FAQ JSON-LD má {len(v_ld)} otázek, stránka {len(viditelne)}")
        for (otazka, odpoved), (ld_otazka, ld_odpoved) in zip(viditelne, v_ld):
            if prosty_text(otazka) != ld_otazka:
                chyba(jmeno, f"FAQ JSON-LD: otázka „{ld_otazka}“ neodpovídá stránce")
            elif prosty_text(odpoved) != ld_odpoved:
                chyba(jmeno, f"FAQ JSON-LD: odpověď na „{ld_otazka}“ neodpovídá stránce")

    # formulace, ktere uz jednou byly opravene
    text = viditelny_text(obsah)
    for vzor, spravne in ZAKAZANE:
        for nalez in sorted({m.group(0) for m in re.finditer(vzor, text)}):
            chyba(jmeno, f"zastaralá formulace „{nalez}“ — {spravne}")

    # odborne stranky musi nest datum aktualizace a zdroje
    if 'class="reviewed"' in obsah or 'class="block zdroj"' in obsah:
        m = re.search(r"Aktualizováno (\d{1,2})\. (\d{1,2})\. (\d{4})\.", obsah)
        if not m:
            chyba(jmeno, "odborná stránka bez řádku „Aktualizováno … Zdroje: …“ (doplň obsah.ZDROJE)")
        else:
            den = date(int(m.group(3)), int(m.group(2)), int(m.group(1)))
            stari = (date.today() - den).days
            if stari > STARI_AKTUALIZACE_DNU:
                upozorneni(jmeno, f"obsah aktualizován {den.day}. {den.month}. {den.year}, před {stari} dny — "
                                  "projít proti aktuálním dokumentům a posunout datum v obsah.ZDROJE")
    return obsah


def zkontroluj_sitemap(stranky, jmena, obsahy):
    sitemap = (KOREN / "sitemap.xml").read_text(encoding="utf-8")
    for cesta in stranky:
        noindex = re.search(r'name="robots"[^>]*noindex', obsahy[cesta.name])
        klic = "/" if cesta.name == "index.html" else f"/{cesta.name}"
        v_mape = f"<loc>{DOMENA}{klic}</loc>" in sitemap
        if cesta.name == "404.html" or noindex:
            if v_mape:
                chyba("sitemap.xml", f"obsahuje stránku, která se nemá indexovat: {cesta.name}")
        elif not v_mape:
            chyba("sitemap.xml", f"chybí {cesta.name}")
    for loc in re.findall(r"<loc>([^<]+)</loc>", sitemap):
        if not loc.startswith(DOMENA):
            chyba("sitemap.xml", f"adresa mimo doménu {DOMENA}: {loc}")
            continue
        stranka = loc[len(DOMENA):].lstrip("/") or "index.html"
        if stranka not in jmena:
            chyba("sitemap.xml", f"odkaz na neexistující stránku {loc}")


def zkontroluj_produkci(stranky, produkce):
    nahlas = chyba if produkce else upozorneni
    s_placeholderem = [p.name for p in stranky if "PLACEHOLDER" in p.read_text(encoding="utf-8")]
    if s_placeholderem:
        nahlas("formulář", "v kódu zůstal PLACEHOLDER: " + ", ".join(s_placeholderem))

    robots = (KOREN / "robots.txt").read_text(encoding="utf-8")
    aktivni = [r.strip() for r in robots.splitlines() if r.strip() and not r.strip().startswith("#")]
    zakazano = "Disallow: /" in aktivni
    bez_sitemapy = not any(r.lower().startswith("sitemap:") for r in aktivni)
    if produkce:
        if zakazano:
            chyba("robots.txt", "zakazuje indexaci celého webu (Disallow: /)")
        if bez_sitemapy:
            chyba("robots.txt", f"chybí řádek Sitemap: {DOMENA}/sitemap.xml")
        if not (KOREN / "CNAME").exists():
            chyba("CNAME", "chybí — přejmenuj CNAME.disabled, až doména míří na hosting")
    return zakazano


def zkontroluj_externi(stranky):
    adresy = set()
    for cesta in stranky:
        for adresa in re.findall(r'<a [^>]*href="(https?://[^"]+)"', cesta.read_text(encoding="utf-8")):
            if not adresa.startswith(DOMENA):
                adresy.add(adresa)
    for adresa in sorted(adresy):
        dotaz = request.Request(adresa, headers={"User-Agent": "Mozilla/5.0 (kontrola webu simulacni-zkousky)"})
        try:
            with request.urlopen(dotaz, timeout=15) as odpoved:
                if odpoved.status >= 400:
                    upozorneni("externí odkaz", f"{adresa} → HTTP {odpoved.status}")
        except error.HTTPError as e:
            upozorneni("externí odkaz", f"{adresa} → HTTP {e.code}")
        except Exception as e:  # sit, DNS, certifikat
            upozorneni("externí odkaz", f"{adresa} → {type(e).__name__}: {e}")
    return len(adresy)


def main() -> int:
    produkce = "--produkce" in sys.argv
    externi = "--externi" in sys.argv

    stranky = sorted(KOREN.glob("*.html"))
    jmena = {p.name for p in stranky}
    obsahy = {p.name: zkontroluj_stranku(p, jmena) for p in stranky}
    zkontroluj_sitemap(stranky, jmena, obsahy)
    staging = zkontroluj_produkci(stranky, produkce)
    pocet_externich = zkontroluj_externi(stranky) if externi else None

    if UPOZORNENI:
        print(f"Upozornění ({len(UPOZORNENI)}):")
        for u in UPOZORNENI:
            print("  !", u)
        print()
    if CHYBY:
        print(f"NALEZENO {len(CHYBY)} problémů:\n")
        for c in CHYBY:
            print("  ✗", c)
        return 1

    zprava = f"OK — {len(stranky)} stránek, žádný rozbitý odkaz"
    if pocet_externich is not None:
        zprava += f", externích odkazů prověřeno {pocet_externich}"
    print(zprava + ".")
    if staging and not produkce:
        print("Režim staging: robots.txt zakazuje indexaci. Před spuštěním musí projít "
              "python3 nastroje/kontrola.py --produkce")
    return 0


if __name__ == "__main__":
    sys.exit(main())
