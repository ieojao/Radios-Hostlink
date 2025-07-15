#!/usr/bin/env python3
"""
Script para limpar arquivos duplicados e manter apenas os mais recentes
"""

import os
from datetime import datetime
from app import app, db, Configuracao

def limpar_arquivos_duplicados():
    """Remove arquivos duplicados e mantém apenas os mais recentes"""
    
    with app.app_context():
        print("=== Verificando arquivos na pasta uploads/config ===")
        
        uploads_config_path = os.path.join('static', 'uploads', 'config')
        
        if not os.path.exists(uploads_config_path):
            print("Pasta não existe!")
            return
        
        arquivos = [f for f in os.listdir(uploads_config_path) if f != '.gitkeep']
        
        if not arquivos:
            print("Nenhum arquivo encontrado!")
            return
        
        print(f"Arquivos encontrados: {len(arquivos)}")
        for arquivo in arquivos:
            caminho_completo = os.path.join(uploads_config_path, arquivo)
            stat = os.stat(caminho_completo)
            data_modificacao = datetime.fromtimestamp(stat.st_mtime)
            print(f"  - {arquivo} (modificado em: {data_modificacao})")
        
        # Agrupar arquivos por tipo (baseado no nome original)
        grupos = {}
        for arquivo in arquivos:
            # Extrair o nome original do arquivo (após o UUID)
            partes = arquivo.split('_', 1)
            if len(partes) > 1:
                nome_original = partes[1]
                if nome_original not in grupos:
                    grupos[nome_original] = []
                grupos[nome_original].append(arquivo)
        
        print(f"\n=== Grupos de arquivos encontrados ===")
        for nome_original, arquivos_grupo in grupos.items():
            print(f"\nGrupo: {nome_original}")
            for arquivo in arquivos_grupo:
                caminho_completo = os.path.join(uploads_config_path, arquivo)
                stat = os.stat(caminho_completo)
                data_modificacao = datetime.fromtimestamp(stat.st_mtime)
                print(f"  - {arquivo} (modificado em: {data_modificacao})")
        
        # Manter apenas o arquivo mais recente de cada grupo
        print(f"\n=== Removendo arquivos duplicados ===")
        for nome_original, arquivos_grupo in grupos.items():
            if len(arquivos_grupo) > 1:
                # Ordenar por data de modificação (mais recente primeiro)
                arquivos_ordenados = sorted(arquivos_grupo, 
                    key=lambda x: os.stat(os.path.join(uploads_config_path, x)).st_mtime, 
                    reverse=True)
                
                # Manter o primeiro (mais recente) e remover os outros
                arquivo_manter = arquivos_ordenados[0]
                arquivos_remover = arquivos_ordenados[1:]
                
                print(f"\nMantendo: {arquivo_manter}")
                for arquivo in arquivos_remover:
                    caminho_remover = os.path.join(uploads_config_path, arquivo)
                    try:
                        os.remove(caminho_remover)
                        print(f"Removido: {arquivo}")
                    except Exception as e:
                        print(f"Erro ao remover {arquivo}: {e}")
        
        print(f"\n=== Verificando configurações no banco ===")
        
        # Verificar se os arquivos configurados no banco ainda existem
        logo_config = Configuracao.query.filter_by(chave='logo').first()
        favicon_config = Configuracao.query.filter_by(chave='favicon').first()
        
        if logo_config and logo_config.valor:
            caminho_logo = logo_config.valor.replace('/static/', '')
            caminho_completo_logo = os.path.join('static', caminho_logo)
            if os.path.exists(caminho_completo_logo):
                print(f"Logo OK: {logo_config.valor}")
            else:
                print(f"Logo não encontrado: {logo_config.valor}")
                # Procurar um arquivo de logo válido
                for arquivo in os.listdir(uploads_config_path):
                    if arquivo != '.gitkeep' and arquivo.lower().endswith(('.png', '.jpg', '.jpeg', '.gif')):
                        novo_caminho = f"/static/uploads/config/{arquivo}"
                        logo_config.valor = novo_caminho
                        print(f"Logo atualizado para: {novo_caminho}")
                        break
        
        if favicon_config and favicon_config.valor:
            caminho_favicon = favicon_config.valor.replace('/static/', '')
            caminho_completo_favicon = os.path.join('static', caminho_favicon)
            if os.path.exists(caminho_completo_favicon):
                print(f"Favicon OK: {favicon_config.valor}")
            else:
                print(f"Favicon não encontrado: {favicon_config.valor}")
                # Procurar um arquivo de favicon válido
                for arquivo in os.listdir(uploads_config_path):
                    if arquivo != '.gitkeep' and arquivo.lower().endswith(('.ico', '.png')):
                        novo_caminho = f"/static/uploads/config/{arquivo}"
                        favicon_config.valor = novo_caminho
                        print(f"Favicon atualizado para: {novo_caminho}")
                        break
        
        # Salvar alterações
        try:
            db.session.commit()
            print("\n=== Alterações salvas com sucesso! ===")
        except Exception as e:
            print(f"\nErro ao salvar alterações: {e}")
            db.session.rollback()

if __name__ == '__main__':
    limpar_arquivos_duplicados() 