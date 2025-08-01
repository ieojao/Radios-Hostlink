from flask import render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required
from models.content import Programacao
from models.database import db
from services.programacao_service import ProgramacaoService
from . import admin_bp

@admin_bp.route('/programacao')
@login_required
def programacao():
    """Lista de programação"""
    programacao_completa = ProgramacaoService.get_programacao_completa()
    return render_template('admin/programacao.html', programacao=programacao_completa)

@admin_bp.route('/programacao/adicionar', methods=['GET', 'POST'])
@login_required
def programacao_adicionar():
    """Adicionar nova programação"""
    if request.method == 'POST':
        try:
            dados = {
                'dia_semana': request.form['dia_semana'],
                'horario_inicio': request.form['horario_inicio'],
                'horario_fim': request.form['horario_fim'],
                'titulo': request.form['titulo'],
                'descricao': request.form.get('descricao', ''),
                'ativo': 'ativo' in request.form
            }
            
            programacao = ProgramacaoService.criar_programacao(dados)
            flash('Programação criada com sucesso!', 'success')
            return redirect(url_for('admin.programacao'))
        except Exception as e:
            flash(f'Erro ao criar programação: {str(e)}', 'error')
    
    return render_template('admin/programacao_form.html')

@admin_bp.route('/programacao/editar/<int:id>', methods=['GET', 'POST'])
@login_required
def programacao_editar(id):
    """Editar programação"""
    programacao = Programacao.query.get_or_404(id)
    
    if request.method == 'POST':
        try:
            dados = {
                'dia_semana': request.form['dia_semana'],
                'horario_inicio': request.form['horario_inicio'],
                'horario_fim': request.form['horario_fim'],
                'titulo': request.form['titulo'],
                'descricao': request.form.get('descricao', ''),
                'ativo': 'ativo' in request.form
            }
            
            ProgramacaoService.atualizar_programacao(id, dados)
            flash('Programação atualizada com sucesso!', 'success')
            return redirect(url_for('admin.programacao'))
        except Exception as e:
            flash(f'Erro ao atualizar programação: {str(e)}', 'error')
    
    return render_template('admin/programacao_form.html', programacao=programacao)

@admin_bp.route('/programacao/deletar/<int:id>', methods=['POST'])
@login_required
def programacao_deletar(id):
    """Deletar programação"""
    try:
        ProgramacaoService.deletar_programacao(id)
        flash('Programação deletada com sucesso!', 'success')
    except Exception as e:
        flash(f'Erro ao deletar programação: {str(e)}', 'error')
    
    return redirect(url_for('admin.programacao')) 