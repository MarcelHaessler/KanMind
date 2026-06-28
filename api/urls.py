from django.urls import path
from .views import RegistrationView, LoginView, BoardListCreateView

urlpatterns = [
    path('registration/', RegistrationView.as_view()),
    path('login/', LoginView.as_view()),
    path('boards/', BoardListCreateView.as_view())
]