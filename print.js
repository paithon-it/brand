/*
 * print.js — si stampa sempre in chiaro.
 *
 * `print.css` riporta i token ai valori chiari, ma non arriva dappertutto:
 * chi colora il codice (Pygments nel libro, il tema sul sito) scrive un
 * foglio suo agganciato a `data-theme="dark"`, e batterlo a colpi di
 * `!important` vorrebbe dire riscrivere una tavolozza intera e tenerla
 * allineata per sempre.
 *
 * Qui si scambia il tema per la durata della stampa e lo si rimette com'era:
 * una riga sola, e segue TUTTO, comprese le regole che nessuno ha previsto.
 *
 * Da caricare in ogni pagina. Senza JavaScript resta `print.css`, che stampa
 * chiaro comunque.
 */
(function () {
  'use strict';

  var radice = document.documentElement;
  var precedente = null;

  function prima() {
    if (precedente !== null) return;          // due eventi, un solo scambio
    precedente = radice.dataset.theme || '';
    radice.dataset.theme = 'light';
  }

  function dopo() {
    if (precedente === null) return;
    if (precedente) radice.dataset.theme = precedente;
    else delete radice.dataset.theme;
    precedente = null;
  }

  window.addEventListener('beforeprint', prima);
  window.addEventListener('afterprint', dopo);

  // Safari non ha mai emesso beforeprint/afterprint: li' l'unico segnale e'
  // il media query che diventa vero.
  if (window.matchMedia) {
    var mq = window.matchMedia('print');
    if (mq.addEventListener) {
      mq.addEventListener('change', function (e) { e.matches ? prima() : dopo(); });
    } else if (mq.addListener) {
      mq.addListener(function (e) { e.matches ? prima() : dopo(); });
    }
  }
})();
