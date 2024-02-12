#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import django


def main():
    
    """Run administrative tasks."""
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'Infin8.settings')


    try:
        django.setup()
        from django.core.management import call_command
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    
    call_command('makemigrations')
    call_command('migrate')
    execute_from_command_line([sys.argv[0], 'runserver', '0.0.0.0:8080'])


if __name__ == '__main__':
    main()
