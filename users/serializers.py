from rest_framework import serializers
from django.contrib.auth.forms import _unicode_ci_compare
from django.contrib.auth.models import (
    Group,
    User,
)
from django.contrib.auth import _clean_credentials
from django.contrib.auth.signals import user_login_failed
from django.db.models import Q
from rest_framework.validators import UniqueValidator
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site
from django.core.mail import EmailMultiAlternatives
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode

UserModel = get_user_model()


class LoginSerializer(serializers.Serializer):
    """!
    Clase para el login en el sistema

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    username = serializers.CharField(label='Username')
    password = serializers.CharField(
        label='Password', style={'input_type': 'password'}
    )

    def validate(self, attrs):
        """!
        Meethod for validated of return serializer is correct

        @param attrs object with field for validate
        @return attrs object that contain the serializer validated
        """

        username = attrs.get('username')
        password = attrs.get('password')
        msg = None
        if username and password:
            user = User.objects.filter(
                Q(username__iexact=username) | Q(email__iexact=username)
            ).distinct()
            credentials = {'username': username, 'password': password}

            if user:
                user = user.first()
                if user.check_password(password):
                    if not user.is_active:
                        msg = 'User not active!'
                else:
                    msg = 'Invalid the password!'
            else:
                msg = 'Invalid credentials!'
        else:
            msg = "Must include 'username' and 'password'."
        if msg:
            user_login_failed.send(
                sender=__name__,
                credentials=_clean_credentials(credentials),
                request=None,
                msg=msg,
            )
            raise serializers.ValidationError(msg)
        attrs['user'] = user
        return attrs


class RegisterSerializer(serializers.ModelSerializer):
    """!
    Clase que registra a usuarios

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        """!
        Meta clase del modelo que establece algunas propiedades

        @author William Páez (paez.william8 at gmail.com)
        """

        model = User
        fields = ('username', 'password', 'password2', 'email',)

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': "Password fields didn't match."}
            )
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
        )
        user.set_password(validated_data['password'])
        user.save()
        # Se asigna el rol Usuario
        user.groups.add(Group.objects.get(name='Usuario'))
        # Token.objects.create(user=user)
        return user


class PasswordChangeSerializer(serializers.ModelSerializer):
    """!
    Clase que permite actualizar la contraseña

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    password = serializers.CharField(
        write_only=True, required=True, validators=[validate_password]
    )
    password2 = serializers.CharField(write_only=True, required=True)
    old_password = serializers.CharField(write_only=True, required=True)

    class Meta:
        """!
        Meta clase del modelo que establece algunas propiedades
        
        @author William Páez (paez.william8 at gmail.com)
        """

        model = User
        fields = ('old_password', 'password', 'password2')

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError(
                {'password': "Password fields didn't match."}
            )
        return attrs

    def validate_old_password(self, value):
        user = self.context['user']
        if not user.check_password(value):
            raise serializers.ValidationError(
                {'old_password': 'Old password is not correct'}
            )
        return value

    def update(self, instance, validated_data):
        instance.set_password(validated_data['password'])
        instance.save()
        return instance


class UserUpdateSerializer(serializers.ModelSerializer):
    """!
    Clase que permite actualizar usuario

    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    email = serializers.EmailField(required=True)

    class Meta:
        """!
        Meta clase del modelo que establece algunas propiedades
        
        @author William Páez (paez.william8 at gmail.com)
        """

        model = User
        fields = ('username', 'first_name', 'last_name', 'email')
        extra_kwargs = {
            'first_name': {'required': True},
            'last_name': {'required': True},
        }

    def validate_email(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(email=value).exists():
            raise serializers.ValidationError(
                {'email': 'This email is already in use.'}
            )
        return value

    def validate_username(self, value):
        user = self.context['request'].user
        if User.objects.exclude(pk=user.pk).filter(username=value).exists():
            raise serializers.ValidationError(
                {'username': 'This username is already in use.'}
            )
        return value

    def update(self, instance, validated_data):
        user = self.context['request'].user
        if user.pk != instance.pk:
            raise serializers.ValidationError(
                {'authorize': "You don't have permission for this user."}
            )
        instance.first_name = validated_data['first_name']
        instance.last_name = validated_data['last_name']
        instance.email = validated_data['email']
        instance.username = validated_data['username']
        instance.save()
        return instance


class UserSerializer(serializers.ModelSerializer):
    """!
    Clase que muestra los campos del usuario
    
    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    class Meta:
        model = User
        fields = ('pk', 'first_name', 'last_name', 'username', 'email')


class PasswordResetSerializer(serializers.Serializer):
    """!
    Clase que muestra los campos del usuario
    
    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    email = serializers.EmailField(required=True)

    def send_mail(
        self,
        subject_template_name,
        email_template_name,
        context,
        from_email,
        to_email,
        html_email_template_name=None,
    ):
        """!
        Método que envía un correo
        
        @author William Páez (paez.william8 at gmail.com)
        """

        subject = loader.render_to_string(subject_template_name, context)
        # Email subject *must not* contain newlines
        subject = "".join(subject.splitlines())
        body = loader.render_to_string(email_template_name, context)

        email_message = EmailMultiAlternatives(subject, body, from_email, [to_email])
        if html_email_template_name is not None:
            html_email = loader.render_to_string(html_email_template_name, context)
            email_message.attach_alternative(html_email, "text/html")

        email_message.send()

    def get_users(self, email):
        """!
        Método que al recibir un correo electrónico, devuelva los usuarios
        coincidentes que deberían recibir un reinicio
        
        @author William Páez (paez.william8 at gmail.com)
        """
        email_field_name = UserModel.get_email_field_name()
        active_users = UserModel._default_manager.filter(
            **{
                "%s__iexact" % email_field_name: email,
                "is_active": True,
            }
        )
        return (
            u
            for u in active_users
            if u.has_usable_password()
            and _unicode_ci_compare(email, getattr(u, email_field_name))
        )

    def create(self, validated_data):
        """!
        Metodo que genera una url de un solo uso y lo envía al usuario
        
        @author William Páez (paez.william8 at gmail.com)
        """

        email = self.validated_data['email']
        from_email = None
        token_generator = default_token_generator
        email_template_name = 'users/password_reset_email.html'
        subject_template_name = 'users/password_reset_subject.txt'
        html_email_template_name = None
        extra_email_context = None
        use_https = self.context['request'].is_secure()
        current_site = get_current_site(self.context['request'])
        site_name = current_site.name
        domain = current_site.domain
        email_field_name = UserModel.get_email_field_name()
        for user in self.get_users(email):
            user_email = getattr(user, email_field_name)
            context = {
                "email": user_email,
                "domain": domain,
                "site_name": site_name,
                "uid": urlsafe_base64_encode(force_bytes(user.pk)),
                "user": user,
                "token": token_generator.make_token(user),
                "protocol": "https" if use_https else "http",
                **(extra_email_context or {}),
            }
            self.send_mail(
                subject_template_name,
                email_template_name,
                context,
                from_email,
                user_email,
                html_email_template_name=html_email_template_name,
            )
        return email


class SetPasswordSerializer(serializers.Serializer):
    """!
    Clase que muestra los campos del usuario
    
    @author William Páez (paez.william8 at gmail.com)
    @copyright <a href='http://www.gnu.org/licenses/gpl-2.0.html'>
        GNU Public License versión 2 (GPLv2)</a>
    """

    new_password1 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True
    )

    new_password2 = serializers.CharField(
        style={'input_type': 'password'}, write_only=True
    )

    def validate(self, attrs):
        new_password1 = attrs.get('new_password1')
        new_password2 = attrs.get('new_password2')
        if new_password1 != new_password2:
            raise serializers.ValidationError('Password not match')
        return attrs

    def create(self, validated_data):
        user = self.context['user']
        user.set_password(validated_data['new_password1'])
        user.save()
        return user
