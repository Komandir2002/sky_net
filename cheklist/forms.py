from django import forms
from . import models



class AplicationsForm(forms.ModelForm):
    class Meta:
        model = models.Applications
        fields = ['status_id', 'bx_id', 'planup_id', 'user_id']