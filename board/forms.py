from dataclasses import field
import imp
from operator import mod
from django import forms
from .models import Board

class WritePost(forms.Form):
    title = forms.CharField(max_length=512, required=True)
    content = forms.CharField(widget=forms.Textarea, required=True)
    created_by = forms.CharField(max_length=128, required=True)


class UpdatePost(forms.ModelForm):
    class Meta:
        model = Board
        fields = ['title', 'content', 'created_by']
