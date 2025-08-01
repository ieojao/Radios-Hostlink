from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from models.content import Locutor
from models.database import db
from . import admin_bp

@admin_bp.route('/locutores')
@login_required
def locutores():
    """Lista de locutores"""
    locutores = Locutor.query.all()
    return render_template('admin/locutores.html', locutores=locutores)

@admin_bp.route('/locutores/adicionar', methods=['GET', 'POST'])
@login_required
def locutores_adicionar():
    """Adicionar novo locutor"""
    if request.method == 'POST':
        try:
            locutor = Locutor(
                nome=request.form['nome'],
                bio=request.form.get('bio', ''),
                redes_sociais=request.form.get('redes_sociais', ''),
                ativo='ativo' in request.form
            )
            db.session.add(locutor)
            db.session.commit()
            flash('Locutor adicionado com sucesso!', 'success')
            return redirect(url_for('admin.locutores'))
        except Exception as e:
            flash(f'Erro ao adicionar locutor: {str(e)}', 'error')
    
    return render_template('admin/locutores_form.html')

@admin_bp.route('/locutores/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def locutores_editar(id):
    """Editar locutor"""
    locutor = Locutor.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            locutor.nome = request.form['nome']
            locutor.bio = request.form.get('bio', '')
            locutor.redes_sociais = request.form.get('redes_sociais', '')
            locutor.ativo = 'ativo' in request.form
            db.session.commit()
            flash('Locutor atualizado com sucesso!', 'success')
            return redirect(url_for('admin.locutores'))
        except Exception as e:
            flash(f'Erro ao atualizar locutor: {str(e)}', 'error')
    
    return render_template('admin/locutores_form.html', locutor=locutor)

@admin_bp.route('/locutores/deletar/<int:id>', methods=['POST'])
@login_required
def locutores_deletar(id):
    """Deletar locutor"""
    try:
        locutor = Locutor.query.get_or_404(id)
        db.session.delete(locutor)
        db.session.commit()
        flash('Locutor deletado com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao deletar locutor: {str(e)}', 'error')
    
    return redirect(url_for('admin.locutores')) 