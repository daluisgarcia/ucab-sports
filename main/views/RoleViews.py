from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from main.models import Role
from main.forms import RoleCreateForm



# Crear juego
class CreateRole(CreateView):
    model = Role
    form_class = RoleCreateForm
    template_name = 'admin/roles/role_form.html'
    success_url = reverse_lazy('main:role_list')

    def post(self, request, *args, **kwargs):
        # print(request.POST)
        form = RoleCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Roles'
        context['botton_submit_title'] = 'Agregar'
        context['botton_cancel_title'] = 'Cancelar'
        context['action'] = 'add'
        return context


# Lista de roles
class RolesList(ListView):
    model = Role
    template_name = 'admin/roles/role_list.html'


# Actualizar rol
class UpdateRole(UpdateView):
    model = Role
    form_class = RoleCreateForm
    template_name = 'admin/roles/role_form.html'
    success_url = reverse_lazy('main:game_list')

    def post(self, request, pk):
        make = get_object_or_404(self.model, pk=pk)
        form = RoleCreateForm(request.POST, instance=make)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)
        form.save()
        self.object = None
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de rol'
        context['botton_title'] = 'Editar rol'
        context['action'] = 'edit'
        return context

