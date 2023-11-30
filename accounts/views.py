from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic.edit import UpdateView
from django.views.generic import DetailView
from .models import Profile
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views.generic.edit import CreateView
from django.views.generic import ListView
from django.http import Http404
from django.contrib.auth.models import Group 
from django.db.models import Q
from django.views import View



class SignUpView(SuccessMessageMixin,CreateView):
    form_class = UserCreationForm
    template_name = 'accounts/form.html'
    success_url = reverse_lazy('profile_update')
    success_message = "Account has been created! Please Login and Update you Profile for getting activeated!"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Account'
        return context
    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return super().form_valid(form)
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            raise Http404("Page not found") 
        return super().get(request, *args, **kwargs)


class PasswordUpdateView(SuccessMessageMixin,PasswordChangeView):
    form_class = PasswordChangeForm
    template_name = "accounts/form.html"
    success_url = reverse_lazy('index')
    success_message = "Password has been updated!"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["title"] = "Password change" 
        return context
    

class ProfileUpdateView(LoginRequiredMixin, SuccessMessageMixin, UpdateView):
    model = Profile
    template_name = 'accounts/form.html'
    success_url = reverse_lazy('profile')
    success_message = "Profile has been Updated!"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Profile'
        return context

    def get_object(self):
        # Try to get the user's profile, or create it if it doesn't exist
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile
    def get_form(self, form_class=None):
        profile = self.get_object()
        # Check the profile type and conditionally add the 'qualifications' field
        if profile.type == 'Premium':
            self.fields = ['name', 'email', 'mobile_number', 'about']
        else:
            self.fields = ['name', 'email', 'mobile_number']
        # Create and return the form with the appropriate fields
        form = super().get_form(form_class)
        return form


class ProfileView(LoginRequiredMixin, DetailView):
    model = Profile
    template_name = 'accounts/profile.html'  
    context_object_name = 'profile' 
    def get_object(self, queryset=None):
        profile, created = Profile.objects.get_or_create(user=self.request.user)
        return profile
    
class ProfileListView(LoginRequiredMixin,ListView):
    model = Profile
    template_name = "accounts/profile_list.html"
    paginate_by = 10
    ordering = ['-pk']
    def get(self, request, *args, **kwargs):
        # Check if the user is a superuser
        if not request.user.is_superuser:
            raise Http404("You don't have permission to access this page.")
        return super().get(request, *args, **kwargs)


class UserProfileUpdateView(LoginRequiredMixin,SuccessMessageMixin,UpdateView):
    model = Profile
    template_name = "accounts/form.html"
    fields="__all__"
    success_message = "Profile has been Updated."
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Profile'
        return context
    def get(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise Http404("You don't have permission to access this page.")
        return super().get(request, *args, **kwargs)

class UserProfileDetailView(DetailView):
    model = Profile
    template_name = "accounts/user_profile_detail.html"
    def get(self, request, *args, **kwargs):
        if not self.request.user.is_superuser:
            raise Http404("You don't have permission to access this page.")
        return super().get(request, *args, **kwargs)
    


