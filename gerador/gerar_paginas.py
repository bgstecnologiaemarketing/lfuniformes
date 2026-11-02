"""Gera as páginas de segmento da LF Uniformes com cabeçalho, rodapé, CSS e JS embutidos."""
import json
import os
import sys

SITE = sys.argv[1]          # pasta com o código-fonte (lf-site)
SAIDA = sys.argv[2]         # pasta de publicação
BASE = "https://lfuniformes.com.br"

css = open(os.path.join(SITE, "assets/css/style.css"), encoding="utf-8").read()
js = open(os.path.join(SITE, "assets/js/main.js"), encoding="utf-8").read()

WA = "5541991697834"


def wa_link(msg):
    from urllib.parse import quote
    return f"https://wa.me/{WA}?text={quote(msg)}"


CABECALHO = """  <a class="skip" href="#conteudo">Pular para o conteúdo</a>
  <header class="topo">
    <div class="topo__in">
      <a href="/" class="marca" aria-label="LF Uniformes, página inicial">
        <img src="/img/logo.png" alt="" width="52" height="52">
        <span class="marca__nome"><strong>LF Uniformes</strong><span>Uniformes executivos</span></span>
      </a>
      <button class="menu-btn" aria-expanded="false" aria-controls="menu">Menu</button>
      <nav id="menu" class="nav" aria-label="Principal">
        <a href="/#linhas">Uniformes</a>
        <a href="/#segmentos">Segmentos</a>
        <a href="/#como-trabalhamos">Como trabalhamos</a>
        <a href="/#clientes">Clientes</a>
        <a href="/#sobre">Sobre</a>
        <a href="#orcamento" class="btn btn--sm">Pedir orçamento</a>
      </nav>
    </div>
  </header>"""

RODAPE = """  <footer class="rodape">
    <div class="rodape__in">
      <div>
        <img class="rodape__logo" src="/img/logo.png" alt="LF Uniformes" width="64" height="64" loading="lazy">
        <p>Uniformes executivos e profissionais para empresas.</p>
        <p class="rodape__cnpj">LF Uniformes Executivos LTDA<br>CNPJ 66.939.750/0001-31</p>
      </div>
      <address>
        LF Uniformes<br>
        R. Luiz França, 1588, Cajuru<br>
        Curitiba, PR, 82940-090<br>
        Seg. a sex., 8h às 18h<br>
        <a href="tel:+554136539065">(41) 3653-9065</a><br>
        <a href="https://wa.me/5541991697834" target="_blank" rel="noopener" data-wa="rodape">WhatsApp (41) 99169-7834</a><br>
        <a href="mailto:comercial@lfuniformes.com.br">comercial@lfuniformes.com.br</a>
      </address>
      <nav aria-label="Rodapé">
        <a href="/">Página inicial</a>
        <a href="/uniformes-para-hospitais/">Uniformes para hospitais</a>
        <a href="/uniformes-para-clinicas/">Uniformes para clínicas</a>
        <a href="/uniformes-para-escolas/">Uniformes para escolas</a>
        <a href="/#perguntas">Perguntas frequentes</a>
      </nav>
    </div>
    <p class="rodape__fim">© <span id="ano">2026</span> LF Uniformes. Todos os direitos reservados.</p>
  </footer>"""

WA_FLUTUANTE = """  <a class="wa-flutuante" href="{link}" target="_blank" rel="noopener" data-wa="flutuante" aria-label="Falar com a LF Uniformes no WhatsApp">
    <svg viewBox="0 0 32 32" width="28" height="28" aria-hidden="true"><path fill="currentColor" d="M16 3a13 13 0 0 0-11.2 19.6L3 29l6.6-1.7A13 13 0 1 0 16 3zm0 23.7c-2 0-3.9-.5-5.6-1.5l-.4-.2-3.9 1 1-3.8-.3-.4A10.7 10.7 0 1 1 16 26.7zm5.9-8c-.3-.2-1.9-1-2.2-1.1-.3-.1-.5-.2-.7.2l-1 1.2c-.2.2-.4.2-.7.1a8.8 8.8 0 0 1-4.4-3.8c-.3-.6.3-.5 1-1.7.1-.2 0-.4 0-.6l-1-2.4c-.3-.6-.5-.5-.7-.5h-.6c-.2 0-.6.1-.9.4-.3.3-1.2 1.1-1.2 2.8s1.2 3.2 1.4 3.5c.2.2 2.4 3.7 5.8 5.2 2.2.9 3 1 4.1.8.7-.1 1.9-.8 2.2-1.5.3-.8.3-1.4.2-1.5-.1-.2-.3-.3-.6-.4z"/></svg>
  </a>"""

FORM = """    <section id="orcamento" class="secao secao--escura">
      <div class="contato">
        <div>
          <h2>{titulo}</h2>
          <p>{texto}</p>
          <ul class="contato__dados">
            <li><a href="{wa}" target="_blank" rel="noopener" data-wa="contato">WhatsApp (41) 99169-7834</a></li>
            <li><a href="tel:+554136539065">Telefone (41) 3653-9065</a></li>
            <li><a href="mailto:comercial@lfuniformes.com.br">comercial@lfuniformes.com.br</a></li>
            <li>Segunda a sexta, das 8h às 18h</li>
          </ul>
        </div>
        <form class="form" id="form-orcamento" data-segmento="{segmento}" novalidate>
          <div class="campo"><label for="f-nome">Seu nome</label><input id="f-nome" name="nome" autocomplete="name" required></div>
          <div class="campo"><label for="f-empresa">{rotulo_empresa}</label><input id="f-empresa" name="empresa" autocomplete="organization" required></div>
          <div class="campo campo--meia"><label for="f-cidade">Cidade</label><input id="f-cidade" name="cidade" autocomplete="address-level2"></div>
          <div class="campo campo--meia"><label for="f-qtd">Colaboradores a uniformizar</label>
            <select id="f-qtd" name="qtd">
              <option value="">Selecione</option>
              <option>Até 10</option><option>11 a 50</option><option>51 a 200</option><option>Mais de 200</option>
            </select>
          </div>
          <fieldset class="campo">
            <legend>Setores a uniformizar</legend>
{setores}
          </fieldset>
          <div class="campo"><label for="f-msg">Mensagem (opcional)</label><textarea id="f-msg" name="mensagem" rows="3" placeholder="{placeholder}"></textarea></div>
          <p class="form__erro" id="form-erro" role="alert" hidden></p>
          <div class="form__acoes">
            <button type="submit" class="btn btn--claro" data-canal="whatsapp">Enviar pelo WhatsApp</button>
            <button type="submit" class="btn btn--linha-clara" data-canal="email">Enviar por e-mail</button>
          </div>
        </form>
      </div>
    </section>"""


def pagina(p):
    url = f"{BASE}/{p['slug']}/"
    wa = wa_link(p["wa_msg"])

    faq_ld = [{"@type": "Question", "name": q, "acceptedAnswer": {"@type": "Answer", "text": r}} for q, r in p["faq"]]
    ld = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Service",
                "@id": url + "#servico",
                "name": p["servico"],
                "serviceType": "Confecção de uniformes",
                "description": p["description"],
                "provider": {"@id": f"{BASE}/#empresa"},
                "areaServed": [
                    {"@type": "City", "name": "Curitiba"},
                    {"@type": "AdministrativeArea", "name": "Região Metropolitana de Curitiba"},
                    {"@type": "AdministrativeArea", "name": "Litoral do Paraná"},
                    {"@type": "Country", "name": "Brasil"},
                ],
                "audience": {"@type": "BusinessAudience", "name": p["publico"]},
                "url": url,
            },
            {
                "@type": "LocalBusiness",
                "@id": f"{BASE}/#empresa",
                "name": "LF Uniformes",
                "url": f"{BASE}/",
                "telephone": "+55-41-3653-9065",
                "address": {"@type": "PostalAddress", "streetAddress": "R. Luiz França, 1588", "addressLocality": "Curitiba", "addressRegion": "PR", "postalCode": "82940-090", "addressCountry": "BR"},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": "LF Uniformes", "item": f"{BASE}/"},
                    {"@type": "ListItem", "position": 2, "name": p["migalha"], "item": url},
                ],
            },
            {"@type": "FAQPage", "mainEntity": faq_ld},
        ],
    }

    linhas_tabela = "\n".join(
        f"            <tr><td>{area}</td><td>{pecas}</td><td>{motivo}</td></tr>" for area, pecas, motivo in p["areas"]
    )
    motivos = "\n".join(f"        <div><h3>{t}</h3><p>{d}</p></div>" for t, d in p["motivos"])
    faq_html = "\n".join(f"        <details><summary>{q}</summary><p>{r}</p></details>" for q, r in p["faq"])
    setores = "\n".join(
        f'            <label class="check"><input type="checkbox" name="linha" value="{s}"> {s}</label>' for s in p["setores_form"]
    )
    outros = "\n".join(
        f'        <li><a href="{href}">{nome}</a></li>' for href, nome in p["outros"]
    )
    aviso = f'\n      <div class="aviso"><p>{p["aviso"]}</p></div>' if p.get("aviso") else ""

    form = FORM.format(
        titulo=p["form_titulo"], texto=p["form_texto"], wa=wa, segmento=p["segmento"],
        rotulo_empresa=p["rotulo_empresa"], setores=setores, placeholder=p["placeholder"],
    )

    html = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <title>{p['title']}</title>
  <meta name="description" content="{p['description']}">
  <link rel="canonical" href="{url}">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta name="theme-color" content="#051129">
  <meta property="og:type" content="website">
  <meta property="og:locale" content="pt_BR">
  <meta property="og:site_name" content="LF Uniformes">
  <meta property="og:url" content="{url}">
  <meta property="og:title" content="{p['title']}">
  <meta property="og:description" content="{p['description']}">
  <meta property="og:image" content="{BASE}/img/og-image.jpg">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="icon" type="image/png" href="/img/favicon.png">
  <link rel="apple-touch-icon" href="/img/apple-touch-icon.png">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Archivo:wdth,wght@75..100,400..800&display=swap" rel="stylesheet">
  <style>
{css}
  </style>
  <script type="application/ld+json">
{json.dumps(ld, ensure_ascii=False, indent=2)}
  </script>
</head>
<body>
{CABECALHO}

  <nav class="migalhas" aria-label="Você está em">
    <ol><li><a href="/">Início</a></li><li aria-current="page">{p['migalha']}</li></ol>
  </nav>

  <main id="conteudo">
    <section class="hero hero--interna">
      <div class="hero__txt">
        <p class="hero__local">{p['sobretitulo']}</p>
        <h1>{p['h1']}</h1>
        <p class="resposta">{p['resposta']}</p>
        <div class="hero__ctas">
          <a class="btn" href="#orcamento">Pedir orçamento</a>
          <a class="btn btn--linha" href="{wa}" target="_blank" rel="noopener" data-wa="hero">Falar no WhatsApp</a>
        </div>
      </div>
      <figure class="hero__img">
        <img src="/img/{p['imagem']}" alt="{p['imagem_alt']}" width="800" height="992" fetchpriority="high" decoding="async">
        <figcaption class="etiqueta">
          <span class="etiqueta__furo" aria-hidden="true"></span>
          {p['etiqueta']}
        </figcaption>
      </figure>
    </section>

    <section class="secao">
      <div class="secao__cab">
        <h2>{p['areas_titulo']}</h2>
        <p>{p['areas_texto']}</p>
      </div>
      <table class="tabela-areas">
        <thead><tr><th scope="col">Setor</th><th scope="col">Peças indicadas</th><th scope="col">Por quê</th></tr></thead>
        <tbody>
{linhas_tabela}
        </tbody>
      </table>{aviso}
    </section>

    <section class="secao secao--clara">
      <div class="secao__cab">
        <h2>{p['motivos_titulo']}</h2>
      </div>
      <div class="motivos">
{motivos}
      </div>
    </section>

    <section class="secao">
      <div class="secao__cab">
        <h2>Como funciona, em média 30 dias úteis</h2>
        <p>O prazo começa a contar na confirmação do pedido com o pagamento da entrada e varia conforme as peças escolhidas.</p>
      </div>
      <ol class="costura">
        <li><h3>Atendimento e orçamento</h3><p>{p['etapa1']}</p></li>
        <li><h3>Tomada de medidas</h3><p>{p['etapa2']}</p></li>
        <li><h3>Tecido e corte</h3><p>Compramos o tecido na cor escolhida, dentro da cartela de cada tecido, e cortamos na nossa modelagem.</p></li>
        <li><h3>Confecção e bordado</h3><p>O bordado com o logo é aprovado antes da produção. Em pedidos maiores, aprovamos também uma peça piloto.</p></li>
        <li><h3>Conferência e entrega</h3><p>Cada peça é conferida no acabamento e entregue separada por colaborador ou setor.</p></li>
      </ol>
    </section>

    <section class="secao secao--clara">
      <div class="secao__cab">
        <h2>Perguntas frequentes</h2>
      </div>
      <div class="faq">
{faq_html}
      </div>
    </section>

    <section class="secao">
      <div class="secao__cab">
        <h2>Outros segmentos que atendemos</h2>
      </div>
      <ul class="outros-segmentos">
{outros}
      </ul>
    </section>

{form}
  </main>

{RODAPE}

{WA_FLUTUANTE.format(link=wa)}

  <script>
{js}
  </script>
</body>
</html>
"""
    pasta = os.path.join(SAIDA, p["slug"])
    os.makedirs(pasta, exist_ok=True)
    with open(os.path.join(pasta, "index.html"), "w", encoding="utf-8") as f:
        f.write(html)
    return url


# ---------------------------------------------------------------------------
OUTROS_TODOS = [
    ("/uniformes-para-hospitais/", "Hospitais"),
    ("/uniformes-para-clinicas/", "Clínicas"),
    ("/uniformes-para-escolas/", "Escolas e colégios"),
    ("/#segmentos", "Recepção e atendimento"),
    ("/#segmentos", "Comercial e administrativo"),
    ("/#segmentos", "Segurança e portaria"),
    ("/#segmentos", "Feiras e eventos"),
]


def outros(excluir):
    return [o for o in OUTROS_TODOS if o[0] != excluir]


PAGINAS = [
    {
        "slug": "uniformes-para-hospitais",
        "segmento": "Hospital",
        "migalha": "Uniformes para hospitais",
        "servico": "Uniformes para recepção, administrativo e equipes de apoio de hospitais",
        "publico": "Hospitais",
        "title": "Uniformes para Hospitais em Curitiba: Recepção e Apoio | LF Uniformes",
        "description": "Uniformes para recepção, internação, administrativo, higienização, manutenção e portaria de hospitais. Medidas tiradas no hospital, bordado com o logo e prazo médio de 30 dias úteis.",
        "sobretitulo": "Uniformes para hospitais em Curitiba",
        "h1": "Uniformes para recepção, administrativo e equipes de apoio de hospitais",
        "resposta": "A LF Uniformes confecciona os uniformes de quem recebe, organiza e mantém o hospital funcionando: recepção e internação, faturamento, central de atendimento, higienização, manutenção e portaria. Levamos a grade de tamanhos até o hospital e bordamos o logo da instituição.",
        "imagem": "feminino.webp",
        "imagem_alt": "Recepcionista com uniforme social azul-marinho em balcão de atendimento",
        "etiqueta": "Medidas tiradas no próprio hospital",
        "areas_titulo": "Uniforme certo para cada setor do hospital",
        "areas_texto": "Um hospital tem equipes com rotinas muito diferentes. Indicamos peças pensadas para cada uma, com a mesma identidade visual.",
        "areas": [
            ("Recepção e internação", "Blazer, camisete ou camisa social, calça social, maxicolete", "Primeiro contato do paciente: o uniforme social transmite organização e confiança."),
            ("Faturamento, administrativo e central de atendimento", "Camisa social, calça social, colete ou pulôver", "Conforto para longas jornadas sentado, sem perder o padrão."),
            ("Higienização e limpeza", "Jaleco para limpeza, calça com elástico, camisa polo", "Peças práticas para movimento constante e lavagem frequente."),
            ("Manutenção e infraestrutura", "Camisa polo em malha piquet, calça, jaqueta", "Resistência para o trabalho em campo, com identificação clara."),
            ("Portaria e segurança", "Camisa social, calça social, jaqueta social", "Presença e autoridade na entrada do hospital."),
        ],
        "aviso": "Não confeccionamos jalecos médicos nem roupas privativas (scrubs) para a equipe assistencial. Nosso foco são as equipes de recepção, administrativo e apoio.",
        "motivos_titulo": "Por que hospitais escolhem a LF",
        "motivos": [
            ("Medidas no hospital, sem tirar ninguém do setor", "Levamos a grade física para os colaboradores provarem no próprio hospital. Para equipes em vários turnos, também há a tabela digital de medidas."),
            ("Uma identidade visual para todos os setores", "Do blazer da recepção à polo da manutenção, as peças seguem a mesma cartela de cores e o mesmo bordado com o logo."),
            ("Reposição para novos colaboradores", "Kits individuais para quem chega à equipe seguem o mesmo prazo do pedido inicial. Pedidos urgentes são avaliados pela nossa produção."),
            ("Garantia de defeito e tamanho", "Se uma peça vier com defeito ou não servir, avaliamos e ajustamos. Quase sempre resolvemos com um ajuste da costureira."),
        ],
        "etapa1": "Entendemos os setores, o número de colaboradores e a identidade do hospital. O orçamento sai em 1 a 2 dias.",
        "etapa2": "Levamos a grade física até o hospital para cada colaborador provar, ou enviamos a tabela digital de medidas para equipes em turnos.",
        "faq": [
            ("A LF Uniformes faz jaleco médico ou scrub?", "Não. Confeccionamos uniformes para recepção, internação, administrativo, higienização, manutenção e portaria de hospitais. Não fazemos jalecos médicos nem roupas privativas para a equipe assistencial."),
            ("Como funciona a tomada de medidas em um hospital com vários turnos?", "Levamos a grade física de tamanhos até o hospital para os colaboradores provarem. Quem não puder provar no horário da visita usa a tabela digital de medidas."),
            ("Qual o prazo de entrega de uniformes para hospitais?", "O prazo médio é de 30 dias úteis a partir da confirmação do pedido e do pagamento da entrada. Pode variar conforme as peças escolhidas."),
            ("Dá para bordar o logo do hospital?", "Sim. Fazemos bordado ou DTF com o logo da instituição, e o bordado passa por uma prova para aprovação antes da produção."),
            ("Como funciona a reposição quando entra um novo colaborador?", "Fazemos kits individuais com o mesmo padrão do pedido original. O prazo é o mesmo do pedido de equipe; pedidos urgentes são avaliados pela produção."),
        ],
        "outros": outros("/uniformes-para-hospitais/"),
        "form_titulo": "Peça um orçamento para o seu hospital",
        "form_texto": "Conte quais setores e quantos colaboradores quer uniformizar. Respondemos em 1 a 2 dias com as peças indicadas e o prazo.",
        "rotulo_empresa": "Hospital",
        "setores_form": ["Recepção e internação", "Administrativo", "Higienização", "Manutenção", "Portaria e segurança"],
        "placeholder": "Cores do hospital, prazo desejado, número de colaboradores por setor…",
        "wa_msg": "Oi, vim pelo site! Gostaria de um orçamento de uniformes para hospital.",
    },
    {
        "slug": "uniformes-para-clinicas",
        "segmento": "Clínica",
        "migalha": "Uniformes para clínicas",
        "servico": "Uniformes para recepção e equipes de clínicas",
        "publico": "Clínicas médicas, odontológicas, de estética e laboratórios",
        "title": "Uniformes para Clínicas em Curitiba: Recepção e Equipe | LF Uniformes",
        "description": "Uniformes para recepção, atendimento, administrativo e equipe de apoio de clínicas médicas, odontológicas, de estética e laboratórios. Bordado com o logo e prazo médio de 30 dias úteis.",
        "sobretitulo": "Uniformes para clínicas em Curitiba",
        "h1": "Uniformes para a recepção e a equipe da sua clínica",
        "resposta": "A LF Uniformes confecciona uniformes para quem atende o paciente antes e depois da consulta: recepção, agendamento, administrativo e equipe de apoio de clínicas médicas, odontológicas, de estética e laboratórios. Modelos sociais e polos com o logo da clínica bordado.",
        "imagem": "feminino.webp",
        "imagem_alt": "Recepcionista de clínica com blazer azul-marinho e blusa branca",
        "etiqueta": "Logo da clínica bordado com prova",
        "areas_titulo": "Uniforme certo para cada função da clínica",
        "areas_texto": "Em uma clínica, a recepção é a primeira impressão do paciente. O uniforme ajuda a transmitir cuidado antes mesmo do atendimento.",
        "areas": [
            ("Recepção e agendamento", "Blazer, camisete social, calça ou saia, maxicolete", "O paciente reconhece de imediato quem está ali para atendê-lo."),
            ("Administrativo e financeiro", "Camisa social, calça social, colete ou pulôver", "Padrão profissional com conforto para o dia todo."),
            ("Auxiliares e equipe de apoio", "Camisa polo em malha piquet bordada, calça", "Peça prática e identificada para quem circula pela clínica."),
            ("Limpeza e conservação", "Jaleco para limpeza, calça com elástico", "Durável e fácil de lavar."),
        ],
        "aviso": "Não confeccionamos jalecos médicos nem roupas privativas (scrubs) para os profissionais de saúde. Nosso foco são a recepção, o administrativo e a equipe de apoio.",
        "motivos_titulo": "Por que clínicas escolhem a LF",
        "motivos": [
            ("Imagem alinhada à marca da clínica", "Escolhemos juntos o tecido e a cor dentro das cartelas, e bordamos o logo com prova de aprovação antes da produção."),
            ("Medidas sem parar o atendimento", "Levamos a grade física até a clínica, a equipe pode provar na nossa loja ou usar a tabela digital de medidas."),
            ("Tecidos indicados para uso diário", "Camisas sociais em Tricoline Ibiza, London Confort, Confort Plus e Amelie; polos em malha piquet."),
            ("Garantia de defeito e tamanho", "Se uma peça vier com defeito ou não servir, avaliamos e ajustamos. Quase sempre resolvemos com um ajuste da costureira."),
        ],
        "etapa1": "Entendemos a equipe, o estilo da clínica e as cores da marca. O orçamento sai em 1 a 2 dias.",
        "etapa2": "Levamos a grade física até a clínica, a equipe prova na nossa loja ou usa a tabela digital de medidas.",
        "faq": [
            ("A LF Uniformes faz jaleco para dentista ou médico?", "Não. Confeccionamos uniformes para recepção, agendamento, administrativo e equipe de apoio de clínicas. Não fazemos jalecos nem scrubs para os profissionais de saúde."),
            ("Atendem clínicas pequenas?", "Sim. Atendemos clínicas de diferentes tamanhos. Algumas peças têm condições específicas de quantidade, que informamos no orçamento."),
            ("Qual o prazo de entrega?", "O prazo médio é de 30 dias úteis a partir da confirmação do pedido e do pagamento da entrada. Pode variar conforme as peças."),
            ("Dá para colocar o logo da clínica?", "Sim, com bordado ou DTF. O bordado passa por uma prova para aprovação antes da produção."),
            ("Quais cores posso escolher?", "Trabalhamos com a cartela de cores de cada tecido, que é bem ampla. Ajudamos a escolher a combinação mais próxima da identidade da clínica."),
        ],
        "outros": outros("/uniformes-para-clinicas/"),
        "form_titulo": "Peça um orçamento para a sua clínica",
        "form_texto": "Conte o tipo de clínica, quantas pessoas e quais funções quer uniformizar. Respondemos em 1 a 2 dias.",
        "rotulo_empresa": "Clínica",
        "setores_form": ["Recepção e agendamento", "Administrativo", "Equipe de apoio", "Limpeza"],
        "placeholder": "Tipo de clínica, cores da marca, prazo desejado…",
        "wa_msg": "Oi, vim pelo site! Gostaria de um orçamento de uniformes para clínica.",
    },
    {
        "slug": "uniformes-para-escolas",
        "segmento": "Escola",
        "migalha": "Uniformes para escolas",
        "servico": "Uniformes para colaboradores de escolas e colégios",
        "publico": "Escolas e colégios",
        "title": "Uniformes para Colaboradores de Escolas e Colégios | LF Uniformes",
        "description": "Uniformes para professores, coordenação, secretaria, portaria, cantina e limpeza de escolas e colégios. Bordado com o brasão da escola e prazo médio de 30 dias úteis.",
        "sobretitulo": "Uniformes para escolas em Curitiba",
        "h1": "Uniformes para professores e colaboradores de escolas e colégios",
        "resposta": "A LF Uniformes confecciona uniformes para toda a equipe da escola: professores, coordenação, secretaria, portaria, inspetores, cantina e limpeza. As peças levam o brasão ou o logo da escola bordado. Não fazemos uniforme escolar para alunos.",
        "imagem": "hero.webp",
        "imagem_alt": "Equipe de colaboradores com uniformes azul-marinho padronizados",
        "etiqueta": "Equipe padronizada para o ano letivo",
        "areas_titulo": "Uniforme certo para cada função na escola",
        "areas_texto": "Pais e alunos identificam com facilidade quem faz parte da equipe, e a escola transmite uma imagem organizada do portão à sala de aula.",
        "areas": [
            ("Professores", "Camisa polo em malha piquet bordada, camisa social", "Conforto para o dia em sala e identificação imediata."),
            ("Coordenação, direção e secretaria", "Blazer, camisa ou camisete social, calça social, maxicolete", "Padrão executivo para o atendimento aos pais."),
            ("Portaria e inspetores", "Camisa polo, jaqueta, calça", "Visibilidade e praticidade na entrada e nos corredores."),
            ("Cantina e limpeza", "Jaleco para limpeza, calça com elástico, camisa polo", "Peças resistentes para lavagem frequente."),
        ],
        "aviso": "Atendemos apenas colaboradores. Não confeccionamos uniforme escolar para alunos.",
        "motivos_titulo": "Por que escolas escolhem a LF",
        "motivos": [
            ("Equipe pronta no início do ano letivo", "Com prazo médio de 30 dias úteis, fechar o pedido no fim do ano anterior garante a equipe uniformizada no primeiro dia de aula."),
            ("Brasão bordado com aprovação", "O bordado do brasão ou logo passa por uma prova antes da produção. Em pedidos maiores, aprovamos também uma peça piloto."),
            ("Medidas na escola", "Levamos a grade física para professores e colaboradores provarem na própria escola, ou usamos a tabela digital de medidas."),
            ("Reposição para novos contratados", "Kits individuais para quem chega no meio do ano seguem o mesmo padrão e prazo do pedido original."),
        ],
        "etapa1": "Entendemos as funções, o número de colaboradores e a identidade da escola. O orçamento sai em 1 a 2 dias.",
        "etapa2": "Levamos a grade física até a escola para cada colaborador provar, ou enviamos a tabela digital de medidas.",
        "faq": [
            ("A LF Uniformes faz uniforme escolar para alunos?", "Não. Confeccionamos uniformes para colaboradores de escolas e colégios: professores, coordenação, secretaria, portaria, cantina e limpeza."),
            ("Quando devo fazer o pedido para o início do ano letivo?", "O prazo médio é de 30 dias úteis a partir da confirmação do pedido e do pagamento da entrada. Para ter a equipe uniformizada no início das aulas, recomendamos fechar o pedido ainda no fim do ano anterior."),
            ("Dá para bordar o brasão da escola?", "Sim. Fazemos bordado ou DTF, e o bordado passa por uma prova para aprovação antes da produção."),
            ("Já atenderam escolas?", "Sim. O Colégio Erasto Gaertner está entre os clientes da LF Uniformes."),
            ("Como funciona a reposição para professores contratados no meio do ano?", "Fazemos kits individuais com o mesmo padrão do pedido original, no mesmo prazo do pedido de equipe."),
        ],
        "outros": outros("/uniformes-para-escolas/"),
        "form_titulo": "Peça um orçamento para a sua escola",
        "form_texto": "Conte quantos colaboradores e quais funções quer uniformizar. Respondemos em 1 a 2 dias com as peças indicadas e o prazo.",
        "rotulo_empresa": "Escola ou colégio",
        "setores_form": ["Professores", "Coordenação e secretaria", "Portaria e inspetores", "Cantina e limpeza"],
        "placeholder": "Cores da escola, data de início das aulas, número de colaboradores…",
        "wa_msg": "Oi, vim pelo site! Gostaria de um orçamento de uniformes para os colaboradores da escola.",
    },
]

if __name__ == "__main__":
    for p in PAGINAS:
        print(pagina(p))
