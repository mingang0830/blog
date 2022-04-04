from statistics import mode
from django.contrib.auth.models import User
from django.db import models


class Board(models.Model):
    title = models.CharField(max_length=512)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null= True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    comment = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Board, on_delete=models.CASCADE, null=True)

    # 댓글이 object형태가 아닌 댓글 자체가 보이도록
    def __str__(self):
        return self.comment
