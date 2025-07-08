#!/usr/bin/env python3
"""
Script para reiniciar o banco de dados no cPanel
Use este script quando houver problemas com o banco de dados
"""

import os
import sys
import shutil
from datetime import datetime

def backup_database():
    """Faz backup do banco de dados atual"""
    db_file = 'radio.db'
    if os.path.exists(db_file):
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_file = f'radio_backup_{timestamp}.db'
        try:
            shutil.copy2(db_file, backup_file)
            print(f"✅ Backup criado: {backup_file}")
            return backup_file
        except Exception as e:
            print(f"❌ Erro ao criar backup: {e}")
            return None
    else:
        print("ℹ️  Nenhum banco de dados encontrado para backup")
        return None

def delete_database():
    """Remove o banco de dados atual"""
    db_file = 'radio.db'
    if os.path.exists(db_file):
        try:
            os.remove(db_file)
            print("✅ Banco de dados removido")
            return True
        except Exception as e:
            print(f"❌ Erro ao remover banco: {e}")
            return False
    else:
        print("ℹ️  Banco de dados não encontrado")
        return True

def create_database():
    """Cria um novo banco de dados"""
    try:
        # Importar a aplicação Flask
        sys.path.insert(0, os.path.dirname(__file__))
        from app import app, db
        
        with app.app_context():
            # Criar todas as tabelas
            db.create_all()
            
            # Criar usuário admin padrão
            from app import Usuario
            from werkzeug.security import generate_password_hash
            
            # Verificar se já existe um usuário admin
            admin = Usuario.query.filter_by(email='admin@radioshostlink.com.br').first()
            if not admin:
                admin = Usuario(
                    nome='Administrador',
                    email='admin@radioshostlink.com.br',
                    senha=generate_password_hash('admin123'),
                    nivel='admin'
                )
                db.session.add(admin)
                db.session.commit()
                print("✅ Usuário admin criado")
            else:
                print("ℹ️  Usuário admin já existe")
            
            print("✅ Banco de dados criado com sucesso!")
            return True
            
    except Exception as e:
        print(f"❌ Erro ao criar banco de dados: {e}")
        return False

def reset_database():
    """Função principal para reiniciar o banco de dados"""
    print("🔄 Reiniciando Banco de Dados")
    print("=" * 40)
    
    # 1. Fazer backup
    print("\n1. Criando backup...")
    backup_file = backup_database()
    
    # 2. Remover banco atual
    print("\n2. Removendo banco atual...")
    if not delete_database():
        print("❌ Não foi possível remover o banco atual")
        return False
    
    # 3. Criar novo banco
    print("\n3. Criando novo banco...")
    if not create_database():
        print("❌ Erro ao criar novo banco")
        
        # Tentar restaurar backup se houver
        if backup_file and os.path.exists(backup_file):
            print("🔄 Tentando restaurar backup...")
            try:
                shutil.copy2(backup_file, 'radio.db')
                print("✅ Backup restaurado")
            except Exception as e:
                print(f"❌ Erro ao restaurar backup: {e}")
        
        return False
    
    print("\n✅ Banco de dados reiniciado com sucesso!")
    print(f"📧 Login: admin@radioshostlink.com.br")
    print(f"🔑 Senha: admin123")
    
    if backup_file:
        print(f"\n💾 Backup salvo como: {backup_file}")
        print("⚠️  Você pode deletar o backup se não precisar mais")
    
    return True

def show_database_info():
    """Mostra informações sobre o banco de dados"""
    db_file = 'radio.db'
    if os.path.exists(db_file):
        size = os.path.getsize(db_file)
        modified = datetime.fromtimestamp(os.path.getmtime(db_file))
        print(f"📊 Banco de dados encontrado:")
        print(f"   📁 Arquivo: {db_file}")
        print(f"   📏 Tamanho: {size:,} bytes")
        print(f"   📅 Modificado: {modified.strftime('%d/%m/%Y %H:%M:%S')}")
    else:
        print("❌ Banco de dados não encontrado")

def main():
    """Função principal"""
    if len(sys.argv) > 1:
        command = sys.argv[1].lower()
        
        if command == 'info':
            show_database_info()
        elif command == 'backup':
            backup_database()
        elif command == 'delete':
            delete_database()
        elif command == 'create':
            create_database()
        elif command == 'reset':
            reset_database()
        else:
            print("❌ Comando inválido")
            print_help()
    else:
        print_help()

def print_help():
    """Mostra ajuda sobre os comandos disponíveis"""
    print("🔄 Script de Gerenciamento do Banco de Dados")
    print("=" * 50)
    print("\nComandos disponíveis:")
    print("  python reset_database.py info    - Mostra informações do banco")
    print("  python reset_database.py backup  - Faz backup do banco atual")
    print("  python reset_database.py delete  - Remove o banco atual")
    print("  python reset_database.py create  - Cria novo banco")
    print("  python reset_database.py reset   - Reinicia o banco (backup + delete + create)")
    print("\nExemplo de uso:")
    print("  python reset_database.py reset")

if __name__ == '__main__':
    main() 