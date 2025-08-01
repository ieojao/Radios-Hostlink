#!/usr/bin/env python3
"""
Script de migração para a nova arquitetura
Este script ajuda a migrar dados da arquitetura antiga para a nova
"""

import os
import sys
import shutil
import sqlite3
from datetime import datetime

def backup_old_files():
    """Faz backup dos arquivos antigos"""
    print("🔄 Fazendo backup dos arquivos antigos...")
    
    # Criar pasta de backup
    backup_dir = f"backup_old_architecture_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    os.makedirs(backup_dir, exist_ok=True)
    
    # Arquivos para fazer backup
    files_to_backup = [
        'app.py',
        'requirements.txt',
        'env_example.txt'
    ]
    
    for file in files_to_backup:
        if os.path.exists(file):
            shutil.copy2(file, backup_dir)
            print(f"✅ Backup de {file}")
    
    # Backup do banco de dados
    if os.path.exists('radio.db'):
        shutil.copy2('radio.db', f"{backup_dir}/radio.db")
        print("✅ Backup do banco de dados")
    
    print(f"✅ Backup completo salvo em: {backup_dir}")
    return backup_dir

def migrate_database():
    """Migra dados do banco antigo para o novo"""
    print("🔄 Migrando dados do banco...")
    
    if not os.path.exists('radio.db'):
        print("⚠️ Banco de dados não encontrado. Criando novo banco...")
        return
    
    try:
        # Conectar ao banco antigo
        conn_old = sqlite3.connect('radio.db')
        cursor_old = conn_old.cursor()
        
        # Verificar se existe a tabela antiga
        cursor_old.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='usuario'")
        if not cursor_old.fetchone():
            print("⚠️ Estrutura antiga não encontrada. Criando novo banco...")
            conn_old.close()
            return
        
        print("✅ Estrutura antiga encontrada. Migrando dados...")
        
        # Migrar usuários
        cursor_old.execute("SELECT id, nome, email, senha, nivel, criado_em FROM usuario")
        usuarios = cursor_old.fetchall()
        
        # Conectar ao novo banco
        from app_factory import create_app
        from models.database import db
        from models.user import Usuario
        
        app = create_app()
        with app.app_context():
            # Criar tabelas
            db.create_all()
            
            # Migrar usuários
            for user_data in usuarios:
                user_id, nome, email, senha, nivel, criado_em = user_data
                
                # Verificar se usuário já existe
                existing_user = Usuario.query.filter_by(email=email).first()
                if not existing_user:
                    usuario = Usuario(
                        id=user_id,
                        nome=nome,
                        email=email,
                        senha=senha,  # Senha já está criptografada
                        nivel=nivel,
                        criado_em=datetime.fromisoformat(criado_em) if criado_em else None,
                        ativo=True
                    )
                    db.session.add(usuario)
                    print(f"✅ Usuário migrado: {email}")
            
            # Migrar programação
            cursor_old.execute("SELECT id, dia_semana, horario_inicio, horario_fim, titulo, descricao, imagem, criado_em FROM programacao")
            programacoes = cursor_old.fetchall()
            
            from models.content import Programacao
            
            for prog_data in programacoes:
                prog_id, dia_semana, horario_inicio, horario_fim, titulo, descricao, imagem, criado_em = prog_data
                
                # Converter horários
                from datetime import datetime, time
                try:
                    inicio = datetime.strptime(horario_inicio, '%H:%M:%S').time() if horario_inicio else time(0, 0)
                    fim = datetime.strptime(horario_fim, '%H:%M:%S').time() if horario_fim else time(0, 0)
                except:
                    inicio = time(0, 0)
                    fim = time(0, 0)
                
                programacao = Programacao(
                    id=prog_id,
                    dia_semana=dia_semana,
                    horario_inicio=inicio,
                    horario_fim=fim,
                    titulo=titulo,
                    descricao=descricao,
                    imagem=imagem,
                    ativo=True,
                    criado_em=datetime.fromisoformat(criado_em) if criado_em else None
                )
                db.session.add(programacao)
                print(f"✅ Programação migrada: {titulo}")
            
            # Migrar locutores
            cursor_old.execute("SELECT id, nome, foto, bio, redes_sociais, criado_em FROM locutor")
            locutores = cursor_old.fetchall()
            
            from models.content import Locutor
            
            for loc_data in locutores:
                loc_id, nome, foto, bio, redes_sociais, criado_em = loc_data
                
                locutor = Locutor(
                    id=loc_id,
                    nome=nome,
                    foto=foto,
                    bio=bio,
                    redes_sociais=redes_sociais,
                    ativo=True,
                    criado_em=datetime.fromisoformat(criado_em) if criado_em else None
                )
                db.session.add(locutor)
                print(f"✅ Locutor migrado: {nome}")
            
            # Migrar banners
            cursor_old.execute("SELECT id, titulo, imagem, link, criado_em FROM banner")
            banners = cursor_old.fetchall()
            
            from models.content import Banner
            
            for ban_data in banners:
                ban_id, titulo, imagem, link, criado_em = ban_data
                
                banner = Banner(
                    id=ban_id,
                    titulo=titulo,
                    imagem=imagem,
                    link=link,
                    ativo=True,
                    criado_em=datetime.fromisoformat(criado_em) if criado_em else None
                )
                db.session.add(banner)
                print(f"✅ Banner migrado: {titulo}")
            
            # Migrar destaques
            cursor_old.execute("SELECT id, titulo, descricao, imagem, link, ordem, ativo, criado_em FROM destaque")
            destaques = cursor_old.fetchall()
            
            from models.content import Destaque
            
            for des_data in destaques:
                des_id, titulo, descricao, imagem, link, ordem, ativo, criado_em = des_data
                
                destaque = Destaque(
                    id=des_id,
                    titulo=titulo,
                    descricao=descricao,
                    imagem=imagem,
                    link=link,
                    ordem=ordem or 0,
                    ativo=bool(ativo),
                    criado_em=datetime.fromisoformat(criado_em) if criado_em else None
                )
                db.session.add(destaque)
                print(f"✅ Destaque migrado: {titulo}")
            
            # Migrar configurações
            cursor_old.execute("SELECT id, chave, valor, criado_em FROM configuracao")
            configuracoes = cursor_old.fetchall()
            
            from models.content import Configuracao
            
            for config_data in configuracoes:
                config_id, chave, valor, criado_em = config_data
                
                config = Configuracao(
                    id=config_id,
                    chave=chave,
                    valor=valor,
                    criado_em=datetime.fromisoformat(criado_em) if criado_em else None
                )
                db.session.add(config)
                print(f"✅ Configuração migrada: {chave}")
            
            # Migrar páginas
            # Página Radio
            cursor_old.execute("SELECT id, titulo, subtitulo, descricao, historia, missao, visao, valores, imagem_principal, imagem_historia, estatisticas, criado_em FROM pagina_radio LIMIT 1")
            pagina_radio_data = cursor_old.fetchone()
            
            if pagina_radio_data:
                from models.pages import PaginaRadio
                
                pr_id, titulo, subtitulo, descricao, historia, missao, visao, valores, imagem_principal, imagem_historia, estatisticas, criado_em = pagina_radio_data
                
                pagina_radio = PaginaRadio(
                    id=pr_id,
                    titulo=titulo,
                    subtitulo=subtitulo,
                    descricao=descricao,
                    historia=historia,
                    missao=missao,
                    visao=visao,
                    valores=valores,
                    imagem_principal=imagem_principal,
                    imagem_historia=imagem_historia,
                    estatisticas=estatisticas,
                    criado_em=datetime.fromisoformat(criado_em) if criado_em else None
                )
                db.session.add(pagina_radio)
                print("✅ Página Radio migrada")
            
            # Página Equipe
            cursor_old.execute("SELECT id, titulo, subtitulo, descricao, mensagem_equipe, imagem_principal, estatisticas_equipe, areas_atuacao, convite_equipe, criado_em FROM pagina_equipe LIMIT 1")
            pagina_equipe_data = cursor_old.fetchone()
            
            if pagina_equipe_data:
                from models.pages import PaginaEquipe
                
                pe_id, titulo, subtitulo, descricao, mensagem_equipe, imagem_principal, estatisticas_equipe, areas_atuacao, convite_equipe, criado_em = pagina_equipe_data
                
                pagina_equipe = PaginaEquipe(
                    id=pe_id,
                    titulo=titulo,
                    subtitulo=subtitulo,
                    descricao=descricao,
                    mensagem_equipe=mensagem_equipe,
                    imagem_principal=imagem_principal,
                    estatisticas_equipe=estatisticas_equipe,
                    areas_atuacao=areas_atuacao,
                    convite_equipe=convite_equipe,
                    criado_em=datetime.fromisoformat(criado_em) if criado_em else None
                )
                db.session.add(pagina_equipe)
                print("✅ Página Equipe migrada")
            
            # Página Contato
            cursor_old.execute("SELECT id, titulo, subtitulo, descricao, telefone_principal, telefone_secundario, email_contato, endereco, horario_funcionamento, redes_sociais, mapa_embed, criado_em FROM pagina_contato LIMIT 1")
            pagina_contato_data = cursor_old.fetchone()
            
            if pagina_contato_data:
                from models.pages import PaginaContato
                
                pc_id, titulo, subtitulo, descricao, telefone_principal, telefone_secundario, email_contato, endereco, horario_funcionamento, redes_sociais, mapa_embed, criado_em = pagina_contato_data
                
                pagina_contato = PaginaContato(
                    id=pc_id,
                    titulo=titulo,
                    subtitulo=subtitulo,
                    descricao=descricao,
                    telefone_principal=telefone_principal,
                    telefone_secundario=telefone_secundario,
                    email_contato=email_contato,
                    endereco=endereco,
                    horario_funcionamento=horario_funcionamento,
                    redes_sociais=redes_sociais,
                    mapa_embed=mapa_embed,
                    criado_em=datetime.fromisoformat(criado_em) if criado_em else None
                )
                db.session.add(pagina_contato)
                print("✅ Página Contato migrada")
            
            # Migrar mensagens
            cursor_old.execute("SELECT id, nome, email, telefone, assunto, mensagem, status, criado_em FROM mensagem_contato")
            mensagens = cursor_old.fetchall()
            
            from models.pages import MensagemContato
            
            for msg_data in mensagens:
                msg_id, nome, email, telefone, assunto, mensagem, status, criado_em = msg_data
                
                msg = MensagemContato(
                    id=msg_id,
                    nome=nome,
                    email=email,
                    telefone=telefone,
                    assunto=assunto,
                    mensagem=mensagem,
                    status=status,
                    criado_em=datetime.fromisoformat(criado_em) if criado_em else None
                )
                db.session.add(msg)
                print(f"✅ Mensagem migrada: {nome}")
            
            # Commit das mudanças
            db.session.commit()
            print("✅ Migração concluída com sucesso!")
        
        conn_old.close()
        
    except Exception as e:
        print(f"❌ Erro durante a migração: {str(e)}")
        return False
    
    return True

def create_new_structure():
    """Cria a nova estrutura de pastas"""
    print("🔄 Criando nova estrutura de pastas...")
    
    # Pastas necessárias
    folders = [
        'logs',
        'static/uploads',
        'static/uploads/programacao',
        'static/uploads/locutores',
        'static/uploads/banners',
        'static/uploads/destaques',
        'static/uploads/config'
    ]
    
    for folder in folders:
        os.makedirs(folder, exist_ok=True)
        print(f"✅ Pasta criada: {folder}")

def main():
    """Função principal do script de migração"""
    print("🚀 Iniciando migração para nova arquitetura...")
    print("=" * 50)
    
    # 1. Backup dos arquivos antigos
    backup_dir = backup_old_files()
    
    # 2. Criar nova estrutura
    create_new_structure()
    
    # 3. Migrar banco de dados
    if migrate_database():
        print("✅ Migração do banco concluída!")
    else:
        print("⚠️ Migração do banco não foi possível. Criando novo banco...")
    
    # 4. Instruções finais
    print("\n" + "=" * 50)
    print("🎉 Migração concluída!")
    print("\n📋 Próximos passos:")
    print("1. Configure o arquivo config.env com suas configurações")
    print("2. Execute: python run.py init-db")
    print("3. Execute: python run.py run")
    print("4. Acesse: http://localhost:5000")
    print("5. Painel admin: http://localhost:5000/admin")
    print("\n📁 Backup dos arquivos antigos salvo em:", backup_dir)
    print("\n📚 Leia o README_ARQUITETURA.md para mais informações")

if __name__ == '__main__':
    main() 