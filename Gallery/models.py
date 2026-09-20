from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
from pathlib import Path 

class MediaItem(models.Model):
    MEDIA_TYPE_CHOICES = [
        ('image', 'Image'),
        ('video', 'Video'),
        ('audio', 'Audio'),
    ]

    title = models.CharField(max_length=255)
    file = models.FileField(upload_to='media_items/')
    media_type = models.CharField(max_length=10, choices=MEDIA_TYPE_CHOICES)
    uploaded_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']
        

    def __str__(self):
        return self.title

class Comment(models.Model):
    media_item = models.ForeignKey(MediaItem, on_delete=models.CASCADE, related_name='Коментарі')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Comment by {self.author} on {self.media_item}'

class Like(models.Model):
    media_item = models.ForeignKey(MediaItem, on_delete=models.CASCADE, related_name='Лайки')
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('media_item', 'user')
        ordering = ['-created_at']

    def __str__(self):
        return f'Like by {self.user} on {self.media_item}'
        