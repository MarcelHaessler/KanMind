from rest_framework.permissions import BasePermission


class IsOwnerOrMember(BasePermission):
    def has_object_permission(self, request, view, obj):
        is_owner = request.user == obj.owner
        is_member = request.user in obj.members.all()

        if request.method == 'DELETE':
            return is_owner
        return is_owner or is_member
    

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