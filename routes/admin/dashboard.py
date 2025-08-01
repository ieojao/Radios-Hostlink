from flask import render_template
from flask_login import login_required
from services.config_service import ConfigService
from models.content import Programacao, Locutor, Banner, Destaque
from models.pages import MensagemContato
from . import admin_bp

@admin_bp.route('/')
@login_required
def dashboard():
    """Dashboard principal do admin"""
    config = ConfigService.get_site_config()
    
    # Estatísticas
    total_programacao = Programacao.query.count()
    total_locutores = Locutor.query.count()
    total_banners = Banner.query.count()
    total_mensagens = MensagemContato.query.count()
    mensagens_nao_lidas = MensagemContato.query.filter_by(status='não_lida').count()
    
    # Programação ativa
    programacao_ativa = Programacao.query.filter_by(ativo=True).count()
    
    # Locutores ativos
    locutores_ativos = Locutor.query.filter_by(ativo=True).count()
    
    # Destaques ativos
    destaques_ativos = Destaque.query.filter_by(ativo=True).count()
    
    return render_template('admin/dashboard.html', 
                         config=config,
                         total_programacao=total_programacao,
                         programacao_ativa=programacao_ativa,
                         total_locutores=total_locutores,
                         locutores_ativos=locutores_ativos,
                         total_banners=total_banners,
                         total_mensagens=total_mensagens,
                         mensagens_nao_lidas=mensagens_nao_lidas,
                         destaques_ativos=destaques_ativos) 