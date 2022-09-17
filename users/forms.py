from django.contrib.auth.forms import (
    UserChangeForm as _UserChangeForm,
    UserCreationForm as _UserCreationForm,
)

from .models import User


class UserCreationForm(_UserCreationForm):
    class Meta:
        model = User
        fields = ("email",)


class UserChangeForm(_UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"
