import secrets
from django.views.generic import CreateView, TemplateView, UpdateView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.forms import PasswordResetForm


class UserCreateView(CreateView):
    """
    Контроллер для регистрации пользователя
    """

    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        """
        Верификация почты пользователя через отправленное письмо
        """
        user = form.save()
        user.is_active = False
        token = secrets.token_hex(16)
        user.token = token
        user.save()
        host = self.request.get_host()
        url = f"http://{host}/users/email-confirm/{token}/"
        send_mail(
            subject="Подтверждение почты",
            message=f"Перейдите по ссылке для подтверждения почты {url}",
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        return super().form_valid(form)


def email_verification(request, token):
    """
    Проверка перехода по ссылке
    """
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse("users:login"))


class UserPasswordResetView(PasswordResetView):
    """
    Контроллер для восстановления пароля
    """

    template_name = "users/password_reset_form.html"
    form_class = PasswordResetForm
    success_url = reverse_lazy("users:login")

    def form_valid(self, form):
        email = form.cleaned_data["email"]
        try:
            user = User.objects.get(email=email)
            if user:
                password = User.objects.make_random_password(length=10)
                user.set_password(password)
                user.save()
                send_mail(
                    subject="Сброс пароля",
                    message=f" Ваш новый пароль {password}",
                    from_email=EMAIL_HOST_USER,
                    recipient_list=[user.email],
                )
            return redirect(reverse("users:login"))
        except:
            return redirect(reverse("users:invalid_email"))


class UserInValidEmail(TemplateView):
    """
    Контроллер отработки исключения, когда нет пользователя с таким email
    """

    template_name = "users/invalid_email.html"


class ProfileView(UpdateView):
    """
    Контроллер профиля пользователя
    """

    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy("users:profile")

    def get_object(self, queryset=None):
        """
        Передаем идентификатор пользователя
        """
        return self.request.user
