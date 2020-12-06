from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from main.models import Post, Tournament, Stage, Game
from main.forms import PostCreateForm, TorneoCreateForm, StageCreateForm

#Crear fase
class CreateStage(CreateView):
    model = Stage
    form_class = StageCreateForm
    template_name = 'admin/stages/create_stage.html'
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
    template_name = 'amdin/stages/stage_detail.html'
