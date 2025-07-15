#!/usr/bin/env python3
"""
Script para verificar as configurações atuais no banco de dados
"""

from app import app, db, Configuracao

def verificar_configuracoes():
    """Verifica as configurações atuais no banco de dados"""
    
    with app.app_context():
        print("=== Configurações atuais no banco de dados ===")
        
        # Buscar todas as configurações
        configs = Configuracao.query.all()
        
        for config in configs:
            print(f"{config.chave}: {config.valor}")
        
        print("\n=== Verificando logo e favicon especificamente ===")
        
        logo_config = Configuracao.query.filter_by(chave='logo').first()
        favicon_config = Configuracao.query.filter_by(chave='favicon').first()
        
        if logo_config:
            print(f"Logo: {logo_config.valor}")
        else:
            print("Logo: não encontrado")
            
        if favicon_config:
            print(f"Favicon: {favicon_config.valor}")
        else:
            print("Favicon: não encontrado")

if __name__ == '__main__':
    verificar_configuracoes() 