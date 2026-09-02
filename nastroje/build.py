#!/usr/bin/env python3
"""Generator webu simulacni-zkousky.cz (BFK systems).

Web ma pres dvacet stranek se stejnou hlavickou, patickou a menu. Rucne
udrzovana kopie hlavicky v kazdem souboru (jako na webu BF technology) se pri
teto velikosti neda uhlidat — proto se stranky generuji.

    python3 nastroje/build.py

Obsah stranek je v nastroje/obsah.py, sablona a menu tady. Vygenerovane .html
soubory v korenu se needituji rucne — build je pri dalsim spusteni prepise.
"""

from __future__ import annotations

import html
import json
import re
from datetime import date
from pathlib import Path

import obsah

KOREN = Path(__file__).resolve().parent.parent
DOMENA = "https://www.simulacni-zkousky.cz"
ZNACKA = "Simulační zkoušky"
FIRMA = "BFK systems s.r.o."

# ---------------------------------------------------------------- menu -----
# (nazev, klic pro zvyrazneni, polozky | odkaz)
NAV = [
    ("Kategorie", "kategorie", [
        ("A1 — do 11 kW", "kategorie-a1.html"),
        ("A2 — 11 až 100 kW", "kategorie-a2.html"),
        ("B1 — 100 kW až 1 MW", "kategorie-b1.html"),
        ("B2 — 1 až 30 MW", "kategorie-b2.html"),
        ("C a D — nad 30 MW", "kategorie-c-d.html"),
        ("Bateriová úložiště (ZUE)", "bateriova-uloziste-zue.html"),
        ("Přidání baterie k FVE", "pridani-baterie-k-fve.html"),
    ]),
    ("Distributoři", "pds", [
        ("ČEZ Distribuce", "cez-distribuce.html"),
        ("EG.D", "egd.html"),
        ("PREdistribuce", "predistribuce.html"),
    ]),
    ("Služby", "sluzby", [
        ("Simulace souladu", "simulace-souladu.html"),
        ("Zkoušky na místě", "zkousky-na-miste.html"),
        ("Zkoušky ochran", "zkousky-ochran.html"),
        ("RTU a dispečerské řízení", "rtu-dispecerske-rizeni.html"),
        ("Podklady k zahájení", "podklady.html"),
    ]),
    ("Proces", "proces", [
        ("Proces připojení krok za krokem", "proces-pripojeni.html"),
        ("ÚPOS — dočasný provoz", "upos.html"),
        ("ÚTP — trvalý provoz", "utp.html"),
        ("Dokument výrobního modulu", "dokument-vyrobniho-modulu.html"),
        ("Rozpadové místo a ochrany", "rozpadove-misto.html"),
        ("Slovník pojmů RfG", "slovnik-rfg.html"),
    ]),
    ("Reference", "reference", "reference.html"),
    ("Kontakt", "kontakt", "kontakt.html"),
]

IKONA_SIT = {
    "linkedin": '<svg viewBox="0 0 24 24" fill="currentColor" aria-hidden="true"><path d="M4.98 3.5a2.5 2.5 0 1 1 0 5 2.5 2.5 0 0 1 0-5zM3 9h4v12H3zM9 9h3.8v1.7h.05c.53-1 1.83-2.06 3.77-2.06 4.03 0 4.78 2.65 4.78 6.1V21h-4v-5.4c0-1.29-.02-2.95-1.8-2.95-1.8 0-2.07 1.4-2.07 2.85V21H9z"/></svg>',
    "web": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.7 2.5 15.3 0 18M12 3c-2.5 2.7-2.5 15.3 0 18"/></svg>',
}

TEL = "+420 776 111 100"
TEL_HREF = "+420776111100"
MAIL = "info@bfksystems.cz"

# Logo webu — originál od klienta (assets/logo_SZ.png). Zmenseniny a prusvitne
# pozadi dela nastroje/generuj-obrazky.py, tady uz jen odkazujeme.
LOGO_IMG = """<picture>
          <source type="image/webp" srcset="assets/logo-sz-300.webp 300w, assets/logo-sz-600.webp 600w" sizes="{sizes}">
          <img src="assets/logo-sz-600.png" alt="simulacni-zkousky.cz" width="1037" height="324" srcset="assets/logo-sz-300.png 300w, assets/logo-sz-600.png 600w" sizes="{sizes}">
        </picture>"""

# Vazba na provozovatele — v hlavicce cele logo BFK vcetne napisu (samotna
# ctvercova znacka bez textu nikomu nerekne, ci web to je). Popisek "provozuje"
# se vejde az na sirokych displejich.
BFK_ZNACKA = """<a class="brand-by" href="https://www.bfksystems.cz/" target="_blank" rel="noopener" title="Web provozuje BFK systems s.r.o.">
        <span class="lbl">provozuje</span>
        <picture>
          <source type="image/webp" srcset="assets/bfk-logo-210.webp 210w, assets/bfk-logo-420.webp 420w" sizes="80px">
          <img src="assets/bfk-logo-420.png" alt="BFK systems s.r.o." width="420" height="171" srcset="assets/bfk-logo-210.png 210w, assets/bfk-logo-420.png 420w" sizes="80px">
        </picture>
      </a>"""


# ------------------------------------------------------------- sablona -----
def hlavicka(aktivni: str) -> str:
    """Sticky hlavicka s rozbalovacim menu."""
    polozky = []
    for nazev, klic, cil in NAV:
        if isinstance(cil, str):
            tridy = ' class="active"' if klic == aktivni else ""
            aria = ' aria-current="page"' if klic == aktivni else ""
            polozky.append(f'      <a{tridy} href="{cil}"{aria}>{nazev}</a>')
            continue
        je_aktivni = klic == aktivni
        podpolozky = "\n".join(
            f'          <a href="{href}">{txt}</a>' for txt, href in cil
        )
        polozky.append(
            f'      <div class="has-sub{" is-active" if je_aktivni else ""}">\n'
            f'        <button class="sub-toggle" type="button" aria-expanded="false">\n'
            f'          {nazev} <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" '
            f'stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="m6 9 6 6 6-6"/></svg>\n'
            f'        </button>\n'
            f'        <div class="sub">\n{podpolozky}\n        </div>\n'
            f'      </div>'
        )
    menu = "\n".join(polozky)

    mobil = []
    for nazev, klic, cil in NAV:
        if isinstance(cil, str):
            mobil.append(f'  <a href="{cil}">{nazev}</a>')
        else:
            mobil.append(f'  <p class="m-group">{nazev}</p>')
            mobil.extend(f'  <a class="m-sub" href="{href}">{txt}</a>' for txt, href in cil)
    mobil.append('  <a href="faq.html">Časté dotazy</a>')
    mobil.append('  <a class="cta-mobile" href="kontakt.html">Nezávazná poptávka</a>')
    mobilni = "\n".join(mobil)

    return f"""<!-- HLAVICKA (generovano z nastroje/build.py) -->
<header class="site-header">
  <div class="container row">
    <div class="brand-wrap">
      <a class="brand" href="index.html" aria-label="simulacni-zkousky.cz – úvodní stránka">
        {LOGO_IMG.format(sizes='150px')}
      </a>
      {BFK_ZNACKA}
    </div>
    <nav class="primary" aria-label="Hlavní navigace">
{menu}
      <a class="header-cta" href="kontakt.html"><span class="dlouhy">Nezávazná poptávka</span><span class="kratky">Poptávka</span></a>
    </nav>
    <button class="hamburger" id="menu-open" type="button" aria-label="Otevřít menu" aria-expanded="false" aria-controls="mmenu">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M3 6h18M3 12h18M3 18h18"/></svg>
    </button>
  </div>
</header>

<div class="mobile-menu" id="mmenu" role="dialog" aria-modal="true" aria-label="Hlavní navigace">
  <button class="close" id="menu-close" type="button" aria-label="Zavřít menu">
    <svg viewBox="0 0 24 24" width="20" height="20" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round"><path d="M18 6 6 18M6 6l12 12"/></svg>
  </button>
{mobilni}
</div>
"""


def paticka() -> str:
    sloupce = []
    for nazev, _klic, cil in NAV[:4]:
        odkazy = "\n".join(f'      <a href="{href}">{txt}</a>' for txt, href in cil)
        sloupce.append(f'    <div>\n      <h4>{nazev}</h4>\n{odkazy}\n    </div>')
    rozcestnik = "\n".join(sloupce[:2])
    rozcestnik2 = "\n".join(sloupce[2:])

    return f"""<!-- PATICKA -->
<footer class="site">
  <div class="container grid">
    <div class="logo-cell">
      {LOGO_IMG.format(sizes='210px')}
      <span class="foot-by">Web provozuje</span>
      <a href="https://www.bfksystems.cz/" target="_blank" rel="noopener">
        <picture>
          <source type="image/webp" srcset="assets/bfk-logo-210.webp 210w, assets/bfk-logo-420.webp 420w" sizes="150px">
          <img class="foot-bfk" src="assets/bfk-logo-420.png" alt="BFK systems s.r.o." width="420" height="171" srcset="assets/bfk-logo-210.png 210w, assets/bfk-logo-420.png 420w" sizes="150px">
        </picture>
      </a>
    </div>
    <div>
      <h4>Kontakt</h4>
      <div><span class="lbl">Tel</span><a href="tel:{TEL_HREF}" style="display:inline">{TEL}</a></div>
      <div><span class="lbl">Mail</span><a href="mailto:{MAIL}" style="display:inline">{MAIL}</a></div>
      <div style="margin-top:10px">Obchodní 455/12<br>405 02 Děčín</div>
      <div style="margin-top:10px">IČO 23571853<br>DIČ CZ23571853</div>
    </div>
{rozcestnik}
{rozcestnik2}
    <div>
      <h4>Dále</h4>
      <a href="reference.html">Reference</a>
      <a href="faq.html">Časté dotazy</a>
      <a href="kontakt.html">Kontakt</a>
      <a href="https://www.bfksystems.cz/" target="_blank" rel="noopener">bfksystems.cz</a>
      <a href="https://www.bftechnology.cz/" target="_blank" rel="noopener">bftechnology.cz</a>
    </div>
  </div>
  <div class="copy">
    <div class="container row">
      <span>© <span id="year">{date.today().year}</span> {FIRMA} – všechna práva vyhrazena</span>
      <span><a href="zasady-zpracovani-osobnich-udaju.html">Zásady zpracování osobních údajů</a></span>
      <span>www.simulacni-zkousky.cz</span>
    </div>
  </div>
</footer>

<script>document.getElementById('year').textContent = new Date().getFullYear();</script>
<script src="assets/nav.js"></script>
"""


def drobecky(cesta: list[tuple[str, str]], nazev: str) -> tuple[str, str]:
    """HTML drobeckove navigace + JSON-LD BreadcrumbList."""
    if not cesta and nazev == "":
        return "", ""
    kusy = ['      <a href="index.html">Úvod</a> <span>›</span>']
    body = [{"@type": "ListItem", "position": 1, "name": "Úvod", "item": f"{DOMENA}/"}]
    for i, (txt, href) in enumerate(cesta, start=2):
        kusy.append(f'      <a href="{href}">{txt}</a> <span>›</span>')
        body.append({"@type": "ListItem", "position": i, "name": txt, "item": f"{DOMENA}/{href}"})
    kusy.append(f'      <span aria-current="page">{nazev}</span>')
    body.append({"@type": "ListItem", "position": len(body) + 1, "name": nazev})
    html_nav = ('    <nav class="breadcrumb" aria-label="Drobečková navigace">\n'
                + "\n".join(kusy) + "\n    </nav>")
    ld = json.dumps({"@context": "https://schema.org", "@type": "BreadcrumbList",
                     "itemListElement": body}, ensure_ascii=False, indent=2)
    return html_nav, ld


def faq_blok(polozky: list[tuple[str, str]], nadpis: str = "Časté dotazy") -> tuple[str, str]:
    """Akordeon + JSON-LD FAQPage."""
    if not polozky:
        return "", ""
    radky = []
    for i, (otazka, odpoved) in enumerate(polozky):
        otevreno = " open" if i == 0 else ""
        radky.append(
            f'      <details{otevreno}>\n'
            f'        <summary>{otazka}</summary>\n'
            f'        <div class="answer">{odpoved}</div>\n'
            f'      </details>'
        )
    blok = f"""<section class="block" id="faq">
  <div class="container">
    <div class="section-head">
      <p class="eyebrow">Ptáte se</p>
      <h2>{nadpis}</h2>
    </div>
    <div class="faq">
{chr(10).join(radky)}
    </div>
  </div>
</section>"""
    ld = json.dumps({
        "@context": "https://schema.org", "@type": "FAQPage",
        "mainEntity": [
            {"@type": "Question", "name": o,
             "acceptedAnswer": {"@type": "Answer", "text": re.sub(r"<[^>]+>", " ", a).strip()}}
            for o, a in polozky
        ],
    }, ensure_ascii=False, indent=2)
    return blok, ld


def stranka(p: dict) -> str:
    """Slozi celou HTML stranku z jednoho zaznamu obsahu."""
    slug = p["slug"]
    url = f"{DOMENA}/" if slug == "index.html" else f"{DOMENA}/{slug}"
    titulek = p["title"] if slug == "index.html" else f'{p["title"]} | {ZNACKA}'

    bc_html, bc_ld = ("", "")
    if p.get("breadcrumb") is not None and slug != "index.html":
        bc_html, bc_ld = drobecky(p.get("breadcrumb", []), p.get("bc_nazev", p["h1"]))

    faq_html, faq_ld = faq_blok(p.get("faq", []), p.get("faq_nadpis", "Časté dotazy"))

    ldjson = ""
    for data in (bc_ld, faq_ld, p.get("ld", "")):
        if data:
            ldjson += f'\n<script type="application/ld+json">\n{data}\n</script>'

    hlava = f"""<!DOCTYPE html>
<html lang="cs">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1, shrink-to-fit=no, viewport-fit=cover">
<title>{titulek}</title>
<meta name="description" content="{html.escape(p["desc"], quote=True)}">
<link rel="canonical" href="{url}">
<link rel="icon" type="image/png" href="assets/favicon.png">

<meta property="og:type" content="website">
<meta property="og:site_name" content="{ZNACKA} – {FIRMA}">
<meta property="og:title" content="{html.escape(p["title"], quote=True)}">
<meta property="og:description" content="{html.escape(p["desc"], quote=True)}">
<meta property="og:url" content="{url}">
<meta property="og:image" content="{DOMENA}/assets/title-photo.jpg">
<meta property="og:locale" content="cs_CZ">
<meta name="theme-color" content="#3C3C3C">

<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Roboto:wght@300;400;500;700;900&display=swap" rel="stylesheet">
<link rel="stylesheet" href="assets/style.css">{ldjson}
</head>

<body>
"""

    # uvodni sekce (mimo domovskou, ktera ma vlastni hero v obsahu)
    uvod = ""
    if p.get("h1"):
        claim = f'\n      <p class="h1-claim">{p["claim"]}</p>' if p.get("claim") else ""
        eyebrow = f'\n      <p class="eyebrow">{p["eyebrow"]}</p>' if p.get("eyebrow") else ""
        overeno = ('\n      <p class="reviewed"><b>Metodiky provozovatelů distribučních soustav se '
                   'průběžně mění.</b> U konkrétního projektu vždy ověřujeme aktuální verzi dokumentů '
                   'příslušného provozovatele.</p>') if p.get("reviewed") else ""
        uvod = f"""<section class="block">
  <div class="container">
{bc_html}
    <div class="section-head">{eyebrow}
      <h1>{p["h1"]}</h1>{claim}
      {p.get("intro", "")}{overeno}
    </div>
    {p.get("anchors", "")}
  </div>
</section>
"""

    pruh = ""
    if p.get("stats"):
        dlazdice = "\n".join(
            f'      <div><div class="num">{c}</div><div class="label">{l}</div></div>'
            for c, l in p["stats"]
        )
        cols = ' cols-2' if len(p["stats"]) == 2 else ""
        pruh = f'<div class="stats-band">\n  <div class="container grid{cols}">\n{dlazdice}\n  </div>\n</div>\n'

    cross = ""
    if p.get("cross"):
        odkazy = "\n".join(f'      <a href="{h}">{t}</a>' for t, h in p["cross"])
        cross = f"""<section class="block{' alt' if p.get('cross_alt') else ''}">
  <div class="container">
    <div class="crosslinks">
      <span class="t">Souvisejicí stránky</span>
{odkazy}
    </div>
  </div>
</section>
"""

    kontakt = "" if p.get("bez_kontaktu") else KONTAKT_PRUH
    return (hlava + hlavicka(p.get("nav", "")) + uvod + pruh + p["body"]
            + faq_html + cross + kontakt + paticka() + "\n</body>\n</html>\n")


# Vyzva ke kontaktu nad patickou — na kazde strance krome kontaktu.
KONTAKT_PRUH = f"""<section class="contact-section" id="poptavka">
  <div class="bg"><picture>
    <source type="image/webp" srcset="assets/title-photo-1024.webp 1024w, assets/title-photo.webp 2048w" sizes="(max-width: 980px) 100vw, 33vw">
    <img src="assets/title-photo.jpg" alt="" aria-hidden="true" loading="lazy" width="2048" height="1536" srcset="assets/title-photo-1024.jpg 1024w, assets/title-photo.jpg 2048w" sizes="(max-width: 980px) 100vw, 33vw">
  </picture></div>
  <div class="container contact-grid">
    <div class="contact-aside">
      <p class="eyebrow">Poptávka</p>
      <h2>Pošlete nám smlouvu<br>o připojení.</h2>
      <p>Ze smlouvy o připojení a jednopólového schématu poznáme kategorii výrobního modulu i rozsah ověření. Ozveme se s tím, co vás čeká, do dvou pracovních dnů.</p>
      <div class="quick">
        <a href="tel:{TEL_HREF}">
          <span class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.12.9.35 1.79.68 2.64a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.44-1.25a2 2 0 0 1 2.11-.45c.85.33 1.74.56 2.64.68A2 2 0 0 1 22 16.92z"/></svg></span>
          {TEL}
        </a>
        <a href="mailto:{MAIL}">
          <span class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg></span>
          {MAIL}
        </a>
      </div>
      <div class="firm">
        <b>{FIRMA}</b><br>
        Obchodní 455/12, 405 02 Děčín<br>
        IČO 23571853 · DIČ CZ23571853
      </div>
    </div>
    <div class="contact-form-card">
      <h3 style="margin:0 0 14px;font-size:20px;color:#222">Co potřebujeme vědět</h3>
      <p style="margin:0 0 18px;font-size:15px">Čím víc toho napíšete rovnou, tím přesněji odpovíme. Ideálně: provozovatel distribuční soustavy, kategorie ze smlouvy o připojení, instalovaný výkon, počet a typ střídačů a jestli je součástí bateriové úložiště.</p>
      <a class="btn btn-primary" href="kontakt.html">Přejít na poptávkový formulář</a>
    </div>
  </div>
</section>
"""


def sitemap(stranky: list[dict]) -> str:
    dnes = date.today().isoformat()
    radky = []
    for p in stranky:
        if p.get("noindex"):
            continue
        slug = p["slug"]
        loc = f"{DOMENA}/" if slug == "index.html" else f"{DOMENA}/{slug}"
        priorita = "1.0" if slug == "index.html" else p.get("prio", "0.7")
        radky.append(f"  <url>\n    <loc>{loc}</loc>\n    <lastmod>{dnes}</lastmod>\n"
                     f"    <priority>{priorita}</priority>\n  </url>")
    return ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'
            + "\n".join(radky) + "\n</urlset>\n")


def main() -> None:
    stranky = obsah.PAGES
    slugy = [p["slug"] for p in stranky]
    if len(slugy) != len(set(slugy)):
        raise SystemExit("duplicitni slug v obsah.PAGES")

    for p in stranky:
        cil = KOREN / p["slug"]
        cil.write_text(stranka(p), encoding="utf-8")
        print(f"  {p['slug']:42s} {cil.stat().st_size // 1024:3d} kB")

    (KOREN / "sitemap.xml").write_text(sitemap(stranky), encoding="utf-8")
    print(f"\n{len(stranky)} stránek + sitemap.xml")


if __name__ == "__main__":
    main()
