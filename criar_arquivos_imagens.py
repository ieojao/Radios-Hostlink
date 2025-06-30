#!/usr/bin/env python3
"""
Script para verificar e criar arquivos de imagem necessários para o site
"""

import os
import shutil
from pathlib import Path

def criar_arquivos_imagens():
    """Cria os arquivos de imagem necessários se não existirem"""
    
    # Pasta de imagens
    images_dir = Path("static/images")
    images_dir.mkdir(exist_ok=True)
    
    # Lista de arquivos necessários
    arquivos_necessarios = {
        "logo.png": "Logo do site (recomendado: 200x80px)",
        "favicon.ico": "Ícone do site (recomendado: 32x32px)",
        "programa.jpg": "Imagem padrão da programação (recomendado: 400x300px)",
        "destaque1.jpg": "Imagem de destaque 1 (recomendado: 400x300px)",
        "destaque2.jpg": "Imagem de destaque 2 (recomendado: 400x300px)",
        "destaque3.jpg": "Imagem de destaque 3 (recomendado: 400x300px)"
    }
    
    print("🔍 Verificando arquivos de imagem...")
    
    for arquivo, descricao in arquivos_necessarios.items():
        caminho_arquivo = images_dir / arquivo
        
        if not caminho_arquivo.exists():
            print(f"❌ {arquivo} não encontrado")
            
            # Criar arquivo placeholder
            if arquivo.endswith('.ico'):
                # Para favicon, criar um SVG inline como fallback
                conteudo = f"""# Placeholder para {arquivo}
# {descricao}
# Substitua por um arquivo .ico real
# Você pode criar um favicon em: https://favicon.io/"""
            else:
                conteudo = f"""# Placeholder para {arquivo}
# {descricao}
# Substitua por uma imagem real (.png, .jpg, .svg)
# Dimensões recomendadas: {descricao.split('(')[1].split(')')[0] if '(' in descricao else 'adequadas'}"""
            
            with open(caminho_arquivo, 'w', encoding='utf-8') as f:
                f.write(conteudo)
            
            print(f"✅ Criado placeholder para {arquivo}")
        else:
            print(f"✅ {arquivo} encontrado")
    
    print("\n📋 Resumo:")
    print("=" * 50)
    print("Arquivos criados como placeholders. Para usar imagens reais:")
    print("1. Substitua os arquivos .txt por imagens reais")
    print("2. Use os nomes exatos: logo.png, favicon.ico, etc.")
    print("3. Para favicon: use https://favicon.io/")
    print("4. Para logos: use editores online ou ferramentas de design")
    print("\n📁 Pasta de imagens: static/images/")

def verificar_configuracoes():
    """Verifica se as configurações estão corretas"""
    print("\n🔧 Verificando configurações...")
    
    # Verificar se o banco de dados existe
    if os.path.exists("instance/radio.db"):
        print("✅ Banco de dados encontrado")
    else:
        print("❌ Banco de dados não encontrado")
        print("   Execute: python app.py para criar o banco")
    
    # Verificar configurações padrão
    configs_padrao = {
        'logo': 'logo.png',
        'favicon': 'favicon.ico'
    }
    
    print("\n📝 Configurações padrão:")
    for chave, valor in configs_padrao.items():
        print(f"   {chave}: {valor}")

def main():
    """Função principal"""
    print("🎨 Criador de Arquivos de Imagem - Radios Hostlink")
    print("=" * 50)
    
    criar_arquivos_imagens()
    verificar_configuracoes()
    
    print("\n🎉 Processo concluído!")
    print("\n💡 Próximos passos:")
    print("1. Substitua os placeholders por imagens reais")
    print("2. Reinicie o servidor: python app.py")
    print("3. Acesse o site para ver as mudanças")

if __name__ == "__main__":
    main() 