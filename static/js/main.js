// Funções principais do site
document.addEventListener('DOMContentLoaded', function() {
    // Inicializar funcionalidades
    initNavigation();
    initTabs();
    initWhatsApp();
    initAnimations();
});

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

// Validação de formulários
function validateForm(form) {
    const inputs = form.querySelectorAll('input[required], textarea[required]');
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



// Lazy loading para imagens
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

// Função debounce para otimização
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

// Função throttle para otimização
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
    

    
    .lazy {
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .lazy.loaded {
        opacity: 1;
    }
`;
document.head.appendChild(style); 