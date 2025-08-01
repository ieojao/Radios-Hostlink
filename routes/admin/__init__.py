from flask import Blueprint

admin_bp = Blueprint('admin', __name__)

# Importar módulos de rota para registrar as rotas
from . import auth
from . import dashboard
from . import programacao
from . import locutores
from . import banners
from . import destaques
from . import paginas
from . import mensagens
from . import configuracoes
from . import usuarios 