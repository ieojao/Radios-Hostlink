@echo off
echo ========================================
echo    Configuracao do Sistema de Radio
echo ========================================
echo.

echo 1. Iniciando Apache...
C:\xampp\apache_start.bat
timeout /t 3 /nobreak >nul

echo 2. Iniciando MySQL...
C:\xampp\mysql_start.bat
timeout /t 3 /nobreak >nul

echo 3. Verificando se os servicos estao rodando...
netstat -an | findstr :80
netstat -an | findstr :3306

echo.
echo ========================================
echo    Configuracao Concluida!
echo ========================================
echo.
echo Agora voce pode:
echo.
echo 1. Abrir o navegador e acessar:
echo    http://localhost/radio-web/install/install.php
echo.
echo 2. Configurar o banco com:
echo    - Host: localhost
echo    - Nome do banco: radio_web
echo    - Usuario: root
echo    - Senha: (deixe em branco)
echo.
echo 3. Apos a instalacao, acesse:
echo    - Site: http://localhost/radio-web/public/
echo    - Admin: http://localhost/radio-web/public/admin/login.php
echo.
echo Pressione qualquer tecla para abrir o navegador...
pause >nul
start http://localhost/radio-web/install/install.php 