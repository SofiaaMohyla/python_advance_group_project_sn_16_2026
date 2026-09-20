from django.db import models
from django.conf import settings

class Event(models.Model):

    TYPE_CHOICES = [
        ("meeting", "Онлайн зустріч"),
        ("conference", "Конференція"),
        ("presentation", "Презентація")
    ]

    title = models.CharField(max_length=150, verbose_name='Назва')
    description = models.TextField(verbose_name="Опис")
    date = models.DateField(blank=True, null=True, verbose_name="Дата проведення")
    place = models.CharField(max_length=300, verbose_name='Місце проведення')
    type = models.CharField(max_length=15, choices=TYPE_CHOICES, verbose_name="Тип події")
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="tasks", verbose_name="Власник")

    #media = models.FileField(upload_to='tasks/', blank=True, null=True, verbose_name="Файли")

    created_at = models.DateTimeField(auto_now=True)
    updated_at = models.DateTimeField(auto_now_add=True)