// LF Uniformes — scripts básicos
(function () {
  var WHATSAPP = '5541991697834';

  // Ano do rodapé
  var ano = document.getElementById('ano');
  if (ano) ano.textContent = new Date().getFullYear();

  // Menu mobile
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

  // Imagem que ainda não foi copiada para o servidor: esconde sem quebrar o layout
  // Se a foto não for encontrada, tenta variações comuns de nome e extensão
  // (ex.: hero.png, Hero.jpg, confecção.jpg) antes de esconder o espaço.
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

  // Origem do visitante (UTMs) guardada para acompanhar as mensagens
  var params = new URLSearchParams(location.search);
  var utm = ['utm_source', 'utm_medium', 'utm_campaign'].map(function (k) { return params.get(k); }).filter(Boolean);
  try {
    if (utm.length) sessionStorage.setItem('lf_origem', utm.join(' / '));
  } catch (e) {}
  function origem() {
    try { return sessionStorage.getItem('lf_origem') || ''; } catch (e) { return ''; }
  }

  // Eventos para o Google Analytics 4 / Tag Manager, quando instalados
  function evento(nome, dados) {
    window.dataLayer = window.dataLayer || [];
    window.dataLayer.push(Object.assign({ event: nome }, dados || {}));
  }
  document.querySelectorAll('[data-wa]').forEach(function (a) {
    a.addEventListener('click', function () { evento('clique_whatsapp', { posicao: a.getAttribute('data-wa') }); });
  });

  // Formulários de materiais (blog): envia para o webhook (n8n/CRM), se configurado,
  // ou abre o WhatsApp com o pedido do material.
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
      var dados = {
        nome: nome, empresa: empresa, whatsapp: zap, email: (d.get('email') || '').trim(),
        material: fm.getAttribute('data-material'), material_titulo: fm.getAttribute('data-material-titulo'),
        artigo: location.pathname, origem: origem()
      };
      evento('download_material', { material: dados.material, artigo: dados.artigo });
      var texto = 'Oi, vim pelo blog da LF! Quero receber o material: ' + dados.material_titulo + '.\n\nNome: ' + nome + '\nEmpresa: ' + empresa + (dados.email ? '\nE-mail: ' + dados.email : '') + '\nArtigo: ' + location.pathname;
      function concluir() {
        fm.innerHTML = '<p class="material__ok" role="status">Pronto! Vamos enviar o material no seu WhatsApp.</p>';
      }
      if (LEAD_WEBHOOK) {
        fetch(LEAD_WEBHOOK, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify(dados) })
          .then(concluir)
          .catch(function () { window.open('https://wa.me/' + WHATSAPP + '?text=' + encodeURIComponent(texto), '_blank', 'noopener'); concluir(); });
      } else {
        window.open('https://wa.me/' + WHATSAPP + '?text=' + encodeURIComponent(texto), '_blank', 'noopener');
        concluir();
      }
    });
  });

  // Formulário de orçamento: monta a mensagem e abre WhatsApp ou e-mail
  var form = document.getElementById('form-orcamento');
  if (!form) return;
  var erro = document.getElementById('form-erro');
  var canal = 'whatsapp';

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

    var linhas = d.getAll('linha');
    var texto = [
      'Oi, vim pelo site! Gostaria de solicitar um orçamento.',
      '',
      form.getAttribute('data-segmento') ? 'Segmento: ' + form.getAttribute('data-segmento') : '',
      'Nome: ' + nome,
      'Empresa: ' + empresa,
      d.get('cidade') ? 'Cidade: ' + d.get('cidade') : '',
      d.get('qtd') ? 'Colaboradores: ' + d.get('qtd') : '',
      linhas.length ? 'Linhas de interesse: ' + linhas.join(', ') : '',
      d.get('mensagem') ? 'Mensagem: ' + d.get('mensagem') : '',
      origem() ? 'Origem: ' + origem() : ''
    ].filter(function (l, i) { return l !== '' || i === 1; }).join('\n');

    evento('envio_orcamento', { canal: canal, colaboradores: d.get('qtd') || '', segmento: form.getAttribute('data-segmento') || 'home' });

    window.open('https://wa.me/' + WHATSAPP + '?text=' + encodeURIComponent(texto), '_blank', 'noopener');
  });
})();
