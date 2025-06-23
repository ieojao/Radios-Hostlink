<?php
// Instalador automático da Rádio Nova Atalaia

// Caminho do SQL
$sqlFile = __DIR__ . '/../database.sql';

function renderForm($error = '') {
    echo '<h2>Instalação da Rádio Nova Atalaia</h2>';
    if ($error) {
        echo '<div style="color:red;">' . $error . '</div>';
    }
    echo '<form method="post">
        <label>Host do Banco de Dados:<br><input type="text" name="db_host" value="localhost" required></label><br><br>
        <label>Nome do Banco de Dados:<br><input type="text" name="db_name" required></label><br><br>
        <label>Usuário do Banco de Dados:<br><input type="text" name="db_user" required></label><br><br>
        <label>Senha do Banco de Dados:<br><input type="password" name="db_pass"></label><br><br>
        <label>Email do Admin:<br><input type="email" name="admin_email" required></label><br><br>
        <label>Senha do Admin:<br><input type="password" name="admin_pass" required></label><br><br>
        <button type="submit">Instalar</button>
    </form>';
}

if ($_SERVER['REQUEST_METHOD'] === 'POST') {
    $db_host = $_POST['db_host'];
    $db_name = $_POST['db_name'];
    $db_user = $_POST['db_user'];
    $db_pass = $_POST['db_pass'];
    $admin_email = $_POST['admin_email'];
    $admin_pass = $_POST['admin_pass'];

    try {
        $pdo = new PDO("mysql:host=$db_host", $db_user, $db_pass, [PDO::ATTR_ERRMODE => PDO::ERRMODE_EXCEPTION]);
        $pdo->exec("CREATE DATABASE IF NOT EXISTS `$db_name` CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci");
        $pdo->exec("USE `$db_name`");
        // Executar SQL do arquivo
        $sql = file_get_contents($sqlFile);
        $pdo->exec($sql);
        // Criar admin
        $hash = password_hash($admin_pass, PASSWORD_DEFAULT);
        $stmt = $pdo->prepare("INSERT INTO usuarios (nome, email, senha, nivel) VALUES (?, ?, ?, 'admin')");
        $stmt->execute(['Administrador', $admin_email, $hash]);
        // Salvar config.php
        $config = "<?php\nreturn [\n    'db_host' => '$db_host',\n    'db_name' => '$db_name',\n    'db_user' => '$db_user',\n    'db_pass' => '$db_pass',\n];\n";
        file_put_contents(__DIR__ . '/../config/config.php', $config);
        echo '<h2>Instalação concluída!</h2>';
        echo '<p>Remova a pasta <b>install</b> por segurança.</p>';
        echo '<a href="../public/index.php">Acessar o site</a>';
        exit;
    } catch (Exception $e) {
        renderForm('Erro: ' . $e->getMessage());
        exit;
    }
} else {
    renderForm();
} 