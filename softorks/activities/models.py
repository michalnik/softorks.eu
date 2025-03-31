from django.db import models


# Create your models here.
class Activity(models.Model):
    created_on = models.DateField()
    title = models.CharField(max_length=255)
    issue_url = models.URLField(max_length=255)
    comment_url = models.URLField(max_length=255)
