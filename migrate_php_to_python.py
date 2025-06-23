#!/usr/bin/env python3
"""
Script para migrar dados do PHP para Python
"""

import sqlite3
import mysql.connector
import os
import sys
from datetime import datetime
from app import app, db, Usuario, Programacao, Locutor, Banner, Configuracao

def connect_mysql(config):
    """Conecta ao banco MySQL do PHP"""
    try:
        connection = mysql.connector.connect(
            host=config.get('db_host', 'localhost'),
            database=config.get('db_name', 'radio_web'),
            user=config.get('db_user', 'root'),
            password=config.get('db_pass', '')
        )
        return connection
    except Exception as e:
        print(f"❌ Erro ao conectar MySQL: {e}")
        return None

def migrate_users(mysql_conn):
    """Migra usuários do PHP para Python"""
    try:
        cursor = mysql_conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM usuarios")
        users = cursor.fetchall()
        
        with app.app_context():
            for user in users:
                # Verificar se usuário já existe
                existing = Usuario.query.filter_by(email=user['email']).first()
                if not existing:
                    new_user = Usuario(
                        nome=user['nome'],
                        email=user['email'],
                        senha=user['senha'],  # Assumindo que já está criptografada
                        nivel=user['nivel'],
                        criado_em=user['criado_em']
                    )
                    db.session.add(new_user)
            
            db.session.commit()
            print(f"✅ {len(users)} usuários migrados")
            
    except Exception as e:
        print(f"❌ Erro ao migrar usuários: {e}")

def migrate_programming(mysql_conn):
    """Migra programação do PHP para Python"""
    try:
        cursor = mysql_conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM programacao")
        programs = cursor.fetchall()
        
        with app.app_context():
            for program in programs:
                # Verificar se programa já existe
                existing = Programacao.query.filter_by(
                    dia_semana=program['dia_semana'],
                    horario_inicio=program['horario_inicio'],
                    titulo=program['titulo']
                ).first()
                
                if not existing:
                    new_program = Programacao(
                        dia_semana=program['dia_semana'],
                        horario_inicio=program['horario_inicio'],
                        horario_fim=program['horario_fim'],
                        titulo=program['titulo'],
                        descricao=program['descricao'],
                        imagem=program['imagem'],
                        criado_em=program['criado_em']
                    )
                    db.session.add(new_program)
            
            db.session.commit()
            print(f"✅ {len(programs)} programas migrados")
            
    except Exception as e:
        print(f"❌ Erro ao migrar programação: {e}")

def migrate_locutors(mysql_conn):
    """Migra locutores do PHP para Python"""
    try:
        cursor = mysql_conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM locutores")
        locutors = cursor.fetchall()
        
        with app.app_context():
            for locutor in locutors:
                # Verificar se locutor já existe
                existing = Locutor.query.filter_by(nome=locutor['nome']).first()
                if not existing:
                    new_locutor = Locutor(
                        nome=locutor['nome'],
                        foto=locutor['foto'],
                        bio=locutor['bio'],
                        redes_sociais=locutor['redes_sociais'],
                        criado_em=locutor['criado_em']
                    )
                    db.session.add(new_locutor)
            
            db.session.commit()
            print(f"✅ {len(locutors)} locutores migrados")
            
    except Exception as e:
        print(f"❌ Erro ao migrar locutores: {e}")

def migrate_banners(mysql_conn):
    """Migra banners do PHP para Python"""
    try:
        cursor = mysql_conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM banners")
        banners = cursor.fetchall()
        
        with app.app_context():
            for banner in banners:
                # Verificar se banner já existe
                existing = Banner.query.filter_by(titulo=banner['titulo']).first()
                if not existing:
                    new_banner = Banner(
                        titulo=banner['titulo'],
                        imagem=banner['imagem'],
                        link=banner['link'],
                        criado_em=banner['criado_em']
                    )
                    db.session.add(new_banner)
            
            db.session.commit()
            print(f"✅ {len(banners)} banners migrados")
            
    except Exception as e:
        print(f"❌ Erro ao migrar banners: {e}")

def migrate_configs(mysql_conn):
    """Migra configurações do PHP para Python"""
    try:
        cursor = mysql_conn.cursor(dictionary=True)
        cursor.execute("SELECT * FROM configuracoes")
        configs = cursor.fetchall()
        
        with app.app_context():
            for config in configs:
                # Verificar se configuração já existe
                existing = Configuracao.query.filter_by(chave=config['chave']).first()
                if not existing:
                    new_config = Configuracao(
                        chave=config['chave'],
                        valor=config['valor'],
                        criado_em=config['criado_em']
                    )
                    db.session.add(new_config)
            
            db.session.commit()
            print(f"✅ {len(configs)} configurações migradas")
            
    except Exception as e:
        print(f"❌ Erro ao migrar configurações: {e}")

def create_default_configs():
    """Cria configurações padrão se não existirem"""
    default_configs = {
        'nome_site': 'Nova Atalaia',
        'logo': 'logo.png',
        'favicon': 'favicon.ico',
        'cor_principal': '#1e3a8a',
        'cor_fundo': '#ffffff',
        'cor_texto': '#333333',
        'cor_botoes': '#3b82f6',
        'cor_links': '#1e40af',
        'fonte': 'Roboto',
        'texto_rodape': '© 2024 Nova Atalaia. Todos os direitos reservados.',
        'email_contato': 'contato@novaatalaia.com.br',
        'url_streaming': 'https://streaming.example.com/live',
        'whatsapp': '5511999999999',
        'facebook': 'https://facebook.com/novaatalaia',
        'instagram': 'https://instagram.com/novaatalaia',
        'youtube': 'https://youtube.com/novaatalaia',
        'css_custom': ''
    }
    
    with app.app_context():
        for key, value in default_configs.items():
            existing = Configuracao.query.filter_by(chave=key).first()
            if not existing:
                new_config = Configuracao(
                    chave=key,
                    valor=value,
                    criado_em=datetime.utcnow()
                )
                db.session.add(new_config)
        
        db.session.commit()
        print("✅ Configurações padrão criadas")

def main():
    print("🔄 Migração PHP → Python")
    print("=" * 40)
    
    # Verificar se o banco Python existe
    if not os.path.exists('radio.db'):
        print("📦 Criando banco de dados Python...")
        with app.app_context():
            db.create_all()
    
    # Configurações do MySQL (ajuste conforme necessário)
    mysql_config = {
        'db_host': 'localhost',
        'db_name': 'radio_web',
        'db_user': 'root',
        'db_pass': ''
    }
    
    # Conectar ao MySQL
    mysql_conn = connect_mysql(mysql_config)
    if not mysql_conn:
        print("⚠️  Não foi possível conectar ao MySQL")
        print("Criando apenas configurações padrão...")
        create_default_configs()
        return
    
    try:
        # Migrar dados
        print("\n📊 Iniciando migração...")
        
        migrate_users(mysql_conn)
        migrate_programming(mysql_conn)
        migrate_locutors(mysql_conn)
        migrate_banners(mysql_conn)
        migrate_configs(mysql_conn)
        
        # Criar configurações padrão se não existirem
        create_default_configs()
        
        print("\n✅ Migração concluída com sucesso!")
        print("🎵 Acesse http://localhost:5000 para ver o site")
        print("📱 Painel admin: http://localhost:5000/admin")
        
    except Exception as e:
        print(f"❌ Erro durante migração: {e}")
    finally:
        mysql_conn.close()

if __name__ == '__main__':
    main() 