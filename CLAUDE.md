# Botín Diario · web (botindiario.com)

Web estática (HTML/CSS/JS, sin compilación). Cada cambio que llega a la rama `main` lo despliega Hostinger automáticamente en `public_html`. **Todo lo que se sube a `main` sale publicado en la web en minutos.**

## Actualizar «El botín del día» (tarea diaria)
1. Edita solo `datos/botin.json`: `fecha` (AAAA-MM-DD, hoy en Madrid), `noticia`, `dato`, `oferta`.
2. Ejecuta `python3 scripts/actualizar_botin.py`. Si falla, corrige el JSON; nunca edites a mano el bloque entre `BOTIN:INICIO` y `BOTIN:FIN` de `index.html`.
3. Commit con el mensaje `Botín del día AAAA-MM-DD` y push a `main`.

## Reglas para lo que se publica
- Solo hechos confirmados por Rockstar, Take-Two, una tienda o un medio serio que hayas abierto. Un rumor nunca va en la portada.
- Si hay contradicciones entre fuentes o dudas, no publiques ese dato: usa otro dato vigente.
- Tú (no vos), claro para España y Latinoamérica. Entre 20 y 400 caracteres por campo.
- HTML permitido: `<strong>` y `<a href="/ruta-interna/">` o enlaces a amazon.es. Nada más.
- Datos fijos comprobados: lanzamiento jueves 19/11/2026 en PS5 y Xbox Series; precarga digital desde el 10/11 (PS5 00:00 hora local; Xbox 01:00 península, 00:00 Canarias), caja con código desde el 12/11; hasta 212 GB; Standard 79,99 €, Ultimate 99,99 €; la caja física trae un código, no disco; desbloqueo a las 00:00 del 19/11 hora peninsular en España (en Canarias son las 23:00 del 18/11, la tienda española libera el juego a la vez).
- No toques ningún otro archivo en la tarea diaria.

## Estructura
- `index.html` portada · `gta-6/*/index.html` artículos · `ofertas/` página de afiliados
- `assets/config.js` ajustes (ID de Amazon `botindiario-21`, WhatsApp, redes, fecha de lanzamiento)
- `ads.txt`, `robots.txt`, `sitemap.xml`, `.htaccess`
