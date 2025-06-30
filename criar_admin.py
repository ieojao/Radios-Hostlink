from app import app, db, Usuario
from werkzeug.security import generate_password_hash
from datetime import datetime

def criar_admin_padrao():
    with app.app_context():
        # Verificar se já existe um usuário admin
        admin_existente = Usuario.query.filter_by(email='admin@radioshostlink.com').first()
        
        if not admin_existente:
            # Criar usuário admin padrão
            admin = Usuario(
                nome='Administrador',
                email='admin@radioshostlink.com',
                senha=generate_password_hash('admin123'),
                nivel='admin',
                criado_em=datetime.utcnow()
            )
            
            db.session.add(admin)
            db.session.commit()
            print("✅ Usuário admin criado com sucesso!")
            print("📧 Email: admin@radioshostlink.com")
            print("🔑 Senha: admin123")
        else:
            print("ℹ️ Usuário admin já existe!")
            print(f"📧 Email: {admin_existente.email}")
        
        # Listar todos os usuários
        print("\n👥 Usuários no sistema:")
        usuarios = Usuario.query.all()
        for usuario in usuarios:
            print(f"  - ID: {usuario.id}, Nome: {usuario.nome}, Email: {usuario.email}")

if __name__ == '__main__':
    criar_admin_padrao() 