from django.conf import settings
from django.db import models


class Poll(models.Model):
    title = models.CharField("Назва", max_length=200)
    description = models.TextField("Опис", blank=True)
    is_active = models.BooleanField("Активне", default=True)
    created_at = models.DateTimeField("Створено", auto_now_add=True)
    updated_at = models.DateTimeField("Оновлено", auto_now=True)
    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="created_polls",
        verbose_name="Автор",
    )

    class Meta:
        ordering = ("-created_at",)
        verbose_name = "Голосування"
        verbose_name_plural = "Голосування"

    def __str__(self):
        return self.title


class PollOption(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="options")
    text = models.CharField("Варіант", max_length=250)

    class Meta:
        ordering = ("id",)
        verbose_name = "Варіант відповіді"
        verbose_name_plural = "Варіанти відповідей"

    def __str__(self):
        return self.text


class Vote(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE, related_name="votes")
    option = models.ForeignKey(PollOption, on_delete=models.CASCADE, related_name="votes")
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="votes")
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=("poll", "user"), name="one_vote_per_user_per_poll"),
        ]
        verbose_name = "Голос"
        verbose_name_plural = "Голоси"

    def __str__(self):
        return f"{self.user} — {self.poll}"
