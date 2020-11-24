
import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ucabSports.settings')

application = get_wsgi_application()

"""
from ucabSports.wsgi import *
"""

from .models import Posts


post = Posts(titulo='Post de prueba', resumen='asdasdasd', cuerpo='más asd')
post.save()
print('Post guardado')


