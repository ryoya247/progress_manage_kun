from django.db import models
from django.utils import timezone
from django.core.validators import MaxValueValidator

# Create your models here.
class Task(models.Model):
    title = models.CharField(max_length=60)
    author = models.ForeignKey(
        'auth.User',
        on_delete=models.CASCADE,
    )
    progress = models.PositiveIntegerField(
        default=0,
        validators=[MaxValueValidator(100)]
    )
    due_date = models.DateField(default=timezone.now)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
