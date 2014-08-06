from django import forms

class ShortenUrlForm(forms.Form):
    url = forms.URLField(max_length=255, min_length=3)
