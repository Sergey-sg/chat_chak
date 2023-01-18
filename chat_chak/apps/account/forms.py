from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, PasswordChangeForm
from django.contrib.auth import get_user_model


class CustomUserLoginForm(UserCreationForm):
    """Model form for create user"""
    class Meta:
        model = get_user_model()
        fields = ('email', 'password',)


class CustomUserChangeForm(UserChangeForm):
    """Model form for update user"""
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'phone_number', 'address', 'photo', 'img_alt')


class CustomRegistrationForm(UserCreationForm):
    """Model form for create user"""

    class Meta:
        model = get_user_model()
        fields = ('email', 'password1', 'password2')


class UserProfileChangeForm(forms.ModelForm):
    """Model form for update user"""
    class Meta:
        model = get_user_model()
        fields = ('first_name', 'last_name', 'photo')


class PasswordProfileChange(PasswordChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('old_password', 'new_password1', 'new_password2')
