# Rádio Web - Template Dinâmico

Este projeto é um template de site para rádios online, totalmente dinâmico, personalizável e pronto para ser utilizado em diferentes emissoras. Inclui painel administrativo protegido, banners dinâmicos, programação, equipe, contato, player de áudio e personalização visual completa.

## Funcionalidades

- **Site público dinâmico**: páginas de Home, Programação, Equipe, Contato e Sobre a Rádio, todas com banners, rodapé, cores, fontes e redes sociais configuráveis.
- **Player de áudio**: integração com streaming ao vivo.
- **Painel administrativo protegido**: login, gerenciamento de programação, locutores, banners e configurações visuais.
- **Formulário de contato**: envio de mensagens para o e-mail configurado.
- **Personalização visual**: cores, fontes, logo, favicon, CSS customizado e links de redes sociais.
- **Banners dinâmicos**: exibidos em todas as páginas, gerenciados pelo admin.
- **Equipe/Locutores**: cadastro e exibição dinâmica dos apresentadores.
- **Grade de programação**: cadastro e exibição por dia da semana.

## Instalação

1. **Clone o repositório e envie os arquivos para seu servidor.**

2. **Crie o banco de dados MySQL** e importe o arquivo `database.sql` para criar as tabelas necessárias:
   ```sql
   mysql -u usuario -p banco < database.sql
   ```

3. **Configure a conexão com o banco de dados** em `config/config.php`:
   ```php
   return [
       'db_host' => 'localhost',
       'db_name' => 'radio',
       'db_user' => 'root',
       'db_pass' => '',
   ];
   ```

4. **Acesse o painel administrativo** em `seusite.com/public/admin/login.php` e faça login.
   - O usuário e senha iniciais devem ser inseridos diretamente na tabela `usuarios` do banco de dados (veja abaixo como criar um admin).

## Criando o usuário admin

Execute no MySQL (ajuste o hash da senha conforme necessário):

```sql
INSERT INTO usuarios (nome, email, senha, nivel) VALUES (
  'Admin', 'admin@seudominio.com.br', 
  '$2y$10$HASHGERADOPHP', -- gere o hash com password_hash('sua_senha', PASSWORD_DEFAULT)
  'admin'
);
```

## Estrutura de Pastas

- `public/` - arquivos públicos do site (index.php, páginas dinâmicas, admin)
- `public/admin/` - painel administrativo (login, banners, locutores, programação, configurações)
- `config/` - configuração do banco de dados
- `app/` - autenticação e funções auxiliares
- `styles.css` - estilos globais do site
- `database.sql` - script para criar as tabelas

## Como funciona

### Site público

- **Home (`public/index.php`)**: exibe player, banners, programação, rodapé e redes sociais.
- **Programação (`programacao.html`)**: grade dinâmica por dia da semana, editável pelo admin.
- **Equipe (`equipe.html`)**: lista de locutores cadastrados.
- **Contato (`contato.html`)**: formulário de contato dinâmico, envia para o e-mail configurado.
- **Sobre a Rádio (`a-radio.html`)**: texto institucional, editável pelo admin.

### Painel Admin

Acesse `public/admin/login.php` para:
- Gerenciar **banners** (adicionar, editar, excluir)
- Gerenciar **locutores** (adicionar, editar, excluir)
- Gerenciar **programação** (adicionar, editar, excluir)
- Alterar **configurações visuais**: nome do site, logo, favicon, cores, fontes, texto do rodapé, CSS customizado, links de redes sociais, e-mail de contato e URL do streaming.

### Personalização Visual

No painel admin, em "Configurações do Site", você pode:
- Alterar cores principais, de fundo, texto, botões e links
- Escolher a fonte (Google Fonts)
- Definir logo e favicon
- Inserir CSS customizado
- Editar texto do rodapé
- Adicionar links de redes sociais

### Segurança

- O painel admin é protegido por login e senha.
- As senhas são armazenadas com hash seguro (password_hash).

## Observações

- O template é neutro, pronto para ser usado em qualquer rádio. Basta preencher as informações no painel admin.
- Os banners, locutores e programação são exibidos dinamicamente conforme cadastrados no painel.
- O formulário de contato envia para o e-mail configurado nas configurações.

## Dúvidas

Se precisar de ajuda para instalar, configurar ou personalizar, entre em contato com o desenvolvedor ou abra uma issue. 