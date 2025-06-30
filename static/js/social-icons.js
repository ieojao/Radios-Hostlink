// Função para detectar e renderizar ícones de redes sociais
function renderSocialIcons() {
    const socialItems = document.querySelectorAll('.social-item');
    
    socialItems.forEach(item => {
        const text = item.textContent.toLowerCase();
        let iconPath = '';
        let platform = '';
        
        // Detectar plataforma baseado no texto
        if (text.includes('facebook') || text.includes('fb.com') || text.includes('facebook.com')) {
            iconPath = '/static/images/social/facebook.svg';
            platform = 'Facebook';
        } else if (text.includes('instagram') || text.includes('ig') || text.includes('insta')) {
            iconPath = '/static/images/social/instagram.svg';
            platform = 'Instagram';
        } else if (text.includes('twitter') || text.includes('x.com') || text.includes('t.co')) {
            iconPath = '/static/images/social/twitter.svg';
            platform = 'Twitter/X';
        } else if (text.includes('youtube') || text.includes('yt') || text.includes('youtu.be')) {
            iconPath = '/static/images/social/youtube.svg';
            platform = 'YouTube';
        } else if (text.includes('whatsapp') || text.includes('wa.me') || text.includes('wa')) {
            iconPath = '/static/images/social/whatsapp.svg';
            platform = 'WhatsApp';
        } else if (text.includes('tiktok') || text.includes('tt')) {
            iconPath = '/static/images/social/tiktok.svg';
            platform = 'TikTok';
        }
        
        // Se encontrou uma plataforma, criar o ícone
        if (iconPath) {
            const icon = document.createElement('img');
            icon.src = iconPath;
            icon.alt = platform;
            icon.width = 20;
            icon.height = 20;
            icon.style.marginRight = '8px';
            icon.style.verticalAlign = 'middle';
            icon.style.filter = 'brightness(0) saturate(100%)';
            
            // Adicionar o ícone antes do texto
            item.insertBefore(icon, item.firstChild);
            
            // Adicionar classe para estilização
            item.classList.add('social-item-with-icon');
        }
    });
}

// Função para criar links clicáveis nas redes sociais
function makeSocialLinksClickable() {
    const socialItems = document.querySelectorAll('.social-item');
    
    socialItems.forEach(item => {
        const text = item.textContent;
        
        // Detectar URLs
        const urlRegex = /(https?:\/\/[^\s]+)/g;
        const urls = text.match(urlRegex);
        
        if (urls) {
            urls.forEach(url => {
                const link = document.createElement('a');
                link.href = url;
                link.target = '_blank';
                link.rel = 'noopener noreferrer';
                link.textContent = url;
                link.style.color = 'inherit';
                link.style.textDecoration = 'underline';
                
                // Substituir o texto pela URL clicável
                item.innerHTML = item.innerHTML.replace(url, link.outerHTML);
            });
        }
    });
}

// Função para estilizar as redes sociais dos locutores
function styleLocutorSocial() {
    const memberSocial = document.querySelectorAll('.member-social');
    
    memberSocial.forEach(container => {
        const socialItems = container.querySelectorAll('.social-item');
        
        socialItems.forEach(item => {
            // Adicionar estilos inline para melhor aparência
            item.style.display = 'inline-block';
            item.style.margin = '4px 8px 4px 0';
            item.style.padding = '6px 12px';
            item.style.backgroundColor = 'rgba(0,0,0,0.05)';
            item.style.borderRadius = '20px';
            item.style.fontSize = '0.9rem';
            item.style.transition = 'all 0.3s ease';
            
            // Efeito hover
            item.addEventListener('mouseenter', function() {
                this.style.backgroundColor = 'rgba(0,0,0,0.1)';
                this.style.transform = 'translateY(-2px)';
            });
            
            item.addEventListener('mouseleave', function() {
                this.style.backgroundColor = 'rgba(0,0,0,0.05)';
                this.style.transform = 'translateY(0)';
            });
        });
    });
}

// Função para criar cards de redes sociais dinâmicos
function createSocialCards(container, redes) {
    if (!redes || typeof redes !== 'object') return;
    
    const socialGrid = document.createElement('div');
    socialGrid.className = 'social-grid';
    
    const platforms = {
        facebook: { name: 'Facebook', icon: 'facebook.svg', color: '#1877f2' },
        instagram: { name: 'Instagram', icon: 'instagram.svg', color: '#e4405f' },
        twitter: { name: 'Twitter/X', icon: 'twitter.svg', color: '#1da1f2' },
        youtube: { name: 'YouTube', icon: 'youtube.svg', color: '#ff0000' },
        whatsapp: { name: 'WhatsApp', icon: 'whatsapp.svg', color: '#25d366' },
        tiktok: { name: 'TikTok', icon: 'tiktok.svg', color: '#ff0050' }
    };
    
    Object.entries(redes).forEach(([platform, url]) => {
        if (platforms[platform] && url) {
            const card = document.createElement('a');
            card.href = url;
            card.target = '_blank';
            card.className = `social-card ${platform}`;
            card.style.background = `linear-gradient(135deg, ${platforms[platform].color}, ${platforms[platform].color}dd)`;
            
            card.innerHTML = `
                <div class="social-icon">
                    <img src="/static/images/social/${platforms[platform].icon}" alt="${platforms[platform].name}" width="48" height="48">
                </div>
                <h3>${platforms[platform].name}</h3>
                <p>Siga-nos no ${platforms[platform].name}</p>
            `;
            
            socialGrid.appendChild(card);
        }
    });
    
    if (socialGrid.children.length > 0) {
        container.appendChild(socialGrid);
    }
}

// Inicializar quando o DOM estiver carregado
document.addEventListener('DOMContentLoaded', function() {
    renderSocialIcons();
    makeSocialLinksClickable();
    styleLocutorSocial();
});

// Exportar funções para uso global
window.SocialIcons = {
    render: renderSocialIcons,
    makeClickable: makeSocialLinksClickable,
    styleLocutor: styleLocutorSocial,
    createCards: createSocialCards
}; 