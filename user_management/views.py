import logging
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils import timezone
from rest_framework import status
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework.views import APIView
from .serializers import UserCreateSerializer
from django.contrib.auth.models import User
from .models import UserProfile
from .handlers import get_current_host
from rest_framework_simplejwt.tokens import RefreshToken

logger = logging.getLogger(__name__)

class UserRegistrationView(APIView):
    """
    API view to handle user registration.

    Users can register by providing their details. An activation email is sent
    to the user's email address with a link to activate their account.
    """
    permission_classes = [AllowAny]  # Allow access without authentication

    @action(detail=False, methods=['post'])
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for user registration.

        Validates the user input and sends an activation email if the data is valid.
        """
        data = request.data
        serializer = UserCreateSerializer(data=data)

        if serializer.is_valid():
            email = data.get('email')
            username = data.get('username')

            # Check if email already exists in the system
            if not User.objects.filter(email=email).exists():
                # Create a new user and hash the password
                user = User.objects.create(
                    first_name=data['first_name'],
                    last_name=data['last_name'],
                    email=email,
                    username=username,
                    password=make_password(data['password']),
                    is_active=False
                )

                # Generate a random token for email activation
                token = get_random_string(length=32)
                # Create a user profile with the activation token
                profile = UserProfile.objects.create(
                    user=user,
                    activation_token=token,
                    token_created_at=timezone.now()
                )

                try:
                    host_url = get_current_host(request)
                    verification_link = f"{host_url}activate/{token}/"
                    subject = 'Activate Your Account'
                    message = f'Hi {user.first_name},\n\nPlease click the link below to activate your account:\n\n{verification_link}'
                    # Send the activation email
                    send_mail(subject, message, settings.EMAIL_HOST_USER, [email])
                    return Response(
                        {'details': 'Please check your email to activate your account.'},
                        status=status.HTTP_201_CREATED
                    )
                except Exception as e:
                    # Handle errors in sending the email
                    return Response(
                        {'error': f'An error occurred while sending the verification email: {str(e)}'},
                        status=status.HTTP_500_INTERNAL_SERVER_ERROR
                    )
            else:
                return Response(
                    {'error': 'This email already exists!'},
                    status=status.HTTP_400_BAD_REQUEST
                )
        # Return validation errors
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserActivationView(APIView):
    """
    API view to handle user account activation.

    Users activate their accounts using a token sent to their email address.
    """
    permission_classes = [AllowAny]  # Allow access without authentication

    @action(detail=False, methods=['post'])
    def post(self, request, token, *args, **kwargs):
        """
        Handle POST requests for account activation using a token.

        Validates the token and activates the user account if the token is valid.
        """
        try:
            # Retrieve user profile using the activation token
            profile = UserProfile.objects.get(activation_token=token)
        except UserProfile.DoesNotExist:
            return Response({'error': 'Invalid token!'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the activation token has expired
        if profile.is_token_expired():
            return Response({'error': 'Token has expired!'}, status=status.HTTP_400_BAD_REQUEST)

        # Activate the user's account
        user = profile.user
        user.is_active = True
        user.save()
        # Clear the activation token after successful activation
        profile.activation_token = None
        profile.token_created_at = None
        profile.save()

        return Response({'details': 'Your account has been activated successfully!'}, status=status.HTTP_200_OK)


class Login(APIView):
    """
    API view to handle user login.

    Users can log in by providing their email and password. A JWT is returned upon successful login.
    """
    permission_classes = [AllowAny]  # Allow access without authentication

    @action(detail=False, methods=['post'])
    def post(self, request, *args, **kwargs):
        """
        Handle POST requests for user login.

        Authenticates the user and returns a JWT if the credentials are valid.
        """
        data = request.data
        email = data.get('email')
        password = data.get('password')

        if email is None or password is None:
            return Response(
                {'error': 'Please provide both email and password'},
                status=status.HTTP_400_BAD_REQUEST
            )
        try:
            # Check if a user with the given email exists
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response(
                {'error': 'Invalid email or password'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Check if the user's account is activated
        if not user.is_active:
            return Response(
                {'error': 'Your account is not activated yet!'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Authenticate the user
        user = authenticate(request, username=email, password=password)
        if user is None:
            return Response(
                {'error': 'Invalid email or password'},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        # Generate JWT tokens for the authenticated user
        refresh_token = RefreshToken.for_user(user)
        access_token = str(refresh_token.access_token)

        return Response({
            'access_token': access_token,
            'refresh_token': str(refresh_token),
        })
