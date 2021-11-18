from django import forms
from .models import Comment
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
import re

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя',  widget=forms.TextInput(attrs={'class': 'form-control', 'autocomplete':"off"}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Подтверждения пароля', widget=forms.PasswordInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя',  widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class CommentForm(forms.ModelForm):

    # def __init__(self, *args, **kwargs):
    #     super(ArticleAddForm, self).__init__(*args, **kwargs)
    #     self.fields['category'].empty_label = ""

    class Meta:
        model = Comment
        # fields = ['title', 'content', 'is_published']
        fields = ['name', 'text']
        #
        widgets = {
            'name': forms.TextInput(attrs = {'class': 'form-control', 'style':'margin-left:20px;', 'autocomplete': 'off'}),
            'text': forms.Textarea(attrs = {'class': 'form-control',  'style': 'height: 200px;width:735px; align:center;', 'autocomplete': 'off'}),
        }
