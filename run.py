#!/usr/bin/env python3
"""
Arquivo principal da aplicação Radios Hostlink
Usando arquitetura modular e factory pattern
"""

import os
import sys
from app_factory import create_app
from models.database import db
from models.user import Usuario
from models.content import Programacao, Locutor, Banner, Destaque, Configuracao
from models.pages import PaginaRadio, PaginaEquipe, PaginaContato, MensagemContato
from werkzeug.security import generate_password_hash
import json

def init_database():
    """Inicializa o banco de dados com dados padrão"""
    with app.app_context():
        # Criar todas as tabelas
        db.create_all()
        
        # Criar usuário admin padrão se não existir
        if not Usuario.query.filter_by(email='admin@radioshostlink.com.br').first():
            admin = Usuario(
                nome='Administrador',
                email='admin@radioshostlink.com.br',
                nivel='admin',
                ativo=True
            )
            admin.set_password('admin123')
            db.session.add(admin)
            db.session.commit()
            print("✅ Usuário admin criado: admin@radioshostlink.com.br / admin123")
        
        # Criar página "A Rádio" padrão se não existir
        if not PaginaRadio.query.first():
            pagina_radio = PaginaRadio(
                titulo='Radios Hostlink',
                subtitulo='Conectando pessoas através da música e informação',
                descricao='Somos uma rádio comprometida em levar entretenimento de qualidade, notícias relevantes e música que inspira. Nossa missão é ser a voz da comunidade, conectando pessoas e criando momentos especiais através do rádio.',
                historia='Fundada com o propósito de servir a comunidade, nossa rádio nasceu da paixão pela música e pelo jornalismo. Ao longo dos anos, construímos uma história de dedicação e compromisso com nossos ouvintes, sempre buscando inovar e oferecer o melhor conteúdo.',
                missao='Levar entretenimento de qualidade, informação relevante e música que inspire e conecte pessoas, sendo uma referência em comunicação e cultura em nossa região.',
                visao='Ser reconhecida como a rádio mais querida e confiável da região, referência em qualidade de programação e compromisso com a comunidade.',
                valores='Qualidade\nCompromisso\nInovação\nComunidade\nTransparência',
                estatisticas=json.dumps({
                    'estatistica_1': {'titulo': 'Anos no Ar', 'valor': '25'},
                    'estatistica_2': {'titulo': 'Ouvintes Diários', 'valor': '50000'},
                    'estatistica_3': {'titulo': 'Programas', 'valor': '15'},
                    'estatistica_4': {'titulo': 'Locutores', 'valor': '8'}
                })
            )
            db.session.add(pagina_radio)
            print("✅ Página 'A Rádio' criada")
        
        # Criar página "Equipe" padrão se não existir
        if not PaginaEquipe.query.first():
            pagina_equipe = PaginaEquipe(
                titulo='Nossa Equipe',
                subtitulo='Conheça os profissionais que fazem a diferença',
                descricao='Nossa equipe é composta por profissionais apaixonados por rádio e comunicação, dedicados a trazer o melhor conteúdo para nossos ouvintes.',
                mensagem_equipe='Trabalhamos juntos para criar uma experiência única e envolvente para nossa audiência.',
                estatisticas_equipe=json.dumps({
                    'estatistica_equipe_1': {'titulo': 'Anos de Experiência', 'valor': '15+'},
                    'estatistica_equipe_2': {'titulo': 'Profissionais', 'valor': '25+'},
                    'estatistica_equipe_3': {'titulo': 'Programas', 'valor': '50+'},
                    'estatistica_equipe_4': {'titulo': 'Prêmios', 'valor': '10+'}
                }),
                areas_atuacao=json.dumps({
                    'area_1': {'titulo': 'Jornalismo', 'descricao': 'Cobertura de notícias locais e nacionais'},
                    'area_2': {'titulo': 'Entretenimento', 'descricao': 'Programas de música e entretenimento'},
                    'area_3': {'titulo': 'Esportes', 'descricao': 'Cobertura esportiva completa'},
                    'area_4': {'titulo': 'Tecnologia', 'descricao': 'Inovação e tendências tecnológicas'},
                    'area_5': {'titulo': 'Cultura', 'descricao': 'Arte, literatura e eventos culturais'},
                    'area_6': {'titulo': 'Comunidade', 'descricao': 'Projetos sociais e comunitários'}
                }),
                convite_equipe='Quer fazer parte da nossa equipe? Entre em contato conosco! Oferecemos oportunidades de crescimento e um ambiente colaborativo.'
            )
            db.session.add(pagina_equipe)
            print("✅ Página 'Equipe' criada")
        
        # Criar página de contato padrão se não existir
        if not PaginaContato.query.first():
            pagina_contato = PaginaContato(
                titulo='Entre em Contato',
                subtitulo='Estamos aqui para ajudar. Entre em contato conosco!',
                descricao='Tem alguma dúvida, sugestão ou quer fazer parte da nossa equipe? Entre em contato conosco através do formulário abaixo ou pelos nossos canais de atendimento.',
                telefone_principal='(11) 99999-9999',
                telefone_secundario='(11) 88888-8888',
                email_contato='contato@radioshostlink.com.br',
                endereco='Rua das Rádios, 123\nBairro Central\nSão Paulo - SP, 01234-567',
                horario_funcionamento='Segunda a Sexta: 8h às 18h\nSábado: 9h às 14h\nDomingo: Fechado',
                redes_sociais=json.dumps({
                    'facebook': 'https://facebook.com/radioshostlink',
                    'instagram': 'https://instagram.com/radioshostlink',
                    'twitter': 'https://twitter.com/radioshostlink',
                    'youtube': 'https://youtube.com/radioshostlink'
                }),
                mapa_embed='<iframe src="https://www.google.com/maps/embed?pb=!1m18!1m12!1m3!1d3657.1234567890123!2d-46.6388!3d-23.5505!2m3!1f0!2f0!3f0!3m2!1i1024!2i768!4f13.1!3m3!1m2!1s0x0%3A0x0!2zMjPCsDMzJzAxLjgiUyA0NsKwMzgnMTkuNyJX!5e0!3m2!1spt-BR!2sbr!4v1234567890123" width="100%" height="300" style="border:0;" allowfullscreen="" loading="lazy"></iframe>'
            )
            db.session.add(pagina_contato)
            print("✅ Página 'Contato' criada")
        
        db.session.commit()
        print("✅ Banco de dados inicializado com sucesso!")

def main():
    """Função principal"""
    global app
    
    # Criar aplicação
    app = create_app()
    
    # Verificar argumentos de linha de comando
    if len(sys.argv) > 1:
        command = sys.argv[1]
        
        if command == 'init-db':
            print("🔄 Inicializando banco de dados...")
            init_database()
            return
        elif command == 'run':
            print("🚀 Iniciando servidor de desenvolvimento...")
            app.run(debug=True, host='0.0.0.0', port=5000)
            return
        elif command == 'help':
            print("""
📋 Comandos disponíveis:

  python run.py init-db    - Inicializa o banco de dados
  python run.py run        - Inicia o servidor de desenvolvimento
  python run.py help       - Mostra esta ajuda

🔧 Configuração:
  - Configure as variáveis de ambiente no arquivo config.env
  - Acesse o painel admin em: http://localhost:5000/admin
  - Credenciais padrão: admin@radioshostlink.com.br / admin123

🎯 Funcionalidades:
  - Site público responsivo
  - Painel administrativo completo
  - API REST para integrações
  - Sistema de programação dinâmica
  - Gerenciamento de conteúdo
            """)
            return
        else:
            print(f"❌ Comando '{command}' não reconhecido.")
            print("Use 'python run.py help' para ver os comandos disponíveis.")
            return
    
    # Comportamento padrão: inicializar banco e rodar servidor
    print("🚀 Iniciando Radios Hostlink...")
    init_database()
    print("🌐 Servidor disponível em: http://localhost:5000")
    print("🔧 Painel admin em: http://localhost:5000/admin")
    app.run(debug=True, host='0.0.0.0', port=5000)

if __name__ == '__main__':
    main() 