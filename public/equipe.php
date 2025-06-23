<?php
require_once __DIR__ . '/../app/Database.php';
require_once __DIR__ . '/../app/Config.php';

$db = Database::getInstance();
$config = Config::getSiteConfig();

$equipe = $db->fetchAll("SELECT * FROM equipe WHERE ativo = 1 ORDER BY nome");
?>
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Equipe - <?= htmlspecialchars($config['nome_site']) ?></title>
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
        .equipe-grid { display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 30px; margin: 40px 0; }
        .membro { text-align: center; background: white; border-radius: 15px; padding: 20px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); transition: transform 0.3s; }
        .membro:hover { transform: translateY(-5px); }
        .membro img { width: 150px; height: 150px; border-radius: 50%; object-fit: cover; margin-bottom: 15px; border: 3px solid var(--cor-principal); }
        .membro h3 { color: var(--cor-principal); margin: 10px 0; }
        .membro p { color: #666; margin: 5px 0; }
        .membro .redes { margin-top: 15px; }
        .membro .redes a { margin: 0 5px; font-size: 20px; text-decoration: none; }
        <?= $config['css_custom'] ?>
    </style>
</head>
<body>
    <!-- Menu principal -->
    <header>
        <img src="<?= htmlspecialchars($config['logo']) ?>" alt="<?= htmlspecialchars($config['nome_site']) ?>" class="logo">
        <nav>
            <a href="index.php">HOME</a>
            <a href="a-radio.php">A RÁDIO</a>
            <a href="programacao.php">PROGRAMAÇÃO</a>
            <a href="equipe.php" class="active">EQUIPE</a>
            <a href="contato.php">CONTATO</a>
        </nav>
    </header>

    <!-- Banner -->
    <section class="banner">
        <h1>NOSSA EQUIPE</h1>
    </section>

    <!-- Equipe -->
    <section class="equipe">
        <div class="container">
            <?php if (!empty($equipe)): ?>
                <div class="equipe-grid">
                    <?php foreach ($equipe as $membro): ?>
                    <div class="membro">
                        <img src="<?= htmlspecialchars($membro['foto']) ?>" alt="<?= htmlspecialchars($membro['nome']) ?>">
                        <h3><?= htmlspecialchars($membro['nome']) ?></h3>
                        <p><strong><?= htmlspecialchars($membro['cargo']) ?></strong></p>
                        <?php if ($membro['descricao']): ?>
                        <p><?= htmlspecialchars($membro['descricao']) ?></p>
                        <?php endif; ?>
                        <?php if ($membro['facebook'] || $membro['instagram'] || $membro['twitter']): ?>
                        <div class="redes">
                            <?php if ($membro['facebook']): ?>
                            <a href="<?= htmlspecialchars($membro['facebook']) ?>" target="_blank">📘</a>
                            <?php endif; ?>
                            <?php if ($membro['instagram']): ?>
                            <a href="<?= htmlspecialchars($membro['instagram']) ?>" target="_blank">📷</a>
                            <?php endif; ?>
                            <?php if ($membro['twitter']): ?>
                            <a href="<?= htmlspecialchars($membro['twitter']) ?>" target="_blank">🐦</a>
                            <?php endif; ?>
                        </div>
                        <?php endif; ?>
                    </div>
                    <?php endforeach; ?>
                </div>
            <?php else: ?>
                <p style="text-align: center; color: #666; margin: 40px 0;">Nenhum membro da equipe cadastrado ainda.</p>
            <?php endif; ?>
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
</body>
</html> 