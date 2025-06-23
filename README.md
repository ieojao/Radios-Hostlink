# 📻 Sistema de Rádio Web - Nova Atalaia

Um sistema completo e moderno para rádios web, com painel administrativo, player de áudio, programação dinâmica, equipe, formulário de contato e personalização visual completa.

## ✨ Funcionalidades

### 🎵 Site Público
- **Player de áudio integrado** com streaming ao vivo
- **Páginas dinâmicas**: Home, Sobre a Rádio, Programação, Equipe e Contato
- **Banners rotativos** gerenciados pelo admin
- **Programação por dia da semana** com interface intuitiva
- **Equipe/Locutores** com fotos e redes sociais
- **Formulário de contato** funcional com envio de e-mail
- **Design responsivo** para todos os dispositivos
- **Personalização visual** completa (cores, fontes, logo, favicon)

### 🔧 Painel Administrativo
- **Login seguro** com autenticação
- **Dashboard** com estatísticas em tempo real
- **Gerenciamento de banners** (adicionar, editar, excluir)
- **Gerenciamento de equipe** (locutores e apresentadores)
- **Gerenciamento de programação** por dia da semana
- **Visualização de mensagens** de contato
- **Configurações do site** (cores, fontes, redes sociais, streaming)

### 🎨 Personalização
- Cores principais, de fundo, texto, botões e links
- Fontes do Google Fonts
- Logo e favicon personalizados
- CSS customizado
- Links de redes sociais
- URL do streaming
- E-mail de contato

## 🚀 Instalação Rápida

### 1. Requisitos
- PHP 7.4 ou superior
- MySQL 5.7 ou superior
- Servidor web (Apache/Nginx)
- Extensões PHP: PDO, PDO_MySQL, mbstring

### 2. Instalação Automática
1. **Faça upload** dos arquivos para seu servidor
2. **Acesse** `http://seudominio.com/install/install.php`
3. **Preencha** as informações do banco de dados e usuário admin
4. **Clique em "Instalar Sistema"**
5. **Acesse** o painel admin em `http://seudominio.com/public/admin/login.php`

### 3. Instalação Manual
Se preferir instalar manualmente:

```bash
# 1. Criar banco de dados
mysql -u root -p
CREATE DATABASE radio_web CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;

# 2. Importar estrutura
mysql -u root -p radio_web < database.sql

# 3. Configurar conexão
# Edite config/config.php com suas credenciais

# 4. Criar usuário admin
mysql -u root -p radio_web
INSERT INTO usuarios (nome, email, senha, nivel) VALUES (
  'Admin', 'admin@seudominio.com', 
  '$2y$10$HASHGERADOPHP', -- use password_hash('sua_senha', PASSWORD_DEFAULT)
  'admin'
);
```

## 📁 Estrutura do Projeto

```
Radios-Hostlink/
├── app/                    # Classes PHP
│   ├── Database.php       # Conexão com banco
│   └── Config.php         # Gerenciamento de configurações
├── config/                # Configurações
│   └── config.php         # Configuração do banco
├── public/                # Arquivos públicos
│   ├── index.php          # Página inicial
│   ├── programacao.php    # Programação
│   ├── equipe.php         # Equipe
│   ├── contato.php        # Contato
│   ├── a-radio.php        # Sobre a rádio
│   └── admin/             # Painel administrativo
│       ├── login.php      # Login
│       ├── index.php      # Dashboard
│       └── logout.php     # Logout
├── install/               # Instalador
│   └── install.php        # Script de instalação
├── styles.css             # Estilos globais
├── database.sql           # Estrutura do banco
└── README.md              # Este arquivo
```

## 🗄️ Estrutura do Banco de Dados

### Tabelas Principais
- **usuarios**: Usuários do painel admin
- **configuracoes**: Configurações do site
- **banners**: Banners rotativos
- **equipe**: Membros da equipe
- **programacao**: Grade de programação
- **contatos**: Mensagens de contato
- **sobre_radio**: Informações sobre a rádio

## 🎯 Como Usar

### 1. Primeiro Acesso
1. Acesse o painel admin: `http://seudominio.com/public/admin/login.php`
2. Faça login com as credenciais criadas na instalação
3. Configure as informações básicas do site em "Configurações"

### 2. Configurações Básicas
No painel admin, configure:
- **Nome do site** e logo
- **Cores** e fontes
- **URL do streaming** para o player
- **Redes sociais** e WhatsApp
- **E-mail** de contato

### 3. Adicionar Conteúdo
- **Banners**: Adicione imagens promocionais
- **Equipe**: Cadastre locutores e apresentadores
- **Programação**: Crie a grade de programação por dia
- **Sobre a Rádio**: Adicione informações institucionais

### 4. Personalização Visual
- Altere cores no painel admin
- Faça upload de logo e favicon
- Adicione CSS customizado se necessário
- Configure fontes do Google Fonts

## 🔒 Segurança

- **Senhas criptografadas** com `password_hash()`
- **Sessões seguras** para autenticação
- **Validação de dados** em formulários
- **Proteção contra SQL injection** com prepared statements
- **Sanitização de saída** com `htmlspecialchars()`

## 🎨 Personalização Avançada

### CSS Customizado
No painel admin, você pode adicionar CSS personalizado:

```css
/* Exemplo de personalização */
.player-bar {
    background: linear-gradient(45deg, #ff6b6b, #4ecdc4);
}

.banner {
    background-image: url('sua-imagem.jpg');
}
```

### Variáveis CSS
O sistema usa variáveis CSS para facilitar a personalização:

```css
:root {
    --cor-principal: #1e3a8a;
    --cor-fundo: #ffffff;
    --cor-texto: #333333;
    --cor-botoes: #3b82f6;
    --cor-links: #1e40af;
}
```

## 📱 Responsividade

O site é totalmente responsivo e funciona em:
- 📱 Smartphones
- 📱 Tablets
- 💻 Desktops
- 🖥️ Monitores grandes

## 🔧 Manutenção

### Backup
Faça backup regular do banco de dados:
```bash
mysqldump -u usuario -p radio_web > backup_$(date +%Y%m%d).sql
```

### Atualizações
- Mantenha o PHP atualizado
- Monitore logs de erro
- Faça backup antes de atualizações

## 🆘 Suporte

### Problemas Comuns

1. **Erro de conexão com banco**
   - Verifique as credenciais em `config/config.php`
   - Confirme se o MySQL está rodando

2. **Player não funciona**
   - Verifique a URL do streaming nas configurações
   - Teste a URL diretamente no navegador

3. **E-mail não envia**
   - Configure corretamente o servidor SMTP
   - Verifique as configurações de e-mail do servidor

### Logs
Verifique os logs do PHP para erros:
- Apache: `/var/log/apache2/error.log`
- Nginx: `/var/log/nginx/error.log`

## 📄 Licença

Este projeto é de uso livre para rádios e emissoras.

## 🤝 Contribuição

Para contribuir com melhorias:
1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Abra um Pull Request

---

**Desenvolvido com ❤️ para a comunidade radiofônica brasileira** 