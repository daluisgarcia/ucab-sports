from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from main.models import PreTeamRegister, PreTeam, PrePerson
from main.forms import TeamRegisterCreateForm


#Crear Torneo
class CreatePreinscription(CreateView):
    models = PreTeamRegister, PreTeam, PrePerson
    form_class = TeamRegisterCreateForm
    template_name = 'layouts/inscription/preinscription_form.html'
    success_url = reverse_lazy('main:preinscription_list')

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
        context['title'] = 'Solicitud de inscripción al torneo'
        context['botton_title'] = 'Solicitar inscripción'
        context['entity'] = 'PreTeamRegister'
        context['action'] = 'add'
        return context


#Lista de torneos
class PreinscriptionList(ListView):
    model = PreTeamRegister
    template_name = 'layouts/inscription/preinscription_list.html'

