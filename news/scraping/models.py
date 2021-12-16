from django.db import models
from django.utils import timezone

# Create your models here.


class Headline(models.Model):
    title = models.CharField(max_length=250)
    summary_one = models.CharField(max_length=250)
    summary_two = models.CharField(max_length=250)
    published_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering = ['published_date']

    class Admin:
        pass
