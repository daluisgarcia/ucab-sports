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
        #Fases y torneos
        stg = request.POST.get('stage', None)
        tour = request.POST.get('tournament', None)
        stage = Stage.objects.get(id=stg)
        tournament = Tournament.objects.get(id=tour)
    
        print('stage:'+ stg +' torneo:'+ tour)

        #Verificar que hayan clasificados en esta fase de este torneo
        if (Classified.objects.filter(id_fase_torneo__id_fase=stage, id_fase_torneo__id_torneo=tournament).count() != 0):
            
            #Verificar que la fase y el torneo coinciden
            if (StageTournament.objects.filter(id_fase=stage, id_torneo=tournament).count() > 0):
                
                return redirect('main:teams_match', pk_torneo=tour, pk_fase=stg)
                
            #En caso de que la fase y el torneo no coinciden
            else:
                messages.error(request, 'La Fase y el torneo seleccionados no coinciden')

        #En caso de que la fase y el torneo no coinciden
        else:
            messages.error(request, 'No hay equipos clasificados en esta fase')

        


    stg = Stage.objects.all()
    tour = Tournament.objects.filter(owner=request.user, inscripcion_abierta=False)

    context = {
        'stage': stg, 
        'tour': tour
    }

    return render(request, 'admin/matches/match_stages_list.html', context)



#Associate the teams to the match
def createTeams(request, pk_torneo, pk_fase):
    print('pk_torneo: '+ pk_torneo +' pk_fase: '+ pk_fase)
    
    fase_torneo = StageTournament.objects.get(id_fase=pk_fase, id_torneo=pk_torneo)
    #print(fase_torneo.equipos_por_partido)

    #clasified in this stage
    clasificados = Classified.objects.filter(id_fase_torneo=fase_torneo).order_by("grupo")

    if(clasificados.first().grupo):
        groups = True
    else:
        groups = False

    #Teams formset that participate in the match
    #Formset creation, 
    #Creación del formset, specifying the form and formset to use. The number of fields is defined by the teams per game.
    PartFormSet = formset_factory(ParticipationCreateForm, formset=ParticipationFormSet, extra=fase_torneo.equipos_por_partido)

    #Manage the form logic
    if request.method == 'POST':
        match_form = MatchCreateForm(request.POST)
        participacion_formset = PartFormSet(request.POST)

        if participacion_formset.is_valid() and match_form.is_valid():

            #Validate if the stage is by groups, selected teams are in the same group
            if groups:
                print('hay grupos')

                #necessary variables for manage the validation logic
                i = 0
                lista_grupos = []
                grupo_anterior = None
                grupo_actual = None

                for part in participacion_formset:
                    num_equipo = 'equipo-' + str(i)
                    i = i + 1
                    equipo = request.POST.get(num_equipo, None)
                    
                    #Searching the group number of this teams and comparing with the previous
                    for clas in clasificados:
                        if(clas.id_equipo.id == int(equipo)):
                            grupo_actual = clas.grupo

                    #Validate that teams aren't repeated and the selected teams are in the same group
                    if ((equipo not in lista_grupos) and ((grupo_anterior == None) or (grupo_actual == grupo_anterior))):
                        lista_grupos.append(equipo)
                        print(lista_grupos)
                        grupo_anterior = grupo_actual
                    else:
                        messages.error(request, 'Los equipos seleccionados no pertenecen al mismo grupo.')
                                            
                        i = 0
                        for part in participacion_formset:
                            part.valor = i
                            i = i + 1

                        context = {
                            'equipos': clasificados,
                            'match_form': match_form,
                            'participacion_formset': participacion_formset,
                            'grupos': groups
                        }

                        return render(request, 'admin/matches/teams_match.html', context)
            
            #Validate if teams are the same
            i = 0
            teams = []
            for part in participacion_formset:
                num_equipo = 'equipo-' + str(i)
                
                equipo = request.POST.get(num_equipo, None)
                
                if(equipo in teams):
                    #returns error
                    messages.error(request, 'Los equipos no se pueden repetir.')
                                            
                    i = 0
                    for part in participacion_formset:
                        part.valor = i
                        i = i + 1

                    context = {
                        'equipos': clasificados,
                        'match_form': match_form,
                        'participacion_formset': participacion_formset,
                        'grupos': groups
                    }

                    return render(request, 'admin/matches/teams_match.html', context)

                teams.append(equipo)
                i = i + 1    

            #team object
            print(match_form['fecha'].value())
            match = Match(
                fecha=match_form['fecha'].value(), 
                direccion=match_form['direccion'].value(), id_fase_torneo=fase_torneo
            )
            #save match
            match.save()

            #save participations of the match
            i = 0
            for part in participacion_formset:
                num_equipo = 'equipo-' + str(i)
                i = i + 1
                equipo = request.POST.get(num_equipo, None)
                print(equipo)
                equipo_object = Team.objects.get(id=equipo)

                participacion = Participation(
                    id_equipo=equipo_object, 
                    id_partido=match, 
                    ganador=part['ganador'].value() if part['ganador'].value() else None, 
                    puntos_equipo=part['puntos_equipo'].value() if part['puntos_equipo'].value() else None,
                    score=part['score'].value() if part['score'].value() else None
                )
                participacion.save()

            messages.success(request, 'El partido se ha creado satisfactoriamente')
            return redirect(reverse_lazy('main:match_list'))

    else:
        match_form = MatchCreateForm(initial=None)
        participacion_formset = PartFormSet(initial=None)

    i = 0
    for part in participacion_formset:
        part.valor = i
        i = i + 1

    context = {
        'equipos': clasificados,
        'match_form': match_form,
        'participacion_formset': participacion_formset,
        'grupos': groups
    }

    return render(request, 'admin/matches/teams_match.html', context)



#Actualizar partido
def updateMatch(request, pk):
   
    #partido y los clasificados
    match = Match.objects.get(id=pk)
    participacion = Participation.objects.filter(id_partido=pk)
    #buscamos a los equipos en la tabla de clasificados
    clasificados = Classified.objects.filter(id_fase_torneo=match.id_fase_torneo).order_by("grupo")

    if(clasificados.first().grupo):
        groups = True
    else:
        groups = False


    #Formset de los equipos que participaron en el partido
    #Creación del formset, especificando el form y el formset a usar. La cantidad de campos está definida por los equipos por partido.
    PartFormSet = formset_factory(ParticipationCreateForm, formset=ParticipationFormSet)

    #participacion_formset = PartFormSet(queryset=participacion, instance=match)
    

    if request.method == 'POST':
        match_form = MatchCreateForm(request.POST, instance=match)
        participacion_formset = PartFormSet(request.POST)

        if match_form.is_valid() and participacion_formset.is_valid():

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
                            'equipos': clasificados,
                            'match_form': match_form,
                            'participacion_formset': participacion_formset,
                            'grupos': groups
                        }

                        return render(request, 'admin/matches/teams_match.html', context)

            match_form.save()
            participacion_formset.save()

            return redirect('main:match_list')
        
    else:
        """
        El problema del participation_formset creo que tiene que ver con el campo checkbox en el form
        Hay que revisar detalladamente
        """
        match_form = MatchCreateForm(instance=match)
        #participacion_formset = PartFormSet(queryset=participacion, instance=match)
        participacion_formset = PartFormSet(instance=match)

    i = 0
    for part in participacion_formset:
        part.valor = i
        i = i + 1

    context = {
        'equipos': clasificados,
        'match_form': match_form,
        'participacion_formset': participacion_formset,
        'grupos': groups
    }

    return render(request, 'admin/matches/teams_match.html', context)



#Lista de partidos
def matchList(request):
    print(request.user)
    matches = Match.objects.filter(id_fase_torneo__id_torneo__owner=request.user).order_by('id_fase_torneo__id_torneo', 'id_fase_torneo__id_fase', '-fecha')

    context = {
        'match_list': matches
    }
    return render(request, 'admin/matches/match_list.html', context)



#Match list for the common users
def publicMatchList(request, pk_torneo):

    stages = StageTournament.objects.filter(id_torneo=pk_torneo)
    matches = Match.objects.filter(id_fase_torneo__id_torneo=pk_torneo).order_by('id_fase_torneo__id_fase', '-fecha')
    participation = Participation.objects.filter(id_partido__id_fase_torneo__id_torneo=pk_torneo).order_by('id_partido')

    #Fases que tengan al menos un partido
    stage_with_match = Match.objects.filter(id_fase_torneo__id_torneo=pk_torneo).distinct('id_fase_torneo__id_fase')
    print(stage_with_match)

    context = {
        'stages': stages,
        'match_list': matches,
        'participation': participation,
        'stage_with_match': stage_with_match
    }
    return render(request, 'layouts/matches/public_matches.html', context)


''' 
Render the detail view or redirect to the main page if user is not the owner

Shows the detail for a match
'''
def matchInfo(request, pk):
    match = Match.objects.get(id=pk)
    if match.id_fase_torneo.id_torneo.owner == request.user:
        match_teams = Participation.objects.filter(id_partido=pk)
        print(match_teams)

        context = {
            'match': match,
            'matchTeams': match_teams
        }

        return render(request, 'admin/matches/match_detail.html', context)
    return redirect('main:admin_index')

 

#Eliminar partido
def deleteMatch(request, pk):
    print(pk)
    match = Match.objects.get(id=pk)
    match.delete()
    print('Torneo eliminado')
    return redirect(reverse_lazy('main:match_list'))


