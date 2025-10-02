from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import generics
from fitness_api import serializers, custom_permissions
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Exercise, Workoutplan
from django.db.models import F

class RegisterApiView(APIView):
    permissions_classes = [AllowAny]

    def post(self, request):
        user = User.objects.create_user(username = request.data.get('username'), password = request.data.get('password'))
        if user:
            return Response(status=201)
        return Response(status=401)


class CreateExercisesApiView(generics.CreateAPIView):
    permission_classes = [IsAdminUser]
    serializer_class = serializers.ExerciseSerializer


class ListExercisesApiView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.ExerciseSerializer
    queryset = Exercise.objects.all()


class DeleteExercisesApiView(generics.DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Exercise.objects.all()


# implement Functionality for users to create tailored workout plans, specifying
# workout frequency, goals, exercise types, and daily session duration
class AddWorkoutApiView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.AddWorkoutSerializer

    
    def perform_create(self, serializer):
        workouts = Workoutplan.objects.filter(user = self.request.user, weekday = serializer.validated_data.get("weekday"), priority__gte = serializer.validated_data.get('priority')).update(priority = F("priority") + 1)
        serializer.save(user = self.request.user)


class DeleteWorkoutApiView(generics.DestroyAPIView):
    permission_classes = [custom_permissions.IsOwner, IsAuthenticated]
    
    def perform_destroy(self, instance):
        priority = instance.priority
        instance.delete()
        Workoutplan.objects.filter(user = self.request.user, weekday = instance.weekday, priority__gt = priority).update(priority = F("priority") -1)

    def get_queryset(self):
        return Workoutplan.objects.filter(user = self.request.user)


class LogoutApiView(APIView):
    permissions_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = RefreshToken(request.data.get('refresh_token'))
        refresh_token.blacklist()
        return Response(status=200)
