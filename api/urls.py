from django.urls import path
from .views import (RegistrationView, LoginView, BoardListCreateView, 
                    BoardDetailView, EmailCheckView, AssignedToMeView, 
                    ReviewingView, TaskCreateView, TaskDetailView, 
                    CommentListCreateView, CommentDeleteView)

urlpatterns = [
    path('registration/', RegistrationView.as_view()),
    path('login/', LoginView.as_view()),
    path('boards/', BoardListCreateView.as_view()),
    path('boards/<int:pk>/', BoardDetailView.as_view()),
    path('email-check/', EmailCheckView.as_view()),
    path('tasks/assigned-to-me/', AssignedToMeView.as_view()),
    path('tasks/reviewing/', ReviewingView.as_view()),
    path('tasks/', TaskCreateView.as_view()),
    path('tasks/<int:pk>/', TaskDetailView.as_view()),
    path('tasks/<int:task_id>/comments/', CommentListCreateView.as_view()),
    path('tasks/<int:task_id>/comments/<int:comment_id>/', CommentDeleteView.as_view()),
]