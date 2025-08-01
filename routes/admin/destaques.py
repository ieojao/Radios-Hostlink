from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from models.content import Destaque
from models.database import db
from . import admin_bp

@admin_bp.route('/destaques')
@login_required
def destaques():
    """Lista de destaques"""
    destaques = Destaque.query.order_by(Destaque.ordem).all()
    return render_template('admin/destaques.html', destaques=destaques)

@admin_bp.route('/destaques/adicionar', methods=['GET', 'POST'])
@login_required
def destaques_adicionar():
    """Adicionar novo destaque"""
    if request.method == 'POST':
        try:
            destaque = Destaque(
                titulo=request.form['titulo'],
                descricao=request.form.get('descricao', ''),
                imagem=request.form.get('imagem', ''),
                link=request.form.get('link', ''),
                ativo='ativo' in request.form,
                ordem=int(request.form.get('ordem', 0))
            )
            db.session.add(destaque)
            db.session.commit()
            flash('Destaque adicionado com sucesso!', 'success')
            return redirect(url_for('admin.destaques'))
        except Exception as e:
            flash(f'Erro ao adicionar destaque: {str(e)}', 'error')
    
    return render_template('admin/destaques_form.html')

@admin_bp.route('/destaques/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def destaques_editar(id):
    """Editar destaque"""
    destaque = Destaque.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            destaque.titulo = request.form['titulo']
            destaque.descricao = request.form.get('descricao', '')
            destaque.imagem = request.form.get('imagem', '')
            destaque.link = request.form.get('link', '')
            destaque.ativo = 'ativo' in request.form
            destaque.ordem = int(request.form.get('ordem', 0))
            db.session.commit()
            flash('Destaque atualizado com sucesso!', 'success')
            return redirect(url_for('admin.destaques'))
        except Exception as e:
            flash(f'Erro ao atualizar destaque: {str(e)}', 'error')
    
    return render_template('admin/destaques_form.html', destaque=destaque)

@admin_bp.route('/destaques/deletar/<int:id>', methods=['POST'])
@login_required
def destaques_deletar(id):
    """Deletar destaque"""
    try:
        destaque = Destaque.query.get_or_404(id)
        db.session.delete(destaque)
        db.session.commit()
        flash('Destaque deletado com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao deletar destaque: {str(e)}', 'error')
    
    return redirect(url_for('admin.destaques')) 