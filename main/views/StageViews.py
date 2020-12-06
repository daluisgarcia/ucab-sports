from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from main.models import Post, Tournament, Stage, Game
from main.forms import PostCreateForm, TorneoCreateForm, StageCreateForm

#Crear fase
class CreateStage(CreateView):
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

class StageList(ListView):
    model = Stage
    template_name = 'admin/stages/stage_list.html'

class StageDetail(DetailView):
    model = Stage
    template_name = 'admin/stages/stage_detail.html'

class UpdateStage(UpdateView):
    model = Stage
    template_name = 'admin/stages/stage_form.html'
    success_url = reverse_lazy('main:stage_list')

    def get(self, request, pk):
        make = get_object_or_404(self.model, pk=pk)
        form = StageCreateForm(instance=make)
        ctx = {'form': form}
        return render(request, self.template_name, ctx)

    def post(self, request, pk):
        make = get_object_or_404(self.model, pk=pk)
        form = StageCreateForm(request.POST, instance=make)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)

        form.save()
        return redirect(self.success_url)

class DeleteStage(DeleteView):
    model = Stage
    success_url = reverse_lazy('main:stage_list')
    template_name = 'admin/stages/stage_confirm_delete.html'