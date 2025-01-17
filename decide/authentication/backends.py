from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend
from django.db.models import Q


class EmailOrUsernameModelBackend(ModelBackend):

    def authenticate(self, request, username=None, password=None, **kwargs):
        auth_type = settings.AUTH_AUTHENTICATION_TYPE
        if auth_type == 'username':
            return super().authenticate(username, password)
        user_model = get_user_model()
        try:
            if auth_type == 'both':
                user = user_model.objects.get(
                    Q(username__iexact=username) | Q(email__iexact=username)
                )
            else:
                user = user_model.objects.get(email__iexact=username)
            if user.check_password(password):
                return user
        except user_model.DoesNotExist:
            return None