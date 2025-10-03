from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework import generics
from fitness_api import serializers, custom_permissions
from rest_framework.views import APIView
from django.contrib.auth.models import User
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Exercise, Workoutplan, CompletedWorkouts, WeightEntry, GoalWeight
from django.db.models import F
from datetime import datetime
from datetime import date
from django.db.utils import IntegrityError
from django.db import transaction

class RegisterApiView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            serialized = serializers.RegisterSerializer(data = request.data)
            if serialized.is_valid(raise_exception = True):
                with transaction.atomic():
                    user = User.objects.create_user(username = serialized.validated_data.get('username'), password = serialized.validated_data.get('password'))
                    GoalWeight.objects.create(user = user, goal_weight = serialized.validated_data.get('goal_weight'))
            return Response({'message' : 'Register Successful'}, status=201)
        except IntegrityError:
            return Response({'message' : 'This username is already in use'}, status=409)
        


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

    
class UpdateWorkoutApiView(generics.UpdateAPIView):
    permission_classes = [custom_permissions.IsOwner, IsAuthenticated]
    serializer_class = serializers.AddWorkoutSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return Workoutplan.objects.filter(user = self.request.user)
    

class DeleteWorkoutApiView(APIView):
    permission_classes = [custom_permissions.IsOwner,IsAuthenticated]

    def patch(self, request, pk):
        try:
            instance = Workoutplan.objects.get(pk = pk)
        except Workoutplan.DoesNotExist:
            return Response({'message' : 'Workout doesnt exist'})
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


class CompleteExerciseTodayApiView(APIView):
    permission_classes = [custom_permissions.IsOwner ,IsAuthenticated]
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
    

class WeightEntryApiView(generics.ListCreateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = serializers.WeightEntrySerializer

    def perform_create(self, serializer):
        serializer.save(user = self.request.user)


class DeleteWeightEntryApiView(generics.DestroyAPIView):
    permission_classes = [custom_permissions.IsOwner, IsAuthenticated]
    serializer_class = serializers.WeightEntrySerializer

    def get_queryset(self):
        return WeightEntry.objects.filter(user = self.request.user)


class RetrieveUpdateGoalWeightApiView(generics.RetrieveUpdateAPIView):
    permission_classes = [custom_permissions.IsOwner, IsAuthenticated]
    serializer_class = serializers.GoalWeightSerializer
    lookup_field = 'pk'

    def get_queryset(self):
        return GoalWeight.objects.filter(user = self.request.user)


class LogoutApiView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = RefreshToken(request.data.get('refresh_token'))
            refresh_token.blacklist()
        except:
            return Response(status=401)
        return Response(status=200)
