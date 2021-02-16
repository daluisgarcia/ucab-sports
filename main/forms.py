from django.forms import *
from django.core.exceptions import ValidationError
from main.models import *


'''
    POST CREATE FORM
'''
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
          'placeholder': 'Título'
        }
      ),
      'cuerpo': Textarea(
        attrs = {
          'placeholder': 'Cuerpo',
          'rows': 5
        }
      )
    }


'''
    TOURNAMENT CREATE FORM
'''
class TournamentCreateForm(ModelForm):
  def __init__(self, *args, **kwargs):
    super().__init__( *args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control'
      form.field.widget.attrs['autocomplete'] = 'off'
      form.field.widget.attrs['required'] = 'true'

  class Meta:
    model = Tournament
    fields = ['nombre', 'fecha_inicio', 'fecha_fin', 'edicion', 'tipo_delegado', 'id_juego']
    widgets = {
      'nombre': TextInput(
        attrs = {
          'placeholder': 'Nombre'
        }
      ),
      'fecha_inicio': DateInput(format=('%Y-%m-%d'), attrs={'type':'date'}),
      'fecha_fin': DateInput(format=('%Y-%m-%d'), attrs={'type':'date'}),
      'edicion': NumberInput(),
      'tipo_delegado': Select(),
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
    

'''
    INITIAL STAGE-TOURNAMENT
'''
class InitialStageTournamentForm(ModelForm):
  def __init__(self, *args, **kwargs):
    super().__init__( *args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control'

  class Meta:
    model = StageTournament
    fields = ['participantes_por_equipo']
    widgets = {
      'participantes_por_equipo': NumberInput(
        attrs = {
          'placeholder': 'Participantes por equipo'
        }
      )
    }


'''
    STAGE-TOURNAMENT CREATE FORM
'''
class StageTournamentCreateForm(forms.Form):
  def __init__(self, *args, **kwargs):
    super().__init__( *args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control'

  class Meta:
    model = StageTournament
    fields = ['id_fase', 'participantes_por_equipo', 'equipos_por_partido', 'num_grupos', 'equipos_por_grupo']
    widgets = {
      'id_fase': Select(),
      'participantes_por_equipo': NumberInput(),
      'participantes_por_equipo': NumberInput(
        attrs = {
          'placeholder': 'número de participantes'
        }
      ),
      'equipos_por_partido': NumberInput(
        attrs = {
          'placeholder': 'Número de equipos'
        }
      ),
      'num_grupos': NumberInput(
        attrs = {
          'placeholder': 'Número de grupos'
        }
      ),
      'equipos_por_grupo': NumberInput(
        attrs = {
          'placeholder': 'Equipos por grupo'
        }
      )
    }


'''
    STAGE CREATE FORM
'''
class StageCreateForm(ModelForm):
  def __init__(self, *args, **kwargs):
    super().__init__( *args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control'
      form.field.widget.attrs['autocomplete'] = 'off'

  class Meta:
    model = Stage
    fields = ['nombre', 'descripcion']
    widgets = {
      'nombre': TextInput(
        attrs = {
          'placeholder': 'Título'
        }
      ),
      'descripcion': Textarea(
        attrs = {
          'placeholder': 'Descripción breve de la fase',
          'rows': 5
        }
      ),
    }


'''
    GAME CREATE FORM
'''
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
          'placeholder': 'Nombre'
        }
      )
    }


'''
    PRE-TEAM CREATE FORM
'''
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
          'placeholder': 'Nombre'
        }
      ),
      'comentario': Textarea(
        attrs = {
          'placeholder': '¿Tiene algún comentario que hacer sobre la inscripción? (opcional)',
          'rows': 5
        }
      )
    }


'''
    PRE-PERSON CREATE FORM
'''
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
          'placeholder': 'Cédula'
        }
      ),
      'nombre': TextInput(
        attrs = {
          'placeholder': 'Nombre'
        }
      ),
      'apellido': TextInput(
        attrs = {
          'placeholder': 'Apellido'
        }
      ),
      'correo': EmailInput(
        attrs = {
          'placeholder': 'Correo',
        }
      ),
      'nickname': TextInput(
        attrs = {
          'placeholder': 'Username (opcional)'
        }
      ),
    }

  #Función para validar fechas de inicio y fin del torneo
  def clean(self):
    cleaned_data = super().clean()
    cedula = cleaned_data.get('cedula')

    if cedula:
      if int(cedula) < 0:
        raise forms.ValidationError('Las cédulas tienen que ser números positivos')


#REVISAR
#La validacion s eetsa haciendo pero no muestra el error en el template :(
'''
    PERSON CREATE FORM
'''
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
        duplicate_cedula = False
        duplicate_correo = False 
        for form in self.forms:
          
            if form.cleaned_data:
                cedula = form.cleaned_data['cedula']
                nombre = form.cleaned_data['nombre']
                apellido = form.cleaned_data['apellido']
                correo = form.cleaned_data['correo']
                nickname = form.cleaned_data['nickname']

                # Verificar que no haya cédulas ni correos repetidos
                if cedula and nombre and apellido and correo:
                    if (cedula in cedulas) and duplicate_cedula == False:
                        form.add_error('cedula', 'Las cédulas deben ser distintas en todos los campos.')
                        print('CEDULAS REPETIDAS')
                        duplicate_cedula = True
                    cedulas.append(cedula)

                    if (correo in correos) and duplicate_correo == False:
                        form.add_error('correo', 'Los correos deben ser distintos en todos los campos.')
                        print('CORREOS REPETIDOS')
                        duplicate_correo = True
                    correos.append(correo)
                  

'''
    TEAM-REGISTER CREATE FORM
'''
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
  


'''
    TEAM-REGISTER CREATE FORMSET
'''
class TeamsRegisterFormSet(formsets.BaseFormSet):
    def clean(self):
        #Validaciones para verificar que haya solamente un delegado
        if any(self.errors):
            return 

        roles = []
        duplicates = False
        duplicate_rol = False
        hay_delegado = False

        for form in self.forms:
            
            if form.cleaned_data:
                role = form.cleaned_data['rol']
                print('Rol validator: ', role)
                # Verificar que no hayan delegados repetidos
                if (role == 'd') or (role=='jd'):
                    hay_delegado = True
                    print('delegado')
                    if role in roles:
                        duplicates = True
                    roles.append(role)
                
                if not role:
                    form.add_error('rol','Debe llenar todos los campos de los roles')
                if duplicates and duplicate_rol == False:
                    form.add_error('rol','Sólo puede existir un delegado por equipo.')
                    duplicate_rol = True

            if(not hay_delegado):
                form.add_error('rol','Tiene que existir un delegado.')


'''
    MATCH CREATE FORM
'''
class MatchCreateForm(ModelForm):
  def __init__(self, *args, **kwargs):
    super().__init__( *args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control'
      form.field.widget.attrs['autocomplete'] = 'off'

  class Meta:
    model = Match
    fields = ['fecha', 'direccion']
    widgets = {
      'fecha': DateInput(format=('%Y-%m-%d'), attrs={'type':'date'}),
      'direccion': TextInput(
        attrs = {
          'placeholder': 'Lugar del partido (opcional)'
        }
      ),
    }



'''
    PARTICIPATION CREATE FORM
'''
class ParticipationCreateForm(ModelForm):
  def __init__(self, *args, **kwargs):
    super().__init__( *args, **kwargs)

  class Meta:
    model = Participation
    fields = ['ganador','puntos_equipo']
    widgets = {
      'ganador': CheckboxInput(),
      'puntos_equipo': NumberInput(
        attrs = {
          'placeholder': 'Puntos'
        }
      )
    }


'''
    PARTICIPATION CREATE FORMSET
'''
class ParticipationFormSet(formsets.BaseFormSet):
    def clean(self):
        #Validar que si todos los campos están llenos, no todos sean ganadores
        if any(self.errors):
            return

        todos_ganadores = True
        puntos = False
        un_ganador = False

        for form in self.forms:
            
            if form.cleaned_data:
                ganador = form.cleaned_data['ganador']
                puntos_equipo = form.cleaned_data['puntos_equipo']

                if ganador == True:
                    un_ganador = True
                if ganador == False:
                    todos_ganadores = False
                if puntos_equipo:
                    puntos = True

        if ((puntos == True) and (un_ganador == False)):
            form.add_error('puntos_equipo','Si va a colocar puntajes tiene que colocar el o los ganadores del partido')

        