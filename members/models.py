from django.db import models

class SpamWebsite(models.Model):
    keyword = models.CharField(max_length=255)
    spam_type = models.CharField(max_length=50)  # Make sure this matches your choices
    # Add other fields if necessary

    def __str__(self):
        return self.keyword
