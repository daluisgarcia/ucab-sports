from django.db import models
from datetime import datetime


class Personas(models.Model):
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
class Equipos(models.Model):
  nombre = models.CharField(max_length=30, verbose_name='Nombre')
  logo = models.ImageField(upload_to='logos/%Y/%m/%d')

  def __str__(self):
    return self.nombre

  class Meta:
    verbose_name = 'Equipo'
    verbose_name_plural = 'Equipos'



class Registro_Equipos(models.Model):
  id_persona = models.ForeignKey(Personas, on_delete=models.CASCADE)
  id_equipo = models.ForeignKey(Equipos, on_delete=models.CASCADE)
  rol = models.CharField(max_length=2, verbose_name='Rol')
  aprobado = models.BooleanField(default=False)

  def __str__(self):
    return self.rol



class Modalidades(models.Model):
  nombre = models.CharField(max_length=30, verbose_name='Nombre')
  part_por_equipo = models.SmallIntegerField(verbose_name='Participantes por equipo')
  equipos_por_partido = models.SmallIntegerField(verbose_name='Equipos por partido')

  def __str__(self):
    return self.nombre

  class Meta:
    verbose_name = 'Modalidad'
    verbose_name_plural = 'Modalidades'



class Juegos(models.Model):
  nombre = models.CharField(max_length=30, verbose_name='Nombre')
  modalidad_juego = models.ManyToManyField(Modalidades)

  def __str__(self):
    return self.nombre

  class Meta:
    verbose_name = 'Juego'
    verbose_name_plural = 'Juegos'



class Permisos(models.Model):
  nombre = models.CharField(max_length=30, verbose_name='Nombre')

  def __str__(self):
    return self.nombre

  class Meta:
    verbose_name = 'Permiso'
    verbose_name_plural = 'Permisos'



class Roles(models.Model):
  id = models.IntegerField(primary_key=True)
  nombre = models.CharField(max_length=30, verbose_name='Nombre')
  rol_permiso = models.ManyToManyField(Permisos)

  def __str__(self):
    return self.nombre

  class Meta:
    verbose_name = 'Rol'
    verbose_name_plural = 'Roles'



class Organizadores(models.Model):
  usuario = models.CharField(max_length=30, verbose_name='Usuario')
  contrasena = models.CharField(max_length=30, verbose_name='Contraseña')
  id_rol = models.ForeignKey(Roles, on_delete=models.SET_NULL, null=True, blank=True)

  def __str__(self):
    return self.usuario

  class Meta:
    verbose_name = 'Organizador'
    verbose_name_plural = 'Organizadores'



class Posts(models.Model):
  titulo = models.CharField(max_length=50, verbose_name='Título')
  resumen = models.CharField(max_length=100, verbose_name='Resumen')
  cuerpo = models.CharField(max_length=400, verbose_name='Contenido')
  imagen = models.ImageField(upload_to='posts/%Y/%m/%d', null=True, blank=True)
  id_organizador = models.ForeignKey(Organizadores, on_delete=models.SET_NULL, null=True, blank=True)

  def __str__(self):
    return self.titulo

  class Meta:
    verbose_name = 'Post'
    verbose_name_plural = 'Posts'



class Torneos(models.Model):
  id_juego = models.ForeignKey(Juegos, on_delete=models.CASCADE)
  nombre = models.CharField(max_length=30, verbose_name='Nombre')
  fecha_inicio = models.DateField(verbose_name='Fecha de inicio')
  fecha_fin = models.DateField(verbose_name='Fecha de fin')
  edicion = models.SmallIntegerField(verbose_name='Edición')
  id_organizador = models.ForeignKey(Organizadores, on_delete=models.SET_NULL, null=True, blank=True)

  def __str__(self):
    return self.nombre

  class Meta:
    verbose_name = 'Torneo'
    verbose_name_plural = 'Torneos'



#¿Los verbose names de esta clase están bien? :(
class Modalidades_Fase(models.Model):
  nombre = models.CharField(max_length=30, verbose_name='Nombre')
  descripcion = models.CharField(max_length=100, verbose_name='Descripción')
  equipos_por_grupo = models.SmallIntegerField(verbose_name='Equipos por grupo')
  num_grupos = models.SmallIntegerField(verbose_name='Número de grupos')

  def __str__(self):
    return self.nombre

  class Meta:
    verbose_name = 'Modalidad de Fase'
    verbose_name_plural = 'Modalidades de Fase'



class Criterios_Ganadores(models.Model):
  criterio = models.CharField(max_length=30, verbose_name='Criterio')

  def __str__(self):
    return self.criterio

  class Meta:
    verbose_name = 'Criterio Ganador'
    verbose_name_plural = 'Criterios Ganadores'



class Criterios_Fase(models.Model):
  id_modalidad = models.ForeignKey(Modalidades_Fase, on_delete=models.CASCADE)
  importancia = models.SmallIntegerField(verbose_name='Importancia')
  id_crit_ganador = models.ForeignKey(Criterios_Ganadores, on_delete=models.SET_NULL, null=True, blank=True)

  def __str__(self):
    return self.importancia



class Fases(models.Model):
  nombre = models.CharField(max_length=30, verbose_name='Nombre')
  num_partidos = models.SmallIntegerField(verbose_name='Número de partidos')
  id_mod_fase = models.ForeignKey(Modalidades_Fase, on_delete=models.SET_NULL, null=True, blank=True)

  def __str__(self):
    return self.nombre

  class Meta:
    verbose_name = 'Fase'
    verbose_name_plural = 'Fases'



class Fase_Torneos(models.Model):
  id_fase = models.ForeignKey(Fases, on_delete=models.CASCADE)
  id_torneo = models.ForeignKey(Torneos, on_delete=models.CASCADE)



class Partidos(models.Model):
  fecha = models.DateField(verbose_name='Fecha del partido')
  direccion = models.CharField(max_length=100, null=True, blank=True, verbose_name='Dirección')
  id_fase_torneo = models.ForeignKey(Fase_Torneos, on_delete=models.SET_NULL, null=True, blank=True)

  def __str__(self):
    return 'Partido del torneo: {}'.format(self.id_fase_torneo.id_torneo.nombre)

  class Meta:
    verbose_name = 'Partido'
    verbose_name_plural = 'Partidos'



class Participacion(models.Model):
  id_equipo = models.ForeignKey(Equipos, on_delete=models.CASCADE)
  id_partido = models.ForeignKey(Partidos, on_delete=models.CASCADE)
  ganador = models.BooleanField()
  puntos_equipo = models.IntegerField(verbose_name='Puntos del equipo')

  def __str__(self):
    return 'Puntaje por equipo {}: {}'.format(self.puntos_equipo).format(self.id_equipo.nombre)

  class Meta:
    verbose_name = 'Partido'
    verbose_name_plural = 'Partidos'
