#!/usr/bin/env python3
"""Kontrola vygenerovaneho webu: odkazy, kotvy, soubory, zakladni meta.

    python3 nastroje/kontrola.py

Nekontroluje externi odkazy (nechodi na sit), jen to, co je v repozitari.
"""

import re
import sys
from pathlib import Path

KOREN = Path(__file__).resolve().parent.parent
CHYBY = []


def chyba(soubor, text):
    CHYBY.append(f"{soubor}: {text}")


def main() -> int:
    stranky = sorted(p for p in KOREN.glob("*.html"))
    jmena = {p.name for p in stranky}

    for cesta in stranky:
        html = cesta.read_text(encoding="utf-8")
        jmeno = cesta.name

        # zakladni meta
        for co, vzor in (("<title>", r"<title>[^<]{10,}</title>"),
                         ("meta description", r'name="description" content="[^"]{40,}"'),
                         ("canonical", r'rel="canonical"'),
                         ("h1", r"<h1[ >]")):
            if not re.search(vzor, html):
                chyba(jmeno, f"chybí {co}")
        if len(re.findall(r"<h1[ >]", html)) > 1:
            chyba(jmeno, "víc než jeden <h1>")

        # parovani zakladnich tagu
        for tag in ("section", "div", "article", "table"):
            otev = len(re.findall(rf"<{tag}[ >]", html))
            zavr = len(re.findall(rf"</{tag}>", html))
            if otev != zavr:
                chyba(jmeno, f"nepárový <{tag}>: {otev} otevřených, {zavr} zavřených")

        # odkazy a zdroje
        for href in re.findall(r'(?:href|src)="([^"]+)"', html):
            if href.startswith(("http://", "https://", "mailto:", "tel:", "#", "data:", "./")):
                continue
            soubor, _, kotva = href.partition("#")
            if not soubor:
                continue
            cil = KOREN / soubor
            if soubor.endswith(".html"):
                if soubor not in jmena:
                    chyba(jmeno, f"odkaz na neexistující stránku {soubor}")
                elif kotva:
                    cilovy = (KOREN / soubor).read_text(encoding="utf-8")
                    if f'id="{kotva}"' not in cilovy:
                        chyba(jmeno, f"odkaz na neexistující kotvu {soubor}#{kotva}")
            elif not cil.exists():
                chyba(jmeno, f"chybí soubor {soubor}")

        # kotvy v ramci stranky
        for kotva in re.findall(r'href="#([^"]+)"', html):
            if f'id="{kotva}"' not in html:
                chyba(jmeno, f"kotva #{kotva} na stránce neexistuje")

    # sitemap
    sitemap = (KOREN / "sitemap.xml").read_text(encoding="utf-8")
    for cesta in stranky:
        if cesta.name in ("404.html",):
            continue
        klic = "/" if cesta.name == "index.html" else f"/{cesta.name}"
        if klic not in sitemap:
            chyba("sitemap.xml", f"chybí {cesta.name}")

    if CHYBY:
        print(f"NALEZENO {len(CHYBY)} problémů:\n")
        for c in CHYBY:
            print("  ✗", c)
        return 1
    print(f"OK — {len(stranky)} stránek, žádný rozbitý odkaz.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
