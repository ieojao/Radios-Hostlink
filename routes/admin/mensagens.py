from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from models.pages import MensagemContato
from models.database import db
from . import admin_bp

@admin_bp.route('/mensagens')
@login_required
def mensagens():
    """Lista de mensagens de contato"""
    mensagens = MensagemContato.query.order_by(MensagemContato.criado_em.desc()).all()
    return render_template('admin/mensagens.html', mensagens=mensagens)

@admin_bp.route('/mensagens/<int:id>')
@login_required
def mensagem_detalhes(id):
    """Detalhes de uma mensagem"""
    mensagem = MensagemContato.query.get_or_404(id)
    
    # Marcar como lida
    if not mensagem.lida:
        mensagem.lida = True
        db.session.commit()
    
    return render_template('admin/mensagem_detalhes.html', mensagem=mensagem)

@admin_bp.route('/mensagens/deletar/<int:id>', methods=['POST'])
@login_required
def mensagem_deletar(id):
    """Deletar mensagem"""
    try:
        mensagem = MensagemContato.query.get_or_404(id)
        db.session.delete(mensagem)
        db.session.commit()
        flash('Mensagem deletada com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao deletar mensagem: {str(e)}', 'error')
    
    return redirect(url_for('admin.mensagens')) 