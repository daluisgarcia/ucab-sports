from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.forms import formset_factory
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.views.generic import DetailView

from main.models import PreTeamRegister, PreTeam, PrePerson, StageTournament, Tournament, Person, Team, HistoryParticipation, Game, Classified
from main.forms import TeamRegisterCreateForm, TeamsRegisterFormSet, PreteamCreateForm, PrePersonCreateForm, PersonsFormSet


#REVISAR
#Cuando no se llenan todos los roles, igual pasa el is_valid() (es decir, no debería pasar ese formulario)

#Inscribir a los participantes del torneo
def createRegisterTeam(request, pk_torneo):
    #Verificamos cuántas personas debe conformar el equipo, esto se hace viendo la fase del torneo que tenga jerarquía = 1
    person_number = StageTournament.objects.get(jerarquia=1, id_torneo=pk_torneo).id_fase.part_por_equipo

    #Verificamos si este tipo de torneo es del tipo_delegado = 'd'. Si es así, entonces se agrega una fila más al person_number
    if(Tournament.objects.get(id=pk_torneo).tipo_delegado == 'd'):
        person_number = person_number + 1

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
                    #Si este usuario no ha solicitado inscripción en otro torneo, entonces lo mete en el array
                    if (PrePerson.objects.filter(cedula=cedula).count() == 0):
                        new_persons.append(PrePerson(cedula=cedula, nombre=nombre, apellido=apellido, correo=correo, nickname=nickname))
                
                    #Verificar que el usuario no trate de inscribirse en el mismo torneo si ya esta inscrito
                    if(PreTeamRegister.objects.filter(id_persona__cedula=cedula, id_torneo=pk_torneo) or HistoryParticipation.objects.filter(id_persona__cedula=cedula, id_torneo=pk_torneo)):
                        messages.error(request, 'El usuario '+ nombre +' '+ apellido +' ya se inscribió con anterioridad al torneo.')
                        return redirect('/torneos/')

            #Con bulk se insertan todos los objetos en el array
            PrePerson.objects.bulk_create(new_persons)
            i=0
            
            for role_form in team_register_formset:
                role = role_form.cleaned_data['rol']
                print('Role Form: ', role)

                #Validar que los roles sean exclusivamente del tipo de delegado
                if((tournament.tipo_delegado == 'd' and role == 'jd') or(tournament.tipo_delegado == 'jd' and role == 'd')):
                    
                    #REVISAR
                    #Salen el error corto y el de "Ha ocurrido un error"
                    messages.error(request, 'El tipo de participantes no coincide con las reglas para este torneo')
                    context = {
                        'person_formset': person_formset,
                        'team_form': team_form,
                        'team_register_formset': team_register_formset,
                        'title': 'Inscribe al equipo y a los participantes', 
                        'botton_title': 'Inscribirse'
                    }
                    return render(request, 'layouts/inscription/preinscription_form.html', context)

                pk_persona = PrePerson.objects.get(cedula=ci[i])

                if role:
                    new_team_register.append(PreTeamRegister(rol=role, id_equipo=pk_team, id_persona=pk_persona,  id_torneo=pk_tournament))
                i=i+1

            PreTeamRegister.objects.bulk_create(new_team_register)

            messages.success(request, 'La solicitud de inscripción al torneo se ha procesado satisfactoriamente')

            #REVISAR ESTE LINK PARA QUE REDIRECCIONE A LOS TORNEOS DEL PARTICIPANTE
            return redirect('main:admin_index')
        
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
                    break
            
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



#Aprobar inscripción
def approveInscription(request, pk_team, pk_tour):
    #Buscamos los registros de PreTeamRegister
    preteamregister = PreTeamRegister.objects.filter(id_equipo=pk_team, id_torneo=pk_tour)
    #print(preteamregister)

    #Arrays donde se ingresarán los datos
    new_persons = []
    register_team = []
    ci = []
    #Creamos los registros de los participantes
    
    for person in preteamregister:
        print(person.id)
        
        #Comparamos con los anteriores registros a ver si este participante ha participado antes en algo
        try:
            anterior_registro = Person.objects.get(cedula=person.id_persona.cedula)
        except Person.DoesNotExist:
            anterior_registro = None

        if anterior_registro is not None:
            print('Sí he participado antes, soy: ', anterior_registro)
            print(anterior_registro.correo)

            #Opciones:
            #Se actualizan los correos y se mandan a ambos correos (en caso de haber uno nuevo y uno viejo) la aprobación de inscripción
            #No se procesa la solicitud porque hay cédulas iguales con nombres distintos. Se le notifica al organizador
            anterior_registro.correo = person.id_persona.correo
            anterior_registro.save()

        #Sino, se forma nuevo registro
        else:
            new_persons.append(Person(cedula=person.id_persona.cedula, nombre=person.id_persona.nombre, apellido=person.id_persona.apellido, correo=person.id_persona.correo, nickname=person.id_persona.nickname))
        
        #De una u otra forma se agrega la cédula en el array
        ci.append(person.id_persona.cedula)

    Person.objects.bulk_create(new_persons)
    print(ci)

    #Creación del equipo 
    for reg in preteamregister:    
        #Busquemos si este equipo ha participado antes en un torneo de este mismo tipo de juego
        #Nombre del torneo tal del juego tal
        torneo = Tournament.objects.filter(id_juego__nombre=reg.id_torneo.id_juego.nombre)
        #torneo = Tournament.objects.get(id_juego=Game.objects.get(nombre=nombre))
        try:
            #Revisar query súper yuca
            ant_registro = HistoryParticipation.objects.filter(id_equipo__nombre=reg.id_equipo.nombre, id_torneo__in=torneo)
        except Team.DoesNotExist:
            ant_registro = None

        #Si no existe, creamos al nuevo equipo
        if not ant_registro:
            nuevo_registro_equipo = Team(nombre=reg.id_equipo.nombre, logo=reg.id_equipo.logo)
            nuevo_registro_equipo.save()
        else:
        #Si existe, lo buscamos
            nuevo_registro_equipo = Team.objects.get(id=ant_registro[0].id_equipo.id)
        break
    
    print(nuevo_registro_equipo)

    #Se guarda al equipo en la tabla de clasificados, con la fase del torneo con jerarquía 1 (jerarquía 1 porque es la primera fase del torneo)

    fase_torneo = StageTournament.objects.get(id_torneo=pk_tour,jerarquia=1)
    equipo_clasificado = Classified(id_equipo=nuevo_registro_equipo, id_fase_torneo=fase_torneo)
    equipo_clasificado.save()
    
    #Creamos los registros de los participantes en el torneo
    i=0
    for reg in preteamregister:
        pk_persona = Person.objects.get(cedula=ci[i])

        register_team.append(HistoryParticipation(id_persona=pk_persona, id_equipo=nuevo_registro_equipo, id_torneo=reg.id_torneo, fecha_registro=reg.fecha_registro, rol=reg.rol))
        print(register_team)
        i=i+1

    HistoryParticipation.objects.bulk_create(register_team)

    #Se verifica si la persona ha solicitado inscripcion en otro torneo, si no es asi Se borran los registros de las tablas PrePerson. Siempre se borran los datos de PreTeamRegister
    i=0
    for reg in preteamregister:    
        person_delete = PrePerson.objects.get(cedula=ci[i])
        #Si tiene solamente una solicitud de inscripcion pendiente, se borra
        if (PreTeamRegister.objects.filter(id_persona=person_delete).count() == 1):
            print('paso')
            person_delete.delete()
        i=i+1
    team_delete = PreTeam.objects.get(id=pk_team)
    team_delete.delete()

    messages.success(request, 'Se ha registrado al equipo en el torneo exitosamente')
    return redirect('/inscripciones/pendientes/')


#Anular inscripción
def failInscription(request, pk_team, pk_tour):
    #Buscamos los registros de PreTeamRegister
    preteamregister = PreTeamRegister.objects.filter(id_equipo=pk_team, id_torneo=pk_tour)

    #Se borran los registros de las tablas PrePerson y a su vez de PreTeamRegister
    for reg in preteamregister:
        person = PrePerson.objects.get(id=reg.id_persona.id)
        #Se borra a la persona unicamente si aparece una sola vez en las solicitudes de inscripcion
        if (PreTeamRegister.objects.filter(id_persona=person).count() == 1):
            person.delete()

    team_delete = PreTeam.objects.get(id=pk_team)
    team_delete.delete()

    messages.success(request, 'Se ha anulado la solicitud de inscripción')
    return redirect('/inscripciones/pendientes/')


#Lista de solicitudes de inscripciones
def preinscriptionList(request):
    register = PreTeamRegister.objects.values('id_equipo','id_equipo__nombre','id_torneo','id_torneo__nombre','id_equipo__comentario').distinct('id_equipo')
    cant_pendientes = PreTeamRegister.objects.filter().count()
    print(register)
    print(cant_pendientes)
    context = {
        'register': register,
        'cant_pendientes': cant_pendientes
    }

    return render(request, 'admin/inscription/preinscription_list.html', context)


#Detalle de solicitud de inscripcion
def preinscriptionDetail(request, pk):
    persons = PreTeamRegister.objects.filter(id_equipo=pk)
    
    context = {
        'persons': persons
    }

    return render(request, 'admin/inscription/preinscription_detail.html', context)


#Lista de inscripciones (Lista de equipos)
def inscriptionList(request):
    register = HistoryParticipation.objects.values('id_equipo','id_equipo__nombre','id_equipo__logo','id_torneo__nombre','fecha_registro','fecha_fin').distinct('id_equipo')
    cant_pendientes = HistoryParticipation.objects.filter().count()
    print(register)
    print(cant_pendientes)
    context = {
        'register': register,
        'cant_pendientes': cant_pendientes
    }

    return render(request, 'admin/inscription/inscription_list.html', context)


#Detalle de inscripcion (detalle de equipo)
def inscriptionDetail(request, pk):
    persons = HistoryParticipation.objects.filter(id_equipo=pk)
    
    context = {
        'persons': persons
    }

    return render(request, 'admin/inscription/inscription_detail.html', context)
