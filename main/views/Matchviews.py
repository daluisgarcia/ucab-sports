from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.forms import formset_factory
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from main.models import Tournament, Match, StageTournament
from main.forms import MatchCreateForm

from ..owner import *

#Falta filtrar los torneos de acuerdo al id del organizador
def createMatch(request):
    stages = StageTournament.objects.filter(id_torneo__owner_id=1)
    print(stages)

    if request.method == 'POST':
        match_form = MatchCreateForm(request.POST)
        self.object = None
        if match_form.is_valid():
            object = match_form.save(commit=False)
            object.owner = self.request.user
            object.save()
            # Obtenemos el id último registro del partido (el que se acaba de insertar)
            c = Match.objects.order_by('-id')[0].id
            print(c)
            return redirect('main:create_match', pk=c)

    else:
        match_form = MatchCreateForm(initial=None)


    context = {
        'match_form': match_form,
        'stages': stages
    }

    return render(request, 'admin/matches/match_stages_list.html', context)



#Asociar los equipos al partido
def createTeams(request, pk_torneo, pk_fase):
    print('pk_torneo: '+ pk_torneo +' pk_fase: '+ pk_fase)





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
