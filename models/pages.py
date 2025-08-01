from datetime import datetime
from models.database import db

class PaginaRadio(db.Model):
    """Modelo da página 'A Rádio'"""
    __tablename__ = 'pagina_radio'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    subtitulo = db.Column(db.String(300))
    descricao = db.Column(db.Text)
    historia = db.Column(db.Text)
    missao = db.Column(db.Text)
    visao = db.Column(db.Text)
    valores = db.Column(db.Text)
    imagem_principal = db.Column(db.String(255))
    imagem_historia = db.Column(db.String(255))
    estatisticas = db.Column(db.Text)  # JSON
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<PaginaRadio {self.titulo}>'

class PaginaEquipe(db.Model):
    """Modelo da página 'Equipe'"""
    __tablename__ = 'pagina_equipe'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    subtitulo = db.Column(db.String(300))
    descricao = db.Column(db.Text)
    mensagem_equipe = db.Column(db.Text)
    imagem_principal = db.Column(db.String(255))
    estatisticas_equipe = db.Column(db.Text)  # JSON
    areas_atuacao = db.Column(db.Text)  # JSON
    convite_equipe = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<PaginaEquipe {self.titulo}>'

class PaginaContato(db.Model):
    """Modelo da página 'Contato'"""
    __tablename__ = 'pagina_contato'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    subtitulo = db.Column(db.String(300))
    descricao = db.Column(db.Text)
    telefone_principal = db.Column(db.String(20))
    telefone_secundario = db.Column(db.String(20))
    email_contato = db.Column(db.String(100))
    endereco = db.Column(db.Text)
    horario_funcionamento = db.Column(db.Text)
    redes_sociais = db.Column(db.Text)  # JSON
    mapa_embed = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<PaginaContato {self.titulo}>'

class MensagemContato(db.Model):
    """Modelo de mensagens de contato"""
    __tablename__ = 'mensagens_contato'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20))
    assunto = db.Column(db.String(200))
    mensagem = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='não_lida')  # não_lida, lida, respondida
    ip_address = db.Column(db.String(45))  # Para rastreamento
    user_agent = db.Column(db.Text)  # Para rastreamento
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<MensagemContato {self.nome}>' 