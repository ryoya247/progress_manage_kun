from django.shortcuts import render

# Create your views here.
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.views import PasswordChangeView, PasswordChangeDoneView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.models import User
from django.urls import reverse_lazy
from django.views import generic


class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy('login')
    template_name = 'accounts/signup.html'



class PasswordChange(LoginRequiredMixin, PasswordChangeView):
    success_url = reverse_lazy('accounts:password_change_done')
    template_name = 'accounts/password_change.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form_name"] = "password_change"
        return context


class PasswordChangeDone(LoginRequiredMixin,PasswordChangeDoneView):
    template_name = 'accounts/password_change_done.html'


class UpdateUserInfomation(LoginRequiredMixin, generic.UpdateView):
    model = User
    fields = [
        'username'
    ]
    template_name = 'accounts/update_user.html'
    success_url = reverse_lazy('tasks:taskList')
