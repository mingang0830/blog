from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import Board, Comment, SubComment


class WritePost(forms.Form):
    title = forms.CharField(max_length=512, required=True, )
    content = forms.CharField(widget=forms.Textarea, required=True)


class UpdatePost(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'content']


class UserForm(UserCreationForm):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs['placeholder'] = "문자, 숫자, @.+-_만 가능"
        self.fields['password1'].widget.attrs['placeholder'] = "8자 이상 문자, 숫자 포함"
    email = forms.EmailField(label="이메일")
    
    class Meta:
        model = User
        fields = ["username", "password1", "password2", "email"]


class LoginForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'password']


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['comment']
        
        
class SubCommentForm(forms.ModelForm):
    class Meta:
        model = SubComment
        fields = ['subcomment']
 