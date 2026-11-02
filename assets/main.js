/* Botín Diario · comportamiento de la web (sin dependencias) */
(function () {
  "use strict";
  var C = window.BOTIN || {};

  function safe(fn, name) {
    try { fn(); } catch (e) { if (window.console) console.warn("[botin] " + name, e); }
  }

  // Cuenta regresiva al lanzamiento
  function initCountdown() {
    var els = document.querySelectorAll("[data-countdown]");
    if (!els.length) return;
    var target = new Date(C.launch || "2026-11-19T00:00:00+01:00").getTime();
    function paint() {
      var ms = target - Date.now();
      var text, short;
      if (ms <= 0) { text = "¡Ya está a la venta!"; short = "¡Ya!"; }
      else {
        var d = Math.floor(ms / 864e5);
        var h = Math.floor((ms % 864e5) / 36e5);
        var m = Math.floor((ms % 36e5) / 6e4);
        text = d + " días, " + h + " h y " + m + " min";
        short = String(d);
      }
      for (var i = 0; i < els.length; i++) {
        els[i].textContent = els[i].getAttribute("data-countdown") === "days" ? short : text;
      }
    }
    paint();
    setInterval(paint, 30000);
  }

  // Botón del canal de WhatsApp: solo aparece si hay enlace configurado
  function initWhatsApp() {
    var btns = document.querySelectorAll("[data-whatsapp]");
    for (var i = 0; i < btns.length; i++) {
      if (C.whatsapp) { btns[i].href = C.whatsapp; btns[i].hidden = false; }
    }
  }

  // Enlaces de redes
  function initSocials() {
    ["tiktok", "instagram", "youtube"].forEach(function (k) {
      var links = document.querySelectorAll('[data-social="' + k + '"]');
      for (var i = 0; i < links.length; i++) if (C[k]) links[i].href = C[k];
    });
  }

  // Añade tu ID de afiliado a todos los enlaces de Amazon marcados
  function initAmazon() {
    if (!C.amazonTag) return;
    var links = document.querySelectorAll("a[data-amazon]");
    for (var i = 0; i < links.length; i++) {
      try {
        var u = new URL(links[i].href);
        u.searchParams.set("tag", C.amazonTag);
        links[i].href = u.toString();
      } catch (e) {}
    }
  }

  function initYear() {
    var y = document.querySelectorAll("[data-year]");
    for (var i = 0; i < y.length; i++) y[i].textContent = new Date().getFullYear();
  }

  function boot() {
    safe(initCountdown, "countdown");
    safe(initWhatsApp, "whatsapp");
    safe(initSocials, "socials");
    safe(initAmazon, "amazon");
    safe(initYear, "year");
  }
  if (document.readyState === "loading") document.addEventListener("DOMContentLoaded", boot);
  else boot();
})();
