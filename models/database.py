from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

# Instâncias das extensões
db = SQLAlchemy()
login_manager = LoginManager()

def init_app(app):
    """Inicializa as extensões do banco de dados"""
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'admin.login'
    
    # Configurar loader de usuário
    from models.user import Usuario
    
    @login_manager.user_loader
    def load_user(user_id):
        return Usuario.query.get(int(user_id)) 