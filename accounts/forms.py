from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from .models import User


class UniqueEmailMixin:
    def clean_email(self):
        email = self.cleaned_data["email"].strip()
        qs = User.objects.filter(email__iexact=email)
        if self.instance and self.instance.pk:
            qs = qs.exclude(pk=self.instance.pk)
        if qs.exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email


class RegisterForm(UniqueEmailMixin, UserCreationForm):
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ("username", "first_name", "last_name", "email")


class LoginForm(AuthenticationForm):
    error_messages = {
        "invalid_login": "Invalid username or password. Please try again.",
        "inactive": "This account is inactive.",
    }


class ProfileForm(UniqueEmailMixin, forms.ModelForm):
    class Meta:
        model = User
        fields = ("first_name", "last_name", "email", "phone", "photo")
