from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.forms import formset_factory
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from main.models import Tournament, Match, StageTournament, Stage, Participation, Team, Classified
from main.forms import MatchCreateForm, StageTourForMatchForm, ParticipationCreateForm, ParticipationFormSet

#Falta filtrar los torneos de acuerdo al id del organizador
def createMatch(request):

    if request.method == 'POST':
        stages = StageTourForMatchForm(request.POST)
        match_form = MatchCreateForm(request.POST)

        if match_form.is_valid() and stages.is_valid():    
            stage = stages['id_fase'].value()
            torneo = stages['id_torneo'].value()
            print('stage:'+ stage +' torneo:'+ torneo)

            #Verificar que la fase y el torneo coinciden
            if (StageTournament.objects.filter(id_fase=stage, id_torneo=torneo).count() > 0):
                #Buscamos la fase del torneo y la asociamos al partido
                stage_tour = StageTournament.objects.get(id_fase=stage, id_torneo=torneo)
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
                return redirect('main:teams_match', pk_partido=partido, pk_torneo=torneo, pk_fase=stage)
        
            #En caso de que la fase y el torneo no coinciden
            else:
                messages.error(request, 'La Fase y el torneo seleccionados no coinciden')
                match_form = MatchCreateForm(initial=None)
                stages = StageTourForMatchForm()

    else:
        match_form = MatchCreateForm(initial=None)
        stages = StageTourForMatchForm()

    context = {
        'match_form': match_form,
        'stages': stages
    }

    return render(request, 'admin/matches/match_stages_list.html', context)



#Asociar los equipos al partido
def createTeams(request, pk_partido, pk_torneo, pk_fase):
    print('pk_partido: '+ pk_partido +' pk_torneo: '+ pk_torneo +' pk_fase: '+ pk_fase)
    
    #Lógica para traerse a los clasificados de la fase
    #Fase del torneo
    fase_torneo = StageTournament.objects.get(id_fase=pk_fase, id_torneo=pk_torneo)
    print(fase_torneo.id)
    print(fase_torneo.equipos_por_partido)    
    #clasificados de esta fase del torneo
    clasificados = Classified.objects.filter(id_fase_torneo=fase_torneo)
    #Equipos
    print(clasificados)


    #LOGICA DE LOS CLASIFICADOS. AYUDA DANIEL C:
    #Lista clasificados
    lista_equipos = {}
    for i in range(1, fase_torneo.equipos_por_partido+1):
        lista_equipos[i] = clasificados


    #Formset de los equipos que participaron en el partido
    #Creación del formset, especificando el form y el formset a usar. La cantidad de campos está definida por los equipos por partido.
    PartFormSet = formset_factory(ParticipationCreateForm, formset=ParticipationFormSet, extra=fase_torneo.equipos_por_partido)

    #Manejar la lógica de los formularios
    if request.method == 'POST':
        participacion_formset = PartFormSet(request.POST)
        print(participacion_formset)

        if participacion_formset.is_valid():
            print('formset válido')
            partido = Match.objects.get(id=pk_partido)

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
        'participacion_formset': participacion_formset
    }

    return render(request, 'admin/matches/teams_match.html', context)



#Lista de solicitudes de inscripciones
def matchList(request):
    print(request.user)
    matches = Match.objects.filter(id_fase_torneo__id_torneo__owner=request.user).order_by('id_fase_torneo__id_torneo')

    context = {
        'match_list': matches
    }
    return render(request, 'admin/matches/match_list.html', context)
