#!/usr/bin/env python3
"""Obsah webu simulacni-zkousky.cz – jedna polozka STRANKY = jedna stranka.

ZKRACENO 13. 9. 2026 na zhruba polovinu puvodniho rozsahu (19 stranek misto 27).
Kolegum byl web prilis obsahly. Zustaly stranky kategorii A1 az D, baterie
a distributori; pryc jsou technicke detaily (slovnik, rozpadove misto, RTU,
zkousky ochran, katalogy zkousek 5.1-5.11 a simulaci 6.1-6.19) a UPOS, UTP, DVM
a podklady jsou spojene na strance Postup. Zkousky se popisuji jen po okruzich
(cinny vykon, jalovy vykon, ochrany, dalkove rizeni...), rozsah urcuje smlouva
o pripojeni. Podrobna verze je v gitu pod commitem c9d4806.

Pri zkracovani zapracovana kontrola faktu z 3. 9. 2026 – nevracet: "ochrany
baterie se lisi od FVE" (jsou shodne), "u B2 povinna cela kapitola simulaci",
DPO jako vysledek UPOS u B1/B2, formulare G97/G98 "k instalacnimu dokumentu",
"kapacita baterie" v telemetrii CEZ (je to stav nabiti), superlativy.

Zkratky: UPOS a UTP BEZ carky – tak je pise PPDS priloha 4 (Umozneni…).

Vecny podklad: interni reserse BFK (podklady/Reserse_web_simulacni_zkousky.pdf)
a kontrola faktu podklady/_KONTROLA_WEB_simulacni-zkousky_2026-09-03.md.
Na web zamerne NEDAVAT: ceny, dodaci lhuty, jmena vyrobcu pod NDA, nepotvrzene
reference. Otevrene body jsou v POZNAMKY-INTERNI.md.
"""

# ---------------------------------------------------------------- ikony ----
I = {
    "dok": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><path d="M14 2v6h6M9 13h6M9 17h4"/></svg>',
    "graf": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 3v18h18"/><path d="m7 15 4-6 3 3 4-7"/></svg>',
    "info": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 8v5M12 16h.01"/></svg>',
    "check": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M9 12l2 2 4-4"/><path d="M21 12c0 4.97-4.03 9-9 9s-9-4.03-9-9 4.03-9 9-9"/></svg>',
    "blesk": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M13 2 3 14h7l-1 8 10-12h-7l1-8z"/></svg>',
    "sit": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="9" y="2" width="6" height="6" rx="1"/><rect x="2" y="16" width="6" height="6" rx="1"/><rect x="16" y="16" width="6" height="6" rx="1"/><path d="M12 8v4M5 16v-2h14v2"/></svg>',
    "hodiny": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>',
    "stit": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M12 3l8 3v6c0 4.5-3.2 8.3-8 9.5C7.2 20.3 4 16.5 4 12V6z"/><path d="m9 12 2 2 4-4"/></svg>',
    "baterie": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="7" width="17" height="10" rx="2"/><path d="M22 11v2M6 11v2M10 11v2M14 11v2"/></svg>',
    "sipky": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M17 3l4 4-4 4M21 7H8M7 21l-4-4 4-4M3 17h13"/></svg>',
    "lupa": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><circle cx="11" cy="11" r="7"/><path d="m20 20-3.5-3.5"/></svg>',
    "tovarna": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M3 21V10l6 4V10l6 4V7l6 4v10z"/><path d="M3 21h18"/></svg>',
}


# ------------------------------------------------------------- pomocnici ---
def sekce(nadpis, telo, eyebrow=None, uvod=None, alt=False, kotva=None):
    hlavicka = ""
    if nadpis or uvod:
        eb = f'\n      <p class="eyebrow">{eyebrow}</p>' if eyebrow else ""
        h2 = f"\n      <h2>{nadpis}</h2>" if nadpis else ""
        u = f"\n      {uvod}" if uvod else ""
        hlavicka = f'    <div class="section-head">{eb}{h2}{u}\n    </div>\n'
    ida = f' id="{kotva}"' if kotva else ""
    return (f'<section class="block{" alt" if alt else ""}"{ida}>\n  <div class="container">\n'
            f'{hlavicka}{telo}\n  </div>\n</section>\n')


def karty(polozky, sloupce=2):
    """polozky = [(ikona, nadpis, html_telo, odkaz|None)]"""
    kusy = []
    for p in polozky:
        ikona, nadpis, telo = p[0], p[1], p[2]
        odkaz = p[3] if len(p) > 3 else None
        if odkaz:
            kusy.append(
                f'      <a class="svc" href="{odkaz}">\n'
                f'        <h3 class="hdr">{ikona}{nadpis}</h3>\n'
                f'        <div class="body">{telo}<span class="go">Otevřít →</span></div>\n'
                f'      </a>')
        else:
            kusy.append(
                f'      <article class="svc">\n'
                f'        <h3 class="hdr">{ikona}{nadpis}</h3>\n'
                f'        <div class="body">{telo}</div>\n'
                f'      </article>')
    trida = "services" + (" cols-2" if sloupce == 2 else "")
    return f'    <div class="{trida}">\n' + "\n".join(kusy) + "\n    </div>"


def tabulka(zahlavi, radky, poznamky=(), min_sirka=None):
    """Zahlavi s prazdnymi retezci = tabulka bez hlavicky (klic–hodnota)."""
    th = "".join(f"<th>{h}</th>" for h in zahlavi)
    hlava = "" if not any(zahlavi) else f"        <thead>\n          <tr>{th}</tr>\n        </thead>\n"
    tr = "\n".join(
        "          <tr>" + "".join(f"<td>{b}</td>" for b in r) + "</tr>" for r in radky)
    styl = f' style="min-width:{min_sirka}px"' if min_sirka else ""
    pozn = "\n".join(f'    <p class="spec-note">{p}</p>' for p in poznamky)
    return (f'    <div class="spec-table">\n      <table{styl}>\n{hlava}'
            f'        <tbody>\n{tr}\n        </tbody>\n      </table>\n    </div>\n{pozn}')


def kroky(polozky):
    """polozky = [(nadpis, text, stitek)]"""
    kusy = [f'      <article class="step">\n        <h3>{n}</h3>\n        <p>{t}</p>\n'
            f'        <span class="tag">{s}</span>\n      </article>' for n, t, s in polozky]
    return '    <div class="steps">\n' + "\n".join(kusy) + "\n    </div>"


def wp(polozky):
    kusy = [f'      <div class="wp-item"><span class="kod">{k}</span><p>{t}</p></div>'
            for k, t in polozky]
    return '    <div class="wp-list">\n' + "\n".join(kusy) + "\n    </div>"


def seznam(polozky):
    return ('    <ul class="checklist">\n'
            + "\n".join(f"      <li>{p}</li>" for p in polozky) + "\n    </ul>")


def cta(text, tlacitko="Nezávazná poptávka", href="kontakt.html#formular"):
    return (f'    <div class="seg-note">\n      <p>{text}</p>\n'
            f'      <a class="btn btn-primary" href="{href}">{tlacitko}</a>\n    </div>')


def callout(titul, text, warn=False):
    return (f'    <div class="callout{" warn" if warn else ""}">\n'
            f'      <span class="t">{titul}</span>\n      {text}\n    </div>')


def kotvy(polozky):
    return ('<ul class="anchor-nav">\n'
            + "\n".join(f'      <li><a href="#{h}">{t}</a></li>' for t, h in polozky)
            + "\n    </ul>")


ZDROJ = ('<p class="spec-note"><b>Zdroj:</b> {}</p>')

STRANKY = []

# =========================================================== DOMOVSKA ======
HERO = """<!-- HERO -->
<section class="hero">
  <div class="photo"><picture>
    <source type="image/webp" srcset="assets/title-photo-1024.webp 1024w, assets/title-photo.webp 2048w" sizes="100vw">
    <img src="assets/title-photo.jpg" alt="Fotovoltaická elektrárna na průmyslové střeše" width="2048" height="1536" fetchpriority="high" srcset="assets/title-photo-1024.jpg 1024w, assets/title-photo.jpg 2048w" sizes="100vw">
  </picture></div>
  <div class="gradient-overlay"></div>
  <div class="content">
    <p class="hero-eyebrow">BFK Systems &middot; ověření souladu s RfG</p>
    <h1>Simulační zkoušky a ověření souladu výroben</h1>
    <p class="hero-claim-big">Simulace souladu, zkoušky na místě a dokumentace pro distributora – od jedné firmy.</p>
    <p class="hero-lead">Bez doloženého souladu s&nbsp;RfG nevydá provozovatel distribuční soustavy (dále také distributor) souhlas s&nbsp;trvalým provozem výrobny. Od kategorie B1, tedy od 100&nbsp;kW, se část požadavků ověřuje simulací a část zkouškami přímo na výrobně. Děláme obojí – včetně žádostí o&nbsp;UPOS a&nbsp;UTP.</p>
    <p class="hero-claim">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>
      Fotovoltaické elektrárny a bateriová úložiště od 100 kW
    </p>
    <p class="hero-claim">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>
      Zkušenosti s FVE projekty až do 36 MWp
    </p>
    <div class="cta-row">
      <a class="btn btn-primary" href="kontakt.html#formular">Nezávazná poptávka</a>
      <a class="btn btn-light" href="proces-pripojeni.html">Jak to probíhá</a>
    </div>
  </div>
</section>
"""

STATISTIKY = ('<div class="stats-band">\n  <div class="container grid">\n'
              '      <div><div class="num">až 36 MWp</div><div class="label">Rozsah zpracovaných FVE projektů</div></div>\n'
              '      <div><div class="num">Desítky</div><div class="label">Protokolů ověření souladu</div></div>\n'
              '      <div><div class="num">3 distributoři</div><div class="label">ČEZ Distribuce · EG.D · PREdistribuce</div></div>\n'
              '  </div>\n</div>\n')

FAQ_CO_JSOU = (
    "Co jsou „simulační zkoušky“?",
    "<p>Běžné označení pro ověření souladu výrobny s RfG. Tvoří ho <b>simulace souladu</b> "
    "(výpočet na modelu výrobny) a <b>zkoušky na místě</b> (ověření na hotové elektrárně). "
    "Rozsah obojího určuje kategorie výrobny.</p>")
FAQ_OD_VYKONU = (
    "Od jakého výkonu se mě to týká?",
    "<p>Zkoušky na místě a simulace přicházejí od kategorie <b>B1, tedy od 100 kW</b>. Menší "
    "výrobny (A1, A2) dokládají soulad doklady ke střídači a instalačním dokumentem.</p>")
FAQ_KATEGORIE = (
    "Jak zjistím kategorii své výrobny?",
    '<p>Najdete ji ve <b>smlouvě o připojení</b>. Orientačně ji poznáte podle výkonu – '
    '<a href="index.html#kategorie">tabulka kategorií</a>. Když si nejste jistí, pošlete nám smlouvu.</p>')
FAQ_CIZI_STAVBA = (
    "Děláte to i pro elektrárny, které jste nestavěli?",
    "<p>Ano, je to velká část naší práce. Studie a zkoušky děláme pro jiné dodavatele fotovoltaiky "
    "i pro investory, kteří si stavbu zajistili sami. Potřebujeme podklady, ne vlastní stavbu.</p>")
FAQ_B1_VYJEZD = (
    "Musí k nám u kategorie B1 někdo přijet?",
    "<p>Ano, na zkoušky na místě – ověření regulace činného a jalového výkonu, ochran, komunikace "
    "s dispečinkem a opětovného připojení. Zbytek požadavků se doloží simulací nebo certifikátem.</p>")

STRANKY.append({
    "slug": "index.html",
    "nav": "",
    "title": "Simulační zkoušky a ověření souladu RfG | BFK Systems",
    "desc": "Ověření souladu výroben s RfG: simulace souladu, zkoušky na místě, Dokument výrobního "
            "modulu a žádosti o UPOS a UTP. Fotovoltaika i bateriová úložiště od 100 kW.",
    "prio": "1.0",
    "body": HERO + STATISTIKY + sekce(
        "Co pro vás uděláme",
        karty([
            (I["graf"], "Simulace souladu",
             "<p>Požadavky, které metodika umožňuje nebo vyžaduje ověřit simulací, prokážeme na modelu "
             "výrobny – typicky odezvu při změnách frekvence a napětí a chování při poruchách.</p>",
             "simulace-souladu.html"),
            (I["lupa"], "Zkoušky na místě",
             "<p>Ověření regulace činného a jalového výkonu, ochran, dálkového řízení a opětovného "
             "připojení přímo na výrobně. Rozsah podle smlouvy o připojení.</p>", "zkousky-na-miste.html"),
            (I["dok"], "Dokumentace a jednání s distributorem",
             "<p>Žádost o UPOS, protokoly, Dokument výrobního modulu, žádost o UTP a vypořádání "
             "připomínek distributora až do konečného provozního oznámení.</p>", "proces-pripojeni.html"),
            (I["baterie"], "Bateriová úložiště",
             "<p>Nové úložiště i doplnění baterie ke stávající fotovoltaice – ověření provozu při "
             "nabíjení i vybíjení a vlastní formuláře distributora.</p>", "bateriova-uloziste-zue.html"),
        ], sloupce=2),
        eyebrow="Služby",
        uvod='<p class="lead">Pojem „simulační zkoušky“ používáme jako souhrnné označení služeb. Odborně '
             'jde o <b>ověření souladu výrobny s nařízením (EU) 2016/631 (RfG)</b>, při kterém se '
             'požadavky dokládají simulacemi souladu, zkouškami souladu, nebo certifikáty zařízení – '
             'podle příslušné metodiky. Elektrárnu jsme stavět nemuseli – stačí nám podklady.</p>',
        kotva="sluzby",
    ) + sekce(
        "Kategorie výrobních modulů",
        tabulka(
            ["Kategorie", "Výkon", "Zkoušky na místě", "Simulace"],
            [['<a href="kategorie-a1.html">A1</a>', "0,8 až 11 kW", "standardně ne", "standardně ne"],
             ['<a href="kategorie-a2.html">A2</a>', "nad 11 kW, pod 100 kW", "standardně ne", "standardně ne"],
             ['<a href="kategorie-b1.html">B1</a>', "100 kW až pod 1 MW", "ano", "vybrané body"],
             ['<a href="kategorie-b2.html">B2</a>', "1 MW až pod 30 MW", "ano", "širší rozsah"],
             ['<a href="kategorie-c-d.html">C</a>', "30 MW až pod 75 MW", "ano", "nejširší rozsah"],
             ['<a href="kategorie-c-d.html">D</a>', "od 75 MW, nebo připojení na 110 kV", "ano",
              "nejširší rozsah"]],
            poznamky=[
                "<b>Kategorii najdete ve smlouvě o připojení</b> a ta je vždy rozhodující. U bateriových "
                "úložišť se zařazení a způsob ověření řídí aktuálními podmínkami příslušného distributora "
                "a v některých kategoriích se může od výroben lišit.",
                "<b>Pozor na jednotky:</b> výkon panelů v kWp není výkon, podle kterého se kategorie "
                "určuje. Rozhoduje jmenovitý činný výkon výrobního modulu – 698 kWp panelů může být "
                "modul s P<sub>n</sub> 550 kW.",
            ],
            min_sirka=640,
        ),
        eyebrow="Do které kategorie spadáte",
        uvod="<p>Rozsah ověření se odvíjí od kategorie výrobního modulu. Klikněte na kategorii – "
             "u každé je popsáno, co se dokládá a co distributor chce.</p>",
        alt=True, kotva="kategorie",
    ) + sekce(
        "Tři cesty, jak požadavek doložit",
        karty([
            (I["lupa"], "Zkouška na místě",
             "<p>Ověření na hotové výrobně a protokol. Některé požadavky jinak doložit nejde – "
             "u kategorie B1 jich je šest.</p>"),
            (I["graf"], "Simulace",
             "<p>Model výrobny a protokol s vyhodnocením splněno / nesplněno. U kategorie B2 a vyšších "
             "kategorií je rozsah simulací podstatně širší.</p>"),
            (I["dok"], "Certifikát zařízení",
             "<p>Vydává ho certifikátor pro konkrétní zařízení – náš protokol ze zkoušky nebo simulace "
             "certifikát není. Nahradí zkoušku nebo simulaci jen tam, kde to Dokument výrobního modulu "
             "připouští; u výrobny z více výrobních jednotek část bodů certifikátem nedoložíte.</p>"),
        ], sloupce=3)
        + callout(
            "Tady se láme rozsah prací i cena",
            "<p>Kterou cestou se který požadavek doloží, určuje Dokument výrobního modulu "
            "distributora. Proto se u dvou výkonově srovnatelných elektráren může rozsah ověření "
            "významně lišit podle počtu a typu výrobních jednotek.</p>"),
        eyebrow="Klíčový koncept", kotva="cesty",
    ) + sekce(
        "Jak to probíhá",
        kroky([
            ("Smlouva o připojení",
             "Určí kategorii výrobny a tím i rozsah ověření. Pošlete nám ji a řekneme vám, "
             "co vás čeká.", "Začátek"),
            ("Žádost o UPOS",
             "Připravíme a podáme žádost o umožnění provozu pro ověření souladu. Distributor "
             "rozhodne do 30 dnů od doložení kompletních podkladů.", "Vyřídíme za vás"),
            ("Zkoušky a simulace",
             "Provedeme je během dočasného provozu, který trvá nejdéle 12 měsíců.", "Naše práce"),
            ("Dokument výrobního modulu",
             "Výsledky shrneme do protokolů a Dokumentu výrobního modulu pro distributora.",
             "Naše práce"),
            ("Žádost o UTP",
             "Podáme žádost o umožnění trvalého provozu. Cílem je konečné provozní oznámení.",
             "Cíl"),
        ])
        + cta("<b>Načasování rozhoduje.</b> Dočasný provoz je omezený na 12 měsíců a zkoušky "
              "fotovoltaiky potřebují slunce. Čím dříve s ověřením souladu v harmonogramu počítáte, "
              "tím menší je riziko zdržení uvedení výrobny do trvalého provozu.",
              "Probrat termín"),
        eyebrow="Postup", alt=True, kotva="postup",
    ) + sekce(
        "Společný základ, vlastní podmínky",
        karty([
            (I["tovarna"], "ČEZ Distribuce",
             "<p>Připojovací podmínky pro VN a VVN od 1. 9. 2025 s technickými přílohami – ochrany, "
             "regulace jalového výkonu, telemetrie a test omezování výkonu.</p>", "cez-distribuce.html"),
            (I["tovarna"], "EG.D",
             "<p>Podklady pro dispečerské řízení a chránění decentrálních zdrojů (DEČE) a nové "
             "připojovací podmínky od 1. 2. 2026.</p>", "egd.html"),
            (I["tovarna"], "PREdistribuce",
             "<p>Spoluautor společných metodik ověřování souladu. K tomu vlastní podnikové normy "
             "a technické podmínky.</p>", "predistribuce.html"),
        ], sloupce=3),
        eyebrow="Distributoři",
        uvod="<p>Základní metodiky ověřování souladu jsou společné pro ČEZ Distribuci, EG.D "
             "a PREdistribuci. Konkrétní technické podmínky, telemetrie, formuláře a některé volitelné "
             "požadavky se řídí dokumenty příslušného distributora.</p>",
        kotva="pds",
    ) + sekce(
        "Co se v poslední době změnilo",
        karty([
            (I["dok"], "Končí přechodné období protokolů",
             "<p>U malých výroben (A1, A2) nahrazuje certifikát ke střídači i protokol laboratoře "
             "vydaný nejpozději 31. 12. 2025. EG.D a PREdistribuce ho uznávají do 31. 12. 2026.</p>",
             "kategorie-a2.html"),
            (I["baterie"], "Baterie mají vlastní pravidla",
             "<p>ČEZ Distribuce vydala k 1. 9. 2025 dodatky k připojovacím podmínkám pro zařízení "
             "pro ukládání elektřiny. Úložiště má vlastní dokument ověřování souladu.</p>",
             "bateriova-uloziste-zue.html"),
            (I["sit"], "Nové připojovací podmínky",
             "<p>ČEZ Distribuce má nové podmínky pro VN a VVN od 1. 9. 2025, EG.D pro VN a VVN "
             "od 1. 2. 2026.</p>", "cez-distribuce.html"),
        ], sloupce=3),
        eyebrow="Aktuálně", alt=True, kotva="aktualne",
    ),
    "faq_nadpis": "Nejčastější dotazy",
    "faq": [FAQ_CO_JSOU, FAQ_OD_VYKONU, FAQ_KATEGORIE, FAQ_B1_VYJEZD, FAQ_CIZI_STAVBA],
})

# ========================================================== KATEGORIE ======
BC_KAT = [("Kategorie výroben", "index.html#kategorie")]

STRANKY.append({
    "slug": "kategorie-a1.html", "nav": "kategorie", "reviewed": True,
    "title": "Výrobní modul A1 – připojení FVE od 0,8 do 11 kW",
    "desc": "Kategorie A1 (0,8 až 11 kW): soulad se prokazuje instalačním dokumentem a doklady ke "
            "střídači, zkoušky na výrobně ani simulace se standardně nevyžadují. Co po vás distributor chce.",
    "eyebrow": "Kategorie výrobního modulu", "h1": "Výrobní modul A1 – 0,8 až 11 kW",
    "bc_nazev": "Kategorie A1", "breadcrumb": BC_KAT,
    "intro": "<p>Nejmenší kategorie – prakticky každá domácí fotovoltaika. U kategorie A1 se "
             "<b>zkoušky na výrobně ani simulace standardně neprovádějí</b>. Soulad se prokazuje "
             "instalačním dokumentem a požadovanými doklady k zařízení; jejich úplnost a vzájemný "
             "soulad jsou podmínkou trvalého provozu.</p>",
    "stats": [("0,8 až 11 kW", "Rozsah kategorie A1"), ("Instalační dokument", "Místo zkoušek a simulací")],
    "body": sekce(
        "Co pro A1 platí",
        karty([
            (I["blesk"], "Rozsah a připojení",
             "<p>Od 0,8 kW do 11 kW včetně, zpravidla do sítě nízkého napětí. Jednofázové připojení "
             "je omezeno na <b>3,7 kVA na fázi</b>.</p>"),
            (I["dok"], "Instalační dokument místo DVM",
             "<p>Soulad se prokazuje <b>instalačním dokumentem výrobního modulu</b> ve verzi platné od "
             "1. 1. 2025 a doklady k zařízení. Podepisuje ho firma, která instalaci provedla, "
             "i žadatel.</p>"),
            (I["check"], "Certifikát, nebo protokol",
             "<p>Ke střídači se dokládá <b>certifikát zařízení od certifikátora</b>, přechodně "
             "i protokol odborné laboratoře, případně výjimka ERÚ. Protokol musí být vydaný nejpozději "
             "31. 12. 2025; EG.D a PREdistribuce ho uznávají do 31. 12. 2026.</p>"),
            (I["hodiny"], "Bez dočasného provozu",
             "<p>U kategorií A1 a A2 nahrazuje proces UPOS předložení instalačního dokumentu. "
             "Žádost o trvalý provoz se podává po splnění podmínek smlouvy o připojení.</p>"),
        ]),
        eyebrow="Fakta",
    ) + sekce(
        "Co po vás distributor bude chtít",
        seznam([
            "Splnění podmínek smlouvy o připojení",
            "Vyplněný a podepsaný instalační dokument výrobního modulu",
            "Certifikát nebo protokol ke střídači",
            "Výchozí revizi elektrického zařízení výrobny, případně i přípojky",
            "Projektovou dokumentaci nebo jednopólové schéma",
            "Protokol o nastavení ochran",
            "Potvrzení montážní firmy, že výrobna odpovídá smlouvě o připojení",
        ]) + callout(
            "Zkontrolujte si doklad ke střídači",
            "<p>Z naší praxe bývá u malých elektráren zádrhelem hlavně doklad ke střídači: "
            "certifikát nemusí pokrývat všechny požadavky instalačního dokumentu a u protokolu "
            "laboratoře je potřeba hlídat datum vydání. Ověříme, co váš střídač doloží a co bude "
            "potřeba doplnit.</p>"),
        eyebrow="Checklist", alt=True,
    ),
    "faq": [
        ("Musím u malé fotovoltaiky dělat nějaké zkoušky?",
         "<p>U standardního postupu A1 se samostatné zkoušky na hotové výrobně ani simulační studie "
         "nevyžadují – soulad se dokládá instalačním dokumentem a doklady ke střídači. Distributor je "
         "ale při uvádění do trvalého provozu oprávněn výrobnu zkontrolovat a vyzkoušet a způsob "
         "doložení se řídí jeho aktuálními požadavky.</p>"),
        ("Kdo instalační dokument podepisuje?",
         "<p>Firma, která instalaci provedla – potvrzuje typ a nastavení zařízení – a žadatel, "
         "který potvrzuje doložení souladu.</p>"),
        ("Střídač má certifikát ze zahraničí. Platí v Česku?",
         "<p>Uznatelnost certifikátu se posuzuje podle rozsahu akreditace, příslušné metodiky "
         "a aktuálních požadavků konkrétního distributora. Zahraniční certifikát proto ověřujeme ještě "
         "před podáním žádosti. Samotné prohlášení výrobce nestačí.</p>"),
    ],
    "cross": [("Kategorie A2", "kategorie-a2.html"),
              ("Postup a podklady", "proces-pripojeni.html"), ("Časté dotazy", "faq.html")],
})

STRANKY.append({
    "slug": "kategorie-a2.html", "nav": "kategorie", "reviewed": True,
    "title": "Výrobní modul A2 (nad 11 kW, pod 100 kW) – doklad ke střídači",
    "desc": "Kategorie A2 (nad 11 kW a pod 100 kW): soulad se dokládá certifikátem nebo protokolem ke střídači "
            "přes instalační dokument. Bez zkoušek a simulací. Co dělat, když certifikát nestačí.",
    "eyebrow": "Kategorie výrobního modulu", "h1": "Výrobní modul A2 – nad 11 kW, pod 100 kW",
    "claim": "Rozhoduje doklad k vašemu střídači.",
    "bc_nazev": "Kategorie A2", "breadcrumb": BC_KAT,
    "intro": "<p>Typická firemní střešní elektrárna. Stejně jako u A1 se zkoušky na výrobně ani "
             "simulace standardně neprovádějí – požadavky jsou ale širší a rozhoduje, co má doložené "
             "váš střídač.</p>",
    "stats": [("nad 11 kW, pod 100 kW", "Rozsah kategorie A2"), ("Instalační dokument", "Místo zkoušek a simulací")],
    "body": sekce(
        "Co pro A2 platí",
        karty([
            (I["blesk"], "Rozsah a požadavky",
             "<p>Nad 11 kW a pod 100 kW, zpravidla nízké napětí. Proti kategorii A1 přibývají "
             "<b>vybrané požadavky kategorie B</b>, které musí doklad ke střídači pokrýt.</p>"),
            (I["dok"], "Instalační dokument A2",
             "<p>Soulad se dokládá instalačním dokumentem ve verzi platné od 1. 1. 2025 a doklady "
             "k zařízení. Je-li certifikátů více, uvádí se, na jaké zařízení a požadavek byl který "
             "vydán.</p>"),
        ], sloupce=2),
        eyebrow="Fakta",
    ) + sekce(
        "Co dělat, když certifikát nepokrývá všechno",
        "<p class=\"lead\">Situace, kterou řešíme nejčastěji: elektrárna stojí, ale doklady ke střídači "
        "jsou starší a část požadavků instalačního dokumentu nepokrývají. Postup je vždy stejný.</p>"
        + wp([
            ("1", "Projdeme instalační dokument bod po bodu proti tomu, co certifikát skutečně obsahuje."),
            ("2", "Vyžádáme od výrobce doplňující certifikát nebo verzi k danému firmwaru."),
            ("3", "Když doplnit nejde, navrhneme řešení – jiné zařízení nebo úpravu konfigurace."),
            ("4", "Zkompletujeme dokumentaci a podáme ji distributorovi."),
        ])
        + callout(
            "Končí přechodné období protokolů laboratoří",
            "<p>Protokol z laboratoře ČEZ Distribuce nebo EG.D nahrazuje certifikát jen tehdy, byl-li "
            "<b>vydaný nejpozději 31. 12. 2025</b>. EG.D a PREdistribuce ho uznávají <b>do 31. 12. 2026</b>, "
            "pak už jen certifikát. ČEZ Distribuce uvádí, že protokoly akceptuje po dobu jejich "
            "platnosti. Máte-li podklady ze starší instalace, zkontrolujte je včas.</p>"),
        eyebrow="Praxe", alt=True,
    ),
    "faq": [
        ("Potřebuju u A2 simulační studii?",
         "<p>U standardního postupu A1 a A2 se simulační studie nevyžaduje – způsob doložení souladu "
         "se řídí instalačním dokumentem a požadavky příslušného distributora. Zlom je na 100 kW, kde "
         "začíná kategorie B1.</p>"),
        ("Mám 99 kW. Nevyplatí se přidat kilowatt?",
         "<p>Rozhodně ne bez rozmyslu – od 100 kW spadáte do kategorie B1 a proces se výrazně "
         "rozšíří: dočasný provoz pro ověření, zkoušky na místě a Dokument výrobního modulu.</p>"),
    ],
    "cross": [("Kategorie B1 – od 100 kW", "kategorie-b1.html"),
              ("Kategorie A1 – 0,8 až 11 kW", "kategorie-a1.html"), ("Časté dotazy", "faq.html")],
})

STRANKY.append({
    "slug": "kategorie-b1.html", "nav": "kategorie", "reviewed": True,
    "title": "Ověření souladu B1 – výrobny 100 kW až pod 1 MW",
    "desc": "Kategorie B1: zkoušky na místě, zbytek požadavků simulací nebo certifikátem. Společná "
            "metodika ČEZ Distribuce, EG.D a PREdistribuce platná od 1. 2. 2025.",
    "eyebrow": "Kategorie výrobního modulu", "h1": "Ověření souladu B1 – 100 kW až pod 1 MW",
    "claim": "Velkou část požadavků lze doložit bez zkoušky na místě.",
    "bc_nazev": "Kategorie B1", "breadcrumb": BC_KAT,
    "intro": "<p>První kategorie, u které metodika ověřování souladu vyžaduje vybrané zkoušky přímo "
             "na výrobně. Od 100 kW přichází dočasný provoz pro ověření souladu a Dokument výrobního "
             "modulu. Jen zkouškou na místě jde doložit šest bodů – <b>ostatní požadavky lze doložit "
             "i simulací nebo certifikátem</b>.</p>",
    "stats": [("16 / 18", "Bodů (synchronní / nesynchronní)"),
              ("6", "Bodů jen zkouškou na místě"),
              ("12 měsíců", "Nejdelší dočasný provoz")],
    "body": sekce(
        "Jedna metodika pro tři distributory",
        karty([
            (I["dok"], "Společná metodika",
             "<p>Metodika ověřování souladu B1 je <b>společná pro ČEZ Distribuce, EG.D i PREdistribuce</b> "
             "a platí od 1. 2. 2025. Pokrývá synchronní (16 bodů) i nesynchronní (18 bodů) moduly.</p>"),
            (I["blesk"], "Fotovoltaika má dva body navíc",
             "<p>Nesynchronní moduly – fotovoltaika a bateriová úložiště – dokládají navíc "
             "<b>rychlý poruchový proud</b> a <b>přednost jalového výkonu před činným</b>.</p>"),
            (I["hodiny"], "Rok na dokončení",
             "<p>Ověření se dokončuje v rámci dočasného provozu po UPOS. Ten platí nejdéle "
             "<b>12 měsíců</b> podle harmonogramu, který se předkládá se žádostí.</p>"),
            (I["info"], "Závady proces zastaví",
             "<p>Při špatně nastavených ochranách nebo nefunkčním opětovném připojení může distributor "
             "UPOS přerušit nebo ukončit a informuje o tom na místě, nebo písemně do 15 pracovních "
             "dnů od zjištění závady.</p>"),
        ]),
        eyebrow="Fakta",
    ) + sekce(
        "Šest zkoušek na výrobně",
        wp([
            ("1", "Řízení činného výkonu"),
            ("2", "Automatické opětovné připojení po výpadku sítě"),
            ("3", "Komunikace s dispečinkem distributora"),
            ("4", "Regulace napětí a jalového výkonu"),
            ("5", "Nastavení ochran"),
            ("6", "Omezování činného výkonu"),
        ]) + callout(
            "Tohle nejde obejít",
            "<p>Tyto body nenahradí simulace ani certifikát. Zkoušky se provádějí <b>na celé "
            "výrobně</b>, ne na jednom střídači – a obvykle je zvládneme jedním výjezdem. "
            "<a href=\"zkousky-na-miste.html\">Jak zkoušky probíhají →</a></p>", warn=True),
        eyebrow="Zkoušky na místě", alt=True,
    ) + sekce(
        "Ostatní požadavky",
        "<p class=\"lead\">Ostatní body lze prokázat i <b>simulací nebo certifikátem</b>. Která cesta "
        "bude výhodnější, se rozhoduje podle konfigurace střídačů.</p>"
        + karty([
            (I["graf"], "Simulace celé výrobny",
             "<p>Model výrobny pokryje elektrárnu bez ohledu na počet střídačů.</p>",
             "simulace-souladu.html"),
            (I["dok"], "Certifikát zařízení",
             "<p>U části bodů použitelný jen u výrobny z jedné výrobní jednotky. "
             "U více jednotek se tyto body dokládají zkouškou nebo simulací celé výrobny.</p>"),
        ])
        + cta("<b>Máte více střídačů?</b> Napište nám jejich počet a typ a kategorii ze smlouvy "
              "o připojení – obratem víte, co půjde certifikáty a co simulací."),
        eyebrow="Simulace nebo certifikát",
    ),
    "faq": [
        ("Musí k nám na B1 přijet technik?",
         "<p>Ano – na šest zkoušek na místě. Zbytek se dokládá simulacemi, certifikáty a vyplněným "
         "Dokumentem výrobního modulu.</p>"),
        ("Jak dlouho ověření B1 trvá?",
         "<p>Dočasný provoz platí nejdéle 12 měsíců podle předloženého harmonogramu. Reálný termín "
         "závisí hlavně na podkladech, koordinaci s dispečinkem a u fotovoltaiky na počasí.</p>"),
        ("Co když zkouška napoprvé neprojde?",
         "<p>Není to konec projektu. Typicky se upraví nastavení střídačů nebo ochran a domluví se nový "
         "termín. Proto děláme simulace dříve než zkoušky.</p>"),
    ],
    "cross": [("Zkoušky na místě", "zkousky-na-miste.html"), ("Simulace souladu", "simulace-souladu.html"),
              ("Postup a podklady", "proces-pripojeni.html"), ("Kategorie B2", "kategorie-b2.html")],
})
STRANKY.append({
    "slug": "kategorie-b2.html", "nav": "kategorie", "reviewed": True,
    "title": "Simulace souladu B2 – výrobny 1 MW až pod 30 MW",
    "desc": "Kategorie B2: výrazně širší rozsah simulací souladu, předání modelů výrobny distributorovi "
            "a zkoušky na místě. Co se mění proti B1 a jak to stihnout.",
    "eyebrow": "Kategorie výrobního modulu", "h1": "Simulace souladu B2 – 1 MW až pod 30 MW",
    "claim": "Oproti B1 se výrazně rozšiřuje rozsah simulací a práce s modely.",
    "bc_nazev": "Kategorie B2", "breadcrumb": BC_KAT,
    "intro": "<p>Od 1 MW se rozsah ověření zásadně mění. K zkouškám na místě přibývá <b>výrazně širší "
             "rozsah simulací</b> a předání modelů výrobny distributorovi.</p>",
    "stats": [("24 / 27", "Bodů (synchronní / nesynchronní)"),
              ("Modely", "Předávají se distributorovi"),
              ("12 měsíců", "Nejdelší dočasný provoz")],
    "body": sekce(
        "Co se mění proti kategorii B1",
        karty([
            (I["graf"], "Širší simulace",
             "<p>Oproti B1 se výrazně rozšiřuje rozsah požadavků a práce s modely výrobního modulu. "
             "U řady požadavků – chování při poruchách v síti, odezva na změny frekvence, napěťová "
             "stabilita – je simulace jednou z přípustných nebo požadovaných forem doložení. Konkrétní "
             "způsob určuje aktuální metodika a Dokument výrobního modulu.</p>"),
            (I["sipky"], "Předání modelů",
             "<p>Distributor u B2 požaduje modely výrobny ve formě strukturních a blokových diagramů "
             "se vstupními daty a výstupy. Plné simulační modely se předávají na jeho žádost.</p>"),
            (I["blesk"], "Přebírá požadavky kategorie C",
             "<p>B2 přejímá vybrané požadavky kategorie C – v praxi „malé C“. Některé z nich, "
             "například umělou setrvačnost, distributoři požadují jen výběrově.</p>"),
            (I["lupa"], "Zkoušky na místě zůstávají",
             "<p>Zkoušky se nikam neztrácejí – rozsah je obdobný jako u B1. Simulace je nenahrazují, "
             "doplňují.</p>"),
        ]),
        eyebrow="Rozdíl",
    ) + sekce(
        "Riziko není technika, ale kalendář",
        "<p class=\"lead\">Dočasný provoz trvá nejdéle 12 měsíců a v té době musí být hotové simulace, "
        "zkoušky, protokoly i Dokument výrobního modulu. Když se model vrátí k přepracování, čas "
        "ubývá rychle.</p>"
        + karty([
            (I["info"], "Proč distributor vrací simulace",
             "<p>Častým důvodem bývá nesoulad modelu se skutečnou konfigurací výrobny nebo neúplné "
             "protokoly. Obojí jde ošetřit ještě před odevzdáním.</p>"),
            (I["hodiny"], "Simulace dříve než zkoušky",
             "<p>Simulace zpravidla odhalí, co je potřeba přenastavit, ještě před zkouškami "
             "na výrobně.</p>"),
        ], sloupce=2)
        + cta("Proti B1 se u B2 významně rozšiřuje rozsah simulací a požadovaných modelů. "
              "<b>Pošlete nám smlouvu o připojení</b> a předem stanovíme konkrétní rozsah ověření."),
        eyebrow="Praxe", alt=True,
    ),
    "faq": [
        ("Proč distributor chce model výrobny?",
         "<p>Počítá s ním chování sítě v místě připojení. Předání ověřených modelů je u B2 samostatný "
         "požadavek, který nejde nahradit certifikátem.</p>"),
        ("Máme střídače bez modelu od výrobce. Co teď?",
         "<p>Část dynamických modelů máme k dispozici od výrobců, u zbytku se model ověřuje proti "
         "měření. Řekněte nám typ střídače a ověříme, na čem jsme.</p>"),
        ("Co když simulace nevyjdou?",
         "<p>Upraví se nastavení výrobních jednotek nebo ochran a test se opakuje. Odhalení nesouladu "
         "v modelu zpravidla umožní provést úpravy ještě před zkouškami na výrobně.</p>"),
    ],
    "cross": [("Simulace souladu", "simulace-souladu.html"), ("Zkoušky na místě", "zkousky-na-miste.html"),
              ("Kategorie C a D", "kategorie-c-d.html"), ("Postup a podklady", "proces-pripojeni.html")],
})

STRANKY.append({
    "slug": "kategorie-c-d.html", "nav": "kategorie", "reviewed": True,
    "title": "Kategorie C a D – od 30 MW a připojení na 110 kV",
    "desc": "Kategorie C (30 MW až pod 75 MW) a D (od 75 MW nebo připojení na 110 kV): nejširší rozsah zkoušek "
            "i simulací a vlastní dokumenty. Kdy výrobna spadne do kategorie D.",
    "eyebrow": "Kategorie výrobního modulu", "h1": "Kategorie C a D – od 30 MW a 110 kV",
    "bc_nazev": "Kategorie C a D", "breadcrumb": BC_KAT,
    "intro": "<p>Nejnáročnější režim ověřování: zkoušky na místě i simulace souladu v nejširším "
             "rozsahu. Rozsah i požadavky distributora se u těchto výkonů řeší individuálně.</p>",
    "stats": [("30 MW až pod 75 MW", "Kategorie C"), ("od 75 MW nebo 110 kV", "Kategorie D")],
    "body": sekce(
        "Dvě cesty do kategorie D",
        karty([
            (I["blesk"], "Podle výkonu",
             "<p>Kategorie C je od 30 MW včetně až pod 75 MW, kategorie D od 75 MW.</p>"),
            (I["sit"], "Podle napěťové hladiny",
             "<p>Podle čl. 5 RfG spadá do kategorie D i výrobna připojená <b>na 110 kV a výše bez ohledu "
             "na výkon</b>. "
             "Fotovoltaika 30 MW na hladině 110 kV je tedy kategorie D, ne C.</p>"),
        ], sloupce=2) + callout(
            "Rozhoduje smlouva o připojení",
            "<p>Než podle výkonu odhadnete rozsah prací, podívejte se do smlouvy o připojení – "
            "u projektů na hranici kategorií se rozsah ověření může výrazně lišit.</p>"),
        eyebrow="Zařazení",
    ) + sekce(
        "Co se ověřuje",
        karty([
            (I["graf"], "Nejširší simulace",
             "<p>Simulace pokrývají chování při poruchách, frekvenční odezvu, napěťovou stabilitu "
             "i další požadavky. Část testů se dělá jen na vyžádání distributora – rozsah proto "
             "potvrzujeme předem.</p>"),
            (I["dok"], "Vlastní dokumenty",
             "<p>Pro typ D existuje samostatný dokument ověřování souladu, pro bateriová úložiště "
             "typu D vlastní verze platná od 1. 9. 2025.</p>"),
            (I["sipky"], "Připojení na pokyn dispečinku",
             "<p>U kategorie D je automatické opětovné připojení zakázané – výrobna se po výpadku "
             "připojuje na pokyn dispečinku distributora.</p>"),
        ], sloupce=3),
        eyebrow="Rozsah", alt=True,
    ) + sekce(
        "Máme to rozpracované",
        '<p class="lead">Aktuálně zpracováváme fotovoltaickou elektrárnu o výkonu přibližně 30 MW '
        'připojenou na hladině 110 kV – kategorie D, distribuční území EG.D.</p>'
        + cta("Chystáte projekt kategorie C nebo D? Ozvěte se co nejdříve, ideálně před podpisem "
              "smlouvy o připojení.", "Domluvit konzultaci"),
        eyebrow="Reference",
    ),
    "faq": [
        ("Proč je fotovoltaika 30 MW na 110 kV kategorie D?",
         "<p>Do kategorie D spadá každý výrobní modul připojený na 110 kV a výše – bez ohledu "
         "na výkon.</p>"),
        ("Kdy s ověřením u projektu C nebo D začít?",
         "<p>Ideálně před podpisem smlouvy o připojení. Rozsah simulací a požadavky distributora se "
         "u těchto výkonů řeší individuálně a zaberou nejvíce času.</p>"),
    ],
    "cross": [("Simulace souladu", "simulace-souladu.html"), ("Kategorie B2", "kategorie-b2.html"),
              ("Reference", "reference.html")],
})

STRANKY.append({
    "slug": "bateriova-uloziste-zue.html", "nav": "kategorie", "reviewed": True,
    "title": "Bateriová úložiště – připojení a ověření souladu",
    "desc": "Bateriové úložiště (ZUE): zařazení do kategorií, ověření souladu při nabíjení i vybíjení, "
            "vlastní formuláře distributorů a co je jinak než u fotovoltaiky.",
    "eyebrow": "Akumulace", "h1": "Bateriová úložiště – ověření souladu",
    "claim": "Zařazení podle podmínek distributora, ověření v obou směrech.",
    "bc_nazev": "Bateriová úložiště", "breadcrumb": BC_KAT,
    "intro": "<p>Zařízení pro ukládání elektřiny – v předpisech <b>ZUE</b>, v praxi nejčastěji "
             "bateriové úložiště – má od 1. 9. 2025 vlastní pravidla. Platí pro baterii totéž co pro "
             "fotovoltaiku? Z velké části ano, ale ne úplně.</p>",
    "stats": [("1. 9. 2025", "Pravidla pro akumulaci"), ("Oba směry", "Nabíjení i vybíjení")],
    "body": sekce(
        "Co pro úložiště platí",
        karty([
            (I["dok"], "Vlastní pravidla a formuláře",
             "<p>ČEZ Distribuce vydala k 1. 9. 2025 dodatky k připojovacím podmínkám pro zařízení "
             "pro ukládání elektřiny. K úložišti se vyplňuje vlastní dokument ověřování souladu.</p>"),
            (I["blesk"], "Zařazení podle podmínek distributora",
             "<p>Zařazení bateriového úložiště a způsob prokázání souladu se řídí aktuálními pravidly provozování distribučních soustav (PPDS) "
             "a dokumenty příslušného distributora. U menších úložišť se používají instalační "
             "dokumenty obdobně jako u kategorií A1 a A2, od 100 kW proces ověření souladu. Přesné "
             "zařazení vždy ověřujeme podle smlouvy o připojení a dokumentace distributora.</p>"),
            (I["hodiny"], "Obdobný postup",
             "<p>Od 100 kW obdobně jako u výrobny: UPOS, dočasný provoz nejdéle 12 měsíců, zkoušky "
             "a simulace a žádost o UTP.</p>"),
            (I["sit"], "Rozšířená telemetrie a řízení",
             "<p>U úložišť s požadavkem na dispečerské řízení se přenáší také stav nabití a distributor "
             "může požadovat omezení dodávky i odběru činného výkonu.</p>"),
        ]),
        eyebrow="Pravidla",
    ) + sekce(
        "Ověřuje se v obou směrech",
        "<p class=\"lead\">To je hlavní rozdíl proti fotovoltaice. Požadavky se prokazují při "
        "<b>vybíjení i nabíjení</b>, včetně přechodů mezi nimi. Podpora napětí jalovým výkonem se "
        "posuzuje pro oba směry činného výkonu.</p>"
        + cta("Doplnění baterie je v naší praxi častým důvodem, proč se ověření souladu řeší znovu "
              "u elektrárny, která už běží. <b>Napište nám výkon a kapacitu úložiště</b> a jestli jde "
              "o nový projekt, nebo doplnění ke stávající FVE."),
        eyebrow="Nabíjení i vybíjení", alt=True,
    ),
    "faq": [
        ("Platí pro baterii stejné zkoušky jako pro fotovoltaiku?",
         "<p>Postup je obdobný, ale ne totožný. Ověřuje se provoz při nabíjení i vybíjení, úložiště "
         "má vlastní dokument ověřování souladu a zařazení se řídí podmínkami příslušného "
         "distributora.</p>"),
        ("Můžeme s baterií poskytovat podpůrné služby?",
         "<p>Podmínky pro podpůrné služby jsou nad rámec ověření souladu a řeší se zvlášť – "
         "s distributorem, provozovatelem přenosové soustavy a agregátorem.</p>"),
        ("Jak často se přezkušují ochrany?",
         "<p>Podle PPDS, přílohy 4 (kap. 12.4) se spínače, ochrany a vybavení pro dálkové řízení "
         "u výroben i úložišť funkčně přezkušují nejméně jednou za čtyři roky. Výsledek se dokládá "
         "zkušebním protokolem, který zůstává u provozovatele a na požádání se předkládá distributorovi. "
         "Na tuhle povinnost se po uvedení do trvalého provozu snadno zapomene.</p>"),
    ],
    "cross": [("Přidání baterie ke stávající FVE", "pridani-baterie-k-fve.html"),
              ("Zkoušky na místě", "zkousky-na-miste.html"), ("Postup a podklady", "proces-pripojeni.html")],
})

STRANKY.append({
    "slug": "pridani-baterie-k-fve.html", "nav": "kategorie", "reviewed": True,
    "title": "Přidání baterie ke stávající FVE – co vás čeká",
    "desc": "Doplnění bateriového úložiště k běžící fotovoltaice: posouzení připojitelnosti, úprava "
            "smlouvy o připojení, ověření souladu úložiště a rozšíření telemetrie.",
    "eyebrow": "Častý dotaz", "h1": "Přidání baterie ke stávající fotovoltaice",
    "claim": "Není to jen montáž. Je to změna připojení.",
    "bc_nazev": "Přidání baterie k FVE", "breadcrumb": BC_KAT,
    "intro": "<p>Elektrárna běží, má konečné provozní oznámení a majitel k ní chce doplnit baterii. "
             "Samotná montáž je rychlá. Administrativně jde ale o <b>změnu zařízení, kterou je potřeba "
             "projednat s distributorem</b> – a právě ta bývá časově náročnější než montáž.</p>",
    "body": sekce(
        "Čtyři věci, které je potřeba vyřešit",
        wp([
            ("1", "<b>Posouzení připojitelnosti.</b> Doplnění úložiště distributor posuzuje znovu."),
            ("2", "<b>Úprava smlouvy o připojení.</b> Úložiště se k připojení doplňuje, zpravidla "
                  "dodatkem ke smlouvě."),
            ("3", "<b>Ověření souladu úložiště.</b> Vlastní dokument ověřování souladu a ověření "
                  "provozu při nabíjení i vybíjení."),
            ("4", "<b>Rozšíření telemetrie.</b> Vyžaduje-li distributor dispečerské řízení, doplní se "
                  "signály úložiště a znovu se ověří přenos dat do dispečinku."),
        ]) + callout(
            "Časté nedorozumění",
            "<p>„Baterie je za střídačem, distributora to nezajímá.“ Zajímá – úložiště mění chování "
            "odběrného místa v obou směrech.</p>"),
        eyebrow="Postup",
    ) + sekce(
        "Kdy je to jednoduché a kdy ne",
        karty([
            (I["check"], "Jednodušší případ",
             "<p>Elektrárna do 100 kW (kategorie A1 nebo A2), hybridní střídač s certifikátem, který "
             "úložiště pokrývá. Vystačí doklady a úprava smlouvy.</p>"),
            (I["info"], "Náročnější případ",
             "<p>Elektrárna od 100 kW, více střídačů, samostatný bateriový střídač. Přichází simulace, "
             "zkoušky na místě a nový dočasný provoz pro ověření.</p>"),
        ], sloupce=2)
        + cta("<b>Nevíte, do které skupiny patříte?</b> Pošlete smlouvu o připojení, jednopólové "
              "schéma a typ střídače – obratem řekneme, co doplnění baterie obnáší."),
        eyebrow="Dva scénáře", alt=True,
    ),
    "faq": [
        ("Přijdu o konečné provozní oznámení?",
         "<p>Provozní oznámení se váže k výrobně v původní konfiguraci. Doplněním úložiště se "
         "konfigurace mění, proto se uvedení do provozu pro nové zařízení opakuje v rozsahu, který "
         "stanoví distributor.</p>"),
        ("Zvládneme to bez odstávky elektrárny?",
         "<p>Samotná montáž vyžaduje krátkou odstávku. Delší je fáze ověřování – v dočasném provozu "
         "se smí vyrábět za podmínek stanovených distributorem.</p>"),
    ],
    "cross": [("Bateriová úložiště", "bateriova-uloziste-zue.html"),
              ("Postup a podklady", "proces-pripojeni.html"), ("Kontakt", "kontakt.html")],
})

# ======================================================= DISTRIBUTORI ======
BC_PDS = [("Distributoři", "index.html#pds")]

STRANKY.append({
    "slug": "cez-distribuce.html", "nav": "pds", "reviewed": True,
    "title": "ČEZ Distribuce – připojovací podmínky a ověření souladu",
    "desc": "Ověření souladu výrobny na území ČEZ Distribuce: připojovací podmínky VN/VVN od 1. 9. 2025, "
            "technické přílohy, telemetrie a test omezování činného výkonu před trvalým provozem.",
    "eyebrow": "Distributor", "h1": "ČEZ Distribuce",
    "claim": "Co je specifické pro území ČEZ Distribuce.",
    "bc_nazev": "ČEZ Distribuce", "breadcrumb": BC_PDS,
    "intro": "<p>Základní metodiky ověřování souladu jsou společné pro ČEZ Distribuci, EG.D "
             "a PREdistribuci. <b>Technické podmínky, ochrany, telemetrie, formuláře</b> a některé "
             "volitelné požadavky se ale řídí dokumenty příslušného distributora. Tady je to, co je "
             "specifické pro ČEZ Distribuci.</p>",
    "stats": [("1. 9. 2025", "Platnost připojovacích podmínek"), ("VP_01 – VP_15", "Technické přílohy")],
    "body": sekce(
        "Co platí od 1. 9. 2025",
        karty([
            (I["dok"], "Připojovací podmínky VN a VVN",
             "<p>Platí od <b>1. 9. 2025</b> a nahradily verzi z roku 2023. Technické požadavky jsou "
             "v přílohách VP_01 až VP_15.</p>"),
            (I["stit"], "Ochrany a jalový výkon",
             "<p>Hodnoty ochran předepisuje příloha VP_05. Jalový výkon se podle velikosti výrobny "
             "řídí buď autonomní charakteristikou Q(U), nebo dálkově z dispečinku.</p>"),
            (I["sit"], "Telemetrie",
             "<p>Řídicí a komunikační jednotka podle VP_06 a funkční zkouška přenosu dat do "
             "dispečinku, kterou je potřeba domluvit s předstihem.</p>"),
            (I["baterie"], "Akumulace",
             "<p>Pro zařízení pro ukládání elektřiny platí dodatky č. 1 a 2 – posouzení "
             "připojitelnosti a proces uvedení do provozu.</p>"),
        ]),
        eyebrow="Připojovací podmínky",
    ) + sekce(
        "Test omezování činného výkonu",
        "<p class=\"lead\">Specifikum ČEZ Distribuce, o kterém řada provozovatelů neví: fyzický test "
        "omezování činného výkonu provádí uživatel sám a jeho <b>protokol je povinnou přílohou "
        "žádosti o UTP</b>. Bez něj distributor žádost nepřijme jako úplnou.</p>"
        + cta("Test si můžete udělat sami – nebo přijedeme, změříme ho a vystavíme protokol "
              "v podobě, kterou distributor čeká.", "Poptat měření"),
        eyebrow="Před trvalým provozem", alt=True,
    ),
    "faq": [
        ("Ověřuje se u ČEZ Distribuce něco jiného než u EG.D?",
         "<p>Základ je společný – metodiky ověřování souladu zpracovaly všechny tři distributoři "
         "společně. Technické podmínky, přílohy, formuláře a některé volitelné požadavky se ale řídí "
         "dokumenty ČEZ Distribuce.</p>"),
        ("Kdo dělá test omezování činného výkonu?",
         "<p>Provádí ho provozovatel výrobny. Můžeme ho změřit za vás a vystavit protokol, který "
         "je povinnou přílohou žádosti o UTP.</p>"),
    ],
    "cross": [("EG.D", "egd.html"), ("PREdistribuce", "predistribuce.html"),
              ("Postup a podklady", "proces-pripojeni.html")],
})

STRANKY.append({
    "slug": "egd.html", "nav": "pds", "reviewed": True,
    "title": "EG.D – dispečerské řízení a ověření souladu výroben",
    "desc": "Ověření souladu výrobny na území EG.D: podklady DEČE pro dispečerské řízení a chránění, "
            "zprovoznění komunikace před UPOS a nové připojovací podmínky od 1. 2. 2026.",
    "eyebrow": "Distributor", "h1": "EG.D",
    "claim": "Komunikace s dispečinkem musí běžet dříve, než se začne zkoušet.",
    "bc_nazev": "EG.D", "breadcrumb": BC_PDS,
    "intro": "<p>Základní metodiky ověřování souladu jsou společné s ostatními distributory. Specifické je "
             "u EG.D hlavně <b>dispečerské řízení a chránění decentrálních zdrojů (DEČE)</b>.</p>",
    "stats": [("1. 11. 2025", "Aktualizace podkladů DEČE"), ("1. 2. 2026", "Nové připojovací podmínky")],
    "body": sekce(
        "Dispečerské řízení a chránění (DEČE)",
        karty([
            (I["dok"], "Dvě verze podle výkonu",
             "<p>Podklady DEČE existují ve verzi pro výrobny 100 až 1000 kW a ve verzi od 1000 kW.</p>"),
            (I["graf"], "Řízení ve stupních",
             "<p>Distributor řídí činný výkon výrobny ve stupních, u větších výroben i jalový výkon, "
             "u úložišť a dobíjecích stanic i příkon.</p>"),
            (I["check"], "Komunikace před UPOS",
             "<p>Podle podkladů DEČE se komunikace s dispečinkem musí zprovoznit ještě před žádostí "
             "o UPOS – bez toho EG.D nepřistoupí ke zkouškám přenosu dat. Z naší projektové praxe patří nefunkční "
             "komunikace s dispečinkem mezi časté důvody zdržení.</p>"),
        ], sloupce=3),
        eyebrow="DEČE",
    ) + sekce(
        "Nové připojovací podmínky od 1. 2. 2026",
        "<p class=\"lead\">EG.D vydala připojovací podmínky pro VN a VVN s platností od <b>1. 2. 2026</b>. "
        "Týkají se hlavně měřicích souprav, trafostanic žadatele a regulace výroben. Ochrany "
        "a telemetrii dál řeší podklady DEČE.</p>"
        + cta("Připravujete projekt na území EG.D? Projdeme s vámi, co z nových podmínek dopadá "
              "na vaši výrobnu."),
        eyebrow="Novinka", alt=True,
    ),
    "faq": [
        ("Proč u EG.D řešíte komunikaci s dispečinkem jako první?",
         "<p>Podle podkladů DEČE EG.D bez zprovozněné komunikace s dispečinkem nepřistoupí ke zkouškám "
         "přenosu dat, a tedy ani k UPOS. Z naší praxe je to navíc častý důvod zdržení.</p>"),
        ("Platí u EG.D stejné metodiky jako u ČEZ Distribuce?",
         "<p>Základní metodiky ano. Specifické jsou podklady DEČE, formuláře a některé požadavky, "
         "které EG.D uplatňuje.</p>"),
    ],
    "cross": [("ČEZ Distribuce", "cez-distribuce.html"), ("PREdistribuce", "predistribuce.html"),
              ("Postup a podklady", "proces-pripojeni.html")],
})

STRANKY.append({
    "slug": "predistribuce.html", "nav": "pds", "reviewed": True,
    "title": "PREdistribuce – ověření souladu na území Prahy",
    "desc": "Ověření souladu výrobny na území PREdistribuce: společné metodiky s ostatními distributory "
            "a vlastní podnikové normy. Specifika projdeme individuálně.",
    "eyebrow": "Distributor", "h1": "PREdistribuce",
    "bc_nazev": "PREdistribuce", "breadcrumb": BC_PDS,
    "intro": "<p>Distribuční území Prahy. Nadřazený rámec – RfG, Příloha 4 PPDS a základní metodiky "
             "ověřování souladu – je <b>společný</b> s ČEZ Distribucí a EG.D. PREdistribuce je "
             "spoluautorem společných metodik.</p>",
    "body": sekce(
        "Co je stejné a co vlastní",
        karty([
            (I["check"], "Společné: základní metodiky",
             "<p>Základní metodiky ověřování souladu jsou společné pro ČEZ Distribuci, EG.D a PREdistribuci. Konkrétní technické podmínky, telemetrie, formuláře a některé volitelné požadavky se řídí dokumenty příslušného distributora.</p>"),
            (I["dok"], "Vlastní: podnikové normy",
             "<p>PREdistribuce má vlastní podnikové normy, které upřesňují technické provedení "
             "a postupy na jejím území.</p>"),
        ], sloupce=2)
        + callout(
            "Podklady si vyžádáme předem",
            "<p>Pro některé konfigurace – zejména fotovoltaiku a bateriová úložiště – si aktuální "
            "podklady PREdistribuce vyžádáme přímo u distributora na začátku projektu. Raději "
            "o dva dny dříve zavoláme, než abychom stavěli rozsah na zastaralé normě.</p>")
        + cta("Máte projekt na území PREdistribuce? Ozvěte se – postup projdeme individuálně."),
        eyebrow="Rámec",
    ),
    "cross": [("ČEZ Distribuce", "cez-distribuce.html"), ("EG.D", "egd.html"), ("Kontakt", "kontakt.html")],
})
# ============================================================= SLUZBY ======
BC_SLU = [("Služby", "index.html#sluzby")]

STRANKY.append({
    "slug": "simulace-souladu.html", "nav": "sluzby",
    "title": "Simulace souladu výrobny s RfG",
    "desc": "Simulace souladu výrobny s RfG: model výrobny, ověření požadavků, které metodika umožňuje "
            "nebo vyžaduje doložit simulací, a protokoly pro distributora. Od kategorie B1.",
    "eyebrow": "Služba", "h1": "Simulace souladu",
    "claim": "Požadavky, které metodika umožňuje nebo vyžaduje ověřit simulací, prokážeme na modelu výrobny.",
    "bc_nazev": "Simulace souladu", "breadcrumb": BC_SLU,
    "intro": "<p>Metodiky u řady požadavků připouštějí více cest ověření – zkoušku, simulaci, nebo "
             "certifikát. <b>Simulací na modelu výrobny</b> se typicky dokládá odezva při změnách "
             "frekvence a napětí, chování při poruchových stavech a další požadavky podle kategorie "
             "výrobního modulu. Počítáme v prostředí DIgSILENT PowerFactory.</p>",
    "stats": [("až 36 MWp", "Rozsah zpracovaných FVE projektů"),
              ("Splněno / nesplněno", "Vyhodnocení u každého požadavku")],
    "body": sekce(
        "Co simulace ověřují",
        seznam([
            "Chování výrobny při poruchách v síti a obnovu výkonu po poruše",
            "Odezvu výrobny na změny frekvence",
            "Napěťovou stabilitu a podporu napětí jalovým výkonem",
            "U větších výroben další požadavky podle metodiky distributora",
        ]) + callout(
            "Rozsah určuje kategorie",
            "<p>U kategorie B1 jde o vybrané body, u B2 a vyšších kategorií je rozsah simulací výrazně širší "
            "a distributorovi se předávají i modely výrobny. Přesný seznam vychází ze smlouvy "
            "o připojení a metodiky distributora – potvrdíme ho předem.</p>"),
        eyebrow="Rozsah",
    ) + sekce(
        "Co model obsahuje",
        wp([
            ("1", "Síť distributora v místě připojení."),
            ("2", "Transformátory a kabelové rozvody výrobny."),
            ("3", "Ochrany s reálným nastavením."),
            ("4", "Modely střídačů, u bateriových systémů i řídicí jednotky úložiště."),
        ]) + callout(
            "Model musí odpovídat skutečnosti",
            "<p>Častým důvodem vrácení dokumentace bývá nesoulad modelu se skutečnou konfigurací "
            "výrobny. Proto začínáme kontrolou podkladů a topologii si necháváme "
            "potvrdit dříve, než spustíme první výpočet.</p>"),
        eyebrow="Model", alt=True,
    ) + sekce(
        "Co dodáme",
        wp([
            ("1", "Kontrolu podkladů a potvrzení rozsahu s distributorem."),
            ("2", "Model výrobny a výpočty podle metodiky distributora."),
            ("3", "Protokoly s vyhodnocením splněno / nesplněno u každého požadavku – podle jeho "
                  "vlastních kritérií v metodice, ne podle jednoho společného limitu."),
            ("4", "Podklady do Dokumentu výrobního modulu a vypořádání připomínek distributora."),
        ])
        + cta("Pošlete nám smlouvu o připojení, jednopólové schéma a typy střídačů – vrátíme se "
              "s rozsahem simulací.", "Poptat simulace"),
        eyebrow="Postup",
    ),
    "faq": [
        ("Kdy je potřeba simulační studie?",
         "<p>Od kategorie B1. U B1 jde o vybrané body, u B2 a vyšších kategorií o výrazně širší rozsah. "
         "U standardního postupu A1 a A2 se simulační studie nevyžaduje.</p>"),
        ("Proč distributor vrací simulace k přepracování?",
         "<p>Z naší praxe bývá častým důvodem nesoulad modelu se skutečnou konfigurací výrobny nebo "
         "neúplné protokoly. Obojí hlídáme ještě před odevzdáním.</p>"),
        ("Máte modely našich střídačů?",
         "<p>Část dynamických modelů máme k dispozici od výrobců, u zbytku se model ověřuje proti "
         "měření. Řekněte nám typ střídače a ověříme, na čem jsme.</p>"),
    ],
    "cross": [("Zkoušky na místě", "zkousky-na-miste.html"), ("Kategorie B2", "kategorie-b2.html"),
              ("Postup a podklady", "proces-pripojeni.html")],
})

STRANKY.append({
    "slug": "zkousky-na-miste.html", "nav": "sluzby",
    "title": "Zkoušky na místě – ověření regulace a ochran výrobny",
    "desc": "Zkoušky výrobny na místě: ověření regulace činného a jalového výkonu, ochran, dálkového "
            "řízení a opětovného připojení. Rozsah podle smlouvy o připojení.",
    "eyebrow": "Služba", "h1": "Zkoušky na místě",
    "claim": "Rozsah podle smlouvy o připojení, protokoly pro distributora.",
    "bc_nazev": "Zkoušky na místě", "breadcrumb": BC_SLU,
    "intro": "<p>Zkoušky se provádějí na hotové výrobně a začínají u kategorie <b>B1, tedy od "
             "100 kW</b>. Co přesně se zkouší, určuje smlouva o připojení a požadavky distributora. "
             "Hlavní okruhy jsou tyto:</p>",
    "body": sekce(
        "Co se ověřuje",
        karty([
            (I["blesk"], "Zkoušky činného výkonu",
             "<p>Ověření regulace činného výkonu a jeho omezení na pokyn distributora.</p>"),
            (I["graf"], "Zkoušky jalového výkonu",
             "<p>Ověření regulace jalového výkonu, účiníku a napětí.</p>"),
            (I["stit"], "Ochrany",
             "<p>Ověření nastavení a funkce síťových ochran, protokol o nastavení ochran.</p>"),
            (I["sit"], "Dálkové řízení",
             "<p>Ověření komunikace a řízení výrobny z dispečinku distributora.</p>"),
            (I["hodiny"], "Opětovné připojení",
             "<p>Ověření automatického opětovného připojení u kategorií, kde ho pravidla provozování "
             "distribučních soustav (PPDS) umožňují. "
             "U výrobních modulů typu D se ověřuje zpětné připojení na pokyn dispečinku "
             "distributora.</p>"),
            (I["baterie"], "Bateriové úložiště",
             "<p>U výroben s baterií ověření provozu úložiště při nabíjení i vybíjení.</p>"),
        ], sloupce=3),
        eyebrow="Okruhy zkoušek",
    ) + sekce(
        "Co musí být připraveno před zkouškou",
        seznam([
            "Dokončená výrobna pod napětím, s výkonem potřebným pro zkoušky",
            "Jednopólové schéma podle skutečného provedení",
            "Nastavené ochrany a protokol o jejich nastavení",
            "Zprovozněná komunikace s dispečinkem, pokud ji distributor vyžaduje",
            "Parametry střídačů a regulace činného a jalového výkonu, včetně přístupu k jejich změně",
            "Přístupné místo měření, dohodnuté předem",
            "Možnost během zkoušky měnit výkon výrobny",
            "Odpovědná osoba na místě a dostupný servis technologie",
            "Termín koordinovaný s distributorem, pokud se zkoušek účastní",
        ]) + callout(
            "Projdeme to s vámi předem",
            "<p>Připravenost výrobny zkontrolujeme před výjezdem, aby se zkoušky nemusely přerušit "
            "kvůli chybějícímu nastavení nebo podkladu.</p>"),
        eyebrow="Příprava", alt=True,
    ) + sekce(
        "Jak to probíhá",
        wp([
            ("1", "Program zkoušek a domluva termínu s distributorem, dispečinkem a dodavateli technologie."),
            ("2", "Výjezd na výrobnu – zkoušky obvykle zvládneme jedním výjezdem. Měříme analyzátorem "
                  "kvality elektřiny třídy A."),
            ("3", "Protokoly o zkouškách a jejich zapracování do Dokumentu výrobního modulu."),
        ]) + callout(
            "Počítejte s počasím",
            "<p>Část zkoušek fotovoltaiky potřebuje dostatek slunce. Když stavba skončí na podzim, "
            "je dobré zkoušky naplánovat co nejdříve – dočasný provoz mezitím běží.</p>"),
        eyebrow="Postup",
    ) + sekce(
        "",
        cta("Potřebujete zkoušky u elektrárny, kterou stavěl někdo jiný? Běžná věc – stačí nám "
            "podklady.", "Domluvit zkoušky"),
    ),
    "faq": [
        ("Musí být u zkoušek distributor?",
         "<p>U části ano – například komunikaci s dispečinkem ověřuje distributor. Termín proto "
         "domlouváme s ním a s dostatečným předstihem.</p>"),
        ("Zkouší se výrobna i po uvedení do trvalého provozu?",
         "<p>Ano. Spínače, ochrany a vybavení pro dálkové řízení se podle PPDS, přílohy 4 (kap. 12.4) "
         "funkčně přezkušují nejméně jednou za čtyři roky; distributor může přezkoušení požadovat i mimo "
         "tuto lhůtu. Po změně zařízení – třeba po doplnění baterie – se ověření opakuje v rozsahu, "
         "který distributor stanoví.</p>"),
    ],
    "cross": [("Simulace souladu", "simulace-souladu.html"), ("Kategorie B1", "kategorie-b1.html"),
              ("Postup a podklady", "proces-pripojeni.html")],
})

# ============================================================= POSTUP ======
STRANKY.append({
    "slug": "proces-pripojeni.html", "nav": "proces", "reviewed": True,
    "title": "Postup ověření souladu – UPOS, zkoušky, DVM a UTP",
    "desc": "Jak probíhá ověření souladu výrobny: smlouva o připojení, žádost o UPOS, zkoušky "
            "a simulace, Dokument výrobního modulu a žádost o UTP. Lhůty a co od vás potřebujeme.",
    "eyebrow": "Postup", "h1": "Postup a podklady",
    "claim": "Od smlouvy o připojení po trvalý provoz.",
    "bc_nazev": "Postup a podklady", "breadcrumb": [],
    "intro": "<p>Ověření souladu není poslední razítko, ale samostatná fáze mezi dostavbou výrobny "
             "a trvalým provozem. Kdo o ní ví od začátku, ušetří měsíce.</p>",
    "body": sekce(
        "Pět kroků",
        kroky([
            ("Smlouva o připojení",
             "Z ní vychází kategorie výrobny a rozsah ověření. K projektové dokumentaci se "
             "distributor vyjadřuje do 30 dnů.", "Začátek"),
            ("Žádost o UPOS",
             "Umožnění provozu pro ověření souladu. Distributor rozhodne do 30 dnů od úplné žádosti "
             "a při splnění stanovených podmínek vydá souhlas s dočasným provozem (u typu D dočasné "
             "provozní oznámení).", "30 dnů"),
            ("Zkoušky a simulace",
             "Provádějí se během dočasného provozu, který trvá nejdéle 12 měsíců. Prodloužit ho lze "
             "jen na žádost – viz lhůty níže.",
             "Nejdéle 12 měsíců"),
            ("Dokument výrobního modulu",
             "Shrnuje výsledky zkoušek a simulací a dokládá distributorovi soulad výrobny.",
             "Protokoly"),
            ("Žádost o UTP",
             "Umožnění trvalého provozu. Při splnění podmínek distributor vydá konečné provozní "
             "oznámení.", "Cíl"),
        ]),
        eyebrow="Průběh", kotva="kroky",
        uvod="<p>Kroky popisují postup pro kategorie <b>B1, B2, C a D</b>. U <b>A1 a A2</b> se žádost "
             "o UPOS nepodává – nahrazuje ji instalační dokument a po splnění podmínek smlouvy "
             "o připojení se podává rovnou žádost o UTP. Pro bateriová úložiště mají distributoři "
             "vlastní dokumenty, u ČEZ Distribuce pro žádosti o UTP od 1. 2. 2026 – viz "
             "<a href=\"bateriova-uloziste-zue.html\">Bateriová úložiště</a>.</p>",
    ) + sekce(
        "Co se dokládá k žádosti o UPOS",
        tabulka(
            ["Bod", "Doklad", "Poznámka"],
            [["a", "Projektová dokumentace podle skutečného provedení", "odsouhlasená distributorem"],
             ["b", "Jednopólové schéma výrobny", "pokud není součástí dokumentace"],
             ["c", "Potvrzení odborné firmy o provedení výrobny", "podle smlouvy o připojení a předpisů"],
             ["d", "Výchozí revize přípojky", "jen pokud se přípojka mění"],
             ["e", "Výchozí revize elektrického zařízení výrobny", "případně další doklad pro zařízení třídy I"],
             ["f", "Protokol o nastavení ochran", ""],
             ["g", "Protokoly o úředním ověření měřicích transformátorů proudu a napětí", ""],
             ["h", "Místní provozní předpisy", "zpracujeme"],
             ["i", "Harmonogram a rozsah zkoušek a simulací", "zpracujeme – určuje délku dočasného provozu"],
             ["j", "Seznam certifikátů zařízení", "certifikáty střídačů a dalšího zařízení"]],
            poznamky=["Základní přehled podle PPDS, přílohy 4, kap. 12.1. Distributor může požadovat "
                      "doplnění dalších dokladů.",
                      "Nekompletní žádost distributor zamítne s uvedením důvodů a podává se nová – "
                      "proto dokumenty kontrolujeme ještě před podáním."],
            min_sirka=680,
        ),
        eyebrow="Žádost o UPOS", alt=True, kotva="upos",
    ) + sekce(
        "Lhůty, které je dobré znát",
        tabulka(
            ["Úkon", "Lhůta"],
            [["Vyjádření distributora k projektové dokumentaci", "30 dnů"],
             ["Rozhodnutí o žádosti o UPOS", "do 30 dnů od úplné žádosti"],
             ["Dočasný provoz pro ověření souladu",
              "<b>nejdéle 12 měsíců</b> podle harmonogramu zkoušek; prodloužit lze jen za podmínek "
              "v dalším řádku"],
             ["Prodloužení při překážce, kterou výrobce neovlivní",
              "o nezbytně nutnou dobu – pokud výrobce překážku bez zbytečného odkladu oznámí, "
              "prokáže a o prodloužení požádá"],
             ["Informování o přerušení nebo ukončení UPOS kvůli závadám, které ovlivňují bezpečný "
              "a spolehlivý provoz sítě",
              "na místě, nebo písemně do 15 pracovních dnů od zjištění závad"],
             ["Rozhodnutí o žádosti o UTP", "do 30 dnů od kompletní žádosti"],
             ["Informování o přerušení UTP kvůli zjištěným nedostatkům",
              "na místě, nebo písemně do 5 pracovních dnů od jejich zjištění"],
             ["Periodické přezkoušení spínačů, ochran a dálkového řízení po uvedení do trvalého provozu",
              "nejméně jednou za čtyři roky"]],
            poznamky=["Žádost o UTP je potřeba podat během platnosti dočasného provozu – jinak může "
                      "distributor výrobnu odpojit. To neplatí, pokud jste ještě během platnosti požádali "
                      "o prodloužení kvůli překážce, kterou nemůžete ovlivnit: do vyřízení žádosti výrobnu "
                      "odpojit nelze.",
                      "Lhůty stanoví PPDS, příloha 4 (kap. 4.8 a 12.1 až 12.4), která platí pro všechny "
                      "distributory. Lhůtu 15 pracovních dnů uvádějí shodně i metodiky ověřování "
                      "souladu B1 a B2."],
            min_sirka=600,
        ),
        eyebrow="Lhůty",
    ) + sekce(
        "Dokument výrobního modulu",
        "<p class=\"lead\">Formulář distributora se seznamem všech požadavků a u každého s cestou, "
        "jak ho doložit – zkouškou, simulací, nebo certifikátem. Vyplněný dokument s protokoly "
        "je jádro žádosti o UTP. U kategorií A1 a A2 ho nahrazuje jednodušší instalační dokument.</p>",
        eyebrow="DVM", alt=True,
    ) + sekce(
        "Co vyřídíme za vás",
        seznam([
            "Žádost o UPOS včetně harmonogramu zkoušek",
            "Zkoušky na místě a simulace souladu",
            "Protokoly a Dokument výrobního modulu",
            "Žádost o UTP a jednání s distributorem až do konečného provozního oznámení",
        ]) + callout(
            "Co vystavujeme a co ne",
            "<p>Vystavujeme <b>protokoly o zkouškách</b>, <b>simulační zprávu s protokoly</b> a vyplněný "
            "<b>Dokument výrobního modulu</b>. <b>Certifikát zařízení nevystavujeme</b> – ten vydává "
            "certifikátor pro konkrétní zařízení. Náš protokol dokládá požadavek zkouškou nebo simulací "
            "tam, kde to metodika připouští; certifikátem není.</p>"),
        eyebrow="Naše práce",
    ) + sekce(
        "Co od vás potřebujeme",
        seznam([
            "Informaci, zda jde o novou výrobnu, změnu stávající, nebo doplnění baterie",
            "Smlouvu o připojení",
            "Projektovou dokumentaci a jednopólové schéma",
            "Typy a počet střídačů, u baterie i typ úložiště",
            "U kategorie B2 a vyšších i parametry a modely střídačů a regulátoru výrobny",
            "Technické listy a certifikáty použitého zařízení",
            "Revizní zprávy, protokol o nastavení ochran a potvrzení zhotovitele, pokud už jsou",
            "Termín dokončení stavby",
            "Kontakty na dodavatele technologie a servis",
        ]) + callout(
            "Co se k žádosti o UTP nemusí dokládat znovu",
            "<p>Doklady a) až h) z žádosti o UPOS se k žádosti o UTP nepřikládají znovu, pokud v ní "
            "potvrdíte, že se zařízení během dočasného provozu nezměnilo a dokumenty budou platné "
            "k předpokládanému dni vydání konečného provozního oznámení. Nově se přikládá Dokument "
            "výrobního modulu, u A1 a A2 instalační dokument.</p>"),
        eyebrow="Podklady", alt=True, kotva="podklady",
    ) + sekce(
        "Kdy se do toho pustit",
        "<p class=\"lead\">Ideálně ve chvíli, kdy máte podepsanou smlouvu o připojení – tedy dříve, "
        "než se začne stavět.</p>"
        + karty([
            (I["graf"], "Simulace ověří nastavení",
             "<p>Simulace ověří navržené nastavení střídačů a ochran, případně ukážou, co je potřeba "
             "upravit. Je lepší to vědět před uvedením do provozu než až po neúspěšné zkoušce.</p>"),
            (I["hodiny"], "Termíny se nedají zrychlit",
             "<p>Zkouška s dispečinkem se domlouvá s předstihem a podklady od výrobců technologie "
             "chodí týdny.</p>"),
            (I["blesk"], "Fotovoltaika potřebuje slunce",
             "<p>Kdo dostaví v listopadu, může na vhodné počasí čekat do jara – a dočasný provoz "
             "mezitím běží.</p>"),
        ], sloupce=3)
        + cta("Chcete si projít harmonogram na konkrétním projektu? Ozvěte se s termínem dokončení "
              "stavby a kategorií ze smlouvy o připojení."),
        eyebrow="Načasování",
    ),
    "cross": [("Simulace souladu", "simulace-souladu.html"), ("Zkoušky na místě", "zkousky-na-miste.html"),
              ("Časté dotazy", "faq.html")],
})

# ================================================================ FAQ ======
STRANKY.append({
    "slug": "faq.html", "nav": "",
    "title": "Časté dotazy k ověření souladu výroben",
    "desc": "Odpovědi na nejčastější otázky k ověření souladu výroben s RfG: kategorie, zkoušky "
            "a simulace, UPOS a UTP, certifikáty, baterie, podklady a termíny.",
    "eyebrow": "Ptáte se", "h1": "Časté dotazy",
    "bc_nazev": "Časté dotazy", "breadcrumb": [],
    "intro": "<p>Otázky, které dostáváme od investorů, projektantů i montážních firem. U konkrétního "
             "projektu vždy ověřujeme aktuální dokumenty příslušného distributora.</p>",
    "body": "",
    "faq_nadpis": "Otázky a odpovědi",
    "faq": [
        FAQ_CO_JSOU, FAQ_OD_VYKONU, FAQ_KATEGORIE,
        ("Jaký je rozdíl mezi zkouškami a simulacemi?",
         "<p>Zkoušky se dělají přímo na hotové výrobně – ověřuje se regulace výkonu, ochrany nebo "
         "dálkové řízení. Simulace dokládají na modelu výrobny požadavky, které metodika umožňuje nebo "
         "vyžaduje ověřit výpočtem – typicky chování při poruchách v síti.</p>"),
        ("Co znamená UPOS a UTP?",
         "<p><b>UPOS</b> je umožnění provozu pro ověření souladu – dočasný provoz, během kterého se "
         "provedou zkoušky. <b>UTP</b> je umožnění trvalého provozu, které končí konečným provozním "
         "oznámením.</p>"),
        ("Jak dlouho platí dočasný provoz?",
         "<p>Nejdéle <b>12 měsíců</b> podle harmonogramu zkoušek. Při překážce, kterou nemůžete "
         "ovlivnit, ho distributor prodlouží o nezbytně nutnou dobu – překážku je ale potřeba bez "
         "zbytečného odkladu oznámit, doložit a o prodloužení požádat.</p>"),
        ("Co když zkoušky nestihneme?",
         "<p>Žádost o UTP je potřeba podat, dokud dočasný provoz platí – jinak může distributor "
         "výrobnu odpojit. Brání-li vám v dokončení překážka, kterou nemůžete ovlivnit, požádejte ještě "
         "během platnosti o prodloužení – do vyřízení žádosti výrobnu odpojit nelze. Ozvěte se co "
         "nejdříve, sestavíme reálný plán zbývajících kroků.</p>"),
        ("Co je Dokument výrobního modulu?",
         '<p>Formulář distributora se seznamem požadavků a cestou jejich ověření. Jeho vyplnění je '
         'jádro celé agendy. <a href="proces-pripojeni.html">Více v postupu →</a></p>'),
        ("Kdy stačí certifikát a nemusí se nic měřit?",
         "<p>Jen u požadavků, kde to Dokument výrobního modulu připouští. U výrobny z více výrobních "
         "jednotek část bodů certifikátem nedoložíte a zkoušky na místě certifikát nenahradí.</p>"),
        FAQ_B1_VYJEZD,
        ("Co je rozpadové místo?",
         "<p>Spínací prvek, na který působí ochrany při odchylkách napětí a frekvence a který odpojí "
         "výrobnu od sítě. Umístění volí provozovatel výrobny, nastavení ochran předepisuje "
         "distributor.</p>"),
        ("Zkouší se výrobna i po uvedení do trvalého provozu?",
         "<p>Ano – spínače, ochrany a vybavení pro dálkové řízení se podle PPDS, přílohy 4 přezkušují "
         "nejméně jednou za čtyři roky.</p>"),
        ("Platí ještě protokoly laboratoří u malých výroben?",
         '<p>Přechodně ano, pokud byly vydané nejpozději 31. 12. 2025. EG.D a PREdistribuce je uznávají '
         'do 31. 12. 2026. <a href="kategorie-a2.html">Podrobněji u kategorie A2 →</a></p>'),
        ("Chci přidat baterii k fotovoltaice. Co mě čeká?",
         '<p>Posouzení připojitelnosti, úprava smlouvy o připojení, ověření souladu úložiště a rozšíření '
         'telemetrie. <a href="pridani-baterie-k-fve.html">Podrobněji →</a></p>'),
        ("Co od nás potřebujete?",
         '<p>Hlavně smlouvu o připojení, jednopólové schéma a typy střídačů. '
         '<a href="proces-pripojeni.html#podklady">Celý seznam →</a></p>'),
        ("Kolik to stojí?",
         "<p>Cena se odvíjí od kategorie výrobny, počtu a typu střídačů a rozsahu zkoušek a simulací. "
         "Pošlete smlouvu o připojení a jednopólové schéma a dostanete konkrétní nabídku.</p>"),
        FAQ_CIZI_STAVBA,
        ("Se kterými distributory pracujete?",
         '<p>Se všemi třemi velkými – <a href="cez-distribuce.html">ČEZ Distribuce</a>, '
         '<a href="egd.html">EG.D</a> a <a href="predistribuce.html">PREdistribuce</a>.</p>'),
    ],
    "cross": [("Postup a podklady", "proces-pripojeni.html"), ("Kategorie B1", "kategorie-b1.html"),
              ("Kontakt", "kontakt.html")],
})

# ========================================================== REFERENCE ======
STRANKY.append({
    "slug": "reference.html", "nav": "reference",
    "title": "Reference – ověření souladu FVE projektů až do 36 MWp",
    "desc": "Vybrané projekty ověření souladu: fotovoltaika ~30 MW na 110 kV kategorie D, FVE 698 kWp "
            "kategorie B1 a fotovoltaika s bateriovým úložištěm.",
    "eyebrow": "Co máme za sebou", "h1": "Reference",
    "claim": "Projekty uvádíme anonymizovaně – na přání investorů.",
    "bc_nazev": "Reference", "breadcrumb": [],
    "intro": "<p>Většina investorů si nepřeje být jmenována, proto uvádíme projekty bez názvů – "
             "s parametry, které o rozsahu práce řeknou více než logo.</p>",
    "body": sekce(
        "Vybrané projekty",
        karty([
            (I["tovarna"], "Fotovoltaika, kategorie D",
             "<p><b>Výkon:</b> ~30 MW, připojení na 110 kV<br><b>Distributor:</b> EG.D<br>"
             "<b>Předmět:</b> simulace souladu, model výrobny, dokumentace<br>"
             "<b>Stav:</b> ve fázi ověřování souladu</p>"),
            (I["blesk"], "Fotovoltaika, kategorie B1",
             "<p><b>Výkon:</b> 698 kWp (P<sub>n</sub> 550 kW)<br><b>Distributor:</b> ČEZ Distribuce<br>"
             "<b>Předmět:</b> zkoušky na místě, protokoly, Dokument výrobního modulu</p>"),
            (I["baterie"], "Fotovoltaika s baterií",
             "<p><b>Výkon:</b> 60 kWp + bateriové úložiště<br><b>Distributor:</b> EG.D<br>"
             "<b>Předmět:</b> etapizace fotovoltaiky a doplnění akumulace</p>"),
        ], sloupce=3),
        eyebrow="Anonymizovaně",
    ) + sekce(
        "Kdo to dělá",
        '<p class="lead">Ověřování souladu zajišťuje <b>BFK Systems s.r.o.</b> Se sesterskou společností '
        '<a href="https://www.bftechnology.cz/" target="_blank" rel="noopener">BF technology</a> '
        'tvoříme jednu skupinu. BF technology staví fotovoltaické elektrárny, BFK Systems dělá '
        'inženýrskou část – projekty, simulace, zkoušky a jednání s distributory. Zkušenosti máme '
        'z projektů pro energetiku, petrochemii i automobilový průmysl.</p>'
        + cta("Chcete referenci na konkrétní typ projektu? Řekněte si o ni – po dohodě s investorem "
              "ji rádi doložíme podrobněji.", "Ozvat se"),
        eyebrow="Skupina", alt=True,
    ),
    "cross": [("Simulace souladu", "simulace-souladu.html"), ("Zkoušky na místě", "zkousky-na-miste.html"),
              ("Kategorie C a D", "kategorie-c-d.html"), ("Kontakt", "kontakt.html")],
})

# =========================================================== KONTAKT ======
FORMULAR = """<section class="contact-section" id="poptavka">
  <div class="bg"><picture>
    <source type="image/webp" srcset="assets/title-photo-1024.webp 1024w, assets/title-photo.webp 2048w" sizes="(max-width: 980px) 100vw, 33vw">
    <img src="assets/title-photo.jpg" alt="" aria-hidden="true" loading="lazy" width="2048" height="1536" srcset="assets/title-photo-1024.jpg 1024w, assets/title-photo.jpg 2048w" sizes="(max-width: 980px) 100vw, 33vw">
  </picture></div>
  <div class="container contact-grid">
    <div class="contact-aside">
      <p class="eyebrow">Kontakt</p>
      <h2>Napište nám,<br>co řešíte.</h2>
      <p>Ozveme se do dvou pracovních dnů. Pokud máte po ruce smlouvu o připojení a jednopólové schéma, přiložte je rovnou – ušetří to jedno kolečko otázek.</p>
      <div class="quick">
        <a href="tel:+420776111100">
          <span class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.12.9.35 1.79.68 2.64a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.44-1.25a2 2 0 0 1 2.11-.45c.85.33 1.74.56 2.64.68A2 2 0 0 1 22 16.92z"/></svg></span>
          +420 776 111 100
        </a>
        <a href="mailto:simulace@bfksystems.cz">
          <span class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg></span>
          simulace@bfksystems.cz
        </a>
        <a href="https://www.bfksystems.cz/" target="_blank" rel="noopener">
          <span class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M3 12h18M12 3c2.5 2.7 2.5 15.3 0 18M12 3c-2.5 2.7-2.5 15.3 0 18"/></svg></span>
          www.bfksystems.cz
        </a>
      </div>
      <div class="firm">
        <b>BFK Systems s.r.o.</b><br>
        Obchodní 455/12, Děčín V-Rozbělesy, 405 02 Děčín<br>
        IČO 23571853 &middot; DIČ CZ23571853
      </div>
    </div>

    <div class="contact-form-card" id="formular">
      <div id="contact-status" role="status"></div>
      <!-- Odesila se pres fetch(), pole "redirect" je zalozni cesta bez JavaScriptu. -->
      <form class="contact-form" id="contact-form" action="https://api.web3forms.com/submit" method="post" autocomplete="on">
        <input type="hidden" name="access_key" value="PLACEHOLDER-DOPLNIT-KLIC-WEB3FORMS">
        <input type="hidden" name="subject" value="Nová poptávka z webu simulacni-zkousky.cz">
        <input type="hidden" name="from_name" value="Poptávkový formulář simulacni-zkousky.cz">
        <input type="hidden" name="replyto" value="">
        <input type="hidden" name="redirect" value="https://www.simulacni-zkousky.cz/kontakt.html?sent=1#formular">
        <div class="hp-field" aria-hidden="true">
          <label for="botcheck">Nevyplňujte</label>
          <input type="checkbox" id="botcheck" name="botcheck" tabindex="-1" autocomplete="off">
        </div>
        <div class="row">
          <div class="field">
            <label for="f-name">Jméno a příjmení *</label>
            <input type="text" id="f-name" name="Jméno a příjmení" required>
          </div>
          <div class="field">
            <label for="f-phone">Telefon *</label>
            <input type="tel" id="f-phone" name="Telefon" required>
          </div>
          <div class="field">
            <label for="f-email">E-mail *</label>
            <input type="email" id="f-email" name="E-mail" required>
          </div>
          <div class="field">
            <label for="f-firma">Firma</label>
            <input type="text" id="f-firma" name="Firma">
          </div>
          <div class="field">
            <label for="f-pds">Distributor</label>
            <select id="f-pds" name="Distributor">
              <option value="">– vyberte –</option>
              <option>ČEZ Distribuce</option>
              <option>EG.D</option>
              <option>PREdistribuce</option>
              <option>Nevím</option>
            </select>
          </div>
          <div class="field">
            <label for="f-kat">Kategorie ze smlouvy o připojení</label>
            <select id="f-kat" name="Kategorie">
              <option value="">– vyberte –</option>
              <option>A1 (0,8 až 11 kW)</option>
              <option>A2 (nad 11 kW, pod 100 kW)</option>
              <option>B1 (100 kW až pod 1 MW)</option>
              <option>B2 (1 MW až pod 30 MW)</option>
              <option>C nebo D (od 30 MW / 110 kV)</option>
              <option>Nevím</option>
            </select>
          </div>
          <div class="field">
            <label for="f-vykon">Instalovaný výkon</label>
            <input type="text" id="f-vykon" name="Výkon" placeholder="např. 698 kWp / 550 kW">
          </div>
          <div class="field">
            <label for="f-bess">Bateriové úložiště</label>
            <select id="f-bess" name="Bateriové úložiště">
              <option value="">– vyberte –</option>
              <option>Ne</option>
              <option>Ano, součást projektu</option>
              <option>Doplňujeme ke stávající FVE</option>
            </select>
          </div>
          <div class="field full">
            <label for="f-zajem">Mám zájem o</label>
            <select id="f-zajem" name="Zájem o">
              <option value="Ověření souladu – kompletně">Ověření souladu kompletně (simulace + zkoušky + dokumentace)</option>
              <option value="Simulace souladu">Simulaci souladu</option>
              <option value="Zkoušky na místě">Zkoušky na místě</option>
              <option value="Vyřízení UPOS / UTP">Vyřízení žádostí o UPOS a UTP</option>
              <option value="Konzultace">Konzultaci / nevím přesně</option>
            </select>
          </div>
          <div class="field full">
            <label for="f-message">Zpráva</label>
            <textarea id="f-message" name="Zpráva" placeholder="Počet a typ střídačů, termín dokončení stavby, do kdy platí dočasný provoz…"></textarea>
          </div>
          <input type="hidden" name="Odesláno z webu" value="simulacni-zkousky.cz">
          <div class="field full">
            <p class="gdpr">Odesláním formuláře berete na vědomí zpracování osobních údajů za účelem vyřízení poptávky. K odeslání formuláře využíváme externí službu jako zpracovatele. Podrobnosti najdete v <a href="zasady-zpracovani-osobnich-udaju.html">zásadách zpracování osobních údajů</a>.</p>
            <button type="submit">Odeslat poptávku</button>
          </div>
        </div>
      </form>
    </div>
  </div>
</section>

<script src="assets/form.js"></script>
"""

STRANKY.append({
    "slug": "kontakt.html", "nav": "kontakt", "bez_kontaktu": True,
    "title": "Kontakt – ověření souladu výroben s RfG",
    "desc": "BFK Systems s.r.o., Obchodní 455/12, Děčín. Poptávka na simulace souladu, zkoušky na "
            "místě a vyřízení dokumentace k dočasnému i trvalému provozu.",
    "eyebrow": "Kontakt", "h1": "Ozvěte se",
    "bc_nazev": "Kontakt", "breadcrumb": [],
    "intro": "<p>Nejrychlejší cesta k odpovědi vede přes smlouvu o připojení – je v ní kategorie "
             "výrobního modulu i rezervovaný výkon, tedy dvě věci, ze kterých se odvíjí celý rozsah "
             "ověření. Pošlete nám ji s poptávkou – stačí e-mailem na simulace@bfksystems.cz.</p>",
    "body": sekce(
        "Kontaktní údaje",
        karty([
            (I["dok"], "BFK Systems s.r.o.",
             "<p>Obchodní 455/12<br>Děčín V-Rozbělesy, 405 02 Děčín</p>"
             "<p>IČO 23571853<br>DIČ CZ23571853</p>"),
            (I["sit"], "Spojení",
             '<p><a href="tel:+420776111100">+420 776 111 100</a><br>'
             '<a href="mailto:simulace@bfksystems.cz">simulace@bfksystems.cz</a><br>'
             '<a href="https://www.bfksystems.cz/" target="_blank" rel="noopener">www.bfksystems.cz</a></p>'),
        ], sloupce=2)
        + callout(
            "Co nám poslat s poptávkou",
            "<p>Smlouvu o připojení (nebo alespoň kategorii a rezervovaný výkon), jednopólové "
            "schéma, počet a typ střídačů a informaci, jestli je součástí bateriové úložiště. "
            "Z toho odhadneme rozsah ověření. "
            "<a href=\"proces-pripojeni.html#podklady\">Co dalšího se hodí →</a></p>"),
        eyebrow="Kde nás najdete",
    ) + sekce(
        "Kdo se vám ozve",
        karty([
            (I["dok"], "PhDr. Jan Böhme",
             "<p><b>Obchodní a finanční ředitel</b></p><p>Nabídky, smlouvy a jednání s investory. "
             "Praxe z managementu, ekonomie a financí.</p>"),
            (I["lupa"], "Bc. Petr Fencl",
             "<p><b>Technický ředitel, specialista na simulace a RfG</b></p><p>Průmyslová automatizace, "
             "fotovoltaika a integrace MES/ERP. Zkušenosti z projektů pro ČEZ a ČEPS.</p>"),
            (I["blesk"], "Michal Kovář",
             "<p><b>Specialista na simulace a RfG, VN a řízení FVE</b></p><p>Vysoké napětí, průmyslové "
             "řízení a aplikace SCADA. Desítky projektů v Evropě i zámoří.</p>"),
        ], sloupce=3)
        + '    <p class="spec-note">Tým a kontakty podle <a href="https://www.bfksystems.cz/" '
          'target="_blank" rel="noopener">www.bfksystems.cz</a>.</p>',
        eyebrow="Tým", alt=True,
    ) + FORMULAR + sekce(
        "Fakturační a identifikační údaje",
        tabulka(
            ["", ""],
            [["Obchodní firma", "BFK Systems s.r.o."],
             ["Sídlo", "Obchodní 455/12, Děčín V-Rozbělesy, 405 02 Děčín"],
             ["IČO", "23571853"],
             ["DIČ", "CZ23571853"],
             ["Zápis v OR", "Krajský soud v Ústí nad Labem, oddíl C, vložka 54375"],
             ["Telefon", '<a href="tel:+420776111100">+420 776 111 100</a>'],
             ["E-mail", '<a href="mailto:simulace@bfksystems.cz">simulace@bfksystems.cz</a>'],
             ["Web", '<a href="https://www.bfksystems.cz/" target="_blank" rel="noopener">www.bfksystems.cz</a>']],
            min_sirka=520,
        ),
        eyebrow="Údaje",
    ),
    "cross": [("Postup a podklady", "proces-pripojeni.html#podklady"), ("Časté dotazy", "faq.html"),
              ("Reference", "reference.html")],
})

# ======================================================== GDPR a 404 ======
STRANKY.append({
    "slug": "zasady-zpracovani-osobnich-udaju.html", "nav": "", "prio": "0.2",
    "title": "Zásady zpracování osobních údajů",
    "desc": "Jak BFK Systems s.r.o. zpracovává osobní údaje z poptávkového formuláře na webu "
            "simulacni-zkousky.cz: účely, právní základ, doba uchování, příjemci a vaše práva.",
    "eyebrow": "Právní informace", "h1": "Zásady zpracování osobních údajů",
    "bc_nazev": "Zásady zpracování osobních údajů", "breadcrumb": [],
    "intro": "<p>Tyto zásady popisují, jak nakládáme s osobními údaji, které nám pošlete přes web "
             "www.simulacni-zkousky.cz.</p>",
    "body": sekce("", """    <div class="legal">
      <p class="updated">Účinné od 1. 9. 2026</p>

      <h2>1. Kdo údaje zpracovává</h2>
      <p>Správcem osobních údajů je <b>BFK Systems s.r.o.</b>, IČO 23571853, se sídlem Obchodní 455/12,
      Děčín V-Rozbělesy, 405 02 Děčín, zapsaná v obchodním rejstříku vedeném Krajským soudem v Ústí nad
      Labem, oddíl C, vložka 54375.</p>
      <p>Kontakt ve věcech ochrany osobních údajů: <a href="mailto:simulace@bfksystems.cz">simulace@bfksystems.cz</a>,
      telefon <a href="tel:+420776111100">+420 776 111 100</a>. Pověřence pro ochranu osobních údajů
      jsme nejmenovali, protože nám tato povinnost ze zákona nevyplývá.</p>

      <h2>2. Jaké údaje a proč</h2>
      <table>
        <tr><th>Účel</th><th>Údaje</th><th>Právní základ</th><th>Doba uchování</th></tr>
        <tr>
          <td>Vyřízení poptávky odeslané formulářem</td>
          <td>jméno a příjmení, telefon, e-mail, firma, údaje o projektu uvedené ve zprávě</td>
          <td>opatření před uzavřením smlouvy na vaši žádost (čl. 6 odst. 1 písm. b) GDPR)</td>
          <td>3 roky od poslední komunikace, pokud nedojde k uzavření smlouvy</td>
        </tr>
        <tr>
          <td>Plnění smlouvy a související dokumentace</td>
          <td>identifikační a kontaktní údaje, údaje o zařízení a projektu</td>
          <td>plnění smlouvy (čl. 6 odst. 1 písm. b) GDPR)</td>
          <td>po dobu trvání smlouvy a 10 let poté (zákonné archivační lhůty)</td>
        </tr>
        <tr>
          <td>Plnění zákonných povinností – účetnictví a daně</td>
          <td>fakturační údaje</td>
          <td>právní povinnost (čl. 6 odst. 1 písm. c) GDPR)</td>
          <td>podle zákona o účetnictví a daňových předpisů, zpravidla 10 let</td>
        </tr>
      </table>
      <p>Vyplnění formuláře je dobrovolné. Bez kontaktních údajů vám ale nemůžeme odpovědět.</p>

      <h2>3. Komu se údaje předávají</h2>
      <p>Osobní údaje nepředáváme nikomu k vlastním účelům. Zapojujeme však zpracovatele, kteří pro
      nás zajišťují technické služby:</p>
      <ul>
        <li>poskytovatel služby pro odeslání a doručení formuláře (odeslaná zpráva prochází jeho
        serverem a je přeposlána na naši e-mailovou adresu);</li>
        <li>poskytovatel webhostingu, na kterém běží tento web;</li>
        <li>poskytovatel e-mailových služeb.</li>
      </ul>
      <p>Údaje mohou být dále předány osobám, kterým to ukládá právní předpis, a v nezbytném rozsahu
      provozovateli distribuční soustavy, pokud je to potřebné k vyřízení vaší zakázky (například
      k podání žádosti o provoz výrobny vaším jménem).</p>

      <h2>4. Předávání mimo EU</h2>
      <p>Někteří zpracovatelé mohou zpracovávat údaje na serverech mimo Evropskou unii. V takovém
      případě se předání opírá o rozhodnutí Evropské komise o odpovídající ochraně, nebo o standardní
      smluvní doložky schválené Evropskou komisí.</p>

      <h2>5. Cookies a analytika</h2>
      <p>Tento web nepoužívá analytické ani reklamní cookies a nesleduje chování návštěvníků.
      Písma i ostatní části stránky se načítají přímo z tohoto webu, ne z externích služeb.</p>

      <h2>6. Vaše práva</h2>
      <ul>
        <li>právo na přístup k osobním údajům,</li>
        <li>právo na opravu nepřesných údajů,</li>
        <li>právo na výmaz, pokud odpadl důvod zpracování,</li>
        <li>právo na omezení zpracování,</li>
        <li>právo na přenositelnost údajů,</li>
        <li>právo vznést námitku proti zpracování založenému na oprávněném zájmu,</li>
        <li>právo podat stížnost u Úřadu pro ochranu osobních údajů, Pplk. Sochora 27, 170 00 Praha 7,
        <a href="https://www.uoou.cz" target="_blank" rel="noopener">www.uoou.cz</a>.</li>
      </ul>
      <p>Svá práva uplatníte na adrese <a href="mailto:simulace@bfksystems.cz">simulace@bfksystems.cz</a>.
      Odpovíme nejpozději do jednoho měsíce.</p>

      <h2>7. Zabezpečení</h2>
      <p>Přenos dat mezi vaším prohlížečem a webem je šifrovaný. Přístup k údajům mají jen pracovníci,
      kteří je potřebují k vyřízení vaší poptávky nebo zakázky.</p>

      <h2>8. Změny</h2>
      <p>Zásady můžeme aktualizovat, pokud se změní způsob zpracování nebo právní úprava. Aktuální
      verze je vždy dostupná na této stránce.</p>
    </div>"""),
    "bez_kontaktu": True,
})

STRANKY.append({
    "slug": "404.html", "nav": "", "noindex": True, "bez_kontaktu": True,
    "title": "Stránka nenalezena",
    "desc": "Požadovaná stránka na webu simulacni-zkousky.cz neexistuje nebo byla přesunuta.",
    "eyebrow": "Chyba 404", "h1": "Tuhle stránku jsme nenašli",
    "breadcrumb": None,
    "intro": "<p>Odkaz může být zastaralý, nebo v adrese chybí písmeno. Zkuste některý z rozcestníků "
             "níž – nebo nám rovnou zavolejte.</p>",
    "body": sekce(
        "Kam dál",
        karty([
            (I["dok"], "Kategorie výroben",
             "<p>A1 až D – co se u které kategorie ověřuje.</p>", "index.html#kategorie"),
            (I["graf"], "Služby",
             "<p>Simulace souladu a zkoušky na místě.</p>", "index.html#sluzby"),
            (I["hodiny"], "Postup a podklady",
             "<p>Pět kroků od smlouvy o připojení po trvalý provoz.</p>", "proces-pripojeni.html"),
            (I["info"], "Časté dotazy",
             "<p>Odpovědi na nejčastější otázky.</p>", "faq.html"),
        ]),
    ),
})

# ================================================ ZDROJE A DATUM AKTUALIZACE ======
# (datum, dokumenty) – vypisuje se dole na strance jako „Aktualizováno … Zdroje: …“.
# Datum menit jen po skutecne kontrole obsahu proti uvedenym dokumentum. kontrola.py
# hlida, ze ho maji vsechny odborne stranky, a upozorni, kdyz je starsi nez pul roku.
AKTUALIZACE = "14. 9. 2026"
P4 = "PPDS, příloha 4 (2025)"
METODIKY = "(ČEZ Distribuce, EG.D, PREdistribuce)"
ZDROJE = {
    "kategorie-a1.html": (AKTUALIZACE,
        "nařízení Komise (EU) 2016/631 (RfG) · " + P4 + ", Tab. 1 a kap. 12.3 · instalační dokument "
        "výrobního modulu A1 pro žádosti o UTP od 1. 1. 2025 · přechodné podmínky EG.D a PREdistribuce "
        "k protokolům odborných laboratoří"),
    "kategorie-a2.html": (AKTUALIZACE,
        "nařízení Komise (EU) 2016/631 (RfG) · " + P4 + ", Tab. 1 a kap. 12.3 · instalační dokument "
        "výrobního modulu A2 pro žádosti o UTP od 1. 1. 2025 · přechodné podmínky EG.D a PREdistribuce "
        "k protokolům odborných laboratoří"),
    "kategorie-b1.html": (AKTUALIZACE,
        P4 + " · metodika ověřování souladu B1 " + METODIKY + ", platná od 1. 2. 2025 · Dokument "
        "výrobního modulu B1 pro UPOS povolené od 1. 12. 2024"),
    "kategorie-b2.html": (AKTUALIZACE,
        P4 + " · metodika ověřování souladu B2 " + METODIKY + ", platná od 1. 2. 2025 · Dokument "
        "výrobního modulu B2 pro UPOS povolené od 1. 12. 2024"),
    "kategorie-c-d.html": (AKTUALIZACE,
        "nařízení Komise (EU) 2016/631 (RfG), čl. 5 · " + P4 + ", Tab. 1 a kap. 9.5 · metodiky ověřování "
        "souladu C a D " + METODIKY + ", platné od 1. 2. 2025"),
    "bateriova-uloziste-zue.html": (AKTUALIZACE,
        P4 + ", kap. 12.4 · dodatky č. 1 a 2 k připojovacím podmínkám ČEZ Distribuce, platné od "
        "1. 9. 2025 · ČEZ Distribuce, ověření souladu akumulace pro žádosti o UTP od 1. 2. 2026 · "
        "metodika ověřování souladu ZUE typu D " + METODIKY + ", platná od 1. 9. 2025"),
    "pridani-baterie-k-fve.html": (AKTUALIZACE,
        P4 + " · dodatky č. 1 a 2 k připojovacím podmínkám ČEZ Distribuce pro zařízení pro ukládání "
        "elektřiny, platné od 1. 9. 2025"),
    "cez-distribuce.html": (AKTUALIZACE,
        "připojovací podmínky ČEZ Distribuce pro VN a VVN s přílohami VP_01 až VP_15, platné od "
        "1. 9. 2025 · dodatky č. 1 a 2 pro zařízení pro ukládání elektřiny, platné od 1. 9. 2025"),
    "egd.html": (AKTUALIZACE,
        "podklady EG.D pro dispečerské řízení a chránění decentrálních zdrojů (DEČE), verze 05, "
        "aktualizace 1. 11. 2025 · připojovací podmínky EG.D pro VN a VVN, platné od 1. 2. 2026"),
    "predistribuce.html": (AKTUALIZACE,
        P4 + " · společné metodiky ověřování souladu, na kterých se PREdistribuce podílí"),
    "simulace-souladu.html": (AKTUALIZACE,
        P4 + " · metodiky ověřování souladu B1, B2, C a D " + METODIKY + ", platné od 1. 2. 2025"),
    "zkousky-na-miste.html": (AKTUALIZACE,
        P4 + ", kap. 9.5 a 12.4 · metodiky ověřování souladu B1 a B2 " + METODIKY + ", platné od "
        "1. 2. 2025"),
    "proces-pripojeni.html": ("16. 9. 2026",
        P4 + ", kap. 4.8 a 12 až 12.4 · metodiky ověřování souladu B1 a B2 " + METODIKY + ", platné "
        "od 1. 2. 2025 · ČEZ Distribuce, ověření souladu akumulace pro žádosti o UTP od 1. 2. 2026"),
}

# Stranky sluzeb dostanou JSON-LD Service.
SLUZBY = {
    "simulace-souladu.html": "Simulace souladu výrobny s RfG",
    "zkousky-na-miste.html": "Zkoušky souladu výrobny na místě",
}

for _p in STRANKY:
    if _p["slug"] in ZDROJE:
        _p["zdroj"] = ZDROJE[_p["slug"]]
    if _p["slug"] in SLUZBY:
        _p["sluzba"] = SLUZBY[_p["slug"]]

PAGES = STRANKY
