# Hostlink - Rádio Web

Este é o projeto de template rádio web usando Flask. Uma aplicação web moderna para gerenciar e exibir programação de rádio gospel.

## 🚀 Características

- **Framework Moderno**: Flask com SQLAlchemy
- **Interface Responsiva**: Design moderno e responsivo
- **Painel Administrativo**: Gerenciamento completo de conteúdo
- **API REST**: Endpoints para integração
- **Banco de Dados**: SQLite (padrão) ou MySQL/PostgreSQL
- **Autenticação**: Sistema de login seguro
- **Programação Dinâmica**: Exibição da programação atual
- **WhatsApp Integration**: Botão de contato direto

## 📋 Pré-requisitos

- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

## 🛠️ Instalação

1. **Clone o repositório**
```bash
git clone <url-do-repositorio>
cd Radios-Hostlink
```

2. **Crie um ambiente virtual**
```bash
python -m venv venv
```

3. **Ative o ambiente virtual**
```bash
# Windows
venv\Scripts\activate

# Linux/Mac
source venv/bin/activate
```

4. **Instale as dependências**
```bash
pip install -r requirements.txt
```

5. **Configure as variáveis de ambiente**
```bash
# Copie o arquivo de exemplo
cp env_example.txt .env

# Edite o arquivo .env com suas configurações
```

6. **Execute a aplicação**
```bash
python app.py
```

A aplicação estará disponível em `http://localhost:5000`

## 📁 Estrutura do Projeto

```
Radios-Hostlink/
├── app.py                 # Aplicação principal Flask
├── requirements.txt       # Dependências Python
├── env_example.txt       # Exemplo de variáveis de ambiente
├── templates/            # Templates HTML
│   ├── base.html         # Template base
│   ├── index.html        # Página inicial
│   ├── programacao.html  # Página de programação
│   ├── a-radio.html      # Página "A Rádio"
│   ├── equipe.html       # Página da equipe
│   ├── contato.html      # Página de contato
│   └── admin/            # Templates do painel admin
│       ├── base.html     # Template base do admin
│       ├── login.html    # Página de login
│       └── dashboard.html # Dashboard principal
├── static/               # Arquivos estáticos
│   ├── css/              # Folhas de estilo
│   │   ├── styles.css    # CSS principal
│   │   └── admin.css     # CSS do painel admin
│   ├── js/               # JavaScript
│   │   ├── main.js       # JS principal
│   │   └── admin.js      # JS do painel admin
│   └── images/           # Imagens
└── README_PYTHON.md      # Esta documentação
```

## 🔧 Configuração

### Variáveis de Ambiente

Crie um arquivo `.env` baseado no `env_example.txt`:

```env
# Configurações do banco de dados
DATABASE_URL=sqlite:///radio.db

# Chave secreta para sessões
SECRET_KEY=sua-chave-secreta-aqui

# Configurações do site
SITE_NAME=Hostlink
SITE_EMAIL=contato@hostlink.com.br
STREAMING_URL=https://streaming.example.com/live
```

### Banco de Dados

O sistema usa SQLite por padrão, mas suporta MySQL e PostgreSQL:

```env
# SQLite (padrão)
DATABASE_URL=sqlite:///radio.db

# MySQL
DATABASE_URL=mysql+pymysql://usuario:senha@localhost/radio_web

# PostgreSQL
DATABASE_URL=postgresql://usuario:senha@localhost/radio_web
```

## 👤 Acesso ao Painel Administrativo

**URL**: `http://localhost:5000/admin`

**Credenciais padrão**:
- **Email**: admin@hostlink.com
- **Senha**: admin123

⚠️ **Importante**: Altere essas credenciais após o primeiro acesso!

## 🎯 Funcionalidades

### Site Público
- **Página Inicial**: Exibição da programação atual
- **Programação**: Grade completa por dia da semana
- **A Rádio**: Informações sobre a rádio
- **Equipe**: Perfis dos locutores
- **Contato**: Formulário de contato e informações

### Painel Administrativo
- **Dashboard**: Visão geral do sistema
- **Programação**: Gerenciar programação
- **Locutores**: Gerenciar equipe
- **Banners**: Gerenciar banners
- **Configurações**: Personalizar site
- **Usuários**: Gerenciar usuários

### API
- `GET /api/programacao-atual`: Retorna programação atual
- Endpoints para CRUD de programação, locutores, etc.

## 🚀 Deploy

### Deploy Local
```bash
python app.py
```

### Deploy em Produção

1. **Usando Gunicorn**
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

2. **Usando Docker**
```dockerfile
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["gunicorn", "-w", "4", "-b", "0.0.0.0:5000", "app:app"]
```

3. **Usando Heroku**
```bash
# Criar Procfile
echo "web: gunicorn app:app" > Procfile

# Deploy
heroku create
git push heroku main
```

## 🔒 Segurança

- Senhas criptografadas com bcrypt
- Sessões seguras
- Proteção CSRF
- Validação de formulários
- Sanitização de dados

## 📱 Responsividade

O site é totalmente responsivo e funciona em:
- Desktop
- Tablet
- Mobile

## 🎨 Personalização

### Cores e Estilo
Edite as configurações no painel admin ou modifique o CSS:

```css
:root {
    --cor-principal: #1e3a8a;
    --cor-botoes: #3b82f6;
    --cor-fundo: #ffffff;
    --cor-texto: #333333;
}
```

### Logo e Imagens
Substitua as imagens na pasta `static/images/`:
- `logo.png` - Logo da rádio
- `favicon.ico` - Ícone do site
- `programa.jpg` - Imagem padrão de programas

## 🐛 Solução de Problemas

### Erro de Conexão com Banco
```bash
# Verificar se o banco foi criado
python -c "from app import db; db.create_all()"
```

### Erro de Dependências
```bash
# Reinstalar dependências
pip install -r requirements.txt --force-reinstall
```

### Erro de Porta
```bash
# Usar porta diferente
python app.py --port 8080
```

## 📞 Suporte

Para suporte técnico:
- Email: contato@novaatalaia.com.br
- WhatsApp: (11) 99999-9999

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 🎉 Próximos Passos

1. Configure suas credenciais de admin
2. Adicione sua programação
3. Personalize o design
4. Configure o streaming
5. Teste todas as funcionalidades
6. Faça backup regular

---

**Desenvolvido com ❤️ para a Nova Atalaia** 