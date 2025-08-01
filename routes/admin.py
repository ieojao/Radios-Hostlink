from flask import Blueprint

# Criar blueprint para rotas administrativas
admin_bp = Blueprint('admin', __name__)

# Importar rotas específicas do admin
from routes.admin.auth import *
from routes.admin.dashboard import *
from routes.admin.programacao import *
from routes.admin.locutores import *
from routes.admin.banners import *
from routes.admin.destaques import *
from routes.admin.configuracoes import *
from routes.admin.usuarios import *
from routes.admin.paginas import *
from routes.admin.mensagens import * 