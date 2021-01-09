from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, View
from django.contrib.auth.mixins import LoginRequiredMixin

from main.models import Post, Tournament, Stage, Game
from main.forms import PostCreateForm


class AdminIndex(LoginRequiredMixin, View):
    template_name = 'admin/adminMain.html'

    def get(self, request):
        return render(request, self.template_name, context=None)

# Lista de juegos
class GamesList(LoginRequiredMixin, ListView):
    model = Game
    template_name = 'admin/game/game.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        context['title'] = 'Lista de Juegos'
        context['create_url'] = reverse_lazy('main:create_game')
        context['list_url'] = reverse_lazy('main:games_list')
        context['entity'] = 'Juegos'
        return context