from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator

# Create your models here.
class Task(models.Model):
    title = models.CharField(
        max_length=60,
        verbose_name="タスク名"
    )
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )
    progress = models.PositiveIntegerField(
        default=0,
        verbose_name="進捗",
        validators=[MaxValueValidator(100)]
    )
    due_date = models.DateField(
        default=timezone.now,
        verbose_name="期限"
    )
    is_complete = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title


class Report(models.Model):
    task = models.ForeignKey(
        Task,
        on_delete=models.CASCADE
    )
    add_progress = models.PositiveIntegerField(
        default=0,
        verbose_name="進捗プラス",
        validators=[MaxValueValidator(100)]
    )
    text = models.TextField(
        default="```\nslackの記法が使えます\n```",
        verbose_name="やったこと",
        max_length=400,
        blank=False
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


    def __str__(self):
        return self.text
