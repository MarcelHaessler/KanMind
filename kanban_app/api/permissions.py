from rest_framework.permissions import BasePermission
from django.shortcuts import get_object_or_404

from ..models import Task, Board


class IsOwnerOrMember(BasePermission):
    """Custom permission to allow only owners or members of a board to access it."""
    def has_object_permission(self, request, view, obj):
        is_owner = request.user == obj.owner
        is_member = request.user in obj.members.all()

        if request.method == 'DELETE':
            return is_owner
        return is_owner or is_member


class CanCreateTaskInBoard(BasePermission):
    """Custom permission to allow only owners or members of a board to create tasks in it."""
    def has_permission(self, request, view):
        board_id = request.data.get('board')
        if not board_id:
            return True
        board = get_object_or_404(Board, id=board_id)
        return request.user == board.owner or request.user in board.members.all()


class IsTaskEditorOrDeleter(BasePermission):
    """Board members may edit a task; only its creator or the board owner may delete it."""
    def has_object_permission(self, request, view, obj):
        board = obj.board
        is_member = request.user == board.owner or request.user in board.members.all()

        if request.method == 'DELETE':
            return request.user == obj.created_by or request.user == board.owner
        return is_member


class IsCommentAuthor(BasePermission):
    """Custom permission to allow only the author of a comment to edit or delete it."""
    def has_object_permission(self, request, view, obj):
        return obj.author == request.user


class IsBoardMember(BasePermission):
    """Custom permission to allow only members of a board to access its tasks."""
    def has_permission(self, request, view):
        task = get_object_or_404(Task, id=view.kwargs['task_id'])
        board = task.board
        return request.user == board.owner or request.user in board.members.all()
