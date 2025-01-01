from django import forms
from .models import PromptModel

class PromptForm(forms.ModelForm):
    class Meta:
        model = PromptModel
        fields = ['field', 'topics', 'file']
        widgets = {
            'myfield': forms.TextInput(attrs={'class': 'myfieldclass'}),
        }
