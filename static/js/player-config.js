// Configurações do Player de Rádio
window.RadioPlayerConfig = {
    // Configurações básicas
    defaultVolume: 0.7,
    autoPlay: false,
    showNotifications: true,
    
    // Configurações de UI
    playerPosition: 'bottom', // 'bottom' ou 'top'
    showProgressBar: true,
    showVolumeControl: true,
    showTrackInfo: true,
    
    // Configurações de streaming
    streamingFormats: ['mp3', 'aac', 'ogg'],
    bufferSize: 10, // segundos
    reconnectAttempts: 3,
    reconnectDelay: 5000, // milissegundos
    
    // Configurações de metadados
    updateMetadataInterval: 10000, // milissegundos
    showCurrentTrack: true,
    
    // Configurações de notificações
    notificationTimeout: 5000,
    showPlayPauseNotification: true,
    
    // Configurações de teclas de atalho
    keyboardShortcuts: {
        playPause: 'Space',
        volumeUp: 'ArrowUp',
        volumeDown: 'ArrowDown',
        mute: 'M',
        togglePlayer: 'P'
    },
    
    // Configurações de cores (podem ser sobrescritas pelo CSS)
    colors: {
        primary: '#667eea',
        secondary: '#764ba2',
        background: '#1a1a2e',
        text: '#ffffff',
        accent: '#10b981'
    },
    
    // Configurações de animações
    animations: {
        enabled: true,
        duration: 300,
        easing: 'cubic-bezier(0.4, 0, 0.2, 1)'
    },
    
    // Configurações de responsividade
    mobile: {
        hideVolumeOnMobile: true,
        compactMode: true,
        touchGestures: true
    },
    
    // Configurações de analytics (opcional)
    analytics: {
        enabled: false,
        trackPlayEvents: true,
        trackVolumeChanges: true,
        trackErrors: true
    },
    
    // Configurações de cache
    cache: {
        enabled: true,
        maxAge: 300000, // 5 minutos
        storageKey: 'radio_player_cache'
    },
    
    // Configurações de fallback
    fallback: {
        enableFallbackStream: true,
        fallbackStreamUrl: null,
        showOfflineMessage: true
    },
    
    // Configurações de qualidade
    quality: {
        autoQuality: true,
        preferredQuality: 'high',
        qualityLevels: ['low', 'medium', 'high']
    },
    
    // Configurações de social
    social: {
        enableSharing: true,
        shareText: 'Ouvindo {station_name}',
        shareUrl: window.location.href
    },
    
    // Configurações de acessibilidade
    accessibility: {
        enableARIA: true,
        enableKeyboardNavigation: true,
        screenReaderSupport: true,
        highContrastMode: false
    },
    
    // Configurações de debug
    debug: {
        enabled: false,
        logLevel: 'info', // 'error', 'warn', 'info', 'debug'
        showConsoleLogs: false
    }
};

// Função para atualizar configurações
window.updatePlayerConfig = function(newConfig) {
    window.RadioPlayerConfig = { ...window.RadioPlayerConfig, ...newConfig };
    
    // Notificar o player sobre mudanças na configuração
    if (window.radioPlayer && window.radioPlayer.updateConfig) {
        window.radioPlayer.updateConfig(window.RadioPlayerConfig);
    }
};

// Função para obter configuração
window.getPlayerConfig = function(key) {
    return key ? window.RadioPlayerConfig[key] : window.RadioPlayerConfig;
};

// Configurações específicas por dispositivo
if (window.innerWidth <= 768) {
    window.RadioPlayerConfig.mobile.compactMode = true;
    window.RadioPlayerConfig.mobile.hideVolumeOnMobile = true;
}

// Configurações específicas por navegador
const userAgent = navigator.userAgent.toLowerCase();
if (userAgent.includes('safari') && !userAgent.includes('chrome')) {
    // Safari tem algumas limitações com autoplay
    window.RadioPlayerConfig.autoPlay = false;
    window.RadioPlayerConfig.showNotifications = false;
}

if (userAgent.includes('firefox')) {
    // Firefox tem melhor suporte para streaming
    window.RadioPlayerConfig.streamingFormats = ['mp3', 'aac', 'ogg', 'webm'];
} 