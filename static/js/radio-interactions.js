// Interações e Animações Avançadas para a Página A Rádio

document.addEventListener('DOMContentLoaded', function() {
    
    // ===== ANIMAÇÕES DE SCROLL =====
    
    // Intersection Observer para animações de entrada
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };
    
    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('animate-in');
                
                // Animação específica para estatísticas
                if (entry.target.classList.contains('stat-item')) {
                    animateStatNumber(entry.target);
                }
            }
        });
    }, observerOptions);
    
    // Observar elementos para animação
    const animateElements = document.querySelectorAll('.stat-item, .mvv-card, .tech-item, .feature');
    animateElements.forEach(el => observer.observe(el));
    
    // ===== ANIMAÇÃO DE NÚMEROS DAS ESTATÍSTICAS =====
    
    function animateStatNumber(statItem) {
        const numberElement = statItem.querySelector('.stat-number');
        const target = parseInt(numberElement.getAttribute('data-target'));
        
        if (!target || numberElement.classList.contains('animated')) return;
        
        numberElement.classList.add('animated');
        
        let current = 0;
        const increment = target / 50;
        const duration = 2000; // 2 segundos
        const stepTime = duration / 50;
        
        const timer = setInterval(() => {
            current += increment;
            if (current >= target) {
                current = target;
                clearInterval(timer);
            }
            numberElement.textContent = Math.floor(current);
        }, stepTime);
    }
    
    // ===== SMOOTH SCROLL PARA LINKS INTERNOS =====
    
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                const headerHeight = document.querySelector('header').offsetHeight;
                const targetPosition = targetElement.offsetTop - headerHeight - 20;
                
                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
    
    // ===== EFEITO PARALLAX NO HERO =====
    
    const heroSection = document.querySelector('.hero-section');
    if (heroSection) {
        let ticking = false;
        
        function updateParallax() {
            const scrolled = window.pageYOffset;
            const rate = scrolled * -0.5;
            heroSection.style.transform = `translateY(${rate}px)`;
            ticking = false;
        }
        
        function requestTick() {
            if (!ticking) {
                requestAnimationFrame(updateParallax);
                ticking = true;
            }
        }
        
        window.addEventListener('scroll', requestTick);
    }
    
    // ===== ANIMAÇÕES DE HOVER AVANÇADAS =====
    
    // Efeito de partículas no hover
    document.querySelectorAll('.mvv-card, .tech-item').forEach(card => {
        card.addEventListener('mouseenter', function() {
            createParticles(this);
        });
    });
    
    function createParticles(element) {
        const rect = element.getBoundingClientRect();
        const particleCount = 5;
        
        for (let i = 0; i < particleCount; i++) {
            const particle = document.createElement('div');
            particle.className = 'particle';
            particle.style.left = Math.random() * rect.width + 'px';
            particle.style.top = Math.random() * rect.height + 'px';
            
            element.appendChild(particle);
            
            // Remover partícula após animação
            setTimeout(() => {
                if (particle.parentNode) {
                    particle.parentNode.removeChild(particle);
                }
            }, 6000);
        }
    }
    
    // ===== ANIMAÇÕES DE TEXTO =====
    
    // Efeito typewriter para títulos
    function typewriterEffect(element, text, speed = 100) {
        element.textContent = '';
        let i = 0;
        
        function type() {
            if (i < text.length) {
                element.textContent += text.charAt(i);
                i++;
                setTimeout(type, speed);
            }
        }
        
        type();
    }
    
    // Aplicar typewriter em elementos específicos
    const typewriterElements = document.querySelectorAll('.hero-title, .section-header h2');
    typewriterElements.forEach(element => {
        const text = element.textContent;
        if (text && !element.classList.contains('typewriter-applied')) {
            element.classList.add('typewriter-applied');
            // typewriterEffect(element, text, 80);
        }
    });
    
    // ===== ANIMAÇÕES DE BOTÕES =====
    
    // Efeito de ripple nos botões
    document.querySelectorAll('.btn').forEach(button => {
        button.addEventListener('click', function(e) {
            const ripple = document.createElement('span');
            const rect = this.getBoundingClientRect();
            const size = Math.max(rect.width, rect.height);
            const x = e.clientX - rect.left - size / 2;
            const y = e.clientY - rect.top - size / 2;
            
            ripple.style.width = ripple.style.height = size + 'px';
            ripple.style.left = x + 'px';
            ripple.style.top = y + 'px';
            ripple.classList.add('ripple');
            
            this.appendChild(ripple);
            
            setTimeout(() => {
                ripple.remove();
            }, 600);
        });
    });
    
    // ===== ANIMAÇÕES DE CARDS =====
    
    // Efeito de elevação nos cards
    document.querySelectorAll('.mvv-card, .tech-item, .stat-item').forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-15px) scale(1.02)';
            this.style.boxShadow = '0 25px 50px rgba(0, 0, 0, 0.4)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
            this.style.boxShadow = '';
        });
    });
    
    // ===== ANIMAÇÕES DE IMAGENS =====
    
    // Lazy loading com fade in
    const images = document.querySelectorAll('img[data-src]');
    const imageObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                const img = entry.target;
                img.src = img.dataset.src;
                img.classList.add('fade-in');
                imageObserver.unobserve(img);
            }
        });
    });
    
    images.forEach(img => imageObserver.observe(img));
    
    // ===== ANIMAÇÕES DE SCROLL SUAVE =====
    
    // Scroll suave para o topo
    const scrollToTopBtn = document.createElement('button');
    scrollToTopBtn.innerHTML = '↑';
    scrollToTopBtn.className = 'scroll-to-top';
    scrollToTopBtn.style.cssText = `
        position: fixed;
        bottom: 30px;
        right: 30px;
        width: 50px;
        height: 50px;
        border-radius: 50%;
        background: var(--gradient-primary);
        border: none;
        color: white;
        font-size: 20px;
        cursor: pointer;
        opacity: 0;
        visibility: hidden;
        transition: all 0.3s ease;
        z-index: 1000;
        box-shadow: 0 4px 20px rgba(16, 185, 129, 0.3);
    `;
    
    document.body.appendChild(scrollToTopBtn);
    
    // Mostrar/ocultar botão de scroll to top
    window.addEventListener('scroll', () => {
        if (window.pageYOffset > 300) {
            scrollToTopBtn.style.opacity = '1';
            scrollToTopBtn.style.visibility = 'visible';
        } else {
            scrollToTopBtn.style.opacity = '0';
            scrollToTopBtn.style.visibility = 'hidden';
        }
    });
    
    scrollToTopBtn.addEventListener('click', () => {
        window.scrollTo({
            top: 0,
            behavior: 'smooth'
        });
    });
    
    // ===== ANIMAÇÕES DE CONTADOR =====
    
    // Contador animado para estatísticas
    function animateCounter(element, target, duration = 2000) {
        let start = 0;
        const increment = target / (duration / 16);
        
        function updateCounter() {
            start += increment;
            if (start < target) {
                element.textContent = Math.floor(start);
                requestAnimationFrame(updateCounter);
            } else {
                element.textContent = target;
            }
        }
        
        updateCounter();
    }
    
    // ===== ANIMAÇÕES DE MENU =====
    
    // Highlight do menu ativo
    const menuItems = document.querySelectorAll('nav a');
    const sections = document.querySelectorAll('section[id]');
    
    window.addEventListener('scroll', () => {
        let current = '';
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            const sectionHeight = section.clientHeight;
            if (window.pageYOffset >= sectionTop - 200) {
                current = section.getAttribute('id');
            }
        });
        
        menuItems.forEach(item => {
            item.classList.remove('active');
            if (item.getAttribute('href') === `#${current}`) {
                item.classList.add('active');
            }
        });
    });
    
    // ===== ANIMAÇÕES DE PERFORMANCE =====
    
    // Debounce para otimizar performance
    function debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }
    
    // Aplicar debounce nas animações de scroll
    const debouncedScrollHandler = debounce(() => {
        // Animações que dependem do scroll
    }, 16);
    
    window.addEventListener('scroll', debouncedScrollHandler);
    
    // ===== ANIMAÇÕES DE CARREGAMENTO =====
    
    // Loading spinner para elementos que carregam dinamicamente
    function showLoading(element) {
        const spinner = document.createElement('div');
        spinner.className = 'loading-spinner';
        element.appendChild(spinner);
    }
    
    function hideLoading(element) {
        const spinner = element.querySelector('.loading-spinner');
        if (spinner) {
            spinner.remove();
        }
    }
    
    // ===== ANIMAÇÕES DE NOTIFICAÇÃO =====
    
    // Sistema de notificações
    function showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.textContent = message;
        notification.style.cssText = `
            position: fixed;
            top: 20px;
            right: 20px;
            padding: 15px 25px;
            border-radius: 8px;
            color: white;
            font-weight: 600;
            z-index: 10000;
            transform: translateX(100%);
            transition: transform 0.3s ease;
            background: ${type === 'success' ? 'var(--primary-green)' : type === 'error' ? '#ef4444' : 'var(--accent-green)'};
        `;
        
        document.body.appendChild(notification);
        
        // Animar entrada
        setTimeout(() => {
            notification.style.transform = 'translateX(0)';
        }, 100);
        
        // Remover após 3 segundos
        setTimeout(() => {
            notification.style.transform = 'translateX(100%)';
            setTimeout(() => {
                if (notification.parentNode) {
                    notification.parentNode.removeChild(notification);
                }
            }, 300);
        }, 3000);
    }
    
    // ===== INICIALIZAÇÃO =====
    
    // Inicializar todas as animações
    function initAnimations() {
        // Adicionar classes de animação aos elementos
        document.querySelectorAll('.mvv-grid').forEach(grid => {
            grid.classList.add('stagger-animate');
        });
        
        document.querySelectorAll('.tech-grid').forEach(grid => {
            grid.classList.add('stagger-animate');
        });
        
        // Trigger inicial para elementos visíveis
        const visibleElements = document.querySelectorAll('.animate-in');
        visibleElements.forEach(el => {
            if (el.classList.contains('stat-item')) {
                animateStatNumber(el);
            }
        });
    }
    
    // Executar inicialização após um pequeno delay
    setTimeout(initAnimations, 100);
    
    // ===== EVENT LISTENERS GLOBAIS =====
    
    // Prevenir comportamento padrão de links vazios
    document.addEventListener('click', (e) => {
        if (e.target.tagName === 'A' && e.target.getAttribute('href') === '#') {
            e.preventDefault();
        }
    });
    
    // Melhorar acessibilidade
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape') {
            // Fechar modais ou notificações
            const notifications = document.querySelectorAll('.notification');
            notifications.forEach(notification => {
                notification.style.transform = 'translateX(100%)';
                setTimeout(() => {
                    if (notification.parentNode) {
                        notification.parentNode.removeChild(notification);
                    }
                }, 300);
            });
        }
    });
    
    console.log('🎵 Interações da página A Rádio carregadas com sucesso!');
}); 