from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from main.models import Game
from main.forms import GameCreateForm



# Crear juego
class CreateGame(CreateView):
    model = Game
    form_class = GameCreateForm
    template_name = 'admin/games/game_form.html'
    success_url = reverse_lazy('main:game_list')

    def post(self, request, *args, **kwargs):
        # print(request.POST)
        form = GameCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'El juego ha sido creado satisfactoriamente')
            return HttpResponseRedirect(self.success_url)
        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación del juego'
        context['botton_title'] = 'Crear juego'
        context['action'] = 'add'
        return context


# Lista de posts
class GamesList(ListView):
    model = Game
    template_name = 'admin/games/game_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Juegos'
        return context


# Actualizar Post
class UpdateGame(UpdateView):
    model = Game
    form_class = GameCreateForm
    template_name = 'admin/games/game_form.html'
    success_url = reverse_lazy('main:game_list')

    def post(self, request, pk):
        make = get_object_or_404(self.model, pk=pk)
        form = GameCreateForm(request.POST, instance=make)
        if not form.is_valid():
            ctx = {'form': form, 'title': 'Edición del juego', 'botton_title': 'Editar juego'}
            return render(request, self.template_name, ctx)
        form.save()
        self.object = None
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición del juego'
        context['botton_title'] = 'Editar juego'
        context['action'] = 'edit'
        return context


#Eliminar juego
@login_required
def deleteGame(request, pk):
    game = Game.objects.get(id=pk)
    game.delete()
    print('Juego eliminado')
    messages.success(request, 'El juego se ha eliminado satisfactoriamente')
    return redirect(reverse_lazy('main:game_list'))
