from statistics import mode
from django.contrib.auth.models import User
from django.db import models
import os

class Board(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_by = models.CharField(max_length=218)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
    upload_file = models.FileField(upload_to='uploads/', null=True)

    def summary(self):
        if len(self.title) > 30:
            return self.title[:30] + '...'
        else:
            return self.title

class Commentable(models.Model):
    class Meta:
        abstract = True
    
    post = models.ForeignKey(Board, on_delete=models.CASCADE, null=True)
    date = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.comment

class Comment(Commentable):
    comment = models.CharField('댓글', max_length=200)
    
class SubComment(Commentable):
    subcomment = models.CharField('대댓글', max_length=150,null=True)
    parent_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    
    