from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from main.models import Post, Tournament, Stage, Game
from main.forms import PostCreateForm, TorneoCreateForm

#Detalle del torneo
class TorneoDetail(ListView):
    template_name = 'admin/torneos/torneos.html'

    """
    def __init__(self, *args, **kwargs):
        id = kwargs.pop('pk')
        model = Posts.objects.get(id = id)
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalle del Torneo'
        context['list_url'] = reverse_lazy('main:torneos_list')
        context['entity'] = 'Torneos'
        return context



#Lista de torneos
class TorneosList(ListView):
    model = Tournament
    template_name = 'admin/torneos/torneos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de Torneos'
        context['create_url'] = reverse_lazy('main:CreateTorneo')
        context['list_url'] = reverse_lazy('main:torneos_list')
        context['entity'] = 'Torneos'
        return context



#Crear Torneo
class CreateTorneo(CreateView):
    model = Tournament
    form_class = TorneoCreateForm
    template_name = 'admin/torneos/create_torneo.html'
    success_url = reverse_lazy('main:torneos_list')

    def post(self, request, *args, **kwargs):
        #print(request.POST)
        form = TorneoCreateForm(request.POST)
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
        context['list_url'] = reverse_lazy('main:torneos_list')
        context['entity'] = 'Torneos'
        return context



#Editar Torneo
class UpdateTorneo(UpdateView):
    model = Tournament
    form_class = TorneoCreateForm
    template_name = 'admin/torneos/create_torneo.html'
    success_url = reverse_lazy('main:torneos_list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición del torneo'
        context['botton_title'] = 'Editar torneo'
        context['list_url'] = reverse_lazy('main:torneos_list')
        context['entity'] = 'Torneos'
        return context
