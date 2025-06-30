# Player de Rádio Moderno

## Visão Geral

O novo player de rádio foi completamente redesenhado para oferecer uma experiência moderna e funcional. Ele inclui controles avançados, interface responsiva e funcionalidades de streaming em tempo real.

## Características Principais

### 🎵 Funcionalidades de Áudio
- **Streaming em tempo real** com suporte a múltiplos formatos (MP3, AAC, OGG)
- **Controle de volume** com slider interativo
- **Botão de mute** para silenciar rapidamente
- **Auto-reconexão** em caso de perda de sinal
- **Buffer inteligente** para reprodução suave

### 🎨 Interface Moderna
- **Design responsivo** que se adapta a qualquer dispositivo
- **Animações suaves** e transições elegantes
- **Tema escuro** com gradientes modernos
- **Controles intuitivos** com tooltips informativos
- **Indicadores visuais** de status (conectando, reproduzindo, erro)

### 📱 Responsividade
- **Mobile-first** design
- **Controles touch-friendly** para dispositivos móveis
- **Modo compacto** em telas pequenas
- **Ocultação automática** de controles desnecessários

### ⌨️ Atalhos de Teclado
- **Espaço**: Play/Pause
- **Setas ↑↓**: Controle de volume
- **M**: Mutar/Desmutar
- **P**: Mostrar/Ocultar player

## Arquivos do Sistema

### CSS
- `static/css/player.css` - Estilos principais do player

### JavaScript
- `static/js/player.js` - Lógica principal do player
- `static/js/player-config.js` - Configurações do player
- `static/js/main.js` - Funcionalidades gerais do site

### Backend
- `app.py` - APIs para streaming e estatísticas

## Configuração

### 1. URL de Streaming

Configure a URL de streaming no arquivo `config.env`:

```env
STREAMING_URL=https://seu-servidor-streaming.com/live
```

Ou através do painel administrativo em **Configurações > Streaming URL**.

### 2. Personalização

O player pode ser personalizado editando o arquivo `static/js/player-config.js`:

```javascript
window.RadioPlayerConfig = {
    defaultVolume: 0.7,
    autoPlay: false,
    showNotifications: true,
    // ... outras configurações
};
```

### 3. Cores e Temas

As cores podem ser personalizadas através das variáveis CSS no arquivo `static/css/player.css`:

```css
:root {
    --player-primary: #667eea;
    --player-secondary: #764ba2;
    --player-background: #1a1a2e;
    --player-text: #ffffff;
}
```

## APIs Disponíveis

### `/api/streaming-url`
Retorna a URL de streaming configurada.

**Resposta:**
```json
{
    "streaming_url": "https://streaming.example.com/live",
    "status": "success"
}
```

### `/api/player-stats`
Retorna estatísticas do player (para futuras implementações).

**Resposta:**
```json
{
    "status": "success",
    "data": {
        "listeners": 0,
        "current_track": {
            "title": "Rádio Online",
            "artist": "Ao Vivo",
            "duration": 0
        },
        "stream_status": "online"
    }
}
```

## Uso Programático

### Inicialização
O player é inicializado automaticamente quando a página carrega.

### Controles via JavaScript
```javascript
// Toggle play/pause
window.radioPlayer.togglePlay();

// Definir volume (0-1)
window.radioPlayer.setVolume(0.5);

// Obter estatísticas
const stats = window.radioPlayer.getStats();

// Atualizar informações da música
window.radioPlayer.updateCurrentTrack({
    title: 'Nome da Música',
    artist: 'Artista',
    cover: 'url-da-capa.jpg'
});
```

### Eventos
```javascript
// Escutar eventos do player
document.addEventListener('playerReady', () => {
    console.log('Player pronto');
});

document.addEventListener('playerPlay', () => {
    console.log('Reprodução iniciada');
});

document.addEventListener('playerPause', () => {
    console.log('Reprodução pausada');
});

document.addEventListener('playerError', (event) => {
    console.log('Erro no player:', event.detail);
});
```

## Compatibilidade

### Navegadores Suportados
- ✅ Chrome 60+
- ✅ Firefox 55+
- ✅ Safari 12+
- ✅ Edge 79+

### Dispositivos
- ✅ Desktop
- ✅ Tablet
- ✅ Mobile
- ✅ Smart TV (navegadores web)

## Troubleshooting

### Problemas Comuns

#### 1. Player não carrega
- Verifique se a URL de streaming está configurada
- Confirme se o servidor de streaming está online
- Verifique o console do navegador para erros

#### 2. Áudio não reproduz
- Verifique se o navegador permite autoplay
- Confirme se o dispositivo não está mutado
- Teste a URL de streaming em outro player

#### 3. Player não aparece
- Verifique se os arquivos CSS e JS estão carregando
- Confirme se não há conflitos com outros scripts
- Verifique se o JavaScript está habilitado

### Logs de Debug

Para ativar logs de debug, edite `player-config.js`:

```javascript
window.RadioPlayerConfig.debug = {
    enabled: true,
    logLevel: 'debug',
    showConsoleLogs: true
};
```

## Personalização Avançada

### Adicionar Novos Controles
```javascript
// Adicionar botão personalizado
const customBtn = document.createElement('button');
customBtn.textContent = 'Meu Botão';
customBtn.addEventListener('click', () => {
    // Sua lógica aqui
});
document.querySelector('.player-controls').appendChild(customBtn);
```

### Modificar Comportamento
```javascript
// Sobrescrever método de play
const originalPlay = window.radioPlayer.play;
window.radioPlayer.play = function() {
    console.log('Play personalizado');
    return originalPlay.call(this);
};
```

## Contribuição

Para contribuir com melhorias no player:

1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Implemente as mudanças
4. Teste em diferentes dispositivos
5. Envie um pull request

## Licença

Este player é parte do projeto Radios Hostlink e segue a mesma licença do projeto principal. 