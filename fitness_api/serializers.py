from rest_framework.serializers import ModelSerializer
from fitness_app import models


class ExerciseSerializer(ModelSerializer):
    class Meta:
        model = models.Exercise
        fields = "__all__"
