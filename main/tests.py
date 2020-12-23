from ucabSports.wsgi import *

from main.models import Post


post = Post(titulo='Post de prueba', resumen='asdasdasd', cuerpo='más asd')
post.save()
print('Post guardado')


