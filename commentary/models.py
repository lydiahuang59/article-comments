from django.db import models
from django.contrib.auth.models import User, AbstractUser
from django import forms
from django.conf import settings
from vote.models import VoteModel

STATUS = (
    (-1, "Removed"),
    (0,"Draft"),
    (1,"Publish")
)

class User(AbstractUser):
    class Meta:
        db_table = 'auth_user'

class Article(models.Model):
    title = models.CharField(max_length=200, unique=True)
    slug = models.SlugField(max_length=200, unique=True)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, related_name='articles')
    created_on = models.DateTimeField(auto_now_add=True)
    source = models.URLField(null=True, blank=True)
    content = models.TextField(max_length=5000)
    status = models.IntegerField(choices=STATUS, default=0)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.title


class Comment(VoteModel, models.Model):
    article = models.ForeignKey(Article, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete= models.CASCADE, related_name='comments')
    content = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)
    status = models.IntegerField(choices=STATUS, default=1)
    score = models.IntegerField(default=0)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_on']

    def __str__(self):
        return self.content

class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={'rows':5}), label='')
    class Meta:
        model = Comment
        fields = ('content',)
