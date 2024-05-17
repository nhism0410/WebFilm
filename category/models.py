from django.db import models


# Create your models here.
class Category(models.Model):
    title = models.CharField(max_length=255, null=False, blank=False)
    def __str__(self):
        return self.title 