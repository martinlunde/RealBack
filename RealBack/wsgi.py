"""
WSGI config for RealBack project.

It exposes the WSGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/howto/deployment/wsgi/
"""

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "RealBack.settings")
application = get_wsgi_application()


if os.getenv('DJANGO_PRODUCTION') is not None:
    from whitenoise.django import DjangoWhiteNoise
    application = DjangoWhiteNoise(application)
