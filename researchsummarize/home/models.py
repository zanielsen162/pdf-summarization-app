from django.db import models
from django.contrib.postgres.fields import ArrayField 

# Create your models here.
class Summary(models.Model):
  title = models.CharField(max_length=255)
  summary = models.TextField()

class Member(models.Model):
  username = models.CharField(max_length=255)
  list = models.JSONField(null=True)