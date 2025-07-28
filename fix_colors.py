#!/usr/bin/env python3
"""
Script para corrigir as cores para o esquema roxo, azul e branco
"""

import os
import re

def fix_colors_in_file(file_path):
    """Corrige as cores em um arquivo específico"""
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Mapeamento de cores para roxo, azul e branco
    color_mappings = [
        # Substituir rosa por roxo
        (r'#f093fb', '#8b5cf6'),  # Rosa para roxo
        (r'#e91e63', '#7c3aed'),  # Rosa escuro para roxo escuro
        (r'#f5576c', '#6366f1'),  # Rosa vermelho para azul
        
        # RGBA rosa para roxo
        (r'rgba\(240, 147, 251,', 'rgba(139, 92, 246,'),
        (r'rgba\(245, 87, 108,', 'rgba(99, 102, 241,'),
        
        # Gradientes com rosa para roxo
        (r'linear-gradient\(45deg, #764ba2, #f093fb\)', 'linear-gradient(45deg, #764ba2, #8b5cf6)'),
        (r'linear-gradient\(135deg, #667eea, #764ba2, #f093fb\)', 'linear-gradient(135deg, #667eea, #764ba2, #8b5cf6)'),
        
        # Sombras com rosa para roxo
        (r'rgba\(240, 147, 251, 0\.4\)', 'rgba(139, 92, 246, 0.4)'),
        (r'rgba\(240, 147, 251, 0\.3\)', 'rgba(139, 92, 246, 0.3)'),
    ]
    
    # Aplicar substituições
    for old_color, new_color in color_mappings:
        content = re.sub(old_color, new_color, content, flags=re.IGNORECASE)
    
    # Escrever de volta
    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    
    print(f"✅ {file_path} corrigido!")

def main():
    """Função principal"""
    print("🎨 Corrigindo cores para roxo, azul e branco...")
    
    # Lista de arquivos para corrigir
    files = [
        'static/css/styles.css',
        'static/css/admin.css',
        'static/css/player-enhanced.css',
        'static/css/mobile-responsive.css',
        'backup-player-antigo/player.css',
        'backup-player-antigo/player.js',
        'backup-player-antigo/player-config.js'
    ]
    
    # Corrigir arquivos
    for file_path in files:
        if os.path.exists(file_path):
            fix_colors_in_file(file_path)
        else:
            print(f"⚠️ Arquivo não encontrado: {file_path}")
    
    print("\n🎉 Cores corrigidas com sucesso!")
    print("\n📋 Esquema de cores final:")
    print("• Azul: #667eea (principal)")
    print("• Roxo: #764ba2 (secundário)")
    print("• Roxo Vibrante: #8b5cf6 (destaque)")
    print("• Branco: #ffffff (elementos claros)")

if __name__ == "__main__":
    main() 