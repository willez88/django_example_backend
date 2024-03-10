from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
from django.utils.http import urlsafe_base64_decode
from rest_framework_simplejwt.tokens import RefreshToken

UserModel = get_user_model()


def JwtToken(user=None):
    token = RefreshToken.for_user(user)
    return {
        'refresh': str(token),
        'token': str(token.access_token),
        'id': user.pk
    }

def get_user(uidb64):
        try:
            # urlsafe_base64_decode() decodes to bytestring
            uid = urlsafe_base64_decode(uidb64).decode()
            user = UserModel._default_manager.get(pk=uid)
        except (
            TypeError,
            ValueError,
            OverflowError,
            UserModel.DoesNotExist,
            ValidationError,
        ):
            user = None
        return user