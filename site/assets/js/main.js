// LF Uniformes — scripts do site
(function () {
  var WHATSAPP = '5541991697834';
  var DIA = 24 * 60 * 60 * 1000;
  var CHAVE_ORIGEM = 'lf_origem';
  var CHAVE_CONSENTIMENTO = 'lf_consentimento';
  var CAMPOS_ORIGEM = ['utm_source', 'utm_medium', 'utm_campaign', 'utm_term', 'utm_content', 'gclid', 'gbraid', 'wbraid'];

  // ---------------------------------------------------------------------------
  // Utilidades
  // ---------------------------------------------------------------------------
  function lerStorage(chave) {
    try { return JSON.parse(window.localStorage.getItem(chave) || 'null'); } catch (e) { return null; }
  }
  function gravarStorage(chave, valor) {
    try { window.localStorage.setItem(chave, JSON.stringify(valor)); } catch (e) {}
  }
  function apagarStorage(chave) {
    try { window.localStorage.removeItem(chave); } catch (e) {}
  }

  window.dataLayer = window.dataLayer || [];
  if (typeof window.gtag !== 'function') {
    window.gtag = function () { window.dataLayer.push(arguments); };
  }
  function evento(nome, dados) {
    window.dataLayer.push(Object.assign({ event: nome }, dados || {}));
  }

  // Código curto do lead: LF-XXXXX (5 caracteres A-Z e 0-9)
  function gerarLeadId() {
    var letras = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789', cod = '';
    var aleatorio = new Uint8Array(5);
    if (window.crypto && window.crypto.getRandomValues) {
      window.crypto.getRandomValues(aleatorio);
    } else {
      for (var i = 0; i < 5; i++) aleatorio[i] = Math.floor(Math.random() * 256);
    }
    for (var j = 0; j < 5; j++) cod += letras.charAt(aleatorio[j] % letras.length);
    return 'LF-' + cod;
  }

  // ---------------------------------------------------------------------------
  // Origem da visita (UTMs + clique do Google), validade de 90 dias,
  // regra de último clique pago: só sobrescreve quando a visita chega COM utm ou gclid.
  // ---------------------------------------------------------------------------
  (function capturarOrigem() {
    var params = new URLSearchParams(window.location.search);
    var nova = {}, temParametro = false;
    CAMPOS_ORIGEM.forEach(function (c) {
      var v = params.get(c);
      if (v) { nova[c] = v.slice(0, 200); temParametro = true; }
    });
    if (temParametro) {
      // Anúncio do Google com marcação automática e sem UTM: identifica como google/cpc
      if (!nova.utm_source && (nova.gclid || nova.gbraid || nova.wbraid)) {
        nova.utm_source = 'google';
        nova.utm_medium = nova.utm_medium || 'cpc';
      }
      nova.pagina_entrada = window.location.pathname;
      nova.capturado_em = Date.now();
      nova.expira_em = Date.now() + 90 * DIA;
      gravarStorage(CHAVE_ORIGEM, nova);
      return;
    }
    var salva = lerStorage(CHAVE_ORIGEM);
    if (salva && (!salva.expira_em || salva.expira_em < Date.now())) apagarStorage(CHAVE_ORIGEM);
  })();

  function origemSalva() {
    var o = lerStorage(CHAVE_ORIGEM);
    if (!o || !o.expira_em || o.expira_em < Date.now()) return null;
    return o;
  }

  // Campos de origem para o dataLayer (sempre presentes, vazios quando não há origem)
  function camposOrigem() {
    var o = origemSalva() || {};
    return {
      utm_source: o.utm_source || '',
      utm_medium: o.utm_medium || '',
      utm_campaign: o.utm_campaign || '',
      utm_term: o.utm_term || '',
      utm_content: o.utm_content || '',
      gclid: o.gclid || '',
      gbraid: o.gbraid || '',
      wbraid: o.wbraid || ''
    };
  }

  // Linha discreta no fim da mensagem do WhatsApp
  function linhaRastreio(leadId) {
    var o = origemSalva();
    if (!o || !o.utm_source) return 'Cód: ' + leadId + ' | Origem: direto/orgânico';
    return 'Cód: ' + leadId +
      ' | Origem: ' + o.utm_source + '/' + (o.utm_medium || '-') +
      ' | Campanha: ' + (o.utm_campaign || '-') +
      ' | Termo: ' + (o.utm_term || '-');
  }

  function abrirWhatsApp(texto) {
    window.open('https://wa.me/' + WHATSAPP + '?text=' + encodeURIComponent(texto), '_blank', 'noopener');
  }

  // ---------------------------------------------------------------------------
  // Ano do rodapé e menu mobile
  // ---------------------------------------------------------------------------
  var ano = document.getElementById('ano');
  if (ano) ano.textContent = new Date().getFullYear();

  var btn = document.querySelector('.menu-btn');
  var nav = document.getElementById('menu');
  if (btn && nav) {
    btn.addEventListener('click', function () {
      var aberto = nav.classList.toggle('aberto');
      btn.setAttribute('aria-expanded', aberto ? 'true' : 'false');
    });
    nav.addEventListener('click', function (e) {
      if (e.target.tagName === 'A') { nav.classList.remove('aberto'); btn.setAttribute('aria-expanded', 'false'); }
    });
  }

  // ---------------------------------------------------------------------------
  // Imagens: tenta variações comuns de nome/extensão antes de esconder o espaço
  // ---------------------------------------------------------------------------
  function variacoes(src) {
    var m = src.match(/^(.*\/)([^\/]+?)\.(\w+)$/);
    if (!m) return [];
    var pasta = m[1], nome = m[2], lista = [];
    var nomes = [nome, nome.charAt(0).toUpperCase() + nome.slice(1), nome.toUpperCase()];
    if (nome === 'confeccao') nomes.push('confecção', 'Confecção', 'confecçao');
    ['jpg', 'jpeg', 'png', 'webp', 'JPG', 'JPEG', 'PNG'].forEach(function (ext) {
      nomes.forEach(function (n) { lista.push(pasta + n + '.' + ext); });
    });
    return lista.filter(function (u) { return u !== src; });
  }
  function tentarProxima(img) {
    if (!img._fila) img._fila = variacoes(img.getAttribute('src'));
    var prox = img._fila.shift();
    if (prox) { img.src = prox; } else { img.classList.add('sem-img'); }
  }
  document.querySelectorAll('img').forEach(function (img) {
    img.addEventListener('error', function () { tentarProxima(img); });
    if (img.complete && img.naturalWidth === 0 && img.getAttribute('loading') !== 'lazy') tentarProxima(img);
  });

  // ---------------------------------------------------------------------------
  // Cliques no WhatsApp: gera o código do lead, acrescenta a linha de rastreio
  // na mensagem e envia o evento clique_whatsapp
  // ---------------------------------------------------------------------------
  document.querySelectorAll('a[href*="wa.me/"]').forEach(function (a) {
    a.addEventListener('click', function () {
      var leadId = gerarLeadId();
      try {
        var url = new URL(a.getAttribute('href'), window.location.href);
        var base = url.searchParams.get('text') || 'Oi, vim pelo site! Gostaria de falar com um consultor.';
        base = base.split('\n\nCód: ')[0];
        // monta com encodeURIComponent (%20 para espaços), formato que o WhatsApp sempre entende
        a.setAttribute('href', url.origin + url.pathname + '?text=' + encodeURIComponent(base + '\n\n' + linhaRastreio(leadId)));
      } catch (e) {}
      evento('clique_whatsapp', Object.assign({
        posicao: a.getAttribute('data-wa') || 'link',
        lead_id: leadId
      }, camposOrigem()));
    });
  });

  // ---------------------------------------------------------------------------
  // Formulários de materiais (blog): webhook (n8n/CRM), se configurado, ou WhatsApp
  // ---------------------------------------------------------------------------
  var LEAD_WEBHOOK = ''; // ex.: 'https://seu-n8n/webhook/lf-leads'
  document.querySelectorAll('form.form-material').forEach(function (fm) {
    fm.addEventListener('submit', function (e) {
      e.preventDefault();
      var d = new FormData(fm);
      var nome = (d.get('nome') || '').trim(), empresa = (d.get('empresa') || '').trim(), zap = (d.get('whatsapp') || '').trim();
      var err = fm.querySelector('.form__erro');
      if (!nome || !empresa || zap.replace(/\D/g, '').length < 10) {
        err.textContent = 'Preencha nome, empresa e um WhatsApp com DDD para receber o material.';
        err.hidden = false;
        return;
      }
      err.hidden = true;
      var leadId = gerarLeadId();
      var dados = Object.assign({
        lead_id: leadId, nome: nome, empresa: empresa, whatsapp: zap, email: (d.get('email') || '').trim(),
        material: fm.getAttribute('data-material'), material_titulo: fm.getAttribute('data-material-titulo'),
        artigo: window.location.pathname
      }, camposOrigem());
      // dataLayer sem dados pessoais
      evento('download_material', Object.assign({ material: dados.material, artigo: dados.artigo, lead_id: leadId }, camposOrigem()));
      var texto = 'Oi, vim pelo blog da LF! Quero receber o material: ' + dados.material_titulo + '.\n\nNome: ' + nome +
        '\nEmpresa: ' + empresa + (dados.email ? '\nE-mail: ' + dados.email : '') + '\nArtigo: ' + window.location.pathname +
        '\n\n' + linhaRastreio(leadId);
      function concluir() {
        fm.innerHTML = '<p class="material__ok" role="status">Pronto! Vamos enviar o material no seu WhatsApp.</p>';
      }
      if (LEAD_WEBHOOK) {
        fetch(LEAD_WEBHOOK, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(dados) })
          .then(concluir)
          .catch(function () { abrirWhatsApp(texto); concluir(); });
      } else {
        abrirWhatsApp(texto);
        concluir();
      }
    });
  });

  // ---------------------------------------------------------------------------
  // Aviso de cookies (LGPD) + Consent Mode do Google
  // O padrão "denied" é definido no <head>, antes do GTM carregar.
  // ---------------------------------------------------------------------------
  function aplicarConsentimento(valor) {
    var estado = valor === 'granted' ? 'granted' : 'denied';
    window.gtag('consent', 'update', {
      ad_storage: estado,
      ad_user_data: estado,
      ad_personalization: estado,
      analytics_storage: estado
    });
    gravarStorage(CHAVE_CONSENTIMENTO, { valor: estado, salvo_em: Date.now(), expira_em: Date.now() + 365 * DIA });
    evento('consentimento_atualizado', { consentimento: estado });
  }

  (function avisoCookies() {
    var salvo = lerStorage(CHAVE_CONSENTIMENTO);
    if (salvo && salvo.expira_em && salvo.expira_em > Date.now()) return;

    var aviso = document.createElement('div');
    aviso.className = 'aviso-cookies';
    aviso.setAttribute('role', 'region');
    aviso.setAttribute('aria-label', 'Aviso de cookies');
    aviso.innerHTML =
      '<p>Usamos cookies para medir as visitas e melhorar nossos anúncios. Você pode aceitar ou recusar. ' +
      '<a href="/privacidade/">Política de Privacidade</a></p>' +
      '<div class="aviso-cookies__acoes">' +
      '<button type="button" class="btn btn--sm btn--linha-clara" data-consentimento="denied">Recusar</button>' +
      '<button type="button" class="btn btn--sm btn--claro" data-consentimento="granted">Aceitar</button>' +
      '</div>';
    document.body.appendChild(aviso);
    document.body.classList.add('com-aviso');

    // Reserva espaço no fim da página e sobe o botão do WhatsApp para o aviso não cobrir nada
    function ajustarAltura() {
      document.documentElement.style.setProperty('--aviso-h', aviso.offsetHeight + 'px');
    }
    ajustarAltura();
    window.addEventListener('resize', ajustarAltura);

    aviso.addEventListener('click', function (e) {
      var escolha = e.target.getAttribute && e.target.getAttribute('data-consentimento');
      if (!escolha) return;
      aplicarConsentimento(escolha);
      aviso.remove();
      document.body.classList.remove('com-aviso');
      document.documentElement.style.removeProperty('--aviso-h');
      window.removeEventListener('resize', ajustarAltura);
    });
  })();

  // Link "Preferências de cookies" (rodapé e página de privacidade): reabre a escolha
  document.querySelectorAll('[data-reabrir-cookies]').forEach(function (el) {
    el.addEventListener('click', function (e) {
      e.preventDefault();
      apagarStorage(CHAVE_CONSENTIMENTO);
      window.location.reload();
    });
  });

  // ---------------------------------------------------------------------------
  // Formulário de orçamento: monta a mensagem e abre o WhatsApp
  // ---------------------------------------------------------------------------
  var form = document.getElementById('form-orcamento');
  if (!form) return;
  var erro = document.getElementById('form-erro');

  form.addEventListener('submit', function (e) {
    e.preventDefault();
    var d = new FormData(form);
    var nome = (d.get('nome') || '').trim();
    var empresa = (d.get('empresa') || '').trim();
    if (!nome || !empresa) {
      erro.textContent = 'Preencha seu nome e o nome da empresa para enviarmos o pedido.';
      erro.hidden = false;
      (nome ? form.empresa : form.nome).focus();
      return;
    }
    erro.hidden = true;

    var leadId = gerarLeadId();
    var segmento = form.getAttribute('data-segmento') || 'home';
    var segmentoNome = form.getAttribute('data-segmento-nome') || '';
    var marcados = d.getAll('linha');
    var legenda = form.querySelector('fieldset legend');
    var rotuloMarcados = legenda ? legenda.textContent.trim() : 'Linhas de interesse';

    var texto = [
      'Oi, vim pelo site! Gostaria de solicitar um orçamento.',
      '',
      segmentoNome ? 'Segmento: ' + segmentoNome : '',
      'Nome: ' + nome,
      'Empresa: ' + empresa,
      d.get('cidade') ? 'Cidade: ' + d.get('cidade') : '',
      d.get('qtd') ? 'Colaboradores: ' + d.get('qtd') : '',
      marcados.length ? rotuloMarcados + ': ' + marcados.join(', ') : '',
      d.get('mensagem') ? 'Mensagem: ' + d.get('mensagem') : ''
    ].filter(function (l, i) { return l !== '' || i === 1; }).join('\n') + '\n\n' + linhaRastreio(leadId);

    // dataLayer sem nome, telefone ou e-mail
    evento('envio_orcamento', Object.assign({
      canal: 'whatsapp',
      colaboradores: d.get('qtd') || '',
      segmento: segmento,
      lead_id: leadId
    }, camposOrigem()));

    abrirWhatsApp(texto);
  });
})();
