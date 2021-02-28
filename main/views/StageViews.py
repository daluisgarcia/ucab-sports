from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
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
@login_required
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

    def numberToLetter(self, number):
        if (number < 1 or number > 26):
            return None
        abc = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
        return abc[number-1]

    def get(self, request, pkt, hierarchy):
        try:
            stageTourn = StageTournament.objects.get(id_torneo=pkt, jerarquia=hierarchy)
        except StageTournament.DoesNotExist:
            raise Http404("No StageTournament matches the given query.")

        if stageTourn.num_grupos == None or stageTourn.num_grupos < 1:
            messages.error(request, 'Esta fase no es por grupos.')
            return redirect(self.success_url, pk=pkt)

        # Array of possible groups
        groups = {}
        for i in range(1, stageTourn.num_grupos+1):
            groups[self.numberToLetter(i)] = {}
            for j in range(1, stageTourn.equipos_por_grupo+1):
                groups[self.numberToLetter(i)][j] = 'grupo-'+self.numberToLetter(i)+'-equipo'+str(j)

        # Getting the teams of the tournament
        classified = Classified.objects.filter(id_fase_torneo=stageTourn.id)

        groups_assigned = {}

        for c in classified:
            if (c.grupo):
                if c.grupo in groups_assigned.keys():
                    groups_assigned[c.grupo][c.id_equipo.id] = True
                else:
                    groups_assigned[c.grupo] = {}
                    groups_assigned[c.grupo][c.id_equipo.id] = True

        str_groups = ''
        if groups_assigned:
            # Creacion de codigo HTML de los selects, iterar sobre los equipos y grupos antes definidos para poder adaptarse a cualquier cambio
            for letter, group in groups.items():
                str_groups = str_groups + '<h4>Grupo '+letter+'</h4>'
                print(group)
                for key, value in group.items():
                    str_groups = str_groups + '<div class="row ml-4">'
                    str_groups = str_groups + ' <div class="form-group-inline">'
                    str_groups = str_groups + '<label>Equipo '+str(key)+'</label>'
                    str_groups = str_groups + '<select class="custom-control-inline" name="'+str(value)+'">'
                    already_added = False
                    for team in classified:
                        if (letter in groups_assigned.keys()) and (team.id_equipo.id in groups_assigned[letter].keys()) and not already_added:
                            str_groups = str_groups + '<option value = "' + str(team.id_equipo.id) + '" selected >' + team.id_equipo.nombre + ' </option>'
                            groups_assigned[letter].pop(team.id_equipo.id)

                            already_added = True

                            if (len(groups_assigned[letter]) == 0):
                                groups_assigned.pop(letter)
                        else:
                            str_groups = str_groups + '<option value = "'+str(team.id_equipo.id)+'" >'+team.id_equipo.nombre+' </option>'
                    str_groups = str_groups + '</select>'
                    str_groups = str_groups + '</div>'
                    str_groups = str_groups + '</div>'

        # Context data
        ctx = {}
        ctx['groups'] = groups
        ctx['classified'] = classified
        ctx['str_groups'] = str_groups

        return render(request, self.template_name, ctx)

    def post(self, request, pkt, hierarchy):

        try:
            stageTourn = StageTournament.objects.get(id_torneo=pkt, jerarquia=hierarchy)
        except StageTournament.DoesNotExist:
            raise Http404("No StageTournament matches the given query.")

        # Iterate over the selects input of the request searching for a certain group number and assigning it
        for i in range(1, stageTourn.num_grupos+1):
            teams = [value for key, value in request.POST.items() if 'grupo-'+self.numberToLetter(i) in key]
            for team in teams:
                classified = Classified.objects.get(id_fase_torneo=stageTourn.id, id_equipo=team)
                classified.grupo = self.numberToLetter(i)
                classified.save()

        messages.success(request, 'Los grupos han sido formados satisfactoriamente.')
        return redirect(self.success_url, pk=pkt)
