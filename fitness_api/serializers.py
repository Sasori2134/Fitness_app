from rest_framework.serializers import ModelSerializer
from fitness_app import models
from rest_framework.exceptions import ValidationError


class ExerciseSerializer(ModelSerializer):
    class Meta:
        model = models.Exercise
        fields = "__all__"


class AddWorkoutSerializer(ModelSerializer):
    class Meta:
        model = models.Workoutplan
        fields = "__all__"

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