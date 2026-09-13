from django.db import models

class Material(models.Model):
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=500)
    file = models.FileField(upload_to='materials/')
    you_tube_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title