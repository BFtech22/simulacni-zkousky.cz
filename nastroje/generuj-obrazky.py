#!/usr/bin/env python3
"""Zmenseniny, WebP varianty a favicon pro web simulacni-zkousky.cz.

Zdroje jsou velke originaly (logo BFK z cenove nabidky, titulni fotka).
Prohlizec ma dostat malou variantu — proto ke kazdemu obrazku generujeme
uzsi verzi a WebP, na ktere se pak odkazuje pres <picture srcset>.

Logo simulacni-zkousky.cz je vektor (assets/logo-simulacni-zkousky.svg,
assets/logo-znacka.svg) a rasterizovat se nemusi — favicon se kresli zvlast,
protoze v 16 px uz z cele znacky nic neni videt.

Spousti se rucne po vymene nektereho z originalu:

    python3 nastroje/generuj-obrazky.py
"""

from pathlib import Path

from PIL import Image, ImageDraw

ASSETS = Path(__file__).resolve().parent.parent / "assets"

ORANZOVA = (240, 138, 0, 255)

# (soubor, sirky zmenseniny)
LOGA = [
    ("bfk-logo.png", [210, 420]),
    ("bfk-logo-white.png", [210, 420]),
]


def uloz(img: Image.Image, cesta: Path, kvalita: int = 90) -> None:
    if cesta.suffix == ".webp":
        img.save(cesta, "WEBP", quality=kvalita, method=6)
    elif cesta.suffix in (".jpg", ".jpeg"):
        img.convert("RGB").save(cesta, "JPEG", quality=kvalita, optimize=True, progressive=True)
    else:
        img.save(cesta, optimize=True)
    print(f"  {cesta.name}  ({cesta.stat().st_size // 1024} kB)")


def zmens(img: Image.Image, sirka: int) -> Image.Image:
    vyska = round(img.height * sirka / img.width)
    return img.resize((sirka, vyska), Image.LANCZOS)


def loga() -> None:
    for jmeno, sirky in LOGA:
        zdroj = ASSETS / jmeno
        if not zdroj.exists():
            print(f"! chybi {zdroj}")
            continue
        print(zdroj.name)
        orig = Image.open(zdroj).convert("RGBA")
        for sirka in sirky:
            maly = zmens(orig, sirka)
            uloz(maly, ASSETS / f"{zdroj.stem}-{sirka}.png")
            uloz(maly, ASSETS / f"{zdroj.stem}-{sirka}.webp")


def logo_webu() -> None:
    """Logo simulacni-zkousky.cz: orez okraju, prusvitne pozadi, zmenseniny.

    Originál (assets/logo_SZ.png) je ctverec s velkym bilym okrajem. Do hlavicky
    potrebujeme tesny orez a pozadi bez bileho obdelniku — bile plochy uvnitr
    znacky (obrazovka, fajfka) musi zustat, takze se pruhlednost pocita jen od
    okraju: pixel je pozadi, dokud narazime na bilou od kraje smerem dovnitr.
    """
    zdroj = ASSETS / "logo_SZ.png"
    if not zdroj.exists():
        print("! chybi assets/logo_SZ.png")
        return
    print(zdroj.name, "→ logo webu")
    orig = Image.open(zdroj).convert("RGBA")
    sirka, vyska = orig.size
    px = orig.load()

    def je_bile(x: int, y: int) -> bool:
        r, g, b, _ = px[x, y]
        return r > 244 and g > 244 and b > 244

    # zaplavove vyplneni od okraju — dovnitr znacky se nedostane
    fronta = [(x, y) for x in range(sirka) for y in (0, vyska - 1)]
    fronta += [(x, y) for y in range(vyska) for x in (0, sirka - 1)]
    pozadi = set()
    while fronta:
        x, y = fronta.pop()
        if (x, y) in pozadi or not (0 <= x < sirka and 0 <= y < vyska):
            continue
        if not je_bile(x, y):
            continue
        pozadi.add((x, y))
        fronta += [(x + 1, y), (x - 1, y), (x, y + 1), (x, y - 1)]
    for x, y in pozadi:
        r, g, b, _ = px[x, y]
        px[x, y] = (r, g, b, 0)

    orez = orig.crop(orig.getbbox())
    print(f"  ořez: {orez.width}×{orez.height} px")
    for sirka_var in (300, 600):
        maly = zmens(orez, sirka_var)
        uloz(maly, ASSETS / f"logo-sz-{sirka_var}.png")
        uloz(maly, ASSETS / f"logo-sz-{sirka_var}.webp")


def bfk_znacka() -> None:
    """Ctvercova znacka z leve casti loga BFK — do hlavicky vedle loga webu."""
    zdroj = ASSETS / "bfk-logo.png"
    if not zdroj.exists():
        return
    print(zdroj.name, "→ značka")
    orig = Image.open(zdroj).convert("RGBA")
    ikona = orig.crop((0, 0, orig.height, orig.height))
    for velikost in (60, 120):
        uloz(zmens(ikona, velikost), ASSETS / f"bfk-znacka-{velikost}.png")
        uloz(zmens(ikona, velikost), ASSETS / f"bfk-znacka-{velikost}.webp")


def favicon() -> None:
    """Oranzovy ctverec s bilou fajfkou.

    Cela znacka (monitor + checklist) je v 16 px necitelna a jeji tmava cast
    by na tmavem prouzku panelu zanikla — v ikone proto zustava jen fajfka
    z oranzoveho odznaku.
    """
    print("favicon (kresleno)")
    n = 720  # kreslime ve velkem a pak zmensujeme, at jsou hrany hladke
    img = Image.new("RGBA", (n, n), (0, 0, 0, 0))
    kresli = ImageDraw.Draw(img)
    kresli.rounded_rectangle([0, 0, n - 1, n - 1], radius=int(n * 0.22), fill=ORANZOVA)
    kresli.line(
        [(n * 0.26, n * 0.53), (n * 0.44, n * 0.71), (n * 0.75, n * 0.31)],
        fill=(255, 255, 255, 255), width=int(n * 0.115), joint="curve",
    )
    # konce cary zakulatit — ImageDraw.line umi jen ostre konce
    for x, y in ((0.26, 0.53), (0.75, 0.31)):
        r = n * 0.0575
        kresli.ellipse([n * x - r, n * y - r, n * x + r, n * y + r], fill=(255, 255, 255, 255))

    for velikost, jmeno in ((180, "favicon.png"), (32, "favicon-32.png")):
        uloz(zmens(img, velikost), ASSETS / jmeno)


def fotky() -> None:
    for jmeno in ("title-photo.jpg",):
        zdroj = ASSETS / jmeno
        if not zdroj.exists():
            continue
        print(zdroj.name)
        orig = Image.open(zdroj)
        uloz(orig, ASSETS / f"{zdroj.stem}.webp")
        maly = zmens(orig, 1024)
        uloz(maly, ASSETS / f"{zdroj.stem}-1024.jpg", 85)
        uloz(maly, ASSETS / f"{zdroj.stem}-1024.webp", 85)


if __name__ == "__main__":
    loga()
    logo_webu()
    bfk_znacka()
    favicon()
    fotky()
