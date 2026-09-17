// Rozbalovaci polozky v hlavnim menu (Kategorie, Distributori, Sluzby).
//
// Bez JS otevira podmenu CSS na :hover a :focus-within. Skript prida na <nav>
// tridu .js-menu a od te chvile ridi viditelnost jen trida .open, kterou meni
// vzdy spolu s aria-expanded. Driv menu otevirala trojice :hover, :focus-within
// a .open najednou, takze Escape sice sundal .open a aria-expanded, ale podmenu
// zustalo videt.
//   - mys: najeti otevre, odjeti zavre; klik na tlacitko menu pripne
//   - dotyk: klepnuti otevre a zavre (hover tam neni)
//   - klavesnice: focus dovnitr otevre, odchod zavre; Escape zavre a vrati
//     focus na tlacitko – menu pak zustane zavrene, dokud focus blok neopusti
//     nebo se tlacitko nestiskne
//   - klik mimo menu zavre vse
(function dropdownMenu() {
  const nav = document.querySelector('nav.primary');
  const wraps = nav ? [...nav.querySelectorAll('.has-sub')] : [];
  if (!wraps.length) return;
  nav.classList.add('js-menu');

  // data-mys = otevreno najetim mysi (odjeti zavre)
  // data-escape = zavreno Escapem (focus uvnitr menu znovu neotevre)
  const nastav = (wrap, otevrit) => {
    wrap.classList.toggle('open', otevrit);
    const b = wrap.querySelector('.sub-toggle');
    if (b) b.setAttribute('aria-expanded', otevrit ? 'true' : 'false');
    if (!otevrit) delete wrap.dataset.mys;
  };
  const otevri = (wrap) => {
    wraps.forEach((w) => { if (w !== wrap) nastav(w, false); });
    nastav(wrap, true);
  };
  // Focus po kliknuti nebo klepnuti menu neotevira – to resi klik.
  const zKlavesnice = (el) => {
    try { return el.matches(':focus-visible'); } catch (e) { return true; }
  };

  wraps.forEach((wrap) => {
    const toggle = wrap.querySelector('.sub-toggle');
    if (!toggle) return;

    toggle.addEventListener('click', (e) => {
      e.preventDefault();
      delete wrap.dataset.escape;
      if (wrap.dataset.mys) { delete wrap.dataset.mys; return; }
      if (wrap.classList.contains('open')) nastav(wrap, false);
      else otevri(wrap);
    });

    wrap.addEventListener('pointerenter', (e) => {
      if (e.pointerType !== 'mouse' || wrap.classList.contains('open')) return;
      otevri(wrap);
      wrap.dataset.mys = '1';
    });
    wrap.addEventListener('pointerleave', (e) => {
      if (e.pointerType !== 'mouse') return;
      delete wrap.dataset.escape;
      if (wrap.dataset.mys) nastav(wrap, false);
    });

    wrap.addEventListener('focusin', (e) => {
      if (wrap.dataset.escape || !zKlavesnice(e.target)) return;
      if (!wrap.classList.contains('open')) otevri(wrap);
      delete wrap.dataset.mys;
    });
    wrap.addEventListener('focusout', (e) => {
      if (wrap.contains(e.relatedTarget)) return;
      delete wrap.dataset.escape;
      if (!wrap.dataset.mys) nastav(wrap, false);
    });
  });

  document.addEventListener('keydown', (e) => {
    if (e.key !== 'Escape') return;
    const otevreny = wraps.find((w) => w.classList.contains('open'));
    if (!otevreny) return;
    e.preventDefault();
    const b = otevreny.querySelector('.sub-toggle');
    const vratitFocus = otevreny.contains(document.activeElement);
    otevreny.dataset.escape = '1';
    nastav(otevreny, false);
    if (b && vratitFocus) b.focus();
  });

  document.addEventListener('click', (e) => {
    if (e.target.closest('nav.primary .has-sub')) return;
    wraps.forEach((w) => nastav(w, false));
  });
})();

// Mobilni celoobrazovkove menu.
//
// Otevrene menu je modalni dialog pres celou obrazovku, takze musi:
//   - hlasit stav na hamburgeru (aria-expanded),
//   - presunout focus dovnitr a po zavreni ho vratit na hamburger,
//   - drzet focus uvnitr (jinak by tabulator utekl na skryty obsah pod menu),
//   - zavirat se Escapem,
//   - zablokovat rolovani stranky pod sebou.
// Driv to byly dva inline onclick handlery, ktere neresily nic z toho.
(function mobileMenu() {
  const menu = document.getElementById('mmenu');
  const open = document.getElementById('menu-open');
  const close = document.getElementById('menu-close');
  if (!menu || !open || !close) return;

  const FOCUSABLE = 'a[href], button:not([disabled]), input, select, textarea, [tabindex]:not([tabindex="-1"])';
  const jeOtevreno = () => menu.classList.contains('open');

  const otevri = () => {
    menu.classList.add('open');
    open.setAttribute('aria-expanded', 'true');
    document.documentElement.classList.add('menu-open');
    close.focus();
  };

  const zavri = ({ vratitFocus = true } = {}) => {
    menu.classList.remove('open');
    open.setAttribute('aria-expanded', 'false');
    document.documentElement.classList.remove('menu-open');
    if (vratitFocus) open.focus();
  };

  open.addEventListener('click', otevri);
  close.addEventListener('click', () => zavri());

  // Kliknuti na polozku menu vede na jinou stranku nebo kotvu — menu zaviráme,
  // ale focus nevracime na hamburger, at neprebliká pred odchodem.
  menu.querySelectorAll('a').forEach((a) => {
    a.addEventListener('click', () => zavri({ vratitFocus: false }));
  });

  document.addEventListener('keydown', (e) => {
    if (!jeOtevreno()) return;

    if (e.key === 'Escape') {
      e.preventDefault();
      zavri();
      return;
    }

    if (e.key !== 'Tab') return;
    const prvky = [...menu.querySelectorAll(FOCUSABLE)].filter((el) => el.offsetParent !== null);
    if (!prvky.length) return;
    const prvni = prvky[0];
    const posledni = prvky[prvky.length - 1];

    if (e.shiftKey && document.activeElement === prvni) {
      e.preventDefault();
      posledni.focus();
    } else if (!e.shiftKey && document.activeElement === posledni) {
      e.preventDefault();
      prvni.focus();
    } else if (!menu.contains(document.activeElement)) {
      e.preventDefault();
      prvni.focus();
    }
  });

  // Pri prechodu na sirsi displej se hamburger schova — menu by pak zustalo
  // viset pres obsah a rolovani zablokovane.
  window.matchMedia('(min-width: 1081px)').addEventListener('change', (e) => {
    if (e.matches && jeOtevreno()) zavri({ vratitFocus: false });
  });
})();
