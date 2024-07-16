from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

from .models import Medicine
# Create your views here.

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        return reverse_lazy('medicines')

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy('medicines')

    def form_valid(self, form):
        user = form.save()
        if user is not None:
            login(self.request, user)
        return super(RegisterPage, self).form_valid(form)

    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('medicines')
        return super(RegisterPage, self).get(*args, **kwargs)

class MedicineList(LoginRequiredMixin, ListView):
    model = Medicine
    context_object_name = 'medicines'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['medicines'] = context['medicines'].filter(user=self.request.user)

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['medicines'] = context['medicines'].filter(
                medicine_name__icontains=search_input)

        context['search_input'] = search_input

        return context

class MedicineDetail(LoginRequiredMixin, DetailView):
    model = Medicine
    context_object_name = 'medicine'

class MedicineCreate(LoginRequiredMixin, CreateView):
    model = Medicine
    fields = ['medicine_name', 'description', 'quantity', 'expiry_date']
    success_url = reverse_lazy('medicines')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super(MedicineCreate, self).form_valid(form)

class MedicineUpdate(LoginRequiredMixin, UpdateView):
    model = Medicine
    fields = ['medicine_name', 'description', 'quantity', 'expiry_date']
    success_url = reverse_lazy('medicines')

class MedicineDelete(LoginRequiredMixin, DeleteView):
    model = Medicine
    context_object_name = 'medicine'
    success_url = reverse_lazy('medicines')
    def get_queryset(self):
        owner = self.request.user
        return self.model.objects.filter(user=owner)