# LF Uniformes — site novo (versão básica para migração)

Site estático (HTML, CSS e JS puros), sem banco de dados. Funciona em qualquer hospedagem: Apache/cPanel, Nginx, Vercel, Netlify, Cloudflare Pages.

## Arquivos

| Arquivo | Para que serve |
| --- | --- |
| index.html | Página inicial, com SEO, dados estruturados (LocalBusiness, WebSite e FAQPage) e formulário de orçamento |
| assets/css/style.css | Estilos |
| assets/js/main.js | Menu mobile, formulário (abre WhatsApp ou e-mail com a mensagem pronta), UTMs e eventos para GA4/GTM |
| 404.html | Página de erro |
| robots.txt | Libera buscadores e robôs de IA, aponta o sitemap |
| sitemap.xml | Mapa do site (atualizar a cada página nova) |
| llms.txt | Resumo da empresa para ferramentas de IA (GEO) |
| .htaccess | Só para Apache: HTTPS, remoção do www, 404, compressão e cache |

## Passo a passo da migração

1. **Colocar as 5 fotos na pasta `img/`** com estes nomes exatos (baixadas do Canva):
   - `img/hero.jpg` (equipe), `img/feminino.jpg`, `img/masculino.jpg`, `img/operacional.jpg`, `img/confeccao.jpg`
   - `img/logo.png` (logo da LF, de preferência com fundo transparente)
   Os clientes aparecem por nome; as imagens do site antigo não são mais necessárias.
2. **Subir os arquivos deste pacote** na raiz do novo servidor, junto com as pastas do passo 1.
3. **Apontar o domínio** lfuniformes.com.br para o novo servidor (DNS) e ativar o SSL (HTTPS).
4. **Conferir:** abrir o site no celular e no computador, testar os botões de WhatsApp e o formulário, abrir /robots.txt, /sitemap.xml e /llms.txt.
5. **Google Search Console:** verificar o domínio e enviar o sitemap (https://lfuniformes.com.br/sitemap.xml).
6. **Validar os dados estruturados** em https://search.google.com/test/rich-results
7. **Opcional — medição:** colar o código do Google Tag Manager ou do GA4 no `<head>` do index.html. Os eventos `clique_whatsapp` e `envio_orcamento` já são enviados ao `dataLayer`.

## O que já foi corrigido em relação ao site antigo

- Um único H1 e hierarquia de títulos correta
- Title e meta description no tamanho certo; meta keywords removida
- CEP corrigido (83323-410) e rodapé corrigido
- Nome "LF Uniformes" padronizado, com "Le Favaro Uniformes Executivos" como nome alternativo nos dados estruturados
- Dados estruturados de empresa local e perguntas frequentes
- Formulário com qualificação (empresa, cidade, nº de colaboradores, linhas de interesse)
- Robôs de IA liberados e llms.txt publicado

## Próxima etapa (depois do questionário)

Criar as páginas internas (linhas, peças-chave, segmentos, como trabalhamos, clientes e cases, sobre, blog), incluir prazos, capacidade produtiva, cases e depoimentos, e ligar o formulário ao CRM.
