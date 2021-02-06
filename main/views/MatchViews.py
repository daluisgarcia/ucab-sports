from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.forms import formset_factory
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib.auth.mixins import LoginRequiredMixin

from main.models import Tournament, Match, StageTournament, Stage, Participation, Team, Classified
from main.forms import MatchCreateForm, ParticipationCreateForm, ParticipationFormSet

#Falta filtrar los torneos de acuerdo al id del organizador
def createMatch(request):

    if request.method == 'POST':
        match_form = MatchCreateForm(request.POST)
        #Fases y torneos
        stg = request.POST.get('stage', None)
        tour = request.POST.get('tournament', None)
        stage = Stage.objects.get(id=stg)
        tournament = Tournament.objects.get(id=tour)

        if match_form.is_valid():    
            print('stage:'+ stg +' torneo:'+ tour)

            #Verificar que la fase y el torneo coinciden
            if (StageTournament.objects.filter(id_fase=stage, id_torneo=tournament).count() > 0):
                #Buscamos la fase del torneo y la asociamos al partido
                stage_tour = StageTournament.objects.get(id_fase=stage, id_torneo=tournament)
                #Objeto del partido
                print(match_form['fecha'].value())
                match = Match(
                    fecha=match_form['fecha'].value(), 
                    direccion=match_form['direccion'].value(), id_fase_torneo=stage_tour
                )
                #Guardamos el partido
                match.save()
                # Obtenemos el id último registro del partido (el que se acaba de insertar)
                partido = Match.objects.order_by('-id')[0].id
                print(partido)
                return redirect('main:teams_match', pk_partido=partido, pk_torneo=tour, pk_fase=stg)
        
            #En caso de que la fase y el torneo no coinciden
            else:
                messages.error(request, 'La Fase y el torneo seleccionados no coinciden')
                match_form = MatchCreateForm(initial=None)

    else:
        match_form = MatchCreateForm(initial=None)

    stg = Stage.objects.all()
    tour = Tournament.objects.filter(owner=request.user, inscripcion_abierta=False)

    context = {
        'match_form': match_form,
        'stage': stg, 
        'tour': tour
    }

    return render(request, 'admin/matches/match_stages_list.html', context)



#Asociar los equipos al partido
def createTeams(request, pk_partido, pk_torneo, pk_fase):
    print('pk_partido: '+ pk_partido +' pk_torneo: '+ pk_torneo +' pk_fase: '+ pk_fase)
    
    #Lógica para traerse a los clasificados de la fase
    #Fase del torneo
    fase_torneo = StageTournament.objects.get(id_fase=pk_fase, id_torneo=pk_torneo)
    #print(fase_torneo.equipos_por_partido)

    #clasificados de esta fase del torneo
    clasificados = Classified.objects.filter(id_fase_torneo=fase_torneo).order_by("grupo")
    #Equipos
    #print(clasificados)

    if(clasificados.first().grupo):
        groups = True
    else:
        groups = False


    #Formset de los equipos que participaron en el partido
    #Creación del formset, especificando el form y el formset a usar. La cantidad de campos está definida por los equipos por partido.
    PartFormSet = formset_factory(ParticipationCreateForm, formset=ParticipationFormSet, extra=fase_torneo.equipos_por_partido)

    #Manejar la lógica de los formularios
    if request.method == 'POST':
        participacion_formset = PartFormSet(request.POST)
        #print(participacion_formset)

        if participacion_formset.is_valid():
            partido = Match.objects.get(id=pk_partido)

            #REVISAR

            #Validar que, si la fase es por grupos, los equipos seleccionados sean del mismo grupo
            
            if groups:
                print('hay grupos')

                #variables necesarias para manejar la lógica de las validaciones
                i = 0
                lista_grupos = []
                grupo_anterior = None
                grupo_actual = None

                for part in participacion_formset:
                    num_equipo = 'equipo-' + str(i)
                    i = i + 1
                    equipo = request.POST.get(num_equipo, None)
                    
                    #Buscamos el número del grupo de este equipo y lo comparamos con el anterior
                    for clas in clasificados:
                        if(clas.id_equipo.id == int(equipo)):
                            grupo_actual = clas.grupo

                    #Validamos que no hayan equipos repetidos y que los equipos sean del mismo grupo
                    if ((equipo not in lista_grupos) and ((grupo_anterior == None) or (grupo_actual == grupo_anterior))):
                        lista_grupos.append(equipo)
                        print(lista_grupos)
                        grupo_anterior = grupo_actual
                    else:
                        messages.error(request, 'Los equipos no se pueden repetir y tiene que elegir equipos que pertenezcan al mismo grupo.')
                                            
                        i = 0
                        for part in participacion_formset:
                            part.valor = i
                            i = i + 1

                        context = {
                            'equipos': Classified.objects.filter(id_fase_torneo=fase_torneo).order_by("grupo"),
                            'participacion_formset': participacion_formset,
                            'grupos': groups
                        }

                        return render(request, 'admin/matches/teams_match.html', context)
            
            i = 0
            for part in participacion_formset:
                num_equipo = 'equipo-' + str(i)
                i = i + 1
                equipo = request.POST.get(num_equipo, None)
                print(equipo)
                equipo_object = Team.objects.get(id=equipo)

                participacion = Participation(
                    id_equipo=equipo_object, 
                    id_partido=partido, 
                    ganador=part['ganador'].value() if part['ganador'].value() else None, 
                    puntos_equipo=part['puntos_equipo'].value() if part['puntos_equipo'].value() else None)
                participacion.save()

            messages.success(request, 'El partido se ha creado satisfactoriamente')
            return redirect(reverse_lazy('main:match_list'))

    else:
        participacion_formset = PartFormSet(initial=None)

    i = 0
    for part in participacion_formset:
        part.valor = i
        i = i + 1

    context = {
        'equipos': clasificados,
        'participacion_formset': participacion_formset,
        'grupos': groups
    }

    return render(request, 'admin/matches/teams_match.html', context)



#Lista de solicitudes de inscripciones
def matchList(request):
    print(request.user)
    matches = Match.objects.filter(id_fase_torneo__id_torneo__owner=request.user).order_by('id_fase_torneo__id_torneo', 'id_fase_torneo__id_fase')

    context = {
        'match_list': matches
    }
    return render(request, 'admin/matches/match_list.html', context)



''' 
Render the detail view or redirect to the main page if user is not the owner

Shows the detail for a match
'''
def matchInfo(request, pk):
    match = Match.objects.get(id=pk)
    if match.id_fase_torneo.id_torneo.owner == request.user:
        match_teams = Participation.objects.filter(id_partido=pk)
        return render(request, 'admin/matches/match_detail.html', {'match': match, 'matchTeams': match_teams})
    return redirect('main:admin_index')


#Eliminar partido
def deleteMatch(request, pk):
    print(pk)
    match = Match.objects.get(id=pk)
    match.delete()
    print('Torneo eliminado')
    return redirect(reverse_lazy('main:match_list'))

