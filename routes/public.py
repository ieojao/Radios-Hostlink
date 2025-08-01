from flask import Blueprint, render_template, request, jsonify
from services.programacao_service import ProgramacaoService
from services.config_service import ConfigService
from models.pages import MensagemContato
from models.database import db

# Criar blueprint para rotas públicas
public_bp = Blueprint('public', __name__)

@public_bp.route('/')
def index():
    """Página inicial"""
    config = ConfigService.get_site_config()
    programacao_atual = ProgramacaoService.get_programacao_atual()
    from models.content import Destaque
    destaques = Destaque.query.filter_by(ativo=True).order_by(Destaque.ordem).all()
    return render_template('index.html', 
                         config=config, 
                         programacao_atual=programacao_atual, 
                         destaques=destaques)

@public_bp.route('/a-radio')
def a_radio():
    """Página 'A Rádio'"""
    config = ConfigService.get_site_config()
    from models.pages import PaginaRadio
    pagina_radio = PaginaRadio.query.first()
    return render_template('a-radio.html', config=config, pagina_radio=pagina_radio)

@public_bp.route('/programacao')
def programacao():
    """Página de programação"""
    config = ConfigService.get_site_config()
    programacao_completa = ProgramacaoService.get_programacao_completa()
    return render_template('programacao.html', 
                         config=config, 
                         programacao=programacao_completa)

@public_bp.route('/equipe')
def equipe():
    """Página da equipe"""
    config = ConfigService.get_site_config()
    from models.content import Locutor
    from models.pages import PaginaEquipe
    locutores = Locutor.query.filter_by(ativo=True).all()
    pagina_equipe = PaginaEquipe.query.first()
    return render_template('equipe.html', 
                         config=config, 
                         locutores=locutores, 
                         pagina_equipe=pagina_equipe)

@public_bp.route('/contato')
def contato():
    """Página de contato"""
    config = ConfigService.get_site_config()
    from models.pages import PaginaContato
    pagina_contato = PaginaContato.query.first()
    return render_template('contato.html', 
                         config=config, 
                         pagina_contato=pagina_contato)

@public_bp.route('/contato/enviar', methods=['POST'])
def enviar_mensagem():
    """Endpoint para enviar mensagem de contato"""
    try:
        mensagem = MensagemContato(
            nome=request.form['nome'],
            email=request.form['email'],
            telefone=request.form.get('telefone', ''),
            assunto=request.form.get('assunto', ''),
            mensagem=request.form['mensagem'],
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', '')
        )
        db.session.add(mensagem)
        db.session.commit()
        
        return jsonify({'success': True, 'message': 'Mensagem enviada com sucesso!'})
    except Exception as e:
        return jsonify({'success': False, 'message': 'Erro ao enviar mensagem. Tente novamente.'}) 