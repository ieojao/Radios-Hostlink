<?php
class Config {
    private static $config = null;

    public static function get($key = null) {
        if (self::$config === null) {
            self::$config = require_once __DIR__ . '/../config/config.php';
        }

        if ($key === null) {
            return self::$config;
        }

        return self::$config[$key] ?? null;
    }

    public static function getSiteConfig() {
        $db = Database::getInstance();
        $config = $db->fetch("SELECT * FROM configuracoes LIMIT 1");
        
        if (!$config) {
            // Configurações padrão
            return [
                'nome_site' => 'Nova Atalaia',
                'logo' => 'logo.png',
                'favicon' => 'favicon.ico',
                'cor_principal' => '#1e3a8a',
                'cor_fundo' => '#ffffff',
                'cor_texto' => '#333333',
                'cor_botoes' => '#3b82f6',
                'cor_links' => '#1e40af',
                'fonte' => 'Roboto',
                'texto_rodape' => '© 2024 Nova Atalaia. Todos os direitos reservados.',
                'email_contato' => 'contato@novaatalaia.com.br',
                'url_streaming' => 'https://streaming.example.com/live',
                'whatsapp' => '5511999999999',
                'facebook' => 'https://facebook.com/novaatalaia',
                'instagram' => 'https://instagram.com/novaatalaia',
                'youtube' => 'https://youtube.com/novaatalaia',
                'css_custom' => ''
            ];
        }

        return $config;
    }
}
?> 