from django.contrib.auth.views import LoginView, LogoutView, PasswordResetView, PasswordResetConfirmView, PasswordResetDoneView
from django.urls import reverse_lazy
from django.views.generic import CreateView, TemplateView
from .forms import UserRegisterForm, UserLoginForm, UserPasswordResetForm, UserSetPasswordForm


class CustomLoginView(LoginView):
    form_class = UserLoginForm
    template_name = 'users/login.html'
    redirect_authenticated_user = True
    success_url = reverse_lazy('pages:index')

class CustomLogoutView(LogoutView):
    next_page = reverse_lazy('app_users:login')

class CustomPasswordResetView(PasswordResetView):
    form_class = UserPasswordResetForm
    template_name = 'users/password_reset.html'
    email_template_name = 'password_reset_email.html'
    success_url = reverse_lazy('app_users:password_reset_done')

class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = UserSetPasswordForm
    template_name = 'users/password_reset_confirm.html'
    success_url = reverse_lazy('app_users:password_reset_complete')

class CustomPasswordResetDoneView(PasswordResetDoneView):
    template_name = 'users/password_reset_done.html'

class CustomRegisterView(CreateView):
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('app_users:login')

# class PasswordResetCompleteView(TemplateView):
#     template_name = 'users/password_reset_complete.html'