from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm, UserChangeForm

from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _
from django.db import models
from PIL import Image
from .models import *

class SignUpUserForm(UserCreationForm):

    class Meta:
        model = User
        fields = ('image','username', 'email','first_name', 'last_name', 'password1', 'password2',)

        widgets = {
            'username': forms.TextInput(attrs={'class':'from-input'}),
        }       

class EditProfileForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('image','username', 'email','first_name', 'last_name',)