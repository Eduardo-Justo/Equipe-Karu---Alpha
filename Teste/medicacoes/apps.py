from django.apps import AppConfig


class MedicacoesConfig(AppConfig):
    """
    Configuração principal do aplicativo 'medicacoes'.

    Esta classe informa ao Django como inicializar a aplicação,
    incluindo qual tipo de campo usar como padrão para chaves primárias
    e o nome do módulo onde o app está localizado.
    """
    default_auto_field = 'django.db.models.BigAutoField'  # Usa BigAutoField como padrão para IDs
    name = 'medicacoes'  # Nome da aplicação dentro do projeto
