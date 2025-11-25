"""
ASGI configuration for the 'karu' project.

Este arquivo expõe o callable ASGI utilizado para executar o
projeto em servidores assíncronos (como Daphne, Uvicorn ou Hypercorn).

Ele é carregado automaticamente quando o projeto roda em modo ASGI.
Nenhuma lógica adicional é necessária aqui — apenas configuração padrão.
"""

import os
from django.core.asgi import get_asgi_application

# Define o módulo de configurações padrão do Django para o ambiente ASGI.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'karu.settings')

# Cria a aplicação ASGI que será usada pelo servidor.
application = get_asgi_application()

