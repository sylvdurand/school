from django import forms

from .models import Dictee

class DicteeForm(forms.ModelForm):

    class Meta:
        model = Dictee
        fields = ('title', 'text', 'type', 'classe', 'niveau')
