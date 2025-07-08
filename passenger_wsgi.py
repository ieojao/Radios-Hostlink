import sys
import os

# Adicionar o diretório atual ao path
sys.path.insert(0, os.path.dirname(__file__))

# Configurar variáveis de ambiente se necessário
os.environ['FLASK_ENV'] = 'production'

# Importar a aplicação
from app import app as application

# Configurar para funcionar em subdiretório
if __name__ == '__main__':
    application.run()