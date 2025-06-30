from app import app, db, Programacao
from datetime import time

def criar_programacao_exemplo():
    with app.app_context():
        # Verificar se já existem programações
        programacoes_existentes = Programacao.query.count()
        
        if programacoes_existentes == 0:
            # Criar programações de exemplo para cada dia da semana
            programacoes = [
                # DOMINGO
                Programacao(dia_semana='DOMINGO', horario_inicio=time(6, 0), horario_fim=time(8, 0), 
                          titulo='Louvor da Manhã', descricao='Comece seu domingo com louvor e adoração'),
                Programacao(dia_semana='DOMINGO', horario_inicio=time(8, 0), horario_fim=time(10, 0), 
                          titulo='Culto Online', descricao='Transmissão ao vivo do culto dominical'),
                Programacao(dia_semana='DOMINGO', horario_inicio=time(10, 0), horario_fim=time(12, 0), 
                          titulo='Gospel Hits', descricao='As melhores músicas gospel'),
                Programacao(dia_semana='DOMINGO', horario_inicio=time(12, 0), horario_fim=time(14, 0), 
                          titulo='Almoço Gospel', descricao='Música para acompanhar seu almoço'),
                Programacao(dia_semana='DOMINGO', horario_inicio=time(14, 0), horario_fim=time(16, 0), 
                          titulo='Tarde de Louvor', descricao='Louvor e adoração para sua tarde'),
                Programacao(dia_semana='DOMINGO', horario_inicio=time(16, 0), horario_fim=time(18, 0), 
                          titulo='Show Gospel', descricao='Programa especial com as melhores músicas'),
                Programacao(dia_semana='DOMINGO', horario_inicio=time(18, 0), horario_fim=time(20, 0), 
                          titulo='Culto da Noite', descricao='Encerrando o domingo com gratidão'),
                
                # SEGUNDA
                Programacao(dia_semana='SEGUNDA', horario_inicio=time(6, 0), horario_fim=time(8, 0), 
                          titulo='Despertar com Louvor', descricao='Comece sua semana com energia'),
                Programacao(dia_semana='SEGUNDA', horario_inicio=time(8, 0), horario_fim=time(10, 0), 
                          titulo='Gospel Workout', descricao='Música para animar seu trabalho'),
                Programacao(dia_semana='SEGUNDA', horario_inicio=time(10, 0), horario_fim=time(12, 0), 
                          titulo='Hits Gospel', descricao='As músicas mais tocadas'),
                Programacao(dia_semana='SEGUNDA', horario_inicio=time(12, 0), horario_fim=time(14, 0), 
                          titulo='Almoço Inspirado', descricao='Música para inspirar seu almoço'),
                Programacao(dia_semana='SEGUNDA', horario_inicio=time(14, 0), horario_fim=time(16, 0), 
                          titulo='Tarde Gospel', descricao='Energia para sua tarde'),
                Programacao(dia_semana='SEGUNDA', horario_inicio=time(16, 0), horario_fim=time(18, 0), 
                          titulo='Ritmo Gospel', descricao='Música com ritmo para animar'),
                Programacao(dia_semana='SEGUNDA', horario_inicio=time(18, 0), horario_fim=time(20, 0), 
                          titulo='Louvor da Noite', descricao='Encerrando o dia com gratidão'),
                
                # TERÇA
                Programacao(dia_semana='TERÇA', horario_inicio=time(6, 0), horario_fim=time(8, 0), 
                          titulo='Manhã Abençoada', descricao='Bênçãos para sua manhã'),
                Programacao(dia_semana='TERÇA', horario_inicio=time(8, 0), horario_fim=time(10, 0), 
                          titulo='Gospel Power', descricao='Poder do evangelho em sua vida'),
                Programacao(dia_semana='TERÇA', horario_inicio=time(10, 0), horario_fim=time(12, 0), 
                          titulo='Top Gospel', descricao='As melhores do gospel'),
                Programacao(dia_semana='TERÇA', horario_inicio=time(12, 0), horario_fim=time(14, 0), 
                          titulo='Almoço Abençoado', descricao='Bênçãos no seu almoço'),
                Programacao(dia_semana='TERÇA', horario_inicio=time(14, 0), horario_fim=time(16, 0), 
                          titulo='Tarde Inspirada', descricao='Inspiração para sua tarde'),
                Programacao(dia_semana='TERÇA', horario_inicio=time(16, 0), horario_fim=time(18, 0), 
                          titulo='Gospel Vibes', descricao='Vibrações positivas'),
                Programacao(dia_semana='TERÇA', horario_inicio=time(18, 0), horario_fim=time(20, 0), 
                          titulo='Adoração Noturna', descricao='Adoração para sua noite'),
                
                # QUARTA
                Programacao(dia_semana='QUARTA', horario_inicio=time(6, 0), horario_fim=time(8, 0), 
                          titulo='Meio da Semana', descricao='Energia para o meio da semana'),
                Programacao(dia_semana='QUARTA', horario_inicio=time(8, 0), horario_fim=time(10, 0), 
                          titulo='Gospel Hits', descricao='Os hits do momento'),
                Programacao(dia_semana='QUARTA', horario_inicio=time(10, 0), horario_fim=time(12, 0), 
                          titulo='Louvor Contínuo', descricao='Louvor sem parar'),
                Programacao(dia_semana='QUARTA', horario_inicio=time(12, 0), horario_fim=time(14, 0), 
                          titulo='Almoço Gospel', descricao='Gospel no seu almoço'),
                Programacao(dia_semana='QUARTA', horario_inicio=time(14, 0), horario_fim=time(16, 0), 
                          titulo='Tarde Gospel', descricao='Gospel para sua tarde'),
                Programacao(dia_semana='QUARTA', horario_inicio=time(16, 0), horario_fim=time(18, 0), 
                          titulo='Ritmo Gospel', descricao='Ritmo para animar'),
                Programacao(dia_semana='QUARTA', horario_inicio=time(18, 0), horario_fim=time(20, 0), 
                          titulo='Culto de Oração', descricao='Momento de oração'),
                
                # QUINTA
                Programacao(dia_semana='QUINTA', horario_inicio=time(6, 0), horario_fim=time(8, 0), 
                          titulo='Quinta Abençoada', descricao='Bênçãos para sua quinta'),
                Programacao(dia_semana='QUINTA', horario_inicio=time(8, 0), horario_fim=time(10, 0), 
                          titulo='Gospel Workout', descricao='Energia para trabalhar'),
                Programacao(dia_semana='QUINTA', horario_inicio=time(10, 0), horario_fim=time(12, 0), 
                          titulo='Hits Gospel', descricao='Os hits mais tocados'),
                Programacao(dia_semana='QUINTA', horario_inicio=time(12, 0), horario_fim=time(14, 0), 
                          titulo='Almoço Inspirado', descricao='Inspiração no almoço'),
                Programacao(dia_semana='QUINTA', horario_inicio=time(14, 0), horario_fim=time(16, 0), 
                          titulo='Tarde Inspirada', descricao='Inspiração para tarde'),
                Programacao(dia_semana='QUINTA', horario_inicio=time(16, 0), horario_fim=time(18, 0), 
                          titulo='Gospel Vibes', descricao='Vibrações positivas'),
                Programacao(dia_semana='QUINTA', horario_inicio=time(18, 0), horario_fim=time(20, 0), 
                          titulo='Louvor da Noite', descricao='Louvor noturno'),
                
                # SEXTA
                Programacao(dia_semana='SEXTA', horario_inicio=time(6, 0), horario_fim=time(8, 0), 
                          titulo='Sexta Abençoada', descricao='Bênçãos para sua sexta'),
                Programacao(dia_semana='SEXTA', horario_inicio=time(8, 0), horario_fim=time(10, 0), 
                          titulo='Gospel Power', descricao='Poder do evangelho'),
                Programacao(dia_semana='SEXTA', horario_inicio=time(10, 0), horario_fim=time(12, 0), 
                          titulo='Top Gospel', descricao='O melhor do gospel'),
                Programacao(dia_semana='SEXTA', horario_inicio=time(12, 0), horario_fim=time(14, 0), 
                          titulo='Almoço Abençoado', descricao='Bênçãos no almoço'),
                Programacao(dia_semana='SEXTA', horario_inicio=time(14, 0), horario_fim=time(16, 0), 
                          titulo='Tarde Inspirada', descricao='Inspiração para tarde'),
                Programacao(dia_semana='SEXTA', horario_inicio=time(16, 0), horario_fim=time(18, 0), 
                          titulo='Gospel Vibes', descricao='Vibrações positivas'),
                Programacao(dia_semana='SEXTA', horario_inicio=time(18, 0), horario_fim=time(20, 0), 
                          titulo='Adoração Noturna', descricao='Adoração noturna'),
                
                # SÁBADO
                Programacao(dia_semana='SÁBADO', horario_inicio=time(6, 0), horario_fim=time(8, 0), 
                          titulo='Sábado Gospel', descricao='Gospel para seu sábado'),
                Programacao(dia_semana='SÁBADO', horario_inicio=time(8, 0), horario_fim=time(10, 0), 
                          titulo='Gospel Hits', descricao='Os hits do gospel'),
                Programacao(dia_semana='SÁBADO', horario_inicio=time(10, 0), horario_fim=time(12, 0), 
                          titulo='Louvor Contínuo', descricao='Louvor sem parar'),
                Programacao(dia_semana='SÁBADO', horario_inicio=time(12, 0), horario_fim=time(14, 0), 
                          titulo='Almoço Gospel', descricao='Gospel no almoço'),
                Programacao(dia_semana='SÁBADO', horario_inicio=time(14, 0), horario_fim=time(16, 0), 
                          titulo='Tarde Gospel', descricao='Gospel para tarde'),
                Programacao(dia_semana='SÁBADO', horario_inicio=time(16, 0), horario_fim=time(18, 0), 
                          titulo='Ritmo Gospel', descricao='Ritmo para animar'),
                Programacao(dia_semana='SÁBADO', horario_inicio=time(18, 0), horario_fim=time(20, 0), 
                          titulo='Show Gospel', descricao='Show especial de sábado'),
            ]
            
            # Adicionar todas as programações
            for programa in programacoes:
                db.session.add(programa)
            
            db.session.commit()
            print("✅ Programações de exemplo criadas com sucesso!")
            print(f"📻 Total de {len(programacoes)} programações criadas")
        else:
            print(f"ℹ️ Já existem {programacoes_existentes} programações no sistema!")
        
        # Mostrar estatísticas
        print("\n📊 Estatísticas da programação:")
        dias_semana = ['DOMINGO', 'SEGUNDA', 'TERÇA', 'QUARTA', 'QUINTA', 'SEXTA', 'SÁBADO']
        for dia in dias_semana:
            count = Programacao.query.filter_by(dia_semana=dia).count()
            print(f"  - {dia}: {count} programas")

if __name__ == '__main__':
    criar_programacao_exemplo() 