from django import forms

class ShortenUrlForm(forms.Form):
    link = forms.URLField(min_length=3, max_length=2000)
