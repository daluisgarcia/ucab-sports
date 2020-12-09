from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from main.models import Post, Tournament, Stage, Game
from main.forms import TournamentCreateForm



#Crear Torneo
class CreateTournament(CreateView):
    model = Tournament
    form_class = TournamentCreateForm
    template_name = 'admin/tournaments/tournament_form.html'
    success_url = reverse_lazy('main:tournament_list')

    def post(self, request, *args, **kwargs):
        #print(request.POST)
        form = TournamentCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación del torneo'
        context['botton_title'] = 'Crear torneo'
        context['entity'] = 'Tournament'
        context['action'] = 'add'
        return context


#Lista de torneos
class TournamentList(ListView):
    model = Tournament
    template_name = 'admin/tournaments/tournament_list.html'


#REVISAR
#No se logran ver los detalles de los torneos :(
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
            ctx = {'form': form}
            return render(request, self.template_name, ctx)
        form.save()
        self.object = None
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición del torneo'
        context['botton_title'] = 'Editar torneo'
        context['entity'] = 'Tournament'
        return context


#Eliminar torneo
class DeleteTournament(DeleteView):
    model = Tournament
    success_url = reverse_lazy('main:tournament_list')
    template_name = 'admin/tournaments/tournament_confirm_delete.html'
