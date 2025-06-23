<?php
session_start();
require_once __DIR__ . '/../../app/Database.php';
require_once __DIR__ . '/../../app/Config.php';

$db = Database::getInstance();
$config = Config::getSiteConfig();

$erro = '';

if ($_POST) {
    $email = trim($_POST['email'] ?? '');
    $senha = $_POST['senha'] ?? '';
    
    if (empty($email) || empty($senha)) {
        $erro = 'Por favor, preencha todos os campos.';
    } else {
        $usuario = $db->fetch("SELECT * FROM usuarios WHERE email = ?", [$email]);
        
        if ($usuario && password_verify($senha, $usuario['senha'])) {
            $_SESSION['admin_id'] = $usuario['id'];
            $_SESSION['admin_nome'] = $usuario['nome'];
            $_SESSION['admin_email'] = $usuario['email'];
            $_SESSION['admin_nivel'] = $usuario['nivel'];
            
            header('Location: index.php');
            exit;
        } else {
            $erro = 'E-mail ou senha incorretos.';
        }
    }
}
?>
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Login - Painel Administrativo</title>
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
            background: linear-gradient(135deg, var(--cor-principal), var(--cor-botoes));
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        .login-container {
            background: white;
            padding: 40px;
            border-radius: 15px;
            box-shadow: 0 10px 30px rgba(0,0,0,0.2);
            width: 100%;
            max-width: 400px;
        }
        .logo {
            text-align: center;
            margin-bottom: 30px;
        }
        .logo img {
            max-width: 150px;
            height: auto;
        }
        .logo h1 {
            color: var(--cor-principal);
            margin-top: 10px;
            font-size: 1.5em;
        }
        .form-grupo {
            margin-bottom: 20px;
        }
        .form-grupo label {
            display: block;
            margin-bottom: 5px;
            font-weight: bold;
            color: var(--cor-texto);
        }
        .form-grupo input {
            width: 100%;
            padding: 12px;
            border: 2px solid #ddd;
            border-radius: 8px;
            font-size: 16px;
        }
        .form-grupo input:focus {
            border-color: var(--cor-principal);
            outline: none;
        }
        .btn-login {
            width: 100%;
            background: var(--cor-principal);
            color: white;
            padding: 12px;
            border: none;
            border-radius: 8px;
            font-size: 16px;
            cursor: pointer;
            transition: background 0.3s;
        }
        .btn-login:hover {
            background: var(--cor-botoes);
        }
        .erro {
            background: #f8d7da;
            color: #721c24;
            padding: 10px;
            border-radius: 5px;
            margin-bottom: 20px;
            text-align: center;
        }
        .voltar {
            text-align: center;
            margin-top: 20px;
        }
        .voltar a {
            color: var(--cor-principal);
            text-decoration: none;
        }
        .voltar a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="login-container">
        <div class="logo">
            <img src="<?= htmlspecialchars($config['logo']) ?>" alt="<?= htmlspecialchars($config['nome_site']) ?>">
            <h1>Painel Administrativo</h1>
        </div>
        
        <?php if ($erro): ?>
        <div class="erro">
            <?= htmlspecialchars($erro) ?>
        </div>
        <?php endif; ?>
        
        <form method="POST">
            <div class="form-grupo">
                <label for="email">E-mail</label>
                <input type="email" id="email" name="email" value="<?= htmlspecialchars($_POST['email'] ?? '') ?>" required>
            </div>
            
            <div class="form-grupo">
                <label for="senha">Senha</label>
                <input type="password" id="senha" name="senha" required>
            </div>
            
            <button type="submit" class="btn-login">Entrar</button>
        </form>
        
        <div class="voltar">
            <a href="../index.php">← Voltar ao site</a>
        </div>
    </div>
</body>
</html> 