from django.db import models
from django.conf import settings

class Event(models.Model):
    title = models.CharField(max_lenth=150, verbose_name='Назва')
    description = models.TextField(verbose_name="Опис")
    date = models.DateField(blank=True, null=True, verbose_name="Дата проведення")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks", verbose_name="Власник")

    #media = models.FileField(upload_to='tasks/', blank=True, null=True, verbose_name="Файли")

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)