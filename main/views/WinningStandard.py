from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin

from main.models import WinningStandard
from main.forms import WinningStandardCreateForm


#Crear fase
class CreateWinningStandard(LoginRequiredMixin, CreateView):
    model = WinningStandard
    form_class = WinningStandardCreateForm
    template_name = 'admin/stages/stage_form.html'
    success_url = reverse_lazy('main:stage_list')

    def post(self, request, *args, **kwargs):
        # print(request.POST)
        form = WinningStandardCreateForm(request.POST)
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
class WinningStandardList(LoginRequiredMixin, ListView):
    model = WinningStandard
    template_name = 'admin/stages/stage_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Fases'
        return context


#Detalle de fase
class WinningStandardDetail(LoginRequiredMixin, DetailView):
    model = WinningStandard
    template_name = 'admin/stages/stage_detail.html'


#Actualizar fase
class UpdateWinningStandard(LoginRequiredMixin, UpdateView):
    model = WinningStandard
    template_name = 'admin/stages/stage_form.html'
    success_url = reverse_lazy('main:stage_list')

    def get(self, request, pk):
        winning_standard = get_object_or_404(self.model, pk=pk)
        form = WinningStandardCreateForm(instance=winning_standard)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk):
        winning_standard = get_object_or_404(self.model, pk=pk)
        form = WinningStandardCreateForm(request.POST, instance=winning_standard)
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
class DeleteWinningStandard(LoginRequiredMixin, DeleteView):
    model = WinningStandard
    success_url = reverse_lazy('main:stage_list')
    template_name = 'admin/stages/stage_confirm_delete.html'