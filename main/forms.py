from django.forms import *
from django.core.exceptions import ValidationError

from main.models import Post, Tournament, Stage, StageTournament, Role, PreTeamRegister

"""
#Create a stage
class CreateStageForm(ModelForm):
  class Meta:
    model = Fases
    fields = ['nombre', 'num_partidos', 'id_mod_fase']

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


#Formsset de las fases del torneo
class BaseStageFormSet(formsets.BaseFormSet):
    def clean(self):
        """
        Adds validation to check that no two links have the same anchor or URL
        and that all links have both an anchor and URL.
        """
        if any(self.errors):
            return

        jerarquias = []
        fases = []
        duplicates = False

        for form in self.forms:
            if form.cleaned_data:
                jerarquia = form.cleaned_data['jerarquia']
                fase = form.cleaned_data['id_fase']

                # Verificar repetidos
                if jerarquia and fase:
                    if jerarquia in jerarquias:
                        duplicates = True
                    jerarquias.append(jer)

                    if fase in fases:
                        duplicates = True
                    fases.append(fase)

                if duplicates:
                    raise forms.ValidationError(
                        'Las fases no pueden tener jerarquías repetidas',
                        code='duplicate_links'
                    )

                # Verificar que los campos estén llenos
                if (fase and not jerarquia) or (jerarquia and not fase):
                    raise forms.ValidationError(
                        'Todas las fases deben tener jerarquía.',
                        code='missing_stage'
                    )


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



#Formulario preinscripción
class TeamRegisterCreateForm(ModelForm):
  def __init__(self, *args, **kwargs):
    super().__init__( *args, **kwargs)
    for form in self.visible_fields():
      form.field.widget.attrs['class'] = 'form-control'

  class Meta:
    model = PreTeamRegister
    fields = ['comentario']
    widgets = {
      'comentario': Textarea(
        attrs = {
          'placeholder': 'Ingrese comentario (opcional)',
          'rows': 5
        }
      )
    }
