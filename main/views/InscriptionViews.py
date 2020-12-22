from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.forms import formset_factory
from django.contrib import messages

from main.models import PreTeamRegister, PreTeam, PrePerson, StageTournament, Tournament
from main.forms import TeamRegisterCreateForm, PreteamCreateForm, PrePersonCreateForm, PersonsFormSet


#Inscribir a los participantes del torneo
def createPersons(request, pk_torneo):
    #Verificamos cuántas personas debe conformar el equipo, esto se hace viendo la fase del torneo que tenga jerarquía = 1
    person_number = StageTournament.objects.get(jerarquia=1, id_torneo=pk_torneo).id_fase.part_por_equipo

    #Obtenemos el torneo
    tournament = Tournament.objects.get(id=pk_torneo)

    #Formset de los participantes
    # Creación del formset, especificando el form y el formset a usar
    PersonFormSet = formset_factory(PrePersonCreateForm, formset=PersonsFormSet, extra=person_number)

    if request.method == 'POST':
        person_formset = PersonFormSet(request.POST)
        team_form = PreteamCreateForm(request.POST)

        if person_formset.is_valid() and team_form.is_valid():
            
            team_form.save()
            #Obtenemos el id último registro del equipo
            pk_team = PreTeam.objects.order_by('-id')[0].id
            
            #Guardar la data por cada form del formset
            new_persons = []

            for person_form in person_formset:
                cedula = person_form.cleaned_data.get('cedula')
                nombre = person_form.cleaned_data.get('nombre')
                apellido = person_form.cleaned_data.get('apellido')
                correo = person_form.cleaned_data.get('correo')
                nickname = person_form.cleaned_data.get('nickname')

                if cedula and nombre and apellido and correo:
                    new_persons.append(PrePerson(cedula=cedula, nombre=nombre, apellido=apellido, correo=correo, nickname=nickname))
                
            #Con bulk se insertan todos los objetos en el array
            PrePerson.objects.bulk_create(new_persons)

            #Trabajar aquí la lógica del insert en la entidad PreTeamRegister


            #hasta aquí

            messages.success(request, 'La solicitud de inscripción al torneo se ha procesado satisfactoriamente')
            return redirect('/torneos/')
        else:
            #Verificar que todos los campos obligatorios estén llenos
            for person_form in person_formset:
                cedula = person_form.cleaned_data.get('cedula')
                nombre = person_form.cleaned_data.get('nombre')
                apellido = person_form.cleaned_data.get('apellido')
                correo = person_form.cleaned_data.get('correo')
                nickname = person_form.cleaned_data.get('nickname')

                if (not cedula) or (not nombre) or (not apellido) or (not correo):
                    messages.error(request, 'Debe llenar todos los campos, excepto el nickname y el comentario')
    else:
        #Formset inicial vacío
        person_formset = PersonFormSet(initial=None)
        #Form del equipo vacío
        team_form = PreteamCreateForm()
        team_register_form = PreteamCreateForm()
    
    context = {
        'person_formset': person_formset,
        'team_form': team_form,
        'title': 'Inscribe a los participantes', 
        'botton_title': 'Inscribirse'
    }

    return render(request, 'layouts/inscription/preinscription_form.html', context)



#Lista de inscripciones
class PreinscriptionList(ListView):
    model = PreTeamRegister
    template_name = 'layouts/inscription/preinscription_list.html'

