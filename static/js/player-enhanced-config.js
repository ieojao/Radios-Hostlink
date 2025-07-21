/* ========================================
   CONFIGURAÇÕES DO PLAYER ENHANCED
   ======================================== */

window.RadioPlayerEnhancedConfig = {
    // ===== CONFIGURAÇÕES BÁSICAS =====
    defaultVolume: 0.7,
    autoPlay: false,

    enableKeyboardShortcuts: true,
    enableTouchGestures: true,
    
    // ===== CONFIGURAÇÕES DE UI =====
    playerPosition: 'bottom', // 'bottom' ou 'top'
    showProgressBar: true,
    showVolumeControl: true,
    showTrackInfo: true,
    enableAnimations: true,
    enableHoverEffects: true,
    
    // ===== CONFIGURAÇÕES DE STREAMING =====
    streamingFormats: ['mp3', 'aac', 'ogg', 'webm'],
    bufferSize: 15, // segundos
    reconnectAttempts: 5,
    reconnectDelay: 3000, // milissegundos
    autoReconnect: true,
    
    // ===== CONFIGURAÇÕES DE METADADOS =====
    updateMetadataInterval: 8000, // milissegundos
    showCurrentTrack: true,
    enableMetadataCache: true,
    cacheDuration: 30000, // 30 segundos
    

    
    // ===== CONFIGURAÇÕES DE TECLAS DE ATALHO =====
    keyboardShortcuts: {
        playPause: 'Space',
        volumeUp: 'ArrowUp',
        volumeDown: 'ArrowDown',
        mute: 'M',
        togglePlayer: 'P',
        reconnect: 'R',
        previous: 'ArrowLeft',
        next: 'ArrowRight'
    },
    
    // ===== CONFIGURAÇÕES DE CORES =====
    colors: {
        primary: '#667eea',
        secondary: '#764ba2',
        accent: '#10b981',
        warning: '#f59e0b',
        error: '#ef4444',
        background: 'linear-gradient(135deg, #1a1a2e 0%, #16213e 50%, #0f3460 100%)',
        surface: 'rgba(255, 255, 255, 0.1)',
        text: '#ffffff',
        textSecondary: 'rgba(255, 255, 255, 0.7)',
        border: 'rgba(255, 255, 255, 0.2)'
    },
    
    // ===== CONFIGURAÇÕES DE ANIMAÇÕES =====
    animations: {
        enabled: true,
        duration: 300,
        easing: 'cubic-bezier(0.4, 0, 0.2, 1)',
        enableHoverEffects: true,
        enableLoadingAnimations: true,
        enableProgressAnimations: true
    },
    
    // ===== CONFIGURAÇÕES DE RESPONSIVIDADE =====
    mobile: {
        hideVolumeOnMobile: true,
        compactMode: true,
        touchGestures: true,
        enableSwipeGestures: true,
        enableTapGestures: true,
        enableLongPressGestures: false
    },
    
    // ===== CONFIGURAÇÕES DE ANALYTICS =====
    analytics: {
        enabled: false,
        trackPlayEvents: true,
        trackVolumeChanges: true,
        trackErrors: true,
        trackUserInteractions: true,
        trackSessionDuration: true
    },
    
    // ===== CONFIGURAÇÕES DE CACHE =====
    cache: {
        enabled: true,
        maxAge: 300000, // 5 minutos
        storageKey: 'radio_player_enhanced_cache',
        enableOfflineMode: false,
        cacheMetadata: true,
        cacheSettings: true
    },
    
    // ===== CONFIGURAÇÕES DE FALLBACK =====
    fallback: {
        enableFallbackStream: true,
        fallbackStreamUrl: null,
        showOfflineMessage: true,
        enableRetryMechanism: true,
        maxRetryAttempts: 3
    },
    
    // ===== CONFIGURAÇÕES DE QUALIDADE =====
    quality: {
        autoQuality: true,
        preferredQuality: 'high',
        qualityLevels: ['low', 'medium', 'high'],
        enableBitrateDetection: true,
        enableQualitySwitching: false
    },
    
    // ===== CONFIGURAÇÕES DE SOCIAL =====
    social: {
        enableSharing: true,
        shareText: 'Ouvindo {station_name}',
        shareUrl: window.location.href,
        enableSocialButtons: false,
        enableNowPlaying: true
    },
    
    // ===== CONFIGURAÇÕES DE ACESSIBILIDADE =====
    accessibility: {
        enableARIA: true,
        enableKeyboardNavigation: true,
        screenReaderSupport: true,
        highContrastMode: false,
        enableFocusIndicators: true,
        enableVoiceCommands: false
    },
    
    // ===== CONFIGURAÇÕES DE PERFORMANCE =====
    performance: {
        enableLazyLoading: true,
        enableOptimizations: true,
        reduceAnimationsOnLowPower: true,
        enableBackgroundThrottling: true,
        maxUpdateInterval: 1000
    },
    
    // ===== CONFIGURAÇÕES DE DEBUG =====
    debug: {
        enabled: false,
        logLevel: 'info', // 'error', 'warn', 'info', 'debug'
        showConsoleLogs: false,
        enablePerformanceMonitoring: false,
        enableErrorReporting: false
    },
    
    // ===== CONFIGURAÇÕES DE PERSONALIZAÇÃO =====
    customization: {
        enableThemeSwitching: false,
        enableCustomColors: false,
        enableCustomFonts: false,
        enableLayoutCustomization: false
    },
    
    // ===== CONFIGURAÇÕES DE INTEGRAÇÃO =====
    integration: {
        enableWebSocket: false,
        enableServerSentEvents: false,
        enablePushNotifications: false,
        enableBackgroundSync: false
    }
};

// ===== FUNÇÕES DE CONFIGURAÇÃO =====

// Função para atualizar configurações
window.updatePlayerEnhancedConfig = function(newConfig) {
    window.RadioPlayerEnhancedConfig = { 
        ...window.RadioPlayerEnhancedConfig, 
        ...newConfig 
    };
    
    // Notificar o player sobre mudanças na configuração
    if (window.radioPlayerEnhanced && window.radioPlayerEnhanced.updateConfig) {
        window.radioPlayerEnhanced.updateConfig(window.RadioPlayerEnhancedConfig);
    }
    
    // Salvar configurações no localStorage
    localStorage.setItem('radioPlayerEnhancedConfig', JSON.stringify(window.RadioPlayerEnhancedConfig));
};

// Função para obter configuração
window.getPlayerEnhancedConfig = function(key) {
    return key ? window.RadioPlayerEnhancedConfig[key] : window.RadioPlayerEnhancedConfig;
};

// Função para resetar configurações
window.resetPlayerEnhancedConfig = function() {
    // Recarregar configurações padrão
    location.reload();
};

// Função para salvar configurações
window.savePlayerEnhancedConfig = function() {
    localStorage.setItem('radioPlayerEnhancedConfig', JSON.stringify(window.RadioPlayerEnhancedConfig));
};

// Função para carregar configurações salvas
window.loadPlayerEnhancedConfig = function() {
    try {
        const saved = localStorage.getItem('radioPlayerEnhancedConfig');
        if (saved) {
            const config = JSON.parse(saved);
            window.RadioPlayerEnhancedConfig = { ...window.RadioPlayerEnhancedConfig, ...config };
        }
    } catch (error) {
        console.error('Erro ao carregar configurações:', error);
    }
};

// ===== CONFIGURAÇÕES ESPECÍFICAS POR DISPOSITIVO =====

// Detectar dispositivo móvel
const isMobile = window.innerWidth <= 768;
const isTablet = window.innerWidth > 768 && window.innerWidth <= 1024;
const isDesktop = window.innerWidth > 1024;

if (isMobile) {
    window.RadioPlayerEnhancedConfig.mobile.compactMode = true;
    window.RadioPlayerEnhancedConfig.mobile.hideVolumeOnMobile = true;
    window.RadioPlayerEnhancedConfig.animations.duration = 200; // Animações mais rápidas

}

if (isTablet) {
    window.RadioPlayerEnhancedConfig.mobile.compactMode = false;
    window.RadioPlayerEnhancedConfig.mobile.hideVolumeOnMobile = false;
}

// ===== CONFIGURAÇÕES ESPECÍFICAS POR NAVEGADOR =====

const userAgent = navigator.userAgent.toLowerCase();

// Safari
if (userAgent.includes('safari') && !userAgent.includes('chrome')) {
    window.RadioPlayerEnhancedConfig.autoPlay = false;
    window.RadioPlayerEnhancedConfig.performance.enableBackgroundThrottling = true;
}

// Firefox
if (userAgent.includes('firefox')) {
    window.RadioPlayerEnhancedConfig.streamingFormats = ['mp3', 'aac', 'ogg', 'webm'];
    window.RadioPlayerEnhancedConfig.performance.enableOptimizations = true;
}

// Chrome/Chromium
if (userAgent.includes('chrome') && !userAgent.includes('edge')) {
    window.RadioPlayerEnhancedConfig.performance.enableLazyLoading = true;
    window.RadioPlayerEnhancedConfig.performance.enableBackgroundThrottling = false;
}

// Edge
if (userAgent.includes('edge')) {
    window.RadioPlayerEnhancedConfig.performance.enableOptimizations = true;
}

// ===== CONFIGURAÇÕES ESPECÍFICAS POR CONEXÃO =====

// Detectar conexão lenta
if ('connection' in navigator) {
    const connection = navigator.connection;
    
    if (connection.effectiveType === 'slow-2g' || connection.effectiveType === '2g') {
        window.RadioPlayerEnhancedConfig.quality.preferredQuality = 'low';
        window.RadioPlayerEnhancedConfig.performance.reduceAnimationsOnLowPower = true;
    }
    
    if (connection.effectiveType === '3g') {
        window.RadioPlayerEnhancedConfig.quality.preferredQuality = 'medium';
    }
}

// ===== CONFIGURAÇÕES DE TEMA =====

// Detectar preferência de tema
if (window.matchMedia && window.matchMedia('(prefers-color-scheme: dark)').matches) {
    window.RadioPlayerEnhancedConfig.colors.background = 'linear-gradient(135deg, #0f0f23 0%, #1a1a2e 50%, #16213e 100%)';
    window.RadioPlayerEnhancedConfig.colors.surface = 'rgba(255, 255, 255, 0.05)';
    window.RadioPlayerEnhancedConfig.colors.border = 'rgba(255, 255, 255, 0.1)';
}

// ===== CONFIGURAÇÕES DE PERFORMANCE =====

// Detectar dispositivo de baixa potência
if ('hardwareConcurrency' in navigator && navigator.hardwareConcurrency <= 2) {
    window.RadioPlayerEnhancedConfig.performance.reduceAnimationsOnLowPower = true;
    window.RadioPlayerEnhancedConfig.animations.enabled = false;
    window.RadioPlayerEnhancedConfig.performance.maxUpdateInterval = 2000;
}

// Detectar memória limitada
if ('deviceMemory' in navigator && navigator.deviceMemory <= 2) {
    window.RadioPlayerEnhancedConfig.cache.enabled = false;
    window.RadioPlayerEnhancedConfig.performance.enableLazyLoading = false;
}

// ===== INICIALIZAÇÃO =====

// Carregar configurações salvas
window.loadPlayerEnhancedConfig();

// Aplicar configurações CSS dinamicamente
function applyConfigToCSS() {
    const config = window.RadioPlayerEnhancedConfig;
    const root = document.documentElement;
    
    // Aplicar cores
    root.style.setProperty('--player-primary', config.colors.primary);
    root.style.setProperty('--player-secondary', config.colors.secondary);
    root.style.setProperty('--player-accent', config.colors.accent);
    root.style.setProperty('--player-warning', config.colors.warning);
    root.style.setProperty('--player-error', config.colors.error);
    root.style.setProperty('--player-bg', config.colors.background);
    root.style.setProperty('--player-surface', config.colors.surface);
    root.style.setProperty('--player-text', config.colors.text);
    root.style.setProperty('--player-text-secondary', config.colors.textSecondary);
    root.style.setProperty('--player-border', config.colors.border);
    
    // Aplicar animações
    if (!config.animations.enabled) {
        root.style.setProperty('--player-transition', 'none');
    } else {
        root.style.setProperty('--player-transition', `all ${config.animations.duration}ms ${config.animations.easing}`);
    }
}

// Aplicar configurações quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    applyConfigToCSS();
});

// Aplicar configurações quando a janela carregar
window.addEventListener('load', function() {
    applyConfigToCSS();
});

// ===== EXPORTAÇÃO PARA USO GLOBAL =====

// Expor configurações globalmente
window.RadioPlayerConfig = window.RadioPlayerEnhancedConfig;

// Manter compatibilidade com configurações antigas
window.updatePlayerConfig = window.updatePlayerEnhancedConfig;
window.getPlayerConfig = window.getPlayerEnhancedConfig; 