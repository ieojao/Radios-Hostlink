// Player de Rádio Moderno
class RadioPlayer {
    constructor() {
        this.audio = null;
        this.isPlaying = false;
        this.volume = 0.7;
        this.streamingUrl = null;
        this.currentTrack = {
            title: 'Rádio Online',
            artist: 'Ao Vivo',
            cover: null
        };
        
        this.init();
    }
    
    init() {
        this.createPlayerHTML();
        this.bindEvents();
        this.loadStreamingUrl();
        this.updatePlayerInfo();
    }
    
    createPlayerHTML() {
        // Criar o HTML do player se não existir
        if (!document.querySelector('.radio-player')) {
            const playerHTML = `
                <div class="radio-player" id="radioPlayer">
                    <div class="player-container">
                        <div class="player-info">
                            <div class="player-cover" id="playerCover">
                                <span class="radio-icon">📻</span>
                            </div>
                            <div class="player-details">
                                <div class="player-title" id="playerTitle">Carregando...</div>
                                <div class="player-subtitle" id="playerSubtitle">Conectando...</div>
                                <div class="player-status">
                                    <div class="status-indicator" id="statusIndicator"></div>
                                    <span class="status-text" id="statusText">Conectando...</span>
                                </div>
                            </div>
                        </div>
                        <div class="player-controls">
                            <button class="control-btn" id="prevBtn" data-tooltip="Anterior">⏮</button>
                            <button class="control-btn play-btn" id="playBtn" data-tooltip="Play/Pause">▶</button>
                            <button class="control-btn" id="nextBtn" data-tooltip="Próximo">⏭</button>
                            <div class="volume-control" data-volume="Volume: 70%">
                                <button class="control-btn" id="muteBtn" data-tooltip="Mutar">🔊</button>
                                <input type="range" class="volume-slider" id="volumeSlider" min="0" max="100" value="70">
                            </div>
                        </div>
                    </div>
                    <div class="player-progress">
                        <div class="progress-bar" id="progressBar"></div>
                    </div>
                </div>
                <button class="player-toggle" id="playerToggle" data-tooltip="Abrir Player">📻</button>
            `;
            
            document.body.insertAdjacentHTML('beforeend', playerHTML);
        }
    }
    
    bindEvents() {
        // Botão de toggle do player
        const playerToggle = document.getElementById('playerToggle');
        const radioPlayer = document.getElementById('radioPlayer');
        
        if (playerToggle) {
            playerToggle.addEventListener('click', () => {
                radioPlayer.classList.toggle('active');
                this.updateToggleButton();
            });
        }
        
        // Botão de play/pause
        const playBtn = document.getElementById('playBtn');
        if (playBtn) {
            playBtn.addEventListener('click', () => this.togglePlay());
        }
        
        // Controle de volume
        const volumeSlider = document.getElementById('volumeSlider');
        const muteBtn = document.getElementById('muteBtn');
        
        if (volumeSlider) {
            volumeSlider.addEventListener('input', (e) => {
                this.setVolume(e.target.value / 100);
                this.updateVolumeDisplay();
            });
        }
        
        if (muteBtn) {
            muteBtn.addEventListener('click', () => this.toggleMute());
        }
        
        // Botões de navegação (para futuras funcionalidades)
        const prevBtn = document.getElementById('prevBtn');
        const nextBtn = document.getElementById('nextBtn');
        
        if (prevBtn) {
            prevBtn.addEventListener('click', () => this.previousTrack());
        }
        
        if (nextBtn) {
            nextBtn.addEventListener('click', () => this.nextTrack());
        }
        
        // Eventos de teclado
        document.addEventListener('keydown', (e) => {
            if (e.code === 'Space' && !e.target.matches('input, textarea')) {
                e.preventDefault();
                this.togglePlay();
            }
        });
    }
    
    async loadStreamingUrl() {
        try {
            // Buscar URL de streaming da configuração
            const response = await fetch('/api/streaming-url');
            const data = await response.json();
            
            if (data.streaming_url) {
                this.streamingUrl = data.streaming_url;
                this.initAudio();
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
        
        // Eventos do áudio
        this.audio.addEventListener('loadstart', () => this.setLoading());
        this.audio.addEventListener('canplay', () => this.setReady());
        this.audio.addEventListener('play', () => this.onPlay());
        this.audio.addEventListener('pause', () => this.onPause());
        this.audio.addEventListener('ended', () => this.onEnded());
        this.audio.addEventListener('error', (e) => this.onError(e));
        this.audio.addEventListener('waiting', () => this.setLoading());
        this.audio.addEventListener('playing', () => this.setPlaying());
        
        // Atualizar progresso
        this.audio.addEventListener('timeupdate', () => this.updateProgress());
        
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
    
    play() {
        if (!this.audio) return;
        
        this.audio.play().then(() => {
            this.isPlaying = true;
            this.updatePlayButton();
            this.updatePlayerCover();
        }).catch(error => {
            console.error('Erro ao reproduzir:', error);
            this.setError('Erro ao reproduzir áudio');
        });
    }
    
    pause() {
        if (!this.audio) return;
        
        this.audio.pause();
        this.isPlaying = false;
        this.updatePlayButton();
        this.updatePlayerCover();
    }
    
    setVolume(volume) {
        this.volume = volume;
        if (this.audio) {
            this.audio.volume = volume;
        }
        this.updateVolumeDisplay();
    }
    
    toggleMute() {
        if (!this.audio) return;
        
        if (this.audio.muted) {
            this.audio.muted = false;
            this.updateMuteButton(false);
        } else {
            this.audio.muted = true;
            this.updateMuteButton(true);
        }
    }
    
    previousTrack() {
        // Funcionalidade para futuras implementações
        console.log('Track anterior');
    }
    
    nextTrack() {
        // Funcionalidade para futuras implementações
        console.log('Próxima track');
    }
    
    updatePlayButton() {
        const playBtn = document.getElementById('playBtn');
        if (playBtn) {
            playBtn.innerHTML = this.isPlaying ? '⏸' : '▶';
        }
    }
    
    updatePlayerCover() {
        const playerCover = document.getElementById('playerCover');
        if (playerCover) {
            if (this.isPlaying) {
                playerCover.classList.add('playing');
            } else {
                playerCover.classList.remove('playing');
            }
        }
    }
    
    updateVolumeDisplay() {
        const volumeControl = document.querySelector('.volume-control');
        const volumeSlider = document.getElementById('volumeSlider');
        const muteBtn = document.getElementById('muteBtn');
        
        if (volumeControl) {
            volumeControl.setAttribute('data-volume', `Volume: ${Math.round(this.volume * 100)}%`);
        }
        
        if (volumeSlider) {
            volumeSlider.value = this.volume * 100;
        }
        
        if (muteBtn) {
            muteBtn.innerHTML = this.volume === 0 ? '🔇' : '🔊';
        }
    }
    
    updateMuteButton(muted) {
        const muteBtn = document.getElementById('muteBtn');
        if (muteBtn) {
            muteBtn.innerHTML = muted ? '🔇' : '🔊';
        }
    }
    
    updateProgress() {
        if (!this.audio) return;
        
        const progressBar = document.getElementById('progressBar');
        if (progressBar) {
            // Para streaming, mostrar progresso baseado no tempo de reprodução
            const progress = (this.audio.currentTime / 100) % 100; // Simular progresso
            progressBar.style.width = `${progress}%`;
        }
    }
    
    updatePlayerInfo() {
        const playerTitle = document.getElementById('playerTitle');
        const playerSubtitle = document.getElementById('playerSubtitle');
        
        if (playerTitle) {
            playerTitle.textContent = this.currentTrack.title;
        }
        
        if (playerSubtitle) {
            playerSubtitle.textContent = this.currentTrack.artist;
        }
    }
    
    updateToggleButton() {
        const playerToggle = document.getElementById('playerToggle');
        const radioPlayer = document.getElementById('radioPlayer');
        
        if (playerToggle && radioPlayer) {
            if (radioPlayer.classList.contains('active')) {
                playerToggle.innerHTML = '📻';
                playerToggle.setAttribute('data-tooltip', 'Fechar Player');
            } else {
                playerToggle.innerHTML = '📻';
                playerToggle.setAttribute('data-tooltip', 'Abrir Player');
            }
        }
    }
    
    setLoading() {
        this.updateStatus('Conectando...', 'loading');
        const playerCover = document.getElementById('playerCover');
        if (playerCover) {
            playerCover.classList.add('player-loading');
        }
    }
    
    setReady() {
        this.updateStatus('Pronto para reproduzir', 'ready');
        const playerCover = document.getElementById('playerCover');
        if (playerCover) {
            playerCover.classList.remove('player-loading');
        }
    }
    
    setPlaying() {
        this.updateStatus('Reproduzindo', 'playing');
    }
    
    setError(message) {
        this.updateStatus(message, 'error');
        const radioPlayer = document.getElementById('radioPlayer');
        if (radioPlayer) {
            radioPlayer.classList.add('player-error');
        }
    }
    
    onPlay() {
        this.isPlaying = true;
        this.updatePlayButton();
        this.updatePlayerCover();
        this.setPlaying();
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
    }
    
    updateStatus(message, type) {
        const statusText = document.getElementById('statusText');
        const statusIndicator = document.getElementById('statusIndicator');
        
        if (statusText) {
            statusText.textContent = message;
        }
        
        if (statusIndicator) {
            statusIndicator.className = 'status-indicator';
            
            switch (type) {
                case 'loading':
                    statusIndicator.style.background = '#f59e0b';
                    break;
                case 'ready':
                    statusIndicator.style.background = '#10b981';
                    break;
                case 'playing':
                    statusIndicator.style.background = '#10b981';
                    break;
                case 'paused':
                    statusIndicator.style.background = '#6b7280';
                    break;
                case 'error':
                    statusIndicator.style.background = '#ef4444';
                    break;
                case 'ended':
                    statusIndicator.style.background = '#6b7280';
                    break;
            }
        }
    }
    
    // Método para atualizar informações da música atual (se disponível)
    updateCurrentTrack(trackInfo) {
        this.currentTrack = { ...this.currentTrack, ...trackInfo };
        this.updatePlayerInfo();
        
        // Atualizar cover se fornecido
        if (trackInfo.cover) {
            const playerCover = document.getElementById('playerCover');
            if (playerCover) {
                playerCover.innerHTML = `<img src="${trackInfo.cover}" alt="Capa da música">`;
            }
        }
    }
    
    // Método para obter estatísticas do player
    getStats() {
        return {
            isPlaying: this.isPlaying,
            volume: this.volume,
            currentTrack: this.currentTrack,
            streamingUrl: this.streamingUrl
        };
    }
}

// Inicializar o player quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    window.radioPlayer = new RadioPlayer();
    
    // Expor métodos globais para uso em outros scripts
    window.toggleRadioPlayer = () => window.radioPlayer.togglePlay();
    window.setRadioVolume = (volume) => window.radioPlayer.setVolume(volume);
    window.getRadioStats = () => window.radioPlayer.getStats();
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