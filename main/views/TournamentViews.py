from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.forms import inlineformset_factory
from django.contrib import messages

from main.models import Post, Tournament, Stage, Game, StageTournament
from main.forms import TournamentCreateForm, StageTournamentCreateForm




#Crear Torneo
class CreateTournament(CreateView):
    model = Tournament
    form_class = TournamentCreateForm
    template_name = 'admin/tournaments/tournament_form.html'

    def post(self, request, *args, **kwargs):
        #print(request.POST)
        form = TournamentCreateForm(request.POST)
        
        if form.is_valid():
            form.save()
            #Obtenemos el id último registro del torneo (el que se acaba de insertar)
            c = Tournament.objects.order_by('-id')[0].id
            print(c)
            return redirect('main:create_stage_tournament', pk=c)
            
        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación del torneo'
        context['botton_title'] = 'Crear torneo'
        context['action'] = 'add'
        return context


#Asociar las fases al torneo (mediante un método)
def createStageTournament(request, pk):
    #Se define formset de la fase
    StageFormSet = inlineformset_factory(Tournament, StageTournament, fields=('id_fase','jerarquia'), extra=7)
    #Obtenemos el torneo
    tournament = Tournament.objects.get(id=pk)
    formset = StageFormSet(queryset=StageTournament.objects.none(), instance=tournament)
    if request.method == 'POST':
        formset = StageFormSet(request.POST, instance=tournament)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'El torneo ha sido creado satisfactoriamente')
            return redirect('/torneos/')
        messages.error(request, 'Cada fase debe llevar su correspondiente jerarquía')
    #Daniel, no me pegues por hacer este context así c:
    context = {'stage_formset': formset, 'title': 'Asociar fases al torneo', 'botton_title': 'Asociar fases'}
    return render(request, 'admin/tournaments/stage_tour_form.html', context)


#Lista de torneos
class TournamentList(ListView):
    model = Tournament
    template_name = 'admin/tournaments/tournament_list.html'


#Detalle del torneo
class TournamentDetail(DetailView):
    model = Tournament
    template_name = 'admin/tournaments/tournament_detail.html'


#Editar Torneo
class UpdateTournament(UpdateView):
    model = Tournament
    form_class = TournamentCreateForm
    template_name = 'admin/tournaments/tournament_form.html'
    success_url = reverse_lazy('main:tournament_list')

    def post(self, request, pk):
        make = get_object_or_404(self.model, pk=pk)
        form = TournamentCreateForm(request.POST, instance=make)
        if not form.is_valid():
            ctx = {'form': form, 'title': 'Edición del torneo', 'botton_title': 'Editar torneo'}
            return render(request, self.template_name, ctx)
        form.save()
        self.object = None
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición del torneo'
        context['botton_title'] = 'Editar torneo'
        return context


#Eliminar torneo
class DeleteTournament(DeleteView):
    model = Tournament
    success_url = reverse_lazy('main:tournament_list')
    template_name = 'admin/tournaments/tournament_confirm_delete.html'
