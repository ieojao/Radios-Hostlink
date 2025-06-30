from app import app, db, Programacao

def verificar_programacoes():
    with app.app_context():
        print("📻 Programações existentes:")
        programas = Programacao.query.all()
        
        if not programas:
            print("Nenhuma programação encontrada!")
        else:
            for programa in programas:
                print(f"  - {programa.dia_semana}: {programa.horario_inicio}-{programa.horario_fim} - {programa.titulo}")
        
        print(f"\n📊 Total: {len(programas)} programações")

if __name__ == '__main__':
    verificar_programacoes() 