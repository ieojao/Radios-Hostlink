<?php
require_once __DIR__ . '/../app/Database.php';
require_once __DIR__ . '/../app/Config.php';

$db = Database::getInstance();
$config = Config::getSiteConfig();

$dias = [
    1 => 'SEGUNDA',
    2 => 'TERÇA', 
    3 => 'QUARTA',
    4 => 'QUINTA',
    5 => 'SEXTA',
    6 => 'SÁBADO',
    7 => 'DOMINGO'
];

$dia_atual = isset($_GET['dia']) ? (int)$_GET['dia'] : date('N');
$programacao = $db->fetchAll("SELECT * FROM programacao WHERE dia_semana = ? ORDER BY hora_inicio", [$dia_atual]);
?>
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Programação - <?= htmlspecialchars($config['nome_site']) ?></title>
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
        .tabs { display: flex; justify-content: center; gap: 10px; margin: 20px 0; flex-wrap: wrap; }
        .tab { padding: 10px 20px; border: none; background: #f0f0f0; cursor: pointer; border-radius: 5px; }
        .tab.active { background: var(--cor-principal); color: white; }
        .programacao-grid { display: grid; gap: 15px; margin: 20px 0; }
        .programa-item { display: flex; align-items: center; padding: 15px; background: white; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }
        .programa-hora { font-weight: bold; color: var(--cor-principal); min-width: 80px; }
        .programa-info h3 { margin: 0 0 5px 0; color: var(--cor-texto); }
        .programa-info p { margin: 0; color: #666; }
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
            <a href="programacao.php" class="active">PROGRAMAÇÃO</a>
            <a href="equipe.php">EQUIPE</a>
            <a href="contato.php">CONTATO</a>
        </nav>
    </header>

    <!-- Banner -->
    <section class="banner">
        <h1>PROGRAMAÇÃO</h1>
    </section>

    <!-- Tabs de dias da semana -->
    <section class="programacao">
        <div class="container">
            <div class="tabs">
                <?php foreach ($dias as $num => $nome): ?>
                <button class="tab <?= $num == $dia_atual ? 'active' : '' ?>" 
                        onclick="window.location.href='?dia=<?= $num ?>'">
                    <?= $nome ?>
                </button>
                <?php endforeach; ?>
            </div>

            <div class="programacao-grid">
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
                    <p style="text-align: center; color: #666;">Nenhuma programação cadastrada para este dia.</p>
                <?php endif; ?>
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