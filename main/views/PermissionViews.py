from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from main.models import Permission
from main.forms import PermissionCreateForm

# Crear juego
class CreatePermission(CreateView):
    model = Permission
    form_class = PermissionCreateForm
    template_name = 'admin/permission/permission_form.html'
    success_url = reverse_lazy('main:permission_list')

    def post(self, request, *args, **kwargs):
        # print(request.POST)
        form = PermissionCreateForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(self.success_url)
        self.object = None
        context = self.get_context_data(**kwargs)
        context['form'] = form
        return render(request, self.template_name, context)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Permisos'
        context['botton_submit_title'] = 'Agregar'
        context['botton_cancel_title'] = 'Cancelar'
        context['action'] = 'add'
        return context


# Lista de roles
class PermissionList(ListView):
    model = Permission
    template_name = 'admin/permission/permission_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Permisos'
        return context


# Actualizar rol
class UpdatePermission(UpdateView):
    model = Permission
    form_class = PermissionCreateForm
    template_name = 'admin/permission/permission_form.html'
    success_url = reverse_lazy('main:permission_list')

    def post(self, request, pk):
        make = get_object_or_404(self.model, pk=pk)
        form = PermissionCreateForm(request.POST, instance=make)
        if not form.is_valid():
            ctx = {'form': form}
            return render(request, self.template_name, ctx)
        form.save()
        self.object = None
        return redirect(self.success_url)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Edición de permisos'
        context['botton_title'] = 'Editar permiso'
        context['action'] = 'edit'
        return context

