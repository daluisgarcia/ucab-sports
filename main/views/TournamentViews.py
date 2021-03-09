from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView, View
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required

from main.models import Post, Tournament, Stage, Game, Stage, StageTournament, Classified, Match, Participation
from main.forms import TournamentCreateForm, InitialStageTournamentForm


#Función que devuelve en un array la tabla de clasificatorias
def tabla_clasificatoria(stage_tournament, datos_tabla):

    clasificados = Classified.objects.filter(id_fase_torneo=stage_tournament).order_by('grupo')
    #Partidos de la fase del torneo
    matches = Match.objects.filter(id_fase_torneo=stage_tournament)

    #Lógica de la tabla de clasificatoria
    tabla_clasificatoria = []

    for team in clasificados:
        #Participaciones de ese equipo
        participacion = Participation.objects.filter(id_partido__in=matches, id_equipo=team.id_equipo)

        puntos_totales = 0
        puntos_ganados = 0
        puntos_empatados = 0
        partidos_jugados = 0
        partidos_empatados = 0
        partidos_ganados = 0
        partidos_perdidos = 0
        for p in participacion:
            #Si alguno de estos campos está lleno, entonces el partido sí ocurrió
            if((p.ganador != None) or (p.puntos_equipo != None) or (p.score != None)):
                #Se cuenta la participación
                partidos_jugados += 1
                #Si hay al menos un ganador, se cuenta la victoria
                if(p.ganador == True):
                    partidos_ganados += 1
                    #Sumamos los puntos del partido
                    if(p.puntos_equipo):
                        puntos_ganados += p.puntos_equipo
                #Verificamos si hay empate
                #Obtenemos el score actual y contamos si todos los otros equipos lo tienen igual
                elif(p.score != None):
                    cant_equipos = Participation.objects.filter(id_partido=p.id_partido).count()
                    cant_equipos_score = Participation.objects.filter(id_partido=p.id_partido, score=p.score).count()
                    #Si la cantidad de equipos = cantidad de equipos que tienen el mismo score, entonces sí hubo empate
                    if(cant_equipos == cant_equipos_score):
                        partidos_empatados += 1
                        #Sumamos los puntos del partido
                        if(p.puntos_equipo):
                            puntos_empatados += p.puntos_equipo
                    #Si no ganó, ni empató, entonces perdió
                    else:
                        partidos_perdidos += 1
                #Si no ganó, ni empató, entonces perdió
                else:
                    partidos_perdidos += 1

        #Suma de los puntos totales
        puntos_totales = (partidos_ganados * puntos_ganados) + (partidos_empatados * puntos_empatados)

        #Equipo
        datos_tabla['equipo'] = team

        #Partidos jugados
        datos_tabla['partidos_jugados'] = partidos_jugados

        #Partidos ganados
        datos_tabla['partidos_ganados'] = partidos_ganados

        #Partidos empatados
        datos_tabla['partidos_empatados'] = partidos_empatados

        #Partidos perdidos
        datos_tabla['partidos_perdidos'] = partidos_perdidos

        #Puntos totales
        datos_tabla['puntos_totales'] = puntos_totales

        tabla_clasificatoria.append(datos_tabla.copy())

    return tabla_clasificatoria


#Función que devuelve en un array los primeros equipos de cada grupo
def formar_grupos(tabla_clasif):
    grupos = []
    grupo = ''

    for clasif in tabla_clasif:
        if((grupo == '') or (grupo != clasif['equipo'].grupo)):
            grupos.append(clasif['equipo'])
        grupo = clasif['equipo'].grupo

    return grupos


''' Redirect to the tournament list or render the form

Create a tournament and assign the owner
'''
class CreateTournament(LoginRequiredMixin, CreateView):
    model = Tournament
    form_class = TournamentCreateForm
    template_name = 'admin/tournaments/tournament_form.html'

    def post(self, request):
        form = TournamentCreateForm(request.POST)
        initial_form = InitialStageTournamentForm(request.POST)

        self.object = None
        if form.is_valid() and initial_form.is_valid():
            #Validate if delegate is jd and participants are only 1
            if((form['tipo_delegado'].value() == 'd') and (int(initial_form['participantes_por_equipo'].value()) == 1)):
                messages.error(request, 'Si el torneo es de un único participante, entonces el tipo de delegado tiene que ser Jugador Delegado.')
                context = self.get_context_data()
                context['form'] = form
                return render(request, self.template_name, context)

            object = form.save(commit=False)
            object.owner = self.request.user
            object.save()
            tour = Tournament.objects.order_by('-id')[0].id

            #Se crea la fase inicial
            fase_inicial = StageTournament(
                id_fase=None,
                id_torneo=object,
                jerarquia=0,
                participantes_por_equipo=initial_form['participantes_por_equipo'].value(),
                equipos_por_partido=1
            )
            fase_inicial.save()
            messages.success(request, 'El torneo ha sido creado satisfactoriamente')
            return redirect('main:tournament_list')
        context = self.get_context_data()
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self):
        context = super().get_context_data()
        context['title'] = 'Creación del torneo'
        context['num_p_form'] = InitialStageTournamentForm(initial=None)
        context['botton_title'] = 'Crear torneo'
        context['action'] = 'add'
        return context


#Teams 
@login_required
def teamsTournament(request, pk_torneo, pk_fase):
    tournament = Tournament.objects.get(id=pk_torneo)
    stage = Stage.objects.get(id=pk_fase)
    clasified = Classified.objects.filter(id_fase_torneo__id_torneo=tournament,id_fase_torneo__id_fase=stage).order_by('grupo')

    context = {
        'tournament': tournament,
        'stage': stage,
        'clasified': clasified
    }
    return render(request, 'admin/tournaments/tournament_teams.html', context)


#Asociar las fases al torneo (mediante un método)
@login_required
def createStageTournament(request, pk):
    # Obtenemos el torneo y se instancia el formset al torneo
    tournament = Tournament.objects.get(id=pk)

    if not tournament.inscripcion_abierta:
        redirect(reverse_lazy('main:tournament_list'))

    #Se define formset de la fase
    StageFormSet = inlineformset_factory(
        Tournament,
        StageTournament,
        fields=('id_fase','participantes_por_equipo','equipos_por_partido','num_grupos','equipos_por_grupo'),
        extra=1
    )

    formset = StageFormSet(queryset=StageTournament.objects.none(), instance=tournament)

    if request.method == 'POST':
        formset = StageFormSet(request.POST, instance=tournament)

        if formset.is_valid():
            jerarquia = 1
            # Creamos las jerarquías en el orden en como llegan las fases en el formset
            for form in formset:
                stage = Stage.objects.get(id=form['id_fase'].value())

                stage_tournament = StageTournament(
                    id_fase=stage, id_torneo=tournament, jerarquia=jerarquia,
                    participantes_por_equipo=form['participantes_por_equipo'].value(),
                    equipos_por_partido=form['equipos_por_partido'].value() if form['equipos_por_partido'].value() else None,
                    num_grupos=form['num_grupos'].value() if form['num_grupos'].value() else None,
                    equipos_por_grupo=form['equipos_por_grupo'].value() if form['equipos_por_grupo'].value() else None
                )
                stage_tournament.save()

                if(jerarquia == 1):
                    stage_1 = StageTournament.objects.get(id_torneo=tournament, jerarquia=jerarquia)

                jerarquia = jerarquia + 1

            #Pasamos a los participantes de la fase con jerarquía 0 a la fase con jerarquía 1
            stage_tour_0 = StageTournament.objects.get(id_torneo=tournament, jerarquia=0)
            teams = Classified.objects.filter(id_fase_torneo=stage_tour_0)
            
            for team in teams:
                clasificado = Classified(id_fase_torneo=stage_1, id_equipo=team.id_equipo)
                clasificado.save()

            #Por último, se elimina la jerarquía 0 de
            stage_tour_0.delete()

            messages.success(request, 'El torneo ha sido creado satisfactoriamente')

            # Se cierra la inscripcion
            tournament.inscripcion_abierta = False
            tournament.save()

            return redirect(reverse_lazy('main:tournament_list'))
        
    context = {
        'stage_formset': formset, 
        'title': 'Asociar fases al torneo', 
        'botton_title': 'Asociar fases',
        'pk': pk
    }
    return render(request, 'admin/tournaments/stage_tour_form.html', context)


''' Render the list view

Shows the tournament list to the owner
'''
class TournamentList(LoginRequiredMixin, ListView):
    model = Tournament
    template_name = 'admin/tournaments/tournament_list.html'
    paginate_by = 5

    def get_queryset(self):
        # Validates some parameters from request to filter if necessary
        if self.request.GET.get('name') and self.request.GET.get('game'):
            return self.model.objects.filter(
                owner=self.request.user,
                nombre__contains = self.request.GET['name'],
                id_juego = self.request.GET['game']
            ).order_by('fecha_inicio')

        elif not self.request.GET.get('name') and self.request.GET.get('game'):
            return self.model.objects.filter(
                owner=self.request.user,
                id_juego=self.request.GET['game']
            ).order_by('fecha_inicio')

        elif self.request.GET.get('name') and not self.request.GET.get('game'):
            return self.model.objects.filter(
                owner=self.request.user,
                nombre__contains=self.request.GET['name']
            ).order_by('fecha_inicio')

        return self.model.objects.filter(owner=self.request.user).order_by('fecha_inicio')

    def get_context_data(self):
        context = super(TournamentList, self).get_context_data()
        context['title'] = 'Torneos'
        context['games'] = Game.objects.all()
        return context


'''
Shows all the tournaments to the common user
'''
class PublicTournamentList(ListView):
    model = Tournament
    template_name = 'layouts/tournaments/public_tournaments_list.html'

    def get(self, request, tipo):
        self.object_list = self.model.objects.order_by('-inscripcion_abierta')
        context = self.get_context_data()
        context['tipo'] = tipo
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Torneos'
        return context


''' 
Render the detail view or redirect to the main page if user is not the owner

Shows the detail for a tournament
'''
def tournamentInfo(request, pk):
    tournament = Tournament.objects.get(id=pk)
    if tournament.owner == request.user:
        #Fases del torneo
        tourStage = StageTournament.objects.filter(id_torneo=pk, id_fase__isnull=False)
        
        if(tournament.inscripcion_abierta == False):
            #Verificar en cuál fase están actualmente los clasificados
            i = 1
            anterior_fase = None
            while (True):
                try:
                    fase = StageTournament.objects.filter(id_torneo=pk, jerarquia=i)
                except StageTournament.DoesNotExist:
                    fase = None
            
                if(fase):
                    clasificados = Classified.objects.filter(id_fase_torneo__in=fase)
                else:
                    break

                if(clasificados):
                    anterior_fase = fase
                else:
                    break
                    
                i = i + 1
            if(not anterior_fase):
                id_fase_clasificados = None
                fase_clasificados = None
                fase_torneo = None
            else:
                id_fase_clasificados = anterior_fase.first().id_fase.id
                fase_clasificados = anterior_fase.first().id_fase
                fase_torneo = anterior_fase
        else:
            id_fase_clasificados = None
            fase_clasificados = None
            fase_torneo = None

        #Verificar que exista una siguiente fase
        if(not fase_torneo):
            next_stage = None
        else:
            try:
                next_stage = StageTournament.objects.get(id_torneo=tournament, jerarquia=fase_torneo[0].jerarquia + 1)
            except StageTournament.DoesNotExist:
                next_stage = None


        context = {
            'tournament': tournament, 
            'tourStage': tourStage,
            'fase_clasificatoria': fase_clasificados,
            'id_fase_clasif': id_fase_clasificados,
            'next_stage': next_stage
        }

        return render(request, 'admin/tournaments/tournament_detail.html', context)
    return redirect('main:admin_index')


#Editar Torneo
class UpdateTournament(LoginRequiredMixin, UpdateView):
    model = Tournament
    form_class = TournamentCreateForm
    template_name = 'admin/tournaments/tournament_form.html'

    def get(self, request, pk):
        tournament = get_object_or_404(self.model, pk=pk)
        if tournament.owner == request.user:
            form = TournamentCreateForm(instance=tournament)
            self.object = None
            ctx = self.get_context_data()
            ctx['form'] = form
            stage_tournament = StageTournament.objects.filter(
                id_torneo=tournament,
                jerarquia=0
            ).first()
            if stage_tournament:
                ctx['num_p_form'] = InitialStageTournamentForm(instance=stage_tournament)
            return render(request, self.template_name, ctx)
        return redirect('main:admin_index')

    def post(self, request, pk):
        tournament = get_object_or_404(self.model, pk=pk)
        if tournament.owner != request.user:
            return redirect('main:admin_index')
        form = TournamentCreateForm(request.POST, instance=tournament)
        stage_tournament = StageTournament.objects.filter(
            id_torneo=tournament,
            jerarquia=0
        ).first()
        stage_form = None
        if stage_tournament:
            stage_form = InitialStageTournamentForm(request.POST, instance=stage_tournament)
        if not form.is_valid() or (stage_form and not stage_form.is_valid()):
            ctx = {
                'form': form,
                'title': 'Edición del torneo',
                'botton_title': 'Editar torneo',
                'num_p_form': stage_form
            }
            return render(request, self.template_name, ctx)
        form.save()
        if stage_form:
            stage_form.save()
        self.object = None
        
        #Si la inscripción todavía sigue abierta entonces no se pueden modificar las fases del torneo
        if(tournament.inscripcion_abierta):
            messages.success(request, 'El torneo ha sido modificado satisfactoriamente')
            return redirect('main:tournament_list')
        else:
            return redirect('main:edit_stage_tournament',  pk=pk)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición del torneo'
        context['action'] = 'edit'
        context['botton_title'] = 'Editar torneo'
        return context


''' Update the relation between Stages and Tournament '''
class UpdateStageTournament(LoginRequiredMixin, View):
    template_name = 'admin/tournaments/stage_tour_form.html'
    refuse_url = reverse_lazy('main:tournament_list')

    def get(self, request, pk):
        tournament = get_object_or_404(Tournament, id=pk)
        # if not tournament.inscripcion_abierta:
        #     redirect(self.refuse_url)

        try:
            stagesTourn = StageTournament.objects.filter(id_torneo=pk).order_by('jerarquia')
        except StageTournament.DoesNotExist:
            raise Http404("No StageTournament matches the given query.")

        context = {
            'stageTournNum': len(stagesTourn),
            'stagesTourn': stagesTourn,
            'stages': Stage.objects.all(),
            'title': 'Editar fases del torneo '+tournament.nombre,
            'botton_title': 'Editar fases',
            'pk': pk
        }
        return render(request, self.template_name, context)

    def splitDictionay(self, dict, id):
        d = []
        d.append(dict.pop('stage-select-' + id))
        d.append(dict.pop('stage-part-' + id))
        d.append(dict.pop('stage-part-match-' + id))
        d.append(dict.pop('stage-num-groups-' + id))
        d.append(dict.pop('stage-team-group-' + id))
        return d

    def post(self, request, pk):
        tournament = get_object_or_404(Tournament, id=pk)
        # if not tournament.inscripcion_abierta:
        #     redirect(self.refuse_url)

        items = {key: value for key, value in request.POST.items() if 'stage-' in key.lower()}
        hierarchy = 0
        keys = list(items.keys())
        while (len(keys) > 0):
            hierarchy += 1

            cont = 2
            id = keys[0][-cont:]   # Gets two last chars
            while True: # Validates if the number on str is lower than 10 and avoid after str errors
                if id[:1] == '-':
                    id = id[2:]
                    break
                cont += 1
                id = keys[0][-cont:]   # Gets two last chars

            if (id == 'NN'):    # Flag to create a new Stage-Tournament
                # Crear nueva Fase-Torneo (Evaluar antepenultimo numero)
                data_number = keys[0][-4:-2]
                if data_number[:1] == '-':  # The number is lower than 10
                    data_number = keys[0][-3:-2]

                data_number = data_number+'NN'
                data = self.splitDictionay(items, data_number)
                keys = list(items.keys())

                stageT = StageTournament(
                    id_fase = get_object_or_404(Stage, pk = int(data[0])),
                    id_torneo = tournament,
                    participantes_por_equipo = int(data[1]),
                    equipos_por_partido=int(data[2]),
                    num_grupos=int(data[3]) if data[3] else None,
                    equipos_por_grupo=int(data[4]) if data[4] else None,
                    jerarquia=hierarchy
                )
                stageT.save()


                continue

            stageT = get_object_or_404(StageTournament, pk = int(id))

            data = self.splitDictionay(items, '0'+id)
            keys = list(items.keys())

            stageT.id_fase = get_object_or_404(Stage, pk = int(data[0]))
            stageT.participantes_por_equipo = int(data[1])
            stageT.equipos_por_partido = int(data[2])
            stageT.num_grupos = int(data[3]) if data[3] else None
            stageT.equipos_por_grupo = int(data[4]) if data[4] else None
            stageT.jerarquia = hierarchy
            stageT.save()

        messages.success(request, 'Se ha modificado el torneo satisfactoriamente')
        return redirect(reverse_lazy('main:tournament_list'))


@login_required
def deleteStageTournament(request, id):
    stage = get_object_or_404(StageTournament, pk=id)
    stage.delete()
    return HttpResponse(status=200)


#Eliminar torneo
class DeleteTournament(LoginRequiredMixin, DeleteView):
    model = Tournament
    success_url = reverse_lazy('main:tournament_list')
    template_name = 'admin/tournaments/tournament_confirm_delete.html'


@login_required
def deleteTournament(request, pk):
    tournament = Tournament.objects.get(id=pk)
    tournament.delete()
    return redirect(reverse_lazy('main:tournament_list'))


#Tabla de clasificatoria
def clasificatorias(request, pk_torneo, pk_fase):
    tournament = Tournament.objects.get(id=pk_torneo)
    stage = Stage.objects.get(id=pk_fase)
    stage_tour = StageTournament.objects.get(id_torneo=pk_torneo, id_fase=pk_fase)

    #Siguiente fase
    next_stage = StageTournament.objects.get(id_torneo=pk_torneo, jerarquia=stage_tour.jerarquia + 1)
    
    datos_tabla = {
        'equipo': None,
        'puntos_totales': None,
        'partidos_jugados': None,
        'partidos_ganados': None,
        'partidos_perdidos': None,
        'partidos_empatados': None,
        'valor': None
    }

    tabla_clasif = tabla_clasificatoria(stage_tour, datos_tabla)
    
    i = 0
    for part in tabla_clasif:
        part['valor'] = i
        i = i + 1

    if request.method == 'POST':
        
        i = 0
        for equipo in tabla_clasif:
            num_equipo = 'equipo-' + str(i)
            i = i + 1
            team = request.POST.get(num_equipo, None)
            if(team):

                nuevo_clasificado = Classified(
                    id_equipo = equipo['equipo'].id_equipo,
                    id_fase_torneo = next_stage
                )
                nuevo_clasificado.save()

        messages.success(request, 'Los equipos han avanzado a la siguiente fase')
        return redirect('main:tournament_detail', pk=tournament.id)


    context = {
        'torneo': tournament,
        'fase': stage,
        'tabla_clasificatoria': tabla_clasif
    }

    return render(request, 'admin/tournaments/clasificatorias.html', context)


#Vista pública de la tabla de clasificatoria
def publicClasified(request, pk_fase_torneo):
    stage_tour = StageTournament.objects.get(id=pk_fase_torneo)

    datos_tabla = {
        'equipo': None,
        'puntos_totales': None,
        'partidos_jugados': None,
        'partidos_ganados': None,
        'partidos_perdidos': None,
        'partidos_empatados': None
    }

    tabla_clasif = tabla_clasificatoria(stage_tour, datos_tabla)

    #Ordenar tabla clasificatoria
    #criterio = range(25)
    #print(list(criterio))
    #tabla_clasif.sort(key = lambda x: criterio.index(x['puntos_totales']))

    #Si existen grupos, guardar posiciones del primer equipo de cada grupo
    if(tabla_clasif[0]['equipo'].grupo):
        grupos = formar_grupos(tabla_clasif)
        print(grupos)
    else:
        grupos = None

    context = {
        'torneo': stage_tour.id_torneo.nombre,
        'fase': stage_tour.id_fase.nombre,
        'tabla_clasificatoria': tabla_clasif,
        'id_torneo': stage_tour.id_torneo.id,
        'grupos': grupos
    }

    return render(request, 'layouts/tournaments/public_clasified.html', context)

