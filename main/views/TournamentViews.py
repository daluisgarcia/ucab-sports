from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from main.models import Post, Tournament, Stage, Game, Stage, StageTournament, Classified
from main.forms import TournamentCreateForm, StageTournamentCreateForm, InitialStageTournamentForm


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


#Asociar las fases al torneo (mediante un método)
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

    def get(self, request):
        if request.user.is_authenticated:
            self.object_list = self.model.objects.filter(owner=request.user)
            context = self.get_context_data()
            return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Torneos'
        return context


'''
Shows all the tournaments to the common user
'''
class PublicTournamentList(ListView):
    model = Tournament
    template_name = 'layouts/tournaments/public_tournaments_list.html'


''' Render the detail view or redirect to the main page if user is not the owner

Shows the detail for a tournament
'''
class TournamentDetail(LoginRequiredMixin, DetailView):
    model = Tournament
    template_name = 'admin/tournaments/tournament_detail.html'

    def get(self, request, pk):
        tournament = get_object_or_404(self.model, pk=pk)
        if tournament.owner == request.user:
            return super(TournamentDetail, self).get(request, pk)
        return redirect('main:admin_index')

def tournamentInfo(request, pk):
    tournament = Tournament.objects.get(id=pk)
    if tournament.owner == request.user:
        tourStage = StageTournament.objects.filter(id_torneo=pk, id_fase__isnull=False)
        return render(request, 'admin/tournaments/tournament_detail.html',
                      {'tournament': tournament, 'tourStage': tourStage})
    return redirect('main:admin_index')

class TournamentBracket(ListView):
    model = Tournament
    template_name = 'layouts/tournaments/tournament_bracket.html'



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
            return render(request, self.template_name, ctx)
        return redirect('main:admin_index')

    def post(self, request, pk):
        tournament = get_object_or_404(self.model, pk=pk)
        if tournament.owner != request.user:
            return redirect('main:admin_index')
        form = TournamentCreateForm(request.POST, instance=tournament)
        if not form.is_valid():
            ctx = {'form': form, 'title': 'Edición del torneo', 'botton_title': 'Editar torneo'}
            return render(request, self.template_name, ctx)
        form.save()
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


#Editar las fases del torneo

def editStageTournament(request, pk):
    #Traemos las fases del torneo
    cantidad_fases = StageTournament.objects.filter(id_torneo=pk, id_fase__isnull=False).count()
    #Cantidad de filas que tendrá el formset
    if(cantidad_fases == 0):
        filas = 1
    else:
        filas = cantidad_fases

    #Se define formset de la fase
    StageFormSet = inlineformset_factory(
        Tournament,
        StageTournament,
        fields=('id_fase','participantes_por_equipo','equipos_por_partido','num_grupos','equipos_por_grupo'),
        extra=0
    )

    #Obtenemos el torneo y se instancia el formset al torneo
    tournament = Tournament.objects.get(id=pk)

    if(cantidad_fases == 0):
        formset = StageFormSet(queryset=StageTournament.objects.none(), instance=tournament)
    else:
        formset = StageFormSet(queryset=StageTournament.objects.filter(id_torneo=pk, id_fase__isnull=False), instance=tournament)

    if request.method == 'POST':
        formset = StageFormSet(request.POST, instance=tournament)
        #print(request.POST)
        if formset.is_valid():
            #Creamos las jerarquías en el orden en como llegan las fases en el formset
            jerarquia = 1
            for form in formset:
                stage = Stage.objects.get(id=form['id_fase'].value())

                if(not form['num_grupos'].value()):
                    num_grupos = None
                else:
                    num_grupos = form['num_grupos'].value()

                if(not form['equipos_por_grupo'].value()):
                    eq_grupo = None
                else:
                    eq_grupo = form['equipos_por_grupo'].value()

                stage_tournament = StageTournament(
                    id_fase=stage,
                    id_torneo=tournament,
                    jerarquia=jerarquia,
                    participantes_por_equipo=form['participantes_por_equipo'].value(),
                    equipos_por_partido=form['equipos_por_partido'].value(),
                    num_grupos=num_grupos,
                    equipos_por_grupo=eq_grupo
                )
                
                stage_tournament.save()
                
                jerarquia = jerarquia + 1

            messages.success(request, 'El torneo ha sido modificado satisfactoriamente')
            return redirect(reverse_lazy('main:tournament_list'))
        
    context = {
        'stage_formset': formset, 
        'title': 'Asociar fases al torneo', 
        'botton_title': 'Asociar fases',
        'pk': pk
    }
    return render(request, 'admin/tournaments/stage_tour_form.html', context)



#Eliminar torneo
class DeleteTournament(LoginRequiredMixin, DeleteView):
    model = Tournament
    success_url = reverse_lazy('main:tournament_list')
    template_name = 'admin/tournaments/tournament_confirm_delete.html'


def deleteTournament(request, pk):
    print(pk)
    tournament = Tournament.objects.get(id=pk)
    tournament.delete()
    print('Torneo eliminado')
    return redirect(reverse_lazy('main:tournament_list'))