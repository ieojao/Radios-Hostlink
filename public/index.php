<?php
// Página inicial do site público
require_once __DIR__ . '/../config/config.php';
require_once __DIR__ . '/../app/Database.php';
require_once __DIR__ . '/../app/Config.php';

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

$db = Database::getInstance();
$config = Config::getSiteConfig();

// Buscar dados dinâmicos
$banners = $db->fetchAll("SELECT * FROM banners WHERE ativo = 1 ORDER BY ordem");
$programacao = $db->fetchAll("SELECT * FROM programacao WHERE dia_semana = ? ORDER BY hora_inicio", [date('N')]);
$equipe = $db->fetchAll("SELECT * FROM equipe WHERE ativo = 1 ORDER BY nome");
?>
<!DOCTYPE html>
<html lang="pt-br">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title><?= htmlspecialchars($config['nome_site']) ?></title>
  <link rel="icon" href="<?= htmlspecialchars($config['favicon']) ?>">
  <link rel="stylesheet" href="../styles.css">
  <link href="https://fonts.googleapis.com/css?family=<?= urlencode($config['fonte']) ?>:400,700&display=swap" rel="stylesheet">
  <style>
    :root {
      --cor-principal: <?= $config['cor_principal'] ?>;
      --cor-fundo: <?= $config['cor_fundo'] ?>;
      --cor-texto: <?= $config['cor_texto'] ?>;
      --cor-botoes: <?= $config['cor_botoes'] ?>;
      --cor-links: <?= $config['cor_links'] ?>;
    }
    body { font-family: '<?= $config['fonte'] ?>', sans-serif; }
    <?= $config['css_custom'] ?>
  </style>
</head>
<body>
  <!-- Player superior -->
  <div class="player-bar">
    <div class="player-info">
      <span class="icon-play">▶</span>
      <div>
        <span class="music-title">AO VIVO</span><br>
        <span class="music-genre"><?= htmlspecialchars($config['nome_site']) ?></span>
      </div>
    </div>
    <div class="player-controls">
      <span class="icon-radio">📻</span>
      <span class="timer">00:00</span>
    </div>
  </div>

  <!-- Menu principal -->
  <header>
    <img src="<?= htmlspecialchars($config['logo']) ?>" alt="<?= htmlspecialchars($config['nome_site']) ?>" class="logo">
    <nav>
      <a href="index.php" class="active">HOME</a>
      <a href="a-radio.php">A RÁDIO</a>
      <a href="programacao.php">PROGRAMAÇÃO</a>
      <a href="equipe.php">EQUIPE</a>
      <a href="contato.php">CONTATO</a>
    </nav>
    <div class="header-buttons">
      <button class="menu-btn">☰</button>
      <button class="play-btn" onclick="togglePlayer()">▶ PLAY</button>
      <button class="sound-btn" onclick="toggleMute()">🔊</button>
      <button class="popup-btn" onclick="openPlayer()">🎵 POPUP</button>
    </div>
  </header>

  <!-- Banner principal -->
  <?php if (!empty($banners)): ?>
  <section class="banner">
    <div class="banner-slider">
      <?php foreach ($banners as $banner): ?>
      <div class="banner-item">
        <img src="<?= htmlspecialchars($banner['imagem']) ?>" alt="<?= htmlspecialchars($banner['titulo']) ?>">
        <div class="banner-content">
          <h1><?= htmlspecialchars($banner['titulo']) ?></h1>
          <p><?= htmlspecialchars($banner['descricao']) ?></p>
        </div>
      </div>
      <?php endforeach; ?>
    </div>
  </section>
  <?php endif; ?>

  <!-- Programação atual -->
  <section class="programacao-atual">
    <div class="container">
      <h2>PROGRAMAÇÃO ATUAL</h2>
      <?php if (!empty($programacao)): ?>
        <?php foreach ($programacao as $programa): ?>
        <div class="programa-item">
          <div class="programa-hora"><?= htmlspecialchars($programa['hora_inicio']) ?></div>
          <div class="programa-info">
            <h3><?= htmlspecialchars($programa['titulo']) ?></h3>
            <p><?= htmlspecialchars($programa['descricao']) ?></p>
          </div>
        </div>
        <?php endforeach; ?>
      <?php else: ?>
        <p>Nenhuma programação cadastrada para hoje.</p>
      <?php endif; ?>
    </div>
  </section>

  <!-- Equipe -->
  <section class="equipe">
    <div class="container">
      <h2>NOSSA EQUIPE</h2>
      <div class="equipe-grid">
        <?php foreach ($equipe as $membro): ?>
        <div class="membro">
          <img src="<?= htmlspecialchars($membro['foto']) ?>" alt="<?= htmlspecialchars($membro['nome']) ?>">
          <h3><?= htmlspecialchars($membro['nome']) ?></h3>
          <p><?= htmlspecialchars($membro['cargo']) ?></p>
        </div>
        <?php endforeach; ?>
      </div>
    </div>
  </section>

  <!-- Rodapé -->
  <footer>
    <div class="container">
      <div class="footer-content">
        <div class="footer-info">
          <img src="<?= htmlspecialchars($config['logo']) ?>" alt="<?= htmlspecialchars($config['nome_site']) ?>" class="footer-logo">
          <p><?= htmlspecialchars($config['texto_rodape']) ?></p>
        </div>
        <div class="footer-social">
          <?php if ($config['facebook']): ?>
          <a href="<?= htmlspecialchars($config['facebook']) ?>" target="_blank">📘 Facebook</a>
          <?php endif; ?>
          <?php if ($config['instagram']): ?>
          <a href="<?= htmlspecialchars($config['instagram']) ?>" target="_blank">📷 Instagram</a>
          <?php endif; ?>
          <?php if ($config['youtube']): ?>
          <a href="<?= htmlspecialchars($config['youtube']) ?>" target="_blank">📺 YouTube</a>
          <?php endif; ?>
        </div>
      </div>
    </div>
  </footer>

  <!-- Botão WhatsApp -->
  <?php if ($config['whatsapp']): ?>
  <a href="https://wa.me/<?= htmlspecialchars($config['whatsapp']) ?>" class="whatsapp-btn" target="_blank">💬</a>
  <?php endif; ?>

  <!-- Player de áudio -->
  <audio id="player" preload="none">
    <source src="<?= htmlspecialchars($config['url_streaming']) ?>" type="audio/mpeg">
  </audio>

  <script>
    let player = document.getElementById('player');
    let isPlaying = false;

    function togglePlayer() {
      if (isPlaying) {
        player.pause();
        isPlaying = false;
        document.querySelector('.play-btn').textContent = '▶ PLAY';
      } else {
        player.play();
        isPlaying = true;
        document.querySelector('.play-btn').textContent = '⏸ PAUSE';
      }
    }

    function toggleMute() {
      player.muted = !player.muted;
      document.querySelector('.sound-btn').textContent = player.muted ? '🔇' : '🔊';
    }

    function openPlayer() {
      window.open('player.php', 'player', 'width=400,height=300');
    }

    // Atualizar timer
    setInterval(() => {
      if (isPlaying) {
        let time = Math.floor(player.currentTime);
        let minutes = Math.floor(time / 60);
        let seconds = time % 60;
        document.querySelector('.timer').textContent = 
          `${minutes.toString().padStart(2, '0')}:${seconds.toString().padStart(2, '0')}`;
      }
    }, 1000);
  </script>
</body>
</html> 