from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from models.content import Configuracao
from models.database import db
from services.config_service import ConfigService
from . import admin_bp

@admin_bp.route('/configuracoes', methods=['GET', 'POST'])
@login_required
def configuracoes():
    """Gerenciar configurações do site"""
    if request.method == 'POST':
        try:
            # Configurações básicas
            configs = {
                'nome_site': request.form.get('nome_site', ''),
                'slogan': request.form.get('slogan', ''),
                'descricao_site': request.form.get('descricao_site', ''),
                'logo': request.form.get('logo', ''),
                'favicon': request.form.get('favicon', ''),
                'fonte': request.form.get('fonte', 'Inter'),
                'streaming_url': request.form.get('streaming_url', ''),
                'whatsapp': request.form.get('whatsapp', ''),
                'email_contato': request.form.get('email_contato', ''),
                'telefone_contato': request.form.get('telefone_contato', ''),
                'endereco_contato': request.form.get('endereco_contato', ''),
                'horario_funcionamento': request.form.get('horario_funcionamento', ''),
                'facebook': request.form.get('facebook', ''),
                'instagram': request.form.get('instagram', ''),
                'twitter': request.form.get('twitter', ''),
                'youtube': request.form.get('youtube', ''),
                'analytics_code': request.form.get('analytics_code', ''),
                'meta_keywords': request.form.get('meta_keywords', ''),
                'meta_description': request.form.get('meta_description', '')
            }
            
            ConfigService.set_multiple_configs(configs)
            flash('Configurações atualizadas com sucesso!', 'success')
            return redirect(url_for('admin.configuracoes'))
        except Exception as e:
            flash(f'Erro ao atualizar configurações: {str(e)}', 'error')
    
    config = ConfigService.get_site_config()
    return render_template('admin/configuracoes.html', config=config) 