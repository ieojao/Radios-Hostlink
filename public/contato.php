<?php
require_once __DIR__ . '/../app/Database.php';
require_once __DIR__ . '/../app/Config.php';

$db = Database::getInstance();
$config = Config::getSiteConfig();

$mensagem = '';
$tipo_mensagem = '';

if ($_POST) {
    $nome = trim($_POST['nome'] ?? '');
    $email = trim($_POST['email'] ?? '');
    $assunto = trim($_POST['assunto'] ?? '');
    $mensagem_texto = trim($_POST['mensagem'] ?? '');
    
    if (empty($nome) || empty($email) || empty($assunto) || empty($mensagem_texto)) {
        $mensagem = 'Por favor, preencha todos os campos.';
        $tipo_mensagem = 'erro';
    } elseif (!filter_var($email, FILTER_VALIDATE_EMAIL)) {
        $mensagem = 'Por favor, insira um e-mail válido.';
        $tipo_mensagem = 'erro';
    } else {
        // Salvar no banco de dados
        try {
            $db->query(
                "INSERT INTO contatos (nome, email, assunto, mensagem, data_envio) VALUES (?, ?, ?, ?, NOW())",
                [$nome, $email, $assunto, $mensagem_texto]
            );
            
            // Enviar e-mail (se configurado)
            if ($config['email_contato']) {
                $headers = "From: $email\r\n";
                $headers .= "Reply-To: $email\r\n";
                $headers .= "Content-Type: text/html; charset=UTF-8\r\n";
                
                $corpo_email = "
                <h2>Nova mensagem de contato</h2>
                <p><strong>Nome:</strong> $nome</p>
                <p><strong>E-mail:</strong> $email</p>
                <p><strong>Assunto:</strong> $assunto</p>
                <p><strong>Mensagem:</strong></p>
                <p>" . nl2br(htmlspecialchars($mensagem_texto)) . "</p>
                ";
                
                mail($config['email_contato'], "Contato via site: $assunto", $corpo_email, $headers);
            }
            
            $mensagem = 'Mensagem enviada com sucesso! Entraremos em contato em breve.';
            $tipo_mensagem = 'sucesso';
            
            // Limpar campos
            $_POST = [];
            
        } catch (Exception $e) {
            $mensagem = 'Erro ao enviar mensagem. Tente novamente.';
            $tipo_mensagem = 'erro';
        }
    }
}
?>
<!DOCTYPE html>
<html lang="pt-br">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Contato - <?= htmlspecialchars($config['nome_site']) ?></title>
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
        .contato-container { display: grid; grid-template-columns: 1fr 1fr; gap: 40px; margin: 40px 0; }
        .formulario { background: white; padding: 30px; border-radius: 15px; box-shadow: 0 4px 15px rgba(0,0,0,0.1); }
        .form-grupo { margin-bottom: 20px; }
        .form-grupo label { display: block; margin-bottom: 5px; font-weight: bold; color: var(--cor-texto); }
        .form-grupo input, .form-grupo textarea { width: 100%; padding: 12px; border: 2px solid #ddd; border-radius: 8px; font-size: 16px; }
        .form-grupo input:focus, .form-grupo textarea:focus { border-color: var(--cor-principal); outline: none; }
        .form-grupo textarea { height: 120px; resize: vertical; }
        .btn-enviar { background: var(--cor-principal); color: white; padding: 12px 30px; border: none; border-radius: 8px; font-size: 16px; cursor: pointer; }
        .btn-enviar:hover { background: var(--cor-botoes); }
        .mensagem { padding: 15px; border-radius: 8px; margin-bottom: 20px; }
        .mensagem.sucesso { background: #d4edda; color: #155724; border: 1px solid #c3e6cb; }
        .mensagem.erro { background: #f8d7da; color: #721c24; border: 1px solid #f5c6cb; }
        .info-contato { background: var(--cor-principal); color: white; padding: 30px; border-radius: 15px; }
        .info-item { margin-bottom: 20px; }
        .info-item h3 { margin-bottom: 10px; }
        .info-item a { color: white; text-decoration: none; }
        .info-item a:hover { text-decoration: underline; }
        @media (max-width: 768px) { .contato-container { grid-template-columns: 1fr; } }
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
            <a href="equipe.php">EQUIPE</a>
            <a href="contato.php" class="active">CONTATO</a>
        </nav>
    </header>

    <!-- Banner -->
    <section class="banner">
        <h1>CONTATO</h1>
    </section>

    <!-- Formulário de contato -->
    <section class="contato">
        <div class="container">
            <div class="contato-container">
                <!-- Formulário -->
                <div class="formulario">
                    <h2>Envie sua mensagem</h2>
                    
                    <?php if ($mensagem): ?>
                    <div class="mensagem <?= $tipo_mensagem ?>">
                        <?= htmlspecialchars($mensagem) ?>
                    </div>
                    <?php endif; ?>
                    
                    <form method="POST">
                        <div class="form-grupo">
                            <label for="nome">Nome completo *</label>
                            <input type="text" id="nome" name="nome" value="<?= htmlspecialchars($_POST['nome'] ?? '') ?>" required>
                        </div>
                        
                        <div class="form-grupo">
                            <label for="email">E-mail *</label>
                            <input type="email" id="email" name="email" value="<?= htmlspecialchars($_POST['email'] ?? '') ?>" required>
                        </div>
                        
                        <div class="form-grupo">
                            <label for="assunto">Assunto *</label>
                            <input type="text" id="assunto" name="assunto" value="<?= htmlspecialchars($_POST['assunto'] ?? '') ?>" required>
                        </div>
                        
                        <div class="form-grupo">
                            <label for="mensagem">Mensagem *</label>
                            <textarea id="mensagem" name="mensagem" required><?= htmlspecialchars($_POST['mensagem'] ?? '') ?></textarea>
                        </div>
                        
                        <button type="submit" class="btn-enviar">Enviar mensagem</button>
                    </form>
                </div>
                
                <!-- Informações de contato -->
                <div class="info-contato">
                    <h2>Informações de contato</h2>
                    
                    <?php if ($config['email_contato']): ?>
                    <div class="info-item">
                        <h3>📧 E-mail</h3>
                        <a href="mailto:<?= htmlspecialchars($config['email_contato']) ?>">
                            <?= htmlspecialchars($config['email_contato']) ?>
                        </a>
                    </div>
                    <?php endif; ?>
                    
                    <?php if ($config['whatsapp']): ?>
                    <div class="info-item">
                        <h3>💬 WhatsApp</h3>
                        <a href="https://wa.me/<?= htmlspecialchars($config['whatsapp']) ?>" target="_blank">
                            <?= htmlspecialchars($config['whatsapp']) ?>
                        </a>
                    </div>
                    <?php endif; ?>
                    
                    <?php if ($config['facebook']): ?>
                    <div class="info-item">
                        <h3>📘 Facebook</h3>
                        <a href="<?= htmlspecialchars($config['facebook']) ?>" target="_blank">
                            Siga-nos no Facebook
                        </a>
                    </div>
                    <?php endif; ?>
                    
                    <?php if ($config['instagram']): ?>
                    <div class="info-item">
                        <h3>📷 Instagram</h3>
                        <a href="<?= htmlspecialchars($config['instagram']) ?>" target="_blank">
                            Siga-nos no Instagram
                        </a>
                    </div>
                    <?php endif; ?>
                    
                    <?php if ($config['youtube']): ?>
                    <div class="info-item">
                        <h3>📺 YouTube</h3>
                        <a href="<?= htmlspecialchars($config['youtube']) ?>" target="_blank">
                            Inscreva-se no canal
                        </a>
                    </div>
                    <?php endif; ?>
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