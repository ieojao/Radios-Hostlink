# Redes Sociais com Ícones Oficiais

## Visão Geral

O sistema de redes sociais foi atualizado para usar os ícones oficiais das plataformas, oferecendo uma experiência visual mais profissional e reconhecível.

## Ícones Disponíveis

### 📱 **Plataformas Suportadas**

#### **Facebook**
- **Ícone**: `static/images/social/facebook.svg`
- **Cor**: #1877f2 (Azul oficial)
- **Detecção**: facebook, fb.com, facebook.com

#### **Instagram**
- **Ícone**: `static/images/social/instagram.svg`
- **Cor**: Gradiente oficial (laranja para rosa)
- **Detecção**: instagram, ig, insta

#### **Twitter/X**
- **Ícone**: `static/images/social/twitter.svg`
- **Cor**: #1da1f2 (Azul oficial)
- **Detecção**: twitter, x.com, t.co

#### **YouTube**
- **Ícone**: `static/images/social/youtube.svg`
- **Cor**: #ff0000 (Vermelho oficial)
- **Detecção**: youtube, yt, youtu.be

#### **WhatsApp**
- **Ícone**: `static/images/social/whatsapp.svg`
- **Cor**: #25d366 (Verde oficial)
- **Detecção**: whatsapp, wa.me, wa

#### **TikTok**
- **Ícone**: `static/images/social/tiktok.svg`
- **Cor**: Gradiente oficial (rosa para azul)
- **Detecção**: tiktok, tt

## Configuração

### 1. **Página de Contato**

Configure as redes sociais no painel administrativo em **Admin > Contato**:

```json
{
  "facebook": "https://facebook.com/radioshostlink",
  "instagram": "https://instagram.com/radioshostlink",
  "twitter": "https://twitter.com/radioshostlink",
  "youtube": "https://youtube.com/radioshostlink",
  "whatsapp": "https://wa.me/5511999999999",
  "tiktok": "https://tiktok.com/@radioshostlink"
}
```

### 2. **Locutores**

Para os locutores, adicione as redes sociais no formato texto:

```
Instagram: @locutor_nome
Facebook: facebook.com/locutor
Twitter: @locutor_nome
WhatsApp: wa.me/5511999999999
```

## Funcionalidades

### 🎨 **Detecção Automática**
- O sistema detecta automaticamente a plataforma baseada no texto
- Ícones são adicionados automaticamente
- Links são tornados clicáveis

### 📱 **Responsividade**
- Ícones se adaptam a diferentes tamanhos de tela
- Efeitos hover suaves
- Animações de transição

### 🔗 **Links Inteligentes**
- URLs são automaticamente convertidas em links clicáveis
- Abrem em nova aba
- Segurança com `rel="noopener noreferrer"`

## Arquivos do Sistema

### **Ícones SVG**
- `static/images/social/facebook.svg`
- `static/images/social/instagram.svg`
- `static/images/social/twitter.svg`
- `static/images/social/youtube.svg`
- `static/images/social/whatsapp.svg`
- `static/images/social/tiktok.svg`

### **JavaScript**
- `static/js/social-icons.js` - Lógica de detecção e renderização

### **CSS**
- `static/css/styles.css` - Estilos das redes sociais

## Uso Programático

### **Detectar e Renderizar Ícones**
```javascript
// Renderizar ícones automaticamente
window.SocialIcons.render();

// Tornar links clicáveis
window.SocialIcons.makeClickable();

// Estilizar redes sociais dos locutores
window.SocialIcons.styleLocutor();
```

### **Criar Cards Dinâmicos**
```javascript
const redes = {
    facebook: "https://facebook.com/radioshostlink",
    instagram: "https://instagram.com/radioshostlink"
};

window.SocialIcons.createCards(container, redes);
```

## Estilos CSS

### **Cards de Redes Sociais**
```css
.social-card {
    background: white;
    padding: 40px 30px;
    border-radius: 15px;
    box-shadow: 0 10px 30px rgba(0, 0, 0, 0.1);
    transition: all 0.3s ease;
}

.social-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2);
}
```

### **Ícones**
```css
.social-icon img {
    width: 48px;
    height: 48px;
    filter: brightness(0) invert(1);
    transition: all 0.3s ease;
}

.social-card:hover .social-icon img {
    transform: scale(1.1);
    filter: brightness(1) invert(0);
}
```

## Cores Oficiais

### **Gradientes por Plataforma**
- **Facebook**: `linear-gradient(135deg, #1877f2, #0d6efd)`
- **Instagram**: `linear-gradient(45deg, #f09433, #e6683c, #dc2743, #cc2366, #bc1888)`
- **Twitter**: `linear-gradient(135deg, #1da1f2, #0ea5e9)`
- **YouTube**: `linear-gradient(135deg, #ff0000, #dc2626)`
- **WhatsApp**: `linear-gradient(135deg, #25d366, #128c7e)`
- **TikTok**: `linear-gradient(45deg, #ff0050, #00f2ea, #ff0050)`

## Compatibilidade

### **Navegadores**
- ✅ Chrome 60+
- ✅ Firefox 55+
- ✅ Safari 12+
- ✅ Edge 79+

### **Dispositivos**
- ✅ Desktop
- ✅ Tablet
- ✅ Mobile

## Personalização

### **Adicionar Nova Plataforma**
1. Crie o ícone SVG em `static/images/social/`
2. Adicione a detecção no `social-icons.js`
3. Configure as cores no CSS
4. Atualize a documentação

### **Exemplo de Nova Plataforma**
```javascript
// Em social-icons.js
} else if (text.includes('linkedin')) {
    iconPath = '/static/images/social/linkedin.svg';
    platform = 'LinkedIn';
}
```

```css
/* Em styles.css */
.social-card.linkedin {
    background: linear-gradient(135deg, #0077b5, #005885);
}
```

## Troubleshooting

### **Problemas Comuns**

#### 1. Ícones não aparecem
- Verifique se os arquivos SVG existem
- Confirme se o JavaScript está carregando
- Verifique o console para erros

#### 2. Links não funcionam
- Confirme se as URLs estão corretas
- Verifique se o formato JSON é válido
- Teste os links manualmente

#### 3. Estilos não aplicam
- Verifique se o CSS está carregando
- Confirme se as classes estão corretas
- Verifique a especificidade do CSS

## Contribuição

Para adicionar novas plataformas:

1. Crie o ícone SVG oficial
2. Adicione a detecção no JavaScript
3. Configure as cores no CSS
4. Teste em diferentes dispositivos
5. Atualize a documentação

## Licença

Os ícones SVG são baseados nos logos oficiais das respectivas plataformas e seguem suas diretrizes de marca. 