# Guia para Resolver Problemas com Imagens

## Problema Identificado
As imagens não estão carregando quando você coloca o link no sistema.

## Soluções

### 1. Verificar se a URL está correta
- ✅ **Correto**: `https://exemplo.com/imagem.jpg`
- ❌ **Incorreto**: `exemplo.com/imagem.jpg` (sem http/https)
- ❌ **Incorreto**: `www.exemplo.com/imagem.jpg` (sem protocolo)

### 2. Testar a URL antes de usar
1. Copie a URL da imagem
2. Cole no navegador
3. Verifique se a imagem carrega
4. Se não carregar, a URL está inválida

### 3. URLs de Exemplo que Funcionam
```txt
https://picsum.photos/800/400
https://images.unsplash.com/photo-1493225457124-a3eb161ffa5f?w=800&h=400&fit=crop
https://loremflickr.com/800/400/music
```

### 4. Problemas Comuns e Soluções

#### Problema: Imagem não aparece
**Causas possíveis:**
- URL inválida ou quebrada
- Site bloqueia hotlinking
- Problemas de CORS
- Imagem muito pesada

**Soluções:**
1. Teste a URL no navegador
2. Use serviços confiáveis (Unsplash, Picsum)
3. Verifique se a imagem não é muito grande
4. Use URLs que começam com https://

#### Problema: Imagem aparece quebrada
**Causas possíveis:**
- Formato não suportado
- Arquivo corrompido
- Problemas de rede

**Soluções:**
1. Use formatos comuns: JPG, PNG, WebP
2. Teste com URLs diferentes
3. Verifique sua conexão com a internet

### 5. Como Usar no Sistema

#### Para Banners:
1. Vá em Admin > Banners > Adicionar Banner
2. Cole a URL completa da imagem no campo "URL da Imagem"
3. O sistema mostrará um preview da imagem
4. Se aparecer "✅ Imagem válida", está funcionando

#### Para Programação:
1. Vá em Admin > Programação > Adicionar Programa
2. Cole a URL da imagem no campo correspondente
3. Salve o programa

#### Para Locutores:
1. Vá em Admin > Locutores > Adicionar Locutor
2. Cole a URL da foto no campo "URL da Foto"
3. Salve o locutor

### 6. Serviços Recomendados

#### Gratuitos e Confiáveis:
- **Unsplash**: https://unsplash.com
- **Picsum**: https://picsum.photos
- **Lorem Picsum**: https://loremflickr.com

#### Como usar Unsplash:
1. Vá para https://unsplash.com
2. Procure uma imagem
3. Clique na imagem
4. Clique em "Download"
5. Copie a URL da imagem (não o link de download)

### 7. Dicas Importantes

1. **Sempre use URLs completas** que começam com http:// ou https://
2. **Teste a URL** no navegador antes de usar
3. **Use imagens otimizadas** para melhor performance
4. **Evite imagens muito grandes** (máximo 2MB)
5. **Use formatos modernos** como WebP quando possível

### 8. Verificação no Sistema

O sistema agora inclui:
- ✅ Validação automática de URLs
- ✅ Preview de imagens em tempo real
- ✅ Feedback visual (✅ válida, ❌ inválida)
- ✅ Tratamento de erros com fallback

### 9. Se ainda não funcionar

1. Verifique se o servidor está rodando
2. Teste com URLs de exemplo fornecidas
3. Verifique o console do navegador (F12) para erros
4. Tente com uma URL diferente
5. Verifique se não há bloqueios de firewall

### 10. Exemplo Prático

**URL que funciona:**
```
https://picsum.photos/800/400
```

**Como testar:**
1. Cole no navegador
2. Deve mostrar uma imagem aleatória
3. Use no sistema
4. Deve aparecer "✅ Imagem válida"

---

**Se ainda tiver problemas, verifique:**
- Sua conexão com a internet
- Se o site da imagem está funcionando
- Se não há bloqueios de CORS
- Se a URL está correta e completa 