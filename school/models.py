from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

TYPE_CLASSE = (
    ('PS', 'Petite section'),
    ('MS', 'Moyenne section'),
    ('GS', 'Grande section'),
    ('CP', 'CP'),
    ('CE1A', 'CE1 A'),
    ('CE1B', 'CE1 B'),
    ('CE1C', 'CE1 C'),
    ('CE2', 'CE2'),
    ('CM1', 'CM1'),
    ('CM2', 'CM2'),
    ('6', '6ieme'),
)

class Dictee(models.Model):
    TYPE_DE_DICTEE = (
        ('L', 'Liste de mots'),
        ('T', 'Text'),
    )
    title = models.CharField(max_length=200)
    text = models.TextField(default='')
    type = models.CharField(max_length=1, choices=TYPE_DE_DICTEE, default='L')
    created_date = models.DateTimeField(default=timezone.now)
    classe = models.CharField(max_length=6,choices=TYPE_CLASSE, default='CE1C', null=True)
    niveau = models.PositiveSmallIntegerField(null=True, default=1)
    def publish(self):
        self.published_date = timezone.now()
        self.save()
    def __str__(self):
        return self.title


class Enfant(models.Model):
    prenom = models.CharField(max_length=20)
    nom = models.CharField(max_length=30)
    classe = models.CharField(max_length=6,choices=TYPE_CLASSE, default='CE1C', null=True)
    def __str__(self):
        return '%s %s' % (self.prenom, self.nom)


class Probleme(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField(default='')
    formule_resultat = models.CharField(default='',max_length=200)
    unite_resultat = models.CharField(default='',max_length=20, null=True)
    created_date = models.DateTimeField(default=timezone.now)
    classe = models.CharField(max_length=6,choices=TYPE_CLASSE, default='CE1C', null=True)

    def __str__(self):
        return '%s' % self.title


class Score(models.Model):
    enfant = models.ForeignKey(Enfant)
    score = models.PositiveSmallIntegerField(default=0)
    def __str__(self):
        return '%s : %d' % (self.enfant.prenom, self.score)

