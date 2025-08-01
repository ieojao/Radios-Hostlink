from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from models.content import Banner
from models.database import db
from . import admin_bp

@admin_bp.route('/banners')
@login_required
def banners():
    """Lista de banners"""
    banners = Banner.query.order_by(Banner.ordem).all()
    return render_template('admin/banners.html', banners=banners)

@admin_bp.route('/banners/adicionar', methods=['GET', 'POST'])
@login_required
def banners_adicionar():
    """Adicionar novo banner"""
    if request.method == 'POST':
        try:
            banner = Banner(
                titulo=request.form['titulo'],
                imagem=request.form.get('imagem', ''),
                link=request.form.get('link', ''),
                ativo='ativo' in request.form,
                ordem=int(request.form.get('ordem', 0))
            )
            db.session.add(banner)
            db.session.commit()
            flash('Banner adicionado com sucesso!', 'success')
            return redirect(url_for('admin.banners'))
        except Exception as e:
            flash(f'Erro ao adicionar banner: {str(e)}', 'error')
    
    return render_template('admin/banners_form.html')

@admin_bp.route('/banners/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def banners_editar(id):
    """Editar banner"""
    banner = Banner.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            banner.titulo = request.form['titulo']
            banner.imagem = request.form.get('imagem', '')
            banner.link = request.form.get('link', '')
            banner.ativo = 'ativo' in request.form
            banner.ordem = int(request.form.get('ordem', 0))
            db.session.commit()
            flash('Banner atualizado com sucesso!', 'success')
            return redirect(url_for('admin.banners'))
        except Exception as e:
            flash(f'Erro ao atualizar banner: {str(e)}', 'error')
    
    return render_template('admin/banners_form.html', banner=banner)

@admin_bp.route('/banners/deletar/<int:id>', methods=['POST'])
@login_required
def banners_deletar(id):
    """Deletar banner"""
    try:
        banner = Banner.query.get_or_404(id)
        db.session.delete(banner)
        db.session.commit()
        flash('Banner deletado com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao deletar banner: {str(e)}', 'error')
    
    return redirect(url_for('admin.banners')) 