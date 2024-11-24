from django import forms

class SpamDetectionForm(forms.Form):
    website_url = forms.URLField(label='Website URL', required=True)
