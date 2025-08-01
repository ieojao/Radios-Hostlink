from datetime import datetime, time
from models.content import Programacao
from models.database import db

class ProgramacaoService:
    """Serviço para gerenciamento de programação"""
    
    @staticmethod
    def get_programacao_atual():
        """Retorna a programação atual baseada no dia e horário"""
        agora = datetime.now()
        dia_semana = agora.strftime('%A').upper()
        hora_atual = agora.time()
        
        # Mapeamento de dias em inglês para português
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
        
        # Buscar programação atual
        programacao = Programacao.query.filter_by(
            dia_semana=dia_portugues, 
            ativo=True
        ).filter(
            Programacao.horario_inicio <= hora_atual,
            Programacao.horario_fim >= hora_atual
        ).first()
        
        return programacao
    
    @staticmethod
    def get_programacao_status():
        """Retorna o status detalhado da programação atual"""
        agora = datetime.now()
        dia_semana = agora.strftime('%A').upper()
        hora_atual = agora.time()
        
        # Mapeamento de dias em inglês para português
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
        
        # Buscar todas as programações do dia
        programacoes = Programacao.query.filter_by(
            dia_semana=dia_portugues, 
            ativo=True
        ).order_by(Programacao.horario_inicio).all()
        
        if not programacoes:
            return {
                'status': 'sem_programacao',
                'mensagem': 'Nenhuma programação cadastrada para hoje',
                'programacao_atual': None,
                'proxima_programacao': None,
                'tempo_restante': None
            }
        
        # Encontrar programação atual
        programacao_atual = None
        proxima_programacao = None
        
        for programa in programacoes:
            if programa.horario_inicio <= hora_atual and programa.horario_fim >= hora_atual:
                programacao_atual = programa
                break
            elif programa.horario_inicio > hora_atual:
                if not proxima_programacao:
                    proxima_programacao = programa
        
        # Calcular tempo restante
        tempo_restante = None
        if programacao_atual:
            fim_programa = datetime.combine(agora.date(), programacao_atual.horario_fim)
            agora_dt = datetime.combine(agora.date(), agora.time())
            diferenca = fim_programa - agora_dt
            tempo_restante = {
                'minutos': int(diferenca.total_seconds() // 60),
                'segundos': int(diferenca.total_seconds() % 60)
            }
        
        return {
            'status': 'ao_vivo' if programacao_atual else 'aguardando',
            'programacao_atual': programacao_atual,
            'proxima_programacao': proxima_programacao,
            'tempo_restante': tempo_restante,
            'hora_atual': hora_atual.strftime('%H:%M'),
            'dia_semana': dia_portugues
        }
    
    @staticmethod
    def get_programacao_por_dia(dia):
        """Retorna programação de um dia específico"""
        dias_validos = ['DOMINGO', 'SEGUNDA', 'TERÇA', 'QUARTA', 'QUINTA', 'SEXTA', 'SÁBADO']
        if dia not in dias_validos:
            return []
        
        return Programacao.query.filter_by(
            dia_semana=dia, 
            ativo=True
        ).order_by(Programacao.horario_inicio).all()
    
    @staticmethod
    def get_programacao_completa():
        """Retorna programação completa organizada por dia"""
        dias_semana = ['DOMINGO', 'SEGUNDA', 'TERÇA', 'QUARTA', 'QUINTA', 'SEXTA', 'SÁBADO']
        programacao_por_dia = {}
        
        for dia in dias_semana:
            programacao_por_dia[dia] = ProgramacaoService.get_programacao_por_dia(dia)
        
        return programacao_por_dia
    
    @staticmethod
    def criar_programacao(dados):
        """Cria uma nova programação"""
        try:
            programacao = Programacao(
                dia_semana=dados['dia_semana'],
                horario_inicio=datetime.strptime(dados['horario_inicio'], '%H:%M').time(),
                horario_fim=datetime.strptime(dados['horario_fim'], '%H:%M').time(),
                titulo=dados['titulo'],
                descricao=dados.get('descricao', ''),
                imagem=dados.get('imagem', ''),
                ativo=dados.get('ativo', True)
            )
            db.session.add(programacao)
            db.session.commit()
            return programacao
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def atualizar_programacao(id, dados):
        """Atualiza uma programação existente"""
        try:
            programacao = Programacao.query.get_or_404(id)
            
            programacao.dia_semana = dados['dia_semana']
            programacao.horario_inicio = datetime.strptime(dados['horario_inicio'], '%H:%M').time()
            programacao.horario_fim = datetime.strptime(dados['horario_fim'], '%H:%M').time()
            programacao.titulo = dados['titulo']
            programacao.descricao = dados.get('descricao', '')
            programacao.imagem = dados.get('imagem', '')
            programacao.ativo = dados.get('ativo', True)
            
            db.session.commit()
            return programacao
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def deletar_programacao(id):
        """Deleta uma programação"""
        try:
            programacao = Programacao.query.get_or_404(id)
            db.session.delete(programacao)
            db.session.commit()
            return True
        except Exception as e:
            db.session.rollback()
            raise e 