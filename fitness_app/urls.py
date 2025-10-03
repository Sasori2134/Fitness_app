from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from . import views


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', views.RegisterApiView.as_view()),
    path('api/log_out/', views.LogoutApiView.as_view()),
    path('api/add_exercise/', views.CreateExercisesApiView.as_view()),
    path('api/list_exercise/', views.ListExercisesApiView.as_view()),
    path('api/delete_exercise/<int:pk>', views.DeleteExercisesApiView.as_view()),
    path('api/add_workout/', views.AddWorkoutApiView.as_view()),
    path('api/delete_workout/<int:pk>', views.DeleteWorkoutApiView.as_view()),
    path('api/list_workouts_for_today/', views.ListWorkoutsForTodayApiView.as_view()),
    path('api/complete_exercise/<int:pk>', views.CompleteExerciseTodayApiView.as_view()),
    path('api/update_workout/<int:pk>', views.UpdateWorkoutApiView.as_view()),
    path('api/weight_entry_listing/', views.WeightEntryApiView.as_view()),
    path('api/delete_weight_entry/', views.DeleteWeightEntryApiView.as_view()),
    path('api/update_retrieve_goal_weight/<int:pk>', views.RetrieveUpdateGoalWeightApiView.as_view())
]