// Odeslani poptavkoveho formulare.
//
// Formular posila JSON pres fetch(), takze navstevnik zustane na strance.
// Pole "redirect" ve formulari je zalozni cesta pro prohlizec bez JavaScriptu —
// tam probehne klasicky POST a navrat zpet s ?sent=1.
//
// Access key je v HTML formulare (kontakt.html), ne tady.

const OK_MSG = 'Děkujeme! Poptávka odešla. Ozveme se do dvou pracovních dnů.';
const ERR_MSG = 'Odeslání se nepodařilo. Zkuste to prosím znovu, nebo nám zavolejte na +420 776 111 100.';

// Stav po navratu z externi sluzby (varianta bez JavaScriptu).
(function stavZUrl() {
  const params = new URLSearchParams(location.search);
  if (!params.has('sent')) return;
  const el = document.getElementById('contact-status');
  if (!el) return;
  const ok = params.get('sent') === '1';
  el.className = ok ? 'ok' : 'err';
  el.textContent = ok ? OK_MSG : ERR_MSG;
  el.scrollIntoView({ block: 'center' });
})();

// Nazvy poli jdou do e-mailu tak, jak jsou napsana ve formulari (proto cesky).
// Predmet a reply-to doplnujeme az pred odeslanim, at jde notifikace rovnou
// zodpovedet zakaznikovi a v predmetu je videt, o co jde.
function doplnMetadata(form) {
  const hodnota = (n) => (form.querySelector(`[name="${n}"]`)?.value || '').trim();
  const nastav = (n, v) => { const el = form.querySelector(`input[name="${n}"]`); if (el && v) el.value = v; };

  const jmeno = hodnota('Jméno a příjmení');
  const kategorie = hodnota('Kategorie');
  const zajem = hodnota('Zájem o');

  nastav('replyto', hodnota('E-mail'));
  nastav('subject', ['Poptávka simulacni-zkousky.cz', zajem, kategorie, jmeno]
    .filter(Boolean).join(' – '));
}

(function odeslani() {
  const form = document.getElementById('contact-form');
  if (!form) return;
  const status = document.getElementById('contact-status');
  const button = form.querySelector('button[type=submit]');
  const key = form.querySelector('input[name="access_key"]');

  if (!key || key.value.startsWith('PLACEHOLDER')) {
    console.warn('[simulacni-zkousky] Access key formuláře není vyplněný — formulář nic neodešle. '
      + 'Doplň ho v kontakt.html (a v nastroje/obsah.py, ať to přežije build).');
  }

  form.addEventListener('submit', async (e) => {
    e.preventDefault();
    const popisek = button.textContent;
    button.disabled = true;
    button.textContent = 'Odesílám…';
    status.className = '';
    status.textContent = '';

    doplnMetadata(form);

    try {
      // Nazvy poli maji diakritiku; z multipartu je nektere sluzby ctou jako
      // Latin-1 a v e-mailu je pak rozsypany caj. Z JSONu se prectou spravne.
      const pole = Object.fromEntries(new FormData(form).entries());
      const res = await fetch(form.action, {
        method: 'POST',
        headers: { Accept: 'application/json', 'Content-Type': 'application/json' },
        body: JSON.stringify(pole),
      });
      const data = await res.json().catch(() => ({}));
      if (res.ok && data.success) {
        status.className = 'ok';
        status.textContent = OK_MSG;
        form.reset();
      } else {
        status.className = 'err';
        status.textContent = ERR_MSG;
        console.warn('[simulacni-zkousky] Odpověď služby:', res.status, data);
      }
    } catch (err) {
      status.className = 'err';
      status.textContent = ERR_MSG;
      console.warn('[simulacni-zkousky] Odeslání selhalo:', err);
    } finally {
      button.disabled = false;
      button.textContent = popisek;
      status.scrollIntoView({ block: 'center' });
    }
  });
})();
