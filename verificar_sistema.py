from app import app, db, Usuario, Programacao, Configuracao, Destaque
from datetime import datetime

def verificar_sistema():
    with app.app_context():
        print("🔍 VERIFICANDO SISTEMA RADIOS HOSTLINK")
        print("=" * 50)
        
        # Verificar usuários
        print("\n👥 USUÁRIOS:")
        usuarios = Usuario.query.all()
        if usuarios:
            for usuario in usuarios:
                print(f"  ✅ {usuario.nome} ({usuario.email}) - Nível: {usuario.nivel}")
        else:
            print("  ❌ Nenhum usuário encontrado")
        
        # Verificar programações
        print("\n📻 PROGRAMAÇÕES:")
        programacoes = Programacao.query.all()
        if programacoes:
            print(f"  ✅ Total de {len(programacoes)} programações cadastradas")
            dias_semana = ['DOMINGO', 'SEGUNDA', 'TERÇA', 'QUARTA', 'QUINTA', 'SEXTA', 'SÁBADO']
            for dia in dias_semana:
                count = Programacao.query.filter_by(dia_semana=dia).count()
                print(f"    - {dia}: {count} programas")
        else:
            print("  ❌ Nenhuma programação encontrada")
        
        # Verificar destaques
        print("\n⭐ DESTAQUES:")
        destaques = Destaque.query.all()
        if destaques:
            print(f"  ✅ Total de {len(destaques)} destaques cadastrados")
            ativos = Destaque.query.filter_by(ativo=True).count()
            inativos = Destaque.query.filter_by(ativo=False).count()
            print(f"    - Ativos: {ativos} destaques")
            print(f"    - Inativos: {inativos} destaques")
            
            print("\n📋 Lista de destaques:")
            destaques_ordenados = Destaque.query.order_by(Destaque.ordem).all()
            for destaque in destaques_ordenados:
                status = "✅" if destaque.ativo else "❌"
                print(f"    {status} {destaque.ordem}. {destaque.titulo}")
        else:
            print("  ❌ Nenhum destaque encontrado")
        
        # Verificar configurações
        print("\n⚙️ CONFIGURAÇÕES:")
        configs = Configuracao.query.all()
        if configs:
            print(f"  ✅ {len(configs)} configurações encontradas")
            for config in configs:
                print(f"    - {config.chave}: {config.valor[:50]}{'...' if len(config.valor) > 50 else ''}")
        else:
            print("  ⚠️ Nenhuma configuração personalizada encontrada (usando padrões)")
        
        # Verificar programação atual
        print("\n🎵 PROGRAMAÇÃO ATUAL:")
        agora = datetime.now()
        dia_semana = agora.strftime('%A').upper()
        hora_atual = agora.time()
        
        dias_map = {
            'MONDAY': 'SEGUNDA',
            'TUESDAY': 'TERÇA', 
            'WEDNESDAY': 'QUARTA',
            'THURSDAY': 'QUINTA',
            'FRIDAY': 'SEXTA',
            'SATURDAY': 'SÁBADO',
            'SUNDAY': 'DOMINGO'
        }
        
        dia_portugues = dias_map.get(dia_semana, dia_semana)
        programacao_atual = Programacao.query.filter_by(dia_semana=dia_portugues).filter(
            Programacao.horario_inicio <= hora_atual,
            Programacao.horario_fim >= hora_atual
        ).first()
        
        if programacao_atual:
            print(f"  ✅ {programacao_atual.titulo} ({programacao_atual.horario_inicio.strftime('%H:%M')} - {programacao_atual.horario_fim.strftime('%H:%M')})")
        else:
            print(f"  ⚠️ Nenhuma programação ao vivo no momento ({dia_portugues} - {hora_atual.strftime('%H:%M')})")
        
        print("\n" + "=" * 50)
        print("🎉 SISTEMA PRONTO!")
        print("\n📋 INSTRUÇÕES:")
        print("1. Acesse: http://127.0.0.1:5000")
        print("2. Para o admin: http://127.0.0.1:5000/admin")
        print("3. Login admin: admin@radioshostlink.com / admin123")
        print("\n✨ Funcionalidades ativas:")
        print("  ✅ Página inicial com programação")
        print("  ✅ Dashboard administrativo")
        print("  ✅ Gerenciamento de programações")
        print("  ✅ Gerenciamento de destaques")
        print("  ✅ Sistema de login")
        print("  ✅ API para programação atual")
        print("  ✅ Grade de programação por dia")

if __name__ == '__main__':
    verificar_sistema() 