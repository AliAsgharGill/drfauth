from rest_framework.response import Response
from rest_framework import status
from rest_framework.views import APIView
from .serializers import UserRegistrationSerializer, UserLoginSerializer, UserProfileSerializer, UserChangePasswordSerializer, SendResetPasswordEmailSerializer,ForgotPasswordSerializer
from django.contrib.auth import authenticate
from .renderers import UserRenderer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAuthenticated
from .models import User

# for generating tokens for user manually using django rest framework and simplejwt
def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)

    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


class UserRegistrationView(APIView):
     # rendrerer_classes is used to give custom response
    renderer_classes = (UserRenderer,)
    def post(self, request, format=None):
        serializer = UserRegistrationSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            user = serializer.save()
            token = get_tokens_for_user(user)
            return Response( {'token': token, ' ': serializer.data}, status=status.HTTP_201_CREATED) 
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLoginView(APIView):
    # renderer_classes is used to give a custom response
    renderer_classes = (UserRenderer,)

    def post(self, request, format=None):
        serializer = UserLoginSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            email = serializer.data.get('email')
            password = serializer.data.get('password')

            # Check if the user with the provided email exists
            user = User.objects.filter(email=email).first()
            if user is None:
                return Response(
                    {"errors": {'email': ['User with this email does not exist.']}},
                    status=status.HTTP_400_BAD_REQUEST
                )

            # Check if the password is correct
            user = authenticate(email=email, password=password)
            if user is not None:
                token = get_tokens_for_user(user)
                return Response({"message": "Login Success", 'token': token}, status=status.HTTP_200_OK)

            # If password is incorrect
            return Response(
                {"errors": {'password': ['Invalid password.']}},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    # rendrerer_classes is used to give custom response
    renderer_classes = (UserRenderer,)
    # to show exact error when user is not authenticated, so user need to provide access token to get access to this view.
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        serializer = UserProfileSerializer(request.user)
        return Response(serializer.data)
    

class UserChangePasswordView(APIView):
    renderer_classes = (UserRenderer,)
    permission_classes = [IsAuthenticated]
    def post(self, request, format=None):
        serializer = UserChangePasswordSerializer(data=request.data, context={'user': request.user})
        if serializer.is_valid(raise_exception=True):
            return Response({"message": "Password changed successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST) 
    
class SendResetPasswordEmailView(APIView):
    renderer_classes = [UserRenderer]
    def get(self, request, format=None):
        serializer = SendResetPasswordEmailSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            return Response({"message": "Password reset link send. Please check your email"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ForgotPasswordView(APIView):
    renderer_classes = [UserRenderer]
    def post(self, request, uid, token, format=None):
        serializer = ForgotPasswordSerializer(data=request.data, context={'uid': uid, 'token': token})
        if serializer.is_valid(raise_exception=True):
            return Response({"message": "Password reset successfully"}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)