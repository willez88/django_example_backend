from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from rest_framework import permissions, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from .serializers import (
    LoginSerializer,
    RegisterSerializer,
    PasswordChangeSerializer,
    PasswordResetSerializer,
    SetPasswordSerializer,
    UserSerializer,
)
from .utils import JwtToken, get_user
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.tokens import default_token_generator

from .permissions import CustomObjectPermissions


class UserViewset(viewsets.ModelViewSet):
    """!
    Clase que crea las acciones estandar

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    model = User
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [CustomObjectPermissions,]
    filterset_fields = ('username', 'first_name', 'last_name')

    @action(
        detail=False, methods=['post'], serializer_class=LoginSerializer,
        permission_classes=[permissions.AllowAny]
    )
    def login(self, request):
        """!
        Función que loguea a los usuarios y retorna el token

        @author William Páez (paez.william8 at gmail.com)
        """

        if request.user.is_authenticated:
            return Response(
                {
                    'non_field_errors': ['You are already authenticated']
                },
                status=400
            )
        data = request.data
        username = data.get('username')
        password = data.get('password')
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        user_auth = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user_auth)
        return Response(JwtToken(user), status=201)

    @action(detail=False, methods=['post'], permission_classes=[permissions.IsAuthenticated])
    def logout(self, request):
        """!
        Función que desloguea usuarios

        @author William Páez (paez.william8 at gmail.com)
        """

        try:
            refresh_token = request.data['refresh_token']
            token = RefreshToken(refresh_token)
            token.blacklist()
            return Response(status=status.HTTP_205_RESET_CONTENT)
        except Exception as error:
            print(error)
            return Response(status=status.HTTP_400_BAD_REQUEST)

    @action(
        detail=False, methods=['post'], serializer_class=RegisterSerializer,
        permission_classes=[permissions.AllowAny]
    )
    def register(self, request):
        """!
        Función que registra usuarios

        @author William Páez (paez.william8 at gmail.com)
        """

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    
    @action(
        detail=False, methods=['put'], serializer_class=PasswordChangeSerializer,
        permission_classes=[permissions.IsAuthenticated],
        url_path='password-change',
    )
    def password_change(self, request):
        """!
        Función que permite cambiar la contraseña a usuarios

        @author William Páez (paez.william8 at gmail.com)
        """

        user = request.user
        serializer = self.serializer_class(
            data=request.data,
            context={'user': user}
        )
        serializer.is_valid(raise_exception=True)
        serializer.update(request.user, request.data)
        return Response(status=status.HTTP_200_OK)

    @action(
        detail=False, methods=['post'], serializer_class=PasswordResetSerializer,
        permission_classes=[permissions.AllowAny],
        url_path='reset/password-reset',
    )
    def password_reset(self, request):
        """!
        Función que permite recuperar la contraseña

        @author William Páez (paez.william8 at gmail.com)
        """

        serializer = self.serializer_class(
            data=request.data,
            context={'request': request}
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_200_OK)

    @action(
        detail=False, methods=['post'], serializer_class=SetPasswordSerializer,
        permission_classes=[permissions.AllowAny],
        url_path='reset', url_name='password-reset-confirm'
    )
    def set_password(self, request):
        """!
        Función que permite establecer la nueva contraseña

        @author William Páez (paez.william8 at gmail.com)
        """

        uidb64 = request.GET.get('uidb64')
        token = request.GET.get('token')
        validlink = False
        INTERNAL_RESET_SESSION_TOKEN = "_password_reset_token"
        token_generator = default_token_generator
        if uidb64 is None and token is None:
            raise ImproperlyConfigured(
                "The URL path must contain 'uidb64' and 'token' parameters."
            )
        user = get_user(uidb64)
        if user is not None:
            session_token = request.session[INTERNAL_RESET_SESSION_TOKEN] = token
            if token_generator.check_token(user, session_token):
                # If the token is valid, display the password reset form.
                validlink = True
                serializer = self.serializer_class(
                    data=request.data,
                    context={'user': user}
                )
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({'validlink': validlink}, status=status.HTTP_200_OK)
            else:
                validlink = False
                return Response(
                    {'validlink': validlink}, status=status.HTTP_200_OK
                )
        return Response(status=status.HTTP_200_OK)
