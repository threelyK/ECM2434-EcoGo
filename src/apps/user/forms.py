from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import get_user_model

from django import forms
from django.forms.widgets import PasswordInput, TextInput

# Registering a user
class CreateUserForm(UserCreationForm):

    class Meta:

        model = get_user_model()

        # The user will have to enter the fields below, password1 and password2 will have to match.
        fields = ['username', 'email', 'password1', 'password2']


# Authenticate a user (Model Form)
class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())