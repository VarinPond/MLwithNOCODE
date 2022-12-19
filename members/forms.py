from django import forms
from django.contrib.auth import password_validation, get_user_model
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from django.utils.text import capfirst

UserModel = get_user_model()


class UserRegisterForm(forms.ModelForm):
    error_messages = {
        "password_mismatch": _("The two password fields didn’t match."),
    }

    username = forms.CharField(
        required=True,
        max_length=25,
        label="Username",
        widget=forms.TextInput(attrs={'placeholder': 'username'}),)
    email = forms.EmailField(
        required=True,
        max_length=100,
        label="Email",
        widget=forms.EmailInput(attrs={'placeholder': 'email'}))
    password1 = forms.CharField(
        required=True,
        max_length=30,
        label="Password",
        widget=forms.PasswordInput(attrs={'placeholder': 'password'}),
        help_text=password_validation.password_validators_help_text_html())
    password2 = forms.CharField(
        required=True,
        max_length=30,
        label="Re-password",
        widget=forms.PasswordInput(
            attrs={'placeholder': 'password confirmation'}),
        help_text=_("Enter the same password as before, for verification."))
    is_superuser = forms.BooleanField(
        widget=forms.HiddenInput(),
        required=False,
        initial=False)

    class Meta:
        model = User
        fields = ['username', 'email', 'password1',
                  'password2', 'is_superuser']

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages["password_mismatch"],
                code="password_mismatch",
            )
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
