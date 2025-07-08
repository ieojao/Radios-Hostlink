# Guia para Reset do Banco de Dados no cPanel

## Quando Usar Este Script

Use o script `reset_database.py` quando:
- O site não carrega devido a problemas no banco
- Erros de "database locked" ou "database corrupted"
- Problemas de permissões no banco de dados
- Necessidade de limpar todos os dados e começar do zero

## Como Usar no cPanel

### 1. Acessar o Terminal do cPanel

1. Faça login no cPanel
2. Procure por "Terminal" ou "SSH Access"
3. Clique para abrir o terminal

### 2. Navegar até o Diretório do Site

```bash
cd public_html/site
```

### 3. Verificar Informações do Banco Atual

```bash
python reset_database.py info
```

Este comando mostra:
- Se o banco existe
- Tamanho do arquivo
- Data da última modificação

### 4. Fazer Backup (Recomendado)

```bash
python reset_database.py backup
```

Cria um backup com timestamp: `radio_backup_20241201_143022.db`

### 5. Reset Completo do Banco

```bash
python reset_database.py reset
```

Este comando:
1. ✅ Faz backup automático
2. ✅ Remove o banco atual
3. ✅ Cria novo banco com todas as tabelas
4. ✅ Cria usuário admin padrão

### 6. Comandos Individuais (Opcional)

Se quiser fazer apenas uma operação específica:

```bash
# Apenas backup
python reset_database.py backup

# Apenas deletar
python reset_database.py delete

# Apenas criar novo
python reset_database.py create
```

## Após o Reset

### 1. Credenciais de Acesso

Após o reset, use estas credenciais:
- **URL**: `seudominio.com/site/admin`
- **Email**: `admin@radioshostlink.com.br`
- **Senha**: `admin123`

### 2. Configurações Iniciais

1. Acesse o painel admin
2. Vá em "Configurações"
3. Configure:
   - Nome do site
   - URL do streaming
   - Email de contato
   - Outras configurações básicas

### 3. Adicionar Conteúdo

Após o reset, você precisará adicionar:
- Programação da rádio
- Locutores
- Banners
- Destaques
- Informações da rádio

## Solução de Problemas

### Erro: "Permission denied"

```bash
# Dar permissões necessárias
chmod 755 public_html/site
chmod 644 public_html/site/reset_database.py
```

### Erro: "Module not found"

```bash
# Instalar dependências
pip install -r requirements.txt
```

### Erro: "Database is locked"

```bash
# Parar aplicação primeiro
# No cPanel: Setup Python App → Stop
# Depois executar o reset
python reset_database.py reset
# Reiniciar aplicação
# No cPanel: Setup Python App → Start
```

### Backup não encontrado

Os backups ficam na mesma pasta do site. Para listar:

```bash
ls -la radio_backup_*.db
```

## Restaurar Backup Manualmente

Se precisar restaurar um backup específico:

```bash
# Listar backups disponíveis
ls -la radio_backup_*.db

# Restaurar backup específico
cp radio_backup_20241201_143022.db radio.db

# Verificar se funcionou
python reset_database.py info
```

## Segurança

⚠️ **ATENÇÃO**: O reset apaga TODOS os dados do banco!

- Sempre faça backup antes
- Use apenas quando necessário
- Mantenha os arquivos de backup seguros
- Altere a senha do admin após o primeiro login

## Logs de Erro

Se algo der errado, verifique:

1. **Terminal do cPanel**: Mensagens de erro
2. **Error Logs**: No cPanel
3. **stderr.log**: Arquivo na pasta do site

## Contato

Se ainda tiver problemas:
1. Verifique os logs de erro
2. Teste comandos individuais
3. Verifique permissões de arquivos
4. Confirme se as dependências estão instaladas 