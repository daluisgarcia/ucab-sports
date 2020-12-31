from django.forms import *
from django.core.exceptions import ValidationError


from main.models import *

"""
#Se deja comentado por si llega a ser necesario
class DateInput(forms.DateInput):
    input_type = "date"

    def __init__(self, **kwargs):
        kwargs["format"] = "%Y-%m-%d"
        super().__init__(**kwargs)
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
    fields = ['titulo', 'cuerpo', 'imagen', 'id_torneo']
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
      ),
      'id_torneo': Select()
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
    fields = ['nombre', 'fecha_inicio', 'fecha_fin', 'edicion', 'id_juego']
    widgets = {
      'nombre': TextInput(
        attrs = {
          'placeholder': 'Ingrese un nombre'
        }
      ),
      'fecha_inicio': DateInput(),
      'fecha_fin': DateInput(),
      'edicion': NumberInput(),
      'id_juego': Select()
    }

  #Función para validar fechas de inicio y fin del torneo
  def clean(self):
    cleaned_data = super().clean()
    fecha_inicio = cleaned_data.get('fecha_inicio')
    fecha_fin = cleaned_data.get('fecha_fin')
    #print(fecha_inicio)
    #print(fecha_fin)

    #Se validan las fechas
    if fecha_fin and fecha_inicio:
      if(fecha_fin < fecha_inicio):
          raise forms.ValidationError('La fecha de fin tiene que ser posterior a la fecha de inicio')



#Formulario de fase de torneo
class StageTournamentCreateForm(forms.Form):
  def __init__(self, *args, **kwargs):
    super().__init__( *args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control'

  class Meta:
    model = StageTournament
    fields = ['id_fase', 'jerarquia']
    widgets = {
      'id_fase': Select(),
      'jerarquia': NumberInput(
        attrs = {
          'placeholder': 'Ingrese la jerarquía'
        }
      )
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
    model = Game
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

#Formulario de permiso
class PermissionCreateForm(ModelForm):
  def __init__(self, *args, **kwargs):
    super().__init__( *args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control'
      form.field.widget.attrs['autocomplete'] = 'off'

  class Meta:
    model = Permission
    fields = ['nombre']
    widgets = {
      'nombre': TextInput(
        attrs = {
          'placeholder': 'Ingrese el nombre del permiso'
        }
      )
    }


#Formularios para la solicitud de inscripción a los torneos

#Inscripción del Equipo
class PreteamCreateForm(ModelForm):
  def __init__(self, *args, **kwargs):
    super().__init__( *args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control'
      form.field.widget.attrs['autocomplete'] = 'off'

  class Meta:
    model = PreTeam
    fields = ['nombre','logo', 'comentario']
    widgets = {
      'nombre': TextInput(
        attrs = {
          'placeholder': 'Ingrese el nombre del equipo'
        }
      ),
      'comentario': Textarea(
        attrs = {
          'placeholder': '¿Tiene algún comentario que hacer sobre la inscripción? (opcional)',
          'rows': 5
        }
      )
    }


#inscripción de los participantes
class PrePersonCreateForm(ModelForm):
  def __init__(self, *args, **kwargs):
    super().__init__( *args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control'

  class Meta:
    model = PrePerson
    fields = ['cedula','nombre','apellido','correo','nickname']
    widgets = {
      'cedula': NumberInput(
        attrs = {
          'placeholder': 'Ingrese la cédula'
        }
      ),
      'nombre': TextInput(
        attrs = {
          'placeholder': 'Ingrese el nombre del participante'
        }
      ),
      'apellido': TextInput(
        attrs = {
          'placeholder': 'Ingrese el apellido del participante'
        }
      ),
      'correo': EmailInput(
        attrs = {
          'placeholder': 'Ingrese el correo del participante',
        }
      ),
      'nickname': TextInput(
        attrs = {
          'placeholder': 'Ingrese el nickname del participante (opcional)'
        }
      ),
    }


#REVISAR
#La validacion s eetsa haciendo pero no muestra el error en el template :(
#Formset de las personas
class PersonsFormSet(formsets.BaseFormSet):
    def clean(self):
        #Validaciones para eviat que hayan correos y cédulas repetidas
        if any(self.errors):
            return

        cedulas = []
        nombres = []
        apellidos = []
        correos = []
        nicknames = []
        duplicates = False

        for form in self.forms:
          
            if form.cleaned_data:
                cedula = form.cleaned_data['cedula']
                nombre = form.cleaned_data['nombre']
                apellido = form.cleaned_data['apellido']
                correo = form.cleaned_data['correo']
                nickname = form.cleaned_data['nickname']

                # Verificar que no haya cédulas ni correos repetidos
                if cedula and nombre and apellido and correo:
                    if cedula in cedulas:
                        duplicates = True
                        print('CEDULAS REPETIDAS')
                    cedulas.append(cedula)

                    if correo in correos:
                        duplicates = True
                        print('CORREOS REPETIDOS')
                    correos.append(correo)
                
                if duplicates:
                    raise forms.ValidationError('Las cédulas y los correos deben ser distintos en todos los campos.')


#Formulario inscripción
class TeamRegisterCreateForm(ModelForm):
  def __init__(self, *args, **kwargs):
    super().__init__( *args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control'

  class Meta:
    model = PreTeamRegister
    fields = ('rol',)
    widgets = {
      'rol': Select()
    }



#Formset de los roles de la inscripción
class TeamsRegisterFormSet(formsets.BaseFormSet):
    def clean(self):
        #Validaciones para verificar que haya solamente un delegado
        if any(self.errors):
            return

        roles = []
        duplicates = False

        for form in self.forms:
            
            if form.cleaned_data:
                role = form.cleaned_data['rol']
                print('Rol validator: ', role)
                # Verificar que no hayan delegados repetidos
                if (role == 'd') or (role=='jd'):
                    print('delegado')
                    if role in roles:
                        duplicates = True
                    roles.append(role)
                
                if not role:
                    raise forms.ValidationError('Debe llenar todos los campos de los roles')
                if duplicates:
                    raise forms.ValidationError('Sólo puede existir un delegado por equipo.')
