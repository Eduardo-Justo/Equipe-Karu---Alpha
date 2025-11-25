"""
Configurações principais do projeto Django 'karu'.

Este arquivo define:
- Aplicações instaladas
- Middleware
- Templates
- Banco de dados
- Configurações de autenticação
- Configurações de arquivos estáticos
- Configurações de segurança e CSRF
- Ajustes automáticos para Codespaces

IMPORTANTE:
Nenhuma lógica foi alterada. Apenas docstrings e comentários de organização foram adicionados.
"""

from pathlib import Path
import os  # Necessário para detectar Codespaces dinamicamente

# Diretório base do projeto (usado como referência para caminhos relativos)
BASE_DIR = Path(__file__).resolve().parent.parent


# ----------------------------- #
# Configurações de Segurança
# ----------------------------- #

# Chave secreta utilizada pelo Django para operações criptográficas.
# Em produção, ela deve ser mantida em segredo absoluto.
SECRET_KEY = 'django-insecure-0q83b4$yw28eo%10j%$gpz#orju8088uc(z^28i06tv*hb7$7&'

# Debug ativado (apenas para desenvolvimento).
DEBUG = True

# Hosts permitidos para o backend.
# Em ambiente local geralmente fica vazio.
ALLOWED_HOSTS = []


# ----------------------------- #
# Aplicativos Instalados
# ----------------------------- #

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # App local responsável pela lógica de medicamentos
    'medicacoes.apps.MedicacoesConfig'
]


# ----------------------------- #
# Middleware (camadas de processamento)
# ----------------------------- #

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',  # Proteção CSRF
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]


# ----------------------------- #
# Arquivo principal de URLs
# ----------------------------- #

ROOT_URLCONF = 'karu.urls'


# ----------------------------- #
# Templates
# ----------------------------- #

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',

        # Diretórios de templates adicionais (vazio por padrão)
        'DIRS': [],

        'APP_DIRS': True,  # Permite carregar templates da pasta /templates dos apps
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]


# ----------------------------- #
# WSGI
# ----------------------------- #

WSGI_APPLICATION = 'karu.wsgi.application'


# ----------------------------- #
# Banco de Dados
# ----------------------------- #

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Banco padrão para testes
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}


# ----------------------------- #
# Validação de Senhas
# ----------------------------- #

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]


# ----------------------------- #
# Internacionalização
# ----------------------------- #

LANGUAGE_CODE = 'en-us'

# Fuso horário configurado para Maceió
TIME_ZONE = 'America/Maceio'

USE_I18N = True
USE_TZ = True


# ----------------------------- #
# Arquivos Estáticos
# ----------------------------- #

# Caminho padrão para arquivos estáticos
STATIC_URL = 'static/'


# ----------------------------- #
# Configuração do Primary Key padrão
# ----------------------------- #

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# ----------------------------- #
# CSRF — Origens confiáveis
# Usado para evitar erros em ambientes de desenvolvimento remotos (Ex.: Codespaces)
# ----------------------------- #

CSRF_TRUSTED_ORIGINS = [
    'https://localhost:8000',
    'http://localhost:8000',
    'https://localhost:8001',
    'http://localhost:8001',
    'http://127.0.0.1:8000',
    'http://127.0.0.1:8001',
    'https://opulent-space-halibut-wrggw5xwwppv25pxg-8001.app.github.dev'
]

# Adiciona automaticamente o domínio do Codespace, caso exista
if 'CODESPACE_NAME' in os.environ:
    codespace_name = os.environ['CODESPACE_NAME']

    # Porta principal (8000)
    CSRF_TRUSTED_ORIGINS.append(f"https://{codespace_name}-8000.app.github.dev")

    # Porta alternativa (8001)
    CSRF_TRUSTED_ORIGINS.append(f"https://{codespace_name}-8001.app.github.dev")



# ----------------------------- #
# Configurações de Login
# ----------------------------- #

# URL para onde o usuário será redirecionado quando tentar acessar algo sem login
LOGIN_URL = '/login/'

# Página inicial após o login
LOGIN_REDIRECT_URL = '/'

# Redirecionamento após logout
LOGOUT_REDIRECT_URL = '/login/'

# Armazenamento de mensagens do Django
MESSAGE_STORAGE = 'django.contrib.messages.storage.session.SessionStorage'