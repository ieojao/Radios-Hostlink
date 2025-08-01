from flask import render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, login_required, current_user
from models.user import Usuario
from models.database import db
from . import admin_bp

@admin_bp.route('/login', methods=['GET', 'POST'])
def login():
    """Página de login do admin"""
    if request.method == 'POST':
        email = request.form['email']
        senha = request.form['senha']
        
        usuario = Usuario.query.filter_by(email=email, ativo=True).first()
        if usuario and usuario.check_password(senha):
            login_user(usuario)
            # Atualizar último login
            usuario.ultimo_login = db.func.now()
            db.session.commit()
            return redirect(url_for('admin.dashboard'))
        else:
            flash('Email ou senha incorretos', 'error')
    
    return render_template('admin/login.html')

@admin_bp.route('/logout')
@login_required
def logout():
    """Logout do usuário"""
    logout_user()
    flash('Você foi desconectado com sucesso!', 'success')
    return redirect(url_for('admin.login')) 