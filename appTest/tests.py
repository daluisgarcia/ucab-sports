#from ucabSports.wsgi import *

import os

from django.core.wsgi import get_wsgi_application

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ucabSports.settings')

application = get_wsgi_application()

from appTest.models import Posts


post = Posts(titulo='Post de prueba', resumen='asdasdasd', cuerpo='más asd')
post.save()
print('Post guardado')


