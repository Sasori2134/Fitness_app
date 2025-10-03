from rest_framework import serializers
from fitness_app import models
from rest_framework.exceptions import ValidationError
from decimal import Decimal
from django.contrib.auth.models import User
from django.core.validators import RegexValidator, MinLengthValidator, MaxLengthValidator


class RegisterSerializer(serializers.ModelSerializer):
    goal_weight = serializers.DecimalField(min_value = Decimal(1), max_digits=5, decimal_places=2)
    password = serializers.CharField(write_only = True, validators = [
        RegexValidator(
            regex = r'^(?=(?:.*\d){3,}).+$',
            message = "You have to include at least 3 numbers"
        ),
        MinLengthValidator(
            limit_value = 8,
            message = "Your password has to be at least 8 characters long"
        ),
        MaxLengthValidator(
            limit_value = 50,
            message = "Your password can't be more than 50 characters"
        )

    ])
    class Meta:
        model = User
        fields = [
            'username',
            'password',
            'goal_weight'
        ]




class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Exercise
        fields = "__all__"


class AddWorkoutSerializer(serializers.ModelSerializer):
    deleted = serializers.BooleanField(read_only = True)
    distance = serializers.DecimalField(min_value = Decimal(1), max_digits=10, decimal_places=2)
    duration = serializers.DecimalField(min_value = 0.3, max_digits=4, decimal_places=2)
    class Meta:
        model = models.Workoutplan
        fields = [
            'weekday',
            'exercise',
            'reps',
            'sets',
            'distance',
            'duration',
            'priority',
            'deleted'
        ]

    def validate(self, data):
        user = self.context.get('request').user
        weekday = data.get('weekday')
        last_priority_workout = models.Workoutplan.objects.filter(user = user, priority = int(data.get('priority'))-1, weekday = weekday)
        if data.get('priority') != 1 and not last_priority_workout:
            raise ValidationError({'priority' : "You can't skip a number in order"})
        if not data.get('reps') and not data.get('sets') and not data.get('distance') and not data.get('duration'):
            raise ValidationError({'workout' : "You must include either reps, sets, distance or duration"})
        if not data.get('reps') and not data.get('sets'):
             raise ValidationError({'workout' : "You must include sets if you include reps"})
        return data
    

class DeleteWorkoutSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Workoutplan
        fields = [
            'weekday',
            'exercise',
            'reps',
            'sets',
            'distance',
            'duration',
            'priority',
            'deleted'
        ]



class WeightEntrySerializer(serializers.ModelSerializer):
    weight = serializers.DecimalField(min_value=Decimal(1), max_digits=5, decimal_places=2)
    date = serializers.DateField(read_only = True)
    class Meta:
        model = models.WeightEntry
        fields = [
            'weight',
            'date'
        ]

class GoalWeightSerializer(serializers.ModelSerializer):
    goal_weight = serializers.DecimalField(min_value = Decimal(1), max_digits=5, decimal_places=2)
    class Meta:
        model = models.GoalWeight
        fields = [
            'goal_weight'
        ]