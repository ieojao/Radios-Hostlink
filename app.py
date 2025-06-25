from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import datetime, time
import os
from dotenv import load_dotenv
import json

# Carregar variáveis de ambiente
load_dotenv('config.env')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'sua-chave-secreta-aqui')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///radio.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Filtro personalizado para JSON
@app.template_filter('from_json')
def from_json_filter(value):
    if value:
        try:
            return json.loads(value)
        except:
            return {}
    return {}

# Filtro para converter quebras de linha em HTML
@app.template_filter('nl2br')
def nl2br_filter(value):
    if value:
        return value.replace('\n', '<br>')
    return value

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

class PaginaRadio(db.Model):
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
    estatisticas = db.Column(db.Text)  # JSON com estatísticas
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class PaginaEquipe(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    subtitulo = db.Column(db.String(300))
    descricao = db.Column(db.Text)
    mensagem_equipe = db.Column(db.Text)
    imagem_principal = db.Column(db.String(255))
    estatisticas_equipe = db.Column(db.Text)  # JSON com estatísticas da equipe
    areas_atuacao = db.Column(db.Text)  # JSON com áreas de atuação
    convite_equipe = db.Column(db.Text)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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
        'nome_site': 'Radios Hostlink',
        'logo': 'logo.png',
        'favicon': 'favicon.ico',
        'cor_principal': '#1e3a8a',
        'cor_fundo': '#ffffff',
        'cor_texto': '#333333',
        'cor_botoes': '#3b82f6',
        'cor_links': '#1e40af',
        'fonte': 'Roboto',
        'texto_rodape': '© 2024 Radios Hostlink. Todos os direitos reservados.',
        'email_contato': 'contato@radioshostlink.com.br',
        'url_streaming': 'https://streaming.example.com/live',
        'whatsapp': '5511999999999',
        'facebook': 'https://facebook.com/radioshostlink',
        'instagram': 'https://instagram.com/radioshostlink',
        'youtube': 'https://youtube.com/radioshostlink',
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
    pagina_radio = PaginaRadio.query.first()
    return render_template('a-radio.html', config=config, pagina_radio=pagina_radio)

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
    pagina_equipe = PaginaEquipe.query.first()
    return render_template('equipe.html', config=config, locutores=locutores, pagina_equipe=pagina_equipe)

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

# Rotas para gerenciar programação
@app.route('/admin/programacao')
@login_required
def admin_programacao():
    config = get_site_config()
    dias_semana = ['DOMINGO', 'SEGUNDA', 'TERÇA', 'QUARTA', 'QUINTA', 'SEXTA', 'SÁBADO']
    programacao_por_dia = {}
    
    for dia in dias_semana:
        programacao_por_dia[dia] = Programacao.query.filter_by(dia_semana=dia).order_by(Programacao.horario_inicio).all()
    
    return render_template('admin/programacao.html', config=config, programacao=programacao_por_dia, dias_semana=dias_semana)

@app.route('/admin/programacao/adicionar', methods=['GET', 'POST'])
@login_required
def admin_programacao_adicionar():
    config = get_site_config()
    
    if request.method == 'POST':
        try:
            programacao = Programacao(
                dia_semana=request.form['dia_semana'],
                horario_inicio=datetime.strptime(request.form['horario_inicio'], '%H:%M').time(),
                horario_fim=datetime.strptime(request.form['horario_fim'], '%H:%M').time(),
                titulo=request.form['titulo'],
                descricao=request.form['descricao'],
                imagem=request.form.get('imagem', '')
            )
            db.session.add(programacao)
            db.session.commit()
            flash('Programa adicionado com sucesso!', 'success')
            return redirect(url_for('admin_programacao'))
        except Exception as e:
            flash(f'Erro ao adicionar programa: {str(e)}', 'error')
    
    dias_semana = ['DOMINGO', 'SEGUNDA', 'TERÇA', 'QUARTA', 'QUINTA', 'SEXTA', 'SÁBADO']
    return render_template('admin/programacao_form.html', config=config, dias_semana=dias_semana)

@app.route('/admin/programacao/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_programacao_editar(id):
    config = get_site_config()
    programacao = Programacao.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            programacao.dia_semana = request.form['dia_semana']
            programacao.horario_inicio = datetime.strptime(request.form['horario_inicio'], '%H:%M').time()
            programacao.horario_fim = datetime.strptime(request.form['horario_fim'], '%H:%M').time()
            programacao.titulo = request.form['titulo']
            programacao.descricao = request.form['descricao']
            programacao.imagem = request.form.get('imagem', '')
            
            db.session.commit()
            flash('Programa atualizado com sucesso!', 'success')
            return redirect(url_for('admin_programacao'))
        except Exception as e:
            flash(f'Erro ao atualizar programa: {str(e)}', 'error')
    
    dias_semana = ['DOMINGO', 'SEGUNDA', 'TERÇA', 'QUARTA', 'QUINTA', 'SEXTA', 'SÁBADO']
    return render_template('admin/programacao_form.html', config=config, programacao=programacao, dias_semana=dias_semana)

@app.route('/admin/programacao/excluir/<int:id>', methods=['POST'])
@login_required
def admin_programacao_excluir(id):
    programacao = Programacao.query.get_or_404(id)
    try:
        db.session.delete(programacao)
        db.session.commit()
        flash('Programa excluído com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao excluir programa: {str(e)}', 'error')
    
    return redirect(url_for('admin_programacao'))

# Rotas para gerenciar locutores
@app.route('/admin/locutores')
@login_required
def admin_locutores():
    config = get_site_config()
    locutores = Locutor.query.order_by(Locutor.nome).all()
    return render_template('admin/locutores.html', config=config, locutores=locutores)

@app.route('/admin/locutores/adicionar', methods=['GET', 'POST'])
@login_required
def admin_locutores_adicionar():
    config = get_site_config()
    
    if request.method == 'POST':
        try:
            locutor = Locutor(
                nome=request.form['nome'],
                foto=request.form.get('foto', ''),
                bio=request.form.get('bio', ''),
                redes_sociais=request.form.get('redes_sociais', '')
            )
            db.session.add(locutor)
            db.session.commit()
            flash('Locutor adicionado com sucesso!', 'success')
            return redirect(url_for('admin_locutores'))
        except Exception as e:
            flash(f'Erro ao adicionar locutor: {str(e)}', 'error')
    
    return render_template('admin/locutores_form.html', config=config)

@app.route('/admin/locutores/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_locutores_editar(id):
    config = get_site_config()
    locutor = Locutor.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            locutor.nome = request.form['nome']
            locutor.foto = request.form.get('foto', '')
            locutor.bio = request.form.get('bio', '')
            locutor.redes_sociais = request.form.get('redes_sociais', '')
            
            db.session.commit()
            flash('Locutor atualizado com sucesso!', 'success')
            return redirect(url_for('admin_locutores'))
        except Exception as e:
            flash(f'Erro ao atualizar locutor: {str(e)}', 'error')
    
    return render_template('admin/locutores_form.html', config=config, locutor=locutor)

@app.route('/admin/locutores/excluir/<int:id>', methods=['POST'])
@login_required
def admin_locutores_excluir(id):
    locutor = Locutor.query.get_or_404(id)
    try:
        db.session.delete(locutor)
        db.session.commit()
        flash('Locutor excluído com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao excluir locutor: {str(e)}', 'error')
    
    return redirect(url_for('admin_locutores'))

# Rotas para gerenciar banners
@app.route('/admin/banners')
@login_required
def admin_banners():
    config = get_site_config()
    banners = Banner.query.order_by(Banner.criado_em.desc()).all()
    return render_template('admin/banners.html', config=config, banners=banners)

@app.route('/admin/banners/adicionar', methods=['GET', 'POST'])
@login_required
def admin_banners_adicionar():
    config = get_site_config()
    
    if request.method == 'POST':
        try:
            banner = Banner(
                titulo=request.form['titulo'],
                imagem=request.form.get('imagem', ''),
                link=request.form.get('link', '')
            )
            db.session.add(banner)
            db.session.commit()
            flash('Banner adicionado com sucesso!', 'success')
            return redirect(url_for('admin_banners'))
        except Exception as e:
            flash(f'Erro ao adicionar banner: {str(e)}', 'error')
    
    return render_template('admin/banners_form.html', config=config)

@app.route('/admin/banners/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_banners_editar(id):
    config = get_site_config()
    banner = Banner.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            banner.titulo = request.form['titulo']
            banner.imagem = request.form.get('imagem', '')
            banner.link = request.form.get('link', '')
            
            db.session.commit()
            flash('Banner atualizado com sucesso!', 'success')
            return redirect(url_for('admin_banners'))
        except Exception as e:
            flash(f'Erro ao atualizar banner: {str(e)}', 'error')
    
    return render_template('admin/banners_form.html', config=config, banner=banner)

@app.route('/admin/banners/excluir/<int:id>', methods=['POST'])
@login_required
def admin_banners_excluir(id):
    banner = Banner.query.get_or_404(id)
    try:
        db.session.delete(banner)
        db.session.commit()
        flash('Banner excluído com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao excluir banner: {str(e)}', 'error')
    
    return redirect(url_for('admin_banners'))

# Rotas para gerenciar configurações
@app.route('/admin/configuracoes', methods=['GET', 'POST'])
@login_required
def admin_configuracoes():
    config = get_site_config()
    
    if request.method == 'POST':
        try:
            # Atualizar configurações
            for key, value in request.form.items():
                if key != 'csrf_token':
                    config_existente = Configuracao.query.filter_by(chave=key).first()
                    if config_existente:
                        config_existente.valor = value
                    else:
                        nova_config = Configuracao(chave=key, valor=value)
                        db.session.add(nova_config)
            
            db.session.commit()
            flash('Configurações atualizadas com sucesso!', 'success')
            return redirect(url_for('admin_configuracoes'))
        except Exception as e:
            flash(f'Erro ao atualizar configurações: {str(e)}', 'error')
    
    return render_template('admin/configuracoes.html', config=config)

# Rotas para gerenciar usuários
@app.route('/admin/usuarios')
@login_required
def admin_usuarios():
    config = get_site_config()
    usuarios = Usuario.query.order_by(Usuario.criado_em.desc()).all()
    return render_template('admin/usuarios.html', config=config, usuarios=usuarios)

@app.route('/admin/usuarios/adicionar', methods=['GET', 'POST'])
@login_required
def admin_usuarios_adicionar():
    config = get_site_config()
    
    if request.method == 'POST':
        try:
            # Verificar se email já existe
            if Usuario.query.filter_by(email=request.form['email']).first():
                flash('Email já cadastrado!', 'error')
                return render_template('admin/usuarios_form.html', config=config)
            
            usuario = Usuario(
                nome=request.form['nome'],
                email=request.form['email'],
                senha=generate_password_hash(request.form['senha']),
                nivel=request.form.get('nivel', 'admin')
            )
            db.session.add(usuario)
            db.session.commit()
            flash('Usuário adicionado com sucesso!', 'success')
            return redirect(url_for('admin_usuarios'))
        except Exception as e:
            flash(f'Erro ao adicionar usuário: {str(e)}', 'error')
    
    return render_template('admin/usuarios_form.html', config=config)

@app.route('/admin/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_usuarios_editar(id):
    config = get_site_config()
    usuario = Usuario.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Verificar se email já existe (exceto para o próprio usuário)
            email_existente = Usuario.query.filter_by(email=request.form['email']).first()
            if email_existente and email_existente.id != usuario.id:
                flash('Email já cadastrado!', 'error')
                return render_template('admin/usuarios_form.html', config=config, usuario=usuario)
            
            usuario.nome = request.form['nome']
            usuario.email = request.form['email']
            usuario.nivel = request.form.get('nivel', 'admin')
            
            # Atualizar senha apenas se fornecida
            if request.form.get('senha'):
                usuario.senha = generate_password_hash(request.form['senha'])
            
            db.session.commit()
            flash('Usuário atualizado com sucesso!', 'success')
            return redirect(url_for('admin_usuarios'))
        except Exception as e:
            flash(f'Erro ao atualizar usuário: {str(e)}', 'error')
    
    return render_template('admin/usuarios_form.html', config=config, usuario=usuario)

@app.route('/admin/usuarios/excluir/<int:id>', methods=['POST'])
@login_required
def admin_usuarios_excluir(id):
    usuario = Usuario.query.get_or_404(id)
    
    # Não permitir excluir o próprio usuário
    if usuario.id == current_user.id:
        flash('Você não pode excluir sua própria conta!', 'error')
        return redirect(url_for('admin_usuarios'))
    
    try:
        db.session.delete(usuario)
        db.session.commit()
        flash('Usuário excluído com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao excluir usuário: {str(e)}', 'error')
    
    return redirect(url_for('admin_usuarios'))

# Rotas para gerenciar página "A Rádio"
@app.route('/admin/a-radio', methods=['GET', 'POST'])
@login_required
def admin_a_radio():
    config = get_site_config()
    pagina_radio = PaginaRadio.query.first()
    
    if request.method == 'POST':
        try:
            if pagina_radio:
                # Atualizar página existente
                pagina_radio.titulo = request.form['titulo']
                pagina_radio.subtitulo = request.form.get('subtitulo', '')
                pagina_radio.descricao = request.form.get('descricao', '')
                pagina_radio.historia = request.form.get('historia', '')
                pagina_radio.missao = request.form.get('missao', '')
                pagina_radio.visao = request.form.get('visao', '')
                pagina_radio.valores = request.form.get('valores', '')
                pagina_radio.imagem_principal = request.form.get('imagem_principal', '')
                pagina_radio.imagem_historia = request.form.get('imagem_historia', '')
                
                # Processar estatísticas
                estatisticas = {}
                for i in range(1, 5):  # Máximo 4 estatísticas
                    titulo = request.form.get(f'estatistica_{i}_titulo', '').strip()
                    valor = request.form.get(f'estatistica_{i}_valor', '').strip()
                    if titulo and valor:
                        estatisticas[f'estatistica_{i}'] = {'titulo': titulo, 'valor': valor}
                
                pagina_radio.estatisticas = json.dumps(estatisticas)
            else:
                # Criar nova página
                estatisticas = {}
                for i in range(1, 5):
                    titulo = request.form.get(f'estatistica_{i}_titulo', '').strip()
                    valor = request.form.get(f'estatistica_{i}_valor', '').strip()
                    if titulo and valor:
                        estatisticas[f'estatistica_{i}'] = {'titulo': titulo, 'valor': valor}
                
                pagina_radio = PaginaRadio(
                    titulo=request.form['titulo'],
                    subtitulo=request.form.get('subtitulo', ''),
                    descricao=request.form.get('descricao', ''),
                    historia=request.form.get('historia', ''),
                    missao=request.form.get('missao', ''),
                    visao=request.form.get('visao', ''),
                    valores=request.form.get('valores', ''),
                    imagem_principal=request.form.get('imagem_principal', ''),
                    imagem_historia=request.form.get('imagem_historia', ''),
                    estatisticas=json.dumps(estatisticas)
                )
                db.session.add(pagina_radio)
            
            db.session.commit()
            flash('Página "A Rádio" atualizada com sucesso!', 'success')
            return redirect(url_for('admin_a_radio'))
        except Exception as e:
            flash(f'Erro ao atualizar página: {str(e)}', 'error')
    
    return render_template('admin/a_radio.html', config=config, pagina_radio=pagina_radio)

# Rotas para gerenciar página "Equipe"
@app.route('/admin/equipe', methods=['GET', 'POST'])
@login_required
def admin_equipe():
    config = get_site_config()
    pagina_equipe = PaginaEquipe.query.first()
    
    if request.method == 'POST':
        try:
            if pagina_equipe:
                # Atualizar página existente
                pagina_equipe.titulo = request.form['titulo']
                pagina_equipe.subtitulo = request.form.get('subtitulo', '')
                pagina_equipe.descricao = request.form.get('descricao', '')
                pagina_equipe.mensagem_equipe = request.form.get('mensagem_equipe', '')
                pagina_equipe.imagem_principal = request.form.get('imagem_principal', '')
                pagina_equipe.convite_equipe = request.form.get('convite_equipe', '')
                
                # Processar estatísticas da equipe
                estatisticas_equipe = {}
                for i in range(1, 5):  # Máximo 4 estatísticas
                    titulo = request.form.get(f'estatistica_equipe_{i}_titulo', '').strip()
                    valor = request.form.get(f'estatistica_equipe_{i}_valor', '').strip()
                    if titulo and valor:
                        estatisticas_equipe[f'estatistica_equipe_{i}'] = {'titulo': titulo, 'valor': valor}
                
                pagina_equipe.estatisticas_equipe = json.dumps(estatisticas_equipe)
                
                # Processar áreas de atuação
                areas_atuacao = {}
                for i in range(1, 7):  # Máximo 6 áreas
                    titulo = request.form.get(f'area_{i}_titulo', '').strip()
                    descricao = request.form.get(f'area_{i}_descricao', '').strip()
                    if titulo and descricao:
                        areas_atuacao[f'area_{i}'] = {'titulo': titulo, 'descricao': descricao}
                
                pagina_equipe.areas_atuacao = json.dumps(areas_atuacao)
            else:
                # Criar nova página
                estatisticas_equipe = {}
                for i in range(1, 5):
                    titulo = request.form.get(f'estatistica_equipe_{i}_titulo', '').strip()
                    valor = request.form.get(f'estatistica_equipe_{i}_valor', '').strip()
                    if titulo and valor:
                        estatisticas_equipe[f'estatistica_equipe_{i}'] = {'titulo': titulo, 'valor': valor}
                
                areas_atuacao = {}
                for i in range(1, 7):
                    titulo = request.form.get(f'area_{i}_titulo', '').strip()
                    descricao = request.form.get(f'area_{i}_descricao', '').strip()
                    if titulo and descricao:
                        areas_atuacao[f'area_{i}'] = {'titulo': titulo, 'descricao': descricao}
                
                pagina_equipe = PaginaEquipe(
                    titulo=request.form['titulo'],
                    subtitulo=request.form.get('subtitulo', ''),
                    descricao=request.form.get('descricao', ''),
                    mensagem_equipe=request.form.get('mensagem_equipe', ''),
                    imagem_principal=request.form.get('imagem_principal', ''),
                    estatisticas_equipe=json.dumps(estatisticas_equipe),
                    areas_atuacao=json.dumps(areas_atuacao),
                    convite_equipe=request.form.get('convite_equipe', '')
                )
                db.session.add(pagina_equipe)
            
            db.session.commit()
            flash('Página "Equipe" atualizada com sucesso!', 'success')
            return redirect(url_for('admin_equipe'))
        except Exception as e:
            flash(f'Erro ao atualizar página: {str(e)}', 'error')
    
    return render_template('admin/equipe.html', config=config, pagina_equipe=pagina_equipe)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        
        # Criar usuário admin padrão se não existir
        if not Usuario.query.filter_by(email='admin@radioshostlink.com.br').first():
            admin = Usuario(
                nome='Administrador',
                email='admin@radioshostlink.com.br',
                senha=generate_password_hash('admin123'),
                nivel='admin'
            )
            db.session.add(admin)
            db.session.commit()
        
        # Criar página "A Rádio" padrão se não existir
        if not PaginaRadio.query.first():
            pagina_radio = PaginaRadio(
                titulo='Radios Hostlink',
                subtitulo='Conectando pessoas através da música e informação',
                descricao='Somos uma rádio comprometida em levar entretenimento de qualidade, notícias relevantes e música que inspira. Nossa missão é ser a voz da comunidade, conectando pessoas e criando momentos especiais através do rádio.',
                historia='Fundada com o propósito de servir a comunidade, nossa rádio nasceu da paixão pela música e pelo jornalismo. Ao longo dos anos, construímos uma história de dedicação e compromisso com nossos ouvintes, sempre buscando inovar e oferecer o melhor conteúdo.',
                missao='Levar entretenimento de qualidade, informação relevante e música que inspire e conecte pessoas, sendo uma referência em comunicação e cultura em nossa região.',
                visao='Ser reconhecida como a rádio mais querida e confiável da região, referência em qualidade de programação e compromisso com a comunidade.',
                valores='Qualidade\nCompromisso\nInovação\nComunidade\nTransparência',
                imagem_principal='',
                imagem_historia='',
                estatisticas=json.dumps({
                    'estatistica_1': {'titulo': 'Anos no Ar', 'valor': '25'},
                    'estatistica_2': {'titulo': 'Ouvintes Diários', 'valor': '50000'},
                    'estatistica_3': {'titulo': 'Programas', 'valor': '15'},
                    'estatistica_4': {'titulo': 'Locutores', 'valor': '8'}
                })
            )
            db.session.add(pagina_radio)
            db.session.commit()
        
        # Criar página "Equipe" padrão se não existir
        if not PaginaEquipe.query.first():
            pagina_equipe = PaginaEquipe(
                titulo='Nossa Equipe',
                subtitulo='Profissionais apaixonados por rádio e comunicação',
                descricao='Nossa equipe é formada por profissionais dedicados e apaixonados por rádio. Cada membro contribui com sua expertise para criar uma programação de qualidade e manter a excelência em tudo que fazemos.',
                mensagem_equipe='Somos uma equipe unida pela paixão pelo rádio e pelo compromisso com a qualidade. Cada dia é uma nova oportunidade de conectar com nossos ouvintes e fazer a diferença na comunidade através da comunicação.',
                imagem_principal='',
                estatisticas_equipe=json.dumps({
                    'estatistica_equipe_1': {'titulo': 'Membros da Equipe', 'valor': '12'},
                    'estatistica_equipe_2': {'titulo': 'Anos de Experiência', 'valor': '150'},
                    'estatistica_equipe_3': {'titulo': 'Especialidades', 'valor': '8'},
                    'estatistica_equipe_4': {'titulo': 'Prêmios', 'valor': '5'}
                }),
                areas_atuacao=json.dumps({
                    'area_1': {'titulo': 'Locução', 'descricao': 'Profissionais responsáveis pela apresentação dos programas e interação com o público.'},
                    'area_2': {'titulo': 'Produção', 'descricao': 'Equipe que cuida da produção de conteúdo, roteiros e coordenação dos programas.'},
                    'area_3': {'titulo': 'Técnica', 'descricao': 'Especialistas em equipamentos, transmissão e qualidade de áudio.'},
                    'area_4': {'titulo': 'Jornalismo', 'descricao': 'Repórteres e editores que garantem informações precisas e relevantes.'},
                    'area_5': {'titulo': 'Marketing', 'descricao': 'Profissionais que cuidam da divulgação e relacionamento com parceiros.'},
                    'area_6': {'titulo': 'Administrativo', 'descricao': 'Equipe que gerencia recursos e garante o funcionamento da rádio.'}
                }),
                convite_equipe='Estamos sempre em busca de talentos apaixonados por rádio e comunicação. Se você tem interesse em fazer parte da nossa equipe, entre em contato conosco! Oferecemos oportunidades de crescimento e um ambiente colaborativo.'
            )
            db.session.add(pagina_equipe)
            db.session.commit()
    
    app.run(debug=True, host='0.0.0.0', port=5000) 