from flask import Blueprint, jsonify, request
from services.programacao_service import ProgramacaoService
from services.config_service import ConfigService
from models.content import Programacao
from datetime import datetime

# Criar blueprint para rotas da API
api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/programacao-atual')
def programacao_atual():
    """API para obter programação atual"""
    status = ProgramacaoService.get_programacao_status()
    
    if status['status'] == 'sem_programacao':
        return jsonify({
            'error': 'Nenhuma programação encontrada',
            'status': 'sem_programacao',
            'mensagem': status['mensagem']
        })
    
    if status['programacao_atual']:
        programacao = status['programacao_atual']
        return jsonify({
            'titulo': programacao.titulo,
            'descricao': programacao.descricao,
            'imagem': programacao.imagem,
            'horario_inicio': programacao.horario_inicio.strftime('%H:%M'),
            'horario_fim': programacao.horario_fim.strftime('%H:%M'),
            'status': 'ao_vivo',
            'tempo_restante': status['tempo_restante'],
            'hora_atual': status['hora_atual']
        })
    elif status['proxima_programacao']:
        programacao = status['proxima_programacao']
        return jsonify({
            'titulo': programacao.titulo,
            'descricao': programacao.descricao,
            'imagem': programacao.imagem,
            'horario_inicio': programacao.horario_inicio.strftime('%H:%M'),
            'horario_fim': programacao.horario_fim.strftime('%H:%M'),
            'status': 'proximo',
            'hora_atual': status['hora_atual']
        })
    
    return jsonify({'error': 'Nenhuma programação encontrada'})

@api_bp.route('/programacao-status')
def programacao_status():
    """API para obter status detalhado da programação"""
    return jsonify(ProgramacaoService.get_programacao_status())

@api_bp.route('/programacao-dia/<dia>')
def programacao_dia(dia):
    """API para buscar programações de um dia específico"""
    try:
        # Validar dia da semana
        dias_validos = ['DOMINGO', 'SEGUNDA', 'TERÇA', 'QUARTA', 'QUINTA', 'SEXTA', 'SÁBADO']
        if dia not in dias_validos:
            return jsonify({'error': 'Dia da semana inválido'}), 400
        
        # Buscar programações do dia
        programacoes = Programacao.query.filter_by(
            dia_semana=dia, 
            ativo=True
        ).order_by(Programacao.horario_inicio).all()
        
        # Verificar qual programa está ao vivo
        agora = datetime.now()
        hora_atual = agora.time()
        
        # Mapear dias da semana para números (0=Segunda, 6=Domingo)
        dias_semana = {
            'SEGUNDA': 0, 'TERÇA': 1, 'QUARTA': 2, 'QUINTA': 3, 
            'SEXTA': 4, 'SÁBADO': 5, 'DOMINGO': 6
        }
        
        # Obter o dia atual da semana (0=Segunda, 6=Domingo)
        dia_atual_num = agora.weekday()
        dia_consulta_num = dias_semana.get(dia, None)
        
        # Verificar se estamos consultando o dia atual
        is_dia_atual = (dia_atual_num == dia_consulta_num)
        
        programacoes_json = []
        programacao_atual = None
        proxima_programacao = None
        
        for programa in programacoes:
            # Só considerar "ao vivo" se for o dia atual
            is_atual = is_dia_atual and (programa.horario_inicio <= hora_atual and programa.horario_fim >= hora_atual)
            is_proximo = is_dia_atual and (programa.horario_inicio > hora_atual and not proxima_programacao)
            
            if is_atual:
                programacao_atual = programa
            elif is_proximo:
                proxima_programacao = programa
            
            # Calcular tempo restante se for o programa atual
            tempo_restante = None
            if is_atual:
                fim_programa = datetime.combine(agora.date(), programa.horario_fim)
                agora_dt = datetime.combine(agora.date(), agora.time())
                diferenca = fim_programa - agora_dt
                tempo_restante = {
                    'minutos': int(diferenca.total_seconds() // 60),
                    'segundos': int(diferenca.total_seconds() % 60)
                }
            
            programacoes_json.append({
                'id': programa.id,
                'titulo': programa.titulo,
                'descricao': programa.descricao,
                'horario_inicio': programa.horario_inicio.strftime('%H:%M'),
                'horario_fim': programa.horario_fim.strftime('%H:%M'),
                'imagem': programa.imagem,
                'is_atual': is_atual,
                'is_proximo': is_proximo,
                'tempo_restante': tempo_restante,
                'status': 'ao_vivo' if is_atual else ('proximo' if is_proximo else 'aguardando')
            })
        
        return jsonify({
            'dia': dia,
            'programacoes': programacoes_json,
            'programacao_atual': programacao_atual.id if programacao_atual else None,
            'proxima_programacao': proxima_programacao.id if proxima_programacao else None,
            'hora_atual': hora_atual.strftime('%H:%M'),
            'total_programas': len(programacoes)
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Erro ao buscar programações: {str(e)}'
        }), 500

@api_bp.route('/streaming-url')
def streaming_url():
    """API para fornecer a URL de streaming do rádio"""
    try:
        streaming_url = ConfigService.get_config('url_streaming')
        
        if streaming_url:
            return jsonify({
                'streaming_url': streaming_url,
                'status': 'success'
            })
        else:
            return jsonify({
                'error': 'URL de streaming não configurada',
                'status': 'error'
            }), 404
    except Exception as e:
        return jsonify({
            'error': f'Erro ao buscar URL de streaming: {str(e)}',
            'status': 'error'
        }), 500

@api_bp.route('/player-stats')
def player_stats():
    """API para estatísticas do player"""
    try:
        return jsonify({
            'status': 'success',
            'data': {
                'listeners': 0,  # Placeholder
                'current_track': {
                    'title': 'Rádio Online',
                    'artist': 'Ao Vivo',
                    'duration': 0
                },
                'stream_status': 'online'
            }
        })
    except Exception as e:
        return jsonify({
            'error': f'Erro ao buscar estatísticas: {str(e)}',
            'status': 'error'
        }), 500

@api_bp.route('/site-config')
def site_config():
    """API para obter configurações do site"""
    try:
        config = ConfigService.get_site_config()
        return jsonify({
            'status': 'success',
            'config': config
        })
    except Exception as e:
        return jsonify({
            'error': f'Erro ao buscar configurações: {str(e)}',
            'status': 'error'
        }), 500 