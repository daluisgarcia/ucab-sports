from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView
from django.contrib import messages

from main.models import Post, Tournament, Stage, Game
from main.forms import PostCreateForm



# Crear Post
class CreatePost(CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'admin/posts/post_form.html'
    success_url = reverse_lazy('main:post_list')

    def post(self, request, *args, **kwargs):
        # print(request.POST)
        form = PostCreateForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'El post ha sido creado satisfactoriamente')
            return HttpResponseRedirect(self.success_url)
        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación del post'
        context['botton_title'] = 'Crear post'
        context['action'] = 'add'
        return context


# Lista de posts
class PostsList(ListView):
    model = Post
    template_name = 'admin/posts/post_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Posts'
        return context


# Detalle del post
class PostDetail(DetailView):
    model = Post
    template_name = 'admin/posts/post_detail.html'


# Actualizar Post
class UpdatePost(UpdateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'admin/posts/post_form.html'
    success_url = reverse_lazy('main:post_list')

    def post(self, request, pk):
        make = get_object_or_404(self.model, pk=pk)
        form = PostCreateForm(request.POST, instance=make)
        if not form.is_valid():
            ctx = {'form': form, 'title': 'Edición del post', 'botton_title': 'Editar post'}
            return render(request, self.template_name, ctx)
        form.save()
        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición del post'
        context['botton_title'] = 'Editar post'
        context['entity'] = 'Post'
        context['action'] = 'edit'
        return context


#Eliminar post
class DeletePost(DeleteView):
    model = Post
    success_url = reverse_lazy('main:post_list')
    template_name = 'admin/posts/post_confirm_delete.html'
