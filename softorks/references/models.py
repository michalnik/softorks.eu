from django.db import models


# Create your models here.
class Reference(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    url = models.URLField()
    source_url = models.URLField()
