#!/usr/bin/env python3
"""
Script para verificar e corrigir o formato do favicon
"""

import os
from PIL import Image
from app import app, db, Configuracao

def verificar_favicon():
    """Verifica e corrige o formato do favicon"""
    
    with app.app_context():
        favicon_config = Configuracao.query.filter_by(chave='favicon').first()
        
        if not favicon_config or not favicon_config.valor:
            print("Favicon não configurado")
            return
        
        caminho_favicon = favicon_config.valor
        
        # Remover /static/ do início se existir
        if caminho_favicon.startswith('/static/'):
            caminho_fisico = caminho_favicon[8:]  # Remove '/static/'
        else:
            caminho_fisico = caminho_favicon
        
        caminho_completo = os.path.join('static', caminho_fisico)
        
        print(f"Verificando favicon: {caminho_completo}")
        
        if not os.path.exists(caminho_completo):
            print("Arquivo não encontrado!")
            return
        
        # Verificar extensão
        nome_arquivo = os.path.basename(caminho_completo)
        extensao = os.path.splitext(nome_arquivo)[1].lower()
        
        print(f"Extensão atual: {extensao}")
        
        # Se não for .ico ou .png, converter
        if extensao not in ['.ico', '.png']:
            print("Convertendo favicon para PNG...")
            
            try:
                # Abrir imagem
                with Image.open(caminho_completo) as img:
                    # Redimensionar para 32x32 se necessário
                    if img.size != (32, 32):
                        img = img.resize((32, 32), Image.Resampling.LANCZOS)
                    
                    # Criar novo nome de arquivo
                    novo_nome = os.path.splitext(nome_arquivo)[0] + '.png'
                    novo_caminho_fisico = os.path.join('uploads', 'config', novo_nome)
                    novo_caminho_completo = os.path.join('static', novo_caminho_fisico)
                    
                    # Salvar como PNG
                    img.save(novo_caminho_completo, 'PNG')
                    
                    # Atualizar no banco de dados
                    novo_caminho_url = f"/static/{novo_caminho_fisico}"
                    favicon_config.valor = novo_caminho_url
                    db.session.commit()
                    
                    # Deletar arquivo antigo
                    os.remove(caminho_completo)
                    
                    print(f"Favicon convertido: {nome_arquivo} -> {novo_nome}")
                    print(f"Novo caminho: {novo_caminho_url}")
                    
            except Exception as e:
                print(f"Erro ao converter favicon: {e}")
        else:
            print("Favicon já está no formato correto")
            
            # Verificar tamanho
            try:
                with Image.open(caminho_completo) as img:
                    print(f"Tamanho atual: {img.size}")
                    if img.size != (32, 32):
                        print("Recomendação: Favicon deveria ter 32x32 pixels para melhor compatibilidade")
            except Exception as e:
                print(f"Erro ao verificar tamanho: {e}")

if __name__ == '__main__':
    verificar_favicon() 