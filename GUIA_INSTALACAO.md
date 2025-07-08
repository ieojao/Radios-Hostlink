# 🚀 Guia de Instalação - Radios Hostlink

## O que você precisa fazer ao receber o projeto:

### 1. 📋 Pré-requisitos
- **Python 3.8 ou superior** instalado
- **pip** (gerenciador de pacotes Python)

### 2. 🛠️ Instalação Rápida

**Abra o terminal/prompt na pasta do projeto e execute:**

```bash
# 1. Criar ambiente virtual (recomendado)
python -m venv venv

# 2. Ativar o ambiente virtual
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Executar o projeto
python run.py
```

### 3. 🌐 Acessar o site
- **Site principal**: http://localhost:5000
- **Painel admin**: http://localhost:5000/admin
- **Login admin**: admin@radioshostlink.com.br / admin123

### 4. ⚙️ Configuração (Opcional)
Se quiser personalizar configurações:
```bash
# Copiar arquivo de exemplo
cp env_example.txt .env
# Editar o arquivo .env com suas configurações
```

### 5. 🎯 Comandos Úteis
```bash
# Verificar se tudo está OK
python run.py --check

# Inicializar banco de dados (se necessário)
python run.py --init-db

# Executar em modo debug
python run.py --debug
```

## ✅ Pronto!
O site estará funcionando em http://localhost:5000

**Dúvidas?** Consulte o README.md para mais detalhes. 