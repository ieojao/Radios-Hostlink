<?php
// Script de instalação do sistema de rádio web

// Verificar se já foi instalado
if (file_exists('../config/config.php')) {
    die('O sistema já foi instalado. Remova o arquivo install.php se deseja reinstalar.');
}

$erro = '';
$sucesso = '';

if ($_POST) {
    $db_host = trim($_POST['db_host'] ?? '');
    $db_name = trim($_POST['db_name'] ?? '');
    $db_user = trim($_POST['db_user'] ?? '');
    $db_pass = $_POST['db_pass'] ?? '';
    
    $admin_nome = trim($_POST['admin_nome'] ?? '');
    $admin_email = trim($_POST['admin_email'] ?? '');
    $admin_senha = $_POST['admin_senha'] ?? '';
    
    if (empty($db_host) || empty($db_name) || empty($db_user) || 
        empty($admin_nome) || empty($admin_email) || empty($admin_senha)) {
        $erro = 'Por favor, preencha todos os campos.';
    } else {
        try {
            // Testar conexão com banco
            $pdo = new PDO("mysql:host=$db_host;charset=utf8", $db_user, $db_pass);
            $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            
            // Criar banco de dados se não existir
            $pdo->exec("CREATE DATABASE IF NOT EXISTS `$db_name` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
            $pdo->exec("USE `$db_name`");
            
            // Ler e executar SQL do arquivo database.sql
            $sql = file_get_contents('../database.sql');
            $pdo->exec($sql);
            
            // Criar arquivo de configuração
            $config_content = "<?php
return [
    'db_host' => '$db_host',
    'db_name' => '$db_name',
    'db_user' => '$db_user',
    'db_pass' => '$db_pass',
    'site_name' => 'Nova Atalaia',
    'site_email' => '$admin_email',
    'streaming_url' => 'https://streaming.example.com/live',
];
?>";
            
            file_put_contents('../config/config.php', $config_content);
            
            // Conectar ao banco criado
            $pdo = new PDO("mysql:host=$db_host;dbname=$db_name;charset=utf8", $db_user, $db_pass);
            $pdo->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);
            
            // Criar usuário admin
            $senha_hash = password_hash($admin_senha, PASSWORD_DEFAULT);
            $stmt = $pdo->prepare("INSERT INTO usuarios (nome, email, senha, nivel) VALUES (?, ?, ?, 'admin')");
            $stmt->execute([$admin_nome, $admin_email, $senha_hash]);
            
            // Inserir configurações padrão
            $stmt = $pdo->prepare("INSERT INTO configuracoes (nome_site, logo, favicon, cor_principal, cor_fundo, cor_texto, cor_botoes, cor_links, fonte, texto_rodape, email_contato, url_streaming, whatsapp, facebook, instagram, youtube, css_custom) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)");
            $stmt->execute([
                'Nova Atalaia',
                'logo.png',
                'favicon.ico',
                '#1e3a8a',
                '#ffffff',
                '#333333',
                '#3b82f6',
                '#1e40af',
                'Roboto',
                '© 2024 Nova Atalaia. Todos os direitos reservados.',
                $admin_email,
                'https://streaming.example.com/live',
                '5511999999999',
                'https://facebook.com/novaatalaia',
                'https://instagram.com/novaatalaia',
                'https://youtube.com/novaatalaia',
                ''
            ]);
            
            $sucesso = 'Sistema instalado com sucesso! Você pode acessar o painel administrativo em: <a href="../public/admin/login.php">Painel Admin</a>';
            
        } catch (Exception $e) {
            $erro = 'Erro na instalação: ' . $e->getMessage();
        }
    }
}
?>
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Instalação - Sistema de Rádio Web</title>
    <link href="https://fonts.googleapis.com/css?family=Roboto:400,700&display=swap" rel="stylesheet">
    <style>
        * { margin: 0; padding: 0; box-sizing: border-box; }
        body { 
            font-family: 'Roboto', sans-serif; 
            background: linear-gradient(135deg, #1e3a8a, #3b82f6);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .install-container {
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            width: 100%;
            max-width: 600px;
        }
        .logo {
            text-align: center;
            margin-bottom: 30px;
        }
        .logo h1 {
            color: #1e3a8a;
            margin-bottom: 10px;
        }
        .form-grupo {
            margin-bottom: 20px;
        }
        .form-grupo label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: #333;
        }
        .form-grupo input {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
        }
        .form-grupo input:focus {
            border-color: #1e3a8a;
            outline: none;
        }
        .btn-install {
            width: 100%;
            background: #1e3a8a;
            color: white;
            padding: 12px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: background 0.3s;
        }
        .btn-install:hover {
            background: #3b82f6;
        }
        .erro {
            background: #f8d7da;
            color: #721c24;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .sucesso {
            background: #d4edda;
            color: #155724;
            padding: 15px;
            border-radius: 8px;
            margin-bottom: 20px;
        }
        .sucesso a {
            color: #155724;
            font-weight: bold;
        }
        .section {
            border-top: 1px solid #eee;
            padding-top: 20px;
            margin-top: 20px;
        }
        .section h3 {
            color: #1e3a8a;
            margin-bottom: 15px;
        }
    </style>
</head>
<body>
    <div class="install-container">
        <div class="logo">
            <h1>📻 Sistema de Rádio Web</h1>
            <p>Instalação e Configuração</p>
        </div>
        
        <?php if ($erro): ?>
        <div class="erro">
            <?= htmlspecialchars($erro) ?>
        </div>
        <?php endif; ?>
        
        <?php if ($sucesso): ?>
        <div class="sucesso">
            <?= $sucesso ?>
        </div>
        <?php else: ?>
        
        <form method="POST">
            <div class="section">
                <h3>Configuração do Banco de Dados</h3>
                
                <div class="form-grupo">
                    <label for="db_host">Host do MySQL</label>
                    <input type="text" id="db_host" name="db_host" value="localhost" required>
                </div>
                
                <div class="form-grupo">
                    <label for="db_name">Nome do Banco de Dados</label>
                    <input type="text" id="db_name" name="db_name" value="radio_web" required>
                </div>
                
                <div class="form-grupo">
                    <label for="db_user">Usuário do MySQL</label>
                    <input type="text" id="db_user" name="db_user" value="root" required>
                </div>
                
                <div class="form-grupo">
                    <label for="db_pass">Senha do MySQL</label>
                    <input type="password" id="db_pass" name="db_pass">
                </div>
            </div>
            
            <div class="section">
                <h3>Usuário Administrador</h3>
                
                <div class="form-grupo">
                    <label for="admin_nome">Nome do Administrador</label>
                    <input type="text" id="admin_nome" name="admin_nome" required>
                </div>
                
                <div class="form-grupo">
                    <label for="admin_email">E-mail do Administrador</label>
                    <input type="email" id="admin_email" name="admin_email" required>
                </div>
                
                <div class="form-grupo">
                    <label for="admin_senha">Senha do Administrador</label>
                    <input type="password" id="admin_senha" name="admin_senha" required>
                </div>
            </div>
            
            <button type="submit" class="btn-install">Instalar Sistema</button>
        </form>
        
        <?php endif; ?>
    </div>
</body>
</html> 