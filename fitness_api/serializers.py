from rest_framework import serializers
from fitness_app import models
from rest_framework.exceptions import ValidationError


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Exercise
        fields = "__all__"


class AddWorkoutSerializer(serializers.ModelSerializer):
    deleted = serializers.BooleanField(read_only = True)
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