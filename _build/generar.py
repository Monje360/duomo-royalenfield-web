#!/usr/bin/env python3
"""
Generador de la web Royal Enfield Madrid Sur (Duomo Motor Bikes): concesionario oficial Royal Enfield en Móstoles.

Uso:  python3 _build/generar.py     (desde la raíz del repo)

Lee _build/modelos.json (precios por color, textos, colores, equipamiento, galerías y fotos de cada moto,
sacados del WordPress anterior) y crea las páginas HTML estáticas, sitemap.xml, robots.txt, llms.txt y el blog.
Para cambiar un precio: edita modelos.json y vuelve a ejecutar este script.
"""
import json, os, re, html, datetime
from urllib.parse import quote

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
M = json.load(open(os.path.join(ROOT, "_build", "modelos.json"), encoding="utf-8"))
TODAY = datetime.date.today().isoformat()

# ------------------------------------------------------------------ DATOS
SITE = "https://royalenfield.duomomotor.com"
NEGOCIO = {
    "nombre": "Royal Enfield Madrid Sur · Duomo Motor Bikes",
    "razon": "DUOMO MOTOR BIKES S.L.",
    "cif": "B-88303029",
    "calle": "Calle Juan de la Cierva, 7-9",
    "cp": "28936",
    "ciudad": "Móstoles",
    "provincia": "Madrid",
    "tel": "910 409 276",
    "telIntl": "+34910409276",
    "email": "info@duomomotor.com",
    "instagram": "https://www.instagram.com/duomomotorbikes/",
    "instagramUser": "@duomomotorbikes",
    "horario": "Lunes a viernes de 10:00 a 14:00 y de 16:00 a 19:30 · Sábados de 10:00 a 14:00",
}
WHATSAPP = "34613915505"; WHATSAPP_TXT = "613 91 55 05"
DIRECCION = f'{NEGOCIO["calle"]}, {NEGOCIO["cp"]} {NEGOCIO["ciudad"]}, {NEGOCIO["provincia"]}'
MAPS_EMBED = "https://www.google.com/maps?q=Duomo+Motor+Bikes,+Calle+Juan+de+la+Cierva+9,+28936+M%C3%B3stoles,+Madrid&output=embed"
MAPS_DIR = "https://www.google.com/maps/dir/?api=1&destination=Duomo+Motor+Bikes+Calle+Juan+de+la+Cierva+9+28936+M%C3%B3stoles"
GEO = {"@type": "GeoCoordinates", "latitude": 40.3156913, "longitude": -3.8449764}
GMAPS = "https://maps.google.com/?cid=11488602729117650723"
INDEXNOW_KEY = "9b3e5c71a2f84d06e1c7b9a3f5d2e840"
FAMS = [("350", "Gama 350", "Monocilíndricas de 349 cc"), ("450", "Gama 450", "Sherpa 450 de 452 cc"), ("650", "Gama 650", "Bicilíndricas de 648 cc")]
CREDITO = "Duomo Motor Bikes, concesionario oficial Royal Enfield en Móstoles (Madrid)."

def e(s): return html.escape(str(s), quote=True)
def eur(n): return f"{n:,.0f}".replace(",", ".") + " €"
def model_url(m): return f"/moto/{m['slug']}/"
def full(m): return f"Royal Enfield {m['name']}"
def jsonld(obj): return '<script type="application/ld+json">' + json.dumps(obj, ensure_ascii=False, separators=(",", ":")) + "</script>"
def plain(s): return re.sub(r"<[^>]+>", "", s)
def mm(slug): return next(m for m in M if m["slug"] == slug)
def precio_min(): return min(m["price"] for m in M)

HORAS = [
    {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "10:00", "closes": "14:00"},
    {"@type": "OpeningHoursSpecification", "dayOfWeek": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday"], "opens": "16:00", "closes": "19:30"},
    {"@type": "OpeningHoursSpecification", "dayOfWeek": "Saturday", "opens": "10:00", "closes": "14:00"}]
DEALER_ID = SITE + "/#concesionario"
DEALER = {
    "@context": "https://schema.org", "@type": "MotorcycleDealer", "@id": DEALER_ID,
    "name": "Royal Enfield Madrid Sur · Duomo Motor Bikes", "alternateName": "Royal Enfield Móstoles", "legalName": NEGOCIO["razon"], "url": SITE + "/",
    "image": SITE + "/assets/img/og/royal-enfield-madrid-sur.jpg", "logo": SITE + "/assets/img/logo/royal-enfield-madrid-sur-negro.png",
    "telephone": NEGOCIO["telIntl"], "email": NEGOCIO["email"], "priceRange": "€€",
    "address": {"@type": "PostalAddress", "streetAddress": NEGOCIO["calle"], "postalCode": NEGOCIO["cp"],
                "addressLocality": NEGOCIO["ciudad"], "addressRegion": "Comunidad de Madrid", "addressCountry": "ES"},
    "openingHoursSpecification": HORAS, "brand": {"@type": "Brand", "name": "Royal Enfield"},
    "geo": GEO, "hasMap": GMAPS, "sameAs": [NEGOCIO["instagram"], GMAPS],
    "aggregateRating": {"@type": "AggregateRating", "ratingValue": "4.8", "bestRating": "5", "ratingCount": "700"},
    "parentOrganization": {"@type": "Organization", "name": "Duomo Motor Bikes", "url": "https://duomomotor.com/"},
}

# ------------------------------------------------------------------ PLANTILLA
def head(title, desc, path, og_img="/assets/img/og/royal-enfield-madrid-sur.jpg", ld=(), noindex=False, preload=None):
    canon = SITE + path
    ld_html = "\n".join(jsonld(x) for x in ld)
    pre = f'<link rel="preload" as="image" href="{preload}" fetchpriority="high">' if preload else ""
    robots = '<meta name="robots" content="noindex, follow">' if noindex else '<meta name="robots" content="index, follow, max-image-preview:large">'
    fonts = "https://fonts.googleapis.com/css2?family=Barlow+Condensed:wght@600;700;800&family=Montserrat:wght@400;500;600;700&display=swap"
    return f"""<!DOCTYPE html>
<html lang="es" class="no-js">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{e(title)}</title>
  <meta name="description" content="{e(desc)}">
  {robots}
  <link rel="canonical" href="{canon}">
  <meta name="theme-color" content="#111111">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="es_ES">
  <meta property="og:site_name" content="Royal Enfield Madrid Sur · Duomo Motor Bikes">
  <meta property="og:title" content="{e(title)}">
  <meta property="og:description" content="{e(desc)}">
  <meta property="og:url" content="{canon}">
  <meta property="og:image" content="{SITE}{og_img}">
  <meta property="og:image:width" content="1200">
  <meta property="og:image:height" content="630">
  <meta property="og:image:alt" content="{e(title)}">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="alternate" type="application/rss+xml" title="Blog Royal Enfield Madrid Sur" href="{SITE}/blog/feed.xml">
  <link rel="icon" href="/favicon.png" sizes="32x32">
  <link rel="apple-touch-icon" href="/assets/img/logo/icon-180.png">
  <link rel="manifest" href="/site.webmanifest">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="{fonts}" rel="stylesheet" media="print" onload="this.media='all'">
  <noscript><link href="{fonts}" rel="stylesheet"></noscript>
  {pre}
  <link rel="stylesheet" href="/assets/css/style.css">
  <script>document.documentElement.classList.remove('no-js')</script>
  {ld_html}
</head>"""

NAV = [("Inicio", "/", "inicio"), ("Motocicletas", "/#gama", "modelos"), ("Nosotros", "/concesionario-royal-enfield-en-madrid-sur/", "nosotros"),
       ("Blog", "/blog/", "blog"), ("Contáctanos", "/contacto/", "contacto")]

def header(active=""):
    links = "".join(f'<a href="{u}"{" class=\"active\" aria-current=\"page\"" if k == active else ""}>{n}</a>' for n, u, k in NAV)
    return f"""<body>
  <a class="skip" href="#contenido">Saltar al contenido</a>
  <header class="site-header site-header--dark">
    <div class="wrap nav">
      <a class="brand" href="/" aria-label="Royal Enfield Madrid Sur · Inicio">
        <img src="/assets/img/logo/royal-enfield-madrid-sur-blanco.png" alt="Royal Enfield Madrid Sur" width="283" height="80">
      </a>
      <nav class="nav__links" id="menu" aria-label="Menú principal">
        {links}
        <a class="btn btn--primary" href="/solicitud-de-prueba/">Solicita una prueba</a>
      </nav>
      <button class="nav__toggle" aria-label="Abrir menú" aria-expanded="false" aria-controls="menu"><span></span><span></span><span></span></button>
    </div>
  </header>
  <main id="contenido">"""

def footer():
    motos = "".join(f'<a href="{model_url(m)}">{e(m["name"])}</a>' for m in M)
    return f"""  </main>
  <footer class="site-footer">
    <div class="wrap footer-grid">
      <div>
        <img class="footer-logo" src="/assets/img/logo/royal-enfield-madrid-sur-blanco.png" alt="Royal Enfield Madrid Sur" width="283" height="80" loading="lazy">
        <p style="max-width:38ch">Noticias de interés, equipamiento nuevo para tu Royal Enfield, ofertas, promociones y más.</p>
        <p class="disclaimer">Royal Enfield y los nombres de sus modelos son marcas registradas de su fabricante. Esta web pertenece a un concesionario oficial, no es la web oficial de la marca. Precios orientativos sujetos a la tarifa y promociones vigentes.</p>
      </div>
      <div>
        <h2>Páginas</h2>
        <a href="/">Inicio</a>
        <a href="/concesionario-royal-enfield-en-madrid-sur/">Nosotros</a>
        <a href="/solicitud-de-prueba/">Solicitud de prueba</a>
        <a href="/blog/">Blog</a>
        <a href="/contacto/">Contacto</a>
      </div>
      <div class="footer-motos">
        <h2>Motocicletas</h2>
        {motos}
      </div>
      <div>
        <h2>Contacto</h2>
        <address>
          <a href="{MAPS_DIR}" target="_blank" rel="noopener"><b>Duomo Motor Bikes</b><br>{e(NEGOCIO["calle"])}<br>{NEGOCIO["cp"]} {e(NEGOCIO["ciudad"])} (Madrid)</a>
          <a href="tel:{NEGOCIO["telIntl"]}">{NEGOCIO["tel"]}</a>
          <a href="mailto:{NEGOCIO["email"]}">{NEGOCIO["email"]}</a>
          <a href="https://wa.me/{WHATSAPP}" target="_blank" rel="noopener">WhatsApp {WHATSAPP_TXT}</a>
          <a href="{NEGOCIO["instagram"]}" target="_blank" rel="noopener">{NEGOCIO["instagramUser"]}</a>
        </address>
      </div>
    </div>
    <div class="wrap footer-bottom">
      <span>© <span id="year">{datetime.date.today().year}</span> {NEGOCIO["razon"]}. Todos los derechos reservados.</span>
      <span><a href="/aviso-legal/">Aviso Legal</a> · <a href="/politica-de-cookies/">Política de Cookies</a> · <a href="/politicas-de-privacidad/">Políticas de Privacidad</a></span>
    </div>
  </footer>
  <a class="wa-float" href="https://wa.me/{WHATSAPP}" target="_blank" rel="noopener" aria-label="Escríbenos por WhatsApp">{ICO["wa"]}</a>
  <script src="/assets/js/config.js"></script>
  <script src="/assets/js/app.js" defer></script>
  <script src="/assets/js/cookies.js" defer></script>
</body>
</html>
"""

def write(path, content):
    fp = os.path.join(ROOT, path.strip("/"), "index.html") if not path.endswith(".html") else os.path.join(ROOT, path.strip("/"))
    os.makedirs(os.path.dirname(fp), exist_ok=True)
    open(fp, "w", encoding="utf-8").write(content)

def crumbs_html(items):
    lis = "".join((f'<li><a href="{u}">{e(n)}</a></li>' if i < len(items) - 1 else f'<li aria-current="page">{e(n)}</li>') for i, (n, u) in enumerate(items))
    return f'<nav class="crumbs wrap" aria-label="Migas de pan"><ol>{lis}</ol></nav>'

def cta_band(title="Solicita una prueba", text="Ven a Royal Enfield Madrid Sur, en Móstoles, y prueba tu próxima Royal Enfield."):
    return f"""<section class="section"><div class="wrap"><div class="cta-band reveal">
      <h2>{title}</h2><p>{text}</p>
      <div class="hero__actions">
        <a class="btn btn--primary" href="/solicitud-de-prueba/">Solicita una prueba</a>
        <a class="btn btn--ghost-light" href="/contacto/">Contáctanos</a>
      </div></div></div></section>"""

def visit_block(h="Dónde estamos"):
    return f"""<div class="visit reveal">
      <div class="visit__info">
        <span class="eyebrow">Concesionario oficial Royal Enfield</span>
        <h2>{h}</h2>
        <div class="info-item"><div class="info-item__ico">{ICO["pin"]}</div><div><h3>Dirección</h3><p>Duomo Motor Bikes · {e(DIRECCION)}</p></div></div>
        <div class="info-item"><div class="info-item__ico">{ICO["clock"]}</div><div><h3>Horario</h3><p>{e(NEGOCIO["horario"])}</p></div></div>
        <div class="info-item"><div class="info-item__ico">{ICO["tel"]}</div><div><h3>Teléfono</h3><a href="tel:{NEGOCIO["telIntl"]}">{NEGOCIO["tel"]}</a></div></div>
        <div class="hero__actions"><a class="btn btn--primary" href="{MAPS_DIR}" target="_blank" rel="noopener">Cómo llegar</a><a class="btn btn--ghost-light" href="/solicitud-de-prueba/">Solicita una prueba</a></div>
      </div>
      <iframe src="{MAPS_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Mapa de Royal Enfield Madrid Sur"></iframe>
    </div>"""

def marquee(words):
    items = "".join(f"<span>{e(w)}</span><i>✦</i>" for w in words)
    return f'<div class="marquee" aria-hidden="true"><div class="marquee__track">{items}{items}</div></div>'

def card(m, lazy=True, h="h3"):
    ncol = len(m["colors"])
    im = m["main"]
    return f"""<article class="card card--re reveal" data-cat="{m["family"]}">
        <a class="card__media" href="{model_url(m)}" tabindex="-1" aria-hidden="true"><img src="/{im["img"]}" alt="{e(full(m))}" width="{im["w"]}" height="{im["h"]}"{' loading="lazy" decoding="async"' if lazy else ''}></a>
        <div class="card__body">
          <span class="card__cat">Gama {m["family"]}</span>
          <{h} class="card__title"><a href="{model_url(m)}">{e(m["name"])}</a></{h}>
          {f'<div class="card__colors">{ncol} colores</div>' if ncol > 1 else '<div class="card__colors">1 color</div>'}
          <div class="card__foot">
            <span class="card__price"><small>Desde</small>{eur(m["price"])}</span>
            <a class="card__link" href="{model_url(m)}">Ver modelo <i>&rsaquo;</i></a>
          </div>
        </div>
      </article>"""

PRICE_NOTE = "PVP recomendado con IVA incluido. Consulta en el concesionario los gastos de matriculación y transporte, la disponibilidad y las condiciones de financiación."

def crumbs_ld(items):
    return {"@context": "https://schema.org", "@type": "BreadcrumbList", "itemListElement": [
        {"@type": "ListItem", "position": i + 1, "name": n, "item": SITE + u} for i, (n, u) in enumerate(items)]}

def faq_ld(qas):
    return {"@context": "https://schema.org", "@type": "FAQPage", "mainEntity": [
        {"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": plain(a)}} for q, a in qas]}

# ------------------------------------------------------------------ ICONOS
ICO = {
    "wa": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M.057 24l1.687-6.163a11.867 11.867 0 01-1.587-5.945C.16 5.335 5.5 0 12.05 0a11.82 11.82 0 018.413 3.488 11.82 11.82 0 013.48 8.414c-.003 6.557-5.338 11.892-11.893 11.892a11.9 11.9 0 01-5.688-1.448L.057 24zm6.597-3.807c1.676.995 3.276 1.591 5.392 1.592 5.448 0 9.886-4.434 9.889-9.885.002-5.462-4.415-9.89-9.881-9.892-5.452 0-9.887 4.434-9.889 9.884a9.86 9.86 0 001.51 5.26l-.999 3.648 3.978-1.607zm11.387-5.464c-.074-.124-.272-.198-.57-.347-.297-.149-1.758-.868-2.031-.967-.272-.099-.47-.149-.669.149-.198.297-.767.967-.94 1.165-.173.198-.347.223-.644.074-.297-.149-1.255-.462-2.39-1.475-.883-.788-1.48-1.761-1.653-2.059-.173-.297-.018-.458.13-.606.134-.133.297-.347.446-.521.151-.172.2-.296.3-.495.099-.198.05-.372-.025-.521-.075-.148-.669-1.611-.916-2.206-.242-.579-.487-.501-.669-.51l-.57-.01c-.198 0-.52.074-.792.372s-1.04 1.016-1.04 2.479 1.065 2.876 1.213 3.074c.149.198 2.095 3.2 5.076 4.487.709.306 1.263.489 1.694.626.712.226 1.36.194 1.872.118.571-.085 1.758-.719 2.006-1.413.248-.695.248-1.29.173-1.414z"/></svg>',
    "pin": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a7 7 0 0 0-7 7c0 5.25 7 13 7 13s7-7.75 7-13a7 7 0 0 0-7-7zm0 9.5A2.5 2.5 0 1 1 12 6a2.5 2.5 0 0 1 0 5.5z"/></svg>',
    "tel": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M6.6 10.8a15.1 15.1 0 0 0 6.6 6.6l2.2-2.2c.3-.3.7-.4 1-.2 1.1.4 2.3.6 3.6.6.6 0 1 .4 1 1V20c0 .6-.4 1-1 1A17 17 0 0 1 3 4c0-.6.4-1 1-1h3.5c.6 0 1 .4 1 1 0 1.3.2 2.5.6 3.6.1.3 0 .7-.2 1z"/></svg>',
    "mail": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M20 4H4a2 2 0 0 0-2 2v12a2 2 0 0 0 2 2h16a2 2 0 0 0 2-2V6a2 2 0 0 0-2-2zm0 4-8 5-8-5V6l8 5 8-5z"/></svg>',
    "clock": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 2a10 10 0 1 0 0 20 10 10 0 0 0 0-20zm1 10.4 3.6 2.1-.8 1.3L11 13V7h2z"/></svg>',
    "ig": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 7a5 5 0 1 0 0 10 5 5 0 0 0 0-10zm0 8.2a3.2 3.2 0 1 1 0-6.4 3.2 3.2 0 0 1 0 6.4zM17.2 5.6a1.2 1.2 0 1 0 0 2.4 1.2 1.2 0 0 0 0-2.4zM21.9 7.1c-.1-1.6-.4-3-1.6-4.2S17.7 1.3 16.1 1.2C14.4 1.1 9.6 1.1 7.9 1.2 6.3 1.3 4.9 1.6 3.7 2.8S2.1 5.5 2 7.1C1.9 8.8 1.9 15.2 2 16.9c.1 1.6.4 3 1.6 4.2s2.6 1.5 4.2 1.6c1.7.1 6.5.1 8.2 0 1.6-.1 3-.4 4.2-1.6s1.5-2.6 1.6-4.2c.2-1.7.2-8.1.1-9.8zm-2.2 11.6a3.3 3.3 0 0 1-1.9 1.9c-1.3.5-4.4.4-5.8.4s-4.5.1-5.8-.4a3.3 3.3 0 0 1-1.9-1.9c-.5-1.3-.4-4.4-.4-5.8s-.1-4.5.4-5.8a3.3 3.3 0 0 1 1.9-1.9c1.3-.5 4.4-.4 5.8-.4s4.5-.1 5.8.4a3.3 3.3 0 0 1 1.9 1.9c.5 1.3.4 4.4.4 5.8s.1 4.5-.4 5.8z"/></svg>',
    "shield": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12 1 3 5v6c0 5.6 3.8 10.7 9 12 5.2-1.3 9-6.4 9-12V5zm-2 16-4-4 1.4-1.4L10 14.2l6.6-6.6L18 9z"/></svg>',
    "wrench": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M22.7 19 13.6 9.9c.9-2.3.4-5-1.5-6.9-2-2-5-2.4-7.4-1.3L9 6 6 9 1.6 4.7C.4 7.1.9 10.1 2.9 12.1c1.9 1.9 4.6 2.4 6.9 1.5l9.1 9.1c.4.4 1 .4 1.4 0l2.3-2.3c.5-.4.5-1.1.1-1.4z"/></svg>',
    "star": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="m12 17.3 6.2 3.7-1.6-7 5.4-4.7-7.1-.6L12 2 9.1 8.7 2 9.3l5.4 4.7-1.6 7z"/></svg>',
    "bike": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M5 11a4 4 0 1 0 0 8 4 4 0 0 0 0-8zm0 6.2a2.2 2.2 0 1 1 0-4.4 2.2 2.2 0 0 1 0 4.4zM19 11a4 4 0 1 0 0 8 4 4 0 0 0 0-8zm0 6.2a2.2 2.2 0 1 1 0-4.4 2.2 2.2 0 0 1 0 4.4zM15.6 6H13v1.8h1.7l1.3 2.2H9.5L8.3 8H10V6.2H5v1.8h1.2l1.6 2.6L6.1 13l1.5.9 1.6-2.4L11 15h3.4l2.3-3.8.8 1.3 1.5-.9z"/></svg>',
    "box": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M21 7.5 12 2 3 7.5v9L12 22l9-5.5zM12 4.3l6.1 3.7L12 11.7 5.9 8zM5 9.7l6 3.6v6.3l-6-3.7zm8 9.9v-6.3l6-3.6v6.2z"/></svg>',
    "euro": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M15 18.5A6.5 6.5 0 0 1 9.2 15H15l1-2H8.6a6 6 0 0 1 0-2H16l1-2H9.2A6.5 6.5 0 0 1 15 5.5c1.6 0 3.1.6 4.2 1.6L21 5.3A9 9 0 0 0 6.6 9H3l-1 2h4.1a9 9 0 0 0 0 2H3l-1 2h4.6A9 9 0 0 0 21 18.7l-1.8-1.8a6.4 6.4 0 0 1-4.2 1.6z"/></svg>',
    "key": '<svg viewBox="0 0 24 24" aria-hidden="true"><path d="M12.7 10A6 6 0 1 0 7 18a6 6 0 0 0 5.7-4H17v4h4v-4h2v-4zM7 14a2 2 0 1 1 0-4 2 2 0 0 1 0 4z"/></svg>',
}


def data_box(resp="Titular"):
    return f"""<div class="data-box">
        <p><strong>{resp}:</strong> {NEGOCIO["razon"]}</p>
        <p><strong>CIF:</strong> {NEGOCIO["cif"]}</p>
        <p><strong>Domicilio:</strong> {e(DIRECCION)}</p>
        <p><strong>Teléfono:</strong> {NEGOCIO["tel"]} · <strong>Email:</strong> <a href="mailto:{NEGOCIO["email"]}">{NEGOCIO["email"]}</a></p>
      </div>"""

LEGAL = {
 "/aviso-legal/": ("Aviso legal", "Condiciones generales de uso del sitio web", f"""
      <h2>1. Titular del sitio web</h2>
      <p>En cumplimiento del artículo 10 de la Ley 34/2002, de 11 de julio, de Servicios de la Sociedad de la Información y de Comercio Electrónico (LSSI-CE), se informa de los datos del titular de este sitio web:</p>
      {data_box()}
      <p>En adelante, «el Titular». Este sitio es la web del concesionario oficial que presenta la gama Royal Enfield disponible en sus instalaciones.</p>
      <h2>2. Objeto</h2>
      <p>El presente aviso legal regula el uso del sitio web, que el Titular pone a disposición de los usuarios con carácter informativo sobre los modelos, promociones y servicios relacionados con la marca Royal Enfield. La navegación por el sitio atribuye la condición de usuario e implica la aceptación plena de las presentes condiciones.</p>
      <h2>3. Condiciones de uso</h2>
      <p>El usuario se compromete a hacer un uso adecuado y lícito del sitio web y de sus contenidos, absteniéndose de:</p>
      <ul>
        <li>Utilizar los contenidos con fines contrarios a la ley, la moral o el orden público.</li>
        <li>Introducir o difundir virus o cualquier otro sistema capaz de causar daños en los sistemas del Titular o de terceros.</li>
        <li>Intentar acceder, utilizar o manipular los datos del Titular o de terceros usuarios.</li>
        <li>Reproducir o copiar los contenidos sin autorización.</li>
      </ul>
      <h2>4. Propiedad intelectual e industrial</h2>
      <p>Los textos, el diseño y el código de este sitio son propiedad del Titular o cuentan con la correspondiente autorización para su uso. «Royal Enfield», su logotipo y las denominaciones de sus modelos son marcas registradas de su fabricante, utilizadas por el Titular en su condición de concesionario oficial. Las imágenes de los modelos son fotografías oficiales de la marca. Queda prohibida su reproducción sin autorización de sus respectivos titulares.</p>
      <h2>5. Exención de responsabilidad</h2>
      <p>Los precios, promociones, colores y especificaciones mostrados tienen carácter orientativo y pueden variar sin previo aviso según la tarifa y las campañas vigentes de la marca. No constituyen una oferta contractual vinculante. Para condiciones definitivas, consulta directamente con el concesionario. El Titular no se responsabiliza de los posibles errores tipográficos ni de la disponibilidad de las unidades.</p>
      <h2>6. Enlaces a terceros</h2>
      <p>Este sitio puede contener enlaces a páginas de terceros (por ejemplo, Instagram o servicios de mapas). El Titular no se hace responsable de los contenidos ni de las políticas de privacidad de dichos sitios.</p>
      <h2>7. Legislación aplicable</h2>
      <p>Las presentes condiciones se rigen por la legislación española. Para cualquier controversia, las partes se someten a los juzgados y tribunales que correspondan conforme a derecho.</p>"""),
 "/politicas-de-privacidad/": ("Política de privacidad", "Tratamiento de datos personales (RGPD y LOPDGDD)", f"""
      <h2>1. Responsable del tratamiento</h2>
      {data_box("Responsable")}
      <p>El Responsable trata los datos personales del usuario de conformidad con el Reglamento (UE) 2016/679 (RGPD) y la Ley Orgánica 3/2018, de 5 de diciembre (LOPDGDD).</p>
      <h2>2. ¿Con qué finalidad tratamos tus datos?</h2>
      <p>Tratamos los datos que nos facilitas a través de los formularios de contacto, de solicitud de prueba y de cita de taller, con las siguientes finalidades:</p>
      <ul>
        <li>Atender tu solicitud de información sobre modelos, promociones, financiación o servicios de posventa.</li>
        <li>Gestionar la relación comercial y, en su caso, la reserva o prueba de un vehículo.</li>
        <li>Si nos das tu consentimiento, remitirte comunicaciones comerciales sobre nuestros productos y servicios.</li>
      </ul>
      <h2>3. Legitimación</h2>
      <p>La base legal del tratamiento es el <strong>consentimiento</strong> que otorgas al enviar el formulario y la aplicación de medidas precontractuales a petición tuya. El envío de comunicaciones comerciales se basa en tu consentimiento expreso, revocable en cualquier momento.</p>
      <h2>4. ¿Durante cuánto tiempo conservamos los datos?</h2>
      <p>Los datos se conservarán mientras exista un interés mutuo o durante el tiempo necesario para cumplir con las obligaciones legales. Cuando ya no sean necesarios, se suprimirán con las medidas de seguridad adecuadas.</p>
      <h2>5. ¿A quién comunicamos tus datos?</h2>
      <p>No se cederán datos a terceros, salvo obligación legal o cuando sea necesario para la prestación del servicio (por ejemplo, proveedores tecnológicos que actúan como encargados del tratamiento —como el servicio de envío de formularios FormSubmit—, entidades financieras en caso de financiación, o la marca para gestionar garantías). No se realizan transferencias internacionales fuera del Espacio Económico Europeo sin las garantías adecuadas.</p>
      <h2>6. ¿Cuáles son tus derechos?</h2>
      <ul>
        <li><strong>Acceso:</strong> saber qué datos tuyos tratamos.</li>
        <li><strong>Rectificación:</strong> corregir datos inexactos.</li>
        <li><strong>Supresión:</strong> solicitar que se eliminen tus datos.</li>
        <li><strong>Oposición y limitación:</strong> oponerte o limitar el tratamiento.</li>
        <li><strong>Portabilidad:</strong> recibir tus datos en un formato estructurado.</li>
        <li><strong>Retirar el consentimiento</strong> en cualquier momento.</li>
      </ul>
      <p>Puedes ejercer estos derechos escribiendo a <a href="mailto:{NEGOCIO["email"]}">{NEGOCIO["email"]}</a> o por correo a nuestro domicilio, indicando el derecho que deseas ejercer. Si consideras que el tratamiento no se ajusta a la normativa, puedes reclamar ante la <a href="https://www.aepd.es" target="_blank" rel="noopener">Agencia Española de Protección de Datos (aepd.es)</a>.</p>
      <h2>7. Seguridad</h2>
      <p>El Responsable adopta las medidas técnicas y organizativas necesarias para garantizar la seguridad y confidencialidad de los datos y evitar su alteración, pérdida o acceso no autorizado.</p>"""),
 "/politica-de-cookies/": ("Política de cookies", "Uso de cookies en este sitio web", """
      <h2>1. ¿Qué son las cookies?</h2>
      <p>Una cookie es un pequeño archivo de texto que un sitio web guarda en tu navegador cuando lo visitas. Sirven para que la web funcione correctamente, recordar tus preferencias y, en su caso, obtener datos estadísticos de uso.</p>
      <h2>2. ¿Qué cookies utilizamos?</h2>
      <p>Este sitio es una web estática con un uso mínimo de cookies. Actualmente utiliza únicamente las siguientes:</p>
      <table class="cookie-tbl">
        <thead><tr><th>Cookie</th><th>Tipo</th><th>Finalidad</th><th>Duración</th></tr></thead>
        <tbody>
          <tr><td>duomo_cookie_consent</td><td>Técnica (propia)</td><td>Recordar tu elección sobre el aviso de cookies para no volver a mostrarlo.</td><td>Persistente</td></tr>
          <tr><td>Google Fonts</td><td>Técnica (terceros)</td><td>Cargar la tipografía del sitio desde los servidores de Google.</td><td>De sesión</td></tr>
          <tr><td>Google Maps</td><td>Terceros</td><td>Mostrar el mapa de ubicación del concesionario.</td><td>Según Google</td></tr>
        </tbody>
      </table>
      <p>Los formularios se gestionan a través de un proveedor externo (FormSubmit), que puede establecer sus propias cookies al enviarlos, sujetas a su política.</p>
      <p>Si en el futuro se incorporan cookies de <strong>analítica o publicidad</strong> (por ejemplo, Google Analytics o píxeles de redes sociales), solo se activarán si aceptas su uso en el aviso de cookies.</p>
      <h2>3. ¿Cómo gestionar las cookies?</h2>
      <p>Al entrar en el sitio puedes <strong>aceptar</strong> o <strong>rechazar</strong> el uso de cookies no esenciales mediante el aviso que aparece en la parte inferior. Además, puedes configurar, bloquear o eliminar las cookies desde la configuración de tu navegador:</p>
      <ul>
        <li><a href="https://support.google.com/chrome/answer/95647" target="_blank" rel="noopener">Google Chrome</a></li>
        <li><a href="https://support.mozilla.org/es/kb/Borrar%20cookies" target="_blank" rel="noopener">Mozilla Firefox</a></li>
        <li><a href="https://support.apple.com/es-es/guide/safari/sfri11471/mac" target="_blank" rel="noopener">Safari</a></li>
        <li><a href="https://support.microsoft.com/es-es/microsoft-edge" target="_blank" rel="noopener">Microsoft Edge</a></li>
      </ul>
      <p>Ten en cuenta que desactivar las cookies técnicas puede afectar al correcto funcionamiento del sitio.</p>"""),
}

def page_legal(url, t, sub, content):
    body = f"""
  <section class="legal"><div class="wrap">
      <h1>{t}</h1>
      <p class="updated">{sub}</p>
      {content}
      <p style="margin-top:24px"><a href="/aviso-legal/">Aviso legal</a> · <a href="/politicas-de-privacidad/">Política de privacidad</a> · <a href="/politica-de-cookies/">Política de cookies</a></p>
  </div></section>"""
    write(url, head(f"{t} · Royal Enfield Madrid Sur", f"{t} de la web de Duomo Motor Bikes, concesionario oficial Royal Enfield en Móstoles.", url, noindex=True) + header() + body + footer())

def page_404():
    body = f"""
  <section class="hero hero--page"><div class="hero__bg"><img src="/assets/img/hero/royal-enfield-madrid-sur-2.webp" alt="" width="1600" height="900"></div>
    <div class="wrap"><div class="hero__inner">
      <span class="eyebrow">Error 404</span>
      <h1>Esta página se ha salido de la carretera</h1>
      <p class="lead">Puede que el modelo haya cambiado de nombre o que el enlace ya no exista. Vuelve a la gama completa o escríbenos.</p>
      <div class="hero__actions"><a class="btn btn--primary" href="/#gama">Ver la gama Royal Enfield</a><a class="btn btn--ghost-light" href="/contacto/">Contactar</a></div>
    </div></div></section>"""
    write("/404.html", head("Página no encontrada · Royal Enfield Madrid Sur", "La página que buscas no existe.", "/404.html", noindex=True) + header() + body + footer())

# ------------------------------------------------------------------ SITEMAP / ROBOTS

BLOG_DIR = os.path.join(ROOT, "blog")
POSTS_JSON = os.path.join(BLOG_DIR, "posts.json")

def blog_posts():
    try:
        return json.load(open(POSTS_JSON, encoding="utf-8"))
    except Exception:
        return []

def bcard_html(p):
    return (f'<article class="bcard reveal"><a class="bcard__media" href="/blog/{p["slug"]}/" tabindex="-1" aria-hidden="true">'
            f'<img src="{e(p["imagen"])}" alt="{e(p["imagenAlt"])}" width="{p.get("w", 1200)}" height="{p.get("h", 800)}" loading="lazy" decoding="async"></a>'
            f'<div class="bcard__body"><span class="bcard__meta">{e(p["categoria"])} · {e(p["fechaTxt"])}</span>'
            f'<h2 class="bcard__title"><a href="/blog/{p["slug"]}/">{e(p["titulo"])}</a></h2>'
            f'<p>{e(p["descripcion"])}</p><a class="bcard__more" href="/blog/{p["slug"]}/">Leer artículo <i>&rsaquo;</i></a></div></article>')

BLOG_VACIO = '<p class="blog-empty">Muy pronto: novedades, rutas y consejos para motoristas de Madrid Sur.</p>'

def blog_index_template():
    url = "/blog/"
    crumbs = [("Inicio", "/"), ("Blog", url)]
    ld = [crumbs_ld(crumbs), {"@context": "https://schema.org", "@type": "Blog", "@id": SITE + "/blog/#blog", "name": "Blog Royal Enfield Madrid Sur", "url": SITE + url,
          "inLanguage": "es-ES", "publisher": {"@id": DEALER_ID}, "about": "Motos, rutas, carnet y mantenimiento en Madrid Sur"}]
    body = f"""
  <section class="hero hero--page">
    <div class="hero__bg"><img src="/assets/img/hero/royal-enfield-madrid-sur-3.webp" alt="" width="1600" height="900"></div>
    <div class="wrap"><div class="hero__inner">
      <span class="eyebrow">Blog · Royal Enfield Madrid Sur</span>
      <h1>Blog <span class="hl">Royal Enfield Madrid Sur</span></h1>
      <p class="lead">Novedades, rutas, consejos y todo sobre la gama Royal Enfield, de la mano de Royal Enfield Madrid Sur.</p>
    </div></div>
  </section>
  {crumbs_html(crumbs)}
  <section class="section" style="padding-top:36px">
    <div class="wrap">
      <div class="bgrid" id="blog-list">%%LISTADO%%</div>
    </div>
  </section>
  {cta_band("Tu nueva Royal Enfield", "Ven a verla y pruébala en Royal Enfield Madrid Sur, en Móstoles.")}
"""
    return head("Blog · Motos Royal Enfield Madrid Sur",
                "Novedades, rutas, consejos y todo sobre la gama Royal Enfield. Blog de Royal Enfield Madrid Sur, concesionario oficial en Móstoles.",
                url, ld=ld) + header("blog") + body + footer()

def blog_article_template():
    body = f"""
  <nav class="crumbs wrap" aria-label="Migas de pan"><ol><li><a href="/">Inicio</a></li><li><a href="/blog/">Blog</a></li><li aria-current="page">%%H1_TEXTO%%</li></ol></nav>
  <article class="post">
    <header class="post__head wrap">
      <span class="eyebrow">%%CATEGORIA%% · <time datetime="%%FECHA_ISO%%">%%FECHA_TXT%%</time> · %%LECTURA%% min de lectura</span>
      <h1>%%H1%%</h1>
      <p class="lead">%%ENTRADILLA%%</p>
      <p class="post__byline">Por el equipo de <a href="/concesionario-royal-enfield-en-madrid-sur/">Royal Enfield Madrid Sur</a>, concesionario oficial Royal Enfield en Móstoles</p>
    </header>
    <figure class="post__cover wrap"><img src="%%COVER_IMG%%" alt="%%COVER_ALT%%" width="%%COVER_W%%" height="%%COVER_H%%" fetchpriority="high"></figure>
    <div class="post__layout wrap">
      <div class="post__body">
        %%TLDR%%
        %%TOC%%
        %%CUERPO%%
        %%FAQ%%
        <div class="post__autor">
          <img src="/assets/img/logo/icon-180.png" alt="" width="64" height="64" loading="lazy">
          <div><p class="post__autor-t">Sobre Royal Enfield Madrid Sur</p>
          <p>Somos Duomo Motor Bikes, concesionario oficial Royal Enfield en Móstoles (Madrid), con taller propio especializado, servicio postventa y recambios originales. <a href="/concesionario-royal-enfield-en-madrid-sur/">Conócenos</a>.</p></div>
        </div>
      </div>
      <aside class="post__aside">
        <div class="post__card">
          <span class="eyebrow">Royal Enfield Madrid Sur</span>
          <p class="post__card-t">%%CTA_TITULO%%</p>
          <p>%%CTA_TEXTO%%</p>
          %%CTA_MODELO%%
          <a class="btn btn--primary btn--block" href="/solicitud-de-prueba/%%CTA_QUERY%%">Pedir prueba</a>
          <a class="btn btn--ghost btn--block" href="/contacto/">Pedir información</a>
        </div>
        <div class="post__zonas">
          <p class="post__card-t">Motocicletas</p>
          <a href="/#gama">Toda la gama Royal Enfield</a>
          <a href="/concesionario-royal-enfield-en-madrid-sur/">Nosotros</a>
          <a href="/contacto/">Contáctanos</a>
        </div>
      </aside>
    </div>
  </article>
  <section class="section section--alt">
    <div class="wrap">
      <h2>Sigue leyendo</h2>
      <p class="sub">Más artículos del blog de Royal Enfield Madrid Sur.</p>
      <div class="bgrid">%%RELACIONADOS%%</div>
    </div>
  </section>
  %%CTA_BAND%%
"""
    h = head("%%TITLE%%", "%%META_DESC%%", "/blog/%%SLUG%%/", og_img="%%OG_IMAGE%%")
    h = h.replace('<meta property="og:type" content="website">', '<meta property="og:type" content="article">\n  <meta property="article:published_time" content="%%FECHA_ISO%%">\n  <meta property="article:section" content="%%CATEGORIA%%">')
    h = h.replace(f'{SITE}%%OG_IMAGE%%', '%%OG_IMAGE_ABS%%')
    h = h.replace("</head>", "  %%JSONLD%%\n</head>")
    return h + header("blog") + body + footer()

MAX_TARJETAS = 30

def blog_listado(posts):
    if not posts: return BLOG_VACIO
    resto = posts[MAX_TARJETAS:]
    out = "".join(bcard_html(p) for p in posts[:MAX_TARJETAS])
    if resto:
        out += ('</div><h2 style="margin-top:56px">Todos los artículos</h2><ul class="blog-archivo">'
                + "".join(f'<li><a href="/blog/{p["slug"]}/">{e(p["titulo"])}</a> <span>{e(p["categoria"])} · {e(p["fechaTxt"])}</span></li>' for p in resto)
                + '</ul><div>')
    return out

def blog_relacionados(p, posts):
    otros = [x for x in posts if x["slug"] != p["slug"]]
    orden = [x for x in otros if x["categoria"] == p["categoria"]] + [x for x in otros if x.get("modelo") == p.get("modelo")] + otros
    vistos, rel = set(), []
    for x in orden:
        if x["slug"] in vistos: continue
        vistos.add(x["slug"]); rel.append(x)
        if len(rel) == 3: break
    return "".join(bcard_html(x) for x in rel) or '<p class="blog-empty">Pronto habrá más artículos. Mientras, mira <a href="/#gama">toda la gama Royal Enfield</a>.</p>'

def blog_feed(posts):
    def rfc(d):
        dt = datetime.datetime.strptime(d, "%Y-%m-%d").replace(hour=8, tzinfo=datetime.timezone.utc)
        return dt.strftime("%a, %d %b %Y %H:%M:%S GMT")
    items = "".join(f'<item><title>{e(p["titulo"])}</title><link>{SITE}/blog/{p["slug"]}/</link><guid isPermaLink="true">{SITE}/blog/{p["slug"]}/</guid>'
                    f'<pubDate>{rfc(p["fecha"])}</pubDate><category>{e(p["categoria"])}</category><description>{e(p["descripcion"])}</description></item>' for p in posts[:30])
    last = rfc(posts[0]["fecha"]) if posts else rfc(TODAY)
    return (f'<?xml version="1.0" encoding="UTF-8"?>\n<rss version="2.0" xmlns:atom="http://www.w3.org/2005/Atom"><channel><title>Blog Royal Enfield Madrid Sur</title>'
            f'<link>{SITE}/blog/</link><atom:link href="{SITE}/blog/feed.xml" rel="self" type="application/rss+xml"/>'
            f'<description>Motos, rutas y consejos. Royal Enfield Madrid Sur, concesionario oficial Royal Enfield en Móstoles.</description>'
            f'<language>es-ES</language><lastBuildDate>{last}</lastBuildDate>{items}</channel></rss>\n')

FILLS_DIR = os.path.join(ROOT, "_build", "blog", "posts")

def blog_rerender(tpl, posts):
    """Vuelve a generar cada artículo con la plantilla actual a partir de sus datos (_build/blog/posts/<slug>.json)."""
    band = cta_band("Tu nueva Royal Enfield", "Ven a verla y pruébala en Royal Enfield Madrid Sur, en Móstoles.")
    n = 0
    for p in posts:
        fp = os.path.join(FILLS_DIR, p["slug"] + ".json")
        if not os.path.exists(fp): continue
        fills = json.load(open(fp, encoding="utf-8"))
        fills["%%RELACIONADOS%%"] = blog_relacionados(p, posts)
        fills["%%CTA_BAND%%"] = band
        html_ = tpl
        for k, v in fills.items(): html_ = html_.replace(k, v)
        faltan = re.findall(r"%%[A-Z_]+%%", html_)
        if faltan: raise SystemExit(f"{p['slug']}: faltan marcadores {faltan}")
        write(f"/blog/{p['slug']}/", html_); n += 1
    return n

def page_blog():
    os.makedirs(os.path.join(ROOT, "_build", "blog"), exist_ok=True)
    tpl_idx = blog_index_template()
    tpl_art = blog_article_template()
    open(os.path.join(ROOT, "_build", "blog", "plantilla-indice.html"), "w", encoding="utf-8").write(tpl_idx)
    open(os.path.join(ROOT, "_build", "blog", "plantilla-articulo.html"), "w", encoding="utf-8").write(tpl_art)
    open(os.path.join(ROOT, "_build", "blog", "cta-band.html"), "w", encoding="utf-8").write(cta_band("Tu nueva Royal Enfield", "Ven a verla y pruébala en Royal Enfield Madrid Sur, en Móstoles."))
    posts = sorted(blog_posts(), key=lambda p: p["fecha"], reverse=True)
    os.makedirs(BLOG_DIR, exist_ok=True)
    open(os.path.join(BLOG_DIR, "index.html"), "w", encoding="utf-8").write(tpl_idx.replace("%%LISTADO%%", blog_listado(posts)))
    open(os.path.join(BLOG_DIR, "feed.xml"), "w", encoding="utf-8").write(blog_feed(posts))
    if not os.path.exists(POSTS_JSON):
        open(POSTS_JSON, "w", encoding="utf-8").write("[]\n")
    print("artículos regenerados:", blog_rerender(tpl_art, posts))

# ------------------------------------------------------------------ HOME
SERVICIOS = [("Taller especializado", "Revisiones periodicas y anuales con sello oficial y garantía", "Mantenimiento-anual-completo"),
             ("Accesorios originales", "Servicios oficiales para mantener siempre tu moto al día", "Asesoramiento-comercial-de-motos"),
             ("Recambios originales", "¿Quieres un poquito más? Instalamos tus accesorios originales", "Recambios-originales"),
             ("Servicio Postventa", "Acompañamos a nuestros clientes durante todo el camino con su moto", "Postventa"),
             ("Asesoramiento comercial", "Amplio equipo comercial para ayudarte a elegir la moto ideal para ti", "Asesor-comercial-de-motos")]
BENEFICIOS = [("Oficial", "Concesionario Oficial Royal Enfield", "Disfruta de todas las ventajas y garantías que te ofrecemos como Concesionario oficial Royal Enfield en Madrid"),
              ("Especialistas", "Taller especializado", "Disponemos de los mejores mecánicos especializados para la puesta a punto, revisión y/o reparación de tu moto."),
              ("A medida", "Financiación a tu medida", "Te financiamos tu nueva moto con o sin entrada, con los plazos que quieras y con las mejores condiciones")]

def stats_html():
    return f"""<div class="stats">
        <div class="stat reveal"><b>+<span data-count="20">20</span></b><span>Profesionales dedicados a ti</span></div>
        <div class="stat reveal reveal-d1"><b>+<span data-count="50">50</span></b><span>Años de experiencia y dedicación</span></div>
        <div class="stat reveal reveal-d2"><b>+<span data-count="1200">1200</span> m²</b><span>De exposición en Madrid Sur</span></div>
        <div class="stat reveal reveal-d3"><b>4.8</b><span>+700 vecinos de Madrid Sur satisfechos · <a href="{GMAPS}" target="_blank" rel="noopener">Google</a></span></div>
      </div>"""

def page_home():
    slides = "".join(f'<div class="hero__slide{" is-active" if i == 0 else ""}"><img src="/assets/img/hero/royal-enfield-madrid-sur-{i+1}.webp" alt="" width="1600" height="900"{"" if i == 0 else " loading=\"lazy\""}></div>' for i in range(3))
    textos = "".join(f'''<div class="hero__txt{" is-active" if i == 0 else ""}" data-slide="{i}"{"" if i == 0 else " hidden"}>
          <span class="eyebrow">{t}</span>
          {"<h1>" if i == 0 else "<h2 class='h1'>"}{h}{"</h1>" if i == 0 else "</h2>"}
          <p class="lead">{d}</p>
          <div class="hero__actions"><a class="btn btn--primary" href="#gama">Descubre tu modelo</a><a class="btn btn--ghost-light" href="/solicitud-de-prueba/">Solicita una prueba</a></div>
        </div>''' for i, (t, h, d) in enumerate(BENEFICIOS))
    counts = {f: sum(1 for m in M if m["family"] == f) for f, _, _ in FAMS}
    bar = '<button class="active" data-filter="Todas">Todas <small>' + str(len(M)) + '</small></button>' + "".join(
        f'<button data-filter="{f}">{n} <small>{counts[f]}</small></button>' for f, n, _ in FAMS)
    cards = "\n".join(card(m) for m in M)
    serv = "".join(f'''<div class="serv reveal"><img src="/assets/img/servicios/{img.lower()}.webp" alt="" width="600" height="600" loading="lazy" decoding="async"><h3>{t}</h3><p>{d}</p></div>''' for t, d, img in SERVICIOS)
    gal = "".join(f'<figure><img src="/assets/img/galeria/royal-enfield-galeria-{i+1}.webp" alt="Royal Enfield" width="800" height="450" loading="lazy" decoding="async"></figure>' for i in range(9))
    ld = [DEALER, {"@context": "https://schema.org", "@type": "WebSite", "name": "Royal Enfield Madrid Sur", "url": SITE + "/", "inLanguage": "es-ES", "publisher": {"@id": DEALER_ID}},
          {"@context": "https://schema.org", "@type": "ItemList", "name": "Gama Royal Enfield", "itemListElement": [
              {"@type": "ListItem", "position": i + 1, "url": SITE + model_url(m), "name": full(m)} for i, m in enumerate(M)]}]
    body = f"""
  <section class="hero hero--re" aria-label="Royal Enfield Madrid Sur">
    <div class="hero__slides">{slides}</div>
    <div class="wrap"><div class="hero__inner">{textos}</div></div>
    <div class="wrap" style="position:relative"><div class="hero__dots" role="tablist" aria-label="Imágenes">{"".join(f'<button aria-label="{t}"{" class=\"is-active\"" if i == 0 else ""}></button>' for i, (t, h, d) in enumerate(BENEFICIOS))}</div></div>
  </section>

  <section class="trust trust--re" aria-label="Royal Enfield Madrid Sur">
    <div class="wrap">
      <div class="trust__item"><span class="trust__ico">{ICO["shield"]}</span><span><b>Oficial</b>Concesionario Royal Enfield</span></div>
      <div class="trust__item"><span class="trust__ico">{ICO["wrench"]}</span><span><b>Especialistas</b>Taller especializado</span></div>
      <div class="trust__item"><span class="trust__ico">{ICO["euro"]}</span><span><b>A medida</b>Financiación con o sin entrada</span></div>
      <div class="trust__item"><span class="trust__ico">{ICO["star"]}</span><span><b>4.8 en Google</b>+700 vecinos satisfechos</span></div>
    </div>
  </section>

  <section class="section" id="gama">
    <div class="wrap">
      <span class="eyebrow" style="display:flex;justify-content:center">Royal Enfield Madrid Sur</span>
      <h2>Descubre tu modelo</h2>
      <div class="cat-bar" id="cat-bar" role="group" aria-label="Filtrar por gama">{bar}</div>
      <div class="grid" id="models-grid">
{cards}
      </div>
      <p class="promo-legal">{PRICE_NOTE}</p>
    </div>
  </section>

  {marquee([m["name"] for m in M])}
  <section class="section section--dark">
    <div class="wrap">
      <div class="servs">{serv}</div>
    </div>
  </section>

  <section class="regal" aria-label="Galería">{gal}</section>

  <section class="section">
    <div class="wrap split">
      <figure class="story__img reveal"><img src="/assets/img/empresa/royal-enfield-duomo.webp" alt="Royal Enfield en Duomo Motor Bikes" width="1024" height="576" loading="lazy" decoding="async"></figure>
      <div class="prose reveal reveal-d1">
        <span class="eyebrow">Sobre nosotros</span>
        <h2>Duomo Motor Bikes, concesionario Royal Enfield en Madrid</h2>
        <p>En Duomo Motor Bikes compartimos la misma filosofía que define a Royal Enfield: pasión por la innovación, el diseño y la evolución constante en el mundo de las motocicletas.</p>
        <p>Una amplia exposición con <b>más de 100 motocicletas</b> donde podrás descubrir la <b>gama completa de Royal Enfield</b>, con taller propio especializado, servicio postventa, recambios originales y boutique para el motorista.</p>
        <div class="hero__actions"><a class="btn btn--dark" href="/concesionario-royal-enfield-en-madrid-sur/">Conócenos</a><a class="btn btn--ghost" href="/solicitud-de-prueba/">Solicita una prueba</a></div>
      </div>
    </div>
  </section>



  <section class="section">
    <div class="wrap">{stats_html()}</div>
  </section>

  <section class="section section--alt">
    <div class="wrap">{visit_block()}</div>
  </section>
  {cta_band()}
"""
    write("/", head("Royal Enfield Madrid Sur · Concesionario Oficial de Royal Enfield en Madrid Sur",
                    f"Concesionario oficial Royal Enfield en Móstoles: toda la gama Royal Enfield desde {eur(precio_min())}, taller especializado, financiación a tu medida y prueba.",
                    "/", ld=ld, preload="/assets/img/hero/royal-enfield-madrid-sur-1.webp") + header("inicio") + body + footer())

# ------------------------------------------------------------------ MODELO
def page_model(m):
    fn = full(m); url = model_url(m); q = quote(m["name"])
    tabs = "".join(f'<button class="ctab{" active" if i == 0 else ""}" type="button" role="tab" aria-selected="{"true" if i == 0 else "false"}" data-color="{i}">{e(c["name"])}</button>' for i, c in enumerate(m["colors"]))
    panes = ""
    for i, c in enumerate(m["colors"]):
        im = c["img"]
        panes += f"""<div class="cpane{" active" if i == 0 else ""}" data-color="{i}"{"" if i == 0 else " hidden"}>
          <figure class="cpane__big"><img src="/{im["img"]}" alt="{e(fn)} {e(c["name"])}" width="{im["w"]}" height="{im["h"]}" loading="lazy" decoding="async"></figure>
          <p class="cpane__price"><span>{e(c["name"])}</span> <b>{eur(c["price"])}</b></p>
        </div>"""
    prices = "".join(f'<li><span>{e(c["name"])}</span><b>{eur(c["price"])}</b></li>' for c in m["colors"])
    equip = "".join(f"""<div class="ecard reveal">{f'<img src="/{q_["img"]["img"]}" alt="{e(fn)}: {e(q_["title"].lower())}" width="{q_["img"]["w"]}" height="{q_["img"]["h"]}" loading="lazy" decoding="async">' if q_["img"] else ''}<div class="ecard__body"><h3>{e(q_["title"])}</h3>{f'<p>{e(q_["text"])}</p>' if q_["text"] else ''}</div></div>""" for q_ in m["equip"])
    gal = "".join(f'<figure><img src="/{g["img"]}" alt="{e(fn)} · foto {i+1}" width="{g["w"]}" height="{g["h"]}" loading="lazy" decoding="async"></figure>' for i, g in enumerate(m["gallery"]))
    mot = m["motor"]
    motor = f"""<section class="section">
    <div class="wrap split">
      {f'<figure class="story__img" style="background:transparent;box-shadow:none"><img src="/{mot["img"]["img"]}" alt="Motor de la {e(fn)}" width="{mot["img"]["w"]}" height="{mot["img"]["h"]}" loading="lazy" decoding="async"></figure>' if mot["img"] else ''}
      <div class="prose reveal"><span class="eyebrow">{e(mot["tagline"] or "Motor | " + m["name"])}</span><p class="lead">{e(mot["text"])}</p></div>
    </div>
  </section>""" if mot["text"] else ""
    others = sorted([x for x in M if x["family"] == m["family"] and x["slug"] != m["slug"]], key=lambda x: abs(x["price"] - m["price"]))[:3]
    hero = m["hero"]
    manual = f'<a class="lnk" href="/{m["manual"]}" target="_blank" rel="noopener" download>Descargar (PDF)</a>' if m["manual"] else f'<a class="lnk" href="/contacto/?modelo={q}#solicita">Pídenosla</a>'
    product = {"@context": "https://schema.org", "@type": ["Product", "Motorcycle"], "name": fn, "sku": m["slug"],
               "brand": {"@type": "Brand", "name": "Royal Enfield"}, "image": [SITE + "/" + c["img"]["img"] for c in m["colors"]],
               "description": mot["text"] or f"{fn} en Royal Enfield Madrid Sur.", "color": [c["name"] for c in m["colors"]],
               "offers": {"@type": "AggregateOffer", "url": SITE + url, "priceCurrency": "EUR", "lowPrice": str(min(c["price"] for c in m["colors"])),
                          "highPrice": str(max(c["price"] for c in m["colors"])), "offerCount": str(len(m["colors"])),
                          "availability": "https://schema.org/InStoreOnly", "seller": {"@id": DEALER_ID}}}
    crumbs = [("Inicio", "/"), ("Motocicletas", "/#gama"), (m["name"], url)]
    body = f"""
  <section class="mhero-re" style="--bg:url('/{hero["img"]}')">
    <div class="wrap">
      <span class="eyebrow">Royal Enfield</span>
      <h1>{e(m["name"])}</h1>
      <p class="mhero-re__price">Desde <b>{eur(m["price"])}</b></p>
      <div class="hero__actions"><a class="btn btn--primary" href="/solicitud-de-prueba/?modelo={q}">Solicita una prueba</a><a class="btn btn--ghost-light" href="#colores">Ver colores y precios</a></div>
    </div>
  </section>
  {crumbs_html(crumbs)}
  {motor}
  <section class="section" id="colores">
    <div class="wrap">
      <span class="eyebrow" style="display:flex;justify-content:center">Colores</span>
      <h2>{e(fn)}</h2>
      <div class="ctabs" role="tablist">{tabs}</div>
      <div class="cpanes">{panes}</div>
      <ul class="pricelist">{prices}</ul>
      <p class="promo-legal">{PRICE_NOTE}</p>
    </div>
  </section>
  <section class="section section--alt">
    <div class="wrap">
      <h2>Equipamiento</h2>
      <div class="ecards">{equip}</div>
    </div>
  </section>
  {f'<section class="section"><div class="wrap"><h2>Galería</h2><div class="mgallery">{gal}</div></div></section>' if gal else ''}
  <section class="section section--alt">
    <div class="wrap">
      <div class="info-cards" style="margin-top:0">
        <div class="reveal"><h3>Ficha técnica</h3><p>Descarga la ficha técnica de tu {e(m["name"])}.</p>{manual}</div>
        <div class="reveal reveal-d1"><h3>Solicita una prueba</h3><p>Prueba la {e(fn)} en Royal Enfield Madrid Sur.</p><a class="lnk" href="/solicitud-de-prueba/?modelo={q}">Solicitar prueba</a></div>
        <div class="reveal reveal-d2"><h3>Contáctanos</h3><p>Disponibilidad, financiación y accesorios.</p><a class="lnk" href="/contacto/?modelo={q}#solicita">Contactar</a></div>
      </div>
    </div>
  </section>
  {f'<section class="section"><div class="wrap"><h2>Más de la gama {m["family"]}</h2><div class="grid">{"".join(card(x) for x in others)}</div></div></section>' if others else ''}
  {cta_band(f"Prueba la {e(fn)}", "Solicita tu prueba en Royal Enfield Madrid Sur, en Móstoles.")}
"""
    meta = f"{fn} desde {eur(m['price'])} en Royal Enfield Madrid Sur. {mot['text']}" if mot["text"] else f"{fn} desde {eur(m['price'])} en Royal Enfield Madrid Sur: colores, precios, equipamiento y prueba en Móstoles."
    if len(meta) > 160: meta = meta[:157].rsplit(" ", 1)[0] + "…"
    write(url, head(f"{fn} · Royal Enfield Madrid Sur", meta, url, og_img="/" + m["og"], ld=[product, crumbs_ld(crumbs)], preload="/" + hero["img"]) + header("modelos") + body + footer())

# ------------------------------------------------------------------ NOSOTROS
def page_nosotros():
    url = "/concesionario-royal-enfield-en-madrid-sur/"
    crumbs = [("Inicio", "/"), ("Nosotros", url)]
    body = f"""
  <section class="hero hero--page">
    <div class="hero__bg"><img src="/assets/img/empresa/concesionario-duomo-motor-bikes.webp" alt="" width="1600" height="900"></div>
    <div class="wrap"><div class="hero__inner">
      <span class="eyebrow">Sobre nosotros</span>
      <h1>Duomo Motor Bikes — Concesionario Royal Enfield en Madrid</h1>
    </div></div>
  </section>
  {crumbs_html(crumbs)}
  <section class="section" style="padding-top:36px">
    <div class="wrap split">
      <div class="prose reveal">
        <p>En Duomo Motor Bikes compartimos la misma filosofía que define a Royal Enfield: pasión por la innovación, el diseño y la evolución constante en el mundo de las motocicletas.</p>
        <p>Somos un <b>concesionario oficial multimarca ubicado en Móstoles (Madrid)</b>, especializado en motos de media cilindrada y en ofrecer a cada motorista una experiencia completa, cercana y profesional.</p>
        <p>Nuestra historia nace de una auténtica pasión por el motor y de una sólida tradición familiar en automoción que se remonta a <b>1960</b>. Décadas de experiencia que nos han permitido construir una base de conocimiento, compromiso y confianza con nuestros clientes.</p>
        <p>En <b>2020</b> iniciamos una nueva etapa centrada exclusivamente en las dos ruedas con la creación de <b>Duomo Motor Bikes</b>, reuniendo un equipo altamente cualificado preparado para asesorarte en cada paso: desde la elección de tu moto hasta su mantenimiento y personalización.</p>
        <p>Hoy ponemos a tu disposición una amplia exposición con <b>más de 100 motocicletas</b>, donde podrás descubrir la <b>gama completa de Royal Enfield</b>, junto a otras marcas referentes como <a href="https://voge.duomomotor.com/">Voge</a> y <a href="https://zontes.duomomotor.com/">Zontes</a>. Una selección pensada para adaptarse a diferentes estilos de conducción, necesidades y niveles de experiencia.</p>
        <p>Pero nuestra relación contigo no termina con la compra. En nuestras instalaciones también encontrarás:</p>
        <ul><li>Taller propio especializado</li><li>Servicio postventa</li><li>Recambios originales y neumáticos</li><li>Boutique con equipamiento para el motorista</li></ul>
        <p>Todo ello para ofrecerte un <b>servicio integral</b>, cómodo y seguro, antes, durante y después de tu compra.</p>
        <p>En Duomo Motor Bikes creemos que una moto no es solo un vehículo: es una forma de vivir la carretera.</p>
        <p>Por eso trabajamos cada día para ofrecerte la mejor experiencia como motorista y ayudarte a encontrar <b>la Royal Enfield perfecta para ti</b>.</p>
      </div>
      <figure class="story__img reveal reveal-d1"><img src="/assets/img/empresa/royal-enfield-duomo.webp" alt="Royal Enfield en Duomo Motor Bikes" width="1024" height="576" loading="lazy" decoding="async"></figure>
    </div>
  </section>
  <section class="section section--alt"><div class="wrap">{stats_html()}</div></section>
  <section class="section"><div class="wrap">{visit_block()}</div></section>
  {cta_band()}
"""
    write(url, head("Concesionario Royal Enfield en Madrid Sur · Duomo Motor Bikes",
                    "Duomo Motor Bikes, concesionario oficial Royal Enfield en Móstoles (Madrid): exposición con más de 100 motos, taller propio, postventa, recambios y boutique.",
                    url, ld=[DEALER, crumbs_ld(crumbs)]) + header("nosotros") + body + footer())

# ------------------------------------------------------------------ FORMULARIOS
def model_select():
    out = '<option value="">Selecciona un modelo…</option>'
    for f, n, _ in FAMS:
        out += f'<optgroup label="{n}">' + "".join(f'<option>{e(m["name"])}</option>' for m in M if m["family"] == f) + "</optgroup>"
    return out + '<option>Aún no lo sé</option>'

def form(tipo):
    prueba = tipo == "prueba"
    subject = "Solicitud de PRUEBA web Royal Enfield · Duomo Motor" if prueba else "Nueva solicitud web Royal Enfield · Duomo Motor"
    extra = """<div class="field">
              <label for="fecha">¿Qué día te viene mejor?</label>
              <input id="fecha" name="dia_preferido" placeholder="Ej.: martes por la tarde">
            </div>""" if prueba else ""
    return f"""<form class="form" id="contact-form" action="https://formsubmit.co/{NEGOCIO["email"]}" method="POST" novalidate>
            <input type="hidden" name="_subject" value="{subject}">
            <input type="hidden" name="_template" value="table">
            <input type="hidden" name="_captcha" value="false">
            <input type="hidden" name="tipo_solicitud" value="{"Prueba de moto" if prueba else "Información"}">
            <input type="hidden" name="departamento" value="Ventas">
            <input type="hidden" name="marca" value="Royal Enfield">
            <input type="text" name="_honey" style="display:none" tabindex="-1" autocomplete="off" aria-hidden="true">
            <div class="field">
              <label for="modelo">Modelo de interés{'*' if prueba else ''}</label>
              <select id="modelo" name="modelo"{' required' if prueba else ''}>{model_select()}</select>
            </div>
            <div class="field--row">
              <div class="field"><label for="nombre">Nombre*</label><input id="nombre" name="nombre" required autocomplete="name"></div>
              <div class="field"><label for="tel">Teléfono*</label><input id="tel" name="telefono" type="tel" required autocomplete="tel" inputmode="tel"></div>
            </div>
            <div class="field"><label for="mail">Email*</label><input id="mail" name="email" type="email" required autocomplete="email"></div>
            {extra}
            <div class="field">
              <label for="msg">Mensaje</label>
              <textarea id="msg" name="mensaje"></textarea>
            </div>
            <label class="check">
              <input type="checkbox" name="acepta_privacidad" value="Sí" required>
              <span>Acepto las <a href="/politicas-de-privacidad/" target="_blank">Políticas de Privacidad</a>.*</span>
            </label>
            <button class="btn btn--primary" type="submit">{"Solicitar prueba" if prueba else "Enviar información"}</button>
            <p class="form__note">* Campos obligatorios. Responsable: {NEGOCIO["razon"]}. Finalidad: responder a tu solicitud. Derechos: acceso, rectificación y supresión en {NEGOCIO["email"]}.</p>
            <div class="form-status" id="form-status" role="status" aria-live="polite" hidden></div>
          </form>"""

def page_form(tipo):
    prueba = tipo == "prueba"
    url = "/solicitud-de-prueba/" if prueba else "/contacto/"
    h1 = "Solicita una prueba" if prueba else "Contacta con los que más saben de Royal Enfield"
    lead = ("Elige tu Royal Enfield y te confirmamos día y hora para probarla en Móstoles." if prueba
            else "Contacta con el equipo de Royal Enfield en Madrid Sur y déjate encantar por especialistas que te ayudarán a encontrar lo que buscas.")
    crumbs = [("Inicio", "/"), ("Solicitud de prueba" if prueba else "Contacto", url)]
    body = f"""
  <section class="hero hero--page">
    <div class="hero__bg"><img src="/assets/img/hero/royal-enfield-madrid-sur-{3 if prueba else 2}.webp" alt="" width="1600" height="900"></div>
    <div class="wrap"><div class="hero__inner">
      <span class="eyebrow">Royal Enfield Madrid Sur</span>
      <h1>{h1}</h1>
      <p class="lead">{lead}</p>
    </div></div>
  </section>
  {crumbs_html(crumbs)}
  <section class="section" id="solicita" style="padding-top:36px">
    <div class="wrap">
      <div class="contact-grid">
        <div class="reveal">{form(tipo)}</div>
        <div class="info-card reveal">
          <div class="info-item"><div class="info-item__ico">{ICO["pin"]}</div><div><h3>Duomo Motor Bikes</h3><p>{e(DIRECCION)}</p></div></div>
          <div class="info-item"><div class="info-item__ico">{ICO["tel"]}</div><div><h3>Teléfono</h3><a href="tel:{NEGOCIO["telIntl"]}">{NEGOCIO["tel"]}</a></div></div>
          <div class="info-item"><div class="info-item__ico">{ICO["wa"]}</div><div><h3>WhatsApp</h3><a href="https://wa.me/{WHATSAPP}" target="_blank" rel="noopener">{WHATSAPP_TXT}</a></div></div>
          <div class="info-item"><div class="info-item__ico">{ICO["mail"]}</div><div><h3>Email</h3><a href="mailto:{NEGOCIO["email"]}">{NEGOCIO["email"]}</a></div></div>
          <div class="info-item"><div class="info-item__ico">{ICO["star"]}</div><div><h3>4.8 en Google</h3><p>+700 vecinos de Madrid Sur satisfechos</p></div></div>
          <iframe class="map-embed" src="{MAPS_EMBED}" loading="lazy" referrerpolicy="no-referrer-when-downgrade" title="Mapa de Royal Enfield Madrid Sur"></iframe>
        </div>
      </div>
    </div>
  </section>
"""
    title = "Solicitud de prueba · Royal Enfield Madrid Sur" if prueba else "Contacto · Royal Enfield Madrid Sur"
    meta = ("Solicita una prueba de cualquier Royal Enfield (Classic 350, Himalayan 450, Interceptor 650…) en Royal Enfield Madrid Sur, en Móstoles."
            if prueba else f"Contacta con Royal Enfield Madrid Sur (Duomo Motor Bikes, Móstoles): teléfono {NEGOCIO['tel']}, WhatsApp {WHATSAPP_TXT} y formulario.")
    write(url, head(title, meta, url, ld=[crumbs_ld(crumbs), DEALER]) + header("contacto" if not prueba else "") + body + footer())

# ------------------------------------------------------------------ SEO
def bloque_blog(*a, **k): return ""

def seo_files():
    urls = [("/", "1.0", "weekly"), ("/concesionario-royal-enfield-en-madrid-sur/", "0.8", "monthly"),
            ("/solicitud-de-prueba/", "0.7", "monthly"), ("/contacto/", "0.7", "monthly")]
    urls += [(model_url(m), "0.9", "weekly") for m in M]
    posts = sorted(blog_posts(), key=lambda p: p["fecha"], reverse=True)
    urls += [("/blog/", "0.8", "daily")] + [(f"/blog/{p['slug']}/", "0.7", "monthly") for p in posts]
    fechas = {f"/blog/{p['slug']}/": p["fecha"] for p in posts}
    if posts: fechas["/blog/"] = posts[0]["fecha"]
    xml = ['<?xml version="1.0" encoding="UTF-8"?>', '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9" xmlns:image="http://www.google.com/schemas/sitemap-image/1.1">']
    for u, p, f in urls:
        imgs = ""
        m = next((x for x in M if model_url(x) == u), None)
        if m: imgs = "".join(f"<image:image><image:loc>{SITE}/{c['img']['img']}</image:loc></image:image>" for c in m["colors"])
        bp = next((x for x in posts if f"/blog/{x['slug']}/" == u), None)
        if bp: imgs = f"<image:image><image:loc>{SITE}{bp['imagen']}</image:loc></image:image>"
        xml.append(f"  <url><loc>{SITE}{u}</loc><lastmod>{fechas.get(u, TODAY)}</lastmod><changefreq>{f}</changefreq><priority>{p}</priority>{imgs}</url>")
    xml.append("</urlset>")
    open(os.path.join(ROOT, "sitemap.xml"), "w", encoding="utf-8").write("\n".join(xml) + "\n")
    open(os.path.join(ROOT, "robots.txt"), "w", encoding="utf-8").write(f"User-agent: *\nAllow: /\nDisallow: /_build/\n\nSitemap: {SITE}/sitemap.xml\n")
    open(os.path.join(ROOT, f"{INDEXNOW_KEY}.txt"), "w", encoding="utf-8").write(INDEXNOW_KEY)
    gama = "\n".join(f"- [{full(m)}]({SITE}{model_url(m)}): gama {m['family']}, desde {eur(m['price'])} ({', '.join(c['name'] + ' ' + eur(c['price']) for c in m['colors'])})" for m in M)
    blog = "\n".join(f"- [{p['titulo']}]({SITE}/blog/{p['slug']}/)" for p in posts[:20])
    open(os.path.join(ROOT, "llms.txt"), "w", encoding="utf-8").write(f"""# Royal Enfield Madrid Sur · Duomo Motor Bikes

> Concesionario oficial Royal Enfield en Móstoles (Madrid). Venta de motos Royal Enfield nuevas, prueba, financiación, taller especializado, accesorios y recambios originales y servicio postventa.

- Dirección: {DIRECCION}
- Teléfono: {NEGOCIO['tel']} · WhatsApp: {WHATSAPP_TXT}
- Email: {NEGOCIO['email']}
- Valoración: 4.8 en Google (+700 reseñas)

## Páginas principales
- [Inicio]({SITE}/)
- [Nosotros]({SITE}/concesionario-royal-enfield-en-madrid-sur/)
- [Solicitud de prueba]({SITE}/solicitud-de-prueba/)
- [Contacto]({SITE}/contacto/)

## Gama Royal Enfield (PVP con IVA, precio por color)
{gama}

## Blog
{blog}
""")
    open(os.path.join(ROOT, "site.webmanifest"), "w", encoding="utf-8").write(json.dumps({
        "name": "Royal Enfield Madrid Sur · Duomo Motor Bikes", "short_name": "Royal Enfield Madrid Sur", "start_url": "/", "display": "browser",
        "background_color": "#111111", "theme_color": "#111111",
        "icons": [{"src": "/assets/img/logo/icon-192.png", "sizes": "192x192", "type": "image/png"},
                  {"src": "/assets/img/logo/icon-512.png", "sizes": "512x512", "type": "image/png"}]}, ensure_ascii=False, indent=1))

if __name__ == "__main__":
    page_home()
    for m in M: page_model(m)
    page_nosotros(); page_form("contacto"); page_form("prueba")
    for u, (t, s, cnt) in LEGAL.items(): page_legal(u, t, s, cnt)
    page_blog(); page_404(); seo_files()
    print(f"OK · {len(M)} modelos")
