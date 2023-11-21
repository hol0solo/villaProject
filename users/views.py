from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView, UpdateView

from mixins.views import TitleMixin
from users.forms import UserLoginForm, UserProfileForm, UserRegistrationForm
from users.models import EmailVerification, User


class UserLoginView(TitleMixin, LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    title = 'Login'


class UserRegistrationView(TitleMixin, CreateView):
    template_name = 'users/registration.html'
    success_url = reverse_lazy('users:login')
    model = User
    form_class = UserRegistrationForm
    title = 'Registration'


class UserProfileView(TitleMixin, LoginRequiredMixin, UpdateView):
    model = User
    form_class = UserProfileForm
    template_name = 'villa/profile.html'
    title = 'Profile'

    def get_success_url(self):
        return reverse_lazy('users:profile', args=(self.object.id,))


class EmailVerificationView(TitleMixin, TemplateView):
    title = 'Подтверждение почты'
    template_name = 'users/email.html'

    def get(self, request, *args, **kwargs):
        code = kwargs['code']
        email = kwargs['email']
        user = User.objects.get(email=email)
        link = EmailVerification.objects.filter(code=code, user=user)
        if link.exists():
            user.is_verified = True
            user.save()
            return super(EmailVerificationView, self).get(request, *args, **kwargs)
        else:
            return reverse_lazy('index')
