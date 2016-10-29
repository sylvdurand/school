from django.contrib import admin

from django.contrib import admin
from .models import Dictee, Enfant, Probleme, Score

admin.site.register(Enfant)
admin.site.register(Probleme)
admin.site.register(Dictee)
admin.site.register(Score)
