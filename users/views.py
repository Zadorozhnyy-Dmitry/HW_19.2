from django.views.generic import CreateView
from users.forms import UserRegisterForm
from users.models import User
from django.urls import reverse_lazy


class RegisterView(CreateView):
    """
    Контроллер для регистрации пользователя
    """
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'
    success_url = reverse_lazy('users:login')
