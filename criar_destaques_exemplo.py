from app import app, db, Destaque

def criar_destaques_exemplo():
    with app.app_context():
        # Verificar se já existem destaques
        destaques_existentes = Destaque.query.count()
        
        if destaques_existentes == 0:
            # Criar destaques de exemplo
            destaques = [
                Destaque(
                    titulo='Programa da Manhã',
                    descricao='Comece seu dia com louvor e adoração. Música gospel para inspirar sua manhã.',
                    imagem='/static/images/destaque1.jpg',
                    link='',
                    ordem=1,
                    ativo=True
                ),
                Destaque(
                    titulo='Show da Tarde',
                    descricao='Música gospel para animar sua tarde. Os melhores hits para energizar seu dia.',
                    imagem='/static/images/destaque2.jpg',
                    link='',
                    ordem=2,
                    ativo=True
                ),
                Destaque(
                    titulo='Louvor da Noite',
                    descricao='Encerre seu dia com gratidão. Louvor e adoração para sua noite.',
                    imagem='/static/images/destaque3.jpg',
                    link='',
                    ordem=3,
                    ativo=True
                ),
                Destaque(
                    titulo='Culto Especial',
                    descricao='Participe dos nossos cultos especiais. Transmissão ao vivo todos os domingos.',
                    imagem='/static/images/destaque1.jpg',
                    link='https://youtube.com/radioshostlink',
                    ordem=4,
                    ativo=True
                ),
                Destaque(
                    titulo='Oração 24h',
                    descricao='Pedidos de oração. Nossa equipe ora por você 24 horas por dia.',
                    imagem='/static/images/destaque2.jpg',
                    link='https://wa.me/5511999999999',
                    ordem=5,
                    ativo=True
                )
            ]
            
            # Adicionar todos os destaques
            for destaque in destaques:
                db.session.add(destaque)
            
            db.session.commit()
            print("✅ Destaques de exemplo criados com sucesso!")
            print(f"⭐ Total de {len(destaques)} destaques criados")
        else:
            print(f"ℹ️ Já existem {destaques_existentes} destaques no sistema!")
        
        # Mostrar estatísticas
        print("\n📊 Estatísticas dos destaques:")
        total = Destaque.query.count()
        ativos = Destaque.query.filter_by(ativo=True).count()
        inativos = Destaque.query.filter_by(ativo=False).count()
        
        print(f"  - Total: {total} destaques")
        print(f"  - Ativos: {ativos} destaques")
        print(f"  - Inativos: {inativos} destaques")
        
        # Listar destaques
        print("\n📋 Destaques cadastrados:")
        destaques = Destaque.query.order_by(Destaque.ordem).all()
        for destaque in destaques:
            status = "✅ Ativo" if destaque.ativo else "❌ Inativo"
            print(f"  - {destaque.ordem}. {destaque.titulo} ({status})")

if __name__ == '__main__':
    criar_destaques_exemplo() 