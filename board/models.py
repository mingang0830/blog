from django.db import models

class Board(models.Model):
    title = models.CharField(max_length=512)
    content = models.TextField()
    created_by = models.CharField(max_length=128)
    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)