from django import forms
from django.contrib.auth.forms import (AuthenticationForm, UserChangeForm,
                                       UserCreationForm)

from users.models import User
from users.tasks import celery_email_verification


class UserLoginForm(AuthenticationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input100', 'placeholder': 'Type your username'
    }))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'input100', 'placeholder': 'Type your password'
    }))

    class Meta:
        model = User
        fields = ['password', 'username']


class UserRegistrationForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input100', 'placeholder': 'Type your username'
    }))
    first_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input100', 'placeholder': 'Type your name'
    }))
    last_name = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'input100', 'placeholder': 'Type your lastname'
    }))
    email = forms.CharField(widget=forms.EmailInput(attrs={
        'class': 'input100', 'placeholder': 'Type your email'
    }))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'input100', 'placeholder': 'Type your password'
    }))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'input100', 'placeholder': 'Confirm your password'
    }))

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'password1', 'password2']

    def save(self, commit=True):
        user = super(UserRegistrationForm, self).save(commit=True)
        celery_email_verification.delay(user.id)
        return user


class UserProfileForm(UserChangeForm):
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4', 'readonly': True}))
    first_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    last_name = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control py-4'}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={'class': 'form-control py-4', 'readonly': True}))
    image = forms.ImageField(widget=forms.FileInput(attrs={'class': 'custom-file-label'}), required=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'image', 'email']
