#!/usr/bin/env python3
"""
Script de inicialização da aplicação Radios Hostlink
"""

import os
import sys
import argparse
from app import app, db

def create_database():
    """Cria o banco de dados e tabelas"""
    try:
        with app.app_context():
            db.create_all()
            print("✅ Banco de dados criado com sucesso!")
            return True
    except Exception as e:
        print(f"❌ Erro ao criar banco de dados: {e}")
        return False

def check_dependencies():
    """Verifica se todas as dependências estão instaladas"""
    try:
        import flask
        import flask_sqlalchemy
        import flask_login
        import werkzeug
        print("✅ Todas as dependências estão instaladas!")
        return True
    except ImportError as e:
        print(f"❌ Dependência faltando: {e}")
        print("Execute: pip install -r requirements.txt")
        return False

def check_env_file():
    """Verifica se o arquivo .env existe"""
    if not os.path.exists('.env'):
        print("⚠️  Arquivo .env não encontrado!")
        print("Copie env_example.txt para .env e configure as variáveis")
        return False
    print("✅ Arquivo .env encontrado!")
    return True

def main():
    parser = argparse.ArgumentParser(description='Radios Hostlink - Rádio Web')
    parser.add_argument('--port', type=int, default=5000, help='Porta para executar (padrão: 5000)')
    parser.add_argument('--host', default='0.0.0.0', help='Host para executar (padrão: 0.0.0.0)')
    parser.add_argument('--debug', action='store_true', help='Executar em modo debug')
    parser.add_argument('--init-db', action='store_true', help='Inicializar banco de dados')
    parser.add_argument('--check', action='store_true', help='Verificar configuração')
    
    args = parser.parse_args()
    
    print("🎵 Radios Hostlink - Rádio Web")
    print("=" * 40)
    
    # Verificar dependências
    if not check_dependencies():
        sys.exit(1)
    
    # Verificar arquivo .env
    if not check_env_file():
        print("⚠️  Continuando sem arquivo .env (usando configurações padrão)")
    
    # Inicializar banco de dados se solicitado
    if args.init_db:
        if create_database():
            print("✅ Inicialização concluída!")
        else:
            print("❌ Erro na inicialização!")
            sys.exit(1)
    
    # Verificar configuração
    if args.check:
        print("\n📋 Verificação de Configuração:")
        print(f"  • Porta: {args.port}")
        print(f"  • Host: {args.host}")
        print(f"  • Debug: {args.debug}")
        print(f"  • Ambiente: {app.config['ENV']}")
        print(f"  • Banco: {app.config['SQLALCHEMY_DATABASE_URI']}")
        return
    
    # Criar banco de dados se não existir
    if not os.path.exists('radio.db'):
        print("📦 Criando banco de dados...")
        if not create_database():
            sys.exit(1)
    
    print(f"\n🚀 Iniciando servidor em http://{args.host}:{args.port}")
    print("📱 Painel admin: http://localhost:5000/admin")
    print("👤 Login: admin@radioshostlink.com.br / admin123")
    print("\nPressione Ctrl+C para parar")
    
    try:
        app.run(
            host=args.host,
            port=args.port,
            debug=args.debug
        )
    except KeyboardInterrupt:
        print("\n👋 Servidor parado!")
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main() 