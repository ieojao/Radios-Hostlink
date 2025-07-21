/* ========================================
   PLAYER DE RÁDIO ENHANCED - FUNCIONALIDADES AVANÇADAS
   ======================================== */

class RadioPlayerEnhanced {
    constructor() {
        this.audio = null;
        this.isPlaying = false;
        this.volume = 0.7;
        this.previousVolume = 0.7;
        this.streamingUrl = null;
        this.isMuted = false;
        this.currentTrack = {
            title: 'Rádio Online',
            artist: 'Ao Vivo',
            cover: null,
            duration: 0,
            currentTime: 0
        };
        
        // Configurações avançadas
        this.config = {
            autoPlay: false,
            showNotifications: true,
            enableMiniPlayer: true,
            enableKeyboardShortcuts: true,
            enableTouchGestures: true,
            reconnectAttempts: 3,
            reconnectDelay: 5000,
            updateInterval: 1000,
            fadeInDuration: 500,
            fadeOutDuration: 300
        };
        
        // Estado do player
        this.state = {
            isLoading: false,
            isError: false,
            isConnected: false,
            reconnectCount: 0,
            lastUpdate: Date.now()
        };
        
        // Cache de dados
        this.cache = {
            metadata: null,
            lastUpdate: 0,
            cacheDuration: 30000 // 30 segundos
        };
        
        this.init();
    }
    
    async init() {
        try {
            this.createPlayerHTML();
            this.bindEvents();
            await this.loadStreamingUrl();
            this.setupKeyboardShortcuts();
            this.setupTouchGestures();
            this.updatePlayerInfo();
            this.startUpdateLoop();
            
            // Carregar configurações salvas
            this.loadSavedSettings();
            

            
            console.log('🎵 Radio Player Enhanced inicializado com sucesso!');
        } catch (error) {
            console.error('❌ Erro ao inicializar player:', error);

        }
    }
    
    createPlayerHTML() {
        // Criar o HTML do player enhanced se não existir
        if (!document.querySelector('.radio-player-enhanced')) {
            const playerHTML = `
                <div class="radio-player-enhanced" id="radioPlayerEnhanced">
                    <div class="player-container-enhanced">
                        <div class="player-info-enhanced">
                            <div class="player-cover-enhanced" id="playerCoverEnhanced">
                                <span class="radio-icon-enhanced">🎵</span>
                            </div>
                            <div class="player-details-enhanced">
                                <div class="player-title-enhanced" id="playerTitleEnhanced">Carregando...</div>
                                <div class="player-subtitle-enhanced" id="playerSubtitleEnhanced">Conectando...</div>
                                <div class="player-status-enhanced">
                                    <div class="status-indicator-enhanced" id="statusIndicatorEnhanced"></div>
                                    <span class="status-text-enhanced" id="statusTextEnhanced">Conectando...</span>
                                </div>
                            </div>
                        </div>
                        <div class="player-controls-enhanced">
                            <button class="control-btn-enhanced" id="prevBtnEnhanced" data-tooltip="Anterior" aria-label="Música anterior">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                                    <path d="M6 6h2v12H6zm3.5 6l8.5 6V6z"/>
                                </svg>
                            </button>
                            <button class="control-btn-enhanced play-btn-enhanced" id="playBtnEnhanced" data-tooltip="Play/Pause" aria-label="Play/Pause">
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" id="playIcon">
                                    <path d="M8 5v14l11-7z"/>
                                </svg>
                                <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor" id="pauseIcon" style="display: none;">
                                    <path d="M6 19h4V5H6v14zm8-14v14h4V5h-4z"/>
                                </svg>
                            </button>
                            <button class="control-btn-enhanced" id="nextBtnEnhanced" data-tooltip="Próximo" aria-label="Próxima música">
                                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                                    <path d="M6 18l8.5-6L6 6v12zM16 6v12h2V6h-2z"/>
                                </svg>
                            </button>
                            <div class="volume-control-enhanced" data-volume="Volume: 70%">
                                <button class="control-btn-enhanced" id="muteBtnEnhanced" data-tooltip="Mutar" aria-label="Mutar/Desmutar">
                                    <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" id="volumeIcon">
                                        <path d="M3 9v6h4l5 5V4L7 9H3zm13.5 3c0-1.77-1.02-3.29-2.5-4.03v8.05c1.48-.73 2.5-2.25 2.5-4.02zM14 3.23v2.06c2.89.86 5 3.54 5 6.71s-2.11 5.85-5 6.71v2.06c4.01-.91 7-4.49 7-8.77s-2.99-7.86-7-8.77z"/>
                                    </svg>
                                    <svg width="18" height="18" viewBox="0 0 24 24" fill="currentColor" id="muteIcon" style="display: none;">
                                        <path d="M16.5 12c0-1.77-1.02-3.29-2.5-4.03v2.21l2.45 2.45c.03-.2.05-.41.05-.63zm2.5 0c0 .94-.2 1.82-.54 2.64l1.51 1.51C20.63 14.91 21 13.5 21 12c0-4.28-2.99-7.86-7-8.77v2.06c2.89.86 5 3.54 5 6.71zM4.27 3L3 4.27 7.73 9H3v6h4l5 5v-6.73l4.25 4.25c-.67.52-1.42.93-2.25 1.18v2.06c1.38-.31 2.63-.95 3.69-1.81L19.73 21 21 19.73l-9-9L4.27 3zM12 4L9.91 6.09 12 8.18V4z"/>
                                    </svg>
                                </button>
                                <input type="range" class="volume-slider-enhanced" id="volumeSliderEnhanced" min="0" max="100" value="70" aria-label="Controle de volume">
                            </div>

                        </div>
                    </div>
                    <div class="player-progress-enhanced">
                        <div class="progress-bar-enhanced" id="progressBarEnhanced"></div>
                    </div>
                </div>
                

                
                <!-- Botão Toggle -->
                <button class="player-toggle-enhanced" id="playerToggleEnhanced" data-tooltip="Abrir Player" aria-label="Abrir/Fechar player">
                    <svg width="24" height="24" viewBox="0 0 24 24" fill="currentColor">
                        <path d="M12 3v10.55c-.59-.34-1.27-.55-2-.55-2.21 0-4 1.79-4 4s1.79 4 4 4 4-1.79 4-4V7h4V3h-6z"/>
                    </svg>
                </button>
                

            `;
            
            document.body.insertAdjacentHTML('beforeend', playerHTML);
        }
    }
    
    bindEvents() {
        // Botão de toggle do player
        const playerToggle = document.getElementById('playerToggleEnhanced');
        const radioPlayer = document.getElementById('radioPlayerEnhanced');
        const miniPlayer = document.getElementById('miniPlayerEnhanced');
        
        if (playerToggle) {
            playerToggle.addEventListener('click', () => {
                this.togglePlayer();
            });
        }
        
        // Botão de play/pause
        const playBtn = document.getElementById('playBtnEnhanced');
        
        if (playBtn) {
            playBtn.addEventListener('click', () => this.togglePlay());
        }
        
        // Controle de volume
        const volumeSlider = document.getElementById('volumeSliderEnhanced');
        const muteBtn = document.getElementById('muteBtnEnhanced');
        
        if (volumeSlider) {
            volumeSlider.addEventListener('input', (e) => {
                this.setVolume(e.target.value / 100);
                this.updateVolumeDisplay();
                this.updateVolumeVisual(e.target.value);
            });
            
            // Atualizar indicador visual inicial
            this.updateVolumeVisual(volumeSlider.value);
        }
        
        if (muteBtn) {
            muteBtn.addEventListener('click', () => this.toggleMute());
        }
        

        
        // Botões de navegação
        const prevBtn = document.getElementById('prevBtnEnhanced');
        const nextBtn = document.getElementById('nextBtnEnhanced');
        
        if (prevBtn) {
            prevBtn.addEventListener('click', () => this.previousTrack());
        }
        
        if (nextBtn) {
            nextBtn.addEventListener('click', () => this.nextTrack());
        }
        
        // Eventos de teclado
        if (this.config.enableKeyboardShortcuts) {
            this.setupKeyboardShortcuts();
        }
        
        // Eventos de toque
        if (this.config.enableTouchGestures) {
            this.setupTouchGestures();
        }
    }
    
    setupKeyboardShortcuts() {
        document.addEventListener('keydown', (e) => {
            // Ignorar se estiver em um input
            if (e.target.matches('input, textarea, select')) return;
            
            switch (e.code) {
                case 'Space':
                    e.preventDefault();
                    this.togglePlay();
                    break;
                case 'ArrowUp':
                    e.preventDefault();
                    this.adjustVolume(0.1);
                    break;
                case 'ArrowDown':
                    e.preventDefault();
                    this.adjustVolume(-0.1);
                    break;
                case 'KeyM':
                    e.preventDefault();
                    this.toggleMute();
                    break;
                case 'KeyP':
                    e.preventDefault();
                    this.togglePlayer();
                    break;
                case 'KeyR':
                    e.preventDefault();
                    this.reconnect();
                    break;
            }
        });
    }
    
    setupTouchGestures() {
        let startY = 0;
        let startVolume = 0;
        
        // Gestos de swipe para volume
        document.addEventListener('touchstart', (e) => {
            if (e.touches.length === 1) {
                startY = e.touches[0].clientY;
                startVolume = this.volume;
            }
        });
        
        document.addEventListener('touchmove', (e) => {
            if (e.touches.length === 1 && this.isPlaying) {
                e.preventDefault();
                const deltaY = startY - e.touches[0].clientY;
                const volumeChange = deltaY / 200; // Sensibilidade
                const newVolume = Math.max(0, Math.min(1, startVolume + volumeChange));
                this.setVolume(newVolume);
            }
        });
    }
    
    async loadStreamingUrl() {
        try {
            this.setState({ isLoading: true });
            
            // Buscar URL de streaming da configuração
            const response = await fetch('/api/streaming-url');
            const data = await response.json();
            
            if (data.streaming_url) {
                this.streamingUrl = data.streaming_url;
                this.initAudio();
                this.setState({ isLoading: false, isConnected: true });
                // Não mostrar notificação de conexão por padrão
                // this.showNotification('Conectado com sucesso!', 'success');
            } else {
                this.setError('URL de streaming não configurada');
            }
        } catch (error) {
            console.error('Erro ao carregar URL de streaming:', error);
            this.setError('Erro ao conectar com o servidor');
        }
    }
    
    initAudio() {
        if (!this.streamingUrl) return;
        
        this.audio = new Audio();
        this.audio.src = this.streamingUrl;
        this.audio.volume = this.volume;
        this.audio.preload = 'none';
        this.audio.crossOrigin = 'anonymous';
        
        // Eventos do áudio
        this.audio.addEventListener('loadstart', () => this.setLoading());
        this.audio.addEventListener('canplay', () => this.setReady());
        this.audio.addEventListener('play', () => this.onPlay());
        this.audio.addEventListener('pause', () => this.onPause());
        this.audio.addEventListener('ended', () => this.onEnded());
        this.audio.addEventListener('error', (e) => this.onError(e));
        this.audio.addEventListener('waiting', () => this.setLoading());
        this.audio.addEventListener('playing', () => this.setPlaying());
        this.audio.addEventListener('stalled', () => this.onStalled());
        this.audio.addEventListener('suspend', () => this.onSuspend());
        
        // Atualizar progresso
        this.audio.addEventListener('timeupdate', () => this.updateProgress());
        
        // Metadata
        this.audio.addEventListener('loadedmetadata', () => this.onMetadataLoaded());
        
        this.setReady();
    }
    
    togglePlay() {
        if (!this.audio) {
            this.initAudio();
            return;
        }
        
        if (this.isPlaying) {
            this.pause();
        } else {
            this.play();
        }
    }
    
    async play() {
        if (!this.audio) return;
        
        try {
            await this.audio.play();
            this.isPlaying = true;
            this.updatePlayButton();
            this.updatePlayerCover();
            // Só mostrar notificação se configurado
            if (this.config.showPlayPauseNotification) {
    
            }
        } catch (error) {
            console.error('Erro ao reproduzir:', error);
            this.setError('Erro ao reproduzir áudio');

        }
    }
    
    pause() {
        if (!this.audio) return;
        
        this.audio.pause();
        this.isPlaying = false;
        this.updatePlayButton();
        this.updatePlayerCover();
        // Só mostrar notificação se configurado
        if (this.config.showPlayPauseNotification) {

        }
    }
    
    setVolume(volume) {
        this.volume = Math.max(0, Math.min(1, volume));
        if (this.audio) {
            this.audio.volume = this.volume;
        }
        this.updateVolumeDisplay();
        this.saveSettings();
    }
    
    adjustVolume(delta) {
        const newVolume = this.volume + delta;
        this.setVolume(newVolume);
    }
    
    toggleMute() {
        if (!this.audio) return;
        
        if (this.isMuted) {
            this.audio.muted = false;
            this.volume = this.previousVolume;
            this.isMuted = false;
            this.updateMuteButton(false);
            // Só mostrar notificação se configurado
            if (this.config.showVolumeNotification) {
    
            }
        } else {
            this.previousVolume = this.volume;
            this.audio.muted = true;
            this.isMuted = true;
            this.updateMuteButton(true);
            // Só mostrar notificação se configurado
            if (this.config.showVolumeNotification) {
    
            }
        }
        
        this.updateVolumeDisplay();
    }
    
    togglePlayer() {
        const radioPlayer = document.getElementById('radioPlayerEnhanced');
        const miniPlayer = document.getElementById('miniPlayerEnhanced');
        const playerToggle = document.getElementById('playerToggleEnhanced');
        
        if (radioPlayer) {
            radioPlayer.classList.toggle('active');
        }
        
        if (miniPlayer) {
            miniPlayer.classList.toggle('active');
        }
        
        this.updateToggleButton();
    }
    

    
    previousTrack() {
        // Funcionalidade para futuras implementações

    }
    
    nextTrack() {
        // Funcionalidade para futuras implementações

    }
    
    reconnect() {
        if (this.state.reconnectCount >= this.config.reconnectAttempts) {

            return;
        }
        
        this.state.reconnectCount++;
        // Só mostrar notificação se configurado
        if (this.config.showReconnectNotification) {

        }
        
        setTimeout(() => {
            this.loadStreamingUrl();
        }, this.config.reconnectDelay);
    }
    
    updatePlayButton() {
        const playBtn = document.getElementById('playBtnEnhanced');
        const playIcon = document.getElementById('playIcon');
        const pauseIcon = document.getElementById('pauseIcon');
        
        if (playBtn) {
            if (this.isPlaying) {
                playIcon.style.display = 'none';
                pauseIcon.style.display = 'block';
            } else {
                playIcon.style.display = 'block';
                pauseIcon.style.display = 'none';
            }
        }
    }
    
    updatePlayerCover() {
        const playerCover = document.getElementById('playerCoverEnhanced');
        
        if (playerCover) {
            if (this.isPlaying) {
                playerCover.classList.add('playing');
            } else {
                playerCover.classList.remove('playing');
            }
        }
    }
    
    updateVolumeDisplay() {
        const volumeControl = document.querySelector('.volume-control-enhanced');
        const volumeSlider = document.getElementById('volumeSliderEnhanced');
        
        if (volumeControl) {
            const volumePercent = Math.round(this.volume * 100);
            volumeControl.setAttribute('data-volume', `Volume: ${volumePercent}%`);
        }
        
        if (volumeSlider) {
            volumeSlider.value = this.volume * 100;
            this.updateVolumeVisual(volumeSlider.value);
        }
    }
    
    updateVolumeVisual(value) {
        const volumeSlider = document.getElementById('volumeSliderEnhanced');
        if (volumeSlider) {
            const percentage = (value - volumeSlider.min) / (volumeSlider.max - volumeSlider.min) * 100;
            volumeSlider.style.setProperty('--volume-percentage', `${percentage}%`);
            
            // Atualizar o pseudo-elemento ::before
            const beforeElement = volumeSlider.querySelector('::before') || 
                                 document.querySelector('.volume-slider-enhanced::before');
            if (beforeElement) {
                beforeElement.style.width = `${percentage}%`;
            }
        }
    }
    
    updateMuteButton(muted) {
        const muteBtn = document.getElementById('muteBtnEnhanced');
        const volumeIcon = document.getElementById('volumeIcon');
        const muteIcon = document.getElementById('muteIcon');
        
        if (muteBtn) {
            if (muted) {
                volumeIcon.style.display = 'none';
                muteIcon.style.display = 'block';
            } else {
                volumeIcon.style.display = 'block';
                muteIcon.style.display = 'none';
            }
        }
    }
    
    updateProgress() {
        if (!this.audio) return;
        
        const progressBar = document.getElementById('progressBarEnhanced');
        if (progressBar) {
            // Para streaming, mostrar progresso baseado no tempo de reprodução
            const progress = (this.audio.currentTime / 100) % 100; // Simular progresso
            progressBar.style.width = `${progress}%`;
        }
    }
    
    updatePlayerInfo() {
        const playerTitle = document.getElementById('playerTitleEnhanced');
        const playerSubtitle = document.getElementById('playerSubtitleEnhanced');
        
        if (playerTitle) {
            playerTitle.textContent = this.currentTrack.title;
        }
        
        if (playerSubtitle) {
            playerSubtitle.textContent = this.currentTrack.artist;
        }
    }
    
    updateToggleButton() {
        const playerToggle = document.getElementById('playerToggleEnhanced');
        const radioPlayer = document.getElementById('radioPlayerEnhanced');
        
        if (playerToggle && radioPlayer) {
            if (radioPlayer.classList.contains('active')) {
                playerToggle.setAttribute('data-tooltip', 'Fechar Player');
                playerToggle.setAttribute('aria-label', 'Fechar player');
            } else {
                playerToggle.setAttribute('data-tooltip', 'Abrir Player');
                playerToggle.setAttribute('aria-label', 'Abrir player');
            }
        }
    }
    

    
    setState(newState) {
        this.state = { ...this.state, ...newState };
    }
    
    setLoading() {
        this.updateStatus('Conectando...', 'loading');
        const playerCover = document.getElementById('playerCoverEnhanced');
        if (playerCover) {
            playerCover.classList.add('player-loading-enhanced');
        }
    }
    
    setReady() {
        this.updateStatus('Pronto para reproduzir', 'ready');
        const playerCover = document.getElementById('playerCoverEnhanced');
        if (playerCover) {
            playerCover.classList.remove('player-loading-enhanced');
        }
    }
    
    setPlaying() {
        this.updateStatus('Reproduzindo', 'playing');
    }
    
    setError(message) {
        this.updateStatus(message, 'error');
        const radioPlayer = document.getElementById('radioPlayerEnhanced');
        if (radioPlayer) {
            radioPlayer.classList.add('player-error-enhanced');
        }
        this.setState({ isError: true, isConnected: false });
    }
    
    onPlay() {
        this.isPlaying = true;
        this.updatePlayButton();
        this.updatePlayerCover();
        this.setPlaying();
        this.setState({ isError: false });
    }
    
    onPause() {
        this.isPlaying = false;
        this.updatePlayButton();
        this.updatePlayerCover();
        this.updateStatus('Pausado', 'paused');
    }
    
    onEnded() {
        this.isPlaying = false;
        this.updatePlayButton();
        this.updatePlayerCover();
        this.updateStatus('Transmissão finalizada', 'ended');
    }
    
    onError(error) {
        console.error('Erro no áudio:', error);
        this.setError('Erro na transmissão');
        this.setState({ isError: true, isConnected: false });
        
        // Tentar reconectar automaticamente
        if (this.state.reconnectCount < this.config.reconnectAttempts) {
            setTimeout(() => this.reconnect(), this.config.reconnectDelay);
        }
    }
    
    onStalled() {
        this.updateStatus('Conexão instável...', 'warning');
    }
    
    onSuspend() {
        this.updateStatus('Conexão suspensa', 'warning');
    }
    
    onMetadataLoaded() {
        if (this.audio) {
            this.currentTrack.duration = this.audio.duration || 0;
        }
    }
    
    updateStatus(message, type) {
        const statusText = document.getElementById('statusTextEnhanced');
        const statusIndicator = document.getElementById('statusIndicatorEnhanced');
        
        if (statusText) {
            statusText.textContent = message;
        }
        
        if (statusIndicator) {
            statusIndicator.className = 'status-indicator-enhanced';
            
            switch (type) {
                case 'loading':
                    statusIndicator.style.background = 'var(--player-warning)';
                    break;
                case 'ready':
                    statusIndicator.style.background = 'var(--player-accent)';
                    break;
                case 'playing':
                    statusIndicator.style.background = 'var(--player-accent)';
                    break;
                case 'paused':
                    statusIndicator.style.background = 'var(--player-text-secondary)';
                    break;
                case 'error':
                    statusIndicator.style.background = 'var(--player-error)';
                    break;
                case 'ended':
                    statusIndicator.style.background = 'var(--player-text-secondary)';
                    break;
                case 'warning':
                    statusIndicator.style.background = 'var(--player-warning)';
                    break;
            }
        }
    }
    
    // Método para atualizar informações da música atual
    updateCurrentTrack(trackInfo) {
        this.currentTrack = { ...this.currentTrack, ...trackInfo };
        this.updatePlayerInfo();
        
        // Atualizar cover se fornecido
        if (trackInfo.cover) {
            const playerCover = document.getElementById('playerCoverEnhanced');
            
            if (playerCover) {
                playerCover.innerHTML = `<img src="${trackInfo.cover}" alt="Capa da música">`;
            }
        }
    }
    
    // Loop de atualização
    startUpdateLoop() {
        setInterval(() => {
            this.updateProgress();
            this.updatePlayerInfo();
            
            // Verificar conexão
            if (this.audio && this.audio.readyState === 0 && this.isPlaying) {
                this.onError(new Error('Conexão perdida'));
            }
        }, this.config.updateInterval);
    }
    
    // Salvar configurações
    saveSettings() {
        const settings = {
            volume: this.volume,
            isMuted: this.isMuted
        };
        
        localStorage.setItem('radioPlayerSettings', JSON.stringify(settings));
    }
    
    // Carregar configurações salvas
    loadSavedSettings() {
        try {
            const saved = localStorage.getItem('radioPlayerSettings');
            if (saved) {
                const settings = JSON.parse(saved);
                this.volume = settings.volume || 0.7;
                this.isMuted = settings.isMuted || false;
                
                // Aplicar configurações
                this.setVolume(this.volume);
                if (this.isMuted) {
                    this.toggleMute();
                }
                // Garantir que não está minimizado
                this.isMinimized = false;
                const radioPlayer = document.getElementById('radioPlayerEnhanced');
                if (radioPlayer) radioPlayer.classList.add('active');
            }
        } catch (error) {
            console.error('Erro ao carregar configurações:', error);
        }
    }
    
    // Método para obter estatísticas do player
    getStats() {
        return {
            isPlaying: this.isPlaying,
            volume: this.volume,
            isMuted: this.isMuted,
            currentTrack: this.currentTrack,
            streamingUrl: this.streamingUrl,
            state: this.state,
            config: this.config
        };
    }
    
    // Método para atualizar configurações
    updateConfig(newConfig) {
        this.config = { ...this.config, ...newConfig };
    }
}

// Inicializar o player quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    window.radioPlayerEnhanced = new RadioPlayerEnhanced();
    
    // Expor métodos globais para uso em outros scripts
    window.toggleRadioPlayerEnhanced = () => window.radioPlayerEnhanced.togglePlay();
    window.setRadioVolumeEnhanced = (volume) => window.radioPlayerEnhanced.setVolume(volume);
    window.getRadioStatsEnhanced = () => window.radioPlayerEnhanced.getStats();
    window.updateRadioTrackEnhanced = (trackInfo) => window.radioPlayerEnhanced.updateCurrentTrack(trackInfo);
});

// Service Worker para cache offline (opcional)
if ('serviceWorker' in navigator) {
    navigator.serviceWorker.register('/sw.js')
        .then(registration => {
            console.log('Service Worker registrado:', registration);
        })
        .catch(error => {
            console.log('Erro ao registrar Service Worker:', error);
        });
} 