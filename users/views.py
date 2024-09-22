import secrets
from django.views.generic import CreateView

from config.settings import EMAIL_HOST_USER
from users.forms import UserRegisterForm
from users.models import User
from django.urls import reverse_lazy, reverse
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404, redirect, render


class UserCreateView(CreateView):
    """
    Контроллер для регистрации пользователя
    """
    model = User
    form_class = UserRegisterForm
    success_url = reverse_lazy('users:login')

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
        url = f'http://{host}/user/email-confirm/{token}/'
        send_mail(
            subject='Подтверждение почты',
            message=f'Перейдите по ссылке для подтверждения почты {url}',
            from_email=EMAIL_HOST_USER,
            recipient_list=[user.email],
        )
        print(f'token_valid: {token}')
        print(f'url_valid: {url}')
        return super().form_valid(form)


def email_verification(request, token):
    """
    Проверка перехода по ссылке
    """
    user = get_object_or_404(User, token=token)
    user.is_active = True
    user.save()
    return redirect(reverse('users:login'))

