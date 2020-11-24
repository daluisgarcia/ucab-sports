from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from main.models import Posts

def index(request):
    return render(request, 'main/index.html', context=None)


#Vista basada en clase
class ListaPosts(ListView):
    model = Posts
    template_name = 'main/posts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        #Diccionario de datos que se le manda a la plantilla
        context['title'] = 'Lista de posts'
        #context['create_url'] = reverse_lazy('category_create')
        #context['list_url'] = reverse_lazy('category_list')
        context['entity'] = 'Posts'
        return context