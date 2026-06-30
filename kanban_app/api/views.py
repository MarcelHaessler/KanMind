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
    serializer_class = BoardSerializer

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(Q(owner=user) | Q(members=user)).distinct()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    permission_classes = [IsOwnerOrMember]

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return BoardUpdateSerializer
        return BoardDetailSerializer


class AssignedToMeView(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(assignee=self.request.user)


class ReviewingView(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(reviewer=self.request.user)


class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsAuthenticated, CanCreateTaskInBoard]

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsTaskEditorOrDeleter]


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [IsBoardMember]

    def get_queryset(self):
        return Comment.objects.filter(task_id=self.kwargs['task_id'])

    def perform_create(self, serializer):
        task = Task.objects.get(id=self.kwargs['task_id'])
        serializer.save(author=self.request.user, task=task)


class CommentDeleteView(generics.DestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCommentAuthor]
    lookup_url_kwarg = 'comment_id'
