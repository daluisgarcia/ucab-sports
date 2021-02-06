from django.db import models
from datetime import datetime
from django.conf import settings

'''
  PERSON MODEL
'''
class Person(models.Model):
  cedula = models.CharField(max_length=10, verbose_name='Cédula')
  nombre = models.CharField(max_length=50, verbose_name='Nombre')
  apellido = models.CharField(max_length=50, verbose_name='Apellido')
  correo = models.EmailField(max_length=100, verbose_name='Email')
  nickname = models.CharField(max_length=30, blank=True, verbose_name='Nickname')
  
  def __str__(self):
    return self.nombre

  class Meta:
    verbose_name = 'Usuario'
    verbose_name_plural = 'Usuarios'


#Revisar luego para cambiar el upload_to
'''
  Team MODEL
'''
class Team(models.Model):
  nombre = models.CharField(max_length=30, verbose_name='Nombre')
  logo = models.ImageField(upload_to='team_logos', null=True, blank=True)

  def __str__(self):
    return self.nombre

  class Meta:
    verbose_name = 'Equipo'
    verbose_name_plural = 'Equipos'


'''
  STAGE MODEL
'''
class Stage(models.Model):
  nombre = models.CharField(max_length=30, verbose_name='Nombre')
  descripcion = models.CharField(max_length=100, verbose_name='Descripción')

  def __str__(self):
    return self.nombre

  class Meta:
    verbose_name = 'Modalidad de Fase'
    verbose_name_plural = 'Modalidades de Fase'


'''
  GAME MODEL
'''
class Game(models.Model):
  nombre = models.CharField(max_length=30, verbose_name='Nombre')

  def __str__(self):
    return self.nombre

  class Meta:
    verbose_name = 'Juego'
    verbose_name_plural = 'Juegos'


'''
  TOURNAMENT MODEL
'''
class Tournament(models.Model):
  nombre = models.CharField(max_length=30, verbose_name='Nombre')
  fecha_inicio = models.DateField(verbose_name='Fecha de inicio')
  fecha_fin = models.DateField(verbose_name='Fecha de fin')
  inscripcion_abierta = models.BooleanField(default=True)
  edicion = models.SmallIntegerField(verbose_name='Edición')
  DELEGADO = (
    ('d','delegado'),
    ('jd','delegado y jugador')
  )
  tipo_delegado = models.CharField(max_length=2, choices=DELEGADO, verbose_name='Tipo de delegado', default='d')
  id_juego = models.ForeignKey(Game, verbose_name='Tipo de juego', on_delete=models.SET_NULL, null=True, blank=True)
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")

  def __str__(self):
    return self.nombre

  class Meta:
    verbose_name = 'Torneo'
    verbose_name_plural = 'Torneos'


'''
  POST MODEL
'''
class Post(models.Model):
  titulo = models.CharField(max_length=50, verbose_name='Título')
  cuerpo = models.CharField(max_length=400, verbose_name='Contenido')
  imagen = models.ImageField(upload_to='post_images', null=True, blank=True)
  owner = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, default="")

  def __str__(self):
    return self.titulo

  class Meta:
    verbose_name = 'Post'
    verbose_name_plural = 'Posts'


'''
  HISTORY PARTICIPATION MODEL
'''
class HistoryParticipation(models.Model):
  ROLES = (
    ('j','jugador'),
    ('d','delegado'),
    ('jd','delegado y jugador')
  )
  id_persona = models.ForeignKey(Person, on_delete=models.CASCADE)
  id_equipo = models.ForeignKey(Team, on_delete=models.CASCADE)
  id_torneo = models.ForeignKey(Tournament, on_delete=models.CASCADE)
  fecha_registro = models.DateField(verbose_name='Fecha de Registro')
  fecha_fin = models.DateField(verbose_name='Fecha de Registro', null=True, blank=True)
  rol = models.CharField(max_length=2, choices=ROLES, verbose_name='Rol')

  def __str__(self):
    return self.rol


'''
  STAGE TOURNAMENT MODEL
'''
class StageTournament(models.Model):
  id_fase = models.ForeignKey(Stage, on_delete=models.CASCADE, null=True)
  id_torneo = models.ForeignKey(Tournament, on_delete=models.CASCADE)
  jerarquia = models.SmallIntegerField(verbose_name='Jerarquia')
  participantes_por_equipo = models.SmallIntegerField(verbose_name='Participantes por equipo')
  equipos_por_partido = models.SmallIntegerField(verbose_name='Equipos por partido')
  num_grupos = models.SmallIntegerField(verbose_name='Numero de grupos', null=True, blank=True)
  equipos_por_grupo = models.SmallIntegerField(verbose_name='Equipos por grupo', null=True, blank=True)


'''
  MATCH MODEL
'''
class Match(models.Model):
  fecha = models.DateField(verbose_name='Fecha del partido')
  direccion = models.CharField(max_length=100, null=True, blank=True, verbose_name='Dirección')
  id_fase_torneo = models.ForeignKey(StageTournament, on_delete=models.SET_NULL, null=True, blank=True)

  def __str__(self):
    return 'Partido del torneo: %s' % (self.id_fase_torneo.id_torneo.nombre)

  class Meta:
    verbose_name = 'Partido'
    verbose_name_plural = 'Partidos'


'''
  PARTICIPATION MODEL
'''
class Participation(models.Model):
  id_equipo = models.ForeignKey(Team, on_delete=models.CASCADE)
  id_partido = models.ForeignKey(Match, on_delete=models.CASCADE)
  ganador = models.BooleanField(null=True, blank=True)
  puntos_equipo = models.IntegerField(verbose_name='Puntos del equipo', null=True, blank=True)

  def __str__(self):
    return 'Puntaje del equipo %s: %s' % (self.id_equipo.nombre,self.puntos_equipo)

  class Meta:
    verbose_name = 'Partido'
    verbose_name_plural = 'Partidos'


'''
  CLASSIFIED MODEL
'''
class Classified(models.Model):
  id_equipo = models.ForeignKey(Team, on_delete=models.CASCADE)
  id_fase_torneo = models.ForeignKey(StageTournament, on_delete=models.CASCADE)
  grupo = models.CharField(max_length=1, verbose_name='Grupo', null=True)


'''
  PRE-PERSON MODEL
'''
class PrePerson(models.Model):
  cedula = models.CharField(max_length=10, verbose_name='Cédula')
  nombre = models.CharField(max_length=50, verbose_name='Nombre')
  apellido = models.CharField(max_length=50, verbose_name='Apellido')
  correo = models.EmailField(max_length=100, verbose_name='Email')
  nickname = models.CharField(max_length=30, blank=True, verbose_name='Nickname')
  
  def __str__(self):
    return self.nombre

  class Meta:
    verbose_name = 'Usuario'
    verbose_name_plural = 'Usuarios'


'''
  PRE-TEAM MODEL
'''
class PreTeam(models.Model):
  nombre = models.CharField(max_length=30, verbose_name='Nombre')
  logo = models.ImageField(upload_to='logos/%Y/%m/%d', null=True, blank=True)
  comentario = models.CharField(max_length=150, verbose_name='Comentario (opcional)', null=True, blank=True)
  
  def __str__(self):
    return self.nombre

  class Meta:
    verbose_name = 'Equipo'
    verbose_name_plural = 'Equipos'


'''
  PRE-TEAM REGISTER MODEL
'''
class PreTeamRegister(models.Model):
  ROLES = (
    ('j','jugador'),
    ('d','delegado'),
    ('jd','delegado y jugador')
  )
  id_persona = models.ForeignKey(PrePerson, on_delete=models.CASCADE)
  id_equipo = models.ForeignKey(PreTeam, on_delete=models.CASCADE)
  id_torneo = models.ForeignKey(Tournament, on_delete=models.CASCADE)
  fecha_registro = models.DateField(auto_now_add=True, verbose_name='Fecha de Registro')
  rol = models.CharField(max_length=2, choices=ROLES, verbose_name='Rol')

  def __str__(self):
    return 'Persona: %s, con rol %s en el equipo %s' % (self.id_persona.nombre,self.rol,self.id_equipo.nombre)
