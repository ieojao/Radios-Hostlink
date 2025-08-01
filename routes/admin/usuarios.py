from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from models.user import Usuario
from models.database import db
from . import admin_bp

@admin_bp.route('/usuarios')
@login_required
def usuarios():
    """Lista de usuários"""
    usuarios = Usuario.query.all()
    return render_template('admin/usuarios.html', usuarios=usuarios)

@admin_bp.route('/usuarios/adicionar', methods=['GET', 'POST'])
@login_required
def usuarios_adicionar():
    """Adicionar novo usuário"""
    if request.method == 'POST':
        try:
            usuario = Usuario(
                nome=request.form['nome'],
                email=request.form['email'],
                nivel=request.form.get('nivel', 'admin'),
                ativo='ativo' in request.form
            )
            usuario.set_password(request.form['senha'])
            db.session.add(usuario)
            db.session.commit()
            flash('Usuário adicionado com sucesso!', 'success')
            return redirect(url_for('admin.usuarios'))
        except Exception as e:
            flash(f'Erro ao adicionar usuário: {str(e)}', 'error')
    
    return render_template('admin/usuarios_form.html')

@admin_bp.route('/usuarios/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def usuarios_editar(id):
    """Editar usuário"""
    usuario = Usuario.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            usuario.nome = request.form['nome']
            usuario.email = request.form['email']
            usuario.nivel = request.form.get('nivel', 'admin')
            usuario.ativo = 'ativo' in request.form
            
            if request.form.get('senha'):
                usuario.set_password(request.form['senha'])
            
            db.session.commit()
            flash('Usuário atualizado com sucesso!', 'success')
            return redirect(url_for('admin.usuarios'))
        except Exception as e:
            flash(f'Erro ao atualizar usuário: {str(e)}', 'error')
    
    return render_template('admin/usuarios_form.html', usuario=usuario)

@admin_bp.route('/usuarios/deletar/<int:id>', methods=['POST'])
@login_required
def usuarios_deletar(id):
    """Deletar usuário"""
    try:
        usuario = Usuario.query.get_or_404(id)
        db.session.delete(usuario)
        db.session.commit()
        flash('Usuário deletado com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao deletar usuário: {str(e)}', 'error')
    
    return redirect(url_for('admin.usuarios')) 