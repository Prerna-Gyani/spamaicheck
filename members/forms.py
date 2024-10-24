from django import forms

class SpamDetectionForm(forms.Form):
    website_url = forms.URLField(label='Website URL', required=True)
    spam_type = forms.ChoiceField(
        label='Type of Spam',
        choices=[
            ('phishing', 'Phishing'),
            ('malware', 'Malware'),
            ('spammy_content', 'Spammy Content'),
        ],
        required=True
    )
