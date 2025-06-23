from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, time
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente
load_dotenv()

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'sua-chave-secreta-aqui')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///radio.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'admin_login'

# Modelos do banco de dados
class Usuario(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    senha = db.Column(db.String(255), nullable=False)
    nivel = db.Column(db.String(20), default='admin')
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

class Programacao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    dia_semana = db.Column(db.String(20), nullable=False)
    horario_inicio = db.Column(db.Time, nullable=False)
    horario_fim = db.Column(db.Time, nullable=False)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    imagem = db.Column(db.String(255))
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

class Locutor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    foto = db.Column(db.String(255))
    bio = db.Column(db.Text)
    redes_sociais = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

class Banner(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100))
    imagem = db.Column(db.String(255))
    link = db.Column(db.String(255))
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

class Configuracao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    chave = db.Column(db.String(100), nullable=False)
    valor = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

@login_manager.user_loader
def load_user(user_id):
    return Usuario.query.get(int(user_id))

# Configurações padrão do site
def get_site_config():
    configs = Configuracao.query.all()
    config_dict = {}
    for config in configs:
        config_dict[config.chave] = config.valor
    
    # Configurações padrão se não existirem
    defaults = {
        'nome_site': 'Nova Atalaia',
        'logo': 'logo.png',
        'favicon': 'favicon.ico',
        'cor_principal': '#1e3a8a',
        'cor_fundo': '#ffffff',
        'cor_texto': '#333333',
        'cor_botoes': '#3b82f6',
        'cor_links': '#1e40af',
        'fonte': 'Roboto',
        'texto_rodape': '© 2024 Nova Atalaia. Todos os direitos reservados.',
        'email_contato': 'contato@novaatalaia.com.br',
        'url_streaming': 'https://streaming.example.com/live',
        'whatsapp': '5511999999999',
        'facebook': 'https://facebook.com/novaatalaia',
        'instagram': 'https://instagram.com/novaatalaia',
        'youtube': 'https://youtube.com/novaatalaia',
        'css_custom': ''
    }
    
    for key, value in defaults.items():
        if key not in config_dict:
            config_dict[key] = value
    
    return config_dict

# Rotas principais
@app.route('/')
def index():
    config = get_site_config()
    programacao_atual = get_programacao_atual()
    return render_template('index.html', config=config, programacao_atual=programacao_atual)

@app.route('/a-radio')
def a_radio():
    config = get_site_config()
    return render_template('a-radio.html', config=config)

@app.route('/programacao')
def programacao():
    config = get_site_config()
    dias_semana = ['DOMINGO', 'SEGUNDA', 'TERÇA', 'QUARTA', 'QUINTA', 'SEXTA', 'SÁBADO']
    programacao_por_dia = {}
    
    for dia in dias_semana:
        programacao_por_dia[dia] = Programacao.query.filter_by(dia_semana=dia).order_by(Programacao.horario_inicio).all()
    
    return render_template('programacao.html', config=config, programacao=programacao_por_dia)

@app.route('/equipe')
def equipe():
    config = get_site_config()
    locutores = Locutor.query.all()
    return render_template('equipe.html', config=config, locutores=locutores)

@app.route('/contato')
def contato():
    config = get_site_config()
    return render_template('contato.html', config=config)

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
    programacao = Programacao.query.filter_by(dia_semana=dia_portugues).filter(
        Programacao.horario_inicio <= hora_atual,
        Programacao.horario_fim >= hora_atual
    ).first()
    
    return programacao

# Rotas da API
@app.route('/api/programacao-atual')
def api_programacao_atual():
    programacao = get_programacao_atual()
    if programacao:
        return jsonify({
            'titulo': programacao.titulo,
            'descricao': programacao.descricao,
            'imagem': programacao.imagem,
            'horario_inicio': programacao.horario_inicio.strftime('%H:%M'),
            'horario_fim': programacao.horario_fim.strftime('%H:%M')
        })
    return jsonify({'error': 'Nenhuma programação encontrada'})

# Rotas do admin
@app.route('/admin/login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        usuario = Usuario.query.filter_by(email=email).first()
        if usuario and check_password_hash(usuario.senha, senha):
            login_user(usuario)
            return redirect(url_for('admin_dashboard'))
        else:
            flash('Email ou senha incorretos', 'error')
    
    return render_template('admin/login.html')

@app.route('/admin/logout')
@login_required
def admin_logout():
    logout_user()
    return redirect(url_for('admin_login'))

@app.route('/admin')
@login_required
def admin_dashboard():
    config = get_site_config()
    total_programacao = Programacao.query.count()
    total_locutores = Locutor.query.count()
    total_banners = Banner.query.count()
    
    return render_template('admin/dashboard.html', 
                         config=config,
                         total_programacao=total_programacao,
                         total_locutores=total_locutores,
                         total_banners=total_banners)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Criar usuário admin padrão se não existir
        if not Usuario.query.filter_by(email='admin@novaatalaia.com.br').first():
            admin = Usuario(
                nome='Administrador',
                email='admin@novaatalaia.com.br',
                senha=generate_password_hash('admin123'),
                nivel='admin'
            )
            db.session.add(admin)
            db.session.commit()
    
    app.run(debug=True, host='0.0.0.0', port=5000) 