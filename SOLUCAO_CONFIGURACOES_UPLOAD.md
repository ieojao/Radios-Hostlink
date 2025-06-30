# Solução de Problemas: Upload nas Configurações

## Problemas Comuns e Soluções

### 1. Arquivo não é enviado

**Sintomas:**
- O arquivo não aparece no preview
- Mensagem de erro ao tentar salvar
- O arquivo não é processado

**Soluções:**
1. **Verificar tamanho do arquivo**
   - Logo: máximo 2MB
   - Favicon: máximo 1MB
   - Reduza o tamanho se necessário

2. **Verificar formato do arquivo**
   - Logo: JPG, PNG, GIF
   - Favicon: ICO, PNG, JPG
   - Converta para formato aceito

3. **Verificar permissões**
   - Pasta `/static/uploads/config/` deve ter permissão de escrita
   - Execute: `chmod 755 static/uploads/config/`

### 2. Preview não funciona

**Sintomas:**
- Imagem não aparece no preview
- Erro "Erro ao carregar imagem"
- Preview em branco

**Soluções:**
1. **Para upload de arquivo**
   - Verifique se o arquivo é uma imagem válida
   - Tente um arquivo diferente
   - Limpe o cache do navegador

2. **Para URL externa**
   - Verifique se a URL é acessível
   - Confirme se a imagem é pública
   - Teste a URL em uma nova aba

### 3. Imagem não aparece no site

**Sintomas:**
- Upload bem-sucedido mas imagem não aparece
- Logo/favicon não carrega no site
- Erro 404 na imagem

**Soluções:**
1. **Verificar caminho do arquivo**
   - O arquivo deve estar em `/static/uploads/config/`
   - Verifique se o nome do arquivo está correto

2. **Verificar configuração no banco**
   - Acesse o banco de dados
   - Verifique se o caminho está salvo corretamente
   - O caminho deve começar com `/static/uploads/`

3. **Limpar cache**
   - Limpe o cache do navegador
   - Recarregue a página com Ctrl+F5
   - Aguarde alguns minutos

### 4. Erro de permissão

**Sintomas:**
- Erro "Permission denied"
- Não é possível salvar arquivo
- Erro 500 no servidor

**Soluções:**
1. **Verificar permissões da pasta**
   ```bash
   chmod 755 static/uploads/
   chmod 755 static/uploads/config/
   ```

2. **Verificar proprietário**
   ```bash
   chown www-data:www-data static/uploads/config/
   ```

3. **Criar pasta se não existir**
   ```bash
   mkdir -p static/uploads/config/
   ```

### 5. Arquivo antigo não é deletado

**Sintomas:**
- Arquivos antigos permanecem no servidor
- Múltiplas versões do mesmo arquivo
- Espaço em disco sendo consumido

**Soluções:**
1. **Verificar função de deletar**
   - A função `delete_uploaded_file()` deve estar funcionando
   - Verifique se o caminho está correto

2. **Limpeza manual**
   - Acesse a pasta `/static/uploads/config/`
   - Delete arquivos antigos manualmente
   - Mantenha apenas os arquivos atuais

### 6. Problemas com URLs externas

**Sintomas:**
- URL não carrega
- Erro de CORS
- Imagem quebrada

**Soluções:**
1. **Verificar acessibilidade da URL**
   - Teste a URL em uma nova aba
   - Verifique se não há bloqueios
   - Confirme se a imagem é pública

2. **Problemas de CORS**
   - Use URLs de CDNs confiáveis
   - Evite URLs que bloqueiam hotlinking
   - Considere fazer upload do arquivo

## Verificações de Diagnóstico

### 1. Verificar Estrutura de Pastas
```bash
ls -la static/uploads/
ls -la static/uploads/config/
```

### 2. Verificar Permissões
```bash
stat static/uploads/config/
```

### 3. Verificar Logs do Servidor
```bash
tail -f /var/log/apache2/error.log
# ou
tail -f /var/log/nginx/error.log
```

### 4. Verificar Configuração no Banco
```sql
SELECT * FROM configuracao WHERE chave IN ('logo', 'favicon');
```

## Comandos Úteis

### Criar Estrutura de Pastas
```bash
mkdir -p static/uploads/config
mkdir -p static/uploads/banners
mkdir -p static/uploads/locutores
mkdir -p static/uploads/programacao
```

### Definir Permissões Corretas
```bash
chmod 755 static/uploads/
chmod 755 static/uploads/config/
chmod 755 static/uploads/banners/
chmod 755 static/uploads/locutores/
chmod 755 static/uploads/programacao/
```

### Limpar Arquivos Antigos
```bash
find static/uploads/ -name "*.jpg" -mtime +30 -delete
find static/uploads/ -name "*.png" -mtime +30 -delete
find static/uploads/ -name "*.gif" -mtime +30 -delete
find static/uploads/ -name "*.ico" -mtime +30 -delete
```

## Testes Recomendados

### 1. Teste de Upload
1. Faça upload de uma imagem pequena (menos de 100KB)
2. Verifique se aparece no preview
3. Salve as configurações
4. Verifique se aparece no site

### 2. Teste de URL
1. Use uma URL de imagem pública (ex: https://via.placeholder.com/200x100)
2. Verifique se aparece no preview
3. Salve as configurações
4. Verifique se aparece no site

### 3. Teste de Substituição
1. Faça upload de uma nova imagem
2. Verifique se a antiga foi deletada
3. Confirme se a nova aparece corretamente

## Contato e Suporte

Se os problemas persistirem:

1. **Verifique os logs** do servidor para erros específicos
2. **Teste em outro navegador** para descartar problemas de cache
3. **Verifique a conexão** com a internet
4. **Consulte a documentação** do Flask e Werkzeug
5. **Entre em contato** com o suporte técnico

---

**Lembre-se**: Sempre faça backup dos arquivos importantes antes de fazer alterações no sistema. 