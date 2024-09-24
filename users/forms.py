from django.contrib.auth.forms import UserCreationForm, PasswordResetForm, UserChangeForm
from django import forms
from catalog.forms import StyleFormMixin
from users.models import User


class UserRegisterForm(StyleFormMixin, UserCreationForm):
    """
    Форма для регистрации пользователя
    """

    class Meta:
        model = User
        fields = ('email', 'password1', 'password2',)


class UserPasswordResetForm(StyleFormMixin, PasswordResetForm):
    """
    Форма для сброса пароля
    """

    class Meta:
        model = User
        fields = ('email',)


class UserProfileForm(StyleFormMixin, UserChangeForm):
    """
    Форма для редактирования профиля пользователя
    """
    model = User
    fields = ('email', 'first_name', 'last_name', 'phone', 'avatar', 'country')

    def __init__(self, *args, **kwargs):
        """
        Исключаем поле "пароль" из формы
        """
        super().__init__(*args, **kwargs)

        self.fields['password'].widget = forms.HiddenInput()
