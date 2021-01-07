from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.forms import formset_factory
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from main.models import Tournament, Match, StageTournament, Stage
from main.forms import MatchCreateForm, StageTourForMatchForm

from ..owner import *

#Falta filtrar los torneos de acuerdo al id del organizador
def createMatch(request):

    if request.method == 'POST':
        stages = StageTourForMatchForm(request.POST)
        match_form = MatchCreateForm(request.POST)

        if match_form.is_valid() and stages.is_valid():    
            stage=stages['id_fase'].value()
            torneo=stages['id_torneo'].value()
            print('stage:'+ stage +' torneo:'+ torneo)

            #Verificar que la fase y el torneo coinciden
            if (StageTournament.objects.filter(id_fase=stage, id_torneo=torneo).count() > 0):
                match_form.save()
                # Obtenemos el id último registro del partido (el que se acaba de insertar)
                c = Match.objects.order_by('-id')[0].id
                print(c)
                return redirect('main:teams_match', pk_partido=c, pk_torneo=torneo, pk_fase=stage)
        
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


    #Hacer un inlineformset de la participación con el EQUIPO (ya que el partido se mantiene estático)


    cant_equipos = StageTournament.objects.get(id_fase=pk_fase, id_torneo=pk_torneo)
    print()
    context = {
        'cant_equipos': cant_equipos.id_fase.equipos_por_partido
    }

    return render(request, 'admin/matches/teams_match.html', context)



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
