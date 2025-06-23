// Funções principais do site
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar funcionalidades
    initPlayer();
    initNavigation();
    initTabs();
    initWhatsApp();
    initAnimations();
});

// Player de rádio
function initPlayer() {
    const playBtn = document.querySelector('.play-btn');
    const soundBtn = document.querySelector('.sound-btn');
    const popupBtn = document.querySelector('.popup-btn');
    const menuBtn = document.querySelector('.menu-btn');
    
    if (playBtn) {
        playBtn.addEventListener('click', function() {
            // Aqui você pode adicionar a lógica para iniciar o streaming
            console.log('Iniciando streaming da rádio');
            this.textContent = this.textContent === '▶ PLAY' ? '⏸ PAUSE' : '▶ PLAY';
        });
    }
    
    if (soundBtn) {
        soundBtn.addEventListener('click', function() {
            // Controle de volume
            console.log('Controle de volume');
        });
    }
    
    if (popupBtn) {
        popupBtn.addEventListener('click', function() {
            // Abrir player em popup
            const popup = window.open('/player-popup', 'player', 'width=400,height=300');
        });
    }
    
    if (menuBtn) {
        menuBtn.addEventListener('click', function() {
            // Menu mobile
            const nav = document.querySelector('nav');
            if (nav) {
                nav.classList.toggle('mobile-open');
            }
        });
    }
}

// Navegação
function initNavigation() {
    const navLinks = document.querySelectorAll('nav a');
    
    navLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            // Remover classe active de todos os links
            navLinks.forEach(l => l.classList.remove('active'));
            // Adicionar classe active no link clicado
            this.classList.add('active');
        });
    });
}

// Tabs de programação
function initTabs() {
    const tabs = document.querySelectorAll('.tab');
    const diasProgramacao = document.querySelectorAll('.dia-programacao');
    
    tabs.forEach(tab => {
        tab.addEventListener('click', function() {
            const dia = this.getAttribute('data-dia');
            
            // Remover classe active de todas as tabs
            tabs.forEach(t => t.classList.remove('active'));
            // Adicionar classe active na tab clicada
            this.classList.add('active');
            
            // Esconder todas as programações
            diasProgramacao.forEach(diaProg => {
                diaProg.style.display = 'none';
            });
            
            // Mostrar programação do dia selecionado
            const programacaoDia = document.getElementById('programacao-' + dia.toLowerCase());
            if (programacaoDia) {
                programacaoDia.style.display = 'block';
            }
        });
    });
}

// Botão WhatsApp
function initWhatsApp() {
    const whatsappBtn = document.querySelector('.whatsapp-btn');
    
    if (whatsappBtn) {
        whatsappBtn.addEventListener('click', function(e) {
            // Adicionar efeito de clique
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'scale(1)';
            }, 150);
        });
    }
}

// Animações
function initAnimations() {
    // Animar elementos quando entram na viewport
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver(function(entries) {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
            }
        });
    }, observerOptions);
    
    // Observar elementos para animação
    const animateElements = document.querySelectorAll('.card, .stat-item, .mvv-item, .locutor-card');
    animateElements.forEach(el => {
        observer.observe(el);
    });
}

// Função para atualizar programação atual
function atualizarProgramacaoAtual() {
    fetch('/api/programacao-atual')
        .then(response => response.json())
        .then(data => {
            if (data.error) {
                console.log('Nenhuma programação atual');
            } else {
                // Atualizar informações da programação atual
                const programaAtual = document.querySelector('.programa-atual');
                if (programaAtual) {
                    const titulo = programaAtual.querySelector('h2');
                    const descricao = programaAtual.querySelector('p');
                    const horario = programaAtual.querySelector('.horario');
                    
                    if (titulo) titulo.textContent = data.titulo;
                    if (descricao) descricao.textContent = data.descricao;
                    if (horario) horario.textContent = `${data.horario_inicio} - ${data.horario_fim}`;
                }
            }
        })
        .catch(error => console.error('Erro ao buscar programação:', error));
}

// Função para atualizar timer
function atualizarTimer() {
    const timer = document.getElementById('timer');
    if (timer) {
        const agora = new Date();
        const minutos = agora.getMinutes().toString().padStart(2, '0');
        const segundos = agora.getSeconds().toString().padStart(2, '0');
        timer.textContent = `${minutos}:${segundos}`;
    }
}

// Inicializar atualizações automáticas
setInterval(atualizarTimer, 1000);
setInterval(atualizarProgramacaoAtual, 300000); // A cada 5 minutos

// Função para scroll suave
function smoothScroll(target, duration = 500) {
    const targetElement = document.querySelector(target);
    if (!targetElement) return;
    
    const targetPosition = targetElement.offsetTop;
    const startPosition = window.pageYOffset;
    const distance = targetPosition - startPosition;
    let startTime = null;
    
    function animation(currentTime) {
        if (startTime === null) startTime = currentTime;
        const timeElapsed = currentTime - startTime;
        const run = ease(timeElapsed, startPosition, distance, duration);
        window.scrollTo(0, run);
        if (timeElapsed < duration) requestAnimationFrame(animation);
    }
    
    function ease(t, b, c, d) {
        t /= d / 2;
        if (t < 1) return c / 2 * t * t + b;
        t--;
        return -c / 2 * (t * (t - 2) - 1) + b;
    }
    
    requestAnimationFrame(animation);
}

// Adicionar scroll suave aos links internos
document.addEventListener('DOMContentLoaded', function() {
    const internalLinks = document.querySelectorAll('a[href^="#"]');
    
    internalLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const target = this.getAttribute('href');
            smoothScroll(target);
        });
    });
});

// Função para validar formulários
function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], textarea[required], select[required]');
    let isValid = true;
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            input.classList.add('error');
            isValid = false;
        } else {
            input.classList.remove('error');
        }
    });
    
    return isValid;
}

// Adicionar validação aos formulários
document.addEventListener('DOMContentLoaded', function() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                alert('Por favor, preencha todos os campos obrigatórios.');
            }
        });
    });
});

// Função para mostrar/ocultar menu mobile
function toggleMobileMenu() {
    const nav = document.querySelector('nav');
    const menuBtn = document.querySelector('.menu-btn');
    
    if (nav && menuBtn) {
        menuBtn.addEventListener('click', function() {
            nav.classList.toggle('mobile-open');
            this.classList.toggle('active');
        });
    }
}

// Inicializar menu mobile
document.addEventListener('DOMContentLoaded', toggleMobileMenu);

// Função para lazy loading de imagens
function initLazyLoading() {
    const images = document.querySelectorAll('img[data-src]');
    
    const imageObserver = new IntersectionObserver((entries, observer) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.remove('lazy');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
}

// Inicializar lazy loading
document.addEventListener('DOMContentLoaded', initLazyLoading);

// Função para debounce
function debounce(func, wait, immediate) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            timeout = null;
            if (!immediate) func(...args);
        };
        const callNow = immediate && !timeout;
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
        if (callNow) func(...args);
    };
}

// Função para throttle
function throttle(func, limit) {
    let inThrottle;
    return function() {
        const args = arguments;
        const context = this;
        if (!inThrottle) {
            func.apply(context, args);
            inThrottle = true;
            setTimeout(() => inThrottle = false, limit);
        }
    };
}

// Adicionar CSS para animações
const style = document.createElement('style');
style.textContent = `
    .animate-in {
        animation: fadeInUp 0.6s ease-out;
    }
    
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(30px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .error {
        border-color: #e53e3e !important;
    }
    
    nav.mobile-open {
        display: flex !important;
        flex-direction: column;
        position: absolute;
        top: 100%;
        left: 0;
        right: 0;
        background: white;
        box-shadow: 0 5px 15px rgba(0,0,0,0.1);
        z-index: 1000;
    }
    
    .lazy {
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .lazy.loaded {
        opacity: 1;
    }
`;
document.head.appendChild(style); 