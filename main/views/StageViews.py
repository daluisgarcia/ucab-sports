from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView

from main.models import Posts, Torneos, Fases, Juegos
from main.forms import PostCreateForm, TorneoCreateForm, StageCreateForm

#Crear fase
class CreateStage(CreateView):
    Model = Fases
    form_class = StageCreateForm
    template_name = 'admin/stages/create_stage.html'
    success_url = reverse_lazy('main:stages_list')

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
    Model = Fases
    template_name = 'admin/stages/stages_list.html'

    def get(self, request):
        return '';

class StageDetail(DetailView):
    Model = Fases
