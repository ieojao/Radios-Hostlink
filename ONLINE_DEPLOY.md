# 🌐 Deploy Online Gratuito

## 🆓 Opções Gratuitas

### 1. **InfinityFree** (Recomendado)
- **URL**: https://infinityfree.net/
- **Recursos**: 5GB espaço, MySQL, PHP 8.1
- **Domínio**: `.epizy.com` gratuito

#### Como usar:
1. **Crie uma conta** no InfinityFree
2. **Crie um site** e escolha um domínio
3. **Acesse o cPanel** ou File Manager
4. **Faça upload** dos arquivos via FTP ou upload direto
5. **Crie o banco MySQL** no painel
6. **Acesse**: `seudominio.epizy.com/install/install.php`

### 2. **000WebHost** (Hostinger)
- **URL**: https://www.000webhost.com/
- **Recursos**: 300MB espaço, MySQL, PHP 8.0
- **Domínio**: `.000webhostapp.com` gratuito

### 3. **Heroku** (Com Docker)
- **URL**: https://heroku.com/
- **Recursos**: 512MB RAM, banco PostgreSQL
- **Domínio**: `.herokuapp.com` gratuito

## 🚀 Deploy Rápido no InfinityFree

### Passo 1: Criar Conta
1. Acesse https://infinityfree.net/
2. Clique em "Sign Up"
3. Preencha os dados e confirme o e-mail

### Passo 2: Criar Site
1. Faça login no painel
2. Clique em "New Website"
3. Escolha um domínio (ex: `minharadio.epizy.com`)
4. Aguarde a criação (pode demorar alguns minutos)

### Passo 3: Upload dos Arquivos
1. Acesse o **File Manager** no painel
2. Vá para a pasta `htdocs`
3. **Faça upload** de todos os arquivos do projeto
4. **Extraia** se necessário

### Passo 4: Configurar Banco
1. No painel, vá em **MySQL Databases**
2. **Crie um banco** com nome `radio_web`
3. **Anote** as credenciais:
   - Host: `sql.infinityfree.com`
   - Usuário: (gerado automaticamente)
   - Senha: (gerada automaticamente)
   - Banco: `radio_web`

### Passo 5: Instalar Sistema
1. Acesse: `seudominio.epizy.com/install/install.php`
2. **Preencha** as informações do banco
3. **Crie** o usuário administrador
4. **Clique** em "Instalar Sistema"

### Passo 6: Acessar
- **Site**: `seudominio.epizy.com/public/`
- **Admin**: `seudominio.epizy.com/public/admin/login.php`

## 🔧 Configurações Específicas

### InfinityFree
```php
// config/config.php
return [
    'db_host' => 'sql.infinityfree.com',
    'db_name' => 'radio_web',
    'db_user' => 'seu_usuario',
    'db_pass' => 'sua_senha',
    'site_name' => 'Minha Rádio',
    'site_email' => 'contato@seudominio.com',
    'streaming_url' => 'https://streaming.example.com/live',
];
```

### 000WebHost
```php
// config/config.php
return [
    'db_host' => 'localhost',
    'db_name' => 'radio_web',
    'db_user' => 'seu_usuario',
    'db_pass' => 'sua_senha',
    'site_name' => 'Minha Rádio',
    'site_email' => 'contato@seudominio.com',
    'streaming_url' => 'https://streaming.example.com/live',
];
```

## ⚠️ Limitações dos Planos Gratuitos

### InfinityFree
- ✅ **Vantagens**: Domínio gratuito, MySQL, PHP 8.1
- ❌ **Limitações**: Anúncios, downtime ocasional, limite de CPU

### 000WebHost
- ✅ **Vantagens**: Interface amigável, SSL gratuito
- ❌ **Limitações**: 300MB espaço, inatividade = suspensão

### Heroku
- ✅ **Vantagens**: Confiável, sem anúncios
- ❌ **Limitações**: Sleep mode, PostgreSQL (não MySQL)

## 🎯 Recomendação

**Para começar rapidamente**: Use **InfinityFree**
- É gratuito
- Tem MySQL
- Domínio próprio
- Fácil de configurar

**Para desenvolvimento**: Use **XAMPP** local
- Sem limitações
- Controle total
- Desenvolvimento offline

## 📞 Suporte

Se tiver problemas com o deploy online:
1. Verifique se todos os arquivos foram uploadados
2. Confirme as credenciais do banco
3. Verifique os logs de erro no painel
4. Teste a conexão com o banco 