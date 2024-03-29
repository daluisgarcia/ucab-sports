from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.views.generic import ListView, CreateView
from django.forms import formset_factory
from django.contrib import messages
from django.forms.utils import ErrorList
from django.views.generic import DetailView, ListView
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from smtplib import SMTPDataError
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Q

from main.models import PreTeamRegister, PreTeam, PrePerson, StageTournament, Tournament, Person, Team, HistoryParticipation, Game, Classified
from main.forms import TeamRegisterCreateForm, TeamsRegisterFormSet, PreteamCreateForm, PrePersonCreateForm, PersonsFormSet


#REVISAR
#Cuando no se llenan todos los roles, igual pasa el is_valid() (es decir, no debería pasar ese formulario)

#Inscribir a los participantes del torneo
def createRegisterTeam(request, pk_torneo):

    #Obtenemos el torneo
    try:
        tournament = Tournament.objects.get(id=pk_torneo)
    except Tournament.DoesNotExist:
        tournament = None

    #Si el torneo fue eliminado o la inscripción fue cerrada, entonces mandar al usuario a la vista de torneos
    if((not tournament) or (tournament.inscripcion_abierta == False)):
        messages.error(request, 'El torneo al que ha tratado de acceder ha cerrado su inscripción o ha sido eliminado del sistema')
        return redirect('main:posts')

    #Verificamos cuántas personas debe conformar el equipo, esto se hace viendo la fase del torneo que tenga jerarquía = 1
    person_number = StageTournament.objects.get(jerarquia=0, id_torneo=pk_torneo, id_fase__isnull=True).participantes_por_equipo

    #Verificamos si este tipo de torneo es del tipo_delegado = 'd'. Si es así, entonces se agrega una fila más al person_number
    if(tournament.tipo_delegado == 'd'):
        PersonFormSet = formset_factory(PrePersonCreateForm, formset=PersonsFormSet, extra=2)
    else:
        PersonFormSet = formset_factory(PrePersonCreateForm, formset=PersonsFormSet, extra=1)
    #Formset de los participantes
    # Creación del formset, especificando el form y el formset a usar


    #Formset de los roles de los participantes
    # Creación del formset, especificando el form y el formset a usar
    TeamRegisterFormSet = formset_factory(TeamRegisterCreateForm, formset=TeamsRegisterFormSet, extra=person_number)

    if request.method == 'POST':
        person_formset = PersonFormSet(request.POST)
        team_form = PreteamCreateForm(request.POST, request.FILES)
        team_register_formset = TeamRegisterFormSet(request.POST)

        if person_formset.is_valid() and team_form.is_valid() and team_register_formset.is_valid():

            #Definimos context que se retornará si el formulario no cumple todas las validaciones
            context = {
                'inscription_fields': zip(person_formset, team_register_formset),
                'person_formset': person_formset,
                'team_register_formset': team_register_formset,
                'tipo_delegado': tournament.tipo_delegado,
                'team_form': team_form,
                'title': 'Inscribe al equipo y a los participantes',
                'botton_title': 'Inscribirse',
                'person_number': person_number,
            }

            #validar que los roles ingresados cumplan los estándares para este torneo
            for role_form in team_register_formset:
                role = role_form.cleaned_data.get('rol')
                if not role:
                    messages.error(request, 'Debe seleccionar el rol de cada participante')
                    return render(request, 'layouts/inscription/preinscription_form.html', context)

                if((tournament.tipo_delegado == 'd' and role == 'jd') or (tournament.tipo_delegado == 'jd' and role == 'd')):
                    messages.error(request, 'El tipo de participantes no coincide con las reglas para este torneo')
                    return render(request, 'layouts/inscription/preinscription_form.html', context)

            #Verificar que el usuario no trate de inscribirse en el mismo torneo si ya esta inscrito
            for person_form in person_formset:
                cedula = person_form.cleaned_data.get('cedula')
                nombre = person_form.cleaned_data.get('nombre')
                apellido = person_form.cleaned_data.get('apellido')
                    
                if(PreTeamRegister.objects.filter(id_persona__cedula=cedula, id_torneo=pk_torneo) or HistoryParticipation.objects.filter(id_persona__cedula=cedula, id_torneo=pk_torneo)):
                    messages.error(request, 'El usuario '+ nombre +' '+ apellido +' ya se inscribió con anterioridad al torneo.')
                    return render(request, 'layouts/inscription/preinscription_form.html', context)
            
            #Validar que el tamaño de la imagen subida no exceda de los 10MB
            try:
                file_logo = team_form.cleaned_data.get('logo')
            except team_form.cleaned_data.get('logo').DoesNotExist:
                file_logo = None
            
            if(file_logo):
                if(file_logo.size > 10000000):
                    messages.error(request, 'El tamaño del logo subido no puede exceder de 10 MB')
                    return render(request, 'layouts/inscription/preinscription_form.html', context)

            team_form.save()
            #Obtenemos el último registro del equipo
            pk_team = PreTeam.objects.order_by('-id')[0]
            
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
                
            #Con bulk se insertan todos los objetos en el array
            PrePerson.objects.bulk_create(new_persons)
            i=0

            person_email = None
            for role_form in team_register_formset:
                role = role_form.cleaned_data['rol']

                pk_persona = PrePerson.objects.get(cedula=ci[i])

                if (role == 'd' or role == 'jd'):
                    person_email = pk_persona.correo

                if role:
                    new_team_register.append(PreTeamRegister(rol=role, id_equipo=pk_team, id_persona=pk_persona,  id_torneo=tournament))
                i=i+1

            PreTeamRegister.objects.bulk_create(new_team_register)

            try:
                send_mail('Nueva solicitud de participacion',
                          'Tienes una nueva solicitud de participacion para el torneo '+tournament.nombre,
                          tournament.owner.email,
                          [tournament.owner.email])

                send_mail('Solicitud de participacion enviada',
                          'Tu solicitud de participacion fue enviada correctamente, estate atento a este correo por cualquier informacion\n'+
                          'Para cualquier duda o problema puedes contactarte con el organizador del torneo a traves del correo: '+tournament.owner.email,
                          tournament.owner.email,
                          [person_email])
            except SMTPDataError:
                messages.success(request, 'Tu solicitud fue procesada pero hubo un error en el envio de correos, ponte en contacto con el organizador')
                return redirect('main:posts')

            messages.success(request, 'La solicitud de inscripción al torneo se ha procesado satisfactoriamente')
            return redirect('main:posts')
        
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
        'inscription_fields': zip(person_formset, team_register_formset),
        'person_formset': person_formset,
        'tipo_delegado': tournament.tipo_delegado,
        'team_form': team_form,
        'title': 'Inscribe al equipo y a los participantes', 
        'botton_title': 'Inscribirse',
        'person_number': person_number,
    } 

    return render(request, 'layouts/inscription/preinscription_form.html', context)



#Aprobar inscripción
@login_required
def approveInscription(request, pk_team, pk_tour):
    #Buscamos los registros de PreTeamRegister
    preteamregister = PreTeamRegister.objects.filter(id_equipo=pk_team, id_torneo=pk_tour)

    #Arrays donde se ingresarán los datos
    new_persons = []
    register_team = []
    ci = []
    #Creamos los registros de los participantes
    
    for person in preteamregister:
        
        #Comparamos con los anteriores registros a ver si este participante ha participado antes en algo
        try:
            anterior_registro = Person.objects.get(cedula=person.id_persona.cedula)
        except Person.DoesNotExist:
            anterior_registro = None

        if anterior_registro is not None:

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

    #Creación del equipo 
    for reg in preteamregister:    
        #Busquemos si este equipo ha participado antes en un torneo de este mismo tipo de juego
        #Nombre del torneo tal del juego tal
        torneo = Tournament.objects.filter(id_juego__nombre=reg.id_torneo.id_juego.nombre)

        try:
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

    #Se guarda al equipo en la tabla de clasificados, con la fase del torneo con jerarquía 0 (jerarquía 0 porque es la fase de inscripcion)
    try:
        fase_torneo = StageTournament.objects.get(id_torneo=pk_tour,jerarquia=0)
    except StageTournament.DoesNotExist:
        fase_torneo = None

    #Si no se encuentra la fase torneo con jerarquía 0, entonces es que se cerró la inscripción, por lo tanto, hay que buscar la fase con jerarquia 1
    if(not fase_torneo):
        fase_torneo = StageTournament.objects.get(id_torneo=pk_tour,jerarquia=1)
    

    equipo_clasificado = Classified(id_equipo=nuevo_registro_equipo, id_fase_torneo=fase_torneo)
    equipo_clasificado.save()
    
    #Creamos los registros de los participantes en el torneo
    i=0
    for reg in preteamregister:
        pk_persona = Person.objects.get(cedula=ci[i])

        register_team.append(HistoryParticipation(id_persona=pk_persona, id_equipo=nuevo_registro_equipo, id_torneo=reg.id_torneo, fecha_registro=reg.fecha_registro, rol=reg.rol))
        i=i+1

    HistoryParticipation.objects.bulk_create(register_team)

    #Se verifica si la persona ha solicitado inscripcion en otro torneo, si no es asi Se borran los registros de las tablas PrePerson. Siempre se borran los datos de PreTeamRegister
    i=0
    email_person = None
    tournament = None
    for reg in preteamregister:    
        person_delete = PrePerson.objects.get(cedula=ci[i])
        # Se obtiene el delegado o jugador delegado para el envio de correo
        if reg.rol == 'd' or reg.rol == 'jd':
            email_person = reg.id_persona
        tournament = reg.id_torneo
        #Si tiene solamente una solicitud de inscripcion pendiente, se borra
        if (PreTeamRegister.objects.filter(id_persona=person_delete).count() == 1):
            person_delete.delete()
        i=i+1
    team_delete = PreTeam.objects.get(id=pk_team)
    team_delete.delete()
    try:
        send_mail('Participacion aprobada',
                  'Tu solicitud de participacion al torneo '+tournament.nombre+' fue aprobada por el organizador\n'+
                  'Para cualquier duda o problema puedes contactarte con el organizador del torneo a traves del correo: '+tournament.owner.email,
                  tournament.owner.email,
                  [email_person.correo])
    except SMTPDataError:
        messages.success(request, 'No se pudo enviar el correo al delegado pero se ha registrado al equipo en el torneo')
        return redirect('main:inscription_list')

    messages.success(request, 'Se ha registrado al equipo en el torneo exitosamente')
    return redirect('main:inscription_list')


#Anular inscripción
@login_required
def failInscription(request, pk_team, pk_tour):
    #Buscamos los registros de PreTeamRegister
    preteamregister = PreTeamRegister.objects.filter(id_equipo=pk_team, id_torneo=pk_tour)

    email_person = None
    tournament = None
    #Se borran los registros de las tablas PrePerson y a su vez de PreTeamRegister
    for reg in preteamregister:
        person = PrePerson.objects.get(id=reg.id_persona.id)
        # Se obtiene el delegado o jugador delegado para el envio de correo
        if reg.rol == 'd' or reg.rol == 'jd':
            email_person = reg.id_persona
        tournament = reg.id_torneo
        #Se borra a la persona unicamente si aparece una sola vez en las solicitudes de inscripcion
        if (PreTeamRegister.objects.filter(id_persona=person).count() == 1):
            person.delete()

    team_delete = PreTeam.objects.get(id=pk_team)
    message = team_delete.comentario
    team_delete.logo.delete(save=True)
    team_delete.delete()

    try:
        send_mail('Participacion rechazada',
                  'Tu solicitud de participacion al torneo '+tournament.nombre+' fue rechazada por el organizador. Motivo: '+str(message)+'\n'+
                  'Para cualquier duda o problema puedes contactarte con el organizador del torneo a traves del correo: '+tournament.owner.email,
                  tournament.owner.email,
                  [email_person.correo])
    except SMTPDataError:
        messages.success(request, 'No se pudo enviar el correo al delegado pero se ha anulado la solicitud de inscripción')
        return redirect('main:inscription_list')

    messages.success(request, 'Se ha anulado la solicitud de inscripción')
    return redirect('main:inscription_list')


#Lista de solicitudes de inscripciones
@login_required
def preinscriptionList(request): 
    #Lista de las solicitudes pendientes
    register = PreTeamRegister.objects.filter(id_torneo__owner=request.user).values('id_equipo','id_equipo__nombre','id_equipo__logo','id_torneo','id_torneo__nombre','id_equipo__comentario').order_by('id_equipo','id_torneo','fecha_registro').distinct('id_equipo')

    solicitudes_pendientes = PreTeamRegister.objects.filter(id_torneo__owner=request.user).distinct('id_equipo')

    #Cantidad de solicitudes aprobadas por torneo
    torneos = []
    inscritos = []
    for solicitudes in solicitudes_pendientes:
        if not solicitudes.id_torneo in torneos:
            torneos.append(solicitudes.id_torneo)

    for i in torneos:
        solicitudes_aprobadas = HistoryParticipation.objects.filter(id_torneo=i).distinct('id_equipo').count()
        inscritos.append({'nombre_torneo': i.nombre, 'cantidad_inscritos': solicitudes_aprobadas})

    #Cantidad de solicitudes pendientes
    cant_pendientes = PreTeamRegister.objects.filter(id_torneo__owner=request.user).count()

    context = {
        'register': register,
        'cant_pendientes': cant_pendientes,
        'inscritos': inscritos
        }

    return render(request, 'admin/inscription/preinscription_list.html', context)


#Detalle de solicitud de inscripcion
def preinscriptionDetail(request, pk):
    persons = PreTeamRegister.objects.filter(id_equipo=pk)
    
    context = {
        'persons': persons
    }

    return render(request, 'admin/inscription/preinscription_detail.html', context)


class InscriptionList(LoginRequiredMixin, ListView):
    template_name = 'admin/inscription/inscription_list.html'
    paginate_by = 10

    def get_queryset(self):
        query = None

        if self.request.GET.get('cedula'):
            query = Q(id_persona__cedula = self.request.GET['cedula'])

        if self.request.GET.get('name'):
            if query:
                query.add(Q(id_persona__nombre__contains = self.request.GET['name']), Q.AND)
            else:
                query = Q(id_persona__nombre__contains = self.request.GET['name'])

        if self.request.GET.get('lastname'):
            if query:
                query.add(Q(id_persona__apellido__contains = self.request.GET['lastname']), Q.AND)
            else:
                query = Q(id_persona__apellido__contains = self.request.GET['lastname'])

        if query:
            return HistoryParticipation.objects.filter(query).order_by('id_persona__cedula').distinct('id_persona__cedula')
        else:
            return HistoryParticipation.objects.order_by('id_persona__cedula').distinct('id_persona__cedula')

    def get_context_data(self):
        ctx = super(InscriptionList, self).get_context_data()

        return ctx


#Detalle de inscripcion (detalle del usuario)
@login_required
def inscriptionDetail(request, pk):
    person = Person.objects.get(id=pk)
    teams = HistoryParticipation.objects.filter(id_persona=person).order_by('-fecha_registro')

    for team in teams:

        places = Classified.objects.filter(id_equipo=team.id_equipo, id_fase_torneo__id_torneo=team.id_torneo)

        max_position = 0
        last_stage = None
        #Validate if the team is in stage with hierarchy 0
        if(places.first().id_fase_torneo.jerarquia != 0):
            for place in places:
                if(place.id_fase_torneo.jerarquia > max_position):
                    max_position = place.id_fase_torneo.jerarquia
                    last_stage = place.id_fase_torneo.id_fase

        team.last_stage = last_stage
    
    context = {
        'person': person,
        'teams': teams
    }

    return render(request, 'admin/inscription/inscription_detail.html', context)
