"""
WSGI config for SaborReserva project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.2/howto/deployment/wsgi/
"""

import os
from SaborReserva import create_app  
from django.core.wsgi import get_wsgi_application

application = create_app()  # Or whatever function initializes your app

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SaborReserva.settings')

application = get_wsgi_application()
