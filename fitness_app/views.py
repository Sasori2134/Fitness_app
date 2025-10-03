from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import generics
from fitness_api import serializers, custom_permissions
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Exercise, Workoutplan, CompletedWorkouts
from django.db.models import F
from datetime import datetime
from datetime import date

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


class AddWorkoutApiView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.AddWorkoutSerializer

    
    def perform_create(self, serializer):
        workouts = Workoutplan.objects.filter(user = self.request.user, weekday = serializer.validated_data.get("weekday"), priority__gte = serializer.validated_data.get('priority')).update(priority = F("priority") + 1)
        serializer.save(user = self.request.user)

    
class DeleteWorkoutApiView(APIView):
    permission_classes = [custom_permissions.IsOwner,IsAuthenticated]

    def patch(self, request, pk):
        instance = Workoutplan.objects.get(pk = pk)
        serialized = serializers.DeleteWorkoutSerializer(instance, data = {'deleted' : True}, partial = True)
        if serialized.is_valid(raise_exception=True):
            serialized.save()
        Workoutplan.objects.filter(user = request.user, weekday = instance.weekday, deleted = False, priority__gt = instance.priority).update(priority = F("priority") -1)
        return Response(status=200)
        

class ListWorkoutsForTodayApiView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.AddWorkoutSerializer
    
    def get_queryset(self):
        return Workoutplan.objects.filter(user = self.request.user, deleted = False, weekday = datetime.now().strftime('%A').lower()).order_by('priority')

#Have to check if this workout was done today
class CompleteExerciseTodayApiView(APIView):
    def post(self, request, pk):
        try:
            completed_workout = Workoutplan.objects.get(pk = pk, weekday = datetime.now().strftime('%A').lower())
        except Workoutplan.DoesNotExist:
            return Response({'message' : "Exercise not found"}, status=404)
        completed_workouts_today = CompletedWorkouts.objects.filter(user = request.user, workout = completed_workout, completion_date = date.today()).exists()
        if completed_workout.priority > 1:
            completed_priority_check = CompletedWorkouts.objects.filter(user = request.user, workout__weekday = datetime.now().strftime('%A').lower(), workout__priority = completed_workout.priority - 1).exists() 
            if not completed_priority_check:
                return Response({'message' : "You can't skip Exercises"})

        if not completed_workouts_today:
            CompletedWorkouts.objects.create(user = request.user, workout = completed_workout)
            try:
                next_workout = Workoutplan.objects.get(user = request.user, weekday = completed_workout.weekday, priority = completed_workout.priority + 1)
            except Workoutplan.DoesNotExist:
                return Response({'message' : 'There are no exercises left for today congrats!'})
            serialized = serializers.DeleteWorkoutSerializer(next_workout)
            return Response(serialized.data)
        return Response({'message' : 'You have already completed this exercise'})

class LogoutApiView(APIView):
    permissions_classes = [IsAuthenticated]

    def post(self, request):
        refresh_token = RefreshToken(request.data.get('refresh_token'))
        refresh_token.blacklist()
        return Response(status=200)
