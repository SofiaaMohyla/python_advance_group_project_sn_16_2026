from django.db import models

class Material(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='materials/images/', blank=True)
    file = models.FileField(upload_to='materials/', blank=True)
    you_tube_link = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.title