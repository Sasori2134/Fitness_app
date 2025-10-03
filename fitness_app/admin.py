from django.contrib import admin
from . import models

admin.site.register(models.Exercise)
admin.site.register(models.Workoutplan)
admin.site.register(models.CompletedWorkouts)
admin.site.register(models.WeightEntry)
admin.site.register(models.GoalWeight)


