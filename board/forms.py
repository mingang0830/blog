from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Board


class WritePost(forms.Form):
    title = forms.CharField(max_length=512, required=True)
    content = forms.CharField(widget=forms.Textarea, required=True)
    created_by = forms.CharField(max_length=128, required=True)


class UpdatePost(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'content', 'created_by']


class UserForm(UserCreationForm):
    email = forms.EmailField(label="이메일")
    
    class Meta:
        model = User
        fields = ("username", "password1", "password2", "email")


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']
