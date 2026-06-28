from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.permissions import AllowAny
from rest_framework.authtoken.models import Token
from django.contrib.auth.models import User
from .models import Board
from .serializers import RegistrationSerializer, BoardSerializer
from django.db.models import Q

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