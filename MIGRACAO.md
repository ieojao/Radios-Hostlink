# 🔄 Guia de Migração - Nova Arquitetura

## 📋 Visão Geral

Este guia explica como migrar do projeto antigo (arquivo único `app.py`) para a nova arquitetura modular.

## 🎯 Por que Migrar?

### ✅ Benefícios da Nova Arquitetura

- **Organização**: Código separado em módulos lógicos
- **Manutenibilidade**: Fácil localização e modificação de código
- **Escalabilidade**: Estrutura preparada para crescimento
- **Testabilidade**: Facilita criação de testes unitários
- **Reutilização**: Componentes modulares e reutilizáveis

### 📊 Comparação

| Aspecto | Arquitetura Antiga | Nova Arquitetura |
|---------|-------------------|------------------|
| **Arquivos** | 1 arquivo (1400+ linhas) | 20+ arquivos organizados |
| **Manutenção** | Difícil | Fácil |
| **Testes** | Complexo | Simples |
| **Escalabilidade** | Limitada | Alta |

## 🚀 Processo de Migração

### 1. **Backup Automático**

Execute o script de migração que fará backup automático:

```bash
python migrate_to_new_architecture.py
```

Este script irá:
- ✅ Fazer backup dos arquivos antigos
- ✅ Criar nova estrutura de pastas
- ✅ Migrar dados do banco
- ✅ Configurar nova arquitetura

### 2. **Configuração Manual**

Após a migração automática, configure manualmente:

#### A. Arquivo de Configuração

Copie o arquivo de exemplo e configure:

```bash
cp config.env.example config.env
```

Edite `config.env` com suas configurações:

```env
# Configurações do banco de dados
DATABASE_URL=sqlite:///radio.db

# Chave secreta (GERE UMA NOVA!)
SECRET_KEY=sua-chave-secreta-muito-segura-aqui

# Configurações do site
SITE_NAME=Radios Hostlink
SITE_EMAIL=contato@radioshostlink.com.br
STREAMING_URL=https://streaming.example.com/live
```

#### B. Instalar Dependências

```bash
pip install -r requirements.txt
```

### 3. **Inicialização**

```bash
# Inicializar banco de dados
python run.py init-db

# Executar aplicação
python run.py run
```

## 📁 Estrutura Após Migração

```
Radios-Hostlink/
├── 📁 models/                 # Modelos do banco
│   ├── database.py           # Configuração DB
│   ├── user.py              # Usuários
│   ├── content.py           # Conteúdo
│   └── pages.py             # Páginas
├── 📁 services/              # Lógica de negócio
│   ├── file_service.py      # Arquivos
│   ├── programacao_service.py # Programação
│   └── config_service.py    # Configurações
├── 📁 routes/                # Rotas
│   ├── public.py            # Site público
│   ├── api.py               # API REST
│   └── admin/               # Painel admin
├── 📁 utils/                 # Utilitários
│   └── filters.py           # Filtros
├── config.py                 # Configurações
├── app_factory.py           # Factory
├── run.py                   # Principal
└── requirements.txt         # Dependências
```

## 🔧 Comandos da Nova Arquitetura

### Desenvolvimento

```bash
# Inicializar banco
python run.py init-db

# Executar servidor
python run.py run

# Ver ajuda
python run.py help
```

### Produção

```bash
# Usando Gunicorn
gunicorn --bind 0.0.0.0:5000 --workers 4 run:app

# Usando Docker
docker-compose up -d
```

## 🔄 Migração de Dados

### Dados Migrados Automaticamente

- ✅ Usuários e senhas
- ✅ Programação da rádio
- ✅ Locutores
- ✅ Banners
- ✅ Destaques
- ✅ Configurações do site
- ✅ Páginas (A Rádio, Equipe, Contato)
- ✅ Mensagens de contato

### Verificação

Após a migração, verifique:

1. **Acesse o site**: http://localhost:5000
2. **Painel admin**: http://localhost:5000/admin
3. **Credenciais**: admin@radioshostlink.com.br / admin123
4. **Dados**: Confirme se todos os dados foram migrados

## 🐛 Solução de Problemas

### Erro de Importação

```bash
# Se houver erro de módulos não encontrados
pip install -r requirements.txt --upgrade
```

### Erro de Banco de Dados

```bash
# Recriar banco
rm radio.db
python run.py init-db
```

### Erro de Permissões

```bash
# Criar pastas necessárias
mkdir -p logs static/uploads
chmod 755 logs static/uploads
```

### Erro de Configuração

```bash
# Verificar arquivo de configuração
cat config.env
# Certifique-se de que todas as variáveis estão definidas
```

## 📚 Documentação

### Arquivos Importantes

- `README_ARQUITETURA.md`: Documentação completa da nova arquitetura
- `config.env.example`: Exemplo de configuração
- `requirements.txt`: Dependências atualizadas
- `run.py`: Arquivo principal da aplicação

### Recursos Adicionais

- [Flask Blueprint Documentation](https://flask.palletsprojects.com/en/2.3.x/blueprints/)
- [Clean Architecture](https://blog.cleancoder.com/uncle-bob/2012/08/13/the-clean-architecture.html)
- [Factory Pattern](https://refactoring.guru/design-patterns/factory-method)

## 🔮 Próximos Passos

Após a migração bem-sucedida:

1. **Teste todas as funcionalidades**
2. **Configure backup automático**
3. **Implemente monitoramento**
4. **Adicione testes automatizados**
5. **Configure CI/CD**

## 🆘 Suporte

Se encontrar problemas durante a migração:

1. **Verifique os logs**: `logs/app.log`
2. **Consulte a documentação**: `README_ARQUITETURA.md`
3. **Restaure o backup**: Use os arquivos em `backup_old_architecture_*`

---

**🎉 Parabéns! Você agora tem uma arquitetura moderna, escalável e profissional!** 