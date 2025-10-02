from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator

class Exercise(models.Model):
    name = models.CharField(max_length=30)
    description = models.CharField(max_length=300)
    instructions = models.CharField(max_length=300)
    target_muscles = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    equipment = models.CharField(max_length=50, null=True)
    difficulty = models.CharField(max_length=30)
    tips = models.CharField(max_length=300)

class Workoutplan(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    weekday = models.CharField(max_length=9, choices=[
        ('mon','monday'),
        ('tue','tuesday'),
        ('wed','wednesday'),
        ('thur','thursday'),
        ('fri','friday'),
        ('sat','saturday'),
        ('sun','sunday')
    ])
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    reps = models.PositiveIntegerField(validators=[MinValueValidator(1)], null=True)
    sets = models.PositiveIntegerField(validators=[MinValueValidator(1)], null=True)
    distance = models.DecimalField(max_digits=5, decimal_places=2, null=True)
    duration = models.DecimalField(max_digits=4, decimal_places=2, null=True)
    priority = models.PositiveIntegerField(validators=[MinValueValidator(1)])