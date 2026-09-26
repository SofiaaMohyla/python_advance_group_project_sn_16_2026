from django.db import models
from django.contrib.auth.models import AbstractUser
from authentication.models import CustomUser
# Create your models here.


class Portfolio(models.Model):
    
    CREATED_TIME_CHOICES = [
        ('Newest', 'Найновіші'),
        ('Oldest', 'Найстаріші'),
    ]
    
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='portfolio')
    title = models.CharField(max_length=100, default='Моє портфоліо', verbose_name='Назва портфоліо')
    description = models.TextField(blank=True, verbose_name='Опис портфоліо')
    created_time = models.CharField(max_length=10, choices=CREATED_TIME_CHOICES, default='Newest', verbose_name='Сортування за часом створення')
    media = models.FileField(upload_to='portfolio/', blank=True, null=True, verbose_name='Медіа')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.title
    
    class Meta:
        verbose_name = 'Портфоліо'
        verbose_name_plural = 'Портфоліо'
        ordering = ['-created_at']
        

class Comments(models.Model):
    portfolio = models.ForeignKey(Portfolio, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='comments')
    content = models.TextField(verbose_name='Коментар')
    media = models.FileField(upload_to='portfolio/', blank=True, null=True, verbose_name='Медіа')
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = 'Коментар'
        verbose_name_plural = 'Коментарі'
        ordering = ['-created_at']