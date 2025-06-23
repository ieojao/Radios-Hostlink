# 🖥️ Instalação com XAMPP (Windows)

## 📥 Passo 1: Baixar e Instalar XAMPP

1. **Baixe o XAMPP** em: https://www.apachefriends.org/download.html
2. **Escolha a versão** com PHP 8.1 ou superior
3. **Execute o instalador** e siga as instruções
4. **Instale em** `C:\xampp` (padrão)

## 🚀 Passo 2: Iniciar os Serviços

1. **Abra o XAMPP Control Panel**
2. **Clique em "Start"** para:
   - Apache
   - MySQL
3. **Verifique se ambos ficaram verdes**

## 📁 Passo 3: Configurar o Projeto

1. **Copie os arquivos** do projeto para:
   ```
   C:\xampp\htdocs\radio-web\
   ```

2. **Abra o navegador** e acesse:
   ```
   http://localhost/radio-web/install/install.php
   ```

3. **Configure o banco** com estas informações:
   - **Host**: `localhost`
   - **Nome do banco**: `radio_web`
   - **Usuário**: `root`
   - **Senha**: (deixe em branco - padrão do XAMPP)

## 🎯 Passo 4: Acessar o Sistema

- **Site público**: `http://localhost/radio-web/public/`
- **Painel admin**: `http://localhost/radio-web/public/admin/login.php`

## ⚙️ Configurações Adicionais

### Habilitar mod_rewrite
1. Abra: `C:\xampp\apache\conf\httpd.conf`
2. Procure por: `#LoadModule rewrite_module modules/mod_rewrite.so`
3. Remova o `#` para descomentar
4. Reinicie o Apache

### Configurar Virtual Host (Opcional)
Adicione ao arquivo `C:\xampp\apache\conf\extra\httpd-vhosts.conf`:

```apache
<VirtualHost *:80>
    DocumentRoot "C:/xampp/htdocs/radio-web/public"
    ServerName radio.local
    <Directory "C:/xampp/htdocs/radio-web/public">
        AllowOverride All
        Require all granted
    </Directory>
</VirtualHost>
```

Depois adicione `127.0.0.1 radio.local` ao arquivo `C:\Windows\System32\drivers\etc\hosts`

## 🔧 Solução de Problemas

### Erro de Conexão com Banco
- Verifique se o MySQL está rodando no XAMPP
- Confirme se a senha está correta (vazia por padrão)

### Erro 500
- Verifique os logs em: `C:\xampp\apache\logs\error.log`
- Confirme se o mod_rewrite está habilitado

### Permissões de Arquivo
- Certifique-se de que o XAMPP tem permissão para ler/escrever nos arquivos

## 📞 Suporte

Se tiver problemas:
1. Verifique se Apache e MySQL estão rodando
2. Confirme se os arquivos estão na pasta correta
3. Verifique os logs de erro do XAMPP 