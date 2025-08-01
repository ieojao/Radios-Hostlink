from datetime import datetime
from models.database import db

class Programacao(db.Model):
    """Modelo de programação da rádio"""
    __tablename__ = 'programacao'
    
    id = db.Column(db.Integer, primary_key=True)
    dia_semana = db.Column(db.String(20), nullable=False)
    horario_inicio = db.Column(db.Time, nullable=False)
    horario_fim = db.Column(db.Time, nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    imagem = db.Column(db.String(255))
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Programacao {self.titulo}>'

class Locutor(db.Model):
    """Modelo de locutor"""
    __tablename__ = 'locutores'
    
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    foto = db.Column(db.String(255))
    bio = db.Column(db.Text)
    redes_sociais = db.Column(db.Text)  # JSON
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Locutor {self.nome}>'

class Banner(db.Model):
    """Modelo de banner"""
    __tablename__ = 'banners'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))
    imagem = db.Column(db.String(255))
    link = db.Column(db.String(255))
    ativo = db.Column(db.Boolean, default=True)
    ordem = db.Column(db.Integer, default=0)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Banner {self.titulo}>'

class Destaque(db.Model):
    """Modelo de destaque"""
    __tablename__ = 'destaques'
    
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    imagem = db.Column(db.String(255))
    link = db.Column(db.String(255))
    ordem = db.Column(db.Integer, default=0)
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Destaque {self.titulo}>'

class Configuracao(db.Model):
    """Modelo de configurações do site"""
    __tablename__ = 'configuracoes'
    
    id = db.Column(db.Integer, primary_key=True)
    chave = db.Column(db.String(100), nullable=False, unique=True)
    valor = db.Column(db.Text)
    descricao = db.Column(db.String(255))
    tipo = db.Column(db.String(20), default='text')  # text, number, boolean, json
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __repr__(self):
        return f'<Configuracao {self.chave}>' 