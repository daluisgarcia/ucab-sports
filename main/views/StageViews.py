from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages

from main.models import Stage, Tournament, Classified, StageTournament
from main.forms import StageCreateForm


#Crear fase
class CreateStage(LoginRequiredMixin, CreateView):
    model = Stage
    form_class = StageCreateForm
    template_name = 'admin/stages/stage_form.html'
    success_url = reverse_lazy('main:stage_list')

    def post(self, request, *args, **kwargs):
        # print(request.POST)
        form = StageCreateForm(request.POST)
        if form.is_valid():
            form.save()
            if 'next' in request.POST:
                return redirect(request.POST['next'])
            return HttpResponseRedirect(self.success_url)
        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de la fase'
        context['botton_title'] = 'Crear fase'
        return context


#Lista de fases
class StageList(LoginRequiredMixin, ListView):
    model = Stage
    template_name = 'admin/stages/stage_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Fases'
        return context


#Detalle de fase
class StageDetail(LoginRequiredMixin, DetailView):
    model = Stage
    template_name = 'admin/stages/stage_detail.html'


#Actualizar fase
class UpdateStage(LoginRequiredMixin, UpdateView):
    model = Stage
    template_name = 'admin/stages/stage_form.html'
    success_url = reverse_lazy('main:stage_list')

    def get(self, request, pk):
        stage = get_object_or_404(self.model, pk=pk)
        form = StageCreateForm(instance=stage)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk):
        stage = get_object_or_404(self.model, pk=pk)
        form = StageCreateForm(request.POST, instance=stage)
        if not form.is_valid():
            ctx = {'form': form, 'title': 'Edición de la fase', 'botton_title': 'Editar fase'}
            return render(request, self.template_name, ctx)
        form.save()
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Fases'
        context['botton_title'] = 'Editar fase'
        context['action'] = 'edit'
        return context


#Eliminar fase
def deleteStage(request, pk):
    stage = Stage.objects.get(id=pk)
    stage.delete()
    print('Fase eliminada')
    messages.success(request, 'La fase se ha eliminado satisfactoriamente')
    return redirect(reverse_lazy('main:stage_list'))


'''
    Assign groups to teams on a stage
'''
class StageGroups(LoginRequiredMixin, View):
    template_name = 'admin/stages/stages_groups.html'
    success_url = 'main:tournament_detail'

    def get(self, request, pkt, pks):
        try:
            stageTourn = StageTournament.objects.get(id_fase=pks, id_torneo=pkt)
        except StageTournament.DoesNotExist:
            raise Http404("No StageTournament matches the given query.")

        if stageTourn.num_grupos == None or stageTourn.num_grupos <= 1:
            return redirect(self.success_url, pk=pkt)

        # Array of possible groups
        groups = {}
        for i in range(1, stageTourn.num_grupos+1):
            groups[i] = {}
            for j in range(1, stageTourn.equipos_por_grupo+1):
                groups[i][j] = 'grupo-'+str(i)+'-equipo'+str(j)

        # Getting the teams of the tournament
        classified = Classified.objects.filter(id_fase_torneo=stageTourn.id)

        # Context data
        ctx = {}
        ctx['groups'] = groups
        ctx['classified'] = classified

        return render(request, self.template_name, ctx)

    def post(self, request, pkt, pks):

        try:
            stageTourn = StageTournament.objects.get(id_fase=pks, id_torneo=pkt)
        except StageTournament.DoesNotExist:
            raise Http404("No StageTournament matches the given query.")

        # Iterate over the selects input of the request searching for a certain group number and assigning it
        for i in range(1, stageTourn.num_grupos+1):
            print('GRUPO-' + str(i))
            teams = [value for key, value in request.POST.items() if 'grupo-'+str(i) in key.lower()]
            for team in teams:
                classified = Classified.objects.get(id_fase_torneo=stageTourn.id, id_equipo=team)
                classified.grupo = i
                classified.save()

        return redirect(self.success_url, pk=pkt)
