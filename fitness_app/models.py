from django.db import models

class Exercise(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    instructions = models.CharField(max_length=300)
    target_muscles = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    equipment = models.CharField(max_length=50, null=True)
    difficulty = models.CharField(max_length=30)
    tips = models.CharField(max_length=300)