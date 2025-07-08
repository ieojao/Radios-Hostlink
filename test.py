#!/usr/bin/env python3
"""
Arquivo de teste para verificar se o Python está funcionando no cPanel
"""

def application(environ, start_response):
    """WSGI application simples para teste"""
    status = '200 OK'
    headers = [('Content-type', 'text/html; charset=utf-8')]
    
    html = """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Teste Python - cPanel</title>
        <meta charset="utf-8">
    </head>
    <body>
        <h1>✅ Python está funcionando!</h1>
        <p>Se você está vendo esta página, o Python está configurado corretamente no seu servidor cPanel.</p>
        <h2>Informações do Sistema:</h2>
        <ul>
            <li><strong>Python Version:</strong> {python_version}</li>
            <li><strong>Current Directory:</strong> {current_dir}</li>
            <li><strong>Script Name:</strong> {script_name}</li>
        </ul>
        <hr>
        <p><a href="/site/">← Voltar para o site principal</a></p>
    </body>
    </html>
    """.format(
        python_version=__import__('sys').version,
        current_dir=__import__('os').getcwd(),
        script_name=environ.get('SCRIPT_NAME', 'N/A')
    )
    
    start_response(status, headers)
    return [html.encode('utf-8')] 