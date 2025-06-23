<?php
// Página inicial do site público
require_once __DIR__ . '/../config/config.php';

function getPDO() {
    $config = require __DIR__ . '/../config/config.php';
    return new PDO(
        "mysql:host=" . $config['db_host'] . ";dbname=" . $config['db_name'],
        $config['db_user'],
        $config['db_pass'],
        [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]
    );
}

function getConfig($chave, $padrao = '') {
    static $pdo = null;
    if (!$pdo) $pdo = getPDO();
    $stmt = $pdo->prepare('SELECT valor FROM configuracoes WHERE chave = ?');
    $stmt->execute([$chave]);
    $v = $stmt->fetchColumn();
    return $v !== false ? $v : $padrao;
}
$site_nome = getConfig('site_nome', 'Rádio Nova Atalaia');
$site_logo = getConfig('site_logo', 'logo.png');
$cor_principal = getConfig('cor_principal', '#005080');
$cor_fundo = getConfig('cor_fundo', '#f5f5f5');
$cor_texto = getConfig('cor_texto', '#222');
$cor_texto_sec = getConfig('cor_texto_sec', '#888');
$cor_botao = getConfig('cor_botao', $cor_principal);
$cor_link = getConfig('cor_link', $cor_principal);
$cor_link_hover = getConfig('cor_link_hover', '#e00');
$fonte_site = getConfig('fonte_site', 'Roboto');
$site_favicon = getConfig('site_favicon', '');
$stream_url = getConfig('stream_url', '');
$rodape_texto = getConfig('rodape_texto', 'Todos os direitos reservados.');
$css_custom = getConfig('css_custom', '');
$rede_facebook = getConfig('rede_facebook', '');
$rede_instagram = getConfig('rede_instagram', '');
$rede_youtube = getConfig('rede_youtube', '');
$rede_twitter = getConfig('rede_twitter', '');
$rede_whatsapp = getConfig('rede_whatsapp', '');
$pdo = getPDO();
$banners = $pdo->query('SELECT * FROM banners ORDER BY id DESC')->fetchAll(PDO::FETCH_ASSOC);
?><!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <title><?= htmlspecialchars($site_nome) ?></title>
  <?php if ($site_favicon): ?>
    <link rel="icon" href="<?= htmlspecialchars($site_favicon) ?>">
  <?php endif; ?>
  <link rel="stylesheet" href="styles.css">
  <link href="https://fonts.googleapis.com/css?family=<?= urlencode($fonte_site) ?>:400,700&display=swap" rel="stylesheet">
  <style>
    body { background: <?= htmlspecialchars($cor_fundo) ?>; color: <?= htmlspecialchars($cor_texto) ?>; font-family: '<?= htmlspecialchars($fonte_site) ?>', Arial, sans-serif; }
    .banner, .header-buttons button, nav a.active { background: <?= htmlspecialchars($cor_principal) ?> !important; }
    nav a.active, .header-buttons button, .banner h1 { color: #fff !important; }
    .player-dinamico { display: flex; align-items: center; gap: 16px; background: #222; color: #fff; padding: 12px 24px; }
    .player-dinamico button { background: <?= htmlspecialchars($cor_botao) ?>; color: #fff; border: none; border-radius: 50%; width: 40px; height: 40px; font-size: 20px; cursor: pointer; }
    .player-dinamico .titulo { font-weight: bold; margin-left: 12px; }
    .player-dinamico audio { display: none; }
    .banners-home { display: flex; flex-wrap: wrap; gap: 24px; justify-content: center; margin: 32px 0; }
    .banner-card { background: #fff; border-radius: 12px; box-shadow: 0 2px 8px #0001; padding: 0; overflow: hidden; width: 340px; text-align: center; transition: box-shadow .2s; }
    .banner-card:hover { box-shadow: 0 4px 16px #0002; }
    .banner-card img { width: 100%; height: 180px; object-fit: cover; display: block; }
    .banner-card .titulo { font-weight: bold; font-size: 18px; margin: 12px 0 8px 0; color: <?= htmlspecialchars($cor_principal) ?>; }
    .banner-card .link { display: inline-block; margin-bottom: 12px; color: #fff; background: <?= htmlspecialchars($cor_principal) ?>; padding: 6px 18px; border-radius: 20px; text-decoration: none; font-size: 15px; }
    a { color: <?= htmlspecialchars($cor_link) ?>; }
    a:hover { color: <?= htmlspecialchars($cor_link_hover) ?>; }
    .footer { background: <?= htmlspecialchars($cor_principal) ?>; color: #fff; text-align: center; padding: 24px 10px 10px 10px; margin-top: 40px; border-radius: 16px 16px 0 0; }
    .footer .redes { margin: 12px 0; }
    .footer .redes a { color: #fff; margin: 0 8px; font-size: 22px; text-decoration: none; transition: color .2s; }
    .footer .redes a:hover { color: <?= htmlspecialchars($cor_link_hover) ?>; }
    <?= $css_custom ?>
  </style>
</head>
<body>
  <!-- Player dinâmico -->
  <?php if ($stream_url): ?>
    <div class="player-dinamico" id="player-dinamico">
      <button id="playpause">▶</button>
      <span class="titulo">AO VIVO</span>
      <audio id="audio-player" src="<?= htmlspecialchars($stream_url) ?>"></audio>
    </div>
    <script>
      const audio = document.getElementById('audio-player');
      const btn = document.getElementById('playpause');
      let playing = false;
      btn.onclick = function() {
        if (playing) {
          audio.pause();
          btn.textContent = '▶';
        } else {
          audio.play();
          btn.textContent = '⏸';
        }
        playing = !playing;
      };
      audio.onended = function() {
        btn.textContent = '▶';
        playing = false;
      };
    </script>
  <?php else: ?>
    <div class="player-dinamico" style="background:#e00;">Streaming não configurado</div>
  <?php endif; ?>

  <!-- Banners dinâmicos -->
  <?php if ($banners && count($banners)): ?>
    <div class="banners-home">
      <?php foreach ($banners as $b): ?>
        <div class="banner-card">
          <?php if ($b['imagem']): ?>
            <img src="<?= htmlspecialchars($b['imagem']) ?>" alt="<?= htmlspecialchars($b['titulo']) ?>">
          <?php endif; ?>
          <div class="titulo"><?= htmlspecialchars($b['titulo']) ?></div>
          <?php if ($b['link']): ?>
            <a href="<?= htmlspecialchars($b['link']) ?>" class="link" target="_blank">Saiba mais</a>
          <?php endif; ?>
        </div>
      <?php endforeach; ?>
    </div>
  <?php endif; ?>

  <!-- Player superior antigo -->
  <div class="player-bar">
    <div class="player-info">
      <span class="icon-play">▶</span>
      <div>
        <span class="music-title">LOUVOR</span><br>
        <span class="music-genre">GOSPEL</span>
      </div>
    </div>
    <div class="player-controls">
      <span class="icon-radio">📻</span>
      <span class="timer">00:00</span>
    </div>
  </div>

  <!-- Menu principal -->
  <header>
    <?php if ($site_logo): ?>
      <img src="<?= htmlspecialchars($site_logo) ?>" alt="<?= htmlspecialchars($site_nome) ?>" class="logo">
    <?php endif; ?>
    <nav>
      <a href="index.php" class="active">HOME</a>
      <a href="a-radio.html">A RÁDIO</a>
      <a href="programacao.html">PROGRAMAÇÃO</a>
      <a href="equipe.html">EQUIPE</a>
      <a href="contato.html">CONTATO</a>
    </nav>
    <div class="header-buttons">
      <button class="menu-btn">☰</button>
      <button class="play-btn">▶ PLAY</button>
      <button class="sound-btn">🔊</button>
      <button class="popup-btn">🎵 POPUP</button>
    </div>
  </header>

  <!-- Banner de programação -->
  <section class="banner">
    <h1><?= htmlspecialchars($site_nome) ?></h1>
  </section>

  <!-- Tabs de dias da semana -->
  <section class="programacao">
    <div class="tabs">
      <button class="tab active">DOMINGO</button>
      <button class="tab">SEGUNDA</button>
      <button class="tab">TERÇA</button>
      <button class="tab">QUARTA</button>
      <button class="tab">QUINTA</button>
      <button class="tab">SEXTA</button>
      <button class="tab">SÁBADO</button>
    </div>
    <div class="programa-atual">
      <img src="programa.jpg" alt="Programação musical">
      <div>
        <span class="rolando-agora">ROLANDO AGORA</span>
        <h2>Programação musical</h2>
      </div>
    </div>
  </section>

  <!-- Rodapé dinâmico -->
  <footer class="footer">
    <div class="redes">
      <?php if ($rede_facebook): ?><a href="<?= htmlspecialchars($rede_facebook) ?>" target="_blank" title="Facebook">&#x1F426;</a><?php endif; ?>
      <?php if ($rede_instagram): ?><a href="<?= htmlspecialchars($rede_instagram) ?>" target="_blank" title="Instagram">&#x1F33A;</a><?php endif; ?>
      <?php if ($rede_youtube): ?><a href="<?= htmlspecialchars($rede_youtube) ?>" target="_blank" title="YouTube">&#x1F4FA;</a><?php endif; ?>
      <?php if ($rede_twitter): ?><a href="<?= htmlspecialchars($rede_twitter) ?>" target="_blank" title="Twitter">&#x1F426;</a><?php endif; ?>
      <?php if ($rede_whatsapp): ?><a href="<?= htmlspecialchars($rede_whatsapp) ?>" target="_blank" title="WhatsApp">&#x1F4AC;</a><?php endif; ?>
    </div>
    <div><?= nl2br(htmlspecialchars($rodape_texto)) ?></div>
  </footer>

  <!-- Botão WhatsApp -->
  <a href="https://wa.me/SEUNUMERO" class="whatsapp-btn">💬</a>
</body>
</html> 