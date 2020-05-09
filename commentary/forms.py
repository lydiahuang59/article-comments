from django.db import models
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':5}), label='')
    class Meta:
        model = Comment
        fields = ('content',)