from django.db import models
from datetime import datetime


class Person(models.Model):
  cedula = models.IntegerField(primary_key=True)
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
class Team(models.Model):
  nombre = models.CharField(max_length=30, verbose_name='Nombre')
  logo = models.ImageField(upload_to='logos/%Y/%m/%d', null=True, blank=True)

  def __str__(self):
    return self.nombre

  class Meta:
    verbose_name = 'Equipo'
    verbose_name_plural = 'Equipos'



class Stage(models.Model):
  nombre = models.CharField(max_length=30, verbose_name='Nombre')
  descripcion = models.CharField(max_length=100, verbose_name='Descripción')
  equipos_por_grupo = models.SmallIntegerField(verbose_name='Equipos por grupo')
  num_grupos = models.SmallIntegerField(verbose_name='Número de grupos')
  part_por_equipo = models.SmallIntegerField(verbose_name='Participantes por equipo')
  equipos_por_partido = models.SmallIntegerField(verbose_name='Equipos por partido')

  def __str__(self):
    return self.nombre

  class Meta:
    verbose_name = 'Modalidad de Fase'
    verbose_name_plural = 'Modalidades de Fase'



class Game(models.Model):
  nombre = models.CharField(max_length=30, verbose_name='Nombre')

  def __str__(self):
    return self.nombre

  class Meta:
    verbose_name = 'Juego'
    verbose_name_plural = 'Juegos'



class Permission(models.Model):
  nombre = models.CharField(max_length=30, verbose_name='Nombre')

  def __str__(self):
    return self.nombre

  class Meta:
    verbose_name = 'Permiso'
    verbose_name_plural = 'Permisos'



class Role(models.Model):
  nombre = models.CharField(max_length=30, verbose_name='Nombre')
  rol_permiso = models.ManyToManyField(Permission)

  def __str__(self):
    return self.nombre

  class Meta:
    verbose_name = 'Rol'
    verbose_name_plural = 'Roles'



class Organizer(models.Model):
  usuario = models.CharField(max_length=30, verbose_name='Usuario')
  contrasena = models.CharField(max_length=30, verbose_name='Contraseña')
  id_rol = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)

  def __str__(self):
    return self.usuario

  class Meta:
    verbose_name = 'Organizador'
    verbose_name_plural = 'Organizadores'



class Post(models.Model):
  titulo = models.CharField(max_length=50, verbose_name='Título')
  cuerpo = models.CharField(max_length=400, verbose_name='Contenido')
  imagen = models.ImageField(upload_to='posts/%Y/%m/%d', null=True, blank=True)
  id_organizador = models.ForeignKey(Organizer, on_delete=models.SET_NULL, null=True, blank=True)

  def __str__(self):
    return self.titulo

  class Meta:
    verbose_name = 'Post'
    verbose_name_plural = 'Posts'



class Tournament(models.Model):
  nombre = models.CharField(max_length=30, verbose_name='Nombre')
  fecha_inicio = models.DateField(verbose_name='Fecha de inicio')
  fecha_fin = models.DateField(verbose_name='Fecha de fin')
  edicion = models.SmallIntegerField(verbose_name='Edición')
  id_juego = models.ForeignKey(Game, verbose_name='Tipo de juego', on_delete=models.SET_NULL, null=True, blank=True)
  id_organizador = models.ForeignKey(Organizer, on_delete=models.SET_NULL, null=True, blank=True)

  def __str__(self):
    return self.nombre

  class Meta:
    verbose_name = 'Torneo'
    verbose_name_plural = 'Torneos'



class HistoryParticipation(models.Model):
  id_persona = models.ForeignKey(Person, on_delete=models.CASCADE)
  id_equipo = models.ForeignKey(Team, on_delete=models.CASCADE)
  id_torneo = models.ForeignKey(Tournament, on_delete=models.CASCADE)
  fecha_registro = models.DateField(verbose_name='Fecha de Registro')
  fecha_fin = models.DateField(verbose_name='Fecha de Registro', null=True, blank=True)
  rol = models.CharField(max_length=2, verbose_name='Rol')

  def __str__(self):
    return self.rol



class WinningStandard(models.Model):
  criterio = models.CharField(max_length=30, verbose_name='Criterio')

  def __str__(self):
    return self.criterio

  class Meta:
    verbose_name = 'Criterio Ganador'
    verbose_name_plural = 'Criterios Ganadores'



class StageStandard(models.Model):
  id_fase = models.ForeignKey(Stage, on_delete=models.CASCADE)
  importancia = models.SmallIntegerField(verbose_name='Importancia')
  id_crit_ganador = models.ForeignKey(WinningStandard, on_delete=models.SET_NULL, null=True, blank=True)

  def __str__(self):
    return self.importancia



class StageTournament(models.Model):
  id_fase = models.ForeignKey(Stage, on_delete=models.CASCADE)
  id_torneo = models.ForeignKey(Tournament, on_delete=models.CASCADE)
  jerarquia = models.SmallIntegerField(verbose_name='Jerarquia')



class Match(models.Model):
  fecha = models.DateField(verbose_name='Fecha del partido')
  direccion = models.CharField(max_length=100, null=True, blank=True, verbose_name='Dirección')
  id_fase_torneo = models.ForeignKey(StageTournament, on_delete=models.SET_NULL, null=True, blank=True)

  def __str__(self):
    return 'Partido del torneo: {}'.format(self.id_fase_torneo.id_torneo.nombre)

  class Meta:
    verbose_name = 'Partido'
    verbose_name_plural = 'Partidos'



class Participation(models.Model):
  id_equipo = models.ForeignKey(Team, on_delete=models.CASCADE)
  id_partido = models.ForeignKey(Match, on_delete=models.CASCADE)
  ganador = models.BooleanField()
  puntos_equipo = models.IntegerField(verbose_name='Puntos del equipo')

  def __str__(self):
    return 'Puntaje por equipo {}: {}'.format(self.puntos_equipo).format(self.id_equipo.nombre)

  class Meta:
    verbose_name = 'Partido'
    verbose_name_plural = 'Partidos'



#Modelos de solicitud de inscripción

class PrePerson(models.Model):
  cedula = models.IntegerField(primary_key=True)
  nombre = models.CharField(max_length=50, verbose_name='Nombre')
  apellido = models.CharField(max_length=50, verbose_name='Apellido')
  correo = models.EmailField(max_length=100, verbose_name='Email')
  nickname = models.CharField(max_length=30, blank=True, verbose_name='Nickname')
  
  def __str__(self):
    return self.nombre

  class Meta:
    verbose_name = 'Usuario'
    verbose_name_plural = 'Usuarios'



class PreTeam(models.Model):
  nombre = models.CharField(max_length=30, verbose_name='Nombre')
  logo = models.ImageField(upload_to='logos/%Y/%m/%d', null=True, blank=True)
  comentario = models.CharField(max_length=150, verbose_name='Comentario (opcional)', null=True, blank=True)
  def __str__(self):
    return self.nombre

  class Meta:
    verbose_name = 'Equipo'
    verbose_name_plural = 'Equipos'



class PreTeamRegister(models.Model):
  id_persona = models.ForeignKey(PrePerson, on_delete=models.CASCADE)
  id_equipo = models.ForeignKey(PreTeam, on_delete=models.CASCADE)
  id_torneo = models.ForeignKey(Tournament, on_delete=models.CASCADE)
  fecha_registro = models.DateField(verbose_name='Fecha de Registro')
  rol = models.CharField(max_length=2, verbose_name='Rol')
  estatus = models.CharField(max_length=2, verbose_name='Rol')

  def __str__(self):
    return self.rol
