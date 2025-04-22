from rest_framework import status, permissions, generics
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .serializers import UserRegistrationSerializer, LoginSerializer, UserInfoSerializer, UserUpdateSerializer
from django.http import JsonResponse
from rest_framework.generics import UpdateAPIView
from django.contrib.auth import get_user_model
from drf_spectacular.utils import extend_schema, OpenApiExample


User = get_user_model()

class SignupView(APIView):
    permission_classes = [permissions.AllowAny]
    @extend_schema(
        request=UserRegistrationSerializer,
        responses={201: UserRegistrationSerializer},
         examples=[
            OpenApiExample(
                'Signup Example',
                value={
                    "email": "test@example.com",
                    "password": "strongpassword123",
                    "user_type": "regular",
                },
                request_only=True,
            ),
        ],
    )


    def post(self, request):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            
            return Response({
                'user': {
                    'email': user.email,
                    'user_type': user.user_type,
                },
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    permission_classes = [permissions.AllowAny]
    @extend_schema(
        request=LoginSerializer,
        responses={200: UserInfoSerializer},
        examples=[
            OpenApiExample(
                'Login Example',
                value={
                    "email": "test@example.com",
                    "password": "strongpassword123",
                },
                request_only=True,
            ),
        ],
    )
 
    
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        request=LoginSerializer,
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password = serializer.validated_data['password']
            
            user = authenticate(email=email, password=password)
            
            if user:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'user': {
                        'email': user.email,
                        'user_type': user.user_type,
                    },
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                })
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def status_view(request):
    return JsonResponse({"status": "working"})

class UserInfoView(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserInfoSerializer

    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        user = self.request.user
        lookup_user_id = self.kwargs["pk"]

        # Admins can view anyone. Users can view themselves.
        if user.is_staff or str(user.id) == lookup_user_id:
            return User.objects.get(pk=lookup_user_id)
        else:
            from rest_framework.exceptions import PermissionDenied
            raise PermissionDenied("You are not allowed to view this information.")

class MeView(generics.RetrieveAPIView):
    serializer_class = UserInfoSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

class UpdateUserView(UpdateAPIView):
    serializer_class = UserUpdateSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user  # The user is updated based on the authenticated request

