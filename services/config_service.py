from models.content import Configuracao
from models.database import db

class ConfigService:
    """Serviço para gerenciamento de configurações do site"""
    
    @staticmethod
    def get_site_config():
        """Retorna todas as configurações do site"""
        configs = Configuracao.query.all()
        config_dict = {}
        for config in configs:
            config_dict[config.chave] = config.valor
        
        # Configurações padrão se não existirem
        defaults = {
            'nome_site': 'Radios Hostlink',
            'logo': 'logo.png',
            'favicon': 'favicon.ico',
            'fonte': 'Roboto',
            'texto_rodape': '© 2024 Radios Hostlink. Todos os direitos reservados.',
            'email_contato': 'contato@radioshostlink.com.br',
            'url_streaming': 'https://streaming.example.com/live',
            'whatsapp': '5511999999999',
            'facebook': 'https://facebook.com/radioshostlink',
            'instagram': 'https://instagram.com/radioshostlink',
            'youtube': 'https://youtube.com/radioshostlink',
            'programacao_padrao_titulo': 'Programação musical',
            'programacao_padrao_descricao': 'Música gospel 24 horas por dia',
            'programacao_padrao_horario': '24h - Ao vivo',
            'programacao_rolando_agora': 'ROLANDO AGORA'
        }
        
        for key, value in defaults.items():
            if key not in config_dict:
                config_dict[key] = value
        
        return config_dict
    
    @staticmethod
    def get_config(key, default=None):
        """Retorna uma configuração específica"""
        config = Configuracao.query.filter_by(chave=key).first()
        return config.valor if config else default
    
    @staticmethod
    def set_config(key, value, descricao=None, tipo='text'):
        """Define uma configuração"""
        try:
            config = Configuracao.query.filter_by(chave=key).first()
            if config:
                config.valor = value
                if descricao:
                    config.descricao = descricao
                if tipo:
                    config.tipo = tipo
            else:
                config = Configuracao(
                    chave=key,
                    valor=value,
                    descricao=descricao,
                    tipo=tipo
                )
                db.session.add(config)
            
            db.session.commit()
            return config
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def set_multiple_configs(configs_dict):
        """Define múltiplas configurações de uma vez"""
        try:
            for key, value in configs_dict.items():
                ConfigService.set_config(key, value)
            return True
        except Exception as e:
            raise e
    
    @staticmethod
    def delete_config(key):
        """Deleta uma configuração"""
        try:
            config = Configuracao.query.filter_by(chave=key).first()
            if config:
                db.session.delete(config)
                db.session.commit()
                return True
            return False
        except Exception as e:
            db.session.rollback()
            raise e
    
    @staticmethod
    def get_configs_by_type(tipo):
        """Retorna configurações por tipo"""
        return Configuracao.query.filter_by(tipo=tipo).all()
    
    @staticmethod
    def get_all_configs():
        """Retorna todas as configurações com metadados"""
        return Configuracao.query.order_by(Configuracao.chave).all() 