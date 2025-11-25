"""
WSGI configuration for the 'karu' project.

Este arquivo expõe o callable WSGI usado por servidores compatíveis com
o padrão WSGI (como Gunicorn, uWSGI ou mod_wsgi) para executar o projeto.

Ele é carregado automaticamente pelos servidores WSGI durante o deploy.
Nenhuma lógica extra além da inicialização padrão do Django é necessária.
"""

import os
from django.core.wsgi import get_wsgi_application

# Define o módulo de configurações padrão do Django para o ambiente WSGI.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'karu.settings')

# Cria a aplicação WSGI que será usada pelo servidor.
application = get_wsgi_application()
