from __future__ import unicode_literals

from django.db import models
from django.utils import timezone



class Dictee(models.Model):
    TYPE_DE_DICTEE = (
        ('L', 'Liste de mots'),
        ('T', 'Text'),
    )
    title = models.CharField(max_length=200)
    text = models.TextField(default='')
    type = models.CharField(max_length=1, choices=TYPE_DE_DICTEE, default='T')
    created_date = models.DateTimeField(
            default=timezone.now)
    niveau = models.PositiveSmallIntegerField(null=True, default=0)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

