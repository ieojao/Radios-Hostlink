# Configuração do Site no cPanel

## Problemas Comuns e Soluções

### 1. Erro "Not Found"
Se você está recebendo erro 404, siga estes passos:

#### Verificar Configuração do Python:
1. Acesse o cPanel
2. Vá em "Setup Python App"
3. Verifique se a aplicação está configurada para:
   - **Python Version**: 3.8 ou superior
   - **Application Root**: `/public_html/site`
   - **Application URL**: `seudominio.com/site`
   - **Application Entry Point**: `passenger_wsgi.py`

#### Verificar Permissões:
```bash
# No terminal do cPanel ou via SSH
chmod 755 /home/devhostlink/public_html/site
chmod 644 /home/devhostlink/public_html/site/passenger_wsgi.py
chmod 644 /home/devhostlink/public_html/site/.htaccess
```

#### Verificar Dependências:
1. Acesse "Terminal" no cPanel
2. Navegue até o diretório: `cd public_html/site`
3. Execute: `pip install -r requirements.txt`

### 2. Testar se o Python está funcionando:
Acesse: `seudominio.com/site/test.py`

Se aparecer uma página com informações do Python, está funcionando.

### 3. Verificar Logs de Erro:
1. No cPanel, vá em "Error Logs"
2. Procure por erros relacionados ao Python ou Flask
3. Verifique também o arquivo `stderr.log` na pasta do site

### 4. Configuração do Banco de Dados:
Se o banco não existir, execute no terminal:
```bash
cd public_html/site
python run.py --init-db
```

### 5. URLs de Acesso:
- **Site Principal**: `seudominio.com/site/`
- **Painel Admin**: `seudominio.com/site/admin`
- **Login Admin**: admin@radioshostlink.com.br / admin123

### 6. Problemas de Permissão de Arquivos:
```bash
# Dar permissão de escrita para uploads
chmod 755 public_html/site/static/uploads
chmod 755 public_html/site/static/uploads/banners
chmod 755 public_html/site/static/uploads/destaques
chmod 755 public_html/site/static/uploads/locutores
chmod 755 public_html/site/static/uploads/programacao
chmod 755 public_html/site/static/uploads/config
```

### 7. Reiniciar Aplicação:
1. No cPanel, vá em "Setup Python App"
2. Clique em "Restart" na sua aplicação
3. Aguarde alguns segundos

### 8. Verificar Configuração do .htaccess:
O arquivo `.htaccess` deve conter as configurações do Passenger:
```
PassengerAppRoot "/home/devhostlink/public_html/site"
PassengerBaseURI "/site"
PassengerPython "/home/devhostlink/virtualenv/public_html/site/3.8/bin/python"
```

### 9. Contato para Suporte:
Se ainda tiver problemas, verifique:
- Logs de erro no cPanel
- Configuração do Python App
- Permissões de arquivos
- Dependências instaladas 