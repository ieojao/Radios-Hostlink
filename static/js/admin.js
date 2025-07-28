// JavaScript para o painel administrativo
document.addEventListener('DOMContentLoaded', function() {
    initAdmin();
});

function initAdmin() {
    initMobileMenu();
    initSidebar();
    initAlerts();
    initForms();
    initCharts();
}

// Menu mobile para admin
function initMobileMenu() {
    const menuToggle = document.querySelector('.menu-toggle');
    const sidebar = document.querySelector('.sidebar');
    
    if (menuToggle && sidebar) {
        menuToggle.addEventListener('click', function() {
            sidebar.classList.toggle('open');
        });
        
        // Fechar sidebar ao clicar fora
        document.addEventListener('click', function(e) {
            if (!sidebar.contains(e.target) && !menuToggle.contains(e.target)) {
                sidebar.classList.remove('open');
            }
        });
    }
}

// Sidebar
function initSidebar() {
    const navItems = document.querySelectorAll('.nav-item');
    
    navItems.forEach(item => {
        item.addEventListener('click', function() {
            // Remover classe active de todos os itens
            navItems.forEach(nav => nav.classList.remove('active'));
            // Adicionar classe active no item clicado
            this.classList.add('active');
        });
    });
}

// Alertas
function initAlerts() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        // Auto-remover alertas após 5 segundos
        setTimeout(() => {
            alert.style.opacity = '0';
            setTimeout(() => {
                alert.remove();
            }, 300);
        }, 5000);
        
        // Botão para fechar alerta
        const closeBtn = alert.querySelector('.close-alert');
        if (closeBtn) {
            closeBtn.addEventListener('click', function() {
                alert.style.opacity = '0';
                setTimeout(() => {
                    alert.remove();
                }, 300);
            });
        }
    });
}

// Formulários
function initForms() {
    const forms = document.querySelectorAll('form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            if (!validateForm(this)) {
                e.preventDefault();
                showAlert('Por favor, preencha todos os campos obrigatórios.', 'error');
            }
        });
    });
}

// Validação de formulários
function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            field.classList.add('error');
            isValid = false;
        } else {
            field.classList.remove('error');
        }
    });
    
    return isValid;
}

// Mostrar alerta
function showAlert(message, type = 'info') {
    const alertDiv = document.createElement('div');
    alertDiv.className = `alert alert-${type}`;
    alertDiv.innerHTML = `
        ${message}
        <button class="close-alert" onclick="this.parentElement.remove()">&times;</button>
    `;
    
    const container = document.querySelector('.page-content') || document.body;
    container.insertBefore(alertDiv, container.firstChild);
    
    // Auto-remover após 5 segundos
    setTimeout(() => {
        alertDiv.style.opacity = '0';
        setTimeout(() => {
            alertDiv.remove();
        }, 300);
    }, 5000);
}

// Gráficos (se necessário)
function initCharts() {
    // Aqui você pode adicionar inicialização de gráficos
    // Por exemplo, usando Chart.js ou similar
    console.log('Charts initialized');
}

// Função para confirmar exclusão
function confirmDelete(message = 'Tem certeza que deseja excluir este item?') {
    return confirm(message);
}

// Função para fazer requisições AJAX
function ajaxRequest(url, method = 'GET', data = null) {
    return new Promise((resolve, reject) => {
        const xhr = new XMLHttpRequest();
        xhr.open(method, url);
        xhr.setRequestHeader('Content-Type', 'application/json');
        
        xhr.onload = function() {
            if (xhr.status >= 200 && xhr.status < 300) {
                try {
                    const response = JSON.parse(xhr.responseText);
                    resolve(response);
                } catch (e) {
                    resolve(xhr.responseText);
                }
            } else {
                reject(new Error('Request failed'));
            }
        };
        
        xhr.onerror = function() {
            reject(new Error('Network error'));
        };
        
        if (data) {
            xhr.send(JSON.stringify(data));
        } else {
            xhr.send();
        }
    });
}

// Função para upload de arquivos
function uploadFile(file, url) {
    return new Promise((resolve, reject) => {
        const formData = new FormData();
        formData.append('file', file);
        
        const xhr = new XMLHttpRequest();
        xhr.open('POST', url);
        
        xhr.onload = function() {
            if (xhr.status >= 200 && xhr.status < 300) {
                try {
                    const response = JSON.parse(xhr.responseText);
                    resolve(response);
                } catch (e) {
                    resolve(xhr.responseText);
                }
            } else {
                reject(new Error('Upload failed'));
            }
        };
        
        xhr.onerror = function() {
            reject(new Error('Network error'));
        };
        
        xhr.send(formData);
    });
}

// Função para preview de imagem
function previewImage(input, previewElement) {
    if (input.files && input.files[0]) {
        const reader = new FileReader();
        
        reader.onload = function(e) {
            previewElement.src = e.target.result;
            previewElement.style.display = 'block';
        };
        
        reader.readAsDataURL(input.files[0]);
    }
}

// Função para formatar data
function formatDate(date) {
    return new Date(date).toLocaleDateString('pt-BR');
}

// Função para formatar hora
function formatTime(time) {
    return new Date(`2000-01-01T${time}`).toLocaleTimeString('pt-BR', {
        hour: '2-digit',
        minute: '2-digit'
    });
}

// Função para debounce
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

// Função para copiar para clipboard
function copyToClipboard(text) {
    if (navigator.clipboard) {
        navigator.clipboard.writeText(text).then(() => {
            showAlert('Copiado para a área de transferência!', 'success');
        }).catch(() => {
            fallbackCopyToClipboard(text);
        });
    } else {
        fallbackCopyToClipboard(text);
    }
}

function fallbackCopyToClipboard(text) {
    const textArea = document.createElement('textarea');
    textArea.value = text;
    document.body.appendChild(textArea);
    textArea.select();
    try {
        document.execCommand('copy');
        showAlert('Copiado para a área de transferência!', 'success');
    } catch (err) {
        showAlert('Erro ao copiar texto', 'error');
    }
    document.body.removeChild(textArea);
}

// Função para exportar dados
function exportData(data, filename, type = 'json') {
    let content, mimeType;
    
    if (type === 'json') {
        content = JSON.stringify(data, null, 2);
        mimeType = 'application/json';
    } else if (type === 'csv') {
        content = convertToCSV(data);
        mimeType = 'text/csv';
    }
    
    const blob = new Blob([content], { type: mimeType });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

function convertToCSV(data) {
    if (!data || !data.length) return '';
    
    const headers = Object.keys(data[0]);
    const csvContent = [
        headers.join(','),
        ...data.map(row => headers.map(header => `"${row[header]}"`).join(','))
    ].join('\n');
    
    return csvContent;
}

// Função para importar dados
function importData(input, callback) {
    const file = input.files[0];
    if (!file) return;
    
    const reader = new FileReader();
    reader.onload = function(e) {
        try {
            const data = JSON.parse(e.target.result);
            callback(data);
        } catch (error) {
            showAlert('Erro ao importar arquivo', 'error');
        }
    };
    reader.readAsText(file);
}

// Função para buscar dados
function searchData(searchTerm, data, fields) {
    if (!searchTerm) return data;
    
    return data.filter(item => {
        return fields.some(field => {
            const value = item[field];
            if (typeof value === 'string') {
                return value.toLowerCase().includes(searchTerm.toLowerCase());
            }
            return false;
        });
    });
}

// Função para ordenar dados
function sortData(data, field, direction = 'asc') {
    return data.sort((a, b) => {
        let aVal = a[field];
        let bVal = b[field];
        
        if (typeof aVal === 'string') {
            aVal = aVal.toLowerCase();
            bVal = bVal.toLowerCase();
        }
        
        if (direction === 'asc') {
            return aVal > bVal ? 1 : -1;
        } else {
            return aVal < bVal ? 1 : -1;
        }
    });
}

// Função para paginação
function paginateData(data, page, perPage) {
    const start = (page - 1) * perPage;
    const end = start + perPage;
    return data.slice(start, end);
}

// Adicionar CSS para funcionalidades do admin
const adminStyle = document.createElement('style');
adminStyle.textContent = `
    .alert {
        transition: opacity 0.3s ease;
    }
    
    .error {
        border-color: #e53e3e !important;
        box-shadow: 0 0 0 1px #e53e3e;
    }
    
    .close-alert {
        background: none;
        border: none;
        font-size: 1.2rem;
        cursor: pointer;
        float: right;
        margin-left: 10px;
    }
    
    .loading {
        opacity: 0.6;
        pointer-events: none;
    }
    
    .spinner {
        display: inline-block;
        width: 20px;
        height: 20px;
        border: 3px solid #f3f3f3;
        border-top: 3px solid #f093fb;
        border-radius: 50%;
        animation: spin 1s linear infinite;
    }
    
    @keyframes spin {
        0% { transform: rotate(0deg); }
        100% { transform: rotate(360deg); }
    }
    
    .tooltip {
        position: relative;
        display: inline-block;
    }
    
    .tooltip .tooltiptext {
        visibility: hidden;
        width: 120px;
        background-color: #333;
        color: #fff;
        text-align: center;
        border-radius: 6px;
        padding: 5px;
        position: absolute;
        z-index: 1;
        bottom: 125%;
        left: 50%;
        margin-left: -60px;
        opacity: 0;
        transition: opacity 0.3s;
    }
    
    .tooltip:hover .tooltiptext {
        visibility: visible;
        opacity: 1;
    }
`;
document.head.appendChild(adminStyle);

// Função para validar URL de imagem
function validarImagem(url) {
    return new Promise((resolve) => {
        if (!url) {
            resolve(false);
            return;
        }
        
        const img = new Image();
        img.onload = () => resolve(true);
        img.onerror = () => resolve(false);
        img.src = url;
    });
}

// Função para testar URL de imagem e mostrar feedback
async function testarImagem(input) {
    const url = input.value.trim();
    const feedback = input.parentNode.querySelector('.imagem-feedback');
    
    if (!url) {
        if (feedback) feedback.remove();
        return;
    }
    
    // Criar ou atualizar feedback
    let feedbackElement = feedback;
    if (!feedbackElement) {
        feedbackElement = document.createElement('div');
        feedbackElement.className = 'imagem-feedback';
        feedbackElement.style.marginTop = '5px';
        feedbackElement.style.fontSize = '0.9rem';
        input.parentNode.appendChild(feedbackElement);
    }
    
    feedbackElement.innerHTML = '🔄 Testando imagem...';
    feedbackElement.style.color = '#666';
    
    const isValid = await validarImagem(url);
    
    if (isValid) {
        feedbackElement.innerHTML = '✅ Imagem válida';
        feedbackElement.style.color = '#667eea';
    } else {
        feedbackElement.innerHTML = '❌ Imagem não encontrada ou inválida';
        feedbackElement.style.color = '#ef4444';
    }
} 