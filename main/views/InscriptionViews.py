from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView
from main.models import PreTeamRegister, PreTeam, PrePerson, StageTournament, Tournament
from django.forms import formset_factory
from main.forms import TeamRegisterCreateForm, PreteamCreateForm



#Inscribir equipo
class CreatePreteam(CreateView):
    model = PreTeam
    form_class = PreteamCreateForm
    template_name = 'layouts/inscription/preinsc_team_form.html'

    def post(self, request, pk_torneo):
        form = PreteamCreateForm(request.POST)
        if form.is_valid():
            form.save()
            #Obtenemos el id último registro del equipo
            pk_preteam = PreTeam.objects.order_by('-id')[0].id
            return redirect('main:create_preperson', pk_torneo, pk_preteam)

        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Crea tu equipo'
        context['botton_title'] = 'Crear equipo'
        context['action'] = 'add'
        return context


#Asociar las fases al torneo (mediante un método)
def createPreperson(request, pk_torneo, pk_preteam):
    #Verificamos cuántas personas debe conformar el equipo, esto se hace viendo la fase del torneo que tenga jerarquía = 1
    person_number = StageTournament.objects.get(jerarquia=1, id_torneo=pk_torneo).id_fase.part_por_equipo
    #print(person_number)

    #Obtenemos el torneo
    tournament = Tournament.objects.get(id=pk_torneo)

    InscriptionFormSet = formset_factory(PrePerson, extra=person_number)

    formset = InscriptionFormSet(queryset=PrePerson.objects.none(), instance=tournament)

    if request.method == 'POST':
        formset = InscriptionFormSet(request.POST, instance=tournament)
        if formset.is_valid():
            formset.save()
            messages.success(request, 'La solicitud al torneo ha sido enviada satisfactoriamente')
            return redirect('/posts/')
        messages.error(request, 'Debe llenar todos los campos de los participantes (menos el nickname)')

    context = {'insc_formset': formset, 'title': 'Ingresa a los participantes', 'botton_title': 'Solicitar inscripción'}
    return render(request, 'layouts/inscription/preinsc_persons_form.html', context)


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


#Lista de inscripciones
class PreinscriptionList(ListView):
    model = PreTeamRegister
    template_name = 'layouts/inscription/preinscription_list.html'

