from django.db import models


# Create your models here.
class Reference(models.Model):
    created_on = models.DateField()
    name = models.CharField(max_length=100)
    description = models.TextField()
    url = models.URLField()
    source_url = models.URLField()

    class Meta:
        indexes = [
            models.Index(fields=['created_on']),
            models.Index(fields=['name']),
            models.Index(fields=['description']),
        ]
