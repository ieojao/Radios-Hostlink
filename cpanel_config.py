#!/usr/bin/env python3
"""
Configurações específicas para o cPanel
"""

import os
import sys

# Configurações do ambiente cPanel
CPANEL_CONFIG = {
    'DEBUG': False,
    'TESTING': False,
    'SECRET_KEY': 'sua-chave-secreta-muito-segura-aqui-2024',
    'DATABASE_URL': 'sqlite:///radio.db',
    'UPLOAD_FOLDER': 'static/uploads',
    'MAX_CONTENT_LENGTH': 16 * 1024 * 1024,  # 16MB
}

# Configurações específicas para subdiretório /site
if os.environ.get('SCRIPT_NAME', '').startswith('/site'):
    CPANEL_CONFIG['APPLICATION_ROOT'] = '/site'
    CPANEL_CONFIG['STATIC_URL_PATH'] = '/site/static'
else:
    CPANEL_CONFIG['APPLICATION_ROOT'] = ''
    CPANEL_CONFIG['STATIC_URL_PATH'] = '/static'

# Função para aplicar configurações
def apply_cpanel_config(app):
    """Aplica as configurações do cPanel na aplicação Flask"""
    for key, value in CPANEL_CONFIG.items():
        app.config[key] = value
    
    # Configurar caminhos para subdiretório
    if CPANEL_CONFIG['APPLICATION_ROOT']:
        app.config['APPLICATION_ROOT'] = CPANEL_CONFIG['APPLICATION_ROOT']
        app.config['STATIC_URL_PATH'] = CPANEL_CONFIG['STATIC_URL_PATH']
    
    return app 