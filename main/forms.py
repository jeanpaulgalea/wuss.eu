from django import forms

class ShortenUrlForm(forms.Form):
    link = forms.URLField(max_length=255, min_length=3)
