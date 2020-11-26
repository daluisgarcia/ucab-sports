from django.forms import *

from main.models import Posts, Torneos



#Crear Post
class PostCreateForm(ModelForm):
  def __init__(self, *args, **kwargs):
    super().__init__( *args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control'
      form.field.widget.attrs['autocomplete'] = 'off'

  class Meta:
    model = Posts
    fields = ['titulo', 'resumen', 'cuerpo', 'imagen']
    widgets = {
      'titulo': TextInput(
        attrs = {
          'placeholder': 'Ingrese un título'
        }
      ),
      'resumen': Textarea(
        attrs = {
          'placeholder': 'Ingrese una descripción',
          'rows': 2
        }
      ),
      'cuerpo': Textarea(
        attrs = {
          'placeholder': 'Ingrese el cuerpo del post',
          'rows': 5
        }
      )
    }



#Crear Torneo
class TorneoCreateForm(ModelForm):
  def __init__(self, *args, **kwargs):
    super().__init__( *args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control'
      form.field.widget.attrs['autocomplete'] = 'off'
      form.field.widget.attrs['required'] = True

  class Meta:
    model = Torneos
    fields = ['nombre', 'fecha_inicio', 'fecha_fin', 'edicion']
    widgets = {
      'nombre': TextInput(
        attrs = {
          'placeholder': 'Ingrese un nombre'
        }
      ),
      'fecha_inicio': DateInput(
        
      ),
      'fecha_fin': DateInput(
        
      ),
      
    }