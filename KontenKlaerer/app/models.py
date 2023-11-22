from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=200)
    parent = models.ForeignKey(
        'self', on_delete=models.CASCADE, null=True, blank=True)
    expense = models.BooleanField(default=True)
