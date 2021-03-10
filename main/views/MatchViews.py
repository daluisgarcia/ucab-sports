import os
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from django.forms import formset_factory
from django.contrib import messages
from django.views.generic import ListView, CreateView, UpdateView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from django.forms import model_to_dict
from django.db.models import Q

from main.models import Tournament, Match, StageTournament, Stage, Participation, Team, Classified
from main.forms import MatchCreateForm, ParticipationCreateForm, ParticipationFormSet

#Falta filtrar los torneos de acuerdo al id del organizador
@login_required
def createMatch(request):

    if request.method == 'POST':
        #Fases y torneos
        stg = request.POST.get('stage', None)
        tour = request.POST.get('tournament', None)
        stage = Stage.objects.get(id=stg)
        tournament = Tournament.objects.get(id=tour)

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

    #Validar que existan al menos 1 torneo y 1 fase en el sistema
    try:
        stg = Stage.objects.all()
    except Stage.DoesNotExist:
        stg = None

    try:
        tour = Tournament.objects.filter(owner=request.user, inscripcion_abierta=False)
    except Tournament.DoesNotExist:
        tour = None
        
    if((not stg) or (not tour)):
        messages.error(request, 'Debe existir al menos una fase y un torneo dentro del sistema')
        return redirect(reverse_lazy('main:match_list'))

    context = {
        'stage': stg, 
        'tour': tour
    }

    return render(request, 'admin/matches/match_stages_list.html', context)



#Associate the teams to the match
@login_required
def createTeams(request, pk_torneo, pk_fase):
    fase_torneo = StageTournament.objects.get(id_fase=pk_fase, id_torneo=pk_torneo)

    #clasified in this stage
    clasificados = Classified.objects.filter(id_fase_torneo=fase_torneo).order_by("grupo")

    if clasificados.first() == None:
        messages.error(request, 'Debes pasar equipos a esa fase para poder hacer eso.')
        return redirect('main:tournament_detail', pk_torneo)

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
                        if 'next' in request.POST.keys():
                            context['next'] = request.POST['next']

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
                    if 'next' in request.POST.keys():
                        context['next'] = request.POST['next']

                    return render(request, 'admin/matches/teams_match.html', context)

                teams.append(equipo)
                i = i + 1    

            #Obtener hora ingresada
            hora = request.POST.get('match-time', None)
            if not hora:
                hora = '00:00'
            fecha_completa = match_form['fecha'].value() + ' ' + hora

            #team object
            match = Match(
                fecha=fecha_completa, 
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
            if 'next' in request.POST.keys():
                return redirect(request.POST['next'])
            return redirect('main:match_list')

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

    if 'next' in request.GET.keys():
        context['next'] = request.GET['next']

    return render(request, 'admin/matches/teams_match.html', context)

#Actualizar partido
@login_required
def updateMatch(request, pk):
   
    #partido y los clasificados
    #match = Match.objects.get(id=pk)
    match = get_object_or_404(Match, pk=pk)
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

    if request.method == 'POST':
        match_form = MatchCreateForm(request.POST, instance=match)
        participacion_formset = PartFormSet(request.POST)

        if match_form.is_valid() and participacion_formset.is_valid():

            #Obtener hora ingresada
            hora = request.POST.get('match-time', None)
            if not hora:
                hora = '00:00'
            fecha_completa = match_form['fecha'].value() + ' ' + hora

            to_update = []

            context = {
                'equipos': clasificados,
                'match_form': match_form,
                'participacion_formset': participacion_formset,
                'grupos': groups,
                'update': True,
                'get_request': False,
                'hora': hora
            }

            if 'next' in request.POST.keys() and request.POST['next']:
                context['next']  = request.POST['next']

            #Validar que, si la fase es por grupos, los equipos seleccionados sean del mismo grupo
            if groups:
                #variables necesarias para manejar la lógica de las validaciones
                i = 0
                lista_grupos = []
                grupo_anterior = None
                grupo_actual = None

                for part in participacion_formset:
                    num_equipo = 'equipo-' + str(i)
                    equipo = request.POST.get(num_equipo, None)
                    
                    #Buscamos el número del grupo de este equipo y lo comparamos con el anterior
                    for clas in clasificados:
                        if(clas.id_equipo.id == int(equipo)):
                            grupo_actual = clas.grupo

                    #Validamos que no hayan equipos repetidos y que los equipos sean del mismo grupo
                    if ((equipo not in lista_grupos) and ((grupo_anterior == None) or (grupo_actual == grupo_anterior))):
                        lista_grupos.append(equipo)
                        grupo_anterior = grupo_actual

                        # Se asignan los datos para actualizar
                        p = participacion[i]
                        p.ganador = part.cleaned_data.get('ganador')
                        p.puntos_equipo = part.cleaned_data.get('puntos_equipo')
                        p.score = part.cleaned_data.get('score')
                        p.id_equipo = get_object_or_404(Team, pk=equipo)

                        to_update.append(p)
                        i = i + 1
                    else:
                        messages.error(request, 'Los equipos no se pueden repetir y tiene que elegir equipos que pertenezcan al mismo grupo.')
                                            
                        i = 0
                        for part in participacion_formset:
                            part.valor = i
                            part.equipo = participacion[i].id_equipo.id
                            i = i + 1

                        return render(request, 'admin/matches/teams_match.html', context)
            else:
                # No existen grupos
                i = 0
                lista_grupos = []

                for part in participacion_formset:
                    num_equipo = 'equipo-' + str(i)
                    equipo = request.POST.get(num_equipo, None)

                    # Validamos que no hayan equipos repetidos y que los equipos sean del mismo grupo
                    if (equipo not in lista_grupos):
                        lista_grupos.append(equipo)

                        # Se asignan los datos para actualizar
                        p = participacion[i]
                        p.ganador = part.cleaned_data.get('ganador')
                        p.puntos_equipo = part.cleaned_data.get('puntos_equipo')
                        p.score = part.cleaned_data.get('score')
                        p.id_equipo = get_object_or_404(Team, pk=equipo)

                        to_update.append(p)
                        i = i + 1
                    else:
                        messages.error(request, 'Los equipos no se pueden repetir')

                        i = 0
                        for part in participacion_formset:
                            part.valor = i
                            part.equipo = participacion[i].id_equipo.id
                            i = i + 1

                        return render(request, 'admin/matches/teams_match.html', context)

            #Se arma el partido que se va a guardar match_form
            Match.objects.filter(id=pk).update(fecha=fecha_completa, direccion=match_form['direccion'].value())
            
            # Se actualizan los registros de participacion
            for part in to_update:
                part.save()
            
            messages.success(request, 'Se han actualizado los partidos correctamente.')

            if 'next' in request.POST.keys() and request.POST['next']:
                return redirect(request.POST['next'])

            return redirect('main:match_list')
         
    else:
        match_form = MatchCreateForm(instance=match)
        
        fecha = match_form['fecha'].value()
        fecha = str(fecha)

        partido = Match(fecha=fecha[0:10], direccion=match_form['direccion'].value())

        match_form = MatchCreateForm(instance=partido)

        hora = fecha[11:16]

        part_array = {}
        part_array['form-INITIAL_FORMS'] = str(0)
        cont = 0
        for part in participacion:
            dict = model_to_dict(part)
            #part_array['form-' + str(cont) + '-id'] = dict['id']
            part_array['form-' + str(cont) + '-ganador'] = dict['ganador']
            part_array['form-' + str(cont) + '-puntos_equipo'] = dict['puntos_equipo']
            part_array['form-' + str(cont) + '-score'] = dict['score']
            cont += 1
        part_array['form-TOTAL_FORMS'] = str(cont)
        participacion_formset = PartFormSet(part_array)

    i = 0
    for part in participacion_formset:
        part.valor = i
        part.equipo = participacion[i].id_equipo.id
        i = i + 1

    context = {
        'equipos': clasificados,
        'match_form': match_form,
        'participacion_formset': participacion_formset,
        'grupos': groups,
        'update': True,
        'get_request': True,
        'hora': hora
    }

    if 'next' in request.GET.keys() and request.GET['next']:
        context['next'] = request.GET['next']

    return render(request, 'admin/matches/teams_match.html', context)


#Lista de partidos
class MatchList(LoginRequiredMixin, ListView):
    template_name = 'admin/matches/match_list.html'
    model = Match
    paginate_by = 5

    def get_queryset(self):
        query = None  # Query builder

        # Validates some parameters from request to filter if necessary
        if self.request.GET.get('tournament') and self.request.GET.get('stage'):
            stage_tournament = StageTournament.objects.filter(
                id_fase=self.request.GET['stage'],
                id_torneo=self.request.GET['tournament']
            )
            if stage_tournament:
                query = Q(id_fase_torneo=stage_tournament[0])
            else:
                query = Q(id_fase_torneo=0)
        elif not self.request.GET.get('tournament') and self.request.GET.get('stage'):
            stage_tournament = StageTournament.objects.filter(id_fase=self.request.GET['stage'])
            for stage in stage_tournament:
                if query:
                    query.add(Q(id_fase_torneo=stage), Q.OR)
                else:
                    query = Q(id_fase_torneo=stage)
        elif self.request.GET.get('tournament') and not self.request.GET.get('stage'):
            stage_tournament = StageTournament.objects.filter(id_torneo=self.request.GET['tournament'])
            for stage in stage_tournament:
                if query:
                    query.add(Q(id_fase_torneo=stage), Q.OR)
                else:
                    query = Q(id_fase_torneo=stage)

        # Query builder execution if necessary
        if query:
            query.add(Q(id_fase_torneo__id_torneo__owner=self.request.user), Q.AND)
            matches = Match.objects.filter(
                query
            ).order_by('id_fase_torneo__id_torneo', 'id_fase_torneo__id_fase', '-fecha')
        else:
            matches = Match.objects.filter(
                id_fase_torneo__id_torneo__owner=self.request.user
            ).order_by('id_fase_torneo__id_torneo', 'id_fase_torneo__id_fase', '-fecha')

        return matches

    def get_context_data(self):
        ctx = super(MatchList, self).get_context_data()

        ctx['tournaments'] = Tournament.objects.filter(owner=self.request.user)
        ctx['stages'] = Stage.objects.all()

        return ctx


''' List of match that belongs to a tournament's stage '''
class MatchListSpecific(LoginRequiredMixin, ListView):
    template_name = 'admin/matches/match_list.html'
    model = Match
    paginate_by = 5

    def get_queryset(self):
        stage_tournament = StageTournament.objects.filter(id_fase=self.kwargs['pks'], id_torneo=self.kwargs['pkt'])
        matches = Match.objects.filter(id_fase_torneo=stage_tournament[0].id)\
            .order_by('id_fase_torneo__id_torneo', 'id_fase_torneo__id_fase', '-fecha')
        return matches

    def get_context_data(self):
        ctx = super(MatchListSpecific, self).get_context_data()
        ctx['specific'] = {'pkt': self.kwargs['pkt'], 'pks': self.kwargs['pks']}
        return ctx

    def get(self, request, pkt, pks):
        stage_tournament = StageTournament.objects.filter(id_fase=pks, id_torneo=pkt)
        clasified = Classified.objects.filter(id_fase_torneo=stage_tournament[0].id).first()

        if((stage_tournament[0].num_grupos) and (not clasified.grupo)):
            messages.error(request, 'Antes de gestionar partidos tiene que asociar los grupos de esta fase')
            return redirect('main:tournament_detail',  pk=pkt)

        return super(MatchListSpecific, self).get(request)


#Match list for the common users
def publicMatchList(request, pk_torneo):

    tournament = Tournament.objects.get(id=pk_torneo)
    stages = StageTournament.objects.filter(id_torneo=pk_torneo)
    matches = Match.objects.filter(id_fase_torneo__id_torneo=pk_torneo).order_by('id_fase_torneo__id_fase', 'fecha')
    participation = Participation.objects.filter(id_partido__id_fase_torneo__id_torneo=pk_torneo).order_by('id_partido')

    #Fases que tengan al menos un partido
    stage_with_match = Match.objects.filter(id_fase_torneo__id_torneo=pk_torneo).distinct('id_fase_torneo__id_fase')

    #Fase para la tabla clasificatoria
    try:
        stage_clasified_table = StageTournament.objects.get(id_torneo=pk_torneo, jerarquia=1)
    except StageTournament.DoesNotExist:
        stage_clasified_table = None

    context = {
        'tournament': tournament,
        'pk_tour': pk_torneo,
        'stages': stages,
        'match_list': matches,
        'participation': participation,
        'stage_with_match': stage_with_match,
        'stage_clasified_table': stage_clasified_table
    }
    return render(request, 'layouts/matches/public_matches.html', context)


class publicMatchListPDF(View):
    template_name = 'reports/tournament_matches.html'

    def get(self, request, pk_torneo):
        stages = StageTournament.objects.filter(id_torneo=pk_torneo)
        matches = Match.objects.filter(id_fase_torneo__id_torneo=pk_torneo).order_by('id_fase_torneo__id_fase','-fecha')
        participation = Participation.objects.filter(id_partido__id_fase_torneo__id_torneo=pk_torneo).order_by(
            'id_partido')

        # Fases que tengan al menos un partido
        stage_with_match = Match.objects.filter(id_fase_torneo__id_torneo=pk_torneo).distinct('id_fase_torneo__id_fase', 'fecha').order_by('-fecha')

        # Fase para la tabla clasificatoria
        try:
            stage_clasified_table = StageTournament.objects.get(id_torneo=pk_torneo, jerarquia=1)
        except StageTournament.DoesNotExist:
            stage_clasified_table = None

        template = get_template(self.template_name)

        tournament = Tournament.objects.get(id=pk_torneo)

        context = {
            'tournament': tournament,
            'pk_tour': pk_torneo,
            'stages': stages,
            'match_list': matches,
            'participation': participation,
            'stage_with_match': stage_with_match,
            'stage_clasified_table': stage_clasified_table
        }

        html = template.render(context)
        response = HttpResponse(content_type = 'application/pdf')
        #response['Content-Disposition'] = 'attachment; filename="report.pdf"'  # Code for direct download
        pisa_status = pisa.CreatePDF(html, dest=response)
        # if error then show some funny view
        if pisa_status.err:
            return HttpResponse('We had some errors <pre>' + html + '</pre>')
        return response


''' 
Render the detail view or redirect to the main page if user is not the owner

Shows the detail for a match
'''
@login_required
def matchInfo(request, pk):
    match = Match.objects.get(id=pk)
    if match.id_fase_torneo.id_torneo.owner == request.user:
        match_teams = Participation.objects.filter(id_partido=pk)

        context = {
            'match': match,
            'matchTeams': match_teams
        }

        return render(request, 'admin/matches/match_detail.html', context)
    return redirect('main:admin_index')

 

#Eliminar partido
@login_required
def deleteMatch(request, pk):
    match = Match.objects.get(id=pk)
    match.delete()
    return redirect(reverse_lazy('main:match_list'))


