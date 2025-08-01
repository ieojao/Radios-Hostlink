from flask import render_template, request, redirect, url_for, flash
from flask_login import login_required
from models.pages import PaginaRadio, PaginaEquipe, PaginaContato
from models.database import db
import json
from . import admin_bp

@admin_bp.route('/a-radio', methods=['GET', 'POST'])
@login_required
def a_radio():
    """Gerenciar página 'A Rádio'"""
    pagina = PaginaRadio.query.first()
    
    if request.method == 'POST':
        try:
            if not pagina:
                pagina = PaginaRadio()
                db.session.add(pagina)
            
            pagina.titulo = request.form['titulo']
            pagina.subtitulo = request.form.get('subtitulo', '')
            pagina.descricao = request.form.get('descricao', '')
            pagina.historia = request.form.get('historia', '')
            pagina.missao = request.form.get('missao', '')
            pagina.visao = request.form.get('visao', '')
            pagina.valores = request.form.get('valores', '')
            pagina.imagem_principal = request.form.get('imagem_principal', '')
            pagina.imagem_historia = request.form.get('imagem_historia', '')
            pagina.estatisticas = request.form.get('estatisticas', '')
            
            db.session.commit()
            flash('Página "A Rádio" atualizada com sucesso!', 'success')
            return redirect(url_for('admin.a_radio'))
        except Exception as e:
            flash(f'Erro ao atualizar página: {str(e)}', 'error')
    
    return render_template('admin/a_radio.html', pagina=pagina)

@admin_bp.route('/equipe', methods=['GET', 'POST'])
@login_required
def equipe():
    """Gerenciar página 'Equipe'"""
    pagina = PaginaEquipe.query.first()
    
    if request.method == 'POST':
        try:
            if not pagina:
                pagina = PaginaEquipe()
                db.session.add(pagina)
            
            pagina.titulo = request.form['titulo']
            pagina.subtitulo = request.form.get('subtitulo', '')
            pagina.descricao = request.form.get('descricao', '')
            pagina.mensagem_equipe = request.form.get('mensagem_equipe', '')
            pagina.estatisticas_equipe = request.form.get('estatisticas_equipe', '')
            pagina.areas_atuacao = request.form.get('areas_atuacao', '')
            pagina.convite_equipe = request.form.get('convite_equipe', '')
            
            db.session.commit()
            flash('Página "Equipe" atualizada com sucesso!', 'success')
            return redirect(url_for('admin.equipe'))
        except Exception as e:
            flash(f'Erro ao atualizar página: {str(e)}', 'error')
    
    return render_template('admin/equipe.html', pagina=pagina)

@admin_bp.route('/contato', methods=['GET', 'POST'])
@login_required
def contato():
    """Gerenciar página 'Contato'"""
    pagina = PaginaContato.query.first()
    
    if request.method == 'POST':
        try:
            if not pagina:
                pagina = PaginaContato()
                db.session.add(pagina)
            
            pagina.titulo = request.form['titulo']
            pagina.subtitulo = request.form.get('subtitulo', '')
            pagina.descricao = request.form.get('descricao', '')
            pagina.telefone_principal = request.form.get('telefone_principal', '')
            pagina.telefone_secundario = request.form.get('telefone_secundario', '')
            pagina.email_contato = request.form.get('email_contato', '')
            pagina.endereco = request.form.get('endereco', '')
            pagina.horario_funcionamento = request.form.get('horario_funcionamento', '')
            pagina.redes_sociais = request.form.get('redes_sociais', '')
            pagina.mapa_embed = request.form.get('mapa_embed', '')
            
            db.session.commit()
            flash('Página "Contato" atualizada com sucesso!', 'success')
            return redirect(url_for('admin.contato'))
        except Exception as e:
            flash(f'Erro ao atualizar página: {str(e)}', 'error')
    
    return render_template('admin/contato.html', pagina=pagina) 