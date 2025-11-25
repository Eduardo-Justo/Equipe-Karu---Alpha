#!/usr/bin/env python
"""
Ponto de entrada para ferramentas administrativas do Django.

Este script é usado para executar comandos como:
- executar o servidor de desenvolvimento
- aplicar migrações
- criar superusuários
- executar shells interativos

Ele simplesmente configura o ambiente Django e repassa
os argumentos de linha de comando para o Django.
"""

import os
import sys


def main():
    """
    Executa tarefas administrativas do Django.

    Define o módulo de configurações padrão e delega
    a execução dos comandos para o Django.
    """
    # Define o módulo de configurações caso não esteja definido.
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'karu.settings')

    try:
        # Importa o executor de comandos do Django.
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        # Erro comum quando Django não está instalado ou o venv não está ativado.
        raise ImportError(
            "Não foi possível importar o Django. "
            "Verifique se ele está instalado e disponível no PYTHONPATH "
            "e se o ambiente virtual está ativado."
        ) from exc

    # Executa o comando passado na linha de comando.
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    # Executa o script principal ao chamar diretamente este arquivo.
    main()
