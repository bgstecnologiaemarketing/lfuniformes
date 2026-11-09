"""Gera o blog da LF Uniformes a partir dos artigos em Markdown (com front matter).

Uso: python3 gerar_blog.py <pasta-fonte-site> <pasta-artigos> <pasta-publicacao>
Cada artigo aprovado é um arquivo .md em <pasta-artigos>, no formato do briefing.
"""
import html
import json
import os
import re
import sys
from datetime import date

import markdown
import yaml

sys.path.insert(0, os.path.dirname(__file__))
from gerar_paginas import CABECALHO, RODAPE, WA_FLUTUANTE, wa_link  # noqa: E402

SITE, ARTIGOS, SAIDA = sys.argv[1], sys.argv[2], sys.argv[3]
BASE = "https://lfuniformes.com.br"
HOJE = date.today().isoformat()

css = open(os.path.join(SITE, "assets/css/style.css"), encoding="utf-8").read()
js = open(os.path.join(SITE, "assets/js/main.js"), encoding="utf-8").read()

CATEGORIAS = {
    "aplicacoes": "Aplicações por segmento",
    "escolha": "Como escolher",
    "cuidados": "Cuidados com o uniforme",
    "gestao": "Gestão do uniforme",
}

MATERIAIS = {
    "guia-cuidados": ("Guia de cuidados com o uniforme", "Um guia para imprimir e entregar à sua equipe, com instruções de lavagem e conservação por tipo de peça."),
    "tabela-medidas": ("Tabela de medidas para a equipe", "A tabela que usamos para definir os tamanhos, pronta para cada colaborador preencher."),
    "checklist-implantacao": ("Checklist para implantar uniforme na empresa", "Os passos para definir modelos, setores, quantidades e regras de uso sem esquecer nada."),
    "planilha-controle": ("Planilha de controle de entrega e reposição", "Controle quem recebeu quais peças, quando e quando repor."),
}

AUTOR = "Equipe LF Uniformes"
REVISOR = "Carlos Alberto dos Santos"

OBRIGATORIOS = ["titulo", "slug", "meta_title", "meta_description", "categoria", "resumo", "material", "data"]


def ler_artigo(caminho):
    texto = open(caminho, encoding="utf-8").read().strip()
    # aceita o bloco colado com ```markdown ... ```
    texto = re.sub(r"^```(?:markdown|md)?\s*\n", "", texto)
    texto = re.sub(r"\n```\s*$", "", texto)
    m = re.match(r"^---\s*\n(.*?)\n---\s*\n(.*)$", texto, re.S)
    if not m:
        raise ValueError(f"{caminho}: front matter (--- ... ---) não encontrado")
    meta = yaml.safe_load(m.group(1)) or {}
    corpo = m.group(2).strip()
    faltando = [c for c in OBRIGATORIOS if not meta.get(c)]
    if faltando:
        raise ValueError(f"{caminho}: campos faltando: {', '.join(faltando)}")
    if meta["categoria"] not in CATEGORIAS:
        raise ValueError(f"{caminho}: categoria inválida '{meta['categoria']}'")
    if meta["material"] not in MATERIAIS and meta["material"] != "orcamento":
        raise ValueError(f"{caminho}: material inválido '{meta['material']}'")
    meta["slug"] = re.sub(r"[^a-z0-9-]", "", str(meta["slug"]).lower())
    meta["data"] = str(meta["data"])
    return meta, corpo


def separar_faq(corpo):
    """Retira a seção '## Perguntas frequentes' e devolve (corpo_sem_faq, [(pergunta, resposta_md)])."""
    m = re.search(r"^##\s+Perguntas frequentes\s*$", corpo, re.M | re.I)
    if not m:
        return corpo, []
    antes, faq_txt = corpo[: m.start()].rstrip(), corpo[m.end():]
    itens = []
    for bloco in re.split(r"^###\s+", faq_txt, flags=re.M)[1:]:
        linhas = bloco.strip().split("\n", 1)
        pergunta = linhas[0].strip()
        resposta = linhas[1].strip() if len(linhas) > 1 else ""
        itens.append((pergunta, resposta))
    return antes, itens


def md_para_html(txt):
    h = markdown.markdown(txt, extensions=["tables", "sane_lists"])
    h = h.replace("<table>", '<div class="tabela-rolagem"><table>').replace("</table>", "</table></div>")
    return h


def texto_puro(md_txt):
    return re.sub(r"<[^>]+>", "", markdown.markdown(md_txt)).strip()


def bloco_material(meta):
    if meta["material"] == "orcamento":
        return f"""<aside class="material">
  <h2>Quer saber quanto fica para a sua equipe?</h2>
  <p>Conte quantos colaboradores e quais setores quer uniformizar. Respondemos em 1 a 2 dias.</p>
  <a class="btn btn--claro" href="/#orcamento">Pedir orçamento</a>
</aside>"""
    titulo, desc = MATERIAIS[meta["material"]]
    return f"""<aside class="material" aria-labelledby="mat-titulo">
  <h2 id="mat-titulo">Receba grátis: {html.escape(titulo)}</h2>
  <p>{html.escape(desc)}</p>
  <form class="form form-material" data-material="{meta['material']}" data-material-titulo="{html.escape(titulo)}" novalidate>
    <div class="campo campo--meia"><label for="m-nome">Seu nome</label><input id="m-nome" name="nome" autocomplete="name" required></div>
    <div class="campo campo--meia"><label for="m-empresa">Empresa</label><input id="m-empresa" name="empresa" autocomplete="organization" required></div>
    <div class="campo campo--meia"><label for="m-zap">WhatsApp com DDD</label><input id="m-zap" name="whatsapp" type="tel" autocomplete="tel" inputmode="tel" required></div>
    <div class="campo campo--meia"><label for="m-email">E-mail (opcional)</label><input id="m-email" name="email" type="email" autocomplete="email"></div>
    <p class="form__erro" role="alert" hidden></p>
    <div class="form__acoes"><button type="submit" class="btn btn--claro">Quero receber</button></div>
  </form>
</aside>"""


def data_br(iso):
    meses = ["janeiro", "fevereiro", "março", "abril", "maio", "junho", "julho", "agosto", "setembro", "outubro", "novembro", "dezembro"]
    a, m, d = iso.split("-")
    return f"{int(d)} de {meses[int(m) - 1]} de {a}"


def head(titulo, descricao, url, ld, extra=""):
    return f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <!-- Consent Mode do Google: tudo negado até o visitante aceitar (antes do GTM) -->
  <script>
  window.dataLayer = window.dataLayer || [];
  function gtag(){{dataLayer.push(arguments);}}
  gtag('consent', 'default', {{
    ad_storage: 'denied',
    ad_user_data: 'denied',
    ad_personalization: 'denied',
    analytics_storage: 'denied',
    wait_for_update: 500
  }});
  try {{
    var lfc = JSON.parse(localStorage.getItem('lf_consentimento') || 'null');
    if (lfc && lfc.valor === 'granted' && lfc.expira_em > Date.now()) {{
      gtag('consent', 'update', {{ad_storage: 'granted', ad_user_data: 'granted', ad_personalization: 'granted', analytics_storage: 'granted'}});
    }}
  }} catch (e) {{}}
  </script>
  <!-- Google Tag Manager -->
  <script>(function(w,d,s,l,i){{w[l]=w[l]||[];w[l].push({{'gtm.start':
  new Date().getTime(),event:'gtm.js'}});var f=d.getElementsByTagName(s)[0],
  j=d.createElement(s),dl=l!='dataLayer'?'&l='+l:'';j.async=true;j.src=
  'https://www.googletagmanager.com/gtm.js?id='+i+dl;f.parentNode.insertBefore(j,f);
  }})(window,document,'script','dataLayer','GTM-PGRMXWQ');</script>
  <!-- End Google Tag Manager -->
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{html.escape(titulo)}</title>
  <meta name="description" content="{html.escape(descricao)}">
  <link rel="canonical" href="{url}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta name="theme-color" content="#051129">
  <meta property="og:locale" content="pt_BR">
  <meta property="og:site_name" content="LF Uniformes">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{html.escape(titulo)}">
  <meta property="og:description" content="{html.escape(descricao)}">
  <meta property="og:image" content="{BASE}/img/og-image.jpg">
  <meta name="twitter:card" content="summary_large_image">{extra}
  <link rel="icon" type="image/png" href="/img/favicon.png">
  <link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
  <link rel="alternate" type="application/rss+xml" title="Blog LF Uniformes" href="{BASE}/blog/feed.xml">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@75..100,400..800&display=swap" rel="stylesheet">
  <style>
{css}
  </style>
  <script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
  </script>
</head>"""


def rodape_pagina(wa):
    return f"""
{RODAPE}

{WA_FLUTUANTE.format(link=wa)}

  <script>
{js}
  </script>
</body>
</html>
"""


def card(meta):
    return f"""        <li class="card">
          <span class="card__cat">{CATEGORIAS[meta['categoria']]}</span>
          <h3><a href="/blog/{meta['slug']}/">{html.escape(meta['titulo'])}</a></h3>
          <p>{html.escape(str(meta['resumo']))}</p>
          <time datetime="{meta['data']}">{data_br(meta['data'])}</time>
        </li>"""


def gerar_artigo(meta, corpo, todos):
    url = f"{BASE}/blog/{meta['slug']}/"
    corpo_sem_faq, faq = separar_faq(corpo)
    partes = corpo_sem_faq.split("[[MATERIAL]]")
    corpo_html = md_para_html(partes[0])
    if len(partes) > 1:
        corpo_html += "\n" + bloco_material(meta) + "\n" + md_para_html("\n".join(partes[1:]))
    else:
        corpo_html += "\n" + bloco_material(meta)

    faq_html = ""
    if faq:
        itens = "\n".join(
            f"        <details><summary>{html.escape(q)}</summary>{md_para_html(r)}</details>" for q, r in faq
        )
        faq_html = f"""
      <h2>Perguntas frequentes</h2>
      <div class="faq">
{itens}
      </div>"""

    grafo = [
        {
            "@type": "BlogPosting",
            "@id": url + "#artigo",
            "headline": meta["titulo"],
            "description": meta["meta_description"],
            "abstract": str(meta["resumo"]),
            "datePublished": meta["data"],
            "dateModified": str(meta.get("atualizado", meta["data"])),
            "inLanguage": "pt-BR",
            "mainEntityOfPage": url,
            "image": f"{BASE}/img/og-image.jpg",
            "keywords": meta.get("palavra_chave", ""),
            "articleSection": CATEGORIAS[meta["categoria"]],
            "author": {"@type": "Organization", "name": "LF Uniformes", "url": f"{BASE}/"},
            "reviewedBy": {"@type": "Person", "name": REVISOR, "worksFor": {"@id": f"{BASE}/#empresa"}},
            "publisher": {"@type": "Organization", "@id": f"{BASE}/#empresa", "name": "LF Uniformes", "logo": {"@type": "ImageObject", "url": f"{BASE}/img/logo.png"}},
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "LF Uniformes", "item": f"{BASE}/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": f"{BASE}/blog/"},
                {"@type": "ListItem", "position": 3, "name": meta["titulo"], "item": url},
            ],
        },
    ]
    if faq:
        grafo.append({
            "@type": "FAQPage",
            "mainEntity": [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": texto_puro(r)}} for q, r in faq],
        })
    ld = {"@context": "https://schema.org", "@graph": grafo}

    relacionados = [a for a in todos if a["slug"] != meta["slug"] and a["categoria"] == meta["categoria"]]
    relacionados += [a for a in todos if a["slug"] != meta["slug"] and a not in relacionados]
    rel_html = ""
    if relacionados:
        rel_html = f"""
    <section class="relacionados" aria-labelledby="rel-titulo">
      <h2 id="rel-titulo">Leia também</h2>
      <ul class="cards">
{chr(10).join(card(a) for a in relacionados[:3])}
      </ul>
    </section>"""

    wa = wa_link(f"Oi, vim pelo blog da LF (artigo: {meta['titulo']}). Gostaria de um orçamento.")
    link_interno = meta.get("link_interno") or "/#orcamento"
    extra = f"""
  <meta property="og:type" content="article">
  <meta property="article:published_time" content="{meta['data']}">
  <meta property="article:section" content="{CATEGORIAS[meta['categoria']]}">"""

    pagina = head(meta["meta_title"], meta["meta_description"], url, {"@context": "https://schema.org", "@graph": grafo}, extra) + f"""
<body>
  <!-- Google Tag Manager (noscript) -->
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-PGRMXWQ" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
  <!-- End Google Tag Manager (noscript) -->
{CABECALHO}

  <nav class="migalhas" aria-label="Você está em">
    <ol><li><a href="/">Início</a></li><li><a href="/blog/">Blog</a></li><li aria-current="page">{html.escape(meta['titulo'])}</li></ol>
  </nav>

  <main id="conteudo">
    <article class="artigo">
      <a class="artigo__cat" href="/blog/#{meta['categoria']}">{CATEGORIAS[meta['categoria']]}</a>
      <h1>{html.escape(meta['titulo'])}</h1>
      <p class="artigo__meta">Por {AUTOR} · Revisão técnica: {REVISOR} · <time datetime="{meta['data']}">{data_br(meta['data'])}</time></p>
      <p class="artigo__resumo">{html.escape(str(meta['resumo']))}</p>
      <div class="artigo__corpo">
{corpo_html}
{faq_html}
      </div>
    </article>

    <section class="artigo-cta">
      <div>
        <h2>Precisa uniformizar a sua equipe?</h2>
        <p>A LF Uniformes confecciona uniformes executivos e profissionais em Curitiba, com modelagem própria e bordado. Orçamento em 1 a 2 dias.</p>
        <div class="hero__ctas">
          <a class="btn" href="{link_interno}">{'Ver como atendemos o seu segmento' if link_interno.startswith('/uniformes-') else 'Pedir orçamento'}</a>
          <a class="btn btn--linha" href="{wa}" target="_blank" rel="noopener" data-wa="artigo">Falar no WhatsApp</a>
        </div>
      </div>
    </section>
{rel_html}
  </main>
""" + rodape_pagina(wa)

    pasta = os.path.join(SAIDA, "blog", meta["slug"])
    os.makedirs(pasta, exist_ok=True)
    open(os.path.join(pasta, "index.html"), "w", encoding="utf-8").write(pagina)


def gerar_indice(todos):
    url = f"{BASE}/blog/"
    grafo = [
        {
            "@type": "Blog",
            "@id": url + "#blog",
            "name": "Blog da LF Uniformes",
            "description": "Guias sobre uniformes profissionais e executivos: aplicações por segmento, como escolher, cuidados e gestão do uniforme.",
            "url": url,
            "inLanguage": "pt-BR",
            "publisher": {"@id": f"{BASE}/#empresa"},
            "blogPost": [{"@type": "BlogPosting", "headline": a["titulo"], "url": f"{url}{a['slug']}/", "datePublished": a["data"]} for a in todos],
        },
        {
            "@type": "BreadcrumbList",
            "itemListElement": [
                {"@type": "ListItem", "position": 1, "name": "LF Uniformes", "item": f"{BASE}/"},
                {"@type": "ListItem", "position": 2, "name": "Blog", "item": url},
            ],
        },
    ]
    secoes = []
    for cod, nome in CATEGORIAS.items():
        arts = [a for a in todos if a["categoria"] == cod]
        if not arts:
            continue
        secoes.append(f"""    <section id="{cod}" class="secao">
      <h2>{nome}</h2>
      <ul class="cards">
{chr(10).join(card(a) for a in arts)}
      </ul>
    </section>""")
    chips = "\n".join(
        f'        <li><a href="#{c}">{n}</a></li>' for c, n in CATEGORIAS.items() if any(a["categoria"] == c for a in todos)
    )
    wa = wa_link("Oi, vim pelo blog da LF! Gostaria de um orçamento.")
    pagina = head(
        "Blog LF Uniformes: guias sobre uniformes profissionais",
        "Guias práticos sobre uniformes profissionais e executivos: como escolher tecidos e modelos, cuidar das peças e implantar o uniforme na sua empresa.",
        url, {"@context": "https://schema.org", "@graph": grafo},
    ) + f"""
<body>
  <!-- Google Tag Manager (noscript) -->
  <noscript><iframe src="https://www.googletagmanager.com/ns.html?id=GTM-PGRMXWQ" height="0" width="0" style="display:none;visibility:hidden"></iframe></noscript>
  <!-- End Google Tag Manager (noscript) -->
{CABECALHO}

  <nav class="migalhas" aria-label="Você está em">
    <ol><li><a href="/">Início</a></li><li aria-current="page">Blog</li></ol>
  </nav>

  <main id="conteudo">
    <header class="blog-cab">
      <h1>Guias sobre uniformes profissionais</h1>
      <p>Como escolher tecidos e modelos, cuidar das peças e implantar o uniforme na sua empresa, com a experiência de quem confecciona.</p>
      <ul class="categorias">
{chips}
      </ul>
    </header>
{chr(10).join(secoes)}
  </main>
""" + rodape_pagina(wa)
    os.makedirs(os.path.join(SAIDA, "blog"), exist_ok=True)
    open(os.path.join(SAIDA, "blog", "index.html"), "w", encoding="utf-8").write(pagina)


def rfc822(iso):
    from email.utils import format_datetime
    from datetime import datetime, timezone, timedelta
    a, m, d = map(int, iso.split("-"))
    return format_datetime(datetime(a, m, d, 9, 0, tzinfo=timezone(timedelta(hours=-3))))


def gerar_feed(todos):
    itens = "\n".join(
        f"""    <item>
      <title>{html.escape(a['titulo'])}</title>
      <link>{BASE}/blog/{a['slug']}/</link>
      <guid>{BASE}/blog/{a['slug']}/</guid>
      <pubDate>{rfc822(a['data'])}</pubDate>
      <description>{html.escape(str(a['resumo']))}</description>
    </item>""" for a in todos
    )
    feed = f"""<?xml version="1.0" encoding="UTF-8"?>
<rss version="2.0">
  <channel>
    <title>Blog LF Uniformes</title>
    <link>{BASE}/blog/</link>
    <description>Guias sobre uniformes profissionais e executivos.</description>
    <language>pt-BR</language>
{itens}
  </channel>
</rss>
"""
    open(os.path.join(SAIDA, "blog", "feed.xml"), "w", encoding="utf-8").write(feed)


def gerar_sitemap(todos):
    urls = [("", HOJE), ("uniformes-para-hospitais/", HOJE), ("uniformes-para-clinicas/", HOJE), ("uniformes-para-escolas/", HOJE), ("privacidade/", HOJE)]
    if todos:
        urls.append(("blog/", max(a["data"] for a in todos)))
        urls += [(f"blog/{a['slug']}/", str(a.get("atualizado", a["data"]))) for a in todos]
    corpo = "\n".join(f"  <url><loc>{BASE}/{u}</loc><lastmod>{d}</lastmod></url>" for u, d in urls)
    open(os.path.join(SAIDA, "sitemap.xml"), "w", encoding="utf-8").write(
        f'<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n{corpo}\n</urlset>\n'
    )


if __name__ == "__main__":
    todos = []
    for nome in sorted(os.listdir(ARTIGOS)):
        if not nome.endswith(".md"):
            continue
        meta, corpo = ler_artigo(os.path.join(ARTIGOS, nome))
        meta["_corpo"] = corpo
        todos.append(meta)
    # só publica artigos com data de hoje ou anterior
    todos = [a for a in todos if a["data"] <= HOJE]
    todos.sort(key=lambda a: a["data"], reverse=True)
    for a in todos:
        gerar_artigo(a, a["_corpo"], todos)
    if todos:
        gerar_indice(todos)
        gerar_feed(todos)
    gerar_sitemap(todos)
    print(f"{len(todos)} artigo(s) publicado(s)")
    for a in todos:
        print(f"  /blog/{a['slug']}/")
