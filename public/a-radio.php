<?php
require_once __DIR__ . '/../app/Database.php';
require_once __DIR__ . '/../app/Config.php';

$db = Database::getInstance();
$config = Config::getSiteConfig();

// Buscar informações sobre a rádio
$sobre_radio = $db->fetch("SELECT * FROM sobre_radio LIMIT 1");
?>
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Sobre a Rádio - <?= htmlspecialchars($config['nome_site']) ?></title>
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
        .sobre-container { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin: 40px 0; align-items: start; }
        .sobre-texto { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .sobre-texto h2 { color: var(--cor-principal); margin-bottom: 20px; }
        .sobre-texto p { line-height: 1.6; margin-bottom: 15px; color: var(--cor-texto); }
        .sobre-imagem { text-align: center; }
        .sobre-imagem img { max-width: 100%; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .estatisticas { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin: 40px 0; }
        .estatistica { text-align: center; background: var(--cor-principal); color: white; padding: 30px; border-radius: 15px; }
        .estatistica .numero { font-size: 2.5em; font-weight: bold; margin-bottom: 10px; }
        .estatistica .descricao { font-size: 1.1em; }
        @media (max-width: 768px) { .sobre-container { grid-template-columns: 1fr; } }
        <?= $config['css_custom'] ?>
    </style>
</head>
<body>
    <!-- Menu principal -->
    <header>
        <img src="<?= htmlspecialchars($config['logo']) ?>" alt="<?= htmlspecialchars($config['nome_site']) ?>" class="logo">
        <nav>
            <a href="index.php">HOME</a>
            <a href="a-radio.php" class="active">A RÁDIO</a>
            <a href="programacao.php">PROGRAMAÇÃO</a>
            <a href="equipe.php">EQUIPE</a>
            <a href="contato.php">CONTATO</a>
        </nav>
    </header>

    <!-- Banner -->
    <section class="banner">
        <h1>A RÁDIO</h1>
    </section>

    <!-- Sobre a rádio -->
    <section class="sobre">
        <div class="container">
            <div class="sobre-container">
                <!-- Texto sobre a rádio -->
                <div class="sobre-texto">
                    <h2>Sobre a <?= htmlspecialchars($config['nome_site']) ?></h2>
                    
                    <?php if ($sobre_radio): ?>
                        <?= nl2br(htmlspecialchars($sobre_radio['conteudo'])) ?>
                    <?php else: ?>
                        <p>A <?= htmlspecialchars($config['nome_site']) ?> é uma emissora comprometida em levar entretenimento, informação e música de qualidade para nossos ouvintes.</p>
                        
                        <p>Nossa missão é conectar pessoas através da música e da comunicação, oferecendo uma programação diversificada que atende a todos os gostos e idades.</p>
                        
                        <p>Com uma equipe dedicada e profissional, trabalhamos diariamente para proporcionar a melhor experiência radiofônica, mantendo sempre a qualidade e a proximidade com nossa audiência.</p>
                        
                        <p>Estamos sempre em busca de inovação e melhoria, utilizando as mais modernas tecnologias para garantir uma transmissão de excelência.</p>
                    <?php endif; ?>
                </div>
                
                <!-- Imagem da rádio -->
                <div class="sobre-imagem">
                    <?php if ($sobre_radio && $sobre_radio['imagem']): ?>
                        <img src="<?= htmlspecialchars($sobre_radio['imagem']) ?>" alt="<?= htmlspecialchars($config['nome_site']) ?>">
                    <?php else: ?>
                        <img src="../assets/radio-studio.jpg" alt="Estúdio da <?= htmlspecialchars($config['nome_site']) ?>">
                    <?php endif; ?>
                </div>
            </div>
            
            <!-- Estatísticas -->
            <div class="estatisticas">
                <div class="estatistica">
                    <div class="numero">24h</div>
                    <div class="descricao">No ar</div>
                </div>
                <div class="estatistica">
                    <div class="numero">100%</div>
                    <div class="descricao">Qualidade</div>
                </div>
                <div class="estatistica">
                    <div class="numero">7</div>
                    <div class="descricao">Dias por semana</div>
                </div>
                <div class="estatistica">
                    <div class="numero">365</div>
                    <div class="descricao">Dias por ano</div>
                </div>
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
</body>
</html> 