import os
from flask import Flask
from config import config
from models.database import init_app as init_db
from utils.filters import filters_bp
from routes.public import public_bp
from routes.api import api_bp

# Importar modelos para garantir que sejam registrados
from models.user import Usuario
from models.content import Programacao, Locutor, Banner, Destaque, Configuracao
from models.pages import PaginaRadio, PaginaEquipe, PaginaContato, MensagemContato

def create_app(config_name=None):
    """Factory para criar a aplicação Flask"""
    
    # Determinar configuração
    if config_name is None:
        config_name = os.getenv('FLASK_ENV', 'development')
    
    # Criar aplicação
    app = Flask(__name__)
    
    # Carregar configuração
    app.config.from_object(config[config_name])
    
    # Inicializar extensões
    init_db(app)
    
    # Registrar blueprints
    app.register_blueprint(filters_bp)
    app.register_blueprint(public_bp)
    app.register_blueprint(api_bp)
    
    # Registrar blueprints do admin (serão criados separadamente)
    from routes.admin import admin_bp
    app.register_blueprint(admin_bp, url_prefix='/admin')
    
    # Configurar logging
    if not app.debug and not app.testing:
        import logging
        from logging.handlers import RotatingFileHandler
        
        # Criar pasta de logs se não existir
        if not os.path.exists('logs'):
            os.mkdir('logs')
        
        # Configurar handler de arquivo
        file_handler = RotatingFileHandler(
            app.config['LOG_FILE'], 
            maxBytes=10240000, 
            backupCount=10
        )
        file_handler.setFormatter(logging.Formatter(
            '%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]'
        ))
        file_handler.setLevel(logging.INFO)
        app.logger.addHandler(file_handler)
        
        app.logger.setLevel(logging.INFO)
        app.logger.info('Radios Hostlink startup')
    
    # Criar pasta de uploads se não existir
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    
    return app 