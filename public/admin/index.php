<?php
session_start();
require_once __DIR__ . '/../../app/Database.php';
require_once __DIR__ . '/../../app/Config.php';

// Verificar se está logado
if (!isset($_SESSION['admin_id'])) {
    header('Location: login.php');
    exit;
}

$db = Database::getInstance();
$config = Config::getSiteConfig();

// Estatísticas
$total_banners = $db->fetch("SELECT COUNT(*) as total FROM banners")['total'];
$total_equipe = $db->fetch("SELECT COUNT(*) as total FROM equipe WHERE ativo = 1")['total'];
$total_programacao = $db->fetch("SELECT COUNT(*) as total FROM programacao")['total'];
$total_contatos = $db->fetch("SELECT COUNT(*) as total FROM contatos")['total'];
$contatos_recentes = $db->fetchAll("SELECT * FROM contatos ORDER BY data_envio DESC LIMIT 5");
?>
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Painel Administrativo - <?= htmlspecialchars($config['nome_site']) ?></title>
    <link rel="icon" href="<?= htmlspecialchars($config['favicon']) ?>">
    <link href="https://fonts.googleapis.com/css?family=<?= urlencode($config['fonte']) ?>:400,700&display=swap" rel="stylesheet">
    <style>
        :root {
            --cor-principal: <?= $config['cor_principal'] ?>;
            --cor-fundo: <?= $config['cor_fundo'] ?>;
            --cor-texto: <?= $config['cor_texto'] ?>;
            --cor-botoes: <?= $config['cor_botoes'] ?>;
        }
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: '<?= $config['fonte'] ?>', sans-serif; 
            background: #f5f5f5;
        }
        .header {
            background: var(--cor-principal);
            color: white;
            padding: 20px;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .header h1 {
            font-size: 1.5em;
        }
        .user-info {
            display: flex;
            align-items: center;
            gap: 15px;
        }
        .logout {
            background: rgba(255,255,255,0.2);
            color: white;
            padding: 8px 15px;
            border: none;
            border-radius: 5px;
            text-decoration: none;
            transition: background 0.3s;
        }
        .logout:hover {
            background: rgba(255,255,255,0.3);
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            padding: 20px;
        }
        .stats-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .stat-card {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
        }
        .stat-card .numero {
            font-size: 2.5em;
            font-weight: bold;
            color: var(--cor-principal);
            margin-bottom: 10px;
        }
        .stat-card .titulo {
            color: #666;
            font-size: 1.1em;
        }
        .menu-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .menu-item {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            text-align: center;
            text-decoration: none;
            color: var(--cor-texto);
            transition: transform 0.3s, box-shadow 0.3s;
        }
        .menu-item:hover {
            transform: translateY(-5px);
            box-shadow: 0 5px 20px rgba(0,0,0,0.15);
            color: var(--cor-principal);
        }
        .menu-item .icon {
            font-size: 2em;
            margin-bottom: 10px;
        }
        .contatos-recentes {
            background: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        .contatos-recentes h3 {
            color: var(--cor-principal);
            margin-bottom: 15px;
        }
        .contato-item {
            border-bottom: 1px solid #eee;
            padding: 10px 0;
        }
        .contato-item:last-child {
            border-bottom: none;
        }
        .contato-item .nome {
            font-weight: bold;
            color: var(--cor-texto);
        }
        .contato-item .email {
            color: #666;
            font-size: 0.9em;
        }
        .contato-item .data {
            color: #999;
            font-size: 0.8em;
        }
        .btn {
            background: var(--cor-principal);
            color: white;
            padding: 10px 20px;
            border: none;
            border-radius: 5px;
            text-decoration: none;
            display: inline-block;
            transition: background 0.3s;
        }
        .btn:hover {
            background: var(--cor-botoes);
        }
    </style>
</head>
<body>
    <div class="header">
        <h1>Painel Administrativo - <?= htmlspecialchars($config['nome_site']) ?></h1>
        <div class="user-info">
            <span>Olá, <?= htmlspecialchars($_SESSION['admin_nome']) ?></span>
            <a href="logout.php" class="logout">Sair</a>
        </div>
    </div>

    <div class="container">
        <!-- Estatísticas -->
        <div class="stats-grid">
            <div class="stat-card">
                <div class="numero"><?= $total_banners ?></div>
                <div class="titulo">Banners</div>
            </div>
            <div class="stat-card">
                <div class="numero"><?= $total_equipe ?></div>
                <div class="titulo">Membros da Equipe</div>
            </div>
            <div class="stat-card">
                <div class="numero"><?= $total_programacao ?></div>
                <div class="titulo">Programas</div>
            </div>
            <div class="stat-card">
                <div class="numero"><?= $total_contatos ?></div>
                <div class="titulo">Mensagens</div>
            </div>
        </div>

        <!-- Menu de navegação -->
        <div class="menu-grid">
            <a href="banners.php" class="menu-item">
                <div class="icon">🖼️</div>
                <div>Gerenciar Banners</div>
            </a>
            <a href="equipe.php" class="menu-item">
                <div class="icon">👥</div>
                <div>Gerenciar Equipe</div>
            </a>
            <a href="programacao.php" class="menu-item">
                <div class="icon">📅</div>
                <div>Gerenciar Programação</div>
            </a>
            <a href="contatos.php" class="menu-item">
                <div class="icon">📧</div>
                <div>Ver Mensagens</div>
            </a>
            <a href="configuracoes.php" class="menu-item">
                <div class="icon">⚙️</div>
                <div>Configurações</div>
            </a>
            <a href="../index.php" class="menu-item">
                <div class="icon">🌐</div>
                <div>Ver Site</div>
            </a>
        </div>

        <!-- Contatos recentes -->
        <div class="contatos-recentes">
            <h3>Mensagens Recentes</h3>
            <?php if (!empty($contatos_recentes)): ?>
                <?php foreach ($contatos_recentes as $contato): ?>
                <div class="contato-item">
                    <div class="nome"><?= htmlspecialchars($contato['nome']) ?></div>
                    <div class="email"><?= htmlspecialchars($contato['email']) ?></div>
                    <div class="assunto"><?= htmlspecialchars($contato['assunto']) ?></div>
                    <div class="data"><?= date('d/m/Y H:i', strtotime($contato['data_envio'])) ?></div>
                </div>
                <?php endforeach; ?>
                <div style="margin-top: 15px;">
                    <a href="contatos.php" class="btn">Ver todas as mensagens</a>
                </div>
            <?php else: ?>
                <p>Nenhuma mensagem recebida ainda.</p>
            <?php endif; ?>
        </div>
    </div>
</body>
</html> 