from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser


class CustomUserCreationForm(UserCreationForm):
    """
    This class is used to customise the form for the CustomUser model.
    """

    class Meta:
        model = CustomUser
        fields = ('username', 'email')


class CustomUserChangeForm(UserChangeForm):
    """
    This class is used to customize the form for the CustomUser model.
    """

    class Meta:
        model = CustomUser
        fields = ('username', 'email')
