from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from main.models import Post, Tournament, Stage, Game
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
class DeleteStage(LoginRequiredMixin, DeleteView):
    model = Stage
    success_url = reverse_lazy('main:stage_list')
    template_name = 'admin/stages/stage_confirm_delete.html'