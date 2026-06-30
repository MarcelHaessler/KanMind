from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from django.db.models import Q

from ..models import Board, Task, Comment
from .serializers import (
    BoardSerializer, BoardDetailSerializer, BoardUpdateSerializer,
    TaskSerializer, CommentSerializer,
)
from .permissions import (
    IsOwnerOrMember, IsTaskEditorOrDeleter, IsCommentAuthor,
    IsBoardMember, CanCreateTaskInBoard,
)


class BoardListCreateView(generics.ListCreateAPIView):
    """View to list all boards for the authenticated user and create new boards."""
    serializer_class = BoardSerializer

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(Q(owner=user) | Q(members=user)).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update, or delete a specific board."""
    queryset = Board.objects.all()
    permission_classes = [IsOwnerOrMember]

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return BoardUpdateSerializer
        return BoardDetailSerializer


class AssignedToMeView(generics.ListAPIView):
    """View to list all tasks assigned to the authenticated user."""
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(assignee=self.request.user)


class ReviewingView(generics.ListAPIView):
    """View to list all tasks that the authenticated user is reviewing."""
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(reviewer=self.request.user)


class TaskCreateView(generics.CreateAPIView):
    """View to create a new task in a specific board."""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, CanCreateTaskInBoard]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    """View to retrieve, update, or delete a specific task."""
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsTaskEditorOrDeleter]


class CommentListCreateView(generics.ListCreateAPIView):
    """View to list all comments for a specific task and create new comments."""
    serializer_class = CommentSerializer
    permission_classes = [IsBoardMember]

    def get_queryset(self):
        return Comment.objects.filter(task_id=self.kwargs['task_id'])

    def perform_create(self, serializer):
        task = Task.objects.get(id=self.kwargs['task_id'])
        serializer.save(author=self.request.user, task=task)


class CommentDeleteView(generics.DestroyAPIView):
    """View to delete a specific comment."""
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCommentAuthor]
    lookup_url_kwarg = 'comment_id'
