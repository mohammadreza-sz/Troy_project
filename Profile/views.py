from django.shortcuts import render
#helen{
from django.views import generic
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django.urls import reverse_lazy
from .forms import ProfileForm
 

class UserRegisterView(generic.CreateView):
    form_class = ProfileForm
    # i hava a question..
    template_name = 'registration/register.html'
    success_url = reverse_lazy('login')

class UserEditView(generic.UpdateView):
    form_class = UserChangeForm
    # i hava a question..
    template_name = 'registration/edit_profile.html'
    success_url = reverse_lazy('home')

    def get_object(self):
        return self.reques.user

#}helen