from rest_framework import viewsets, permissions, status, generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import action
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.utils.translation import gettext_lazy as _
from .serializers import (
    UserSerializer, UserProfileSerializer,
    ChangePasswordSerializer, LoginSerializer
)

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    """ViewSet for viewing and editing User instances."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAdminUser]

    def get_queryset(self):
        """Return objects for the current authenticated user only."""
        queryset = self.queryset
        if not self.request.user.is_staff:
            queryset = queryset.filter(id=self.request.user.id)
        return queryset

    @action(detail=False, methods=['get'], permission_classes=[permissions.IsAuthenticated])
    def me(self, request):
        """Return the authenticated user."""
        serializer = self.get_serializer(request.user)
        return Response(serializer.data)

class LoginView(APIView):
    """API view for user login."""
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        """Handle GET requests for user login."""
        return Response({'message': _('Please login with POST request')})

    def post(self, request):
        """Handle POST requests for user login."""
        print("Login request data:", request.data)
        
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            phone_number = serializer.validated_data['phone_number']
            password = serializer.validated_data['password']
            
            # بررسی وجود کاربر
            try:
                user_exists = User.objects.filter(phone_number=phone_number).exists()
                if not user_exists:
                    print(f"User with phone_number {phone_number} does not exist")
                    return Response(
                        {'error': _('کاربری با این شماره تلفن یافت نشد')},
                        status=status.HTTP_401_UNAUTHORIZED
                    )
            except Exception as e:
                print(f"Error checking user: {e}")
            
            # احراز هویت کاربر
            user = authenticate(phone_number=phone_number, password=password)
            
            if user:
                # ثبت ورود کاربر
                login(request, user)
                
                # ایجاد یا بازیابی توکن
                token, created = Token.objects.get_or_create(user=user)
                
                print(f"Login successful for user: {phone_number}, token: {token.key}")
                
                # ارسال پاسخ موفقیت‌آمیز
                return Response({
                    'message': _('Login successful'),
                    'token': token.key,
                    'user': UserSerializer(user).data
                })
            else:
                # دیباگ در صورت شکست احراز هویت
                print(f"Authentication failed for phone_number: {phone_number}")
                return Response(
                    {'error': _('نام کاربری یا رمز عبور اشتباه است')},
                    status=status.HTTP_401_UNAUTHORIZED
                )
        
        print("Validation errors:", serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(APIView):
    """API view for user logout."""
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        """Handle POST requests for user logout."""
        # حذف توکن کاربر
        try:
            request.user.auth_token.delete()
        except (AttributeError, Token.DoesNotExist):
            pass
        
        logout(request)
        return Response({'message': _('Logout successful')})

    def get(self, request):
        """Handle GET requests for user logout."""
        # حذف توکن کاربر
        try:
            request.user.auth_token.delete()
        except (AttributeError, Token.DoesNotExist):
            pass
            
        logout(request)
        return Response({'message': _('Logout successful')})

class UserProfileView(generics.RetrieveUpdateAPIView):
    """API view for retrieving and updating user profile."""
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Return the authenticated user."""
        return self.request.user

class ChangePasswordView(generics.UpdateAPIView):
    """API view for changing password."""
    serializer_class = ChangePasswordSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        """Return the authenticated user."""
        return self.request.user

    def update(self, request, *args, **kwargs):
        """Handle PUT requests for changing password."""
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = self.get_object()
            user.set_password(serializer.validated_data['new_password'])
            user.save()
            return Response({'message': _('Password changed successfully')})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
