from django.contrib.auth.forms import UserChangeForm as _UserChangeForm
from django.contrib.auth.forms import UserCreationForm as _UserCreationForm
from django.forms import EmailField

from .models import User


class UserCreationForm(_UserCreationForm):
    class Meta(_UserCreationForm.Meta):
        model = User
        fields = ("email", "name")
        field_classes = {"email": EmailField}


class UserChangeForm(_UserChangeForm):
    class Meta:
        model = User
        fields = "__all__"


class RegistrationForm(_UserCreationForm):
    class Meta(_UserCreationForm.Meta):
        model = User
        fields = ("email", "name")
        field_classes = {"email": EmailField}
