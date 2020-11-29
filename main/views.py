from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from main.models import Posts, Torneos, Fases
from main.forms import PostCreateForm, TorneoCreateForm

def index(request):
    return render(request, 'index.html', context=None)



#Lista de posts
class ListaPosts(ListView):
    model = Posts
    template_name = 'posts/posts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        #Diccionario de datos que se le manda a la plantilla
        context['title'] = 'Lista de posts'
        context['create_url'] = reverse_lazy('crear_post')
        context['list_url'] = reverse_lazy('lista_posts')
        context['entity'] = 'Posts'
        return context



#Crear Post
class CrearPost(CreateView):
    model = Posts
    form_class = PostCreateForm
    template_name = 'posts/create_post.html'
    success_url = reverse_lazy('lista_posts')

    def post(self, request, *args, **kwargs):
        print(request.POST)
        form = PostCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de post'
        context['list_url'] = reverse_lazy('lista_posts')
        context['entity'] = 'Posts'
        return context



#Lista de torneos
class ListaTorneos(ListView):
    model = Torneos
    template_name = 'torneos/torneos.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        #Diccionario de datos que se le manda a la plantilla
        context['title'] = 'Lista de Torneos'
        context['create_url'] = reverse_lazy('crear_torneo')
        context['list_url'] = reverse_lazy('lista_torneos')
        context['entity'] = 'Torneos'
        return context


#Crear Torneo
class CrearTorneo(CreateView):
    model = Torneos
    form_class = TorneoCreateForm
    template_name = 'torneos/create_torneo.html'
    success_url = reverse_lazy('lista_torneos')

    def post(self, request, *args, **kwargs):
        print(request.POST)
        form = TorneoCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación de torneo'
        context['list_url'] = reverse_lazy('lista_torneos')
        context['entity'] = 'Torneos'
        return context

class CreateStage(CreateView):
    Model = Fases
    template_name = 'stages/create.html'

    def get(self, request):
        return ''

    def post(self, request):
        return ''