from django.db import models


class DataFiles(models.Model):
    filename = models.CharField(max_length=200)
