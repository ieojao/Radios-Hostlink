# Guia: Upload de Arquivos nas Configurações do Site

## Visão Geral

O sistema de configurações do site agora permite fazer upload de arquivos para **Logo** e **Favicon** diretamente do seu computador, além de continuar aceitando URLs externas como alternativa.

## Como Funciona

### 1. Acesso às Configurações
- Faça login no painel administrativo
- Clique em "Configurações" no menu lateral
- Role até a seção "Arquivos"

### 2. Upload de Logo

#### Opção A: Upload de Arquivo
1. Clique em "Selecionar arquivo de logo"
2. Escolha uma imagem do seu computador
3. **Formatos aceitos**: JPG, PNG, GIF
4. **Tamanho máximo**: 2MB
5. A imagem será salva automaticamente no servidor

#### Opção B: URL Externa
1. Cole a URL da imagem no campo "OU URL do Logo"
2. A URL deve ser pública e acessível

### 3. Upload de Favicon

#### Opção A: Upload de Arquivo
1. Clique em "Selecionar arquivo de favicon"
2. Escolha uma imagem do seu computador
3. **Formatos aceitos**: ICO, PNG, JPG
4. **Tamanho recomendado**: 32x32px
5. **Tamanho máximo**: 1MB
6. O favicon será salva automaticamente no servidor

#### Opção B: URL Externa
1. Cole a URL do favicon no campo "OU URL do Favicon"
2. A URL deve ser pública e acessível

## Funcionalidades

### Preview em Tempo Real
- Ao selecionar um arquivo, você verá um preview imediato
- Ao inserir uma URL, o preview também será exibido
- O preview mostra como a imagem aparecerá no site

### Validação Automática
- **Tamanho**: Verifica se o arquivo não excede o limite
- **Formato**: Aceita apenas tipos de imagem válidos
- **URL**: Valida se a URL é acessível

### Gerenciamento Automático
- Arquivos antigos são deletados automaticamente quando substituídos
- Os arquivos são organizados na pasta `/static/uploads/config/`
- Nomes únicos são gerados para evitar conflitos

## Vantagens do Upload de Arquivos

### 1. Controle Total
- Você tem controle completo sobre as imagens
- Não depende de serviços externos
- As imagens ficam salvas no seu servidor

### 2. Performance
- Carregamento mais rápido
- Não depende da disponibilidade de URLs externas
- Melhor SEO e experiência do usuário

### 3. Segurança
- Evita problemas com URLs quebradas
- Reduz dependência de serviços externos
- Maior confiabilidade

## Estrutura de Pastas

```
static/
├── uploads/
│   ├── config/          # Logo e favicon
│   ├── banners/         # Imagens de banners
│   ├── locutores/       # Fotos dos locutores
│   └── programacao/     # Imagens da programação
```

## Dicas para Imagens

### Logo
- **Formato recomendado**: PNG (transparência)
- **Dimensões**: 200-400px de largura
- **Resolução**: 72-150 DPI
- **Fundo**: Transparente ou branco

### Favicon
- **Formato recomendado**: ICO ou PNG
- **Dimensões**: 32x32px
- **Cores**: Contrastantes e visíveis
- **Simplicidade**: Design simples e reconhecível

## Solução de Problemas

### Imagem não aparece
1. Verifique se o arquivo foi enviado corretamente
2. Confirme se o formato é aceito
3. Verifique se o tamanho não excede o limite
4. Recarregue a página

### Erro no upload
1. Verifique a conexão com a internet
2. Tente um arquivo menor
3. Confirme se o formato é válido
4. Limpe o cache do navegador

### Preview não funciona
1. Verifique se a URL é válida
2. Confirme se a imagem é pública
3. Tente uma URL diferente
4. Verifique se não há bloqueios de CORS

## Exemplos de URLs Válidas

### Logo
```
https://exemplo.com/logo.png
https://cdn.exemplo.com/images/logo.jpg
https://static.exemplo.com/assets/logo.gif
```

### Favicon
```
https://exemplo.com/favicon.ico
https://cdn.exemplo.com/favicon.png
https://static.exemplo.com/favicon.jpg
```

## Backup e Segurança

### Backup Automático
- Os arquivos são salvos com nomes únicos
- Versões antigas são mantidas até serem substituídas
- Estrutura organizada facilita backups

### Segurança
- Apenas arquivos de imagem são aceitos
- Tamanhos limitados previnem abusos
- Validação de tipos de arquivo
- Sanitização de nomes de arquivo

## Próximos Passos

1. **Teste o sistema**: Faça upload de uma logo e favicon
2. **Verifique o resultado**: Acesse o site para ver as mudanças
3. **Ajuste se necessário**: Modifique as configurações conforme necessário
4. **Mantenha backups**: Faça backup regular dos arquivos importantes

---

**Nota**: Este sistema substitui completamente o método anterior de apenas URLs, oferecendo mais flexibilidade e controle sobre as imagens do site. 