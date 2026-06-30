from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Board
from .serializers import (RegistrationSerializer, BoardSerializer, BoardDetailSerializer, 
                          BoardUpdateSerializer, UserSerializer, TaskSerializer, 
                          CommentSerializer, Comment)
from .permissions import IsOwnerOrMember, IsTaskEditorOrDeleter, IsCommentAuthor
from django.db.models import Q
from .models import Board, Task

class RegistrationView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            token, created = Token.objects.get_or_create(user=user)
            return Response({
                'token': token.key,
                'fullname': user.first_name,
                'email': user.email,
                'user_id': user.id
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')

        # 2. TODO: User über die email suchen.
        #    Was, wenn es die email nicht gibt? -> User.objects.get() wirft dann einen Fehler.
        #    Fang ihn mit try/except User.DoesNotExist ab und gib eine 400-Antwort zurück.
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {"error": "User not found"},                   
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 3. TODO: Passwort prüfen mit user.check_password(password).
        #    Wenn FALSCH -> 400 zurückgeben (gleiche Meldung wie oben ist ok,
        #    aus Sicherheitsgründen sagt man absichtlich nicht, WAS falsch war).
        if not user.check_password(password):
            return Response(
                {"error": "Invalid email or password"},                   
                status=status.HTTP_400_BAD_REQUEST,
            )

        # 4. TODO: Alles korrekt -> Token holen und Antwort bauen.
        #    Schau bei RegistrationView ab: Token.objects.get_or_create(user=user)
        #    und ein Response-Dict mit token / fullname / email / user_id, status 200.
        
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'fullname': user.first_name,
            'email': user.email,
            'user_id': user.id
        }, status=status.HTTP_200_OK)
    

class BoardListCreateView(generics.ListCreateAPIView):
    serializer_class = BoardSerializer

    def get_queryset(self):
        user = self.request.user
        return Board.objects.filter(Q(owner=user) | Q(members=user)).distinct()
    
    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BoardDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Board.objects.all()
    serializer_class = BoardDetailSerializer
    permission_classes = [IsOwnerOrMember]

    def get_serializer_class(self):
        if self.request.method in ['PATCH', 'PUT']:
            return BoardUpdateSerializer
        return BoardDetailSerializer
    

class EmailCheckView(APIView):
    def get(self, request):
        email = request.query_params.get('email')

        if not email:
            return Response({"error": "Email parameter is required."}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            user = User.objects.get(email=email)
            serializer = UserSerializer(user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({"error": "User not found."}, status=status.HTTP_404_NOT_FOUND)
        

class AssignedToMeView(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        user = self.request.user
        return Task.objects.filter(assignee=user)


class ReviewingView(generics.ListAPIView):
    serializer_class = TaskSerializer

    def get_queryset(self):
        return Task.objects.filter(reviewer=self.request.user)
    

class TaskCreateView(generics.CreateAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)


class TaskDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [IsTaskEditorOrDeleter]


class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer

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