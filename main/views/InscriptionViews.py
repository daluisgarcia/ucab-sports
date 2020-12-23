from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.forms import formset_factory
from django.contrib import messages
from django.core.exceptions import ValidationError

from main.models import PreTeamRegister, PreTeam, PrePerson, StageTournament, Tournament
from main.forms import TeamRegisterCreateForm, TeamsRegisterFormSet, PreteamCreateForm, PrePersonCreateForm, PersonsFormSet


#REVISAR
#Cuando no se llenan todos los roles, igual pasa el is_valid() (es decir, no debería pasar ese formulario)

#Inscribir a los participantes del torneo
def createPersons(request, pk_torneo):
    #Verificamos cuántas personas debe conformar el equipo, esto se hace viendo la fase del torneo que tenga jerarquía = 1
    person_number = StageTournament.objects.get(jerarquia=1, id_torneo=pk_torneo).id_fase.part_por_equipo

    #Obtenemos el torneo
    tournament = Tournament.objects.get(id=pk_torneo)

    #Formset de los participantes
    # Creación del formset, especificando el form y el formset a usar
    PersonFormSet = formset_factory(PrePersonCreateForm, formset=PersonsFormSet, extra=person_number)

    #Formset de los roles de los participantes
    # Creación del formset, especificando el form y el formset a usar
    TeamRegisterFormSet = formset_factory(TeamRegisterCreateForm, formset=TeamsRegisterFormSet, extra=person_number)

    if request.method == 'POST':
        person_formset = PersonFormSet(request.POST)
        team_form = PreteamCreateForm(request.POST)
        team_register_formset = TeamRegisterFormSet(request.POST)

        if person_formset.is_valid() and team_form.is_valid() and team_register_formset.is_valid():
            
            team_form.save()
            #Obtenemos el último registro del equipo
            pk_team = PreTeam.objects.order_by('-id')[0]
            #Obtenemos el registro del torneo
            pk_tournament = Tournament.objects.get(id=pk_torneo)
            
            #Guardar la data por cada form del formset
            new_persons = []
            new_team_register = []
            #Array de cédulas
            ci = []

            for person_form in person_formset:
                cedula = person_form.cleaned_data.get('cedula')
                nombre = person_form.cleaned_data.get('nombre')
                apellido = person_form.cleaned_data.get('apellido')
                correo = person_form.cleaned_data.get('correo')
                nickname = person_form.cleaned_data.get('nickname')
                ci.append(cedula)
                
                if cedula and nombre and apellido and correo:
                    new_persons.append(PrePerson(cedula=cedula, nombre=nombre, apellido=apellido, correo=correo, nickname=nickname))

            #Con bulk se insertan todos los objetos en el array
            PrePerson.objects.bulk_create(new_persons)

            i=0
            
            for role_form in team_register_formset:
                role = role_form.clean()
                print('Form: ', role)

                pk_persona = PrePerson.objects.get(cedula=ci[i])

                if role:
                    new_team_register.append(PreTeamRegister(rol=role, estatus='p', id_equipo=pk_team, id_persona=pk_persona,  id_torneo=pk_tournament))
                i=i+1
            
            PreTeamRegister.objects.bulk_create(new_team_register)

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
                    messages.error(request, 'Debe llenar los campos de los datos de los participantes')
            
            for role_form in team_register_formset:
                role = role_form.cleaned_data.get('rol')

                if (not role):
                    messages.error(request, 'Debe llenar los roles de los participantes')
            
    else:
        #Formset inicial vacío
        person_formset = PersonFormSet(initial=None)
        team_register_formset = TeamRegisterFormSet(initial=None)
        #Form del equipo vacío
        team_form = PreteamCreateForm()
    
    context = {
        'person_formset': person_formset,
        'team_form': team_form,
        'team_register_formset': team_register_formset,
        'title': 'Inscribe al equipo y a los participantes', 
        'botton_title': 'Inscribirse'
    }

    return render(request, 'layouts/inscription/preinscription_form.html', context)



#Lista de inscripciones
class PreinscriptionList(ListView):
    model = PreTeamRegister
    template_name = 'layouts/inscription/preinscription_list.html'

