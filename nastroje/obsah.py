#!/usr/bin/env python3
"""Obsah webu simulacni-zkousky.cz — jedna polozka PAGES = jedna stranka.

Vecny podklad: interni reserse BFK "Reserse pro web Simulacni zkousky"
(25. 8. 2026, podklady/Reserse_web_simulacni_zkousky.pdf), ktera cituje
metodiky CEZd / EG.D / PREdi, PPDS Prilohu 4 a RfG (EU) 2016/631.

DULEZITE — co se na web zamerne NEDAVA (rese¨rse, sekce A a E):
  * seznam laboratori (VUT, CVUT…) jako certifikatoru — certifikaty vydava
    akreditovane zkusebni pracoviste, ne laborator PDS (ta vydava protokol)
  * "zakaz SVR pred UTP" — nedolozeno
  * "vymena ochrany bez kusove zkousky" — nedolozeno
  * konkretni ceny a dodaci lhuty — chybi business input
  * reference "B1 999 kW EG.D" a "B2 4,4 MW CEZ" — nepotvrzena cisla
  * jmena vyrobcu, jejichz dynamicke modely kryje NDA
Seznam otevrenych bodu je v POZNAMKY-INTERNI.md.
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


def cta(text, tlacitko="Nezávazná poptávka", href="kontakt.html"):
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
    <p class="hero-claim-big">Simulace souladu, zkoušky na místě, Dokument výrobního modulu — od jedné firmy.</p>
    <p class="hero-lead">Bez doloženého souladu s&nbsp;RfG nevydá provozovatel distribuční soustavy souhlas s&nbsp;trvalým provozem. Od kategorie B1, tedy od 100&nbsp;kW, se část požadavků prokazuje výpočtem dopředu a část funkčními zkouškami přímo na výrobně. Děláme obojí — včetně žádostí o&nbsp;ÚPOS a&nbsp;ÚTP.</p>
    <p class="hero-claim">
      <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round"><path d="M20 6 9 17l-5-5"/></svg>
      Fotovoltaika i bateriová úložiště, 100 kW až 36 MWp
    </p>
    <div class="cta-row">
      <a class="btn btn-primary" href="kontakt.html">Nezávazná poptávka</a>
      <a class="btn btn-light" href="proces-pripojeni.html">Jak proces probíhá</a>
    </div>
  </div>
</section>
"""

HUB_UVOD = sekce(
    "Dvě různé věci pod jedním názvem",
    karty([
        (I["lupa"], "Zkoušky na místě",
         "<p>Funkční zkoušky na hotové výrobně: řízení činného výkonu, automatické opětovné připojení, "
         "regulace U, Q a cos&nbsp;φ, nastavení ochran, omezování výkonu a komunikace s dispečinkem. "
         "Kapitola 5 metodik ověřování souladu.</p>", "zkousky-na-miste.html"),
        (I["graf"], "Simulace souladu",
         "<p>Matematický model výrobny, na kterém se prokáží požadavky, které se na hotové elektrárně "
         "měřit nedají — překlenutí poruch, RoCoF, frekvenční odezva. Kapitola 6 metodik.</p>",
         "simulace-souladu.html"),
    ]),
    eyebrow="Terminologie",
    uvod='<p class="lead">„Simulační zkoušky“ je jazyk, kterým se na to ptají zákazníci. Odborně jde o dvě '
         'věci, které spolu tvoří <b>ověření souladu výrobního modulu s nařízením (EU) 2016/631 (RfG)</b>: '
         'zkoušky na místě a simulace souladu. Podle kategorie výrobny se dělá jedno, druhé, nebo obojí — '
         'a část požadavků jde nahradit certifikátem zařízení.</p>',
) + sekce(
    "Tři cesty, jak požadavek doložit",
    karty([
        (I["lupa"], "Zkouška na místě",
         "<p>Měření na hotové výrobně, technik s kvalimetrem třídy A a protokol s průběhy veličin. "
         "U kategorie B1 je takto vázáno <b>šest bodů</b>, které nelze obejít ani simulací, ani certifikátem.</p>"),
        (I["graf"], "Simulace",
         "<p>Ověřený dynamický model výrobny a report s verdiktem splněno/nesplněno pro každý bod. "
         "U kategorie B2 a výše je celá kapitola simulací povinná — včetně předání modelu distributorovi.</p>"),
        (I["dok"], "Certifikát zařízení",
         "<p>Osvědčení o souladu od akreditovaného zkušebního pracoviště. Nahradí zkoušku nebo simulaci jen tam, kde to "
         "Tabulka&nbsp;1 Dokumentu výrobního modulu připouští — a jen u výrobny z jediné výrobní jednotky.</p>"),
    ], sloupce=3)
    + callout(
        "Tady se láme rozsah prací i cena",
        "<p>Kde Tabulka 1 připouští víc cest, stačí jedna — ale doložená na všechny relevantní komponenty. "
        "Rozhodují tři omezení: body označené „jen zkouška“ nejde nahradit ničím, certifikát platí pouze pro "
        "výrobnu z jedné výrobní jednotky (čtyři střídače už certifikátem nedoložíte) a body označené (s) se "
        "ověřují na výrobnu jako celek.</p>"
        "<p>Proto se u dvou stejně velkých elektráren může rozsah ověření lišit i násobně. "
        "<a href=\"dokument-vyrobniho-modulu.html\">Jak Tabulka 1 vypadá →</a></p>"),
    eyebrow="Klíčový koncept",
    uvod='<p class="lead">Každý požadavek Dokumentu výrobního modulu se prokazuje jednou ze tří cest. '
         'Která to bude, neurčuje dodavatel ani investor — určuje to Tabulka&nbsp;1 metodiky '
         'příslušného provozovatele distribuční soustavy.</p>',
    alt=True, kotva="cesty",
) + sekce(
    "Kategorie výrobních modulů",
    tabulka(
        ["Kategorie", "Rozsah výkonu", "Zkoušky na místě", "Simulace souladu", "Certifikát"],
        [
            ['<a href="kategorie-a1.html">A1</a>', "0,8 kW – 11 kW včetně", "ne", "ne",
             "certifikát nebo protokol laboratoře"],
            ['<a href="kategorie-a2.html">A2</a>', "nad 11 kW – pod 100 kW", "ne", "ne",
             "certifikát nebo protokol laboratoře"],
            ['<a href="kategorie-b1.html">B1</a>', "100 kW – pod 1 MW",
             "<b>6 bodů „jen zkouška“</b>", "10 / 12 bodů — lze i certifikátem",
             "jen výrobna z 1 VJ"],
            ['<a href="kategorie-b2.html">B2</a>', "1 MW – pod 30 MW", "ano, širší rozsah než B1",
             "povinná celá kapitola 6 + předání modelu", "jen výrobna z 1 VJ"],
            ['<a href="kategorie-c-d.html">C</a>', "30 MW – pod 75 MW", "ano", "ano, plný rozsah",
             "částečně"],
            ['<a href="kategorie-c-d.html">D</a>', "od 75 MW <b>nebo</b> připojení na 110 kV a výše",
             "ano", "ano — až 19 testů 6.1–6.19", "částečně"],
        ],
        poznamky=[
            "Dělení A1/A2 a B1/B2 je české upřesnění, v RfG není. U nesynchronních výroben "
            "(fotovoltaika, bateriová úložiště) se posuzuje celkový výkon výrobny, ne jednotlivé moduly.",
            "<b>Kategorie je uvedena ve smlouvě o připojení</b> a ta je vždy rozhodující. "
            "Do kategorie D vedou dvě cesty — výkon od 75 MW, nebo napěťová hladina 110 kV a výše "
            "bez ohledu na výkon.",
            "<b>Pozor na jednotky:</b> <i>kWp</i> je špičkový výkon fotovoltaických panelů, "
            "<i>Pn</i> je jmenovitý činný výkon výrobního modulu (typicky dán střídači) a "
            "<i>rezervovaný výkon</i> je hodnota sjednaná ve smlouvě o připojení. Kategorii "
            "neurčuje kWp — 698 kWp panelů může být výrobní modul s Pn 550 kW. Rozhodný údaj "
            "vždy ověřujeme podle smlouvy o připojení a definice příslušného provozovatele.",
        ],
        min_sirka=880,
    ),
    eyebrow="Do které kategorie spadáte",
    uvod="<p>Rozsah povinností se řídí instalovaným výkonem a napěťovou hladinou. Klikněte na kategorii — "
         "u každé je popsané, co se prokazuje, co se měří na místě a jaké dokumenty distributor chce.</p>",
    kotva="kategorie",
) + sekce(
    "Proces připojení v pěti krocích",
    kroky([
        ("Smlouva o připojení a projekt",
         "SoP určí kategorii výrobního modulu a rezervovaný výkon. K projektové dokumentaci se PDS "
         "vyjadřuje do 30 dnů.", "SoP + PD"),
        ("Žádost o ÚPOS",
         "Dossier podle PPDS, přílohy 4, kap. 12.1, body a)–j). PDS rozhodne do 30 dnů od úplné žádosti "
         "a vydá Dočasné provozní oznámení.", "Vyřídíme za vás"),
        ("Zkoušky a simulace",
         "Dočasný provoz platí nejdéle 12 měsíců. U každého bodu Tabulky 1 se volí cesta ověření: "
         "zkouška, simulace, nebo certifikát.", "Naše práce"),
        ("Protokoly a DVM",
         "Každé ověření = protokol s průběhy veličin a verdiktem splněno/nesplněno. Vyplněný Dokument "
         "výrobního modulu to shrnuje.", "Naše práce"),
        ("ÚTP a konečné provozní oznámení",
         "Žádost o trvalý provoz. Zkoušky řádně provedené v rámci ÚPOS už PDS neopakuje. KPO platí do "
         "odpojení výrobny.", "Vyřídíme za vás"),
    ])
    + cta("<b>Načasování rozhoduje.</b> Dočasný provoz je omezený na 12 měsíců a zkoušky fotovoltaiky "
          "potřebují dostatečný osvit — termín s distributorem se sjednává týdny předem. Čím dřív o fázi "
          "ověření víte, tím méně zdrží.",
          "Probrat termín", "kontakt.html"),
    eyebrow="Kde ve stavbě se to řeší",
    uvod='<p>Ověření souladu není poslední razítko, ale samostatná fáze mezi dostavbou a trvalým provozem. '
         'Detailní časová osa i všechny lhůty jsou na stránce <a href="proces-pripojeni.html">proces '
         'připojení</a>.</p>',
    alt=True, kotva="proces",
) + sekce(
    "Co pro vás uděláme",
    karty([
        (I["graf"], "Simulace souladu",
         "<p>Dynamický model výrobny v DIgSILENT PowerFactory, katalog testů podle kategorie a report "
         "s kvantitativním verdiktem pro každý bod.</p>", "simulace-souladu.html"),
        (I["lupa"], "Zkoušky na místě",
         "<p>Jeden výjezd, všechny protokoly. Kvalimetr třídy A podle ČSN EN 61000-4-30, koordinace "
         "s dispečinkem a se servisem střídačů.</p>", "zkousky-na-miste.html"),
        (I["stit"], "Zkoušky ochran",
         "<p>Funkční zkouška ochran rozpadového místa a protokol o nastavení ochran — povinná položka "
         "žádosti o ÚPOS.</p>", "zkousky-ochran.html"),
        (I["sit"], "RTU a dispečerské řízení",
         "<p>Audit signálů proti tabulce telemetrie, doplnění RTU, funkční zkouška přenosu dat "
         "s dispečinkem a protokol.</p>", "rtu-dispecerske-rizeni.html"),
        (I["dok"], "Dokumentace a jednání s PDS",
         "<p>Žádost o ÚPOS i o ÚTP, vyplněný Dokument výrobního modulu, místní provozní předpisy "
         "a vypořádání připomínek distributora.</p>", "podklady.html"),
        (I["baterie"], "Bateriová úložiště",
         "<p>Vlastní metodika ZUE od 1. 9. 2025: ověření v režimu dodávky i odběru, jiné hodnoty ochran, "
         "samostatný dokument ověřování souladu.</p>", "bateriova-uloziste-zue.html"),
    ], sloupce=3),
    eyebrow="Služby",
    uvod="<p>Velkou část studií zpracováváme pro jiné dodavatele fotovoltaiky a pro investory, kteří si "
         "stavbu zajistili sami. Elektrárnu jsme stavět nemuseli — potřebujeme od vás jen podklady.</p>",
    kotva="sluzby",
) + sekce(
    "Metodiky jsou společné, procesy nejsou",
    karty([
        (I["tovarna"], "ČEZ Distribuce",
         "<p>Připojovací podmínky vn/vvn od 1. 9. 2025 s přílohami VP_01–VP_15: nastavení ochran, "
         "charakteristika Q(U), telemetrie, fyzický test omezování výkonu.</p>", "cez-distribuce.html"),
        (I["tovarna"], "EG.D",
         "<p>Podklady DE ČE pro dispečerské řízení a chránění ve dvou verzích podle výkonu, stupně "
         "řízení P0–P4 a procesní formuláře podle čl. 41 RfG.</p>", "egd.html"),
        (I["tovarna"], "PREdistribuce",
         "<p>Praha a Roztoky, podnikové normy řady PN KA 5xx. Nadřazený rámec je shodný — PREdistribuce "
         "je spoluautorem společných metodik.</p>", "predistribuce.html"),
    ], sloupce=3),
    eyebrow="Provozovatelé distribučních soustav",
    uvod="<p><b>Metodiky ověřování souladu B1 a B2 (od 1. 2. 2025) i metodika pro bateriová úložiště "
         "(od 1. 9. 2025) jsou společné pro ČEZ Distribuce, EG.D a PREdistribuce.</b> Co se ověřuje, je "
         "tedy stejné. Liší se připojovací podmínky, formuláře, telemetrie a nastavení ochran.</p>",
    alt=True, kotva="pds",
) + sekce(
    "Co se v posledních měsících změnilo",
    karty([
        (I["dok"], "Protokolům laboratoří končí platnost",
         "<p>Protokol odborné laboratoře (ČEZ Distribuce, EG.D) je u A1 a A2 pořád platnou alternativou "
         "certifikátu — ale jen ten <b>vydaný do 31. 12. 2025</b> a jen <b>do 31. 12. 2026</b>. "
         "Od 1. 1. 2027 uznají distributoři už jen osvědčení o souladu od akreditovaného "
         "certifikátora. Starší podklady ke střídačům je načase projít.</p>", "kategorie-a2.html"),
        (I["baterie"], "Bateriová úložiště mají vlastní metodiku",
         "<p>Od <b>1. 9. 2025</b> platí společná metodika ověřování souladu ZUE a dodatky připojovacích "
         "podmínek ČEZ Distribuce. Ověřuje se v obou provozních režimech a hodnoty ochran se od "
         "fotovoltaiky liší.</p>", "bateriova-uloziste-zue.html"),
        (I["sit"], "Nové připojovací podmínky",
         "<p>ČEZ Distribuce vydala připojovací podmínky vn/vvn s platností od <b>1. 9. 2025</b>, EG.D "
         "připojovací podmínky VN/VVN od <b>1. 2. 2026</b> — měřicí soupravy u výroben nad 250 kW "
         "a trafostanice žadatele.</p>", "cez-distribuce.html"),
    ], sloupce=3),
    eyebrow="Aktuálně",
    uvod="<p>Agenda ověřování souladu se mění každou sezónu. Tři změny, které se právě teď nejčastěji "
         "podepisují na rozsahu prací:</p>",
    kotva="aktualne",
)

STRANKY.append({
    "slug": "index.html",
    "nav": "",
    "title": "Simulační zkoušky a ověření souladu RfG | BFK Systems",
    "desc": "Ověření souladu výroben s RfG: simulace souladu v DIgSILENT PowerFactory, zkoušky na místě, "
            "Dokument výrobního modulu, žádosti o ÚPOS a ÚTP. Fotovoltaika i baterie od 100 kW.",
    "prio": "1.0",
    "body": HERO + '<div class="stats-band">\n  <div class="container grid">\n'
            '      <div><div class="num">100 kW – 36 MWp</div><div class="label">Rozsah zpracovaných studií</div></div>\n'
            '      <div><div class="num">Desítky</div><div class="label">Protokolů ověření souladu</div></div>\n'
            '      <div><div class="num">3 hlavní PDS</div><div class="label">ČEZ Distribuce · EG.D · PREdistribuce</div></div>\n'
            '  </div>\n</div>\n' + HUB_UVOD,
    "faq": [
        ("Co jsou „simulační zkoušky“?",
         "<p>Souhrnné označení pro ověření souladu výrobny s RfG: <b>simulace souladu</b> (matematický "
         "model výrobny) a <b>zkoušky na místě</b> (měření na hotové elektrárně). Rozsah obojího určuje "
         "kategorie výrobního modulu.</p>"),
        ("Od jakého výkonu se mě to týká?",
         "<p>Ověření souladu se týká každé výrobny a každého bateriového úložiště připojeného paralelně "
         "s distribuční soustavou. Do 100 kW (kategorie A1 a A2) se ale prokazuje jen doklady k zařízení "
         "— certifikátem, nebo protokolem laboratoře — bez zkoušek na výrobně a bez simulací. "
         "Od 100 kW (kategorie B1) přicházejí zkoušky "
         "na místě i simulace.</p>"),
        ("Jak zjistím kategorii své výrobny?",
         "<p>Je uvedena ve <b>smlouvě o připojení</b>. Orientačně ji poznáte z výkonu podle tabulky výš — "
         "u fotovoltaiky s baterií se posuzuje celkový výkon výrobny. Rozhodující je vždy smlouva.</p>"),
        ("Musí k nám u B1 někdo fyzicky přijet?",
         "<p>Ano. U kategorie B1 je šest bodů vázaných výhradně na zkoušku na místě: řízení činného "
         "výkonu, automatické opětovné připojení, komunikace a výměna informací, regulace U/Q/cos φ, "
         "nastavení ochran a omezování výkonu. Zbytek se dá doložit od stolu simulací nebo certifikátem.</p>"),
        ("Kdy stačí certifikát a nemusí se nic měřit?",
         "<p>Jen u bodů, kde to Tabulka 1 připouští, a <b>jen u výrobny složené z jediné výrobní "
         "jednotky</b>. Máte-li čtyři střídače, certifikátem to nedoložíte a řeší se to simulací celé "
         "výrobny. Body „jen zkouška“ nenahradí certifikát nikdy.</p>"),
        ("Platí ještě protokoly laboratoří?",
         "<p>Ano, ale s dvojím omezením. Protokol odborné laboratoře — dnes těm požadavkům vyhovují "
         "laboratoře <b>ČEZ Distribuce</b> a <b>EG.D</b> — nahrazuje u A1 a A2 certifikát jen tehdy, "
         "byl-li <b>vydán nejpozději 31. 12. 2025</b>, a distributoři ho akceptují <b>do 31. 12. 2026</b>. "
         "Od <b>1. 1. 2027</b> jde soulad A1 a A2 doložit už jen osvědčením o souladu od akreditovaného "
         "zkušebního pracoviště podle nařízení (ES) č. 765/2008, nebo výjimkou ERÚ.</p>"),
        ("Děláte to i pro elektrárny, které jste nestavěli?",
         "<p>Ano, tvoří to velkou část naší práce — zpracováváme studie pro jiné dodavatele fotovoltaiky "
         "i pro investory. Potřebujeme <a href=\"podklady.html\">podklady</a>, ne vlastní stavbu.</p>"),
    ],
    "faq_nadpis": "Na co se ptají nejčastěji",
    "cross": [("Všechny časté dotazy", "faq.html"), ("Slovník pojmů RfG", "slovnik-rfg.html"),
              ("Reference", "reference.html"), ("Podklady k zahájení", "podklady.html")],
})

# ========================================================== KATEGORIE ======
BC_KAT = [("Kategorie výroben", "index.html#kategorie")]

STRANKY.append({
    "slug": "kategorie-a1.html", "nav": "kategorie", "reviewed": True,
    "title": "Výrobní modul A1 — připojení FVE do 11 kW",
    "desc": "Kategorie A1 (0,8 až 11 kW): soulad se prokazuje instalačním dokumentem a certifikáty "
            "zařízení. Žádné zkoušky na výrobně, žádné simulace. Co po vás distributor chce.",
    "eyebrow": "Kategorie výrobního modulu", "h1": "Výrobní modul A1 — do 11 kW",
    "bc_nazev": "Kategorie A1", "breadcrumb": BC_KAT,
    "intro": "<p>Nejmenší kategorie výrobních modulů. Prakticky každá domácí fotovoltaika. Dobrá zpráva: "
             "<b>žádné zkoušky na výrobně ani simulace se nedělají</b> — všechno se dokládá papírově. "
             "Špatná zpráva: papíry musí sedět, jinak distributor trvalý provoz nepovolí.</p>",
    "stats": [("0,8 – 11 kW", "Rozsah kategorie A1"), ("0", "Zkoušek a simulací na výrobně")],
    "body": sekce(
        "Co pro A1 platí",
        karty([
            (I["blesk"], "Rozsah a připojení",
             "<p>Od 0,8 kW do 11 kW včetně, zpravidla do sítě nízkého napětí. Jednofázové připojení do nn "
             "je omezeno na <b>3,7 kVA na fázi</b>. Výstupní výkon střídače (desetiminutový průměr) nesmí "
             "překročit <b>110 % jmenovitého výkonu</b>.</p>"),
            (I["dok"], "Instalační dokument místo DVM",
             "<p>Soulad se prokazuje <b>Instalačním dokumentem výrobního modulu A1</b> (zveřejněn "
             "1. 10. 2024, platný od 1. 1. 2025) a certifikáty použitého zařízení. Dokument vyplňuje "
             "a podepisuje odborná firma, která výstavbu realizuje.</p>"),
            (I["check"], "Certifikát, protokol, nebo výjimka",
             "<p>Soulad se dokládá osvědčením o souladu (certifikátem) od <b>akreditovaného zkušebního "
             "pracoviště</b> podle nařízení (ES) č. 765/2008, protokolem odborné laboratoře, nebo výjimkou "
             "ERÚ. Protokol platí přechodně: musí být vydaný do 31. 12. 2025 a uznává se do 31. 12. 2026.</p>"),
            (I["hodiny"], "Bez fáze dočasného provozu",
             "<p>U kategorií A1 a A2 se žádost o uvedení do trvalého provozu podává rovnou po splnění "
             "podmínek smlouvy o připojení — nečeká se na zkoušky, protože žádné nejsou.</p>"),
        ]),
        eyebrow="Fakta",
    ) + sekce(
        "Co po vás distributor bude chtít",
        seznam([
            "Smlouvu o připojení a splnění jejích podmínek",
            "Vyplněný a podepsaný Instalační dokument výrobního modulu A1",
            "Certifikáty střídače od akreditovaného certifikátora",
            "Výchozí revizi elektrického zařízení výrobny i přípojky",
            "Projektovou dokumentaci a jednopólové schéma",
            "Protokol o nastavení ochran, pokud jej podmínky připojení vyžadují",
        ]) + callout(
            "Zkontrolujte si doklad ke střídači",
            "<p>Nejčastější zádrhel u malých elektráren není zkouška, ale doklad ke střídači: certifikát "
            "nemusí pokrývat všechny požadavky instalačního dokumentu a u protokolu laboratoře je potřeba "
            "hlídat, že byl vydaný do 31. 12. 2025 — po 31. 12. 2026 už ho distributor neuzná. Ověříme, "
            "co váš střídač doloží a co bude potřeba doplnit.</p>"),
        eyebrow="Checklist", alt=True,
    ) + sekce("", ZDROJ.format(
        "Instalační dokument VM A1 (synchronní i nesynchronní), zveřejněn 1. 10. 2024, platný od "
        "1. 1. 2025 · PPDS, příloha 4, Tab. 1"), ),
    "faq": [
        ("Musím u malé fotovoltaiky dělat nějaké zkoušky?",
         "<p>Ne. U kategorie A1 se soulad prokazuje jen doklady k zařízení — certifikátem, nebo "
         "protokolem laboratoře — a instalačním dokumentem. Zkoušky na výrobně ani simulace se "
         "nedělají.</p>"),
        ("Kdo instalační dokument vyplňuje a podepisuje?",
         "<p>Odborná firma, která výstavbu realizuje. Součástí je i seznam certifikátů použitého "
         "zařízení.</p>"),
        ("Střídač má certifikát ze zahraničí. Platí v Česku?",
         "<p>Jen pokud jej vydal subjekt akreditovaný podle nařízení (ES) 765/2008 pro požadavky PPDS, "
         "přílohy 4. Samotné prohlášení výrobce nestačí.</p>"),
    ],
    "cross": [("Kategorie A2 — 11 až 100 kW", "kategorie-a2.html"),
              ("Slovník pojmů RfG", "slovnik-rfg.html"),
              ("Proces připojení", "proces-pripojeni.html")],
})

STRANKY.append({
    "slug": "kategorie-a2.html", "nav": "kategorie", "reviewed": True,
    "title": "Výrobní modul A2 — 11 až 100 kW a certifikát střídače",
    "desc": "Kategorie A2 (11 až 100 kW): soulad certifikátem střídače přes instalační dokument. "
            "Protokol odborné laboratoře platí přechodně do 31. 12. 2026, pak už jen certifikát.",
    "eyebrow": "Kategorie výrobního modulu", "h1": "Výrobní modul A2 — 11 až 100 kW",
    "claim": "Rozhoduje certifikát vašeho střídače.",
    "bc_nazev": "Kategorie A2", "breadcrumb": BC_KAT,
    "intro": "<p>Typická firemní střešní elektrárna. Stejně jako u A1 se nic neměří na výrobně a nedělají "
             "se simulace — ale požadavky jsou širší a všechno stojí a padá s tím, co má doložené váš "
             "střídač.</p>",
    "stats": [("11 – 100 kW", "Rozsah kategorie A2"), ("31. 12. 2026", "Dokdy platí protokoly laboratoří")],
    "body": sekce(
        "Co pro A2 platí",
        karty([
            (I["blesk"], "Rozsah a požadavky",
             "<p>Nad 11 kW a pod 100 kW, zpravidla nízké napětí (výjimečně vn). Nad rámec kategorie A1 "
             "přebírá <b>vybrané požadavky kategorie B</b> — čl. 14.2 až 14.5 a čl. 20 RfG.</p>"),
            (I["dok"], "Instalační dokument VM A2",
             "<p>Soulad se opět prokazuje jen doklady k zařízení prostřednictvím instalačního dokumentu "
             "platného od 1. 1. 2025. Bez zkoušek na výrobně, bez simulací.</p>"),
            (I["check"], "Jaký certifikát uznají",
             "<p>Osvědčení o souladu vydané <b>akreditovaným zkušebním pracovištěm</b> podle nařízení "
             "(ES) č. 765/2008 a ČSN EN ISO/IEC 17025:2018. "
             "Je-li certifikátů víc, přikládá se příloha s uvedením, na jaké zařízení a na jaký požadavek "
             "byl každý vydán.</p>"),
            (I["sipky"], "U EG.D navíc formuláře",
             "<p>K instalačnímu dokumentu se u EG.D dokládají procesní formuláře <b>0920-G97</b> (povinné "
             "doklady podle čl. 41.3 RfG) a <b>0920-G98</b> (rozdělení odpovědností podle čl. 41.4).</p>"),
        ]),
        eyebrow="Fakta",
    ) + sekce(
        "Co dělat, když certifikát nepokrývá všechno",
        "<p class=\"lead\">Situace, kterou řešíme nejčastěji: elektrárna stojí, ale doklady ke střídači "
        "jsou starší a část požadavků instalačního dokumentu nepokrývají. Postup je vždy stejný.</p>"
        '    <ol class="kroky">'
        "<li>Projdeme instalační dokument bod po bodu proti tomu, co certifikát skutečně obsahuje.</li>"
        "<li>Vyžádáme od výrobce doplňující certifikát nebo aktuální verzi k danému firmwaru.</li>"
        "<li>Když doplnit nejde, navrhneme technické řešení — jiné zařízení nebo úpravu konfigurace.</li>"
        "<li>Zkompletujeme dokumentaci a podáme ji distributorovi.</li></ol>"
        + callout(
            "Protokolům laboratoří končí platnost",
            "<p>Protokol odborné laboratoře (ČEZ Distribuce, EG.D) nahrazuje certifikát jen tehdy, byl-li "
            "<b>vydaný nejpozději 31. 12. 2025</b> — a distributoři ho uznají <b>jen do 31. 12. 2026</b>. "
            "Od 1. 1. 2027 zbývá osvědčení o souladu od akreditovaného certifikátora, nebo výjimka ERÚ. "
            "Máte-li podklady ze starší instalace, zkontrolujte je dřív, než je pošlete s žádostí.</p>"),
        eyebrow="Praxe", alt=True,
    ) + sekce("", ZDROJ.format(
        "Instalační dokument VM A2 (platný od 1. 1. 2025) · formuláře EG.D 0920-G97 a 0920-G98 · "
        "PPDS, příloha 4, Tab. 1 · ČEZ Distribuce, Ověření souladu s RfG, a EG.D, Změna procesu "
        "prokázání souladu s RfG — ověřeno 3. 9. 2026")),
    "faq": [
        ("Co když certifikát nepokrývá všechny požadavky?",
         "<p>Doplní se doklady od výrobce, případně se mění zařízení nebo jeho konfigurace. "
         "Projdeme s vámi, co konkrétně chybí.</p>"),
        ("Potřebuju u A2 simulační studii?",
         "<p>Ne. Simulace se u kategorií A1 a A2 nedělají. Zlom je až na 100 kW, kde začíná kategorie "
         "B1.</p>"),
        ("Mám 99 kW. Nevyplatí se přidat kilowatt?",
         "<p>Rozhodně ne bez rozmyslu — od 100 kW spadáte do kategorie B1 a proces se výrazně rozšíří: "
         "dočasný provoz pro ověření, šest funkčních zkoušek na místě a Dokument výrobního modulu. "
         "Rozdíl v pracnosti je řádový.</p>"),
    ],
    "cross": [("Kategorie B1 — od 100 kW", "kategorie-b1.html"),
              ("EG.D — formuláře a dispečerské řízení", "egd.html"),
              ("Slovník pojmů RfG", "slovnik-rfg.html")],
})

STRANKY.append({
    "slug": "kategorie-b1.html", "nav": "kategorie", "reviewed": True,
    "title": "Ověření souladu B1 — výrobny 100 kW až 1 MW",
    "desc": "Kategorie B1: šest funkčních zkoušek na místě, zbytek bodů simulací nebo certifikátem. "
            "Společná metodika ČEZ Distribuce, EG.D a PREdistribuce platná od 1. 2. 2025.",
    "eyebrow": "Kategorie výrobního modulu", "h1": "Ověření souladu B1 — 100 kW až 1 MW",
    "claim": "Většinu doložíme od stolu. Na místě zbývá šest zkoušek.",
    "bc_nazev": "Kategorie B1", "breadcrumb": BC_KAT,
    "intro": "<p>První kategorie, kde se skutečně měří. Od 100 kW včetně přichází dočasný provoz pro "
             "ověření souladu, Dokument výrobního modulu a technik na výrobně. Rozsah je ale menší, než "
             "se obvykle čeká — <b>velkou část požadavků jde doložit simulací nebo certifikátem</b>.</p>",
    "stats": [("16 / 18", "Bodů Tabulky 1 (synchronní / nesynchronní)"),
              ("6", "Bodů vázaných jen na zkoušku"),
              ("12 měsíců", "Nejdelší platnost dočasného provozu")],
    "anchors": kotvy([("Co metodika žádá", "fakta"), ("Šest zkoušek na místě", "zkousky"),
                      ("Co doložíme od stolu", "od-stolu"), ("Časté dotazy", "faq")]),
    "body": sekce(
        "Jedna metodika pro tři distributory",
        karty([
            (I["dok"], "Společná metodika od 1. 2. 2025",
             "<p>Metodika ověřování souladu B1 je <b>společná pro ČEZ Distribuce, EG.D i "
             "PREdistribuce</b> (Dokumenty výrobního modulu zveřejněny 1. 12. 2024). Jeden dokument "
             "pokrývá synchronní (16 bodů) i nesynchronní (18 bodů) výrobní moduly.</p>"),
            (I["blesk"], "Nesynchronní moduly navíc",
             "<p>Fotovoltaika a bateriová úložiště mají oproti synchronním zdrojům dva simulační body "
             "navíc — <b>rychlý poruchový proud (k = 2)</b> a <b>prioritu jalového výkonu před "
             "činným</b>.</p>"),
            (I["hodiny"], "Rok na dokončení",
             "<p>Ověření se dokončuje v rámci dočasného provozu (ÚPOS). Ten platí nejdéle "
             "<b>12 měsíců</b> podle harmonogramu zkoušek, který se předkládá se žádostí.</p>"),
            (I["info"], "Zjištěné závady proces zastaví",
             "<p>Při špatně nastavených ochranách nebo nefunkčním automatickém opětovném připojení "
             "distributor zkoušky přeruší — na místě, nebo písemně do 15 pracovních dnů.</p>"),
        ]),
        eyebrow="Fakta", kotva="fakta",
    ) + sekce(
        "Šest bodů, které se musí odměřit na výrobně",
        wp([
            ("1", "Řízení činného výkonu — u nesynchronních modulů s úpravou do jedné minuty."),
            ("2", "Automatické opětovné připojení po výpadku."),
            ("3", "Komunikace a výměna informací s dispečinkem provozovatele distribuční soustavy."),
            ("4", "Regulace napětí, jalového výkonu a účiníku (U / Q / cos φ)."),
            ("5", "Nastavení ochran rozpadového místa."),
            ("6", "Omezování činného výkonu."),
        ]) + callout(
            "Tohle nejde obejít",
            "<p>Body označené v Tabulce 1 jako „jen zkouška“ nenahradí simulace ani certifikát. Kdo "
            "tvrdí, že se u B1 nic neměří, metodiku nečetl — a distributor to pozná. Zkoušky se navíc "
            "provádějí <b>na výrobnu jako celek</b>, ne na jeden střídač.</p>"
            "<p>Dobrá zpráva: zvládnou se v jednom výjezdu. "
            "<a href=\"zkousky-na-miste.html\">Jak zkoušky probíhají →</a></p>", warn=True),
        eyebrow="Zkoušky na místě", alt=True, kotva="zkousky",
    ) + sekce(
        "Zbytek doložíme od stolu",
        "<p class=\"lead\">Zbývajících 10 bodů u synchronních a 12 bodů u nesynchronních modulů lze "
        "prokázat <b>simulací nebo certifikátem</b>. Která cesta bude levnější, se rozhoduje podle "
        "konfigurace střídačů.</p>"
        + karty([
            (I["graf"], "Simulace celé výrobny",
             "<p>Model v DIgSILENT PowerFactory pokryje výrobnu bez ohledu na počet střídačů. "
             "Nezbytná, jakmile se výrobna skládá z víc výrobních jednotek.</p>", "simulace-souladu.html"),
            (I["dok"], "Certifikát zařízení",
             "<p>Levnější cesta — ale použitelná <b>jen u výrobny z jediné výrobní jednotky</b> a jen "
             "tam, kde to Tabulka 1 připouští.</p>", "dokument-vyrobniho-modulu.html"),
        ])
        + cta("<b>Čtyři střídače? Certifikát vám nepomůže.</b> Řekněte nám počet a typ střídačů "
              "a kategorii ze smlouvy o připojení — obratem víte, jestli se u vás rozsah ověření řeší "
              "certifikáty, nebo simulací."),
        eyebrow="Simulace nebo certifikát", kotva="od-stolu",
    ) + sekce("", ZDROJ.format(
        "Metodika ověřování souladu B1 (synchronní i nesynchronní), ČEZ Distribuce + EG.D + "
        "PREdistribuce, platná od 1. 2. 2025 · PPDS, příloha 4")),
    "faq": [
        ("Musí k nám na B1 přijet technik?",
         "<p>Ano — na šest funkčních zkoušek. Zbytek požadavků se dokládá simulacemi, certifikáty "
         "a vyplněným Dokumentem výrobního modulu.</p>"),
        ("Máme čtyři střídače, stačí certifikáty?",
         "<p>Ne. Certifikát platí jen pro výrobnu složenou z jedné výrobní jednotky. U víc střídačů se "
         "příslušné body řeší simulací celé výrobny.</p>"),
        ("Jak dlouho ověření B1 trvá?",
         "<p>Limit dočasného provozu je 12 měsíců a je nastavený podle harmonogramu zkoušek, který "
         "se předkládá se žádostí. Reálný termín závisí hlavně na dostupnosti podkladů, na koordinaci "
         "s dispečinkem a u fotovoltaiky na počasí — zkouška opětovného připojení potřebuje dostatečný "
         "osvit.</p>"),
        ("Co když zkouška napoprvé neprojde?",
         "<p>Stává se to a není to konec projektu. Typicky se mění parametrizace střídačů nebo nastavení "
         "ochran, závada se odstraní a domluví se nový termín. Proto se simulace dělají dřív než "
         "zkoušky.</p>"),
    ],
    "cross": [("Zkoušky na místě", "zkousky-na-miste.html"), ("Simulace souladu", "simulace-souladu.html"),
              ("Dokument výrobního modulu", "dokument-vyrobniho-modulu.html"),
              ("ÚPOS — dočasný provoz", "upos.html"), ("Kategorie B2", "kategorie-b2.html")],
})

STRANKY.append({
    "slug": "kategorie-b2.html", "nav": "kategorie", "reviewed": True,
    "title": "Simulace souladu B2 — výrobny 1 až 30 MW",
    "desc": "Kategorie B2: povinná celá kapitola simulací souladu, předání ověřeného modelu výrobny "
            "distributorovi a praktické zkoušky na místě. 24 až 27 bodů Tabulky 1.",
    "eyebrow": "Kategorie výrobního modulu", "h1": "Simulace souladu B2 — 1 až 30 MW",
    "claim": "Skok proti B1: celá kapitola simulací je povinná.",
    "bc_nazev": "Kategorie B2", "breadcrumb": BC_KAT,
    "intro": "<p>Od 1 MW se rozsah ověření zásadně mění. K funkčním zkouškám na místě přibývá "
             "<b>povinná celá kapitola simulací souladu</b> a povinnost předat provozovateli distribuční "
             "soustavy ověřený simulační model výrobny. Počet bodů Tabulky 1 skáče z 16/18 na 24/27.</p>",
    "stats": [("24 / 27", "Bodů Tabulky 1 (synchronní / nesynchronní)"),
              ("Povinná", "Celá kapitola simulací souladu"),
              ("12 měsíců", "Nejdelší platnost dočasného provozu")],
    "anchors": kotvy([("Co se mění proti B1", "rozdil"), ("Katalog simulací", "simulace"),
                      ("Jak to dodáváme", "dodavka"), ("Časté dotazy", "faq")]),
    "body": sekce(
        "Co se mění proti kategorii B1",
        karty([
            (I["graf"], "Povinná kapitola simulací",
             "<p>Zatímco u B1 jde o jednotlivé body, u B2 je <b>celá kapitola simulací souladu "
             "povinná</b>: frekvenční stabilita, RoCoF, LFSM-O i LFSM-U, FSM, překlenutí poruch UVRT "
             "a OVRT, obnova činného výkonu po poruše, napěťová stabilita, podpora napětí jalovým "
             "výkonem, ostrovní provoz, robustnost a detekce ztráty úhlové stability. Nesynchronní "
             "moduly mají navíc rychlý poruchový proud, prioritu Q před P a tlumení oscilací.</p>"),
            (I["sipky"], "Předání modelu distributorovi",
             "<p>Povinnou součástí je <b>předání ověřeného simulačního modelu výrobny</b>. Model musí "
             "odrážet ustálený stav, přechodné i elektromagnetické jevy — ne jen jednu vybranou "
             "situaci.</p>"),
            (I["blesk"], "Přebírá požadavky kategorie C",
             "<p>B2 přejímá vybrané požadavky kategorie C podle čl. 15 RfG — v praxi „malé C“. "
             "Umělou setrvačnost ale ČEZ Distribuce po kategorii B2 nepožaduje (jen C a D).</p>"),
            (I["lupa"], "Zkoušky na místě zůstávají",
             "<p>Praktické zkoušky se nikam neztrácejí — rozsah je obdobný jako u B1 a podle typu "
             "zařízení se rozšiřuje. Simulace je nenahrazují, doplňují.</p>"),
        ]),
        eyebrow="Rozdíl", kotva="rozdil",
    ) + sekce(
        "Riziko není technika, ale zdržení",
        "<p class=\"lead\">U projektů této velikosti bývá největší problém kalendář. Dočasný provoz "
        "trvá nejdéle 12 měsíců a v té době musí být hotové simulace, zkoušky, protokoly i vyplněný "
        "Dokument výrobního modulu. Když se model vrátí k přepracování, čas ubývá rychle.</p>"
        + karty([
            (I["info"], "Proč distributor vrací simulace",
             "<p>Nejčastěji proto, že model neodpovídá skutečné konfiguraci výrobny, je chybně zvolený "
             "referenční výkon u frekvenčních testů, nebo jsou protokoly neúplné. Všechny tři důvody jde "
             "ošetřit ještě před odevzdáním.</p>"),
            (I["hodiny"], "Simulace dřív než zkoušky",
             "<p>Simulace odhalí, co je potřeba přenastavit — a to je levnější zjistit u počítače než "
             "na výrobně s technikem a dispečinkem. Proto pořadí: model, úpravy, teprve pak výjezd.</p>"),
        ], sloupce=2)
        + cta("Rozdíl mezi B1 a B2 není v ceně o pár procent — je v tom, že u B2 přibývá celá "
              "kapitola simulací a předání modelu. <b>Pošlete nám smlouvu o připojení</b> a řekneme "
              "vám rozsah dřív, než začne běžet dočasný provoz."),
        eyebrow="Praxe", alt=True, kotva="simulace",
    ) + sekce(
        "Jak to dodáváme",
        wp([
            ("A", "Simulace souladu — model výrobny v DIgSILENT PowerFactory, katalog testů podle "
                  "metodiky, report s verdiktem splněno/nesplněno u každého bodu, předání modelu "
                  "distributorovi."),
            ("B", "Zkoušky na místě — jeden výjezd, kvalimetr třídy A podle ČSN EN 61000-4-30, "
                  "koordinace s dispečinkem, ochranářem i servisem střídačů."),
            ("C", "Dokumentace — vyplněný Dokument výrobního modulu, protokoly, žádost o ÚPOS "
                  "a o ÚTP, vypořádání připomínek distributora."),
        ]),
        eyebrow="Část A, B, C", kotva="dodavka",
    ) + sekce("", ZDROJ.format(
        "Metodika ověřování souladu B2 (synchronní i nesynchronní), ČEZ Distribuce + EG.D + "
        "PREdistribuce, platná od 1. 2. 2025 · upřesnění požadavků RfG ČEZ Distribuce (VP_09) "
        "platné od 1. 9. 2025")),
    "faq": [
        ("Proč distributor chce simulační model celé výrobny?",
         "<p>Předání ověřeného modelu je samostatný bod Tabulky 1. Distributor s ním počítá stabilitu "
         "sítě v místě připojení — proto model musí odrážet ustálený stav i dynamické děje.</p>"),
        ("Máme střídače bez modelu od výrobce. Co teď?",
         "<p>Část dynamických modelů máme k dispozici od výrobců, u zbytku se model validuje proti "
         "měření. Řekněte nám typ střídače a ověříme, na čem jsme.</p>"),
        ("Co když simulace nevyjdou?",
         "<p>Upraví se nastavení výrobních jednotek nebo ochran a test se opakuje. Právě proto se "
         "simulace dělají před zkouškami na místě — úprava v modelu stojí zlomek toho co opakovaný "
         "výjezd.</p>"),
        ("Je u B2 potřeba umělá setrvačnost?",
         "<p>ČEZ Distribuce ji po kategorii B2 nepožaduje — týká se kategorií C a D. Rozhodující jsou "
         "vždy podmínky připojení konkrétního provozovatele a smlouva o připojení.</p>"),
    ],
    "cross": [("Simulace souladu (služba)", "simulace-souladu.html"),
              ("Zkoušky na místě", "zkousky-na-miste.html"),
              ("Kategorie C a D", "kategorie-c-d.html"),
              ("Dokument výrobního modulu", "dokument-vyrobniho-modulu.html")],
})

STRANKY.append({
    "slug": "kategorie-c-d.html", "nav": "kategorie", "reviewed": True,
    "title": "Kategorie C a D — nad 30 MW a připojení na 110 kV",
    "desc": "Kategorie C (30–75 MW) a D (od 75 MW nebo připojení na 110 kV a výše): plný rozsah zkoušek "
            "i simulací, u typu D až 19 testů 6.1 až 6.19 a vlastní Dokument výrobního modulu.",
    "eyebrow": "Kategorie výrobního modulu", "h1": "Kategorie C a D — nad 30 MW a 110 kV",
    "bc_nazev": "Kategorie C a D", "breadcrumb": BC_KAT,
    "intro": "<p>Nejnáročnější režim ověřování. Zkoušky na místě i simulace souladu v plném rozsahu, "
             "u typu D až devatenáct simulačních testů. Do posouzení vstupuje i provozovatel přenosové "
             "soustavy.</p>",
    "stats": [("30 – 75 MW", "Kategorie C"), ("≥ 75 MW nebo 110 kV", "Kategorie D"),
              ("6.1 – 6.19", "Katalog simulací u typu D")],
    "body": sekce(
        "Dvě cesty do kategorie D",
        karty([
            (I["blesk"], "Podle výkonu",
             "<p>Kategorie C je 30 až 75 MW, kategorie D od 75 MW. To je cesta, se kterou počítá "
             "většina lidí.</p>"),
            (I["sit"], "Podle napěťové hladiny",
             "<p>Do kategorie D spadá i výrobna připojená <b>na 110 kV a výše bez ohledu na výkon</b>. "
             "Fotovoltaika 30 MW na hladině 110 kV je tedy kategorie D, ne C. Na sítě 110 kV se "
             "zpravidla připojují výrobní moduly nad 10 MW.</p>"),
        ]) + callout(
            "Rozhoduje smlouva o připojení",
            "<p>Kategorie výrobního modulu je uvedená ve smlouvě o připojení a ta je závazná. Než "
            "podle výkonu odhadnete rozsah prací, podívejte se do smlouvy — u projektů na hranici "
            "kategorií to bývá rozdíl v milionech.</p>"),
        eyebrow="Zařazení",
    ) + sekce(
        "Co se u C a D ověřuje",
        karty([
            (I["graf"], "Až 19 simulačních testů",
             "<p>U nesynchronního typu D katalog testů <b>6.1 až 6.19</b>: frekvenční stabilita, RoCoF, "
             "LFSM-O a LFSM-U, přípustné snížení výkonu při podfrekvenci, konstantní činný výkon, "
             "profily UVRT a OVRT, rychlý poruchový proud, obnova výkonu po poruše, napěťová stabilita, "
             "podpora napětí jalovým výkonem, tlumení oscilací, umělá setrvačnost, ostrovní provoz "
             "a detekce ztráty úhlové stability.</p>"),
            (I["check"], "FSM je povinná",
             "<p>Režim frekvenční citlivosti (test 6.19) je povinná schopnost. Testy 6.13 až 6.18 se "
             "provádějí, pokud je provozovatel distribuční soustavy požaduje — což se u konkrétního "
             "projektu vždy ověřuje předem.</p>"),
            (I["dok"], "Vlastní dokumenty",
             "<p>Pro nesynchronní typ D existuje samostatný Dokument výrobního modulu (30 bodů), "
             "pro akumulaci typu D pak DVM-ZUE-D (29 bodů, platný od 1. 9. 2025).</p>"),
            (I["sipky"], "Vstupuje provozovatel přenosové soustavy",
             "<p>U typu D se posouzení neomezuje na distributora. Automatické opětovné připojení bývá "
             "u typu D zakázáno — výrobna najíždí jen na pokyn dispečinku.</p>"),
        ]),
        eyebrow="Rozsah", alt=True,
    ) + sekce(
        "Máme to za sebou",
        '<p class="lead">Dokončovaná zakázka: fotovoltaická elektrárna o výkonu přibližně 30 MW '
        'připojená na hladině 110 kV, kategorie D, distribuční území EG.D — s kompletním katalogem '
        'simulací 6.1 až 6.19. Českých firem, které mají tento rozsah odpracovaný, je málo.</p>'
        + cta("Chystáte projekt kategorie C nebo D? Rozsah simulací i požadavky distributora se "
              "u těchto výkonů řeší individuálně — ozvěte se co nejdřív, ideálně před podpisem "
              "smlouvy o připojení.", "Domluvit konzultaci"),
        eyebrow="Reference",
    ) + sekce("", ZDROJ.format(
        "PPDS, příloha 4, Tab. 1 a str. 13 · katalog simulací 6.1–6.19 (metodika pro nesynchronní typ D) "
        "· DVM-D a DVM-ZUE-D")),
    "cross": [("Simulace souladu", "simulace-souladu.html"), ("Kategorie B2", "kategorie-b2.html"),
              ("Bateriová úložiště (ZUE)", "bateriova-uloziste-zue.html"),
              ("Reference", "reference.html")],
})

STRANKY.append({
    "slug": "bateriova-uloziste-zue.html", "nav": "kategorie", "reviewed": True,
    "title": "ZUE / BESS — připojení a ověření souladu bateriového úložiště",
    "desc": "Zařízení pro ukládání elektřiny: společná metodika ověřování souladu ZUE od 1. 9. 2025, "
            "ověření v režimu dodávky i odběru, LFSM-U, vlastní hodnoty ochran a DVM-ZUE.",
    "eyebrow": "Akumulace", "h1": "Bateriová úložiště — ověření souladu ZUE",
    "claim": "Pro baterii neplatí to samé co pro fotovoltaiku.",
    "bc_nazev": "Bateriová úložiště (ZUE)", "breadcrumb": BC_KAT,
    "intro": "<p>Zařízení pro ukládání elektřiny — v předpisech <b>ZUE</b>, v katalozích "
             "<b>BESS</b> nebo <b>BSAE</b> — má od 1. 9. 2025 vlastní balík pravidel. Nejčastější "
             "dotaz, který dostáváme, zní: platí pro baterii totéž co pro fotovoltaiku? "
             "Neplatí.</p>",
    "stats": [("1. 9. 2025", "Platnost metodiky ZUE"), ("Oba režimy", "Dodávka i odběr"),
              ("29 bodů", "DVM-ZUE typu D")],
    "anchors": kotvy([("Co platí od 9/2025", "predpisy"), ("Oba provozní režimy", "rezimy"),
                      ("Dynamika a ochrany", "dynamika"), ("Časté dotazy", "faq")]),
    "body": sekce(
        "Co od 1. 9. 2025 platí",
        karty([
            (I["dok"], "Společná metodika ZUE",
             "<p>Metodika ověřování souladu zařízení pro ukládání elektřiny je společná pro "
             "<b>ČEZ Distribuce, EG.D i PREdistribuce</b> — stejně jako metodiky B1 a B2. K tomu "
             "dodatky č. 1 a 2 k připojovacím podmínkám ČEZ Distribuce (posouzení připojitelnosti "
             "a proces) a u EG.D dokument DVM-ZUE-D s 29 body.</p>"),
            (I["blesk"], "Kategorie se určuje stejně",
             "<p>Zařazení do A1 až D se u akumulace řídí <b>celkovým výkonem</b> — stejně jako "
             "u výroben. U hybridní elektrárny FVE + BESS se posuzuje výrobna jako celek.</p>"),
            (I["hodiny"], "Proces a lhůty",
             "<p>Dočasný provoz pro ověření souladu, rozhodnutí o trvalém provozu <b>do 30 dnů</b> "
             "od kompletní žádosti, dočasný provoz nejdéle <b>12 měsíců</b>. Ochrany a dálkové "
             "řízení se přezkušují <b>minimálně jednou za čtyři roky</b>.</p>"),
            (I["sit"], "Rozšířená telemetrie",
             "<p>U akumulace se přenáší i aktuální kapacita baterie a řídí se příkon ve stupních. "
             "<a href=\"rtu-dispecerske-rizeni.html\">Telemetrie a RTU →</a></p>"),
        ]),
        eyebrow="Předpisy", kotva="predpisy",
    ) + sekce(
        "Ověřuje se v obou provozních režimech",
        "<p class=\"lead\">To je hlavní rozdíl proti fotovoltaice. Požadavky se prokazují "
        "<b>v dodávce i v odběru</b>, včetně přechodů mezi nimi. Režim frekvenční citlivosti (FSM) "
        "se ověřuje v obou režimech.</p>"
        + karty([
            (I["sipky"], "Přechod při podfrekvenci",
             "<p>Při poklesu frekvence pod <b>49,0 Hz</b> se akumulace musí automaticky přepnout do "
             "dodávky — jinak se odpojí. Tohle je bod, na kterém se nejčastěji láme nastavení "
             "řídicího systému.</p>"),
            (I["graf"], "PQ diagram pro oba směry",
             "<p>Podpora napětí jalovým výkonem se u akumulace posuzuje pro <b>oba směry činného "
             "výkonu</b>. PQ diagram tedy není jednosměrný jako u výrobny.</p>"),
        ], sloupce=2),
        eyebrow="Dodávka i odběr", alt=True, kotva="rezimy",
    ) + sekce(
        "Dynamické požadavky a ochrany",
        karty([
            (I["blesk"], "LFSM-U je povinné",
             "<p>Omezená frekvenční citlivost při podfrekvenci: práh <b>49,8 Hz</b>, statika "
             "<b>5 %</b>, v režimu dodávky.</p>"),
            (I["blesk"], "Rychlý poruchový proud",
             "<p>Samostatný požadavek s gradientem <b>k = 3</b> — jen v režimu dodávky, odezva do "
             "10 ms, test při 40 % jmenovitého výkonu. S LFSM-U nijak nesouvisí, i když se to často "
             "plete do jedné věty.</p>"),
            (I["info"], "Tři různé referenční výkony",
             "<p>Detail, který v protokolech dělá největší zmatek: LFSM-O se vztahuje k <b>Pn</b>, "
             "odezva při podfrekvenci k <b>Pmax</b> a LFSM-U ke <b>skutečnému výkonu v okamžiku "
             "dosažení prahu</b>. Chybný referenční výkon je jeden z běžných důvodů, proč se "
             "simulace vrací k přepracování.</p>"),
            (I["stit"], "Jiné hodnoty ochran než u FVE",
             "<p>Nastavení ochran akumulace (například U&lt;&lt; na úrovni 0,45 Un) se nesmí "
             "mechanicky přenášet na fotovoltaiku — hodnoty se mezi ZUE a FVE liší. "
             "<a href=\"rozpadove-misto.html\">Tabulka nastavení ochran →</a></p>"),
        ]),
        eyebrow="Technika", kotva="dynamika",
    ) + sekce(
        "",
        cta("Bateriová úložiště jsou dnes nejčastější důvod, proč se ověření souladu řeší znovu "
            "u elektrárny, která už běží. <b>Napište nám výkon a kapacitu úložiště</b> a jestli jde "
            "o nový projekt nebo doplnění ke stávající FVE.")
        + ZDROJ.format(
            "Metodika ověřování souladu ZUE (typ D nesynchronní), společná ČEZ Distribuce + EG.D + "
            "PREdistribuce, platná od 1. 9. 2025 · dodatky č. 1 a 2 připojovacích podmínek ČEZ "
            "Distribuce (1. 9. 2025) · DVM-ZUE-D, 29 bodů (EG.D)"),
        alt=True,
    ),
    "faq": [
        ("Platí pro baterii stejné zkoušky jako pro fotovoltaiku?",
         "<p>Ne. Akumulace má vlastní metodiku ověřování souladu platnou od 1. 9. 2025, ověřuje se "
         "v obou provozních režimech a hodnoty ochran se od fotovoltaiky liší.</p>"),
        ("Co se stane při podfrekvenci?",
         "<p>Pod 49,0 Hz se úložiště musí automaticky přepnout do dodávky, jinak se odpojí. Ověřuje "
         "se to jako součást souladu.</p>"),
        ("Můžeme s baterií poskytovat podpůrné služby?",
         "<p>Zapojení akumulace do podpůrných služeb je možné po splnění podmínek připojení, "
         "dokončení procesu uvedení do provozu a splnění samostatných podmínek příslušného "
         "distributora, ČEPS a agregátora. Podmínky pro poskytování podpůrných služeb jsou nad "
         "rámec ověření souladu — řeší se zvlášť.</p>"),
        ("Jak často se u akumulace přezkušují ochrany?",
         "<p>Ochrany a dálkové řízení minimálně jednou za čtyři roky. Je to periodická povinnost, "
         "na kterou se po vydání konečného provozního oznámení snadno zapomene.</p>"),
    ],
    "cross": [("Přidání baterie ke stávající FVE", "pridani-baterie-k-fve.html"),
              ("Rozpadové místo a ochrany", "rozpadove-misto.html"),
              ("RTU a dispečerské řízení", "rtu-dispecerske-rizeni.html"),
              ("Kategorie C a D", "kategorie-c-d.html")],
})

STRANKY.append({
    "slug": "pridani-baterie-k-fve.html", "nav": "kategorie", "reviewed": True,
    "title": "Přidání baterie ke stávající FVE — co vás čeká",
    "desc": "Doplnění bateriového úložiště k běžící fotovoltaice: posouzení připojitelnosti, změna "
            "smlouvy o připojení, ověření souladu ZUE a rozšíření telemetrie.",
    "eyebrow": "Nejčastější dotaz", "h1": "Přidání baterie ke stávající fotovoltaice",
    "claim": "Není to jen montáž. Je to nové připojení.",
    "bc_nazev": "Přidání baterie k FVE", "breadcrumb": BC_KAT,
    "intro": "<p>Elektrárna běží roky, má konečné provozní oznámení a majitel k ní chce dostavět "
             "baterie. Technicky je to práce na jeden až dva dny. Administrativně jde o "
             "<b>změnu smlouvy o připojení</b> a o nové ověření souladu — a to je ta část, která "
             "projekty zdržuje.</p>",
    "body": sekce(
        "Čtyři věci, které je potřeba vyřešit",
        wp([
            ("1", "<b>Posouzení připojitelnosti.</b> Doplnění akumulace se posuzuje znovu — "
                  "u ČEZ Distribuce podle dodatku č. 1 připojovacích podmínek."),
            ("2", "<b>Změna smlouvy o připojení.</b> Podává se žádost o připojení zařízení pro "
                  "ukládání elektřiny; smlouva o připojení se mění."),
            ("3", "<b>Ověření souladu ZUE.</b> Vedle Dokumentu výrobního modulu se dokládá "
                  "i dokument ověřování souladu zařízení pro ukládání elektřiny — s ověřením "
                  "v režimu dodávky i odběru."),
            ("4", "<b>Rozšíření telemetrie.</b> U akumulace se přenáší i aktuální kapacita baterie "
                  "a řídí se příkon ve stupních. Signály se doplňují do tabulky telemetrie "
                  "a znovu se dělá funkční zkouška přenosu dat."),
        ]) + callout(
            "Časté nedorozumění",
            "<p>„Baterie je za střídačem, distributora to nezajímá.“ Zajímá — akumulace mění chování "
            "odběrného místa v obou směrech a má vlastní požadavky na ochrany a na dynamiku. "
            "Nastavení ochran fotovoltaiky se na úložiště přenést nedá, hodnoty se liší.</p>"),
        eyebrow="Postup",
    ) + sekce(
        "Kdy je to jednoduché a kdy ne",
        karty([
            (I["check"], "Jednodušší případ",
             "<p>Elektrárna do 100 kW (kategorie A1 nebo A2), jeden střídač s hybridním provozem "
             "a certifikátem, který akumulaci pokrývá. Vystačí papíry — instalační dokument, "
             "certifikáty, změna smlouvy.</p>"),
            (I["info"], "Náročnější případ",
             "<p>Elektrárna od 100 kW, víc střídačů, samostatný bateriový střídač bez modelu "
             "od výrobce. Přichází simulace, zkoušky na místě v obou režimech a nový dočasný "
             "provoz pro ověření.</p>"),
        ], sloupce=2)
        + cta("<b>Nevíte, do které skupiny patříte?</b> Pošlete smlouvu o připojení, jednopólové "
              "schéma a typ střídače — obratem řekneme, co doplnění baterie u vaší elektrárny "
              "obnáší."),
        eyebrow="Dva scénáře", alt=True,
    ),
    "faq": [
        ("Baterie k existující FVE — musí se znovu něco prokazovat?",
         "<p>Ano: posouzení připojitelnosti, změna smlouvy o připojení, ověření souladu zařízení pro "
         "ukládání elektřiny a rozšíření telemetrie.</p>"),
        ("Přijdu o konečné provozní oznámení?",
         "<p>Stávající provozní oznámení se váže k výrobně v původní konfiguraci. Doplněním "
         "akumulace se konfigurace mění, proto se proces uvedení do provozu pro nové zařízení "
         "opakuje v rozsahu, který stanoví distributor.</p>"),
        ("Zvládneme to bez odstávky elektrárny?",
         "<p>Samotná montáž vyžaduje krátkou odstávku. Delší dopad má fáze ověřování — v dočasném "
         "provozu se smí vyrábět, ale za podmínek stanovených distributorem.</p>"),
    ],
    "cross": [("Ověření souladu ZUE", "bateriova-uloziste-zue.html"),
              ("Rozpadové místo a ochrany", "rozpadove-misto.html"),
              ("ÚPOS — dočasný provoz", "upos.html"),
              ("Podklady k zahájení", "podklady.html")],
})

# ======================================================= DISTRIBUTORI ======
BC_PDS = [("Distributoři", "index.html#pds")]

STRANKY.append({
    "slug": "cez-distribuce.html", "nav": "pds", "reviewed": True,
    "title": "ČEZ Distribuce — připojovací podmínky, ochrany, telemetrie",
    "desc": "Připojovací podmínky vn/vvn ČEZ Distribuce od 1. 9. 2025 a přílohy VP: nastavení ochran, "
            "charakteristika Q(U), telemetrie, fyzický test omezování činného výkonu.",
    "eyebrow": "Provozovatel distribuční soustavy", "h1": "ČEZ Distribuce",
    "claim": "Průvodce podmínkami platnými od 1. 9. 2025.",
    "bc_nazev": "ČEZ Distribuce", "breadcrumb": BC_PDS,
    "intro": "<p>Metodiky ověřování souladu jsou společné pro všechny tři velké distributory — "
             "co se ověřuje, je tedy stejné jako u EG.D i PREdistribuce. Co se liší, jsou "
             "<b>připojovací podmínky, nastavení ochran, telemetrie a formuláře</b>. Tahle stránka "
             "shrnuje to, co je specifické pro ČEZ Distribuci.</p>",
    "stats": [("1. 9. 2025", "Platnost připojovacích podmínek vn/vvn"),
              ("VP_01 – VP_15", "Přílohy s technickými požadavky"),
              ("IEC 60870-5-104", "Protokol telemetrie")],
    "anchors": kotvy([("Co platí od 9/2025", "podminky"), ("Telemetrie a RTU", "telemetrie"),
                      ("Q(U) a regulace U/Q", "regulace"), ("Test omezování výkonu", "vp10")]),
    "body": sekce(
        "Co platí od 1. 9. 2025",
        karty([
            (I["dok"], "Nové připojovací podmínky",
             "<p>Připojovací podmínky pro vn a vvn platné od <b>1. 9. 2025</b> nahradily verzi z roku "
             "2023. K nim patří dodatky č. 1 a 2 pro zařízení pro ukládání elektřiny a volné přílohy "
             "<b>VP_01 až VP_15</b> — ochrany, Q(U), telemetrie, testy.</p>"),
            (I["blesk"], "Upřesnění požadavků RfG (VP_09)",
             "<p>Rychlý poruchový proud s gradientem <b>k = 3</b>. Umělou setrvačnost ČEZ Distribuce "
             "požaduje jen u kategorií C a D. Start ze tmy ani ostrovní provoz nepožaduje.</p>"),
            (I["stit"], "Ochrany rozpadového místa (VP_05)",
             "<p>Předepsané hodnoty a zpoždění pro výrobní moduly i akumulaci od 0 do 30 MW. "
             "Ochrany za rozpadovým místem se nastavují shodně s rozpadovým místem. "
             "<a href=\"rozpadove-misto.html\">Kompletní tabulka →</a></p>"),
            (I["baterie"], "Dodatky pro akumulaci",
             "<p>Dodatek č. 1 řeší posouzení připojitelnosti úložiště, dodatek č. 2 samotný proces "
             "včetně lhůty 30 dnů na rozhodnutí o trvalém provozu a periodického přezkoušení ochran "
             "jednou za čtyři roky.</p>"),
        ]),
        eyebrow="Připojovací podmínky", kotva="podminky",
    ) + sekce(
        "Telemetrie a řídicí jednotka",
        karty([
            (I["sit"], "Řídicí a komunikační jednotka (VP_06)",
             "<p>Záložní napájení <b>minimálně 8 hodin</b> po odpojení, mobilní síť <b>2G + 4G</b> "
             "(SIM kartu na nn a vn dodává distributor; na vvn se připojuje opticky nebo metalicky "
             "přes transformovnu), telemetrie protokolem <b>IEC 60870-5-104</b>, šifrování IPSec "
             "nebo podle IEC 62351-5.</p>"),
            (I["check"], "Funkční zkouška přenosu dat (VP_07)",
             "<p>Žádost o funkční zkoušku bod–bod do dispečerského řídicího systému se podává "
             "s vyplněnou tabulkou telemetrie <b>VP_02</b>. Zkouška se koordinuje s dispečinkem — "
             "termín je potřeba domluvit s předstihem.</p>"),
        ], sloupce=2),
        eyebrow="Data do dispečinku", alt=True, kotva="telemetrie",
    ) + sekce(
        "Jalový výkon: Q(U), nebo U/Q?",
        tabulka(
            ["Rezervovaný výkon", "Způsob regulace", "Poznámka"],
            [["pod 1 MW", "Q(U) — autonomní charakteristika",
              "Body 0,94 / 0,97 / 1,05 / 1,08 Un, časová konstanta 20 s, rozsah cos φ ±0,9 (VP_08)"],
             ["1 MW a více", "U/Q regulace", "Dálkové řízení napětí jalovým výkonem podle pokynů dispečinku"],
             ["od 30 MW", "vždy U/Q regulace", "Bez ohledu na další parametry"]],
            poznamky=["Platí pro vn a vvn. Rozhoduje rezervovaný výkon podle smlouvy o připojení "
                      "(VP_12, aktualizace 12/2025). U akumulace platí PQ diagram pro oba směry "
                      "činného výkonu."],
            min_sirka=760,
        ),
        eyebrow="Regulace napětí", kotva="regulace",
    ) + sekce(
        "Fyzický test omezování činného výkonu",
        "<p class=\"lead\">Zvláštnost ČEZ Distribuce, o které řada provozovatelů neví: tenhle test "
        "<b>si provádí uživatel sám</b>, bez účasti distributora — a jeho protokol je "
        "<b>povinnou přílohou žádosti o trvalý provoz</b>.</p>"
        + wp([
            ("Stupně", "0 – 30 – 60 – 100 % instalovaného výkonu."),
            ("Sekvence", "Doporučené pořadí 100 → 60 → 30 → 100 → 0 → 100 %."),
            ("Podmínky", "Start při výkonu nejméně 70 % Pi, ustálení na každém stupni minimálně "
                         "jednu minutu."),
            ("Výstup", "Protokol podle VP_11 — bez něj distributor žádost o trvalý provoz "
                       "nepřijme jako úplnou."),
        ])
        + cta("Test si můžete udělat sami — nebo přijedeme, změříme ho kvalimetrem třídy A "
              "a vystavíme protokol rovnou v podobě, kterou distributor čeká.",
              "Poptat měření"),
        eyebrow="VP_10 a VP_11", alt=True, kotva="vp10",
    ) + sekce("", ZDROJ.format(
        "Připojovací podmínky vn a vvn ČEZ Distribuce s přílohami VP_05 až VP_15, platné od "
        "1. 9. 2025 (VP_12 aktualizace 12/2025) · dodatky č. 1 a 2 pro ZUE")),
    "cross": [("Rozpadové místo a ochrany", "rozpadove-misto.html"),
              ("RTU a dispečerské řízení", "rtu-dispecerske-rizeni.html"),
              ("EG.D", "egd.html"), ("ÚTP — trvalý provoz", "utp.html")],
})

STRANKY.append({
    "slug": "egd.html", "nav": "pds", "reviewed": True,
    "title": "EG.D — dispečerské řízení DE ČE, telemetrie a formuláře",
    "desc": "EG.D: podklady DE ČE pro dispečerské řízení a chránění, stupně řízení P0 až P4, "
            "telemetrie IEC 60870-5-104, formuláře 0920-G97 a G98 a nové připojovací podmínky "
            "od 1. 2. 2026.",
    "eyebrow": "Provozovatel distribuční soustavy", "h1": "EG.D",
    "claim": "Funkční zkouška s dispečinkem bez překvapení.",
    "bc_nazev": "EG.D", "breadcrumb": BC_PDS,
    "intro": "<p>Metodiky ověřování souladu jsou společné se zbylými distributory. Specifické je "
             "u EG.D hlavně <b>dispečerské řízení a chránění decentrálních zdrojů (DE ČE)</b> "
             "a sada procesních formulářů.</p>",
    "stats": [("v05 · 1. 11. 2025", "Aktuální podklady DE ČE"),
              ("P0 – P4", "Stupně řízení činného výkonu"),
              ("1. 2. 2026", "Nové připojovací podmínky VN/VVN")],
    "anchors": kotvy([("Dispečerské řízení", "dece"), ("Řízení P a Q", "rizeni"),
                      ("Formuláře", "formulare"), ("Co je nového", "novinky")]),
    "body": sekce(
        "Dispečerské řízení a chránění (DE ČE)",
        karty([
            (I["dok"], "Dvě verze podle výkonu",
             "<p>Podklady existují ve verzi pro <b>100 až 1000 kW</b> a ve verzi <b>od 1000 kW</b>. "
             "Obě jsou ve verzi 05 s poslední aktualizací 1. 11. 2025. Přenos dat probíhá telegramem "
             "podle <b>IEC 60870-5-104</b>.</p>"),
            (I["baterie"], "Vnořená akumulace a dobíjecí stanice",
             "<p>Pro vnořené zařízení pro ukládání elektřiny, dobíjecí stanice a řízení odběru se "
             "řídí příkon ve stupních <b>IP1 až IP4</b> (0 / 25 / 50 / 100 %). Telemetrie akumulace "
             "zahrnuje i aktuální kapacitu baterie.</p>"),
            (I["graf"], "Meteorologická data",
             "<p>Distributor může požadovat teplotu, vítr a u fotovoltaiky osvit. Výrobna na to musí "
             "být připravena — realizace do <b>4 měsíců</b> od oznámení požadavku.</p>"),
            (I["check"], "Funkční zkouška s dispečinkem",
             "<p>Celý řetězec RTU → telegram 104 → zkouška s dispečerským řídicím systémem → "
             "protokol. Právě tady se předání výroben nejčastěji zastaví. "
             "<a href=\"rtu-dispecerske-rizeni.html\">Jak to řešíme →</a></p>"),
        ]),
        eyebrow="DE ČE", kotva="dece",
    ) + sekce(
        "Stupně řízení činného a jalového výkonu",
        tabulka(
            ["Veličina", "Rozsah výrobny", "Stupně a kroky"],
            [["Činný výkon P", "všechny", "P0 – P4: 0 / 0 / 30 (50) / 60 (70) / 100 % instalovaného výkonu"],
             ["Jalový výkon Q", "100 – 1000 kW", "5 diskrétních stupňů: ±0,375·Pinst, ±0,185·Pinst, 0"],
             ["Jalový výkon Q", "od 1 MW", "povely s krokem přibližně 200 kVAr"],
             ["Příkon (ZUE, dobíjení, DSR)", "všechny", "IP1 – IP4: 0 / 25 / 50 / 100 %"]],
            poznamky=["Přesné hodnoty pro konkrétní výrobnu vždy vycházejí z podkladů DE ČE ve verzi "
                      "platné v době připojení a z technických podmínek připojení."],
            min_sirka=780,
        ),
        eyebrow="Tabulka pro projektanty", alt=True, kotva="rizeni",
    ) + sekce(
        "Formuláře, které EG.D chce",
        karty([
            (I["dok"], "0920-G97",
             "<p>Povinné doklady podle <b>čl. 41.3 RfG</b> — přehled toho, co se k výrobně dokládá.</p>"),
            (I["dok"], "0920-G98",
             "<p>Rozdělení odpovědností při zkouškách a simulacích podle <b>čl. 41.4 RfG</b> — kdo "
             "za co ručí.</p>"),
        ], sloupce=2)
        + callout(
            "Formuláře se mění",
            "<p>Čísla i verze formulářů EG.D průběžně aktualizuje. U konkrétního projektu vždy "
            "stahujeme aktuální verzi z webu distributora — a hlídáme, aby se nepodalo něco "
            "v neplatné podobě.</p>"),
        eyebrow="Papíry", kotva="formulare",
    ) + sekce(
        "Nové připojovací podmínky od 1. 2. 2026",
        "<p class=\"lead\">EG.D vydala připojovací podmínky VN/VVN s platností od <b>1. 2. 2026</b>. "
        "Týkají se hlavně měřicích souprav u výroben nad 250 kW, trafostanic žadatele a regulace "
        "výroben. Ochrany a telemetrii neřeší — pro ně dál platí DE ČE a PPDS, příloha 4.</p>"
        + cta("Připravujete projekt na území EG.D? Projdeme s vámi, co z nových podmínek dopadá "
              "na vaši konfiguraci."),
        eyebrow="Novinka", alt=True, kotva="novinky",
    ) + sekce("", ZDROJ.format(
        "Podklady pro dispečerské řízení a chránění decentrálních zdrojů (DE ČE) 100–1000 kW a od "
        "1000 kW, verze 05, aktualizace 1. 11. 2025 · formuláře 0920-G97 a 0920-G98 · připojovací "
        "podmínky VN/VVN EG.D od 1. 2. 2026")),
    "cross": [("ČEZ Distribuce", "cez-distribuce.html"),
              ("RTU a dispečerské řízení", "rtu-dispecerske-rizeni.html"),
              ("Kategorie A2 — formuláře", "kategorie-a2.html"),
              ("Bateriová úložiště (ZUE)", "bateriova-uloziste-zue.html")],
})

STRANKY.append({
    "slug": "predistribuce.html", "nav": "pds", "reviewed": True,
    "title": "PREdistribuce — ověření souladu na území Prahy",
    "desc": "PREdistribuce: společný rámec RfG, PPDS příloha 4 a metodiky B1/B2, k tomu podnikové "
            "normy řady PN KA. Specifika projdeme individuálně.",
    "eyebrow": "Provozovatel distribuční soustavy", "h1": "PREdistribuce",
    "bc_nazev": "PREdistribuce", "breadcrumb": BC_PDS,
    "intro": "<p>Distribuční území Prahy a Roztok. Nadřazený rámec — RfG, PPDS příloha 4 a společné "
             "metodiky ověřování souladu B1, B2 a ZUE — je <b>shodný</b> s ČEZ Distribucí a EG.D. "
             "PREdistribuce je jejich spoluautorem.</p>",
    "body": sekce(
        "Co je stejné a co vlastní",
        karty([
            (I["check"], "Stejné: co se ověřuje",
             "<p>Metodiky B1 a B2 platné od 1. 2. 2025 i metodika ZUE od 1. 9. 2025 jsou společné. "
             "Body Tabulky 1, cesty ověření i logika Dokumentu výrobního modulu se tedy neliší.</p>"),
            (I["dok"], "Vlastní: podnikové normy",
             "<p>PREdistribuce má vlastní podnikové normy řady <b>PN KA 5xx</b>, které upřesňují "
             "technické provedení a postupy na jejím území.</p>"),
        ], sloupce=2)
        + callout(
            "Nepředstíráme detail, který nemáme",
            "<p>Pro některé konfigurace — zejména nesynchronní moduly a bateriová úložiště — si "
            "aktuální podklady PREdistribuce vyžádáme přímo u distributora na začátku projektu. "
            "Raději si o dva dny dřív zavoláme, než abychom postavili rozsah na zastaralé normě.</p>"),
        eyebrow="Rámec",
    ) + sekce(
        "",
        cta("Máte projekt na území PREdistribuce? Ozvěte se — postup projdeme individuálně "
            "a rozsah potvrdíme proti aktuálním podkladům distributora."),
        alt=True,
    ) + sekce("", ZDROJ.format(
        "Společné metodiky ověřování souladu B1, B2 a ZUE (PREdistribuce je spoluautorem) · "
        "podnikové normy řady PN KA")),
    "cross": [("ČEZ Distribuce", "cez-distribuce.html"), ("EG.D", "egd.html"),
              ("Kategorie B1", "kategorie-b1.html"), ("Kontakt", "kontakt.html")],
})

# =========================================================== SLUZBY =======
BC_SLU = [("Služby", "index.html#sluzby")]

STRANKY.append({
    "slug": "simulace-souladu.html", "nav": "sluzby", "reviewed": True,
    "title": "Simulace souladu výrobny — DIgSILENT PowerFactory",
    "desc": "Simulace souladu: dynamický model výrobny v DIgSILENT PowerFactory, katalog testů podle "
            "metodiky PDS, report s verdiktem splněno/nesplněno a předání modelu distributorovi.",
    "eyebrow": "Služba · část A", "h1": "Simulace souladu",
    "claim": "Digitální dvojče výrobny — a report, který distributor přijme.",
    "bc_nazev": "Simulace souladu", "breadcrumb": BC_SLU,
    "intro": "<p>„Digitální dvojče“ zní marketingově, tak rovnou konkrétně: jde o "
             "<b>validovaný dynamický model vaší výrobny</b>, na kterém se prokáží požadavky, které "
             "se na hotové elektrárně změřit nedají — překlenutí poruch, rychlé změny frekvence, "
             "frekvenční odezva. Model se počítá v prostředí <b>DIgSILENT PowerFactory</b>.</p>",
    "stats": [("100 kW – 36 MWp", "Rozsah zpracovaných studií"),
              ("10 ms / 200 ms", "Rozlišení záznamů RMS"),
              ("Splněno / nesplněno", "Verdikt u každého bodu")],
    "body": sekce(
        "Co model obsahuje",
        wp([
            ("1", "Ekvivalent distribuční soustavy v místě připojení."),
            ("2", "Blokový transformátor."),
            ("3", "Trafostanice a kabelové rozvody vn i nn."),
            ("4", "Ochrany a rozpadová místa s reálným nastavením."),
            ("5", "Dynamické modely všech střídačů — u bateriových systémů i model PCS."),
        ]) + callout(
            "Model musí odpovídat skutečnosti",
            "<p>Nejčastější důvod, proč distributor simulace vrací: model neodpovídá skutečné "
            "konfiguraci výrobny. Proto začínáme auditem vstupů a topologii si necháváme potvrdit "
            "dřív, než se spustí první test. Druhý nejčastější důvod je chybně zvolený referenční "
            "výkon u frekvenčních testů.</p>"),
        eyebrow="Rozsah",
    ) + sekce(
        "Jak studie probíhá",
        wp([
            ("WP1", "Audit vstupů — projektová dokumentace, smlouva o připojení a technické podmínky, "
                    "datové listy, projednání rozsahu s distributorem."),
            ("WP2", "Model výrobny — topologie, agregace střídačů, bateriové úložiště, ochrany "
                    "a rozpadová místa."),
            ("WP3", "Statické výpočty — chod sítě, zkraty podle IEC 60909, PQ diagram a návrh "
                    "kompenzace."),
            ("WP4", "Dynamické RMS simulace — frekvence a RoCoF, LFSM-O a LFSM-U, UVRT a OVRT, "
                    "poruchový proud, Q(U)."),
            ("WP5", "Protokol a Dokument výrobního modulu, u akumulace i dokument ověřování souladu; "
                    "předání ověřeného modelu distributorovi."),
            ("WP6", "Vypořádání připomínek distributora a finální schválení."),
        ]),
        eyebrow="Postup", alt=True,
    ) + sekce(
        "Katalog testů podle kategorie",
        "<p class=\"lead\">Rozsah není libovolný — vychází z metodiky pro danou kategorii. "
        "U nesynchronního typu D jde až o devatenáct testů 6.1 až 6.19:</p>"
        + seznam([
            "Frekvenční stabilita a RoCoF (±2 Hz/s)",
            "LFSM-O — omezení výkonu při nadfrekvenci od 50,2 Hz, statika 5 %",
            "LFSM-U — zvýšení výkonu při podfrekvenci od 49,8 Hz",
            "Přípustné snížení činného výkonu při podfrekvenci",
            "Konstantní činný výkon",
            "Překlenutí poruchy — profily UVRT a OVRT",
            "Rychlý poruchový proud",
            "Obnova činného výkonu po poruše",
            "Napěťová stabilita a podpora napětí jalovým výkonem",
            "Tlumení oscilací",
            "Umělá setrvačnost (u kategorií C a D)",
            "Ostrovní provoz a detekce ztráty úhlové stability",
            "Režim frekvenční citlivosti FSM — povinná schopnost",
        ])
        + callout(
            "Ne všechno se dělá vždy",
            "<p>Testy 6.13 až 6.18 se provádějí, pokud je provozovatel distribuční soustavy "
            "požaduje; FSM (6.19) je povinná. U kategorie B1 jde jen o vybrané body, u B2 je celá "
            "kapitola simulací povinná. <b>Rozsah proto potvrzujeme proti metodice a smlouvě "
            "o připojení, ne odhadem.</b></p>"),
        eyebrow="Co se počítá",
    ) + sekce(
        "",
        cta("Chcete vědět, co bude vaše studie obsahovat? Pošlete smlouvu o připojení, jednopólové "
            "schéma a typy střídačů — vrátíme se s rozsahem a s tím, které body půjde doložit "
            "certifikátem.", "Poptat simulační studii")
        + ZDROJ.format("Katalog simulací 6.1–6.19 (metodika pro nesynchronní typ D; parametry se "
                       "podle kategorie liší) · metodiky ověřování souladu B1 a B2"),
        alt=True,
    ),
    "cross": [("Zkoušky na místě", "zkousky-na-miste.html"), ("Kategorie B2", "kategorie-b2.html"),
              ("Dokument výrobního modulu", "dokument-vyrobniho-modulu.html"),
              ("Podklady k zahájení", "podklady.html")],
})

STRANKY.append({
    "slug": "zkousky-na-miste.html", "nav": "sluzby", "reviewed": True,
    "title": "Zkoušky na místě — funkční zkoušky a měření třídy A",
    "desc": "Funkční zkoušky výrobny na místě: řízení výkonu, opětovné připojení, regulace U/Q/cos φ, "
            "ochrany, omezování P. Kvalimetr třídy A podle ČSN EN 61000-4-30, protokoly do DVM.",
    "eyebrow": "Služba · část B", "h1": "Zkoušky na místě instalace",
    "claim": "Jeden výjezd, všechny protokoly.",
    "bc_nazev": "Zkoušky na místě", "breadcrumb": BC_SLU,
    "intro": "<p>Funkční zkoušky se provádějí <b>na výrobnu jako celek</b> a začínají už u kategorie "
             "B1 — ne až od 1 MW. Přijedeme s měřicí technikou, zkoordinujeme dispečink, ochranáře "
             "i servis střídačů a odjedeme se sadou protokolů, které jdou rovnou do Dokumentu "
             "výrobního modulu.</p>",
    "stats": [("Třída A", "Kvalimetr dle ČSN EN 61000-4-30"),
              ("≥ 3 kHz", "Vzorkování záznamu"),
              ("5.1 – 5.11", "Katalog zkoušek")],
    "body": sekce(
        "Co se na místě zkouší",
        seznam([
            "Regulace činného výkonu — setpoint a gradient 10 % za minutu",
            "Automatické opětovné připojení po poruše",
            "Komunikace s dispečinkem (zkoušku provádí distributor)",
            "Regulace napětí, jalového výkonu a účiníku (U / Q / cos φ)",
            "Desetiminutová přepěťová ochrana",
            "Ostatní ochrany rozpadového místa",
            "Omezování činného výkonu ve stupních 0 / 30 / 60 / 100 %",
            "Start ze tmy a rychlé přifázování — jen na žádost distributora",
            "Zařízení pro záznam poruch",
            "Dodatečný jalový výkon",
        ]),
        eyebrow="Katalog 5.1 až 5.11",
    ) + sekce(
        "Čím měříme",
        karty([
            (I["lupa"], "Kvalimetr třídy A",
             "<p>Analyzátor kvality elektřiny podle <b>ČSN EN 61000-4-30, třída A</b>, se záznamem "
             "10 ms i 200 ms RMS a vzorkováním nejméně 3 kHz — přesně jak žádá metodika.</p>"),
            (I["stit"], "Přesnost pro ochrany",
             "<p>Pro ověření ochran je požadována přesnost <b>0,1 % Un</b> u napětí a <b>0,01 % fn</b> "
             "u frekvence. Sekundární tester ochran vezeme s sebou.</p>"),
            (I["check"], "Bez generátorové soupravy",
             "<p>Vybrané body nesynchronní kategorie B1 jde provést bez vlastního zdroje napětí "
             "a frekvence — nemusí se tedy na stavbu vozit generátor.</p>"),
            (I["hodiny"], "Koordinace termínu",
             "<p>Termín zkoušky s dispečinkem se sjednává s předstihem, zpravidla zhruba osm týdnů. "
             "U fotovoltaiky navíc rozhoduje počasí — zkouška opětovného připojení potřebuje "
             "alespoň 50 % jmenovitého výkonu ze slunce, takže v zimě se termín hledá hůř.</p>"),
        ]),
        eyebrow="Vybavení", alt=True,
    ) + sekce(
        "Průběh výjezdu",
        wp([
            ("Z1", "Program zkoušek a koordinace termínu s distributorem i s dodavateli technologie."),
            ("Z2", "Zkoušky síťových ochran všech rozpadových míst — desetiminutová nadpěťová ochrana "
                   "a stupně U&gt;, U&lt;, f&gt;, f&lt;."),
            ("Z3", "Provozní zkoušky — řízení činného výkonu, automatické opětovné připojení, "
                   "regulace U, Q a cos φ, omezování výkonu."),
            ("Z4", "Ověření zařízení pro záznam poruch a koordinace zkoušky komunikace s dispečinkem."),
            ("Z5", "Protokoly, zápis do Dokumentu výrobního modulu a kompletace podkladů k žádosti "
                   "o trvalý provoz."),
        ]) + callout(
            "Hybridní výrobny FVE + BESS",
            "<p>U elektráren s bateriovým úložištěm přibývají provozní zkoušky akumulace "
            "<b>v obou režimech — dodávka i odběr</b> — včetně místního zadání přes RTU. Počítejte "
            "s delším dnem na výrobně.</p>"),
        eyebrow="Postup",
    ) + sekce(
        "",
        cta("Potřebujete zkoušky u elektrárny, kterou stavěl někdo jiný? Běžná věc — potřebujeme "
            "jen podklady, ne vlastní stavbu.", "Domluvit termín")
        + ZDROJ.format("Katalog zkoušek 5.1–5.11 · metodiky ověřování souladu B1 a B2, kap. 3 "
                       "(požadavky na vybavení)"),
        alt=True,
    ),
    "cross": [("Zkoušky ochran", "zkousky-ochran.html"), ("Simulace souladu", "simulace-souladu.html"),
              ("Kategorie B1", "kategorie-b1.html"),
              ("ČEZ Distribuce — test omezování P", "cez-distribuce.html")],
})

STRANKY.append({
    "slug": "zkousky-ochran.html", "nav": "sluzby", "reviewed": True,
    "title": "Zkoušky ochran a protokol o nastavení ochran",
    "desc": "Funkční zkouška síťových ochran rozpadového místa, sekundární zkouška zkušebními "
            "přístroji a protokol o nastavení ochran — povinná příloha žádosti o dočasný provoz.",
    "eyebrow": "Služba", "h1": "Zkoušky ochran",
    "claim": "Protokol, bez kterého se žádost o ÚPOS nehne.",
    "bc_nazev": "Zkoušky ochran", "breadcrumb": BC_SLU,
    "intro": "<p><b>Protokol o nastavení ochran je povinnou položkou žádosti o dočasný provoz</b> "
             "(bod f) seznamu podkladů podle PPDS, přílohy 4). Bez něj distributor žádost nepovažuje "
             "za úplnou a třicetidenní lhůta na rozhodnutí nezačne běžet.</p>",
    "body": sekce(
        "Dva způsoby, jak ochrany ověřit",
        karty([
            (I["blesk"], "Za skutečných podmínek",
             "<p>Zkouška při reálném ději na výrobně — třífázový výpadek, opětovné zapnutí, "
             "odchylky frekvence. Ověřuje se náběh i vypínací čas.</p>"),
            (I["lupa"], "Sekundární zkouška",
             "<p>Simulace zkušebními přístroji, kdy se do ochrany pouští definované napětí "
             "a frekvence. Rychlejší a opakovatelná — používá se, kde skutečné podmínky vyvolat "
             "nelze.</p>"),
        ], sloupce=2)
        + callout(
            "Certifikát ochranu nezastoupí",
            "<p>Certifikát síťové ochrany nepokrývá body označené jako „jen zkouška“. "
            "<b>Nastavení se vždy ověřuje na místě</b> — bez ohledu na to, jaké doklady k ochraně "
            "má výrobce.</p>", warn=True),
        eyebrow="Metodika",
    ) + sekce(
        "Co dodáme",
        seznam([
            "Návrh nastavení ochran podle podmínek příslušného distributora",
            "Funkční zkoušku ochran všech rozpadových míst",
            "Ověření náběhů a vypínacích časů",
            "Protokol o nastavení ochran do žádosti o dočasný provoz",
            "Export nastavení a zápis do Dokumentu výrobního modulu",
            "Periodické přezkoušení u akumulace — minimálně jednou za čtyři roky",
        ])
        + callout(
            "Hodnoty se liší podle distributora i podle zařízení",
            "<p>ČEZ Distribuce předepisuje nastavení ochran rozpadového místa v příloze VP_05, "
            "EG.D vychází z podkladů DE ČE a PPDS, přílohy 4. Navíc platí, že hodnoty pro "
            "<b>bateriové úložiště nejsou stejné jako pro fotovoltaiku</b> — mechanické přenesení "
            "nastavení je jedna z nejčastějších chyb. "
            "<a href=\"rozpadove-misto.html\">Tabulka hodnot podle VP_05 →</a></p>"),
        eyebrow="Výstup", alt=True,
    ) + sekce("", cta("Máte přenastavené ochrany po výměně střídače nebo doplnění baterie? "
                      "Ozvěte se — projdeme, co je potřeba znovu doložit.")),
    "cross": [("Rozpadové místo a ochrany", "rozpadove-misto.html"),
              ("Zkoušky na místě", "zkousky-na-miste.html"), ("ÚPOS — dočasný provoz", "upos.html"),
              ("Podklady k zahájení", "podklady.html")],
})

STRANKY.append({
    "slug": "rtu-dispecerske-rizeni.html", "nav": "sluzby", "reviewed": True,
    "title": "RTU, telemetrie a dispečerské řízení výrobny",
    "desc": "Telemetrie IEC 60870-5-104, řídicí a komunikační jednotka, audit signálů proti tabulce "
            "telemetrie a funkční zkouška přenosu dat s dispečinkem — pro ČEZ Distribuce i EG.D.",
    "eyebrow": "Služba", "h1": "RTU, telemetrie a dispečerské řízení",
    "claim": "Nejčastější důvod, proč hotová elektrárna nejde předat.",
    "bc_nazev": "RTU a dispečerské řízení", "breadcrumb": BC_SLU,
    "intro": "<p>Elektrárna je hotová, revize podepsané — a předání stojí na tom, že do dispečinku "
             "nechodí data. Tahle situace se opakuje u velké části projektů, protože telemetrie se "
             "typicky řeší až na konci, když už na ni není čas.</p>",
    "stats": [("IEC 60870-5-104", "Protokol přenosu"), ("8 h", "Záloha řídicí jednotky (ČEZd)"),
              ("2G + 4G", "Mobilní připojení (ČEZd)")],
    "body": sekce(
        "Co je společné oběma distributorům",
        karty([
            (I["sit"], "Protokol IEC 60870-5-104",
             "<p>Telemetrie i povely jdou tímto protokolem. Rozsah signálů se liší podle "
             "distributora a podle velikosti výrobny.</p>"),
            (I["graf"], "Řízení činného výkonu ve stupních",
             "<p>ČEZ Distribuce 0 / 30 / 60 / 100 %, EG.D stupně P0 až P4. U akumulace k tomu "
             "přibývá řízení příkonu a přenos aktuální kapacity baterie.</p>"),
            (I["blesk"], "Řízení jalového výkonu",
             "<p>Podle rezervovaného výkonu buď autonomní charakteristika Q(U), nebo dálková "
             "regulace U/Q podle pokynů dispečinku.</p>"),
            (I["check"], "Funkční zkouška přenosu dat",
             "<p>Bez zkoušky bod–bod do dispečerského řídicího systému se výrobna nepředá. "
             "Koordinuje se s dispečinkem a je potřeba ji naplánovat dopředu.</p>"),
        ]),
        eyebrow="Základ",
    ) + sekce(
        "Co nabízíme",
        wp([
            ("1", "<b>Audit signálů</b> — porovnáme, co RTU skutečně posílá, proti tabulce telemetrie "
                  "distributora (u ČEZ Distribuce příloha VP_02, u EG.D rozsah podle DE ČE)."),
            ("2", "<b>Doplnění RTU a řídicí jednotky</b> — u ČEZ Distribuce podle VP_06: záložní "
                  "napájení nejméně 8 hodin, mobilní síť 2G + 4G, šifrování IPSec nebo dle "
                  "IEC 62351-5."),
            ("3", "<b>Nastavení a odladění přenosu</b> — mapování signálů, stupně řízení výkonu, "
                  "u akumulace i příkon a kapacita baterie."),
            ("4", "<b>Funkční zkouška s dispečinkem</b> a protokol, který jde přiložit k žádosti."),
        ])
        + cta("Stojí vám předání na telemetrii? Napište, jaké RTU máte a kdo je distributor — "
              "audit signálů zvládneme na dálku.", "Poptat audit signálů"),
        eyebrow="Služba", alt=True,
    ) + sekce(
        "Rozdíly mezi distributory",
        tabulka(
            ["", "ČEZ Distribuce", "EG.D"],
            [["Rozsah signálů", "tabulka telemetrie VP_02", "podklady DE ČE podle velikosti výrobny"],
             ["Řídicí jednotka", "VP_06 — 8 h záloha, 2G + 4G, IPSec / IEC 62351-5",
              "podle DE ČE, verze 05 (1. 11. 2025)"],
             ["Řízení činného výkonu", "stupně 0 / 30 / 60 / 100 %", "stupně P0 – P4"],
             ["Meteodata", "podle podmínek připojení",
              "teplota, vítr, u FVE osvit — realizace do 4 měsíců od požadavku"],
             ["Zkouška přenosu", "žádost přes digitální komunikační kanál (VP_07)",
              "funkční zkouška s dispečerským řídicím systémem"]],
            min_sirka=820,
        ),
        eyebrow="Přehled",
    ),
    "cross": [("ČEZ Distribuce", "cez-distribuce.html"), ("EG.D", "egd.html"),
              ("Bateriová úložiště (ZUE)", "bateriova-uloziste-zue.html"),
              ("ÚTP — trvalý provoz", "utp.html")],
})

STRANKY.append({
    "slug": "podklady.html", "nav": "sluzby", "reviewed": True,
    "title": "Podklady k žádosti o dočasný provoz — checklist a) až j)",
    "desc": "Co provozovatel distribuční soustavy chce k žádosti o dočasný provoz: projektová "
            "dokumentace, jednopólové schéma, revize, protokol o nastavení ochran, MPP, harmonogram "
            "zkoušek a certifikáty.",
    "eyebrow": "Co potřebujeme od vás", "h1": "Podklady k zahájení",
    "claim": "Pečlivé podklady zkracují celý proces o týdny.",
    "bc_nazev": "Podklady k zahájení", "breadcrumb": BC_SLU,
    "intro": "<p>PPDS, příloha 4 předepisuje k žádosti o dočasný provoz pro ověření souladu body "
             "a) až j). Zní to úředně, ve skutečnosti jde o věci, které na stavbě většinou "
             "existují — jen nejsou pohromadě. Tady je ten samý seznam v lidské řeči, i s tím, co "
             "z něj umíme dodat my.</p>",
    "body": sekce(
        "Seznam podkladů podle PPDS, přílohy 4",
        tabulka(
            ["", "Doklad podle předpisu", "Lidsky — co po vás chceme"],
            [["a", "Projektová dokumentace odsouhlasená distributorem, aktualizovaná podle skutečného "
                   "provedení", "finální dokumentaci „as-built“"],
             ["b", "Jednopólové schéma výrobny, odběrného místa a výrobního modulu",
              "jednopólové schéma, pokud není součástí dokumentace"],
             ["c", "Potvrzení odborné firmy o souladu se smlouvou o připojení, povolením a PPDS",
              "potvrzení zhotovitele — šablonu dodáme"],
             ["d", "Výchozí revize elektrického zařízení pro připojení k distribuční soustavě",
              "revizi přípojky"],
             ["e", "Výchozí revize elektrického zařízení výrobny", "revizi výrobny"],
             ["f", "Protokol o nastavení ochran",
              'protokol od ochranáře — <a href="zkousky-ochran.html">umíme zajistit</a>'],
             ["g", "Protokoly o úředním ověření měřicích transformátorů proudu a napětí",
              "kalibrační listy měřicích transformátorů"],
             ["h", "Místní provozní předpisy", "MPP — umíme zpracovat"],
             ["i", "Harmonogram a rozsah zkoušek a simulací",
              "zpracujeme my — určuje i délku dočasného provozu"],
             ["j", "Seznam certifikátů od certifikátora", "certifikáty střídačů a dalšího zařízení"]],
            poznamky=["Žádost o uvedení do trvalého provozu zrcadlí body a) až h) a přidává "
                      "Dokument výrobního modulu a instalační dokument. U ČEZ Distribuce je "
                      "povinnou přílohou i protokol fyzického testu omezování činného výkonu."],
            min_sirka=820,
        ),
        eyebrow="Body a) až j)",
    ) + sekce(
        "Co potřebujeme navíc pro simulace a zkoušky",
        seznam([
            "Smlouvu o připojení včetně všech dodatků a technických podmínek",
            "Jednopólové schéma s rozpadovými místy a délkami kabelů",
            "Projektovou dokumentaci skutečného provedení",
            "Tabulku telemetrie odsouhlasenou distributorem",
            "Datové listy technologie — střídače, transformátory, baterie",
            "Matematický model střídačů nebo bateriového PCS od výrobce",
            "Protokoly o nastavení ochran a exporty nastavení",
            "Kontakt na technika řídicího systému nebo RTU pro součinnost při zkouškách",
        ])
        + callout(
            "Model PCS objednejte co nejdřív",
            "<p>U bateriových systémů bývá dodání matematického modelu od výrobce nejdelší položkou "
            "celého projektu — klidně několik týdnů. Vyžádejte si ho hned na začátku, ne až když "
            "začne běžet dočasný provoz.</p>"),
        eyebrow="Pro naši práci", alt=True,
    ) + sekce(
        "",
        cta("<b>Nevíte, co z toho máte a co chybí?</b> Projdeme to s vámi po telefonu — obvykle "
            "je za deset minut jasno, co je potřeba dohledat.", "Zavolat nám", "kontakt.html")
        + ZDROJ.format("PPDS, příloha 4, kap. 12.1 (str. 68–70) a kap. 12.3"),
    ),
    "cross": [("ÚPOS — dočasný provoz", "upos.html"), ("ÚTP — trvalý provoz", "utp.html"),
              ("Zkoušky ochran", "zkousky-ochran.html"),
              ("Dokument výrobního modulu", "dokument-vyrobniho-modulu.html")],
})

# ============================================================ PROCES ======
BC_PROC = [("Proces", "proces-pripojeni.html")]

STRANKY.append({
    "slug": "proces-pripojeni.html", "nav": "proces", "reviewed": True,
    "title": "Proces připojení výrobny — kroky a lhůty",
    "desc": "Časová osa připojení výrobny do distribuční soustavy: smlouva o připojení, žádost "
            "o dočasný provoz, zkoušky a simulace, Dokument výrobního modulu, trvalý provoz "
            "a konečné provozní oznámení — včetně lhůt.",
    "eyebrow": "Časová osa", "h1": "Proces připojení výrobny",
    "claim": "Pět kroků a lhůty, které je dobré znát předem.",
    "bc_nazev": "Proces připojení", "breadcrumb": [],
    "intro": "<p>Ověření souladu není poslední razítko, ale samostatná fáze mezi dostavbou "
             "a trvalým provozem. Kdo o ní ví od začátku, ušetří měsíce — kdo se o ní dozví "
             "měsíc před koncem dočasného provozu, obvykle žádá o prodloužení.</p>",
    "body": sekce(
        "Pět kroků",
        kroky([
            ("Smlouva o připojení a projekt",
             "Smlouva určí kategorii výrobního modulu, rezervovaný výkon a podmínky. K projektové "
             "dokumentaci se distributor vyjadřuje do 30 dnů.", "30 dnů na vyjádření"),
            ("Žádost o dočasný provoz (ÚPOS)",
             "Kompletní dossier podle PPDS, přílohy 4, kap. 12.1, body a) až j). Distributor "
             "rozhodne do 30 dnů od úplné žádosti a vydá Dočasné provozní oznámení.",
             "30 dnů od úplné žádosti"),
            ("Zkoušky a simulace",
             "Dočasný provoz trvá nejdéle 12 měsíců podle předloženého harmonogramu. U každého bodu "
             "Tabulky 1 se doloží zkouška, simulace, nebo certifikát.", "nejdéle 12 měsíců"),
            ("Protokoly a Dokument výrobního modulu",
             "Každé ověření znamená protokol s průběhy veličin a verdiktem splněno/nesplněno. "
             "Vyplněný DVM to shrnuje do jednoho dokumentu.", "naše práce"),
            ("Trvalý provoz a KPO",
             "Žádost o uvedení do trvalého provozu. Zkoušky řádně provedené v rámci dočasného "
             "provozu distributor neopakuje. Konečné provozní oznámení platí do odpojení výrobny.",
             "cíl procesu"),
        ]),
        eyebrow="Od smlouvy ke konečnému provoznímu oznámení",
    ) + sekce(
        "Lhůty, které zákazníka zajímají",
        tabulka(
            ["Úkon", "Lhůta", "Zdroj"],
            [["Vyjádření distributora k projektové dokumentaci", "30 dnů", "PPDS, příloha 4"],
             ["Rozhodnutí o žádosti o dočasný provoz (od úplné žádosti)", "do 30 dnů",
              "PPDS, příloha 4, kap. 12.1"],
             ["Platnost Dočasného provozního oznámení",
              "<b>nejdéle 12 měsíců</b> podle harmonogramu zkoušek",
              "PPDS, příloha 4 · dodatek č. 2 ČEZ Distribuce"],
             ["Prodloužení při překážce nezávislé na vůli výrobce",
              "o nezbytně nutnou dobu — oznámit bez odkladu", "PPDS, příloha 4"],
             ["Oznámení přerušení nebo ukončení dočasného provozu",
              "na místě, nebo písemně do 15 pracovních dnů", "PPDS, příloha 4 · metodiky B1 a B2"],
             ["Rozhodnutí o trvalém provozu u akumulace", "do 30 dnů od kompletní žádosti",
              "dodatek č. 2 ČEZ Distribuce"],
             ["Periodické přezkoušení ochran a dálkového řízení (akumulace)",
              "minimálně 1× za 4 roky", "dodatek č. 2 ČEZ Distribuce"]],
            min_sirka=820,
        )
        + callout(
            "12 měsíců, ne 24",
            "<p>V oběhu se drží údaj 24 měsíců — ten se ale vztahuje k jinému institutu evropského "
            "nařízení. <b>Dočasný provoz pro ověření souladu platí nejdéle 12 měsíců</b> a konkrétní "
            "dobu stanoví distributor podle harmonogramu zkoušek, který mu předložíte.</p>", warn=True),
        eyebrow="Tabulka lhůt", alt=True,
    ) + sekce(
        "Kdy se do toho pustit",
        "<p class=\"lead\">Ideálně ve chvíli, kdy máte podepsanou smlouvu o připojení — tedy dřív, "
        "než se začne stavět. Důvody jsou tři:</p>"
        + karty([
            (I["graf"], "Simulace ovlivní nastavení",
             "<p>Ze simulací vyjde, jak se mají nastavit střídače a ochrany. Je levnější to vědět "
             "před uvedením do provozu než po prvním neúspěšném pokusu.</p>"),
            (I["hodiny"], "Termíny se nedají zrychlit",
             "<p>Zkouška s dispečinkem se domlouvá s předstihem a model PCS od výrobce baterií "
             "chodí týdny. Ani jedno se nedá dohnat ve zbývajícím měsíci.</p>"),
            (I["blesk"], "Fotovoltaika potřebuje slunce",
             "<p>Zkouška opětovného připojení vyžaduje dostatečný osvit. Kdo skončí stavbu v listopadu, "
             "může na vhodné počasí čekat do jara — a dočasný provoz mezitím běží.</p>"),
        ], sloupce=3)
        + cta("Chcete si projít harmonogram na konkrétním projektu? Ozvěte se s termínem dokončení "
              "stavby a s kategorií ze smlouvy o připojení."),
        eyebrow="Načasování",
    ),
    "cross": [("ÚPOS — dočasný provoz", "upos.html"), ("ÚTP — trvalý provoz", "utp.html"),
              ("Podklady k zahájení", "podklady.html"), ("Slovník pojmů RfG", "slovnik-rfg.html")],
})

STRANKY.append({
    "slug": "upos.html", "nav": "proces", "reviewed": True,
    "title": "ÚPOS — dočasný provoz pro ověření souladu",
    "desc": "Co je ÚPOS a Dočasné provozní oznámení, jak se podává žádost, jak dlouho dočasný provoz "
            "platí (12 měsíců), kdy jde prodloužit a kdy jej distributor přeruší.",
    "eyebrow": "Proces", "h1": "ÚPOS — dočasný provoz pro ověření souladu",
    "claim": "Fáze, ve které se smí vyrábět jen kvůli zkouškám.",
    "bc_nazev": "ÚPOS", "breadcrumb": BC_PROC,
    "intro": "<p>U ČEZ Distribuce se tomu oficiálně říká <b>souhlas s dočasným provozem pro ověření "
             "souladu</b>, jinde <b>umožnění provozu pro ověření souladu</b>. Zkratka je stejná: "
             "ÚPOS. Je to fáze, ve které výrobna smí běžet — ale jen proto, aby se na ní daly "
             "provést zkoušky a doložit soulad.</p>",
    "stats": [("30 dnů", "Rozhodnutí od úplné žádosti"),
              ("12 měsíců", "Nejdelší platnost dočasného provozu")],
    "body": sekce(
        "ÚPOS a DPO — jak to spolu souvisí",
        karty([
            (I["dok"], "ÚPOS je souhlas",
             "<p>Podáte žádost s podklady a) až j). Distributor ji posoudí a <b>do 30 dnů od úplné "
             "žádosti</b> rozhodne.</p>"),
            (I["check"], "DPO je výsledek",
             "<p>Schválením vzniká <b>Dočasné provozní oznámení</b> — dokument, kterým se dočasný "
             "provoz řídí. Platí nejdéle 12 měsíců a konkrétní dobu určí distributor podle "
             "harmonogramu zkoušek, který jste předložili.</p>"),
        ], sloupce=2),
        eyebrow="Dva pojmy, jeden proces",
    ) + sekce(
        "Prodloužení a přerušení",
        karty([
            (I["hodiny"], "Prodloužení lze — za podmínek",
             "<p>Nastane-li překážka nezávislá na vůli výrobce, distributor prodlouží dobu "
             "dočasného provozu o nezbytně nutnou dobu. Překážku je nutné <b>bez odkladu oznámit, "
             "prokázat a o prodloužení požádat</b> — ne až po vypršení.</p>"),
            (I["info"], "Přerušení při závadách",
             "<p>Distributor může dočasný provoz přerušit nebo ukončit, pokud se zjistí závady — "
             "typicky špatně nastavené výrobní jednotky či ochrany nebo nefunkční automatické "
             "opětovné připojení. Oznamuje to na místě, nebo písemně do 15 pracovních dnů.</p>"),
        ], sloupce=2)
        + callout(
            "„ÚPOS nám za tři měsíce končí a zkoušky nikde“",
            "<p>Nejčastější tísňové volání, které dostáváme. Postup je vždycky stejný: sestavíme "
            "reálný harmonogram zbývajících úkonů, určíme, co musí proběhnout jako první "
            "(zpravidla simulace a nastavení ochran), rezervujeme termín s dispečinkem a paralelně "
            "připravíme žádost o prodloužení. <b>Čím dřív zavoláte, tím víc cest ještě zůstává "
            "otevřených.</b></p>"),
        eyebrow="Když se to nestíhá", alt=True,
    ) + sekce(
        "",
        cta("Blíží se vám konec dočasného provozu? Napište datum z Dočasného provozního oznámení "
            "a kategorii výrobny — ozveme se do dvou pracovních dnů.", "Řešit termín")
        + ZDROJ.format("PPDS, příloha 4, kap. 12.1 (str. 68–70) · metodiky ověřování souladu B1 "
                       "a B2 · dodatek č. 2 ČEZ Distribuce"),
    ),
    "faq": [
        ("Jak dlouho DPO platí?",
         "<p>Nejdéle 12 měsíců, podle harmonogramu zkoušek. Při překážce mimo vaši vůli lze požádat "
         "o prodloužení o nezbytně nutnou dobu.</p>"),
        ("Co když to nestihneme?",
         "<p>Bez prodloužení hrozí konec dočasného provozu. Harmonogram je proto potřeba řešit co "
         "nejdřív — ne měsíc před koncem.</p>"),
        ("Můžeme v dočasném provozu vyrábět a prodávat?",
         "<p>Dočasný provoz je určen k ověření souladu a probíhá za podmínek stanovených "
         "distributorem v Dočasném provozním oznámení. Obchodní podmínky výroby v této fázi je "
         "potřeba ověřit u distributora a u obchodníka — nejsou součástí metodiky ověřování "
         "souladu.</p>"),
    ],
    "cross": [("Podklady k žádosti", "podklady.html"), ("ÚTP — trvalý provoz", "utp.html"),
              ("Proces připojení", "proces-pripojeni.html"), ("Kategorie B1", "kategorie-b1.html")],
})

STRANKY.append({
    "slug": "utp.html", "nav": "proces", "reviewed": True,
    "title": "ÚTP — trvalý provoz a konečné provozní oznámení",
    "desc": "Žádost o uvedení do trvalého provozu: jaké přílohy distributor chce, co už neopakuje "
            "a co je konečné provozní oznámení (KPO).",
    "eyebrow": "Proces", "h1": "ÚTP — uvedení do trvalého provozu",
    "claim": "Poslední krok, na kterém se nejčastěji zadrhne papírování.",
    "bc_nazev": "ÚTP", "breadcrumb": BC_PROC,
    "intro": "<p>Cíl celého procesu. Po dokončení zkoušek a simulací se podává žádost o uvedení do "
             "trvalého provozu a distributor vydá <b>konečné provozní oznámení</b>, které platí "
             "do odpojení výrobny.</p>",
    "body": sekce(
        "Co žádost obsahuje",
        karty([
            (I["dok"], "Zrcadlí žádost o dočasný provoz",
             "<p>Dokumentace odpovídá bodům a) až h) žádosti o ÚPOS a navíc přibývá "
             "<b>i) Dokument výrobního modulu</b> a <b>j) instalační dokument</b>.</p>"),
            (I["check"], "Zkoušky se neopakují",
             "<p>Zkoušky řádně provedené v rámci dočasného provozu distributor neopakuje — ledaže "
             "se změnily okolnosti (jiná konfigurace, jiné nastavení).</p>"),
            (I["blesk"], "U ČEZ Distribuce navíc",
             "<p>Povinnou přílohou je <b>protokol fyzického testu omezování činného výkonu</b> "
             "podle VP_11. Test si provádí uživatel sám. "
             "<a href=\"cez-distribuce.html#vp10\">Jak na něj →</a></p>"),
            (I["hodiny"], "Lhůta u akumulace",
             "<p>U zařízení pro ukládání elektřiny rozhodne distributor <b>do 30 dnů</b> od "
             "kompletní žádosti.</p>"),
            (I["info"], "U kategorií A1 a A2",
             "<p>Žádost se podává rovnou po splnění podmínek smlouvy o připojení — bez fáze "
             "dočasného provozu, protože se nic nezkouší.</p>"),
            (I["stit"], "Po vydání KPO",
             "<p>U akumulace nezapomeňte na periodické přezkoušení ochran a dálkového řízení "
             "minimálně jednou za čtyři roky.</p>"),
        ]),
        eyebrow="Přílohy",
    ) + sekce(
        "",
        cta("Kompletujeme podklady, podáváme žádost, vypořádáváme připomínky a dotahujeme proces "
            "až do vydání konečného provozního oznámení. <b>Nemusíte s distributorem jednat "
            "sami.</b>", "Předat nám papírování")
        + ZDROJ.format("PPDS, příloha 4, kap. 12.3 (str. 70–72) · dodatek č. 2 ČEZ Distribuce · VP_11"),
        alt=True,
    ),
    "cross": [("ÚPOS — dočasný provoz", "upos.html"), ("Podklady k zahájení", "podklady.html"),
              ("Dokument výrobního modulu", "dokument-vyrobniho-modulu.html"),
              ("ČEZ Distribuce", "cez-distribuce.html")],
})

STRANKY.append({
    "slug": "dokument-vyrobniho-modulu.html", "nav": "proces", "reviewed": True,
    "title": "Dokument výrobního modulu (DVM) — jak ho vyplnit",
    "desc": "Dokument výrobního modulu: Tabulka 1 požadavků, cesta ověření u každého bodu, počty bodů "
            "pro B1, B2, typ D a akumulaci, nejčastější chyby při vyplňování.",
    "eyebrow": "Proces", "h1": "Dokument výrobního modulu",
    "claim": "Formulář, kolem kterého se točí celá agenda.",
    "bc_nazev": "Dokument výrobního modulu", "breadcrumb": BC_PROC,
    "intro": "<p>DVM je formulář provozovatele distribuční soustavy s <b>Tabulkou 1 požadavků</b>. "
             "U každého požadavku je předepsaná cesta ověření — zkouška, simulace, nebo certifikát — "
             "a odkaz na kapitolu metodiky. Vyplněný DVM je hlavní výstup celého ověřování souladu "
             "a příloha žádosti o trvalý provoz.</p>",
    "body": sekce(
        "Kolik bodů má který dokument",
        tabulka(
            ["Kategorie", "Dokument", "Počet bodů"],
            [["A1 a A2", "Instalační dokument výrobního modulu", "místo DVM, platný od 1. 1. 2025"],
             ["B1", "DVM B1", "16 synchronní / 18 nesynchronní"],
             ["B2", "DVM B2", "24 synchronní / 27 nesynchronní"],
             ["D (nesynchronní)", "DVM-D", "30"],
             ["Akumulace typu D", "DVM-ZUE-D", "29 (od 1. 9. 2025)"]],
            poznamky=["Dokumenty výrobního modulu pro B1 a B2 byly zveřejněny 1. 12. 2024, metodiky "
                      "k nim platí od 1. 2. 2025."],
            min_sirka=680,
        ),
        eyebrow="Přehled",
    ) + sekce(
        "Tři pravidla, o která se láme rozsah prací",
        karty([
            (I["stit"], "Body „jen zkouška“ nejde nahradit",
             "<p>Tam, kde Tabulka 1 předepisuje výhradně zkoušku, nepomůže ani sebelepší simulace, "
             "ani certifikát. U kategorie B1 je takových bodů šest.</p>"),
            (I["dok"], "Certifikát jen u jedné výrobní jednotky",
             "<p>Certifikátem lze doložit požadavek pouze u výrobny složené z <b>jediné výrobní "
             "jednotky</b>. Dva a víc střídačů znamená, že se příslušné body řeší simulací.</p>"),
            (I["sit"], "Body označené (s)",
             "<p>Ověřují se na <b>výrobnu jako celek</b>, ne na jednotlivé zařízení. Nedají se "
             "„poskládat“ z dokladů k jednotlivým komponentám.</p>"),
        ], sloupce=3)
        + callout(
            "Kde se v DVM nejčastěji chybuje",
            "<p><b>Chybějící certifikát na komponentu</b> — doklad je na střídač, ale ne na ochranu "
            "nebo na transformátor. <b>Chybný referenční výkon</b> u frekvenčních testů: LFSM-O se "
            "vztahuje k jinému výkonu než LFSM-U. <b>Neúplné protokoly</b> bez průběhů veličin. "
            "Všechny tři vedou k vrácení dokumentace a ke ztrátě týdnů z dočasného provozu.</p>"),
        eyebrow="Pravidla", alt=True,
    ) + sekce(
        "Kde formulář vzít",
        "<p class=\"lead\">Formuláře vydávají provozovatelé distribučních soustav a průběžně je "
        "aktualizují. <b>Nenabízíme ke stažení vlastní „vzor DVM“</b> — stáhli byste si tím riziko, "
        "že vyplníte neplatnou verzi. U konkrétního projektu vždy pracujeme s aktuálním dokumentem "
        "příslušného distributora.</p>"
        + cta("<b>Vyplníme DVM za vás</b> — jako součást ověření souladu, včetně protokolů "
              "a vypořádání připomínek distributora.", "Poptat ověření souladu"),
        eyebrow="Poctivá odpověď",
    ) + sekce("", ZDROJ.format(
        "Dokumenty výrobního modulu B1 a B2 (zveřejněny 1. 12. 2024) · DVM-D · DVM-ZUE-D "
        "(od 1. 9. 2025) · instalační dokumenty VM A1 a A2 (od 1. 1. 2025)")),
    "cross": [("Kategorie B1", "kategorie-b1.html"), ("Kategorie B2", "kategorie-b2.html"),
              ("Simulace souladu", "simulace-souladu.html"), ("ÚTP — trvalý provoz", "utp.html")],
})

STRANKY.append({
    "slug": "rozpadove-misto.html", "nav": "proces", "reviewed": True,
    "title": "Rozpadové místo a nastavení ochran (VP_05)",
    "desc": "Nastavení ochran rozpadového místa podle VP_05 ČEZ Distribuce: hodnoty U>>>, U>>, U>, "
            "U<, U<<, f> a f< se zpožděním, a jak se funkční zkouška ochran provádí.",
    "eyebrow": "Proces", "h1": "Rozpadové místo a nastavení ochran",
    "claim": "Tabulka, kterou hledá každý ochranář.",
    "bc_nazev": "Rozpadové místo", "breadcrumb": BC_PROC,
    "intro": "<p>Rozpadové místo je místo, kde síťová ochrana odpojí výrobní modul od distribuční "
             "soustavy při poruše. Jeho nastavení předepisuje provozovatel distribuční soustavy — "
             "u ČEZ Distribuce příloha <b>VP_05</b> připojovacích podmínek.</p>",
    "body": sekce(
        "Nastavení ochran podle VP_05 (ČEZ Distribuce)",
        tabulka(
            ["Ochrana", "Nastavení", "Zpoždění", "Poznámka"],
            [["U&gt;&gt;&gt;", "1,20 × Un", "0,1 s",
              "třístupňová nadpěťová ochrana je povinná u nových a rekonstruovaných zařízení"],
             ["U&gt;&gt;", "1,15 × Un", "5 s", "bez U&gt;&gt;&gt; se nastaví 1,15 Un / 0,1 s"],
             ["U&gt;", "1,11 × Un", "0 s",
              "desetiminutový průměr („desetiminutová ochrana“ střídačů), alternativně 60 s"],
             ["U&lt;", "0,70 × Un", "2,7 s / 0,5 s", "nesynchronní / synchronní výrobní modul"],
             ["U&lt;&lt;", "0,45 × Un (vn a nn) · 0,30 × Un (vvn)", "0,2 s", ""],
             ["f&gt;", "51,5 Hz", "0,1 s", ""],
             ["f&lt;", "47,5 Hz", "0,1 s", ""]],
            poznamky=[
                "Hodnoty platí pro výrobní moduly a akumulaci od 0 do 30 MW podle VP_05 ČEZ "
                "Distribuce (platnost od 1. 9. 2025). Ochrany za rozpadovým místem se nastavují "
                "shodně s rozpadovým místem; od 30 MW se nastavení řeší individuálně.",
                "<b>Pro EG.D a PREdistribuci tato tabulka neplatí</b> — vycházejte z PPDS, přílohy 4 "
                "a z podkladů DE ČE. Hodnoty pro bateriová úložiště se navíc od fotovoltaiky liší "
                "a nesmí se mechanicky přenášet.",
            ],
            min_sirka=860,
        ),
        eyebrow="Tabulka hodnot",
    ) + sekce(
        "Jak se ochrany ověřují",
        karty([
            (I["blesk"], "Za skutečných podmínek",
             "<p>Zkouška při reálném ději — třífázový výpadek sítě, opětovné zapnutí, odchylky "
             "frekvence.</p>"),
            (I["lupa"], "Sekundární zkouška",
             "<p>Simulace zkušebními přístroji. Ověřuje se <b>náběh i vypínací čas</b>, ne jen "
             "nastavená hodnota.</p>"),
        ], sloupce=2)
        + callout(
            "Nastavení bez zkoušky neplatí",
            "<p>Že je v ochraně nastavená správná hodnota, samo o sobě nestačí. Metodika žádá "
            "funkční zkoušku a protokol o nastavení ochran — a ten je povinnou položkou žádosti "
            "o dočasný provoz. <a href=\"zkousky-ochran.html\">Zkoušky ochran →</a></p>"),
        eyebrow="Metodika", alt=True,
    ) + sekce("", ZDROJ.format(
        "VP_05 ČEZ Distribuce (platnost od 1. 9. 2025) · PPDS, příloha 4, kap. 12.2")),
    "cross": [("Zkoušky ochran", "zkousky-ochran.html"), ("ČEZ Distribuce", "cez-distribuce.html"),
              ("Bateriová úložiště (ZUE)", "bateriova-uloziste-zue.html"),
              ("Slovník pojmů RfG", "slovnik-rfg.html")],
})


def slovnik(polozky):
    kusy = [f"      <div>\n        <dt>{t}</dt>\n        <dd>{d}</dd>\n      </div>" for t, d in polozky]
    return '    <dl class="glossary">\n' + "\n".join(kusy) + "\n    </dl>"


STRANKY.append({
    "slug": "slovnik-rfg.html", "nav": "proces", "reviewed": True,
    "title": "Slovník pojmů RfG — ÚPOS, DVM, LFSM, FRT a další",
    "desc": "Vysvětlení zkratek kolem ověřování souladu výroben: RfG, PPDS příloha 4, ÚPOS, DPO, ÚTP, "
            "DVM, FRT, UVRT, LFSM-O a LFSM-U, FSM, RoCoF, Q(U), ZUE a další.",
    "eyebrow": "Referenční přehled", "h1": "Slovník pojmů RfG",
    "bc_nazev": "Slovník pojmů", "breadcrumb": BC_PROC,
    "intro": "<p>Zkratky, které v této agendě potkáte v každém dokumentu. Každé heslo má kotvu, "
             "takže na něj jde odkázat přímo — třeba <a href=\"#upos\">#upos</a>.</p>",
    "body": sekce(
        "Předpisy a dokumenty",
        slovnik([
            ('<span id="rfg">RfG</span>',
             "Nařízení Komise (EU) 2016/631, „Requirements for Generators“. Evropská pravidla pro "
             "připojování výroben k elektrizační soustavě. V Česku jsou provedena přes PPDS, přílohu 4."),
            ('<span id="ppds">PPDS, příloha 4</span>',
             "Pravidla provozování distribučních soustav, příloha 4 — pravidla pro paralelní provoz "
             "výroben a akumulačních zařízení se sítí provozovatele distribuční soustavy (únor 2022). "
             "Základní český předpis celé agendy."),
            ('<span id="sop">SoP</span><small>smlouva o připojení</small>',
             "Určuje kategorii výrobního modulu, rezervovaný výkon a podmínky připojení. Bez platné "
             "smlouvy o připojení nelze připojit nic — a je to i dokument, ve kterém se kategorie "
             "hledá."),
            ('<span id="dvm">DVM</span><small>Dokument výrobního modulu</small>',
             "Formulář s Tabulkou 1 požadavků; u každého bodu je předepsaná cesta ověření — zkouška, "
             "simulace, nebo certifikát. Varianty: B1, B2, DVM-D a DVM-ZUE-D. "
             '<a href="dokument-vyrobniho-modulu.html">Detail →</a>'),
            ('<span id="instalacni-dokument">Instalační dokument</span>',
             "Obdoba DVM pro kategorie A1 a A2, platná od 1. 1. 2025. Soulad se prokazuje certifikáty "
             "— bez zkoušek na výrobně a bez simulací."),
            ('<span id="certifikat">Certifikát zařízení</span>',
             "Osvědčení o souladu vydané akreditovaným zkušebním pracovištěm podle nařízení (ES) "
             "č. 765/2008. Nahradí zkoušku nebo "
             "simulaci jen tam, kde to Tabulka 1 připouští, a jen u výrobny z jedné výrobní jednotky."),
        ]),
        eyebrow="Co je co",
    ) + sekce(
        "Proces",
        slovnik([
            ('<span id="upos">ÚPOS</span>',
             "Souhlas s dočasným provozem pro ověření souladu (jinde „umožnění provozu pro ověření "
             "souladu“). Fáze, ve které se smí vyrábět jen kvůli zkouškám a simulacím. "
             '<a href="upos.html">Detail →</a>'),
            ('<span id="dpo">DPO</span><small>Dočasné provozní oznámení</small>',
             "Vydá provozovatel distribuční soustavy po schválení žádosti o ÚPOS. Platí nejdéle "
             "12 měsíců podle harmonogramu zkoušek."),
            ('<span id="utp">ÚTP / KPO</span>',
             "Uvedení do trvalého provozu a konečné provozní oznámení — cíl celého procesu. KPO "
             "platí do odpojení výrobny. <a href=\"utp.html\">Detail →</a>"),
            ('<span id="ve-vm-vj">VE / VM / VJ</span>',
             "Výrobna elektřiny (celý areál) → výrobní modul (jednotka prokazování souladu, jedno "
             "rozpadové místo) → výrobní jednotka (konkrétní střídač nebo generátor)."),
            ('<span id="kategorie">Kategorie výrobního modulu</span>',
             "A1, A2, B1, B2, C, D — podle výkonu a napěťové hladiny. Dělení A1/A2 a B1/B2 je české "
             "upřesnění, v RfG není. Kategorie je dána ve smlouvě o připojení."),
            ('<span id="rozpadove-misto">Rozpadové místo</span>',
             "Místo, kde síťová ochrana odpojí výrobní modul od distribuční soustavy při poruše. "
             'Nastavení předepisuje distributor. <a href="rozpadove-misto.html">Tabulka hodnot →</a>'),
        ]),
        eyebrow="Fáze a pojmy", alt=True,
    ) + sekce(
        "Technické požadavky",
        slovnik([
            ('<span id="frt">FRT / UVRT / OVRT</span>',
             "Fault Ride Through — schopnost výrobny „přežít“ krátký pokles (UVRT) nebo zvýšení "
             "(OVRT) napětí bez odpojení."),
            ('<span id="lfsm">LFSM-O / LFSM-U</span>',
             "Omezená frekvenční citlivost: automatické snížení činného výkonu při nadfrekvenci "
             "(od 50,2 Hz) a zvýšení při podfrekvenci (od 49,8 Hz), statika 5 %."),
            ('<span id="fsm">FSM</span><small>Frequency Sensitive Mode</small>',
             "Plná frekvenční odezva činného výkonu v pásmu ±200 mHz. U kategorií C a D povinná "
             "schopnost, ověřuje se simulací."),
            ('<span id="rocof">RoCoF</span>',
             "Rate of Change of Frequency — odolnost proti rychlosti změny frekvence (±2 Hz/s)."),
            ('<span id="qu">Q(U) a U/Q regulace</span>',
             "Q(U) je autonomní řízení jalového výkonu podle napětí (charakteristika s mrtvým "
             "pásmem). U/Q je dálková regulace napětí jalovým výkonem podle pokynů dispečinku. "
             "Který režim platí, se u ČEZ Distribuce odvíjí od rezervovaného výkonu."),
            ('<span id="statika">Statika</span>',
             "Poměr relativní změny frekvence k relativní změně činného výkonu. U LFSM se pracuje "
             "se statikou 5 %."),
            ('<span id="pref">Pref</span><small>referenční výkon</small>',
             "Výkon, ke kterému se vztahuje odezva při frekvenčních testech. Pozor: pro LFSM-O, pro "
             "odezvu při podfrekvenci a pro LFSM-U u akumulace to nejsou tytéž hodnoty — chybný "
             "referenční výkon je běžný důvod, proč se simulace vrací."),
            ('<span id="pq">PQ diagram</span>',
             "Zobrazení dovolené kombinace činného a jalového výkonu. U akumulace platí pro oba "
             "směry činného výkonu."),
            ('<span id="kvalimetr">Kvalimetr třídy A</span>',
             "Analyzátor kvality elektřiny podle ČSN EN 61000-4-30, třída A — povinné vybavení "
             "zkoušek: záznam 10 ms i 200 ms RMS, vzorkování nejméně 3 kHz."),
        ]),
        eyebrow="Zkratky z metodik",
    ) + sekce(
        "Provoz a komunikace",
        slovnik([
            ('<span id="zue">ZUE / BSAE / BESS</span>',
             "Zařízení pro ukládání elektřiny (termín předpisů) = bateriový systém akumulace = "
             "battery energy storage system. Tři názvy pro totéž. "
             '<a href="bateriova-uloziste-zue.html">Detail →</a>'),
            ('<span id="dece">DE ČE</span>',
             "Podklady EG.D pro dispečerské řízení a chránění decentrálních zdrojů. Popisují rozsah "
             "signálů, stupně řízení výkonu a telemetrii. <a href=\"egd.html\">Detail →</a>"),
            ('<span id="drs">DŘS</span><small>dispečerský řídicí systém</small>',
             "Systém dispečinku distributora, do kterého výrobna posílá telemetrii a od kterého "
             "přijímá povely. Přenos probíhá protokolem IEC 60870-5-104."),
            ('<span id="opm">OPM</span><small>odběrné a předávací místo</small>',
             "Místo, kde se předává elektřina mezi distribuční soustavou a zákazníkem — v němž je "
             "osazeno fakturační měření."),
            ('<span id="tps">TPS</span><small>transformovna / předávací stanice</small>',
             "Uzel, přes který se výrobna připojuje na vyšší napěťovou hladinu; na vvn se přes něj "
             "vede i komunikace do dispečinku."),
        ]),
        eyebrow="Zkratky z provozu", alt=True,
    ),
    "cross": [("Proces připojení", "proces-pripojeni.html"), ("Kategorie výroben", "index.html#kategorie"),
              ("Časté dotazy", "faq.html")],
})

# ====================================================== FAQ / REFERENCE ===
STRANKY.append({
    "slug": "faq.html", "nav": "", "reviewed": True,
    "title": "Časté dotazy k ověření souladu výroben",
    "desc": "Osmnáct nejčastějších dotazů k simulačním zkouškám a ověření souladu s RfG: kategorie, "
            "ÚPOS, DVM, certifikáty, ochrany, baterie a co dělat, když se to nestíhá.",
    "eyebrow": "Ptáte se", "h1": "Časté dotazy",
    "bc_nazev": "Časté dotazy", "breadcrumb": [],
    "intro": "<p>Otázky, které dostáváme od investorů, projektantů i montážních firem. Odpovědi "
             "vycházejí z platných metodik — u konkrétního projektu vždy ověřujeme aktuální verzi "
             "dokumentů příslušného distributora.</p>",
    "body": "",
    "faq_nadpis": "Osmnáct otázek a odpovědí",
    "faq": [
        ("Co jsou „simulační zkoušky“?",
         "<p>Souhrnné označení pro ověření souladu výrobny s RfG: <b>simulace souladu</b> (matematický "
         "model výrobny) a <b>zkoušky na místě</b> (měření na hotové elektrárně).</p>"),
        ("Koho se to týká?",
         "<p>Každé výrobny a každého zařízení pro ukládání elektřiny připojeného paralelně "
         "s distribuční soustavou. Rozsah určuje kategorie výrobního modulu uvedená ve smlouvě "
         "o připojení.</p>"),
        ("Jak zjistím kategorii své výrobny?",
         "<p>Je uvedena ve smlouvě o připojení. Orientačně ji poznáte podle výkonu — "
         "<a href=\"index.html#kategorie\">tabulka kategorií</a>. U fotovoltaiky s baterií se "
         "posuzuje celkový výkon výrobny.</p>"),
        ("Co je ÚPOS a DPO?",
         "<p>ÚPOS je souhlas s dočasným provozem pro ověření souladu, DPO je Dočasné provozní "
         "oznámení, kterým jej distributor potvrdí. <a href=\"upos.html\">Detail →</a></p>"),
        ("Jak dlouho dočasné provozní oznámení platí?",
         "<p>Nejdéle <b>12 měsíců</b>, podle harmonogramu zkoušek. Při překážce nezávislé na vaší "
         "vůli lze požádat o prodloužení o nezbytně nutnou dobu.</p>"),
        ("Co když to nestihneme?",
         "<p>Bez prodloužení hrozí konec dočasného provozu. Harmonogram je proto potřeba řešit co "
         "nejdřív — ne měsíc před koncem. Ozvěte se, sestavíme reálný plán zbývajících úkonů.</p>"),
        ("Co je Dokument výrobního modulu?",
         "<p>Formulář distributora s tabulkou všech požadavků a cestou jejich ověření. Jeho vyplnění "
         "je jádro celé agendy. <a href=\"dokument-vyrobniho-modulu.html\">Detail →</a></p>"),
        ("Kdy stačí certifikát a nemusí se nic měřit?",
         "<p>Jen u bodů, kde to Tabulka 1 připouští, a jen u výrobny složené z jedné výrobní "
         "jednotky. Body označené „jen zkouška“ certifikát nenahradí nikdy.</p>"),
        ("Platí ještě protokoly laboratoří?",
         "<p>Ano, přechodně. Protokol odborné laboratoře (ČEZ Distribuce, EG.D) nahrazuje u A1 a A2 "
         "certifikát, pokud byl <b>vydaný do 31. 12. 2025</b>; distributoři ho akceptují <b>do "
         "31. 12. 2026</b>. Od 1. 1. 2027 už jen osvědčení o souladu od akreditovaného zkušebního "
         "pracoviště podle nařízení (ES) č. 765/2008, nebo výjimka ERÚ.</p>"),
        ("Musí k nám u kategorie B1 někdo fyzicky přijet?",
         "<p>Ano, na šest funkčních zkoušek: řízení činného výkonu, automatické opětovné připojení, "
         "komunikace s dispečinkem, regulace U/Q/cos φ, nastavení ochran a omezování výkonu. Zbytek "
         "lze doložit od stolu.</p>"),
        ("Co je rozpadové místo?",
         "<p>Místo, kde síťová ochrana odpojí výrobnu od sítě při poruše. Jeho nastavení předepisuje "
         "distributor. <a href=\"rozpadove-misto.html\">Detail →</a></p>"),
        ("Jaké hodnoty ochran ČEZ Distribuce vyžaduje?",
         "<p>Podle přílohy VP_05 — například U&gt;&gt;&gt; na 1,2 Un se zpožděním 0,1 s nebo f&lt; "
         "na 47,5 Hz se zpožděním 0,1 s. <a href=\"rozpadove-misto.html\">Celá tabulka →</a></p>"),
        ("Co se změnilo pro baterie od 1. 9. 2025?",
         "<p>Platí nová společná metodika ověřování souladu ZUE: ověřuje se v obou provozních "
         "režimech, povinné je LFSM-U a akumulace má vlastní dokument ověřování souladu. "
         "<a href=\"bateriova-uloziste-zue.html\">Detail →</a></p>"),
        ("Chci přidat baterii k FVE — co mě čeká?",
         "<p>Posouzení připojitelnosti, změna smlouvy o připojení, ověření souladu zařízení pro "
         "ukládání elektřiny a rozšíření telemetrie. "
         "<a href=\"pridani-baterie-k-fve.html\">Detail →</a></p>"),
        ("Proč distributor vrací simulace k přepracování?",
         "<p>Nejčastěji proto, že model neodpovídá skutečné konfiguraci výrobny, je chybně zvolený "
         "referenční výkon u frekvenčních testů, nebo jsou protokoly neúplné.</p>"),
        ("Co budete potřebovat od nás?",
         "<p>Podklady a) až j) k žádosti o dočasný provoz plus technické podklady pro model. "
         "<a href=\"podklady.html\">Kompletní checklist →</a></p>"),
        ("Kolik to stojí?",
         "<p>Cena se odvíjí od kategorie výrobního modulu, počtu a typu střídačů a od toho, kolik "
         "bodů půjde doložit certifikátem místo simulace. Proto ji neuvádíme paušálně — pošlete "
         "smlouvu o připojení a jednopólové schéma a dostanete konkrétní nabídku.</p>"),
        ("Děláte to i pro elektrárny, které jste nestavěli?",
         "<p>Ano, tvoří to velkou část naší práce. Studie zpracováváme pro jiné dodavatele "
         "fotovoltaiky i pro investory, kteří si stavbu zajistili sami.</p>"),
    ],
    "cross": [("Slovník pojmů RfG", "slovnik-rfg.html"), ("Proces připojení", "proces-pripojeni.html"),
              ("Podklady k zahájení", "podklady.html"), ("Kontakt", "kontakt.html")],
})

STRANKY.append({
    "slug": "reference.html", "nav": "reference",
    "title": "Reference — ověření souladu od 100 kW do 36 MWp",
    "desc": "Vybrané projekty ověření souladu: fotovoltaika ~30 MW na 110 kV kategorie D, FVE 698 kWp "
            "kategorie B1 a hybridní výrobna FVE s bateriovým úložištěm.",
    "eyebrow": "Co máme za sebou", "h1": "Reference",
    "claim": "Projekty uvádíme anonymizovaně — na přání investorů.",
    "bc_nazev": "Reference", "breadcrumb": [],
    "intro": "<p>U ověřování souladu si většina investorů nepřeje být jmenována, proto uvádíme "
             "projekty bez názvů — s parametry, které o rozsahu práce vypovídají víc než logo.</p>",
    "stats": [("100 kW – 36 MWp", "Rozsah zpracovaných studií"),
              ("Desítky", "Protokolů ověření souladu"),
              ("3 hlavní PDS", "ČEZ Distribuce · EG.D · PREdistribuce")],
    "body": sekce(
        "Vybrané projekty",
        karty([
            (I["tovarna"], "FVE ~30 MW, 110 kV — kategorie D",
             "<p><b>Distributor:</b> EG.D<br><b>Předmět:</b> kompletní simulace souladu 6.1 až 6.19, "
             "model výrobny, dokumentace<br><b>Stav:</b> ve fázi ověřování souladu</p>"
             "<p>Nejnáročnější kategorie, jakou lze v distribuční soustavě potkat — připojení na "
             "hladině 110 kV a plný rozsah simulací podle Tabulky 1, tedy body 6.1 až 6.19 "
             "včetně tlumení výkonových oscilací a robustnosti.</p>"),
            (I["blesk"], "FVE 698 kWp (Pn 550 kW) — kategorie B1",
             "<p><b>Distributor:</b> ČEZ Distribuce<br><b>Předmět:</b> zkoušky na místě včetně "
             "fyzického testu omezování činného výkonu, protokoly, DVM</p>"
             "<p>Typický projekt kategorie B1: šest funkčních zkoušek v jednom výjezdu, zbytek "
             "doložený od stolu.</p>"),
            (I["baterie"], "FVE 60 kWp + bateriové úložiště",
             "<p><b>Distributor:</b> EG.D<br><b>Předmět:</b> etapizace fotovoltaiky a následné "
             "doplnění akumulace</p>"
             "<p>Ukázka toho, jak se doplnění baterie promítne do smlouvy o připojení "
             "a do ověřování souladu.</p>"),
        ], sloupce=3),
        eyebrow="Anonymizovaně",
    ) + sekce(
        "Kdo to dělá",
        "<p class=\"lead\">Ověřování souladu zajišťuje <b>BFK Systems s.r.o.</b> Se sesterskou "
        "společností <a href=\"https://www.bftechnology.cz/\" target=\"_blank\" rel=\"noopener\">BF "
        "technology</a> tvoříme jednu skupinu — stejné vedení, stejné sídlo i telefon. BF technology "
        "staví fotovoltaické elektrárny, BFK Systems dělá inženýrskou část: projekty, simulace, "
        "zkoušky a jednání s provozovateli distribučních soustav. Zkušenosti máme z projektů pro "
        "energetiku, petrochemii i automobilový průmysl.</p>"
        + cta("Chcete referenci na konkrétní typ projektu? Řekněte si o ni — po dohodě "
              "s investorem ji rádi doložíme podrobněji.", "Ozvat se"),
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
      <p>Ozveme se do dvou pracovních dnů. Pokud máte po ruce smlouvu o připojení a jednopólové schéma, přiložte je rovnou — ušetří to jedno kolečko otázek.</p>
      <div class="quick">
        <a href="tel:+420776111100">
          <span class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72c.12.9.35 1.79.68 2.64a2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.44-1.25a2 2 0 0 1 2.11-.45c.85.33 1.74.56 2.64.68A2 2 0 0 1 22 16.92z"/></svg></span>
          +420 776 111 100
        </a>
        <a href="mailto:info@bfksystems.cz">
          <span class="ico"><svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"><rect x="2" y="4" width="20" height="16" rx="2"/><path d="m22 7-10 6L2 7"/></svg></span>
          info@bfksystems.cz
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

    <div class="contact-form-card">
      <div id="contact-status" role="status"></div>
      <!-- Odesila se pres fetch(), pole "redirect" je zalozni cesta bez JavaScriptu. -->
      <form class="contact-form" id="contact-form" action="https://api.web3forms.com/submit" method="post" autocomplete="on">
        <input type="hidden" name="access_key" value="PLACEHOLDER-DOPLNIT-KLIC-WEB3FORMS">
        <input type="hidden" name="subject" value="Nová poptávka z webu simulacni-zkousky.cz">
        <input type="hidden" name="from_name" value="Poptávkový formulář simulacni-zkousky.cz">
        <input type="hidden" name="replyto" value="">
        <input type="hidden" name="redirect" value="https://www.simulacni-zkousky.cz/kontakt.html?sent=1#poptavka">
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
              <option value="">— vyberte —</option>
              <option>ČEZ Distribuce</option>
              <option>EG.D</option>
              <option>PREdistribuce</option>
              <option>Nevím</option>
            </select>
          </div>
          <div class="field">
            <label for="f-kat">Kategorie ze smlouvy o připojení</label>
            <select id="f-kat" name="Kategorie">
              <option value="">— vyberte —</option>
              <option>A1 (do 11 kW)</option>
              <option>A2 (11 – 100 kW)</option>
              <option>B1 (100 kW – 1 MW)</option>
              <option>B2 (1 – 30 MW)</option>
              <option>C nebo D (nad 30 MW / 110 kV)</option>
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
              <option value="">— vyberte —</option>
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
              <option value="Zkoušky ochran">Zkoušky ochran a protokol o nastavení</option>
              <option value="RTU a telemetrie">RTU, telemetrii a dispečerské řízení</option>
              <option value="Vyřízení UPOS / UTP">Vyřízení žádostí o ÚPOS a ÚTP</option>
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
    "title": "Kontakt — ověření souladu výroben s RfG",
    "desc": "BFK Systems s.r.o., Obchodní 455/12, Děčín. Poptávka na simulace souladu, zkoušky na "
            "místě a vyřízení dokumentace k dočasnému i trvalému provozu.",
    "eyebrow": "Kontakt", "h1": "Ozvěte se",
    "bc_nazev": "Kontakt", "breadcrumb": [],
    "intro": "<p>Nejrychlejší cesta k odpovědi vede přes smlouvu o připojení — je v ní kategorie "
             "výrobního modulu i rezervovaný výkon, tedy dvě věci, ze kterých se odvíjí celý rozsah "
             "ověření. Přiložte ji rovnou k poptávce.</p>",
    "body": sekce(
        "Kontaktní údaje",
        karty([
            (I["dok"], "BFK Systems s.r.o.",
             "<p>Obchodní 455/12<br>Děčín V-Rozbělesy, 405 02 Děčín</p>"
             "<p>IČO 23571853<br>DIČ CZ23571853</p>"),
            (I["sit"], "Spojení",
             '<p><a href="tel:+420776111100">+420 776 111 100</a><br>'
             '<a href="mailto:info@bfksystems.cz">info@bfksystems.cz</a><br>'
             '<a href="https://www.bfksystems.cz/" target="_blank" rel="noopener">www.bfksystems.cz</a></p>'),
        ], sloupce=2)
        + callout(
            "Co nám poslat s poptávkou",
            "<p>Smlouvu o připojení (nebo alespoň kategorii a rezervovaný výkon), jednopólové "
            "schéma, počet a typ střídačů a informaci, jestli je součástí bateriové úložiště. "
            "Z toho se dá odhadnout rozsah i to, které body půjde doložit certifikátem. "
            "<a href=\"podklady.html\">Kompletní seznam podkladů →</a></p>"),
        eyebrow="Kde nás najdete",
    ) + sekce(
        "Kdo se vám ozve",
        karty([
            (I["lupa"], "Bc. Petr Fencl",
             "<p><b>Technický ředitel</b></p><p>Specialista na průmyslovou automatizaci, "
             "fotovoltaiku a integrace MES/ERP. Zkušenosti z projektů pro ČEZ a ČEPS.</p>"),
            (I["dok"], "PhDr. Jan Böhme",
             "<p><b>Obchodní a finanční ředitel</b></p><p>Nabídky, smlouvy a jednání s investory. "
             "Praxe z managementu, ekonomie a financí.</p>"),
            (I["blesk"], "Michal Kovář",
             "<p><b>Specialista VN a řízení FVE</b></p><p>Vysoké napětí, průmyslové řízení "
             "a aplikace SCADA. Desítky projektů v Evropě i zámoří.</p>"),
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
             ["E-mail", '<a href="mailto:info@bfksystems.cz">info@bfksystems.cz</a>'],
             ["Web", '<a href="https://www.bfksystems.cz/" target="_blank" rel="noopener">www.bfksystems.cz</a>']],
            min_sirka=520,
        ),
        eyebrow="Údaje",
    ),
    "cross": [("Podklady k zahájení", "podklady.html"), ("Časté dotazy", "faq.html"),
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
      <p>Kontakt ve věcech ochrany osobních údajů: <a href="mailto:info@bfksystems.cz">info@bfksystems.cz</a>,
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
          <td>Plnění zákonných povinností — účetnictví a daně</td>
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
      Načítá webové fonty z externí služby; při jejich stažení se přenáší IP adresa vašeho zařízení,
      což je technicky nezbytné pro doručení obsahu.</p>

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
      <p>Svá práva uplatníte na adrese <a href="mailto:info@bfksystems.cz">info@bfksystems.cz</a>.
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
    "desc": "Požadovaná stránka na webu simulacni-zkousky.cz neexistuje.",
    "eyebrow": "Chyba 404", "h1": "Tuhle stránku jsme nenašli",
    "breadcrumb": None,
    "intro": "<p>Odkaz může být zastaralý, nebo v adrese chybí písmeno. Zkuste některý z rozcestníků "
             "níž — nebo nám rovnou zavolejte.</p>",
    "body": sekce(
        "Kam dál",
        karty([
            (I["dok"], "Kategorie výroben",
             "<p>A1, A2, B1, B2, C a D — co se u které kategorie ověřuje.</p>", "index.html#kategorie"),
            (I["graf"], "Služby",
             "<p>Simulace souladu, zkoušky na místě, ochrany, telemetrie.</p>", "index.html#sluzby"),
            (I["hodiny"], "Proces připojení",
             "<p>Pět kroků od smlouvy o připojení ke konečnému provoznímu oznámení.</p>",
             "proces-pripojeni.html"),
            (I["info"], "Časté dotazy",
             "<p>Osmnáct nejčastějších otázek i s odpověďmi.</p>", "faq.html"),
        ]),
    ),
})

PAGES = STRANKY
