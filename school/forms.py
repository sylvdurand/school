from django import forms

from .models import Dictee, Probleme

class DicteeForm(forms.ModelForm):

    class Meta:
        model = Dictee
        fields = ('title', 'text', 'type', 'classe', 'niveau')

class ProblemeForm(forms.ModelForm):
    class Meta:
        model = Probleme
        fields = ('title', 'text', 'formule_resultat', 'unite_resultat', 'classe')
