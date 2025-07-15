#!/usr/bin/env python3
"""
Script para corrigir caminhos de arquivos no banco de dados
"""

import os
import sys
from app import app, db, Configuracao

def corrigir_caminhos_arquivos():
    """Corrige os caminhos dos arquivos no banco de dados"""
    
    with app.app_context():
        # Buscar configurações de logo e favicon
        logo_config = Configuracao.query.filter_by(chave='logo').first()
        favicon_config = Configuracao.query.filter_by(chave='favicon').first()
        
        print("=== Verificando configurações atuais ===")
        
        if logo_config:
            print(f"Logo atual: {logo_config.valor}")
        else:
            print("Logo: não encontrado")
            
        if favicon_config:
            print(f"Favicon atual: {favicon_config.valor}")
        else:
            print("Favicon: não encontrado")
        
        print("\n=== Verificando arquivos na pasta uploads ===")
        
        # Verificar arquivos na pasta uploads/config
        uploads_config_path = os.path.join('static', 'uploads', 'config')
        if os.path.exists(uploads_config_path):
            arquivos = os.listdir(uploads_config_path)
            print(f"Arquivos encontrados em {uploads_config_path}:")
            for arquivo in arquivos:
                if arquivo != '.gitkeep':
                    print(f"  - {arquivo}")
        else:
            print(f"Pasta {uploads_config_path} não existe")
        
        print("\n=== Corrigindo caminhos ===")
        
        # Corrigir logo se necessário
        if logo_config and logo_config.valor:
            caminho_atual = logo_config.valor
            
            # Se o caminho não começa com /static/, corrigir
            if not caminho_atual.startswith('/static/'):
                # Verificar se é um arquivo local
                if not caminho_atual.startswith('http'):
                    # Procurar o arquivo na pasta uploads
                    nome_arquivo = os.path.basename(caminho_atual)
                    for arquivo in os.listdir(uploads_config_path):
                        if arquivo != '.gitkeep' and nome_arquivo in arquivo:
                            novo_caminho = f"/static/uploads/config/{arquivo}"
                            logo_config.valor = novo_caminho
                            print(f"Logo corrigido: {caminho_atual} -> {novo_caminho}")
                            break
                    else:
                        print(f"Arquivo de logo não encontrado: {caminho_atual}")
        
        # Corrigir favicon se necessário
        if favicon_config and favicon_config.valor:
            caminho_atual = favicon_config.valor
            
            # Se o caminho não começa com /static/, corrigir
            if not caminho_atual.startswith('/static/'):
                # Verificar se é um arquivo local
                if not caminho_atual.startswith('http'):
                    # Procurar o arquivo na pasta uploads
                    nome_arquivo = os.path.basename(caminho_atual)
                    for arquivo in os.listdir(uploads_config_path):
                        if arquivo != '.gitkeep' and nome_arquivo in arquivo:
                            novo_caminho = f"/static/uploads/config/{arquivo}"
                            favicon_config.valor = novo_caminho
                            print(f"Favicon corrigido: {caminho_atual} -> {novo_caminho}")
                            break
                    else:
                        print(f"Arquivo de favicon não encontrado: {caminho_atual}")
        
        # Salvar alterações
        try:
            db.session.commit()
            print("\n=== Alterações salvas com sucesso! ===")
        except Exception as e:
            print(f"\nErro ao salvar alterações: {e}")
            db.session.rollback()
        
        print("\n=== Configurações finais ===")
        
        if logo_config:
            print(f"Logo: {logo_config.valor}")
        if favicon_config:
            print(f"Favicon: {favicon_config.valor}")

if __name__ == '__main__':
    corrigir_caminhos_arquivos() 