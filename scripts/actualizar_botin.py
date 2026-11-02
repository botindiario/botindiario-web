#!/usr/bin/env python3
"""Actualiza el bloque «El botín del día» de la portada a partir de datos/botin.json.

Uso:  python3 scripts/actualizar_botin.py
El JSON tiene esta forma:
{
  "fecha": "2026-11-03",
  "noticia": "Texto con <strong>negritas</strong> y <a href=\"/gta-6/mapa/\">enlaces internos</a>",
  "dato": "…",
  "oferta": "…"
}
Solo se permiten <strong>…</strong> y <a href="/ruta-interna/">…</a> (o enlaces a amazon.es);
cualquier otra etiqueta hace fallar el script, para que nunca se publique HTML roto o peligroso.
"""
import html, json, os, re, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MESES = ["enero", "febrero", "marzo", "abril", "mayo", "junio", "julio", "agosto",
         "septiembre", "octubre", "noviembre", "diciembre"]
ICONS = {
 "noticia": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M4 5h13v14H6a2 2 0 0 1-2-2V5Z"/><path d="M17 9h3v8a2 2 0 0 1-2 2"/><path d="M8 9h5M8 13h5M8 16h3"/></svg>',
 "dato": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><circle cx="8" cy="15" r="4"/><path d="m11 12 9-9M17 6l2 2M15 8l2 2"/></svg>',
 "oferta": '<svg viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" aria-hidden="true"><path d="M3 12V4h8l10 10-8 8L3 12Z"/><circle cx="7.5" cy="8.5" r="1.5"/></svg>',
}
LABELS = {"noticia": "Noticia", "dato": "Dato útil", "oferta": "Oferta"}
TAG = re.compile(r"<[^>]*>")
OK = re.compile(r'^(<strong>|</strong>|</a>|<a href="(/[a-z0-9\-/]*|https://www\.amazon\.es/[^"<>\s]*)">)$')

def clean(text, field):
    for t in TAG.findall(text):
        if not OK.match(t):
            sys.exit(f"ERROR en «{field}»: etiqueta no permitida {t!r}")
    # escapa todo lo que no sea etiqueta permitida
    parts, last = [], 0
    for m in TAG.finditer(text):
        parts.append(html.escape(text[last:m.start()], quote=False)); parts.append(m.group(0)); last = m.end()
    parts.append(html.escape(text[last:], quote=False))
    out = "".join(parts).strip()
    if out.count("<strong>") != out.count("</strong>") or out.count("<a ") != out.count("</a>"):
        sys.exit(f"ERROR en «{field}»: etiquetas sin cerrar")
    if not 20 <= len(TAG.sub("", out)) <= 400:
        sys.exit(f"ERROR en «{field}»: el texto debe tener entre 20 y 400 caracteres")
    return out

def main():
    data = json.load(open(os.path.join(ROOT, "datos", "botin.json"), encoding="utf-8"))
    y, m, d = map(int, data["fecha"].split("-"))
    items = "\n".join(
        f'<li><span class="ic">{ICONS[k]}</span><div><b class="k">{LABELS[k]}</b><p>{clean(data[k], k)}</p></div></li>'
        for k in ("noticia", "dato", "oferta"))
    block = (f'<!-- BOTIN:INICIO (generado por scripts/actualizar_botin.py, no editar a mano) -->\n'
             f'<header><h2 id="botin-hoy">El botín del día</h2><time datetime="{y:04d}-{m:02d}-{d:02d}">{d} de {MESES[m-1]}</time></header>\n'
             f'<ol>\n{items}\n</ol>\n<!-- BOTIN:FIN -->')
    p = os.path.join(ROOT, "index.html")
    s = open(p, encoding="utf-8").read()
    a, b = s.index("<!-- BOTIN:INICIO"), s.index("<!-- BOTIN:FIN -->") + len("<!-- BOTIN:FIN -->")
    s = s[:a] + block + s[b:]
    # la fecha de la portada en el sitemap
    sm = os.path.join(ROOT, "sitemap.xml")
    x = open(sm, encoding="utf-8").read()
    x = re.sub(r"(<loc>https://botindiario\.com/</loc><lastmod>)[0-9-]+", rf"\g<1>{data['fecha']}", x)
    open(p, "w", encoding="utf-8").write(s)
    open(sm, "w", encoding="utf-8").write(x)
    print("Botín del día actualizado:", data["fecha"])

if __name__ == "__main__":
    main()
