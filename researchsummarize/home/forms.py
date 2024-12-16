from django import forms

class PromptForm(forms.Form):
    field = forms.CharField(label='Research field:', widget=forms.TextInput(attrs={'id': 'topic', 'placeholder':" "}), required=False)
    topics = forms.CharField(label='Your research interest(s):', widget=forms.TextInput(attrs={'id': 'topic', 'placeholder':" "}), required=True)
    file = forms.FileField()