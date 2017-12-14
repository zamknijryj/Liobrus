from django.db import models


class Oceny(models.Model):
    test = models.CharField(max_length=140)
    oceny = models.CharField(max_length=10)

    def __str__(self):
        return "Test"
