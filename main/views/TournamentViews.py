from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.core.exceptions import ValidationError
from django.forms.formsets import formset_factory

from main.models import Post, Tournament, Stage, Game, StageTournament
from main.forms import TournamentCreateForm, StageTournamentCreateForm, BaseStageFormSet


#REVISAR
#Función para validar fechas de inicio y fin del torneo
def validar_fechas(fecha_inicio,fecha_fin):
    if(fecha_fin < fecha_inicio):
        raise ValidationError(_('La fecha de fin tiene que ser posterior a la fecha de inicio'))



#Crear Torneo
class CreateTournament(CreateView):
    model = Tournament
    form_class = TournamentCreateForm
    template_name = 'admin/tournaments/tournament_form.html'

    def post(self, request, *args, **kwargs):
        #print(request.POST)
        form = TournamentCreateForm(request.POST)
        
        """
        for key, value in request.POST.items():
            print("%s %s" % (key, value))
            if key == 'fecha_inicio':
                aux_fecha_inicio = value
            if key == 'fecha_fin':
                aux_fecha_fin = value
        """
        #Se validan las fechas
        #validar_fechas(aux_fecha_inicio,aux_fecha_fin)
        
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
        context['entity'] = 'Tournament'
        context['action'] = 'add'
        return context


#Asociar las fases al torneo
class CreateStageTournament(CreateView):
    model = StageTournament
    #Si no se pone este campo de fields, da error
    fields = '__all__'
    #El problema es que hay conflicto si se llaman más de dos clases es una misma Vista Basada en Clases
    #form_classes = StageTournamentCreateForm, BaseStageFormSet
    StageFormSet = formset_factory(StageTournamentCreateForm, formset=BaseStageFormSet)
    template_name = 'admin/tournaments/stage_tour_form.html'
    success_url = reverse_lazy('main:tournament_list')


    def post(self, request, pk):
        #print(request.POST)
        stage_formset = StageFormSet(request.POST)

        if stage_formset.is_valid():
            #Creamos array que contendrá todas las fases del torneo
            fases_tor = []

            for stage in stage_formset:
                jerarquia = stage.cleaned_data.get('jerarquia')
                fase = stage.cleaned_data.get('id_fase')

                if jerarquia and fase:
                    #Se agrega al array todos los elementos contenidos en el formset
                    fases_tor.append(StageTournament(id_fase=fase, id_torneo=pk, jerarquia=jerarquia))

            #bulk_create inserta el array en la tabla de las fases de los torneos
            StageTournament.objects.bulk_create(fases_tor)
        
        self.object = None
        context = self.get_context_data(**kwargs)    
        context['stage_formset'] = stage_formset
        return render(request, self.template_name, context)


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Asociar fases al torneo'
        context['botton_title'] = 'Asociar fases'
        context['entity'] = 'StageTournament'
        context['action'] = 'add'
        return context


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
