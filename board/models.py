from statistics import mode
from django.contrib.auth.models import User
from django.db import models


class Board(models.Model):
    title = models.CharField(max_length=512)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null= True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)

class Commentable(models.Model):
    class Meta:
        abstract = True
    
    post = models.ForeignKey(Board, on_delete=models.CASCADE, null=True)
    comment = models.TextField()

    def __str__(self):
        return self.comment

class Comment(Commentable):
    date = models.DateTimeField(auto_now_add=True)
    
class SubComment(Commentable):
    parent_comment = models.ForeignKey(Comment, on_delete=models.CASCADE, null=True)
    