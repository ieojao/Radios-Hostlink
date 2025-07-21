/* ========================================
   MENU MÓVEL - HAMBÚRGUER
   ======================================== */

document.addEventListener('DOMContentLoaded', function() {
    const header = document.querySelector('header');
    const nav = document.querySelector('nav');
    const headerButtons = document.querySelector('.header-buttons');
    
    // Criar botão hambúrguer
    function createMobileMenu() {
        // Verificar se já existe
        if (document.querySelector('.mobile-menu-toggle')) {
            return;
        }
        
        const mobileToggle = document.createElement('button');
        mobileToggle.className = 'mobile-menu-toggle';
        mobileToggle.innerHTML = `
            <span class="hamburger-line"></span>
            <span class="hamburger-line"></span>
            <span class="hamburger-line"></span>
        `;
        mobileToggle.setAttribute('aria-label', 'Abrir menu de navegação');
        
        // Adicionar antes da navegação
        header.insertBefore(mobileToggle, nav);
        
        // Event listener para toggle
        mobileToggle.addEventListener('click', function() {
            nav.classList.toggle('mobile-open');
            mobileToggle.classList.toggle('active');
            
            // Atualizar aria-label
            const isOpen = nav.classList.contains('mobile-open');
            mobileToggle.setAttribute('aria-label', 
                isOpen ? 'Fechar menu de navegação' : 'Abrir menu de navegação'
            );
        });
        
        // Fechar menu ao clicar em um link
        const navLinks = nav.querySelectorAll('a');
        navLinks.forEach(link => {
            link.addEventListener('click', function() {
                nav.classList.remove('mobile-open');
                mobileToggle.classList.remove('active');
                mobileToggle.setAttribute('aria-label', 'Abrir menu de navegação');
            });
        });
        
        // Fechar menu ao clicar fora
        document.addEventListener('click', function(e) {
            if (!header.contains(e.target) && nav.classList.contains('mobile-open')) {
                nav.classList.remove('mobile-open');
                mobileToggle.classList.remove('active');
                mobileToggle.setAttribute('aria-label', 'Abrir menu de navegação');
            }
        });
    }
    
    // Verificar se deve mostrar menu móvel
    function checkMobileMenu() {
        if (window.innerWidth <= 768) {
            createMobileMenu();
        } else {
            // Remover menu móvel em desktop
            const mobileToggle = document.querySelector('.mobile-menu-toggle');
            if (mobileToggle) {
                mobileToggle.remove();
            }
            nav.classList.remove('mobile-open');
        }
    }
    
    // Verificar na carga inicial
    checkMobileMenu();
    
    // Verificar no resize
    window.addEventListener('resize', checkMobileMenu);
    
    // Adicionar estilos CSS dinamicamente
    const mobileStyles = `
        <style>
            @media (max-width: 768px) {
                .mobile-menu-toggle {
                    display: flex;
                    flex-direction: column;
                    justify-content: space-around;
                    width: 30px;
                    height: 30px;
                    background: transparent;
                    border: none;
                    cursor: pointer;
                    padding: 0;
                    z-index: 10;
                    order: 2;
                }
                
                .hamburger-line {
                    width: 100%;
                    height: 3px;
                    background: var(--cor-principal, #1e3a8a);
                    border-radius: 2px;
                    transition: all 0.3s ease;
                    transform-origin: center;
                }
                
                .mobile-menu-toggle.active .hamburger-line:nth-child(1) {
                    transform: rotate(45deg) translate(6px, 6px);
                }
                
                .mobile-menu-toggle.active .hamburger-line:nth-child(2) {
                    opacity: 0;
                }
                
                .mobile-menu-toggle.active .hamburger-line:nth-child(3) {
                    transform: rotate(-45deg) translate(6px, -6px);
                }
                
                nav {
                    position: fixed;
                    top: 0;
                    left: -100%;
                    width: 100%;
                    height: 100vh;
                    background: rgba(30, 58, 138, 0.95);
                    backdrop-filter: blur(10px);
                    display: flex;
                    flex-direction: column;
                    justify-content: center;
                    align-items: center;
                    transition: left 0.3s ease;
                    z-index: 1000;
                    gap: 30px;
                }
                
                nav.mobile-open {
                    left: 0;
                }
                
                nav a {
                    font-size: 1.5rem;
                    padding: 15px 25px;
                    border-radius: 25px;
                    background: rgba(255, 255, 255, 0.1);
                    color: white;
                    text-decoration: none;
                    transition: all 0.3s ease;
                    border: 2px solid transparent;
                }
                
                nav a:hover,
                nav a.active {
                    background: var(--cor-botoes, #3b82f6);
                    border-color: white;
                    transform: scale(1.05);
                }
                
                .header-buttons {
                    order: 3;
                }
                
                /* Overlay para fundo escuro */
                nav::before {
                    content: '';
                    position: absolute;
                    top: 0;
                    left: 0;
                    width: 100%;
                    height: 100%;
                    background: rgba(0, 0, 0, 0.3);
                    z-index: -1;
                }
            }
            
            @media (max-width: 480px) {
                .mobile-menu-toggle {
                    width: 25px;
                    height: 25px;
                }
                
                .hamburger-line {
                    height: 2px;
                }
                
                nav a {
                    font-size: 1.3rem;
                    padding: 12px 20px;
                }
            }
        </style>
    `;
    
    // Adicionar estilos ao head
    if (!document.querySelector('#mobile-menu-styles')) {
        const styleElement = document.createElement('div');
        styleElement.id = 'mobile-menu-styles';
        styleElement.innerHTML = mobileStyles;
        document.head.appendChild(styleElement);
    }
});

/* ========================================
   MELHORIAS DE TOUCH PARA MÓVEL
   ======================================== */

// Melhorar feedback de toque
document.addEventListener('DOMContentLoaded', function() {
    // Adicionar feedback visual para toques
    const touchElements = document.querySelectorAll('button, a, .tab, .card, .programa-item');
    
    touchElements.forEach(element => {
        element.addEventListener('touchstart', function() {
            this.style.transform = 'scale(0.95)';
            this.style.transition = 'transform 0.1s ease';
        });
        
        element.addEventListener('touchend', function() {
            this.style.transform = '';
            this.style.transition = '';
        });
    });
    
    // Prevenir zoom em inputs no iOS
    const inputs = document.querySelectorAll('input, textarea, select');
    inputs.forEach(input => {
        input.addEventListener('focus', function() {
            if (window.innerWidth <= 768) {
                this.style.fontSize = '16px';
            }
        });
    });
    
    // Melhorar scroll suave
    const smoothScrollLinks = document.querySelectorAll('a[href^="#"]');
    smoothScrollLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);
            
            if (targetElement) {
                targetElement.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
});

/* ========================================
   OTIMIZAÇÕES DE PERFORMANCE MÓVEL
   ======================================== */

// Debounce para eventos de resize
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

// Otimizar scroll para performance
let ticking = false;
function updateOnScroll() {
    if (!ticking) {
        requestAnimationFrame(function() {
            // Aqui você pode adicionar animações baseadas no scroll
            ticking = false;
        });
        ticking = true;
    }
}

// Adicionar listener de scroll otimizado
window.addEventListener('scroll', updateOnScroll, { passive: true });

// Otimizar resize
const optimizedResize = debounce(function() {
    // Recalcular layouts se necessário
}, 250);

window.addEventListener('resize', optimizedResize);

/* ========================================
   MELHORIAS DE ACESSIBILIDADE MÓVEL
   ======================================== */

document.addEventListener('DOMContentLoaded', function() {
    // Melhorar navegação por teclado
    const focusableElements = document.querySelectorAll(
        'a, button, input, textarea, select, [tabindex]:not([tabindex="-1"])'
    );
    
    focusableElements.forEach(element => {
        element.addEventListener('keydown', function(e) {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                this.click();
            }
        });
    });
    
    // Adicionar skip links para acessibilidade
    if (!document.querySelector('.skip-link')) {
        const skipLink = document.createElement('a');
        skipLink.href = '#main-content';
        skipLink.className = 'skip-link';
        skipLink.textContent = 'Pular para o conteúdo principal';
        document.body.insertBefore(skipLink, document.body.firstChild);
        
        // Adicionar ID ao main
        const main = document.querySelector('main');
        if (main && !main.id) {
            main.id = 'main-content';
        }
    }
    
    // Adicionar estilos para skip link
    const skipLinkStyles = `
        <style>
            .skip-link {
                position: absolute;
                top: -40px;
                left: 6px;
                background: var(--cor-principal, #1e3a8a);
                color: white;
                padding: 8px;
                text-decoration: none;
                border-radius: 4px;
                z-index: 10000;
                transition: top 0.3s ease;
            }
            
            .skip-link:focus {
                top: 6px;
            }
        </style>
    `;
    
    if (!document.querySelector('#skip-link-styles')) {
        const styleElement = document.createElement('div');
        styleElement.id = 'skip-link-styles';
        styleElement.innerHTML = skipLinkStyles;
        document.head.appendChild(styleElement);
    }
}); 