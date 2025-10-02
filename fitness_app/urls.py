from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView,TokenRefreshView
from . import views


urlpatterns = [
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/register/', views.RegisterApiView.as_view()),
    path('api/log_out/', views.LogoutApiView.as_view()),
    path('api/addexercise/', views.CreateExercisesApiView.as_view()),
    path('api/listexercise/', views.ListExercisesApiView.as_view()),
    path('api/deleteexercise/<int:pk>', views.DeleteExerrcisesApiView.as_view())
]