from django.urls import path 
from rest_framework_simplejwt.views import TokenRefreshView
from . import views 

urlpatterns = [
    path('refresh/', TokenRefreshView.as_view()),
    path('register/', views.RegistrationView.as_view(), name='register'),
    path('activate/', views.ActivationView.as_view()),
    path('login/', views.LoginView.as_view()),
]
