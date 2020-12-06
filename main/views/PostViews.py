from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView

from main.models import Posts, Torneos, Fases, Juegos
from main.forms import PostCreateForm, TorneoCreateForm

# Lista de posts
class PostsList(ListView):
    model = Posts
    template_name = 'admin/posts/posts.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Lista de posts'
        context['create_url'] = reverse_lazy('main:create_post')
        context['list_url'] = reverse_lazy('main:posts_list')
        context['entity'] = 'Posts'
        return context


# REVISAR
# Detalle del post
class PostDetail(ListView):
    template_name = 'admin/posts/post_detalle.html'

    """
    def __init__(self, *args, **kwargs):
        id = kwargs.pop('pk')
        model = Posts.objects.get(id = id)
    """

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Detalle del post'
        context['list_url'] = reverse_lazy('main:posts_list')
        context['entity'] = 'Posts'
        return context


# Crear Post
class CreatePost(CreateView):
    model = Posts
    form_class = PostCreateForm
    template_name = 'admin/posts/create_post.html'
    success_url = reverse_lazy('main:posts_list')

    def post(self, request, *args, **kwargs):
        # print(request.POST)
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
        context['title'] = 'Creación del post'
        context['botton_title'] = 'Crear post'
        context['list_url'] = reverse_lazy('main:posts_list')
        context['entity'] = 'Posts'
        context['action'] = 'add'
        return context


# Actualizar Post
class UpdatePost(UpdateView):
    model = Posts
    form_class = PostCreateForm
    template_name = 'admin/posts/create_post.html'
    success_url = reverse_lazy('main:posts_list')

    def get_context_data(self, **kwargs):
        # Obtener la instancia del objeto
        # print(self.get_object())
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición del post'
        context['botton_title'] = 'Editar post'
        context['list_url'] = reverse_lazy('main:posts_list')
        context['entity'] = 'Posts'
        context['action'] = 'edit'
        return context
