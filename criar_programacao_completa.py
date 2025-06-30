#!/usr/bin/env python3
"""
Script para criar programação completa que cubra todo o dia
"""

from app import app, db, Programacao
from datetime import time
import os

def criar_programacao_completa():
    """Cria programação que cobre todo o dia para todos os dias da semana"""
    
    with app.app_context():
        # Primeiro, vamos limpar programações existentes
        print("Limpando programações existentes...")
        Programacao.query.delete()
        db.session.commit()
        
        # Programação para cada dia da semana
        dias_semana = ['DOMINGO', 'SEGUNDA', 'TERÇA', 'QUARTA', 'QUINTA', 'SEXTA', 'SÁBADO']
        
        # Programas para cada período do dia
        programas = [
            {
                'inicio': time(6, 0),   # 06:00
                'fim': time(9, 0),      # 09:00
                'titulo': 'Programa da Manhã',
                'descricao': 'Comece seu dia com louvor e adoração. Música gospel para animar sua manhã.'
            },
            {
                'inicio': time(9, 0),   # 09:00
                'fim': time(12, 0),     # 12:00
                'titulo': 'Show da Manhã',
                'descricao': 'Música gospel e mensagens edificantes para sua manhã.'
            },
            {
                'inicio': time(12, 0),  # 12:00
                'fim': time(15, 0),     # 15:00
                'titulo': 'Programa do Almoço',
                'descricao': 'Música relaxante e reflexões para o horário de almoço.'
            },
            {
                'inicio': time(15, 0),  # 15:00
                'fim': time(18, 0),     # 18:00
                'titulo': 'Show da Tarde',
                'descricao': 'Música gospel para animar sua tarde e preparar para o fim do dia.'
            },
            {
                'inicio': time(18, 0),  # 18:00
                'fim': time(21, 0),     # 21:00
                'titulo': 'Programa da Noite',
                'descricao': 'Louvor e adoração para encerrar seu dia com gratidão.'
            },
            {
                'inicio': time(21, 0),  # 21:00
                'fim': time(23, 59),    # 23:59
                'titulo': 'Louvor da Noite',
                'descricao': 'Música gospel suave para relaxar e meditar antes de dormir.'
            },
            {
                'inicio': time(0, 0),   # 00:00
                'fim': time(6, 0),      # 06:00
                'titulo': 'Programa da Madrugada',
                'descricao': 'Música gospel 24 horas por dia. Louvor contínuo.'
            }
        ]
        
        # Criar programação para cada dia
        total_criado = 0
        for dia in dias_semana:
            print(f"\nCriando programação para {dia}...")
            
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
        
        print(f"\n✅ Programação completa criada com sucesso!")
        print(f"📊 Total de programas criados: {total_criado}")
        print(f"📅 Dias da semana: {len(dias_semana)}")
        print(f"⏰ Programas por dia: {len(programas)}")
        
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

if __name__ == '__main__':
    print("🎵 Criando programação completa para a rádio...")
    criar_programacao_completa() 