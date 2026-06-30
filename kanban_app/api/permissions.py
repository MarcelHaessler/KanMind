from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404

from ..models import Task, Board


class IsOwnerOrMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        is_owner = request.user == obj.owner
        is_member = request.user in obj.members.all()

        if request.method == 'DELETE':
            return is_owner
        return is_owner or is_member


class CanCreateTaskInBoard(BasePermission):
    def has_permission(self, request, view):
        board_id = request.data.get('board')
        if not board_id:
            return True
        board = get_object_or_404(Board, id=board_id)
        return request.user == board.owner or request.user in board.members.all()


class IsTaskEditorOrDeleter(BasePermission):
    def has_object_permission(self, request, view, obj):
        board = obj.board
        is_member = request.user == board.owner or request.user in board.members.all()

        if request.method == 'DELETE':
            return request.user == obj.created_by or request.user == board.owner
        return is_member


class IsCommentAuthor(BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsBoardMember(BasePermission):
    def has_permission(self, request, view):
        task = get_object_or_404(Task, id=view.kwargs['task_id'])
        board = task.board
        return request.user == board.owner or request.user in board.members.all()
