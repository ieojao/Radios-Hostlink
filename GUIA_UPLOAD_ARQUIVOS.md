# 📁 Guia do Sistema de Upload de Arquivos

## 🎯 O que mudou?

Agora você pode **selecionar arquivos diretamente do seu computador** em vez de apenas colocar links de imagens!

## ✅ Funcionalidades Implementadas

### 1. **Upload de Arquivos**
- ✅ Selecionar imagens do computador
- ✅ Preview em tempo real
- ✅ Validação de tipos de arquivo
- ✅ Tamanho máximo: 16MB
- ✅ Formatos aceitos: PNG, JPG, JPEG, GIF, WebP, ICO

### 2. **Sistema Híbrido**
- ✅ **Opção 1**: Selecionar arquivo do computador
- ✅ **Opção 2**: Colocar URL da imagem
- ✅ Prioridade para arquivo selecionado

### 3. **Gerenciamento Automático**
- ✅ Nomes únicos para evitar conflitos
- ✅ Organização em pastas por tipo
- ✅ Exclusão automática de arquivos antigos
- ✅ Backup de imagens existentes

## 📋 Como Usar

### **Para Banners:**

1. **Vá em**: Admin > Banners > Adicionar Banner
2. **Opção A - Upload de arquivo**:
   - Clique em "Selecionar Imagem"
   - Escolha uma imagem do seu computador
   - Veja o preview automaticamente
3. **Opção B - URL**:
   - Cole uma URL de imagem no campo "OU URL da Imagem"
4. **Preencha**: Título e Link (opcional)
5. **Clique**: "Adicionar Banner"

### **Para Locutores:**

1. **Vá em**: Admin > Locutores > Adicionar Locutor
2. **Opção A - Upload de arquivo**:
   - Clique em "Selecionar Foto"
   - Escolha uma foto do seu computador
   - Veja o preview em formato circular
3. **Opção B - URL**:
   - Cole uma URL de foto no campo "OU URL da Foto"
4. **Preencha**: Nome, Biografia, Redes Sociais
5. **Clique**: "Adicionar Locutor"

### **Para Programação:**

1. **Vá em**: Admin > Programação > Adicionar Programa
2. **Opção A - Upload de arquivo**:
   - Clique em "Selecionar Imagem"
   - Escolha uma imagem do seu computador
   - Veja o preview automaticamente
3. **Opção B - URL**:
   - Cole uma URL de imagem no campo "OU URL da Imagem"
4. **Preencha**: Título, Dia, Horários, Descrição
5. **Clique**: "Adicionar Programa"

## 🗂️ Estrutura de Pastas

```
static/
├── images/          ← Imagens fixas (logo, favicon, etc.)
└── uploads/         ← Arquivos enviados pelos usuários
    ├── banners/     ← Imagens de banners
    ├── locutores/   ← Fotos de locutores
    └── programacao/ ← Imagens de programas
```

## 🎨 Dicas para Imagens

### **Dimensões Recomendadas:**
- **Banners**: 800x400 pixels
- **Fotos de Locutores**: 300x300 pixels (quadrada)
- **Imagens de Programação**: 400x300 pixels

### **Formatos Suportados:**
- **PNG**: Melhor qualidade, arquivos maiores
- **JPG/JPEG**: Boa qualidade, arquivos menores
- **WebP**: Melhor compressão, moderno
- **GIF**: Para animações simples
- **ICO**: Para favicons

### **Tamanho de Arquivo:**
- **Máximo**: 16MB por arquivo
- **Recomendado**: Menos de 2MB para melhor performance
- **Para web**: Otimize as imagens antes de enviar

## 🔧 Funcionalidades Técnicas

### **Validação Automática:**
- ✅ Verifica extensão do arquivo
- ✅ Valida tamanho máximo
- ✅ Gera nomes únicos
- ✅ Previne conflitos

### **Preview em Tempo Real:**
- ✅ Mostra imagem selecionada
- ✅ Exibe nome e tamanho do arquivo
- ✅ Preview para URLs também
- ✅ Limpa campos automaticamente

### **Gerenciamento de Arquivos:**
- ✅ Salva em pastas organizadas
- ✅ Deleta arquivos antigos automaticamente
- ✅ Mantém URLs existentes
- ✅ Backup de imagens atuais

## ⚠️ Problemas Comuns e Soluções

### **Arquivo não carrega:**
1. Verifique se o formato é suportado
2. Verifique se o tamanho é menor que 16MB
3. Tente uma imagem diferente
4. Use a opção de URL como alternativa

### **Preview não aparece:**
1. Verifique se selecionou um arquivo válido
2. Tente recarregar a página
3. Verifique o console do navegador (F12)

### **Erro ao salvar:**
1. Verifique se preencheu todos os campos obrigatórios
2. Tente com uma imagem menor
3. Verifique sua conexão com a internet

## 🚀 Vantagens do Novo Sistema

### **Para o Usuário:**
- ✅ Mais fácil de usar
- ✅ Não precisa de URLs externas
- ✅ Preview imediato
- ✅ Controle total sobre as imagens

### **Para o Sistema:**
- ✅ Arquivos organizados
- ✅ Melhor performance
- ✅ Menos dependência externa
- ✅ Backup automático

### **Para o Site:**
- ✅ Carregamento mais rápido
- ✅ Imagens sempre disponíveis
- ✅ Melhor SEO
- ✅ Experiência mais profissional

## 💡 Dicas Importantes

1. **Sempre otimize suas imagens** antes de enviar
2. **Use formatos apropriados** para cada tipo de imagem
3. **Mantenha backups** das suas imagens originais
4. **Teste em diferentes dispositivos** para verificar a qualidade
5. **Use nomes descritivos** para seus arquivos

---

**O sistema de upload está funcionando! 🎉**

Agora você pode facilmente adicionar imagens ao seu site selecionando arquivos diretamente do seu computador. 