# 🚀 Guia de Deploy - Sistema de Rádio Web

Este guia irá ajudá-lo a fazer o deploy do sistema de rádio web em diferentes ambientes.

## 📋 Pré-requisitos

### Servidor Web
- **Apache 2.4+** ou **Nginx 1.18+**
- **PHP 7.4+** com as seguintes extensões:
  - PDO
  - PDO_MySQL
  - mbstring
  - json
  - session
  - fileinfo
  - gd (para processamento de imagens)
- **MySQL 5.7+** ou **MariaDB 10.2+**

### Recursos Mínimos
- **RAM**: 512MB
- **Espaço em disco**: 1GB
- **CPU**: 1 core

## 🌐 Deploy em Hosting Compartilhado

### 1. Preparação
```bash
# Faça download do projeto
git clone https://github.com/seu-usuario/radios-hostlink.git
cd radios-hostlink

# Ou faça upload via FTP/SFTP
```

### 2. Upload dos Arquivos
1. **Via FTP/SFTP**: Faça upload de todos os arquivos para a pasta `public_html` ou `www`
2. **Via cPanel**: Use o gerenciador de arquivos para fazer upload
3. **Via SSH**: Use `scp` ou `rsync`

### 3. Configuração do Banco
1. Acesse o painel do seu hosting
2. Crie um banco de dados MySQL
3. Anote as credenciais (host, nome, usuário, senha)

### 4. Instalação
1. Acesse: `http://seudominio.com/install/install.php`
2. Preencha as informações do banco de dados
3. Crie o usuário administrador
4. Clique em "Instalar Sistema"

### 5. Configuração Final
1. Acesse o painel admin: `http://seudominio.com/public/admin/login.php`
2. Configure as informações básicas do site
3. Adicione banners, equipe e programação
4. Remova a pasta `install` por segurança

## 🐳 Deploy com Docker

### 1. Dockerfile
```dockerfile
FROM php:8.1-apache

# Instalar extensões PHP
RUN docker-php-ext-install pdo pdo_mysql mbstring

# Instalar dependências
RUN apt-get update && apt-get install -y \
    libpng-dev \
    libjpeg-dev \
    libfreetype6-dev \
    && docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install gd

# Configurar Apache
RUN a2enmod rewrite
COPY public/.htaccess /var/www/html/.htaccess

# Copiar arquivos
COPY . /var/www/html/

# Configurar permissões
RUN chown -R www-data:www-data /var/www/html \
    && chmod -R 755 /var/www/html

EXPOSE 80
```

### 2. Docker Compose
```yaml
version: '3.8'

services:
  web:
    build: .
    ports:
      - "80:80"
    depends_on:
      - db
    environment:
      - DB_HOST=db
      - DB_NAME=radio_web
      - DB_USER=radio_user
      - DB_PASS=radio_pass
    volumes:
      - ./uploads:/var/www/html/uploads

  db:
    image: mysql:8.0
    environment:
      MYSQL_DATABASE: radio_web
      MYSQL_USER: radio_user
      MYSQL_PASSWORD: radio_pass
      MYSQL_ROOT_PASSWORD: root_pass
    volumes:
      - db_data:/var/lib/mysql
    ports:
      - "3306:3306"

volumes:
  db_data:
```

### 3. Executar
```bash
docker-compose up -d
```

## ☁️ Deploy na AWS

### 1. EC2 com Amazon Linux 2
```bash
# Atualizar sistema
sudo yum update -y

# Instalar Apache
sudo yum install httpd -y
sudo systemctl start httpd
sudo systemctl enable httpd

# Instalar PHP
sudo amazon-linux-extras install php8.1 -y
sudo yum install php-pdo php-mysqlnd php-mbstring php-gd -y

# Instalar MySQL
sudo yum install mysql-server -y
sudo systemctl start mysqld
sudo systemctl enable mysqld

# Configurar MySQL
sudo mysql_secure_installation
```

### 2. Configurar Apache
```bash
# Habilitar mod_rewrite
sudo a2enmod rewrite

# Configurar virtual host
sudo nano /etc/httpd/conf.d/radio.conf
```

```apache
<VirtualHost *:80>
    ServerName seudominio.com
    DocumentRoot /var/www/html/public
    
    <Directory /var/www/html/public>
        AllowOverride All
        Require all granted
    </Directory>
    
    ErrorLog logs/radio_error.log
    CustomLog logs/radio_access.log combined
</VirtualHost>
```

### 3. Deploy dos Arquivos
```bash
# Clonar projeto
cd /var/www
sudo git clone https://github.com/seu-usuario/radios-hostlink.git html

# Configurar permissões
sudo chown -R apache:apache /var/www/html
sudo chmod -R 755 /var/www/html
```

## 🌍 Deploy no Google Cloud Platform

### 1. App Engine
```yaml
# app.yaml
runtime: php81

handlers:
- url: /.*
  script: auto
  secure: always

env_variables:
  DB_HOST: "/cloudsql/project:region:instance"
  DB_NAME: "radio_web"
  DB_USER: "radio_user"
  DB_PASS: "radio_pass"
```

### 2. Cloud SQL
```bash
# Criar instância MySQL
gcloud sql instances create radio-mysql \
    --database-version=MYSQL_8_0 \
    --tier=db-f1-micro \
    --region=us-central1

# Criar banco de dados
gcloud sql databases create radio_web --instance=radio-mysql

# Criar usuário
gcloud sql users create radio_user \
    --instance=radio-mysql \
    --password=radio_pass
```

## 🔧 Configurações de Produção

### 1. Otimizações de Performance
```apache
# .htaccess
# Compressão GZIP
<IfModule mod_deflate.c>
    AddOutputFilterByType DEFLATE text/html text/css application/javascript
</IfModule>

# Cache de navegador
<IfModule mod_expires.c>
    ExpiresActive On
    ExpiresByType image/jpg "access plus 1 month"
    ExpiresByType text/css "access plus 1 month"
</IfModule>
```

### 2. Configurações PHP
```ini
; php.ini
memory_limit = 256M
max_execution_time = 300
opcache.enable = 1
opcache.memory_consumption = 128
```

### 3. SSL/HTTPS
```bash
# Certbot (Let's Encrypt)
sudo certbot --apache -d seudominio.com

# Configurar redirecionamento HTTPS
RewriteEngine On
RewriteCond %{HTTPS} off
RewriteRule ^(.*)$ https://%{HTTP_HOST}%{REQUEST_URI} [L,R=301]
```

## 🔒 Segurança

### 1. Firewall
```bash
# UFW (Ubuntu)
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 22/tcp
sudo ufw enable

# iptables (CentOS/RHEL)
sudo firewall-cmd --permanent --add-service=http
sudo firewall-cmd --permanent --add-service=https
sudo firewall-cmd --reload
```

### 2. Backup Automático
```bash
#!/bin/bash
# backup.sh
DATE=$(date +%Y%m%d_%H%M%S)
mysqldump -u usuario -p radio_web > backup_$DATE.sql
tar -czf backup_$DATE.tar.gz backup_$DATE.sql public/uploads/
rm backup_$DATE.sql

# Adicionar ao crontab
# 0 2 * * * /path/to/backup.sh
```

### 3. Monitoramento
```bash
# Logrotate
sudo nano /etc/logrotate.d/radio
```

```
/var/log/radio_*.log {
    daily
    missingok
    rotate 52
    compress
    delaycompress
    notifempty
    create 644 www-data www-data
}
```

## 📊 Monitoramento e Logs

### 1. Logs de Acesso
```bash
# Apache
tail -f /var/log/apache2/access.log

# Nginx
tail -f /var/log/nginx/access.log
```

### 2. Logs de Erro
```bash
# PHP
tail -f /var/log/php_errors.log

# Apache
tail -f /var/log/apache2/error.log
```

### 3. Monitoramento de Recursos
```bash
# Uso de CPU e memória
htop

# Espaço em disco
df -h

# Uso de banco de dados
mysql -u root -p -e "SHOW PROCESSLIST;"
```

## 🚨 Troubleshooting

### Problemas Comuns

1. **Erro 500 - Internal Server Error**
   ```bash
   # Verificar logs
   tail -f /var/log/apache2/error.log
   
   # Verificar permissões
   sudo chown -R www-data:www-data /var/www/html
   sudo chmod -R 755 /var/www/html
   ```

2. **Erro de Conexão com Banco**
   ```bash
   # Testar conexão
   mysql -u usuario -p -h host banco
   
   # Verificar configurações
   cat config/config.php
   ```

3. **Player não funciona**
   ```bash
   # Testar URL do streaming
   curl -I https://streaming.example.com/live
   
   # Verificar configurações
   cat config/config.php | grep streaming
   ```

## 📞 Suporte

Para suporte técnico:
- 📧 Email: suporte@seudominio.com
- 💬 WhatsApp: +55 11 99999-9999
- 📱 Telegram: @suporte_radio

---

**Boa sorte com seu projeto de rádio web! 🎵** 