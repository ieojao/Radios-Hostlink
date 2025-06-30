#!/usr/bin/env python3
"""
Script para criar programações específicas e únicas para cada dia da semana
"""

from app import app, db, Programacao
from datetime import time
import os

def criar_programacao_especifica():
    """Cria programações específicas e únicas para cada dia da semana"""
    
    with app.app_context():
        # Primeiro, vamos limpar programações existentes
        print("Limpando programações existentes...")
        Programacao.query.delete()
        db.session.commit()
        
        # Programações específicas para cada dia
        programacoes_por_dia = {
            'DOMINGO': [
                {
                    'inicio': time(6, 0), 'fim': time(9, 0),
                    'titulo': 'Culto da Manhã',
                    'descricao': 'Culto dominical com louvor, adoração e palavra de Deus.'
                },
                {
                    'inicio': time(9, 0), 'fim': time(12, 0),
                    'titulo': 'Gospel Dominical',
                    'descricao': 'As melhores músicas gospel para seu domingo especial.'
                },
                {
                    'inicio': time(12, 0), 'fim': time(15, 0),
                    'titulo': 'Almoço com Louvor',
                    'descricao': 'Música gospel para o almoço em família no domingo.'
                },
                {
                    'inicio': time(15, 0), 'fim': time(18, 0),
                    'titulo': 'Tarde de Adoração',
                    'descricao': 'Tarde especial de louvor e adoração dominical.'
                },
                {
                    'inicio': time(18, 0), 'fim': time(21, 0),
                    'titulo': 'Culto da Noite',
                    'descricao': 'Culto dominical da noite com palavra e louvor.'
                },
                {
                    'inicio': time(21, 0), 'fim': time(23, 59),
                    'titulo': 'Louvor Dominical',
                    'descricao': 'Encerrando o domingo com muito louvor e gratidão.'
                },
                {
                    'inicio': time(0, 0), 'fim': time(6, 0),
                    'titulo': 'Madrugada de Oração',
                    'descricao': 'Madrugada de oração e intercessão dominical.'
                }
            ],
            
            'SEGUNDA': [
                {
                    'inicio': time(6, 0), 'fim': time(9, 0),
                    'titulo': 'Segunda com Energia',
                    'descricao': 'Comece sua semana com energia e louvor gospel.'
                },
                {
                    'inicio': time(9, 0), 'fim': time(12, 0),
                    'titulo': 'Gospel na Segunda',
                    'descricao': 'Música gospel para animar sua segunda-feira.'
                },
                {
                    'inicio': time(12, 0), 'fim': time(15, 0),
                    'titulo': 'Almoço Motivacional',
                    'descricao': 'Almoço com músicas que motivam para a semana.'
                },
                {
                    'inicio': time(15, 0), 'fim': time(18, 0),
                    'titulo': 'Tarde de Segunda',
                    'descricao': 'Tarde de segunda com louvor e adoração.'
                },
                {
                    'inicio': time(18, 0), 'fim': time(21, 0),
                    'titulo': 'Noite de Oração',
                    'descricao': 'Noite de oração e intercessão para a semana.'
                },
                {
                    'inicio': time(21, 0), 'fim': time(23, 59),
                    'titulo': 'Louvor da Segunda',
                    'descricao': 'Encerrando a segunda com louvor e gratidão.'
                },
                {
                    'inicio': time(0, 0), 'fim': time(6, 0),
                    'titulo': 'Madrugada de Segunda',
                    'descricao': 'Madrugada de segunda com música gospel suave.'
                }
            ],
            
            'TERÇA': [
                {
                    'inicio': time(6, 0), 'fim': time(9, 0),
                    'titulo': 'Terça com Louvor',
                    'descricao': 'Terça-feira começando com muito louvor e adoração.'
                },
                {
                    'inicio': time(9, 0), 'fim': time(12, 0),
                    'titulo': 'Gospel na Terça',
                    'descricao': 'Música gospel para animar sua terça-feira.'
                },
                {
                    'inicio': time(12, 0), 'fim': time(15, 0),
                    'titulo': 'Almoço com Adoração',
                    'descricao': 'Almoço de terça com músicas de adoração.'
                },
                {
                    'inicio': time(15, 0), 'fim': time(18, 0),
                    'titulo': 'Tarde de Terça',
                    'descricao': 'Tarde de terça com louvor e reflexão.'
                },
                {
                    'inicio': time(18, 0), 'fim': time(21, 0),
                    'titulo': 'Noite de Adoração',
                    'descricao': 'Noite de terça com adoração e louvor.'
                },
                {
                    'inicio': time(21, 0), 'fim': time(23, 59),
                    'titulo': 'Louvor da Terça',
                    'descricao': 'Encerrando a terça com louvor e gratidão.'
                },
                {
                    'inicio': time(0, 0), 'fim': time(6, 0),
                    'titulo': 'Madrugada de Terça',
                    'descricao': 'Madrugada de terça com música gospel.'
                }
            ],
            
            'QUARTA': [
                {
                    'inicio': time(6, 0), 'fim': time(9, 0),
                    'titulo': 'Quarta com Energia',
                    'descricao': 'Quarta-feira começando com energia e louvor.'
                },
                {
                    'inicio': time(9, 0), 'fim': time(12, 0),
                    'titulo': 'Gospel na Quarta',
                    'descricao': 'Música gospel para animar sua quarta-feira.'
                },
                {
                    'inicio': time(12, 0), 'fim': time(15, 0),
                    'titulo': 'Almoço com Louvor',
                    'descricao': 'Almoço de quarta com louvor e adoração.'
                },
                {
                    'inicio': time(15, 0), 'fim': time(18, 0),
                    'titulo': 'Tarde de Quarta',
                    'descricao': 'Tarde de quarta com música gospel.'
                },
                {
                    'inicio': time(18, 0), 'fim': time(21, 0),
                    'titulo': 'Noite de Oração',
                    'descricao': 'Noite de oração e intercessão na quarta.'
                },
                {
                    'inicio': time(21, 0), 'fim': time(23, 59),
                    'titulo': 'Louvor da Quarta',
                    'descricao': 'Encerrando a quarta com louvor e gratidão.'
                },
                {
                    'inicio': time(0, 0), 'fim': time(6, 0),
                    'titulo': 'Madrugada de Quarta',
                    'descricao': 'Madrugada de quarta com música gospel.'
                }
            ],
            
            'QUINTA': [
                {
                    'inicio': time(6, 0), 'fim': time(9, 0),
                    'titulo': 'Quinta com Louvor',
                    'descricao': 'Quinta-feira começando com louvor e adoração.'
                },
                {
                    'inicio': time(9, 0), 'fim': time(12, 0),
                    'titulo': 'Gospel na Quinta',
                    'descricao': 'Música gospel para animar sua quinta-feira.'
                },
                {
                    'inicio': time(12, 0), 'fim': time(15, 0),
                    'titulo': 'Almoço com Adoração',
                    'descricao': 'Almoço de quinta com adoração e louvor.'
                },
                {
                    'inicio': time(15, 0), 'fim': time(18, 0),
                    'titulo': 'Tarde de Quinta',
                    'descricao': 'Tarde de quinta com música gospel.'
                },
                {
                    'inicio': time(18, 0), 'fim': time(21, 0),
                    'titulo': 'Noite de Adoração',
                    'descricao': 'Noite de quinta com adoração e louvor.'
                },
                {
                    'inicio': time(21, 0), 'fim': time(23, 59),
                    'titulo': 'Louvor da Quinta',
                    'descricao': 'Encerrando a quinta com louvor e gratidão.'
                },
                {
                    'inicio': time(0, 0), 'fim': time(6, 0),
                    'titulo': 'Madrugada de Quinta',
                    'descricao': 'Madrugada de quinta com música gospel.'
                }
            ],
            
            'SEXTA': [
                {
                    'inicio': time(6, 0), 'fim': time(9, 0),
                    'titulo': 'Sexta com Alegria',
                    'descricao': 'Sexta-feira começando com alegria e louvor.'
                },
                {
                    'inicio': time(9, 0), 'fim': time(12, 0),
                    'titulo': 'Gospel na Sexta',
                    'descricao': 'Música gospel para animar sua sexta-feira.'
                },
                {
                    'inicio': time(12, 0), 'fim': time(15, 0),
                    'titulo': 'Almoço com Alegria',
                    'descricao': 'Almoço de sexta com músicas alegres.'
                },
                {
                    'inicio': time(15, 0), 'fim': time(18, 0),
                    'titulo': 'Tarde de Sexta',
                    'descricao': 'Tarde de sexta com louvor e adoração.'
                },
                {
                    'inicio': time(18, 0), 'fim': time(21, 0),
                    'titulo': 'Noite de Louvor',
                    'descricao': 'Noite de sexta com muito louvor e adoração.'
                },
                {
                    'inicio': time(21, 0), 'fim': time(23, 59),
                    'titulo': 'Louvor da Sexta',
                    'descricao': 'Encerrando a sexta com louvor e gratidão.'
                },
                {
                    'inicio': time(0, 0), 'fim': time(6, 0),
                    'titulo': 'Madrugada de Sexta',
                    'descricao': 'Madrugada de sexta com música gospel.'
                }
            ],
            
            'SÁBADO': [
                {
                    'inicio': time(6, 0), 'fim': time(9, 0),
                    'titulo': 'Sábado com Paz',
                    'descricao': 'Sábado começando com paz e louvor.'
                },
                {
                    'inicio': time(9, 0), 'fim': time(12, 0),
                    'titulo': 'Gospel no Sábado',
                    'descricao': 'Música gospel para relaxar no sábado.'
                },
                {
                    'inicio': time(12, 0), 'fim': time(15, 0),
                    'titulo': 'Almoço Tranquilo',
                    'descricao': 'Almoço de sábado com músicas tranquilas.'
                },
                {
                    'inicio': time(15, 0), 'fim': time(18, 0),
                    'titulo': 'Tarde de Sábado',
                    'descricao': 'Tarde de sábado com louvor e adoração.'
                },
                {
                    'inicio': time(18, 0), 'fim': time(21, 0),
                    'titulo': 'Noite de Sábado',
                    'descricao': 'Noite de sábado com música gospel.'
                },
                {
                    'inicio': time(21, 0), 'fim': time(23, 59),
                    'titulo': 'Louvor do Sábado',
                    'descricao': 'Encerrando o sábado com louvor e gratidão.'
                },
                {
                    'inicio': time(0, 0), 'fim': time(6, 0),
                    'titulo': 'Madrugada de Sábado',
                    'descricao': 'Madrugada de sábado com música gospel.'
                }
            ]
        }
        
        # Criar programação para cada dia
        total_criado = 0
        for dia, programas in programacoes_por_dia.items():
            print(f"\n🎵 Criando programação específica para {dia}...")
            
            for programa in programas:
                # Criar programa
                novo_programa = Programacao(
                    dia_semana=dia,
                    horario_inicio=programa['inicio'],
                    horario_fim=programa['fim'],
                    titulo=programa['titulo'],
                    descricao=programa['descricao']
                )
                
                db.session.add(novo_programa)
                total_criado += 1
                print(f"  ✓ {programa['titulo']} ({programa['inicio'].strftime('%H:%M')}-{programa['fim'].strftime('%H:%M')})")
        
        # Salvar no banco
        db.session.commit()
        
        print(f"\n✅ Programação específica criada com sucesso!")
        print(f"📊 Total de programas criados: {total_criado}")
        print(f"📅 Dias da semana: {len(programacoes_por_dia)}")
        
        # Mostrar resumo por dia
        print(f"\n📋 Resumo por dia:")
        for dia in programacoes_por_dia.keys():
            count = len(programacoes_por_dia[dia])
            print(f"  • {dia}: {count} programas específicos")
        
        # Verificar programação atual
        from datetime import datetime
        agora = datetime.now()
        print(f"\n🕐 Horário atual: {agora.strftime('%H:%M')}")
        
        # Buscar programa atual
        from app import get_programacao_atual
        programa_atual = get_programacao_atual()
        
        if programa_atual:
            print(f"🎵 Programa atual: {programa_atual.titulo}")
            print(f"📝 Descrição: {programa_atual.descricao}")
            print(f"⏰ Horário: {programa_atual.horario_inicio.strftime('%H:%M')} - {programa_atual.horario_fim.strftime('%H:%M')}")
        else:
            print("❌ Nenhum programa encontrado para o horário atual")
        
        print("\n🌐 Acesse o site para ver a programação funcionando!")
        print("🔧 Para editar programas, acesse: /admin/programacao")
        print("📝 Cada dia agora tem sua programação específica e configurável!")

if __name__ == '__main__':
    print("🎵 Criando programação específica para cada dia da semana...")
    criar_programacao_especifica() 