from django import forms

class UriSAFForm(forms.Form):
    leukocytes = forms.IntegerField(label='Leukocytes')