from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DetailView
from django.contrib import messages
from django.conf import settings
from django.contrib.auth.mixins import LoginRequiredMixin

from main.models import Post, Tournament, Stage, Game
from main.forms import PostCreateForm


# Crear Post
class CreatePost(LoginRequiredMixin, CreateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'admin/posts/post_form.html'
    success_url = reverse_lazy('main:post_list')

    def post(self, request, *args, **kwargs):
        # print(request.POST)
        form = PostCreateForm(request.POST, request.FILES)
        self.object = None
        if form.is_valid():
            object = form.save(commit=False)
            object.owner = self.request.user
            object.save()
            return HttpResponseRedirect(self.success_url)
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Creación del post'
        context['button_title'] = 'Crear post'
        context['action'] = 'add'
        return context


# Lista de posts
class PostsList(LoginRequiredMixin, ListView):
    model = Post
    template_name = 'admin/posts/post_list.html'

    def get(self, request):
        if request.user.is_authenticated:
            self.object_list = self.model.objects.filter(owner=request.user)
            context = self.get_context_data()
            return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Posts'
        return context

# Lista de posts para el publico en general
class PublicPostList(ListView):
    model = Post
    template_name = 'admin/posts/public_post_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Posts'
        return context

# Detalle del post
class PostDetail(DetailView):
    model = Post
    template_name = 'admin/posts/post_detail.html'

    def get(self, request, pk):
        post = get_object_or_404(self.model, pk=pk)
        if post.owner == request.user:
            return super(PostDetail, self).get(request, pk)
        return redirect('main:admin_index')

# Actualizar Post
class UpdatePost(LoginRequiredMixin, UpdateView):
    model = Post
    form_class = PostCreateForm
    template_name = 'admin/posts/post_form.html'
    success_url = reverse_lazy('main:post_list')

    def get(self, request, pk):
        post = get_object_or_404(self.model, pk=pk)
        if post.owner == request.user:
            form = PostCreateForm(instance=post)
            self.object = None
            ctx = self.get_context_data()
            ctx['form'] = form
            return render(request, self.template_name, ctx)
        return redirect('main:admin_index') 

    def post(self, request, pk): 
        post = get_object_or_404(self.model, pk=pk)
        if post.owner != request.user:
            return redirect('main:admin_index')
        form = PostCreateForm(request.POST, instance=post)
        if not form.is_valid():
            ctx = {'form': form, 'title': 'Edición del post', 'button_title': 'Editar post'}
            return render(request, self.template_name, ctx)
        form.save()
        self.object = None
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición del post'
        context['button_title'] = 'Editar post'
        context['entity'] = 'Post'
        context['action'] = 'edit'
        return context


#Eliminar post
def deletePost(request, pk):
    post = Post.objects.get(id=pk)
    post.delete()
    print('Post eliminado')
    messages.success(request, 'El post se ha eliminado satisfactoriamente')
    return redirect(reverse_lazy('main:post_list'))
