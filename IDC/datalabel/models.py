from django.db import models
from django.utils import timezone

# Create your models here.


class RequestModel(models.Model):
    projectName = models.CharField(max_length=64)
    projectDesc = models.TextField()
    projectRootDir = models.CharField(max_length=128)
    categories = models.TextField(help_text="please provide in \
                                             cat1, cat2, cat3 format")
    dateCreated = models.DateTimeField(default=timezone.now)
    author = models.CharField(max_length=64)
    ready = models.CharField(max_length=10, default="not ready")
