from django.forms import *

from main.models import Post, Tournament, Stage, Role

"""
#Create a stage
class CreateStageForm(ModelForm):
  class Meta:
    model = Fases
    fields = ['nombre', 'num_partidos', 'id_mod_fase']
"""

#Formulario de post
class PostCreateForm(ModelForm):
  def __init__(self, *args, **kwargs):
    super().__init__( *args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control'
      form.field.widget.attrs['autocomplete'] = 'off'

  class Meta:
    model = Post
    fields = ['titulo', 'cuerpo', 'imagen']
    widgets = {
      'titulo': TextInput(
        attrs = {
          'placeholder': 'Ingrese un título'
        }
      ),
      'cuerpo': Textarea(
        attrs = {
          'placeholder': 'Ingrese el cuerpo del post',
          'rows': 5
        }
      )
    }


#Formulario de torneo
class TournamentCreateForm(ModelForm):
  def __init__(self, *args, **kwargs):
    super().__init__( *args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control'
      form.field.widget.attrs['autocomplete'] = 'off'
      form.field.widget.attrs['required'] = True

  class Meta:
    model = Tournament
    fields = ['nombre', 'fecha_inicio', 'fecha_fin', 'edicion']
    widgets = {
      'nombre': TextInput(
        attrs = {
          'placeholder': 'Ingrese un nombre'
        }
      ),
      'fecha_inicio': DateInput(),
      'fecha_fin': DateInput(),
      
    }


#Formulario de fase
class StageCreateForm(ModelForm):
  def __init__(self, *args, **kwargs):
    super().__init__( *args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control'
      form.field.widget.attrs['autocomplete'] = 'off'

  class Meta:
    model = Stage
    fields = ['nombre', 'descripcion', 'equipos_por_grupo', 'num_grupos', 'part_por_equipo', 'equipos_por_partido']
    widgets = {
      'nombre': TextInput(
        attrs = {
          'placeholder': 'Ingrese un título'
        }
      ),
      'descripcion': Textarea(
        attrs = {
          'placeholder': 'Ingrese el cuerpo del post',
          'rows': 5
        }
      ),
      'equipos_por_grupo': NumberInput(),
      'num_grupos': NumberInput(),
      'part_por_equipo': NumberInput(),
      'equipos_por_partido': NumberInput(),
    }



#Formulario de juego
class GameCreateForm(ModelForm):
  def __init__(self, *args, **kwargs):
    super().__init__( *args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control'
      form.field.widget.attrs['autocomplete'] = 'off'

  class Meta:
    model = Stage
    fields = ['nombre']
    widgets = {
      'nombre': TextInput(
        attrs = {
          'placeholder': 'Ingrese el nombre del juego'
        }
      )
    }

#Formulario de rol
class RoleCreateForm(ModelForm):
  def __init__(self, *args, **kwargs):
    super().__init__( *args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control'
      form.field.widget.attrs['autocomplete'] = 'off'

  class Meta:
    model = Role
    fields = ['nombre']
    widgets = {
      'nombre': TextInput(
        attrs = {
          'placeholder': 'Ingrese el nombre del Rol'
        }
      )
    }