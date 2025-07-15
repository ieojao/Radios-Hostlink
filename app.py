from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from datetime import datetime, time
import os
from dotenv import load_dotenv
import json
import uuid

# Carregar variáveis de ambiente
load_dotenv('config.env')

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'sua-chave-secreta-aqui')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///radio.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Configurações para upload de arquivos
app.config['UPLOAD_FOLDER'] = 'static/uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max file size
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'webp', 'ico'}

# Criar pasta de uploads se não existir
os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)

def allowed_file(filename):
    """Verifica se a extensão do arquivo é permitida"""
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def save_uploaded_file(file, folder=''):
    """Salva um arquivo enviado e retorna o caminho"""
    if file and allowed_file(file.filename):
        # Gerar nome único para o arquivo
        filename = secure_filename(file.filename)
        unique_filename = f"{uuid.uuid4().hex}_{filename}"
        
        # Criar pasta se não existir
        upload_path = os.path.join(app.config['UPLOAD_FOLDER'], folder)
        os.makedirs(upload_path, exist_ok=True)
        
        # Salvar arquivo
        file_path = os.path.join(upload_path, unique_filename)
        file.save(file_path)
        
        # Retornar caminho relativo para o banco de dados (com /static/ no início)
        return f"/static/uploads/{folder}/{unique_filename}"
    return None

def delete_uploaded_file(file_path):
    """Deleta um arquivo enviado"""
    if file_path and not file_path.startswith('http'):
        try:
            # Remover /static/ do início se existir
            if file_path.startswith('/static/'):
                file_path = file_path[8:]  # Remove '/static/'
            
            full_path = os.path.join('static', file_path)
            if os.path.exists(full_path):
                os.remove(full_path)
                return True
        except Exception as e:
            print(f"Erro ao deletar arquivo {file_path}: {e}")
    return False

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

class Destaque(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    imagem = db.Column(db.String(255))
    link = db.Column(db.String(255))
    ordem = db.Column(db.Integer, default=0)  # Para controlar a ordem de exibição
    ativo = db.Column(db.Boolean, default=True)
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

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

class MensagemContato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), nullable=False)
    telefone = db.Column(db.String(20))
    assunto = db.Column(db.String(200))
    mensagem = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default='não_lida')  # não_lida, lida, respondida
    criado_em = db.Column(db.DateTime, default=datetime.utcnow)

class PaginaContato(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    titulo = db.Column(db.String(200), nullable=False)
    subtitulo = db.Column(db.String(300))
    descricao = db.Column(db.Text)
    telefone_principal = db.Column(db.String(20))
    telefone_secundario = db.Column(db.String(20))
    email_contato = db.Column(db.String(100))
    endereco = db.Column(db.Text)
    horario_funcionamento = db.Column(db.Text)
    redes_sociais = db.Column(db.Text)  # JSON com redes sociais
    mapa_embed = db.Column(db.Text)  # Código embed do Google Maps
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
        'css_custom': '',
        'programacao_padrao_titulo': 'Programação musical',
        'programacao_padrao_descricao': 'Música gospel 24 horas por dia',
        'programacao_padrao_horario': '24h - Ao vivo',
        'programacao_rolando_agora': 'ROLANDO AGORA'
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
    destaques = Destaque.query.filter_by(ativo=True).order_by(Destaque.ordem).all()
    return render_template('index.html', config=config, programacao_atual=programacao_atual, destaques=destaques)

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
    pagina_contato = PaginaContato.query.first()
    return render_template('contato.html', config=config, pagina_contato=pagina_contato)

@app.route('/contato/enviar', methods=['POST'])
def enviar_mensagem():
    try:
        mensagem = MensagemContato(
            nome=request.form['nome'],
            email=request.form['email'],
            telefone=request.form.get('telefone', ''),
            assunto=request.form.get('assunto', ''),
            mensagem=request.form['mensagem']
        )
        db.session.add(mensagem)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Mensagem enviada com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': 'Erro ao enviar mensagem. Tente novamente.'})

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

@app.route('/api/programacao-dia/<dia>')
def api_programacao_dia(dia):
    """API para buscar programações de um dia específico"""
    try:
        # Validar dia da semana
        dias_validos = ['DOMINGO', 'SEGUNDA', 'TERÇA', 'QUARTA', 'QUINTA', 'SEXTA', 'SÁBADO']
        if dia not in dias_validos:
            return jsonify({'error': 'Dia da semana inválido'}), 400
        
        # Buscar programações do dia
        programacoes = Programacao.query.filter_by(dia_semana=dia).order_by(Programacao.horario_inicio).all()
        
        # Verificar qual programa está ao vivo
        agora = datetime.now()
        hora_atual = agora.time()
        
        programacoes_json = []
        for programa in programacoes:
            is_atual = (programa.horario_inicio <= hora_atual and programa.horario_fim >= hora_atual)
            
            programacoes_json.append({
                'id': programa.id,
                'titulo': programa.titulo,
                'descricao': programa.descricao,
                'horario_inicio': programa.horario_inicio.strftime('%H:%M'),
                'horario_fim': programa.horario_fim.strftime('%H:%M'),
                'imagem': programa.imagem,
                'is_atual': is_atual
            })
        
        return jsonify({
            'dia': dia,
            'programacoes': programacoes_json
        })
        
    except Exception as e:
        return jsonify({
            'error': f'Erro ao buscar programações: {str(e)}'
        }), 500

@app.route('/api/streaming-url')
def api_streaming_url():
    """API para fornecer a URL de streaming do rádio"""
    try:
        # Buscar URL de streaming das configurações
        streaming_config = Configuracao.query.filter_by(chave='streaming_url').first()
        
        if streaming_config and streaming_config.valor:
            return jsonify({
                'streaming_url': streaming_config.valor,
                'status': 'success'
            })
        else:
            # Fallback para variável de ambiente
            streaming_url = os.getenv('STREAMING_URL')
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

@app.route('/api/player-stats')
def api_player_stats():
    """API para estatísticas do player (para futuras implementações)"""
    try:
        # Aqui você pode adicionar estatísticas como:
        # - Número de ouvintes ativos
        # - Música atual (se disponível via metadados)
        # - Status do servidor de streaming
        
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
    total_mensagens = MensagemContato.query.count()
    mensagens_nao_lidas = MensagemContato.query.filter_by(status='não_lida').count()
    
    return render_template('admin/dashboard.html', 
                         config=config,
                         total_programacao=total_programacao,
                         total_locutores=total_locutores,
                         total_banners=total_banners,
                         total_mensagens=total_mensagens,
                         mensagens_nao_lidas=mensagens_nao_lidas)

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
            # Processar upload de imagem
            imagem_path = None
            if 'imagem_arquivo' in request.files:
                file = request.files['imagem_arquivo']
                if file and file.filename:
                    imagem_path = save_uploaded_file(file, 'programacao')
            
            # Se não foi enviado arquivo, usar URL se fornecida
            if not imagem_path:
                imagem_path = request.form.get('imagem_url', '')
            
            programacao = Programacao(
                dia_semana=request.form['dia_semana'],
                horario_inicio=datetime.strptime(request.form['horario_inicio'], '%H:%M').time(),
                horario_fim=datetime.strptime(request.form['horario_fim'], '%H:%M').time(),
                titulo=request.form['titulo'],
                descricao=request.form.get('descricao', ''),
                imagem=imagem_path
            )
            db.session.add(programacao)
            db.session.commit()
            flash('Programa adicionado com sucesso!', 'success')
            return redirect(url_for('admin_programacao'))
        except Exception as e:
            flash(f'Erro ao adicionar programa: {str(e)}', 'error')
    
    return render_template('admin/programacao_form.html', config=config)

@app.route('/admin/programacao/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_programacao_editar(id):
    config = get_site_config()
    programacao = Programacao.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Processar upload de imagem
            imagem_path = programacao.imagem  # Manter imagem atual por padrão
            if 'imagem_arquivo' in request.files:
                file = request.files['imagem_arquivo']
                if file and file.filename:
                    # Deletar imagem antiga se existir
                    if programacao.imagem:
                        delete_uploaded_file(programacao.imagem)
                    # Salvar nova imagem
                    imagem_path = save_uploaded_file(file, 'programacao')
            
            # Se não foi enviado arquivo, usar URL se fornecida
            if not imagem_path or (imagem_path == programacao.imagem and request.form.get('imagem_url')):
                imagem_path = request.form.get('imagem_url', '')
            
            programacao.dia_semana = request.form['dia_semana']
            programacao.horario_inicio = datetime.strptime(request.form['horario_inicio'], '%H:%M').time()
            programacao.horario_fim = datetime.strptime(request.form['horario_fim'], '%H:%M').time()
            programacao.titulo = request.form['titulo']
            programacao.descricao = request.form.get('descricao', '')
            programacao.imagem = imagem_path
            
            db.session.commit()
            flash('Programa atualizado com sucesso!', 'success')
            return redirect(url_for('admin_programacao'))
        except Exception as e:
            flash(f'Erro ao atualizar programa: {str(e)}', 'error')
    
    return render_template('admin/programacao_form.html', config=config, programacao=programacao)

@app.route('/admin/programacao/excluir/<int:id>', methods=['POST'])
@login_required
def admin_programacao_excluir(id):
    programacao = Programacao.query.get_or_404(id)
    try:
        # Deletar arquivo de imagem se existir
        if programacao.imagem:
            delete_uploaded_file(programacao.imagem)
        
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
            # Processar upload de foto
            foto_path = None
            if 'foto_arquivo' in request.files:
                file = request.files['foto_arquivo']
                if file and file.filename:
                    foto_path = save_uploaded_file(file, 'locutores')
            
            # Se não foi enviado arquivo, usar URL se fornecida
            if not foto_path:
                foto_path = request.form.get('foto_url', '')
            
            locutor = Locutor(
                nome=request.form['nome'],
                foto=foto_path,
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
            # Processar upload de foto
            foto_path = locutor.foto  # Manter foto atual por padrão
            if 'foto_arquivo' in request.files:
                file = request.files['foto_arquivo']
                if file and file.filename:
                    # Deletar foto antiga se existir
                    if locutor.foto:
                        delete_uploaded_file(locutor.foto)
                    # Salvar nova foto
                    foto_path = save_uploaded_file(file, 'locutores')
            
            # Se não foi enviado arquivo, usar URL se fornecida
            if not foto_path or (foto_path == locutor.foto and request.form.get('foto_url')):
                foto_path = request.form.get('foto_url', '')
            
            locutor.nome = request.form['nome']
            locutor.foto = foto_path
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
        # Deletar arquivo de foto se existir
        if locutor.foto:
            delete_uploaded_file(locutor.foto)
        
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
            # Processar upload de imagem
            imagem_path = None
            if 'imagem_arquivo' in request.files:
                file = request.files['imagem_arquivo']
                if file and file.filename:
                    imagem_path = save_uploaded_file(file, 'banners')
            
            # Se não foi enviado arquivo, usar URL se fornecida
            if not imagem_path:
                imagem_path = request.form.get('imagem_url', '')
            
            banner = Banner(
                titulo=request.form['titulo'],
                imagem=imagem_path,
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
            # Processar upload de imagem
            imagem_path = banner.imagem  # Manter imagem atual por padrão
            if 'imagem_arquivo' in request.files:
                file = request.files['imagem_arquivo']
                if file and file.filename:
                    # Deletar imagem antiga se existir
                    if banner.imagem:
                        delete_uploaded_file(banner.imagem)
                    # Salvar nova imagem
                    imagem_path = save_uploaded_file(file, 'banners')
            
            # Se não foi enviado arquivo, usar URL se fornecida
            if not imagem_path or (imagem_path == banner.imagem and request.form.get('imagem_url')):
                imagem_path = request.form.get('imagem_url', '')
            
            banner.titulo = request.form['titulo']
            banner.imagem = imagem_path
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
        # Deletar arquivo de imagem se existir
        if banner.imagem:
            delete_uploaded_file(banner.imagem)
        
        db.session.delete(banner)
        db.session.commit()
        flash('Banner excluído com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao excluir banner: {str(e)}', 'error')
    
    return redirect(url_for('admin_banners'))

# Rotas para gerenciar destaques
@app.route('/admin/destaques')
@login_required
def admin_destaques():
    config = get_site_config()
    destaques = Destaque.query.order_by(Destaque.ordem).all()
    return render_template('admin/destaques.html', config=config, destaques=destaques)

@app.route('/admin/destaques/adicionar', methods=['GET', 'POST'])
@login_required
def admin_destaques_adicionar():
    config = get_site_config()
    
    if request.method == 'POST':
        try:
            # Processar upload de imagem
            imagem_path = None
            if 'imagem_arquivo' in request.files:
                file = request.files['imagem_arquivo']
                if file and file.filename:
                    imagem_path = save_uploaded_file(file, 'destaques')
            
            # Se não foi enviado arquivo, usar URL se fornecida
            if not imagem_path:
                imagem_path = request.form.get('imagem_url', '')
            
            # Determinar ordem (última + 1)
            ultima_ordem = db.session.query(db.func.max(Destaque.ordem)).scalar() or 0
            
            destaque = Destaque(
                titulo=request.form['titulo'],
                descricao=request.form.get('descricao', ''),
                imagem=imagem_path,
                link=request.form.get('link', ''),
                ordem=ultima_ordem + 1,
                ativo=request.form.get('ativo', False) == 'on'
            )
            db.session.add(destaque)
            db.session.commit()
            flash('Destaque adicionado com sucesso!', 'success')
            return redirect(url_for('admin_destaques'))
        except Exception as e:
            flash(f'Erro ao adicionar destaque: {str(e)}', 'error')
    
    return render_template('admin/destaques_form.html', config=config)

@app.route('/admin/destaques/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def admin_destaques_editar(id):
    config = get_site_config()
    destaque = Destaque.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            # Processar upload de imagem
            imagem_path = destaque.imagem  # Manter imagem atual por padrão
            if 'imagem_arquivo' in request.files:
                file = request.files['imagem_arquivo']
                if file and file.filename:
                    # Deletar imagem antiga se existir
                    if destaque.imagem:
                        delete_uploaded_file(destaque.imagem)
                    # Salvar nova imagem
                    imagem_path = save_uploaded_file(file, 'destaques')
            
            # Se não foi enviado arquivo, usar URL se fornecida
            if not imagem_path or (imagem_path == destaque.imagem and request.form.get('imagem_url')):
                imagem_path = request.form.get('imagem_url', '')
            
            destaque.titulo = request.form['titulo']
            destaque.descricao = request.form.get('descricao', '')
            destaque.imagem = imagem_path
            destaque.link = request.form.get('link', '')
            destaque.ordem = int(request.form.get('ordem', 0))
            destaque.ativo = request.form.get('ativo', False) == 'on'
            
            db.session.commit()
            flash('Destaque atualizado com sucesso!', 'success')
            return redirect(url_for('admin_destaques'))
        except Exception as e:
            flash(f'Erro ao atualizar destaque: {str(e)}', 'error')
    
    return render_template('admin/destaques_form.html', config=config, destaque=destaque)

@app.route('/admin/destaques/excluir/<int:id>', methods=['POST'])
@login_required
def admin_destaques_excluir(id):
    destaque = Destaque.query.get_or_404(id)
    try:
        # Deletar arquivo de imagem se existir
        if destaque.imagem:
            delete_uploaded_file(destaque.imagem)
        
        db.session.delete(destaque)
        db.session.commit()
        flash('Destaque excluído com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao excluir destaque: {str(e)}', 'error')
    
    return redirect(url_for('admin_destaques'))

@app.route('/admin/destaques/ordem', methods=['POST'])
@login_required
def admin_destaques_ordem():
    """Atualizar ordem dos destaques via AJAX"""
    try:
        dados = request.get_json()
        for item in dados:
            destaque = Destaque.query.get(item['id'])
            if destaque:
                destaque.ordem = item['ordem']
        
        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# Rotas para gerenciar configurações
@app.route('/admin/configuracoes', methods=['GET', 'POST'])
@login_required
def admin_configuracoes():
    config = get_site_config()
    
    if request.method == 'POST':
        try:
            # Processar upload de logo
            logo_path = config.get('logo', '')
            if 'logo_arquivo' in request.files:
                file = request.files['logo_arquivo']
                if file and file.filename:
                    # Deletar logo antiga se existir
                    if logo_path and logo_path.startswith('/static/uploads/'):
                        delete_uploaded_file(logo_path)
                    # Salvar nova logo
                    logo_path = save_uploaded_file(file, 'config')
            
            # Se não foi enviado arquivo, usar URL se fornecida
            if not logo_path or (logo_path == config.get('logo', '') and request.form.get('logo_url')):
                logo_path = request.form.get('logo_url', '')
            
            # Processar upload de favicon
            favicon_path = config.get('favicon', '')
            if 'favicon_arquivo' in request.files:
                file = request.files['favicon_arquivo']
                if file and file.filename:
                    # Deletar favicon antigo se existir
                    if favicon_path and favicon_path.startswith('/static/uploads/'):
                        delete_uploaded_file(favicon_path)
                    # Salvar novo favicon
                    favicon_path = save_uploaded_file(file, 'config')
            
            # Se não foi enviado arquivo, usar URL se fornecida
            if not favicon_path or (favicon_path == config.get('favicon', '') and request.form.get('favicon_url')):
                favicon_path = request.form.get('favicon_url', '')
            
            # Atualizar configurações
            configuracoes_para_atualizar = {
                'nome_site': request.form.get('nome_site', ''),
                'email_contato': request.form.get('email_contato', ''),
                'texto_rodape': request.form.get('texto_rodape', ''),
                'url_streaming': request.form.get('url_streaming', ''),
                'whatsapp': request.form.get('whatsapp', ''),
                'facebook': request.form.get('facebook', ''),
                'instagram': request.form.get('instagram', ''),
                'youtube': request.form.get('youtube', ''),
                'cor_principal': request.form.get('cor_principal', '#007bff'),
                'cor_fundo': request.form.get('cor_fundo', '#ffffff'),
                'cor_texto': request.form.get('cor_texto', '#333333'),
                'cor_botoes': request.form.get('cor_botoes', '#007bff'),
                'cor_links': request.form.get('cor_links', '#007bff'),
                'fonte': request.form.get('fonte', 'Roboto'),
                'css_custom': request.form.get('css_custom', ''),
                'programacao_rolando_agora': request.form.get('programacao_rolando_agora', 'ROLANDO AGORA'),
                'programacao_padrao_titulo': request.form.get('programacao_padrao_titulo', 'Programação musical'),
                'programacao_padrao_descricao': request.form.get('programacao_padrao_descricao', 'Música gospel 24 horas por dia'),
                'programacao_padrao_horario': request.form.get('programacao_padrao_horario', '24h - Ao vivo'),
                'logo': logo_path,
                'favicon': favicon_path
            }
            
            for key, value in configuracoes_para_atualizar.items():
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
            if not pagina_equipe:
                pagina_equipe = PaginaEquipe()
                db.session.add(pagina_equipe)
            
            pagina_equipe.titulo = request.form['titulo']
            pagina_equipe.subtitulo = request.form['subtitulo']
            pagina_equipe.descricao = request.form['descricao']
            pagina_equipe.mensagem_equipe = request.form['mensagem_equipe']
            pagina_equipe.imagem_principal = request.form.get('imagem_principal', '')
            pagina_equipe.estatisticas_equipe = request.form['estatisticas_equipe']
            pagina_equipe.areas_atuacao = request.form['areas_atuacao']
            pagina_equipe.convite_equipe = request.form['convite_equipe']
            
            db.session.commit()
            flash('Página de equipe atualizada com sucesso!', 'success')
            return redirect(url_for('admin_equipe'))
        except Exception as e:
            flash(f'Erro ao atualizar página de equipe: {str(e)}', 'error')
    
    return render_template('admin/equipe.html', config=config, pagina_equipe=pagina_equipe)

# Rotas para gerenciar mensagens de contato
@app.route('/admin/mensagens')
@login_required
def admin_mensagens():
    config = get_site_config()
    mensagens = MensagemContato.query.order_by(MensagemContato.criado_em.desc()).all()
    return render_template('admin/mensagens.html', config=config, mensagens=mensagens)

@app.route('/admin/mensagens/<int:id>')
@login_required
def admin_mensagem_detalhes(id):
    config = get_site_config()
    mensagem = MensagemContato.query.get_or_404(id)
    
    # Marcar como lida
    if mensagem.status == 'não_lida':
        mensagem.status = 'lida'
        db.session.commit()
    
    return render_template('admin/mensagem_detalhes.html', config=config, mensagem=mensagem)

@app.route('/admin/mensagens/status/<int:id>', methods=['POST'])
@login_required
def admin_mensagem_status(id):
    mensagem = MensagemContato.query.get_or_404(id)
    novo_status = request.form['status']
    
    if novo_status in ['não_lida', 'lida', 'respondida']:
        mensagem.status = novo_status
        db.session.commit()
        flash('Status da mensagem atualizado com sucesso!', 'success')
    else:
        flash('Status inválido!', 'error')
    
    return redirect(url_for('admin_mensagem_detalhes', id=id))

@app.route('/admin/mensagens/excluir/<int:id>', methods=['POST'])
@login_required
def admin_mensagem_excluir(id):
    mensagem = MensagemContato.query.get_or_404(id)
    try:
        db.session.delete(mensagem)
        db.session.commit()
        flash('Mensagem excluída com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao excluir mensagem: {str(e)}', 'error')
    
    return redirect(url_for('admin_mensagens'))

# Rota para gerenciar página de contato
@app.route('/admin/contato', methods=['GET', 'POST'])
@login_required
def admin_contato():
    config = get_site_config()
    pagina_contato = PaginaContato.query.first()
    
    if request.method == 'POST':
        try:
            if not pagina_contato:
                pagina_contato = PaginaContato()
                db.session.add(pagina_contato)
            
            pagina_contato.titulo = request.form['titulo']
            pagina_contato.subtitulo = request.form['subtitulo']
            pagina_contato.descricao = request.form['descricao']
            pagina_contato.telefone_principal = request.form['telefone_principal']
            pagina_contato.telefone_secundario = request.form['telefone_secundario']
            pagina_contato.email_contato = request.form['email_contato']
            pagina_contato.endereco = request.form['endereco']
            pagina_contato.horario_funcionamento = request.form['horario_funcionamento']
            pagina_contato.redes_sociais = request.form['redes_sociais']
            pagina_contato.mapa_embed = request.form['mapa_embed']
            
            db.session.commit()
            flash('Página de contato atualizada com sucesso!', 'success')
            return redirect(url_for('admin_contato'))
        except Exception as e:
            flash(f'Erro ao atualizar página de contato: {str(e)}', 'error')
    
    return render_template('admin/contato.html', config=config, pagina_contato=pagina_contato)

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
                subtitulo='Conheça os profissionais que fazem a diferença',
                descricao='Nossa equipe é composta por profissionais apaixonados por rádio e comunicação, dedicados a trazer o melhor conteúdo para nossos ouvintes.',
                mensagem_equipe='Trabalhamos juntos para criar uma experiência única e envolvente para nossa audiência.',
                imagem_principal='https://images.unsplash.com/photo-1522071820081-009f0129c71c?w=800',
                estatisticas_equipe=json.dumps({
                    'estatistica_equipe_1': {'titulo': 'Anos de Experiência', 'valor': '15+'},
                    'estatistica_equipe_2': {'titulo': 'Profissionais', 'valor': '25+'},
                    'estatistica_equipe_3': {'titulo': 'Programas', 'valor': '50+'},
                    'estatistica_equipe_4': {'titulo': 'Prêmios', 'valor': '10+'}
                }),
                areas_atuacao=json.dumps({
                    'area_1': {'titulo': 'Jornalismo', 'descricao': 'Cobertura de notícias locais e nacionais'},
                    'area_2': {'titulo': 'Entretenimento', 'descricao': 'Programas de música e entretenimento'},
                    'area_3': {'titulo': 'Esportes', 'descricao': 'Cobertura esportiva completa'},
                    'area_4': {'titulo': 'Tecnologia', 'descricao': 'Inovação e tendências tecnológicas'},
                    'area_5': {'titulo': 'Cultura', 'descricao': 'Arte, literatura e eventos culturais'},
                    'area_6': {'titulo': 'Comunidade', 'descricao': 'Projetos sociais e comunitários'}
                }),
                convite_equipe='Quer fazer parte da nossa equipe? Entre em contato conosco! Oferecemos oportunidades de crescimento e um ambiente colaborativo.'
            )
            db.session.add(pagina_equipe)

        # Criar dados padrão para página de contato
        if not PaginaContato.query.first():
            pagina_contato = PaginaContato(
                titulo='Entre em Contato',
                subtitulo='Estamos aqui para ajudar. Entre em contato conosco!',
                descricao='Tem alguma dúvida, sugestão ou quer fazer parte da nossa equipe? Entre em contato conosco através do formulário abaixo ou pelos nossos canais de atendimento.',
                telefone_principal='(11) 99999-9999',
                telefone_secundario='(11) 88888-8888',
                email_contato='contato@radioshostlink.com.br',
                endereco='Rua das Rádios, 123\nBairro Central\nSão Paulo - SP, 01234-567',
                horario_funcionamento='Segunda a Sexta: 8h às 18h\nSábado: 9h às 14h\nDomingo: Fechado',
                redes_sociais=json.dumps({
                    'facebook': 'https://facebook.com/radioshostlink',
                    'instagram': 'https://instagram.com/radioshostlink',
                    'twitter': 'https://twitter.com/radioshostlink',
                    'youtube': 'https://youtube.com/radioshostlink'
                }),
                mapa_embed='<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3657.1234567890123!2d-46.6388!3d-23.5505!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMjPCsDMzJzAxLjgiUyA0NsKwMzgnMTkuNyJX!5e0!3m2!1spt-BR!2sbr!4v1234567890123" width="100%" height="300" style="border:0;" allowfullscreen="" loading="lazy"></iframe>'
            )
            db.session.add(pagina_contato)

        db.session.commit()
    
    app.run(debug=True, host='0.0.0.0', port=5000) 