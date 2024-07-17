from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.urls import reverse_lazy

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.contrib.auth import get_user_model

from django.contrib.auth.models import User


from .models import Medicine
from .forms import MedicineForm
# Create your views here.

# class CustomLoginView(LoginView):
#     template_name = 'base/login.html'
#     fields = '__all__'
#     redirect_authenticated_user = True

#     def get_success_url(self):
#         return reverse_lazy('medicines')

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True

    def get_success_url(self):
        user = self.request.user
        if user.is_authenticated:
            if user.is_staff:  # Check if the user is an admin
                return reverse_lazy('admin:index')  # Redirect to the admin page
            return reverse_lazy('medicines')  # Redirect to the medicines page
        return super().get_success_url()  # Fallback


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

# class MedicineList(LoginRequiredMixin, ListView):
#     model = Medicine
#     context_object_name = 'medicines'
    
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['medicines'] = context['medicines'].filter(user=self.request.user)

#         search_input = self.request.GET.get('search-area') or ''
#         if search_input:
#             context['medicines'] = context['medicines'].filter(
#                 medicine_name__icontains=search_input)

#         context['search_input'] = search_input

#         return context

class MedicineList(LoginRequiredMixin, ListView):
    model = Medicine
    context_object_name = 'medicines'
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        # Check if the user is an admin
        if self.request.user.is_staff:
            context['medicines'] = Medicine.objects.all()  # Admin sees all medicines
        else:
            context['medicines'] = context['medicines'].filter(user=self.request.user)  # Regular user sees their medicines

        search_input = self.request.GET.get('search-area') or ''
        if search_input:
            context['medicines'] = context['medicines'].filter(
                medicine_name__icontains=search_input)

        context['search_input'] = search_input

        return context


class MedicineDetail(LoginRequiredMixin, DetailView):
    model = Medicine
    context_object_name = 'medicine'

# class MedicineCreate(LoginRequiredMixin, CreateView):
#     model = Medicine
#     form_class = MedicineForm
#     # fields = ['medicine_name', 'description', 'quantity', 'expiry_date']
#     success_url = reverse_lazy('medicines')

#     def form_valid(self, form):
#         form.instance.user = self.request.user
#         return super(MedicineCreate, self).form_valid(form)

class MedicineCreate(LoginRequiredMixin, CreateView):
    model = Medicine
    form_class = MedicineForm
    success_url = reverse_lazy('medicines')

    def form_valid(self, form):
        # Set the user to the currently logged-in user
        form.instance.user = self.request.user
        return super().form_valid(form)

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_staff:
            # Remove the 'user' field for non-admin users
            form.fields.pop('user', None)
        return form

# class MedicineUpdate(LoginRequiredMixin, UpdateView):
#     model = Medicine
#     form_class = MedicineForm
#     # fields = ['medicine_name', 'description', 'quantity', 'expiry_date']
#     success_url = reverse_lazy('medicines')

class MedicineUpdate(LoginRequiredMixin, UpdateView):
    model = Medicine
    form_class = MedicineForm
    success_url = reverse_lazy('medicines')

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        if not self.request.user.is_staff:
            # Remove the 'user' field for non-admin users
            form.fields.pop('user', None)
        return form

# class MedicineDelete(LoginRequiredMixin, DeleteView):
#     model = Medicine
#     context_object_name = 'medicine'
#     success_url = reverse_lazy('medicines')
#     def get_queryset(self):
#         owner = self.request.user
#         return self.model.objects.filter(user=owner)

class MedicineDelete(LoginRequiredMixin, DeleteView):
    model = Medicine
    context_object_name = 'medicine'
    success_url = reverse_lazy('medicines')

    def get_queryset(self):
        # Allow admins to delete any medicine, otherwise filter by the current user
        if self.request.user.is_staff:
            return self.model.objects.all()
        return self.model.objects.filter(user=self.request.user)


class UserMedicineList(LoginRequiredMixin, ListView):
    model = Medicine
    context_object_name = 'medicines'
    template_name = 'base/user_medicines.html'

    def get_queryset(self):
        user_id = self.kwargs['user_id']
        return Medicine.objects.filter(user__id=user_id)  # Fetch medicines for the specified user

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user_id = self.kwargs['user_id']
        context['user'] = User.objects.get(id=user_id)  # Add the user to the context

        search_input = self.request.GET.get('search-area') or ''
        medicines = context['medicines']

        if search_input:
            medicines = medicines.filter(medicine_name__icontains=search_input)

        context['medicines'] = medicines
        context['search_input'] = search_input

        return context