# LF Uniformes — código-fonte do site

- `site/` — fonte da home (index.html, assets/css/style.css, assets/js/main.js, img/, robots, llms, .htaccess)
- `gerador/gerar_paginas.py` — gera as páginas de segmento (hospitais, clínicas, escolas)
- `gerador/gerar_blog.py` — gera o blog a partir dos artigos em `artigos/*.md`
- `artigos/` — um arquivo .md por artigo aprovado (formato do briefing do blog)

## Gerar a pasta de publicação

    python3 gerador/gerar_paginas.py site publicar
    python3 gerador/gerar_blog.py site artigos publicar

A home publicada é o site/index.html com o CSS e o JS embutidos.
Artigos com data futura só entram quando a data chegar (basta rodar o gerador de novo).

## Leads dos materiais do blog

Em site/assets/js/main.js, preencha LEAD_WEBHOOK com a URL de um webhook (n8n) para receber
nome, empresa, WhatsApp, e-mail, material e artigo. Vazio = abre o WhatsApp da LF com o pedido.

## Branches

- `main` — site publicado. A Hostinger faz o deploy desta branch em `public_html`. Não editar à mão.
- `fonte` — este código-fonte. Alterações são feitas aqui, o site é gerado em `publicar/` e o conteúdo vai para a `main`.

## Build

    python3 gerador/build.py publicar

Gera a pasta `publicar/` completa (home, 404, segmentos, privacidade, blog, sitemap e arquivos estáticos). O conteúdo dela é o que vai para a branch `main`.
