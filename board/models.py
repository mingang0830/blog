from django.contrib.auth.models import User
from django.db import models


class Board(models.Model):
    title = models.CharField(max_length=512)
    content = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.DO_NOTHING, null= True)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)
