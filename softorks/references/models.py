from django.db import models


# Create your models here.
class Reference(models.Model):
    created_on = models.DateField()
    name = models.CharField(max_length=100)
    description = models.TextField()
    url = models.URLField()
    source_url = models.URLField()
    # mypy complaints here about:
    #    references/models.py:5: error: Could not resolve manager type for
    #    "references.models.Reference.objects"  [django-manager-missing]
    objects: models.Manager["Reference"] = models.Manager()

    class Meta:
        indexes = [
            models.Index(fields=["created_on"]),
            models.Index(fields=["name"]),
            models.Index(fields=["description"]),
        ]
